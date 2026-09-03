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

- **Static site generator**: Jekyll 3.10.0 (GitHub Pages' built-in builder)
- **Hosting**: GitHub Pages, custom domain via `CNAME`
- **CSS**: hand-written, minified in CI by `clean-css`
- **Icons**: Font Awesome 6.7.2 (cdnjs)
- **Images**: WebP with `srcset`
- **PWA**: Web app manifest + service worker

Plugins are limited to the GitHub Pages whitelist: `jekyll-seo-tag` and `jekyll-sitemap`.

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

`season.events` in `club.yml` drives the `/events/` page (cards, `Event` schema and the
screen-reader list) **and** the announcement bar. Entries marked `beginner: true` also
appear in the bar. Add a date once and it shows up in all four places.

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
| Events | `/events/` |
| Fixtures & Results | `/fixtures/` |
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

## Fixtures

`/fixtures/` renders from `_data/fixtures.yml`, which is **generated** — never
edit it by hand. The `sync-fixtures.yml` workflow pulls the club's Google
Calendar nightly, converts it to YAML and commits only if something changed.
To change a fixture, edit the calendar.

Because the fixtures end up as static HTML, they are indexable by Google, get
`SportsEvent` schema, match the site theme and load no third-party code.

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

Recurring calendar entries are expanded into individual dates. Home/away is
inferred from whether the event location matches the club venue.

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

Pushing to `master` deploys automatically via GitHub Pages.

Workflows:

| Workflow | What it does |
|---|---|
| `build-check.yml` | Builds the site, validates all JSON-LD, runs htmlproofer on internal links and images. Runs on PRs and pushes. |
| `minify-all-css.yml` | Minifies `assets/css/*.css` and `_includes/*.css`, commits the `.min.css` files back. |
| `sync-fixtures.yml` | Pulls the Google Calendar into `_data/fixtures.yml` nightly, commits on change. |
| `scheduled-rebuild.yml` | Nightly Pages rebuild so build-time date filtering stays current without a push. |

### A note on security headers

GitHub Pages serves static files only and **cannot set custom HTTP response headers** —
no CSP, `X-Frame-Options`, or `Referrer-Policy`. HTTPS and HSTS come from the repository's
"Enforce HTTPS" setting. A previous `.htaccess` in this repo was inert (GitHub Pages is not
Apache) and has been removed. Moving to a host that supports a `_headers` file
(Cloudflare Pages, Netlify) is the only way to add them.

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
