#!/usr/bin/env python3
"""Convert and compress the repo's images, in place, safely.

Run by .github/workflows/optimise-images.yml on any push that touches an image,
and safe to run by hand:

    python3 -m venv /tmp/imgenv && /tmp/imgenv/bin/pip install pillow
    /tmp/imgenv/bin/python .github/scripts/optimise-images.py          # do it
    /tmp/imgenv/bin/python .github/scripts/optimise-images.py --check  # report only

WHAT IT WILL AND WILL NOT DO

Only team crests get their format or filename changed. They are looked up by
slug with the extension tried in turn, so nothing in the site points at a crest
by path and renaming one cannot break a link. Everything else keeps its exact
filename and format, because `<img src>`, manifest.json and the JSON-LD schema
all reference those paths literally.

Favicons are never resized: manifest.json declares their dimensions, and a
mismatch breaks the install prompt. They only get lossless PNG optimisation.

WHY THERE IS A MANIFEST

Re-encoding a lossy image repeatedly degrades it a little each time. Every
optimised file's hash is recorded in image-manifest.json; a file whose hash
still matches is left alone. Edit or replace an image and the hash changes, so
it gets optimised once more and then settles. Delete the manifest and every
image is re-encoded once, which costs one generation of quality on the JPEGs.
"""
import argparse
import hashlib
import io
import json
import os
import re
import sys

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow is not installed: pip install pillow")

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MANIFEST = os.path.join(ROOT, ".github", "image-manifest.json")

# Anything under these never gets touched.
SKIP_DIRS = {"_site", ".git", ".jekyll-cache", ".vscode", ".opencode", "vendor", "node_modules"}

RASTER = (".png", ".jpg", ".jpeg", ".webp")

# Longest side each folder is allowed, and how to treat it. First match wins,
# so the specific folders have to come before the general ones.
#   crest    convert to webp, lowercase the filename, drop the original
#   lossless never resize, never re-encode lossily
#   normal   cap the longest side, re-encode in the same format
RULES = [
    ("assets/images/teams", 120, "crest"),
    ("assets/favicon", None, "lossless"),
    ("assets/images", 1200, "normal"),
    ("images", 1200, "normal"),
]

# Keep the new file only if it saves at least this much. Stops a pointless
# rewrite (and a pointless commit) when a file is already about as small as it
# is going to get, and stops a lossy re-encode being spent on a rounding error.
MIN_SAVING = 0.05

# Only resize when a file is over its cap by a real margin. A 1270px image
# against a 1200px cap is not worth re-encoding: the 6% saved in pixels can
# easily cost more than it saves, because the original may have been through a
# better PNG compressor than Pillow is.
RESIZE_SLACK = 1.05

JPEG_QUALITY = 82
WEBP_QUALITY = 85


def rule_for(relpath):
    posix = relpath.replace(os.sep, "/")
    for prefix, max_side, mode in RULES:
        if posix.startswith(prefix + "/"):
            return max_side, mode
    return None, None


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(65536), b""):
            h.update(block)
    return h.hexdigest()


