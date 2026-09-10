#!/usr/bin/env python3
"""
Season opener graphic for social. Renders the club crest, a headline and the
first fixture of each team onto a black/gold card, in two sizes:

  season-opener-<year>-square.png     1080x1080  WhatsApp announcements
  season-opener-<year>-portrait.png   1080x1350  Facebook and Instagram

WhatsApp centre-crops anything taller than a square, which is why the square
version exists and why nothing readable sits in the top or bottom bars.

To regenerate next season: change YEAR and FIXTURES below, then

    python3 scripts/season-graphic.py

Output lands in .vscode/social/ (gitignored, so renders never reach the site).
Needs Pillow and the Lato fonts (fonts-lato).
"""

import os
from PIL import Image, ImageDraw, ImageFont

# --- edit these two each season ----------------------------------------------
YEAR = 2026
FIXTURES = [
    ("1sts  ·  SUN 27 SEPT", "Away to Cardiff Raptors 1  ·  Sport Wales, Cardiff"),
    ("2nds  ·  SAT 3 OCT",   "Home to Cardiff City 2  ·  John Frost, Newport"),
    ("3rds  ·  SUN 11 OCT",  "Away to Swansea Roar 2  ·  Pontardawe"),
]
HEADLINE = ("THE CAMPAIGN", "BEGINS")
FOOTER = "FOR NEWPORT!"
# -----------------------------------------------------------------------------

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CREST = os.path.join(REPO, "images", "newport-centurions-korfball-club-800.webp")
OUTDIR = os.path.join(REPO, ".vscode", "social")

FDIR = "/usr/share/fonts/truetype/lato/"
BLACK = FDIR + "Lato-Black.ttf"
BOLD = FDIR + "Lato-Bold.ttf"

GOLD = (255, 184, 28)
ORANGE = (245, 130, 32)
WHITE = (255, 255, 255)
INK = (11, 11, 11)


def background(W, H, cy_frac):
    """Warm radial glow behind the crest, built small then upscaled (fast)."""
    sw, sh = 120, int(120 * H / W)
    glow = Image.new("RGB", (sw, sh))
    gp = glow.load()
    cx, cy = sw * 0.5, sh * cy_frac
    maxd = (sw ** 2 + sh ** 2) ** 0.5
    for y in range(sh):
        for x in range(sw):
            d = (((x - cx) ** 2 + (y - cy) ** 2) ** 0.5) / (maxd * 0.62)
            t = max(0.0, 1.0 - d) ** 1.7
            gp[x, y] = (int(7 + 46 * t), int(7 + 26 * t), int(7 + 3 * t))
    return glow.resize((W, H), Image.LANCZOS)


def tracked(draw, W, y, text, font, fill, track=0):
    """Centred text with manual letter-spacing, which Pillow has no option for."""
    widths = [draw.textlength(c, font=font) for c in text]
    total = sum(widths) + track * (len(text) - 1)
    cur = (W - total) / 2
    for c, w in zip(text, widths):
        draw.text((cur, y), c, font=font, fill=fill)
        cur += w + track


def build(W, H, L, out_name):
    img = background(W, H, L["glow"])
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, L["bar"]], fill=ORANGE)

    crest = Image.open(CREST).convert("RGBA").resize(L["crest"], Image.LANCZOS)
    img.paste(crest, ((W - L["crest"][0]) // 2, L["crest_y"]), crest)

    # BEGINS is tracked much wider so the two lines read as one block rather
    # than a long line sitting over a short one.
    hf = ImageFont.truetype(BLACK, L["head"])
    tracked(d, W, L["h1"], HEADLINE[0], hf, GOLD, track=L["head"] // 18)
    tracked(d, W, L["h2"], HEADLINE[1], hf, GOLD, track=L["head"] / 2.7)
    d.rectangle([W * 0.315, L["rule"], W * 0.685, L["rule"] + 6], fill=ORANGE)

    f_hd = ImageFont.truetype(BLACK, L["fx_head"])
    f_bd = ImageFont.truetype(BOLD, L["fx_sub"])
    y = L["fx_y"]
    for head, sub in FIXTURES:
        tracked(d, W, y, head, f_hd, GOLD, track=1)
        tracked(d, W, y + L["fx_gap"], sub, f_bd, WHITE)
        y += L["fx_step"]

    d.rectangle([0, L["foot"], W, H], fill=ORANGE)
    tracked(d, W, L["foot"] + L["foot_pad"], FOOTER,
            ImageFont.truetype(BLACK, L["foot_size"]), INK, track=L["foot_track"])

    os.makedirs(OUTDIR, exist_ok=True)
    img.save(os.path.join(OUTDIR, out_name + ".png"))
    img.save(os.path.join(OUTDIR, out_name + ".jpg"), quality=92)
    print("wrote {}.png / .jpg  ({}x{})".format(out_name, W, H))


SQUARE = dict(glow=0.21, bar=8, crest=(300, 375), crest_y=36,
              head=88, h1=436, h2=536, rule=654,
              fx_head=38, fx_sub=28, fx_y=694, fx_gap=50, fx_step=98,
              foot=1000, foot_pad=20, foot_size=40, foot_track=9)

PORTRAIT = dict(glow=0.245, bar=9, crest=(420, 525), crest_y=62,
                head=108, h1=606, h2=728, rule=876,
                fx_head=42, fx_sub=30, fx_y=926, fx_gap=54, fx_step=112,
                foot=1276, foot_pad=20, foot_size=44, foot_track=10)

if __name__ == "__main__":
    build(1080, 1080, SQUARE, "season-opener-{}-square".format(YEAR))
    build(1080, 1350, PORTRAIT, "season-opener-{}-portrait".format(YEAR))
