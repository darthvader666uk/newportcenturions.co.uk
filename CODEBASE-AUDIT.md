# Newport Centurions — Audit & Work Tracker

**Audited:** 2026-09-02 · **Host:** GitHub Pages · **Branch:** master

Everything found, ordered easiest → hardest. `[x]` = done and verified in this pass.

---

## Tier 1 — Trivial (minutes each) — ALL DONE

| # | Item | Status |
|---|---|---|
| 1 | Dangling `.graymatter` symlink crashed `./dev.sh` and `./build.sh` locally | [x] removed |
| 2 | `_includes/ai-content-enhancement.html` — never included by anything | [x] deleted |
| 3 | `_includes/ai-sponsors-schema.html` — never included; duplicated sponsors.md's inline schema | [x] deleted |
| 4 | `_data/social.yml` — never referenced; social links existed in 4 places | [x] deleted, replaced by `club.yml` |
| 5 | `glossary.md:106` — `assign` referencing a `_data/glossary.yml` that doesn't exist | [x] removed |
| 6 | `index.md` opened a second `<main>` inside the layout's — invalid HTML, 2 landmarks | [x] `<div>` |
| 7 | `/thank-you/` was indexed and in the sitemap | [x] `sitemap: false` + `noindex` |
| 8 | `/404` was `index, follow` | [x] `noindex, follow` |
| 9 | `robots.txt` disallowed `/assets/css/critical.css` and `/404.html` pointlessly | [x] removed |
| 10 | `README.md` + `LICENSE` were published to the live site | [x] excluded from build |
| 11 | Glossary wasn't in the nav — only reachable from body links | [x] added to About submenu |
| 12 | `compress_html:` config was inert (no compress layout existed) | [x] removed |
| 13 | 7 DNS-prefetch hints for origins never fetched (social domains, GA, Google Fonts) | [x] → 1 real preconnect |
| 14 | `"telephone": ""` in LocalBusiness schema — invalid empty value | [x] removed |

## Tier 2 — Easy (under an hour) — ALL DONE

| # | Item | Status |
|---|---|---|
| 15 | **Two `FAQPage` blocks** on `/faq/` — a 6-question include *and* a 16-question inline block | [x] kept the richer inline one, deleted the include |
| 16 | **Two `BreadcrumbList` blocks** on `/events/` and `/sponsors/` | [x] inline ones removed |
| 17 | Layout's 60-line breadcrumb `elsif` chain emitted a **Home-only breadcrumb** on `/events/`, `/testimonials/`, `/thank-you/`, `/404` | [x] replaced with `page.breadcrumb` front matter, 10 pages tagged |
| 18 | `ai-local-business-schema` was included on **every** page — the 404 advertised opening hours | [x] scoped off 404 / thank-you |
| 19 | `security.txt` expired 2025-12-31, pointed at two 404s, wrong contact email | [x] refreshed to 2027, dead links dropped, email aligned |
| 20 | `.htaccess` was **inert** on GitHub Pages and served publicly at `/.htaccess` | [x] deleted *(decision: stay on GH Pages)* |
| 21 | Hand-written `sitemap.xml` / `feed.xml` overrode the plugins; feed generated 0 items | [x] deleted, `jekyll-sitemap` + `jekyll-feed` now generate them *(decision)* |
| 22 | `SearchAction` schema advertised `/search?q=` — a page that doesn't exist | [x] removed |
| 23 | No CI verified the site builds before Pages published it | [x] `build-check.yml`: build + JSON-LD validation + htmlproofer |
| 24 | README claimed a `pages/` dir, a `social.md`, "Netlify-compatible" form, FA 6.4.0, and security headers — all false | [x] rewritten |

## Tier 3 — Medium (the real work) — ALL DONE

| # | Item | Status |
|---|---|---|
| 25 | **Service worker served stale HTML forever.** Cache-first on navigations meant returning visitors never saw updated dates or content until `CACHE_NAME` was manually bumped | [x] rewritten: network-first for HTML, stale-while-revalidate for assets, offline fallback, analytics never intercepted |
| 26 | **No single source of truth.** Training times, venue, dates, fees hardcoded across 19 files | [x] `_data/club.yml` created and threaded through the layout, footer, homepage, announcement bar, `llms.txt`, and both schema includes |
| 27 | **Announcement bar advertised a past date** ("Season Back Aug 18!") on every page | [x] now renders only *upcoming* beginner sessions from `club.yml`, with an evergreen fallback |
| 28 | **GA4 fired before consent**, no privacy policy — UK GDPR / PECR exposure | [x] `/privacy/` page + self-hosted consent banner; GA4 loads only on accept, declining clears `_ga*` cookies, choice re-openable from the policy page |

**Verified after every change:** clean build, 63 JSON-LD blocks all parsing, 1 `<main>` per page, 1 breadcrumb per content page, 0 gtag script tags before consent, thank-you/404 out of the sitemap.

---

## Remaining — not yet done

### Small

- [ ] **Google Fonts on `/testimonials/`** — loaded via a render-blocking `<link rel="stylesheet">` in the page body, and it's the only page using it. Now disclosed in the privacy policy, but self-hosting the two fonts would remove a third party and speed the page up.
- [ ] **~80 inline `style=` attributes** across pages (`thank-you.md` is the worst). Should be classes in `styles.css`.
- [ ] **Remaining hardcoded club facts in prose.** `club.yml` covers the structured data and chrome, but body copy still repeats training times and dates: `events.md` (24 occurrences), `faq.md` (11), `contact.md`/`join.md`/`glossary.md` (3 each). Tedious but mechanical.
- [ ] **`events.md` duplicates `club.yml`** — its `Event` schema, visible cards and screen-reader list all hardcode the same four dates. Best candidate for the next threading pass.

### Medium

- [ ] **Nightly rebuild.** Past-date filtering happens at *build* time, so a session date only drops off the announcement bar on the next push. A scheduled workflow would keep it honest without manual pushes.
- [ ] **News / match reports (`_posts`).** There are none. The RSS feed, sitemap post-loop and Atom feed are all wired and empty. This is the content that earns repeat visits and backlinks for a 3× champion club.
- [ ] **Site search.** `SearchAction` was removed rather than faked. If you want search, a client-side index over 13 pages is straightforward — then the schema can come back.

### Larger / needs you

- [ ] **Photography.** 6 images total: 3 logo sizes, 2 kit shots, 1 fundraising sticker. No team photos, no action shots, no venue photo. Single biggest win for the join-us conversion path — and it needs real photos, not code.
- [ ] **Fixtures / league table page.** The obvious missing page for a competitive club.
- [ ] **Security headers.** Genuinely impossible on GitHub Pages (no custom response headers). Only fixable by moving to Cloudflare Pages or Netlify, which support a `_headers` file. Decision was to stay put; the README now states this accurately instead of claiming headers that never applied.
