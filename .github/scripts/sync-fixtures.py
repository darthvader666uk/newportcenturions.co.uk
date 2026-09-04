#!/usr/bin/env python3
"""
Sync fixtures from the club's Google Calendar into _data/fixtures.yml.

Run by .github/workflows/sync-fixtures.yml on a schedule. The site itself stays
fully static: this turns the calendar into committed data, which Jekyll renders
as ordinary HTML. That keeps fixtures indexable by Google, fast, themed, and
free of third-party code on the page -- and means the calendar itself can stay
private, because visitors never touch it.

The calendar is NOT public, so FIXTURES_ICS_URL holds its *secret* iCal address.
It must be stored as a GitHub Actions secret, never a repository variable and
never committed: this repo is public, and secrets (unlike variables) are also
masked in workflow logs. This script never prints the URL.

Usage:
    FIXTURES_ICS_URL="https://calendar.google.com/calendar/ical/.../private-<hash>/basic.ics" \
        python3 .github/scripts/sync-fixtures.py

Exits 0 and writes nothing if the URL is unset, so the workflow is harmless
until the secret is added.
"""

import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta, date, timezone

try:
    import yaml
    from icalendar import Calendar
    import recurring_ical_events
except ImportError as exc:  # pragma: no cover - workflow installs these
    sys.exit(f"Missing dependency: {exc}. Run: pip install icalendar recurring-ical-events pyyaml")


# How far either side of today to publish. Past fixtures become "recent results".
MONTHS_BACK = 4
MONTHS_AHEAD = 12

OUTPUT = "_data/fixtures.yml"
PLACEHOLDER = "REPLACE_WITH_YOUR_ICS_URL"

# Don't emit empty grids for months far in the future.
MAX_MONTHS_AHEAD = 18

# Category keys and their display labels (also the legend order).
# The legend groups by colour, so "Games" covers the lot. What kind of game it
# is gets said per entry instead: a title with tournament or cup in it reads as
# a Tournament, anything else as a League game.
CATEGORY_LABELS = [
    ("game", "Games"),
    ("training", "Training"),
    ("social", "Socials"),
    ("club", "Club & Meetings"),
    ("other", "Other"),
]
VALID_CATEGORIES = {k for k, _ in CATEGORY_LABELS}

# Explicit tags a calendar event title can carry, e.g. "[Social] Pub night"
# or "Pub night #social". These win over keyword detection.
TAG_SYNONYMS = {
    "game": "game", "games": "game", "match": "game", "matches": "game",
    "fixture": "game", "fixtures": "game", "tournament": "game", "cup": "game",
    "training": "training", "train": "training",
    "social": "social", "socials": "social",
    "club": "club", "admin": "club", "meeting": "club", "committee": "club",
    "other": "other",
}

# Fixtures are usually written "Newport 2 V Cardiff City 2". Matched as a word
# so it catches v, V, vs and versus with or without a full stop, but not "v2"
# or a word that merely starts with v.
VERSUS_RE = re.compile(r"\bv(?:s|ersus)?\.?\s", re.I)

# Whoever is named first in a fixture is at home, so "Newport 2 V Cardiff City 2"
# is a home game and reversing it makes it away. These are the words that mean
# "us" in a fixture title; an explicit [Home]/[Away] tag still wins over them.
HOME_TEAM_TOKENS = ("newport", "centurion")


def team_slug(name):
    """Crest lookup key for a team name.

    The squad number is dropped, so Newport 1, 2 and 3 share one crest, as do
    a visiting club's sides. Everything else becomes lowercase and hyphenated:
    "Cardiff City 2" -> "cardiff-city".
    """
    name = re.sub(r"\s+\d+$", "", name.strip())
    # Our own sides all resolve to one crest however they are written, so
    # "Newport 2" and "Newport Centurions" both find the club badge.
    if any(k in name.lower() for k in HOME_TEAM_TOKENS):
        return "newport"
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def split_fixture(title):
    """Split "Newport 2 V Cardiff City 2" into its two sides.

    Returns (home, away) in the order written, or (None, None) if the title is
    not a head-to-head fixture. Tournaments have no single opponent, so they
    fall through and get rendered as a one-sided card.
    """
    m = VERSUS_RE.search(title)
    if not m:
        return None, None
    home = " ".join(title[:m.start()].split())
    away = " ".join(title[m.end():].split())
    if not home or not away:
        return None, None
    return home, away

