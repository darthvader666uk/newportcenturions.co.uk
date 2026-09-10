# Newport Centurions Korfball Club — newportcenturions.co.uk

Jekyll-powered website for Newport Centurions Korfball Club, hosted on GitHub Pages.

## Quick Start

```bash
# Install dependencies
bundle install

# Run development server
./dev.sh

# Build for production
./build.sh
```

## Tech Stack

- **Static site generator**: Jekyll 3.10.0
- **Hosting**: Cloudflare Pages, built in GitHub Actions and uploaded with `wrangler`
- **CSS**: hand-written, minified in CI by `clean-css`
- **Icons**: Font Awesome 6.7.2 (cdnjs)
- **Images**: WebP with `srcset`
- **PWA**: Web app manifest + service worker

Plugins are `jekyll-seo-tag` and `jekyll-sitemap`. The `whitelist:` key in `_config.yml`
and the Jekyll 3.10 pin are both leftovers from GitHub Pages' built-in builder. Now that we
build the site ourselves neither constrains us, so a move to Jekyll 4 is available whenever
someone wants to do it as its own change.

## Project Structure

```
.
├── _config.yml                 # Site config + navigation menu
├── _data/
│   ├── club.yml                # ← Single source of truth for club facts
│   ├── fixtures.yml            # GENERATED from Google Calendar - do not edit
│   └── sponsors.yml            # Sponsor entries
├── _layouts/
│   └── default.html            # The only layout; every page uses it
├── _includes/
│   ├── navigation.html         # Header nav (reads site.navigation)
│   ├── footer.html
│   ├── announcement.html       # Announcement bar (auto-filters past dates)
│   ├── consent.html            # Cookie banner + gated analytics loader
│   ├── embed-facade.html       # Click-to-load wrapper for YouTube / Maps
│   ├── training.html           # Renders training times from club.yml
│   ├── critical.css/.min.css   # Inlined into <head> by the layout
│   ├── ai-*.html               # JSON-LD structured data blocks
├── assets/
│   ├── css/                    # styles.css, fonts.css (+ .min versions)
│   ├── fonts/                  # Self-hosted subset woff2
│   ├── favicon/
│   └── images/
├── images/                     # Logo variants
├── *.md                        # Pages live at the repo root, not in pages/
├── sw.js                       # Service worker
├── manifest.json               # Web app manifest
├── robots.txt
├── llms.txt                    # Summary for AI crawlers
└── .well-known/security.txt
```

`sitemap.xml` is **generated** by `jekyll-sitemap` — there is no source file for it.

## Editing club information

**Training times, venue, season dates, fees, member counts, awards and social links all
live in [`_data/club.yml`](_data/club.yml).** Change them there and they update across the
site — including the JSON-LD structured data, the footer, the homepage and the
announcement bar.

Do not hardcode these facts into individual pages.

### Season events

There is no hand-kept event list. Every date on the site comes from the club's Google
Calendar via `_data/fixtures.yml`: the `/events/` page, the beginner cards at the top of
it, the announcement bar and `llms.txt`. `club.yml` keeps only `season.label` and
`season.start_date`.

An event counts as a **beginner session** if it is tagged `[Beginners]` in Google
Calendar, or simply says "beginners" in the title of a training session. In practice the
title alone is enough, so no tagging is needed for the usual case. Those entries get an
orange ring on their card, a **Beginners** pill, and a mention in the announcement bar.

The keyword fallback is scoped to training deliberately, so "Cardiff Uni Beginners
Tournament" stays a game the club travels to rather than a come-and-try session. If a
competitive event ever should be ringed, tag it `[Beginners]` explicitly.

The ring is a shape cue rather than a sixth colour: the five category colours are already
spoken for, and a ring survives colour blindness where another orange would not. There is
no legend row for it, because the entries say "Beginners" in their own titles.

### Leagues

Prefix a fixture with its league code and the sync strips the code from the title, shows it
as a small pill on the card, and names the league in full in the details pop-up instead of
the generic "League game".

```
[Game] WKL: Newport 2 V Cardiff City 2
[Game] WRL: Exeter City 1 V Newport Centurions
```

