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

Plugins are limited to the GitHub Pages whitelist: `jekyll-seo-tag`, `jekyll-sitemap`,
`jekyll-feed`.

## Project Structure

```
.
├── _config.yml                 # Site config + navigation menu
├── _data/
│   ├── club.yml                # ← Single source of truth for club facts
│   └── sponsors.yml            # Sponsor entries
├── _layouts/
│   └── default.html            # The only layout; every page uses it
├── _includes/
│   ├── navigation.html         # Header nav (reads site.navigation)
│   ├── footer.html
│   ├── announcement.html       # Announcement bar (auto-filters past dates)
│   ├── consent.html            # Cookie banner + gated analytics loader
│   ├── ai-*.html               # JSON-LD structured data blocks
├── assets/
│   ├── css/                    # styles.css + critical.css (+ .min versions)
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

`sitemap.xml` and `feed.xml` are **generated** by `jekyll-sitemap` / `jekyll-feed` — there
are no source files for them.

## Editing club information

**Training times, venue, season dates, fees, member counts, awards and social links all
live in [`_data/club.yml`](_data/club.yml).** Change them there and they update across the
site — including the JSON-LD structured data, the footer, the homepage and the
announcement bar.

Do not hardcode these facts into individual pages.

### Beginner session dates

`season.beginner_sessions` in `club.yml` drives the announcement bar. Dates in the past are
filtered out **at build time**, so the bar never advertises a date that has already passed —
but this only re-evaluates when the site rebuilds (i.e. on push).

## Pages

| Page | URL |
|---|---|
| Homepage | `/` |
| About Us | `/about/` |
| What is Korfball? | `/what-is-korfball/` |
| Join Us | `/join-us/` |
| Events | `/events/` |
| FAQ | `/faq/` |
| Glossary | `/glossary/` |
| Testimonials | `/testimonials/` |
| Sponsors | `/sponsors/` |
| Support Us | `/support/` |
| Contact | `/contact/` |
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

## Service Worker

`sw.js` is **network-first for HTML** and stale-while-revalidate for assets. This matters:
an earlier cache-first version meant returning visitors never saw content updates.

Bump `CACHE_VERSION` in `sw.js` when changing the precache list.

## SEO

- `jekyll-seo-tag` handles titles, canonicals, Open Graph and Twitter cards
- JSON-LD: Organization, WebSite, SportsTeam, SportsActivityLocation, Event, FAQPage,
  HowTo, BreadcrumbList
- `llms.txt` provides a plain-text summary for AI crawlers
- Generated `sitemap.xml` and Atom `feed.xml`

## Deployment

Pushing to `master` deploys automatically via GitHub Pages.

The `.github/workflows/minify-all-css.yml` workflow minifies `assets/css/*.css` on push and
commits the `.min.css` files back.

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