# Fallback keyword detection for untagged events. First match wins, so order
# matters: club (AGMs/meetings) is checked before game so "WKA AGM" isn't a
# game, and game before training so "Beginners Tournament" is a game.
KEYWORD_RULES = [
    ("club", ["agm", "committee", "meeting"]),
    ("game", ["tournament", "cup", "match", "inter area", "inter-area", "league"]),
    ("social", ["social", "pub", "bowling", "awards", "beach", "meal", "party",
                "christmas", "ice hockey", "curry", "night out"]),
    ("training", ["training", "session", "beginner", "korf"]),
]


# Beginner sessions are the club's way in for new players, so they get picked
# out of the calendar for the top of /events/ and the announcement bar. Tag one
# "[Beginners]", or just say "beginners" in a training session's title.
BEGINNER_TAGS = {"beginner", "beginners"}

# Competitions get a trophy on the calendar. Scoped to games, so a social
# called "trophy night" or a committee "cup draw" does not pick one up.
TROPHY_KEYWORDS = ("tournament", "cup")


def categorise(title):
    """Return (category, side, beginner, trophy, cleaned_title).

    Category and an optional home/away side are read from tags in the event
    title, e.g. "[Game] [Home] Cardiff Dragons" or "Pub night #social".
    Category falls back to keyword detection. `side` is only meaningful for
    games and comes from a [Home]/[Away] tag, a #home/#away hashtag, a leading
    "Home"/"Away" word, or failing all of those, from who is named first in a
    "A v B" title. `beginner` marks a session aimed
    at newcomers, `trophy` marks a competition. All recognised tags are
    stripped from the title before display."""
    t = title.strip()
    cat = None
    side = None
    beginner = False

    # Consume any number of leading [..] tags: "[Game] [Home]", "[Home][Game]".
    while True:
        m = re.match(r"^\[([^\]]+)\]\s*", t)
        if not m:
            break
        key = m.group(1).strip().lower()
        if key in ("home", "away"):
            side = side or key
        elif key in BEGINNER_TAGS:
            beginner = True
            cat = cat or "training"
        elif key in TAG_SYNONYMS:
            cat = cat or TAG_SYNONYMS[key]
        else:
            break  # unrecognised bracket -> leave it in the title
        t = t[m.end():].strip()

    # #hashtags anywhere, for category and/or side.
    for tag in re.findall(r"#(\w+)", t):
        low = tag.lower()
        if low in ("home", "away") and side is None:
            side = low
            t = re.sub(r"#" + re.escape(tag) + r"\b", "", t)
        elif low in BEGINNER_TAGS:
            beginner = True
            cat = cat or "training"
            t = re.sub(r"#" + re.escape(tag) + r"\b", "", t)
        elif low in TAG_SYNONYMS and cat is None:
            cat = TAG_SYNONYMS[low]
            t = re.sub(r"#" + re.escape(tag) + r"\b", "", t)

    if cat is None:
        low = " " + t.lower() + " "
        for candidate, keywords in KEYWORD_RULES:
            if any(k in low for k in keywords):
                cat = candidate
                break

    # "Team A v Team B" with nothing else to go on is a fixture.
    if cat is None and VERSUS_RE.search(t):
        cat = "game"


    if cat not in VALID_CATEGORIES:
        cat = "other"

    # For games only, accept a plain leading "Home"/"Away" or "(home)"/"(away)"
    # so it works even without brackets. Scoped to games so socials that happen
    # to say "away day" aren't mislabelled.
    if cat == "game" and side is None:
        lead = re.match(r"^(home|away)\b[\s:.–-]*", t, re.I)
        if lead:
            side = lead.group(1).lower()
            t = t[lead.end():].strip()
            # "Away v Cardiff" would otherwise display as "v Cardiff".
            t = re.sub(r"^v(?:s|ersus)?\.?\s+", "", t, flags=re.I)
        elif re.search(r"\((home|away)\)", t, re.I):
            side = re.search(r"\((home|away)\)", t, re.I).group(1).lower()
            t = re.sub(r"\((home|away)\)", "", t, flags=re.I)

    # Last resort: read it off the running order. Home team is named first, so
    # "Newport 2 V Cardiff City 2" is home and "Cardiff City 2 V Newport 2" is
    # away. Newport first wins outright, which also settles an all-Newport
    # fixture like "Newport 1 v Newport 3" as a home game. A title with no
    # Newport side in it is left unmarked: there is nothing to read.
    if cat == "game" and side is None:
        versus = VERSUS_RE.search(t)
        if versus:
            if any(k in t[:versus.start()].lower() for k in HOME_TEAM_TOKENS):
                side = "home"
            elif any(k in t[versus.end():].lower() for k in HOME_TEAM_TOKENS):
                side = "away"

    # Untagged fallback. Scoped to training on purpose: "Cardiff Uni Beginners
    # Tournament" is a game the club travels to, not a come-and-try session.
    if not beginner and cat == "training" and "beginner" in t.lower():
        beginner = True

    low = t.lower()
    trophy = cat == "game" and any(k in low for k in TROPHY_KEYWORDS)

    return cat, side, beginner, trophy, " ".join(t.split())