The codes live in `league_codes` in `club.yml`. Only listed codes are recognised, and the
code may come before or after the `[Game]` tag. An unrecognised prefix is deliberately left
in the title rather than stripped, so a typo shows up on the page instead of being silently
absorbed into the home team's name, which is what breaks the crest lookup.

### Trophies

A game whose title contains **tournament** or **cup** gets a trophy icon on its card and in
the details popover, and reads as a **Tournament** there. Any other game reads as a
**League game**. The legend just says *Games*, because it groups by colour and both kinds
share one; the distinction is made per entry, where it is actually useful. It is scoped to games, so a social called "trophy
night" or a committee "cup draw" does not pick one up, and a plain league fixture stays
unmarked. The icon is a CSS mask rather than an emoji, so it takes the category's own
colour and renders identically on every platform.

Past dates are filtered twice, deliberately:

1. **At build time** — so crawlers and AI scrapers only ever see live dates.
2. **In the browser** — so a date that passes between rebuilds is hidden anyway.

A nightly `scheduled-rebuild.yml` workflow keeps the build-time pass current without
needing a push.

## Pages

| Page | URL |
|---|---|
| Homepage | `/` |
| About Us | `/about/` |
| What is Korfball? | `/what-is-korfball/` |
| Join Us | `/join-us/` |
| Training & Events | `/events/` |
| FAQ | `/faq/` |
| Glossary | `/glossary/` |
| Testimonials | `/testimonials/` |
| Sponsors | `/sponsors/` |
| Support Us | `/support/` |
| Contact | `/contact/` |
| Search | `/search/` |
| Privacy Policy | `/privacy/` |
| Thank You (form redirect, noindex) | `/thank-you/` |
| Team Store (external) | rcs-teamwear.com |

### Adding a page

1. Create `newpage.md` at the repo root with `layout: default` and a `permalink:`.
2. Add `breadcrumb: "Short Name"` to the front matter — this drives the `BreadcrumbList`
   schema. Omit it on pages that shouldn't have breadcrumbs (404, form confirmations).
3. Add it to `navigation:` in `_config.yml` if it belongs in the menu.
4. Use `sitemap: false` and `robots: "noindex, follow"` to keep it out of search results.

## Privacy & Analytics

Google Analytics 4 is **gated behind consent** (`_includes/consent.html`). Nothing
analytics-related loads until the visitor accepts; declining clears any `_ga*` cookies.
The choice is stored in an `nc_consent` cookie for 6 months and can be changed from the
[privacy policy](privacy.md) page.

To disable analytics entirely, blank out `analytics_id` at the top of
`_includes/consent.html`.

## Calendar

`/events/` renders from `_data/fixtures.yml`, which is **generated** — never
edit it by hand. The `sync-fixtures.yml` workflow pulls the club's Google
Calendar every half hour, converts it to YAML and commits only if something
changed. To change a fixture, edit the calendar.

Because the entries end up as static HTML, they are indexable by Google, carry
`SportsEvent`/`Event` schema, match the site theme and load no third-party code.

It renders as a **fixture list**, one month at a time with prev/next above it. Games with
two named sides get a fixture card: both teams with their crests, kick-off time and a
home/away pill. Everything else, socials, training and meetings, gets a single title line.
Each entry is colour-coded by category, and clicking one opens its full details: date,
time, location and the calendar description. Where there is a location, the address links
out to Google Maps.

On desktop the details open as a popover beside the entry so the month stays visible; on a
phone they open as a centred sheet, which is the only thing that reads well at that width.

There is **one list**, used by everyone. The earlier month grid had a visually hidden
agenda duplicated beneath it for screen readers and crawlers; the list replaced both, so
there is no `aria-hidden` grid, no duplicated text and every card is in the tab order.

### The season

The pager covers the whole playing season, **September to May**, empty months included, so
it walks the season in order rather than skipping the quiet ones and jumping December
straight to March. A month with nothing in it says so, and points at training, which runs
weekly whether or not it is entered in the calendar.

The bounds are `season.first_month` and `season.last_month` in `club.yml` (9 and 5). They
wrap the year end, and the sync works out which season today falls in: in February you get
February to May, and over the summer it looks ahead to the next September. Months with
events *outside* the season still appear on their own, up to 18 months out.