def encode(im, fmt):
    """Encode to bytes in the given format, returning the smallest good option."""
    best = None
    attempts = []

    if fmt == "JPEG":
        attempts.append(dict(format="JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True))
    elif fmt == "WEBP":
        attempts.append(dict(format="WEBP", quality=WEBP_QUALITY, method=6))
    elif fmt == "PNG":
        attempts.append(dict(format="PNG", optimize=True))

    for opts in attempts:
        buf = io.BytesIO()
        save = im
        if opts["format"] == "JPEG" and save.mode in ("RGBA", "LA", "P"):
            save = save.convert("RGB")
        save.save(buf, **opts)
        data = buf.getvalue()
        if best is None or len(data) < len(best):
            best = data

    # A PNG with 256 colours or fewer converts to a palette losslessly, which
    # is usually a big win on flat artwork. Anything with more colours is left
    # in truecolour rather than quietly posterised.
    if fmt == "PNG":
        rgba = im.convert("RGBA")
        colours = rgba.getcolors(maxcolors=256)
        if colours is not None:
            buf = io.BytesIO()
            rgba.convert("P", palette=Image.ADAPTIVE, colors=256).save(
                buf, format="PNG", optimize=True)
            data = buf.getvalue()
            if len(data) < len(best):
                best = data

    return best


def process(path, relpath, max_side, mode, apply_changes):
    before = os.path.getsize(path)
    im = Image.open(path)
    im.load()
    fmt = im.format

    target = path
    if mode == "crest":
        slug = re.sub(r"[^a-z0-9]+", "-", os.path.splitext(os.path.basename(relpath))[0].lower()).strip("-")
        target = os.path.join(os.path.dirname(path), slug + ".webp")
        fmt = "WEBP"

    resized = False
    if max_side and max(im.size) > max_side * RESIZE_SLACK:
        im.thumbnail((max_side, max_side), Image.LANCZOS)
        resized = True

    if mode == "lossless" and fmt != "PNG":
        return None  # nothing safe to do to a lossy file we may not resize

    if im.mode == "P" and fmt in ("JPEG", "WEBP"):
        im = im.convert("RGBA" if "transparency" in im.info else "RGB")

    data = encode(im, fmt)
    if data is None:
        return None

    renaming = os.path.abspath(target) != os.path.abspath(path)
    saving = (before - len(data)) / before

    # Never write a bigger file. Resizing does not earn an exception: if the
    # re-encode comes out larger, the original was better compressed than
    # anything we can produce, and taking it would cost quality AND bytes.
    if len(data) >= before and not renaming:
        return None

    # Otherwise take it if it saves something worth having, or if the resize
    # itself was the point.
    if not (saving >= MIN_SAVING or resized or renaming):
        return None

    if apply_changes:
        with open(target, "wb") as fh:
            fh.write(data)
        if renaming:
            os.remove(path)

    return dict(path=relpath, target=os.path.relpath(target, ROOT), before=before,
                after=len(data), resized=resized, renamed=renaming)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true",
                    help="report what would change without writing anything")
    args = ap.parse_args()

    manifest = {}
    if os.path.exists(MANIFEST):
        try:
            manifest = json.load(open(MANIFEST))
        except ValueError:
            manifest = {}

    results = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".git")]
        for name in sorted(filenames):
            if not name.lower().endswith(RASTER):
                continue
            path = os.path.join(dirpath, name)
            relpath = os.path.relpath(path, ROOT)
            max_side, mode = rule_for(relpath)
            if mode is None:
                continue
            # Already optimised and untouched since: leave it alone rather than
            # re-encoding it and losing a generation of quality.
            if manifest.get(relpath.replace(os.sep, "/")) == sha256(path):
                continue
            try:
                r = process(path, relpath, max_side, mode, apply_changes=not args.check)
            except Exception as err:                      # noqa: BLE001
                print("  SKIP  %s (%s)" % (relpath, err))
                continue
            if r:
                results.append(r)
            elif not args.check:
                manifest[relpath.replace(os.sep, "/")] = sha256(path)

    if not results:
        print("Nothing to optimise: every image is already at its target size.")
    else:
        total_before = sum(r["before"] for r in results)
        total_after = sum(r["after"] for r in results)
        print("%-52s %10s %10s %8s" % ("file", "before", "after", "saved"))
        for r in sorted(results, key=lambda x: x["before"] - x["after"], reverse=True):
            note = ""
            if r["renamed"]:
                note = " -> " + os.path.basename(r["target"])
            elif r["resized"]:
                note = " (resized)"
            print("  %-50s %8.1fKB %8.1fKB %6.0f%%%s" % (
                r["path"][:50], r["before"] / 1024, r["after"] / 1024,
                100 * (r["before"] - r["after"]) / r["before"], note))
        print("\n  total %.0fKB -> %.0fKB, saved %.0fKB (%.0f%%)" % (
            total_before / 1024, total_after / 1024,
            (total_before - total_after) / 1024,
            100 * (total_before - total_after) / total_before))

    if not args.check:
        for r in results:
            t = os.path.join(ROOT, r["target"])
            if os.path.exists(t):
                manifest[r["target"].replace(os.sep, "/")] = sha256(t)
            if r["renamed"]:
                manifest.pop(r["path"].replace(os.sep, "/"), None)
        manifest = {k: v for k, v in sorted(manifest.items())
                    if os.path.exists(os.path.join(ROOT, k))}
        json.dump(manifest, open(MANIFEST, "w"), indent=2, sort_keys=True)
        open(MANIFEST, "a").write("\n")


if __name__ == "__main__":
    main()