def build_months(events, today):
    """Events grouped by month, for the current month plus every later month
    that has one, up to MAX_MONTHS_AHEAD."""
    current = date(today.year, today.month, 1)
    horizon = current
    for _ in range(MAX_MONTHS_AHEAD):
        horizon = (horizon.replace(day=28) + timedelta(days=7)).replace(day=1)
    event_months = {(e["date"].year, e["date"].month) for e in events}

    months = []
    y, m = current.year, current.month
    while date(y, m, 1) <= horizon:
        if (y, m) == (current.year, current.month) or (y, m) in event_months:
            agenda = sorted(
                (e for e in events if (e["date"].year, e["date"].month) == (y, m)),
                key=lambda e: (e["date_iso"], e["start_time"] or ""),
            )
            months.append({
                "key": f"{y:04d}-{m:02d}",
                "label": date(y, m, 1).strftime("%B %Y"),
                "events": [
                    {"id": e["id"], "title": e["title"], "category": e["category"],
                     "beginner": e.get("beginner", False),
                     "trophy": e.get("trophy", False),
                     "side": e.get("side"), "date_iso": e["date_iso"],
                     "day": e["date"].day, "weekday": e["date"].strftime("%a"),
                     "month_abbr": e["date"].strftime("%b"),
                     "time": e["start_time"], "end_time": e["end_time"],
                     "all_day": e["all_day"], "location": e["location"],
                     "home_team": e.get("home_team"), "away_team": e.get("away_team"),
                     "home_slug": e.get("home_slug"), "away_slug": e.get("away_slug")}
                    for e in agenda
                ],
            })

        if m == 12:
            y, m = y + 1, 1
        else:
            m += 1
    return months


def build_payload(events, today=None):
    """Categorise, deduplicate, sort and assemble the full data file from a list
    of raw event dicts. Shared by the live sync and local testing."""
    today = today or date.today()

    for e in events:
        cat, side, beginner, trophy, clean_title = categorise(e["title"])
        e["category"] = cat
        e["side"] = side
        e["beginner"] = beginner
        e["trophy"] = trophy
        e["title"] = clean_title

        home, away = split_fixture(clean_title) if cat == "game" else (None, None)
        e["home_team"] = home
        e["away_team"] = away
        e["home_slug"] = team_slug(home) if home else None
        e["away_slug"] = team_slug(away) if away else None

    seen = set()
    unique = []
    for e in sorted(events, key=lambda x: (x["date_iso"], x["start_time"] or "")):
        key = (e["date_iso"], e["title"].lower())
        if key in seen or not e["title"]:
            continue
        seen.add(key)
        unique.append(e)

    # A stable handle for each event, so the month grid and the agenda can both
    # point at the same entry in the page's detail payload without repeating it.
    for i, e in enumerate(unique, 1):
        e["id"] = "e%d" % i

    return {
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "Google Calendar",
        "categories": [{"key": k, "label": l} for k, l in CATEGORY_LABELS],
        "fixtures": unique,
        "months": build_months(unique, today),
    }


class _StrQuotingDumper(yaml.SafeDumper):
    pass


def _represent_str(dumper, data):
    # Force-quote any string a YAML 1.1 parser (Ruby/Jekyll's Psych) might read
    # as a number, time or date. PyYAML leaves "08:00" unquoted because its
    # sexagesimal detector ignores the leading zero, but Psych then parses it as
    # 480.0. Quoting anything starting with a digit or containing ":" is a safe,
    # cross-parser fix.
    style = "'" if data and (data[0].isdigit() or ":" in data) else None
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style=style)


_StrQuotingDumper.add_representer(str, _represent_str)


def _without_timestamp(text):
    """The file minus its `generated:` line, for comparing runs."""
    return "\n".join(l for l in text.splitlines() if not l.startswith("generated:"))