**The page always opens on the current month**, and it works that out twice over. The sync
drops months that have passed, so the data itself starts at the current one. The script then
picks the month from the *browser's* clock, so even a page cached from last month opens on
this one. Verified across the November rollover with the clock stubbed.

If the current month has nothing in it, the page falls forward to the next month that does.
If a page is somehow cached past the end of the data entirely, it opens on the most recent
month rather than the oldest.

Paging is progressive enhancement. With JavaScript off, every month stays on the page,
which is what a crawler sees, and the `Event` schema in the head lists every upcoming
entry regardless, so paging never hides anything from search engines.

### Team crests

Crests live in `assets/images/teams/<slug>.webp` and are picked up automatically: drop a
file in named after the club and it appears. There is no list to maintain, and no need to
convert or resize it first, because the *Optimise Images* workflow does that (see
**Images** below). `png`, `svg`, `jpg` and `jpeg` are all accepted.

The slug comes from the team name with its squad number removed, so one file covers all of
a club's sides. `Cardiff City 1`, `2` and `3` all use `cardiff-city.webp`. Newport's own
badge comes from `crest:` in `club.yml` rather than this folder, so the club logo is not
duplicated, and every way of writing our name resolves to it.

Both sides' badges also appear in the details pop-up, resolved through the same
`crest-url.html` include so the pop-up and the card behind it can never disagree.

Without a file a team shows its initials in the category colour, so a missing crest looks
deliberate rather than broken.

> If a crest shows as initials when the file is clearly there, restart the dev server.
> Jekyll does not reload `_config.yml` while `--watch` is running, and `crest_formats`
> lives there. The include falls back to a built-in list to soften this, but a stale
> server can still be serving HTML from before the file existed. `assets/images/teams/README.md` repeats the rules next to
the files, with a one-liner for converting a download.

They render at 30px as a **rounded square**, not a circle: several korfball crests are
square with the club's name banded across the bottom, and a circular clip cuts it off.

### Categorising an event

Category comes from the calendar event title: prefix it with a tag, which the
sync strips before display.

| Tag | Category |
|---|---|
| `[Game]` | Games |
| `[Training]` | Training sessions |
| `[Social]` | Socials |
| `[Club]` | Committee / AGMs / admin |
| `[Beginners]` | Training, and ringed on `/events/` |

Hashtags work too (`#social`). Untagged events are auto-classified by keyword
(tournament/cup → game, AGM/committee → club, and so on).

**Home/away** (games only): usually nothing to do. Write the fixture the normal way round
and whoever is named first is at home, across all three teams:

| Title | Reads as |
|---|---|
| `Newport 1 V Cardiff City 1` | home |
| `Newport 2 V Cardiff City 2` | home |
| `Cardiff City 3 V Newport 3` | away |
| `Bristol 1 v Exeter 2` | a game, but unmarked: no Newport side to read |

`v`, `V`, `vs` and `versus` all work, and a title written that way is recognised as a game
without needing `[Game]`. Newport first wins outright, so an internal `Newport 1 v
Newport 3` reads as home.

To override it, add `[Home]` or `[Away]`, e.g. `[Game] [Home] Cardiff Dragons`.
`#home`/`#away`, or a plain leading `Home`/`Away`, also work and beat the running order.
A **Home** / **Away** pill then shows on the fixture card. It's ignored on non-games.

The club calendar is **private and stays private** — because the sync turns it into
committed data, visitors never need access to it.

**One-off setup** (until this is done the page shows an empty state and the
workflow exits cleanly):

1. Google Calendar → the fixtures calendar → *Settings and sharing*
2. Scroll to *Integrate calendar* and copy the **Secret address in iCal format**
   (it ends in `.ics`)
3. Repo → Settings → Secrets and variables → Actions → **Secrets** tab →
   *New repository secret*, named `FIXTURES_ICS_URL`
4. Run *Sync Fixtures* once from the Actions tab to confirm

> It must be a **secret**, not a variable. This repo is public, and only secrets
> are masked in workflow logs. The sync script never prints the URL either.

If you ever hit *Reset* on the secret address in Google Calendar, the old URL stops
working — update the secret with the new one. The workflow will fail with a message
telling you exactly that.

Recurring calendar entries are expanded into individual dates.

### How often it syncs

