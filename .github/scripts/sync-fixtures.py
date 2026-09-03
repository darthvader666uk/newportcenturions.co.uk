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

    # Deduplicate (same title on the same day) and sort.
    seen = set()
    unique = []
    for f in sorted(fixtures, key=lambda x: (x["date_iso"], x["start_time"] or "")):
        key = (f["date_iso"], f["title"].lower())
        if key in seen:
            continue
        seen.add(key)
        unique.append(f)

    payload = {
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "Google Calendar",
        "fixtures": unique,
    }

    header = (
        "# GENERATED FILE - DO NOT EDIT BY HAND.\n"
        "#\n"
        "# Written by .github/workflows/sync-fixtures.yml from the club's Google\n"
        "# Calendar. To change a fixture, edit the calendar; the next sync picks\n"
        "# it up. Edits made here will be overwritten.\n\n"
    )

    with open(OUTPUT, "w", encoding="utf-8") as fh:
        fh.write(header)
        yaml.safe_dump(payload, fh, sort_keys=False, allow_unicode=True, default_flow_style=False)

    print(f"Wrote {OUTPUT}: {len(unique)} fixtures between {start} and {end}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