def write_payload(payload):
    header = (
        "# GENERATED FILE - DO NOT EDIT BY HAND.\n"
        "#\n"
        "# Written by .github/workflows/sync-fixtures.yml from the club's Google\n"
        "# Calendar. To change an entry, edit the calendar; the next sync picks\n"
        "# it up. Edits made here will be overwritten.\n"
        "#\n"
        "# Category comes from a [Tag] or #tag in the event title (Game, Training,\n"
        "# Social, Club), falling back to keyword detection. See the script header.\n\n"
    )
    body = yaml.dump(payload, Dumper=_StrQuotingDumper, sort_keys=False,
                     allow_unicode=True, default_flow_style=False)
    text = header + body

    # `generated` is a fresh timestamp on every run, so writing unconditionally
    # would make the file differ every time and the workflow would commit and
    # rebuild the site every half hour whether or not the calendar changed.
    # If nothing but that line has moved, leave the file exactly as it is.
    if os.path.exists(OUTPUT):
        existing = open(OUTPUT, encoding="utf-8").read()
        if _without_timestamp(existing) == _without_timestamp(text):
            print("No calendar changes; leaving _data/fixtures.yml alone.")
            return False

    with open(OUTPUT, "w", encoding="utf-8") as fh:
        fh.write(text)
    return True


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "newportcenturions.co.uk fixtures sync"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def as_date(value):
    """icalendar gives date for all-day events and datetime otherwise."""
    if isinstance(value, datetime):
        return value.date()
    return value


def as_time(value):
    if isinstance(value, datetime):
        return value.strftime("%H:%M")
    return None


def clean(text):
    if text is None:
        return ""
    return " ".join(str(text).split())


def main():
    url = os.environ.get("FIXTURES_ICS_URL", "").strip()

    if not url or PLACEHOLDER in url:
        print("FIXTURES_ICS_URL not configured yet - nothing to do.")
        return 0

    if not url.endswith(".ics"):
        sys.exit(
            "FIXTURES_ICS_URL does not look like an iCal address (should end in .ics).\n"
            "Use the 'Secret address in iCal format' from Google Calendar → "
            "Settings and sharing → Integrate calendar."
        )

    # Deliberately never echo the URL - it is a secret.
    print("Fetching calendar…")
    try:
        raw = fetch(url)
    except urllib.error.HTTPError as exc:
        if exc.code in (401, 403, 404):
            sys.exit(
                f"Calendar fetch failed with HTTP {exc.code}.\n"
                "The secret iCal address is probably wrong or has been reset.\n"
                "Re-copy it from Google Calendar → Settings and sharing → "
                "Integrate calendar → 'Secret address in iCal format', and update "
                "the FIXTURES_ICS_URL repository secret."
            )
        sys.exit(f"Calendar fetch failed with HTTP {exc.code}.")
    except urllib.error.URLError as exc:
        sys.exit(f"Could not reach Google Calendar: {exc.reason}")

    if b"BEGIN:VCALENDAR" not in raw[:2048]:
        sys.exit(
            "Response was not an iCalendar file. Check FIXTURES_ICS_URL points at "
            "the .ics address rather than the embed or HTML view."
        )

    calendar = Calendar.from_ical(raw)

    today = date.today()
    start = today - timedelta(days=MONTHS_BACK * 31)
    end = today + timedelta(days=MONTHS_AHEAD * 31)

    # Expands RRULEs, so weekly/recurring entries appear as individual dates.
    occurrences = recurring_ical_events.of(calendar).between(start, end)

    fixtures = []
    for event in occurrences:
        summary = clean(event.get("SUMMARY"))
        if not summary:
            continue

        dtstart = event.get("DTSTART")
        if dtstart is None:
            continue
        start_value = dtstart.dt
        dtend = event.get("DTEND")
        end_value = dtend.dt if dtend is not None else None

        event_date = as_date(start_value)

        fixtures.append({
            "title": summary,
            "date": event_date,
            # Plain string alongside the Date so Liquid can compare it to
            # `'now' | date: '%Y-%m-%d'` without type juggling.
            "date_iso": event_date.isoformat(),
            "start_time": as_time(start_value),
            "end_time": as_time(end_value) if end_value is not None else None,
            "location": clean(event.get("LOCATION")),
            "description": clean(event.get("DESCRIPTION"))[:400],
            "all_day": not isinstance(start_value, datetime),
        })

    payload = build_payload(fixtures, today)
    written = write_payload(payload)

    verb = "Wrote" if written else "Checked"
    dates = [f["date_iso"] for f in payload["fixtures"]]
    span = f"{min(dates)} to {max(dates)}" if dates else "no dates"
    print(f"{verb} {OUTPUT}: {len(payload['fixtures'])} events, {span} "
          f"(scanned {start} to {end}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