The workflow runs every 30 minutes, so an edit in Google Calendar reaches the
site within about half an hour with nothing to press. It only commits when the
calendar actually changed, so a quiet week adds no commits and no rebuilds.

The `generated:` timestamp in the data file is deliberately left alone when
nothing else moved. Rewriting it on every run would make the file differ every
time, and the workflow would commit and rebuild the site 48 times a day whether
or not anything had changed.

Two things worth knowing about GitHub's scheduled runs:

- They are best effort. Under load a run can land late or be skipped, and the
  next one picks it up, so worst case is roughly an hour rather than 30 minutes.
- GitHub disables scheduled workflows on a public repo after 60 days with no
  commits. Push anything and they resume.

To sync immediately, run *Sync Fixtures* from the Actions tab, or:

```bash
gh workflow run sync-fixtures.yml
```

Change the cadence by editing the `cron` line in the workflow. Going much below
30 minutes is not worth it: the run itself takes about half a minute, and the
Pages rebuild that follows a change takes longer than the polling gap you save.

## Images

Images are optimised automatically. Add one, push, and `optimise-images.yml` shrinks it
and commits the result back, so nobody has to remember to do it by hand.

| Where | What happens |
|---|---|
| `assets/images/teams/` | Converted to a 120px `webp` with a lowercase filename. Safe to rename, because crests are looked up by slug with each extension tried in turn, so nothing points at one by path. |
| `assets/favicon/` | Lossless PNG optimisation only, never resized: `manifest.json` declares their dimensions. |
| everything else | Capped at 1200px on the longest side and re-encoded in the **same format under the same name**, because `<img src>`, `manifest.json` and the JSON-LD schema reference those paths literally. |

Re-encoding a lossy image repeatedly degrades it, so each optimised file's hash is recorded
in `.github/image-manifest.json` and anything already done is skipped. That also means a
push with no new images produces no commit. Delete the manifest and everything gets
re-encoded once, costing one generation of quality on the JPEGs.

It never writes a file that came out bigger, even when it had to resize, because that
would mean losing quality *and* gaining bytes. Run it locally to see what it would do:

```bash
python3 -m venv /tmp/imgenv && /tmp/imgenv/bin/pip install pillow && /tmp/imgenv/bin/python .github/scripts/optimise-images.py --check
```

The first run took the repo's images from 899KB to 525KB.

## Search

`/search/` is client-side: `search.json` is generated at build time from every
page, and the page filters it in the browser. No index to maintain and no
third-party service.

## Third-party embeds

The Google Map on `/contact/` and the YouTube video on `/what-is-korfball/` use
a **click-to-load facade** (`_includes/embed-facade.html`). Nothing is requested
from Google or YouTube until the visitor clicks, which keeps them out of the
consent problem and saves ~1.5MB of payload.

Fonts are self-hosted in `assets/fonts/` (subset) rather than loaded from
Google Fonts.

## Service Worker

`sw.js` is **network-first for HTML** and stale-while-revalidate for assets. This matters:
an earlier cache-first version meant returning visitors never saw content updates.

Bump `CACHE_VERSION` in `sw.js` when changing the precache list.

## SEO

- `jekyll-seo-tag` handles titles, canonicals, Open Graph and Twitter cards
- JSON-LD: Organization, WebSite, SportsTeam, SportsActivityLocation, Event, FAQPage,
  HowTo, BreadcrumbList
- `llms.txt` provides a plain-text summary for AI crawlers
- Generated `sitemap.xml`

## Deployment

Pushing to `master` builds the site in GitHub Actions and uploads `_site` straight to
Cloudflare Pages with `wrangler`. Nothing is uploaded unless the build, the JSON-LD
validation and htmlproofer all pass, so a broken commit stops at CI rather than on the
live site.

Cloudflare's own Git integration is deliberately NOT connected. The free plan allows 500
Cloudflare-run builds a month and `sync-fixtures.yml` commits to `master` on its own
schedule, which would eat into that for no benefit. Direct uploads do not count against
the cap and they let us gate the deploy on the checks above.

Two repository secrets are required, both set up in `deploy.yml`'s header comment:
`CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID`.

Workflows:

| Workflow | What it does |
|---|---|
| `deploy.yml` | Builds, validates, and uploads to Cloudflare Pages. Runs on pushes to `master`, daily at 04:15 UTC, and on demand. |
| `build-check.yml` | The same build and checks, on pull requests only. `deploy.yml` covers `master`. |
| `minify-all-css.yml` | Minifies `assets/css/*.css` and `_includes/*.css`, commits the `.min.css` files back. |
| `sync-fixtures.yml` | Pulls the Google Calendar into `_data/fixtures.yml` every 30 minutes, commits on change. Also runs on demand. |
| `optimise-images.yml` | Converts and compresses any image that lands in the repo, commits the result back. |

### Response headers and caching

Both live in `_headers`, which Cloudflare Pages reads at the edge. That file is commented
in full, but two things are worth repeating because they are easy to get wrong:

- Jekyll skips underscore-prefixed files, so `_headers` only reaches `_site` because
  `_config.yml` lists it under `include:`. Losing it is silent, so `deploy.yml` fails the
  build if the file is not there.
- A splat in `_headers` matches greedily to the end of the path. There is no `/*.html`
  rule, and there does not need to be: Cloudflare Pages already serves HTML as
  `max-age=0, must-revalidate`, which is what date-filtered pages need.

No asset filename is content-hashed. `styles.min.css` keeps that name forever and
`optimise-images.yml` rewrites photos in place under the same path, so nothing except
fonts gets a long `immutable` cache.

The CSP ships as `Content-Security-Policy-Report-Only` until it has been watched on a real
page with cookies accepted. Analytics is injected at runtime after consent, so `connect-src`
and `img-src` are the entries most likely to need a correction.

HSTS is not in `_headers`. The Cloudflare zone already sends it, and duplicating it here
would just mean two headers saying the same thing.

A previous `.htaccess` in this repo was inert (neither host is Apache) and has been removed.
The `ssl:` and `enforce_ssl:` keys that used to sit near the top of `_config.yml` were the
same kind of thing. Jekyll has no such settings and never read them, so they have gone too.
Real HSTS now comes from the Cloudflare zone.

### Cutover to Cloudflare Pages

Do these in order. The site stays up on GitHub Pages until step 4.

1. Create the Pages project and add the two secrets, per the comment at the top of
   `.github/workflows/deploy.yml`.
2. Run **Deploy** from the Actions tab. It publishes to `newportcenturions.pages.dev`.
3. Check that URL properly: the announcement bar, `/events/`, the fixtures, the service
   worker, and `curl -I` on a stylesheet to confirm the `_headers` rules are being applied.
4. Pages project, Custom domains, add `newportcenturions.co.uk`. The domain is already on
   Cloudflare nameservers, so Cloudflare updates the DNS record itself and the old GitHub
   Pages A records go away. Add `www` at the same time if it is in use.
5. Confirm HSTS is still on the response (`curl -I https://newportcenturions.co.uk`). It
   comes from the zone rather than from the origin, so it should be unaffected, but check.
6. Repo Settings, Pages, set the source to None.
7. Delete `CNAME`. It only ever meant anything to GitHub Pages.

Traffic reached the site through Cloudflare AND Fastly before this, because the zone was
proxying in front of GitHub Pages. That is why GitHub could not issue its own certificate
and `"https_enforced"` was `false` on the Pages API. The cutover removes the second hop.

## Development Requirements

- Ruby >= 2.7.0
- Bundler >= 2.0.0

## Contact Form

The contact form posts to [FormSubmit](https://formsubmit.co), which forwards submissions to
the club email address. There is no backend to maintain. This is documented in the privacy
policy.

## Social Media

- **Facebook**: [@newportcenturions](https://facebook.com/newportcenturions)
- **Twitter**: [@newportkorfball](https://twitter.com/newportkorfball)
- **Instagram**: [@newportkorfball](https://instagram.com/newportkorfball)
- **YouTube**: [@newportcenturionskorfball5878](https://youtube.com/@newportcenturionskorfball5878)

## License

© Newport Centurions Korfball Club. All rights reserved.

---

**Welsh League Champions 2022/2023 & 2025** 🏆

<a href="https://www.buymeacoffee.com/darthvader666uk" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" style="height: 51px !important;width: 217px !important;" ></a>
