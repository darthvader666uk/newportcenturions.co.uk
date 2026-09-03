# Newport Centurions — Audit & Work Tracker

**Audited:** 2026-09-02 · **Host:** GitHub Pages · **Branch:** master

Everything found, ordered easiest → hardest. `[x]` = done and verified.

---

## Batch 1 — committed separately (28 items)

Tier 1 (trivial), Tier 2 (easy) and Tier 3 (service worker, `club.yml`, announcement bar,
privacy/consent). See that commit message for the full breakdown.

---

## Batch 2 — the remainder

### Done

| # | Item | Status |
|---|---|---|
| 1 | `events.md` hardcoded the same four dates in three places (schema, cards, SR list) | [x] fully driven by `club.yml`; `season.beginner_sessions` → `season.events` with a `beginner:` flag shared with the announcement bar |
| 2 | Announcement bar only filtered past dates at build time | [x] now filters at build time *and* in the browser, so it self-corrects between rebuilds |
| 3 | No rebuild between pushes, so build-time date filtering could go stale | [x] `scheduled-rebuild.yml` — nightly Pages build via API, no empty commits |
| 4 | Training times / venue still hardcoded in prose and 3 schema includes | [x] shared `_includes/training.html`; threaded through `ai-answer-snippets`, `ai-article-schema`, `ai-howto-schema`, `join`, `contact`, `glossary`, `support`, `what-is-korfball` |
| 5 | Footer showed 24-hour times while every other page used 12-hour | [x] unified via the shared include |
| 6 | Google Fonts loaded render-blocking from the page body on `/testimonials/` | [x] self-hosted + subset. Rubik Distressed 300KB → 82KB (uppercase-only, matching `text-transform: uppercase`) |
| 7 | **Google Maps iframe** on `/contact/` loaded on page view, setting third-party cookies before consent | [x] click-to-load facade + a plain "Open in Google Maps" link |
| 8 | **YouTube iframe** on `/what-is-korfball/` — same problem | [x] click-to-load facade, switched to `youtube-nocookie.com` |
| 9 | ~~No news/results section~~ | **REVERTED** — you don't want a news section. `_posts/`, the post layout, `/news/`, the post CSS and `jekyll-feed` are all removed. The feed only ever generated zero items, so it went too. |
| 10 | **`include_relative` in the layout broke any page outside the repo root** — the site would have failed to build the moment a post was added | [x] `critical.css` moved to `_includes/`, layout uses `include`; CI minifier updated to cover both directories |
| 11 | `SearchAction` schema was removed in batch 1 because `/search/` didn't exist | [x] built client-side search (`search.json` + `/search/`), schema restored pointing at a real page |
| 12 | `/search/` was `noindex` but still listed in the sitemap | [x] `sitemap: false` |
| 13 | **Black headings on a dark card** on `/thank-you/` — inline `color: #000` over `rgba(255,255,255,0.05)`, effectively invisible text | [x] fixed via `.thankyou-card` class |
| 14 | `/thank-you/` fired a `confirm()` popup after 30 seconds asking to redirect | [x] removed |
| 15 | ~44 inline `style=` attributes across source files | [x] down to 8, all legitimate one-offs (honeypot `display:none`, dynamic `aspect-ratio`). Shared `.page-cta`, `.media-block`, `.youtube-link`, `.site-logo` classes added |
| 16 | Glossary, News and Search missing from navigation | [x] all added |
| 17 | README didn't describe posts, search, embeds, fonts or the new workflows | [x] updated |

### Verified after every change

- Clean build; **71 JSON-LD blocks, 0 invalid**
- 16 pages; exactly one `<main>` and one `<h1>` each; zero images missing `alt`
- **24 internal link targets, 0 broken**
- **0 iframes and 0 gtag script tags load on page view**
- Search ranking spot-checked: `"what is korfball"` → `/what-is-korfball/`, `"how do i join"` → `/join-us/`, `"sponsors"` → `/sponsors/`
- Post pipeline validated end-to-end with a throwaway post (URL, feed entry, sitemap, schema, news index), then removed

---

## Batch 3

| Item | Status |
|---|---|
| News section removed at your request — `_posts/`, `_layouts/post.html`, `news.md`, post CSS, nav entry, config defaults | [x] |
| `jekyll-feed` and `feed.xml` removed — the feed only ever generated zero items and nothing will ever populate it | [x] also dropped from `Gemfile`, `robots.txt` and the layout's `rel=alternate` |
| Windows `Zone.Identifier` artefacts were being copied into the built site | [x] excluded |
| **Fixtures auto-loaded from Google Calendar** | [x] see below |

### Fixtures pipeline

`sync-fixtures.yml` fetches the calendar's `.ics` nightly, `sync-fixtures.py` converts it to
`_data/fixtures.yml`, and commits only on change. `/fixtures/` renders that as static HTML.

Chosen over an iframe embed because the fixtures end up **indexable by Google**, carry
`SportsEvent` schema, match the site theme, work with JS off, and load no third-party code —
matching the click-to-load approach taken for the map and video.

Tested against a synthetic calendar covering timed events, all-day events, escaped commas in
`LOCATION`, and an `RRULE` (correctly expanded to individual dates). Upcoming/past split,
home/away inference and schema output all verified.

**Calendar access:** the club calendar is private — anonymous requests to both the embed and
the public iCal URL return 401/404. That's fine for this design: the sync turns the calendar
into committed data, so visitors never touch it. (Worth noting the iframe-embed alternative
would *not* have worked — logged-out visitors would have seen an error.)

Needs the **secret iCal address** added as a repository **secret** named `FIXTURES_ICS_URL`.
Secret, not variable: the repo is public and only secrets are masked in Actions logs. The
script never prints the URL and refuses anything that isn't a `.ics`.

Error paths tested: unset URL (exits 0, no-op), non-`.ics` URL, and a real 401/403/404 —
each gives an actionable message rather than a traceback.

## In progress

- [ ] **`FIXTURES_ICS_URL`** — add the calendar's *Secret address in iCal format* as a
      repository **secret** (Settings → Secrets and variables → Actions → Secrets), then run
      *Sync Fixtures* from the Actions tab. `/fixtures/` populates itself from then on.
      Full steps in the README.

## Parked

<!-- PHOTOGRAPHY — parked 2026-09-03, no photos available yet.
     Un-park when the club has usable images.

     Current state: 6 images total — 3 logo sizes, 2 kit shots, 1 fundraising
     sticker. No team photos, no action shots, no venue photo.

     Worth doing when photos exist, because it is the biggest remaining win for
     the join-us conversion path. A prospective member currently cannot see what
     a session actually looks like.

     When the time comes, in rough priority order:
       1. One wide action shot for the homepage hero / og:image
       2. A team photo for /about/
       3. A venue/sports-hall shot for /contact/ and /join-us/, so beginners
          know what they are walking into
       4. Two or three candid session shots for /testimonials/

     The site already handles images properly — WebP with srcset, explicit
     width/height, lazy loading below the fold — so this is a content job, not
     a code one. -->

- [ ] **Photography** — parked, no photos available. Details in the HTML comment above.

## Batch 4 — SEO & AI-search pass

### Fixed

| Item | Status |
|---|---|
| **Hidden content carrying structured data, in 3 places** — `ai-answer-snippets.html`, `ai-testimonials-schema.html` and a block in `what-is-korfball.md` were all `display:none` while carrying `Question`/`Answer` microdata. That breaks Google's rule against marking up content readers can't see (manual-action risk), and hidden text carries no ranking weight, so it was pure downside. | [x] what-is-korfball's became a visible "at a glance" summary; the testimonials one was deleted. The homepage block was first made visible, then removed entirely (too cluttered) — all six Q&As already live on `/faq/`, so nothing was lost and the include was deleted. **0 violations remain.** |
| **Every page title repeated the brand twice** — "About Newport Centurions Korfball Club \| Newport Centurions Korfball Club" (73 chars), because jekyll-seo-tag appends `site.title` to titles that already contained it. Half the SERP budget wasted on every page. | [x] all 16 titles rewritten, now **41–58 chars** (was 64–93, every one over the limit) |
| Homepage had **six `h3`s before its `h1`** (the hidden block sat above the hero) | [x] h1 now first; order is h1 → h2 → h2 → h2 → h3s |
| `what-is-korfball` opened with an `h2` before the `h1` | [x] fixed |
| `h1 → h3` skips on about, contact, join-us; `h2 → h4` skip on **every** page (footer used `h4`) | [x] footer → `h2`, card headings promoted, about's timeline `h4`s → `h3` |
| **Club `Organization` entity fragmented** — repeated as separate inline nodes instead of referencing the canonical `@id`, so parsers saw several unrelated orgs with the same name. `sponsors.md` even used `…co.uk#organization` (no slash), a genuinely *different* entity from `…co.uk/#organization`. | [x] all now reference one canonical `@id`; verified a single `@id` form site-wide |
| `robots.txt` said nothing about AI crawlers, and let the thin `/search/` page and `search.json` be indexed | [x] **20 AI/search agents explicitly allowed** (GPTBot, ClaudeBot, PerplexityBot, Google-Extended, CCBot, Applebot-Extended, Amazonbot, meta-externalagent, MistralAI-User, YouBot…), `/search/` and `search.json` disallowed |
| Breadcrumbs existed only as schema, no visible trail | [x] visible breadcrumb nav on all 13 content pages, driven by the same `page.breadcrumb` front matter — schema and UI can't drift apart |
| `/events/` duplicated every visible event into an `sr-only` block — screen-reader users heard each event twice, for no crawler benefit | [x] removed |
| Homepage was thin at 482 words | [x] ~444 words of chrome + a real 6-question FAQ section |

### Result

**16/16 pages clean.** 72 JSON-LD blocks all parsing, one `<main>` and one `<h1>` per page,
zero images missing `alt`, 23 internal links all resolving, zero hidden-schema violations.

### Worth knowing

`FAQPage` and `HowTo` schema no longer produce Google **rich results** — Google restricted
FAQ rich results to government/health sites in Aug 2023 and deprecated HowTo entirely in
Sept 2023. Both are kept because LLMs and answer engines still parse them, which is what
this pass was for — but don't expect FAQ accordions in Google's SERP.

## Accepted limitations

- **Security headers** (CSP, `X-Frame-Options`, `Referrer-Policy`) are impossible on GitHub
  Pages, which cannot set custom HTTP response headers. Decision was to stay on Pages; the
  README now states this accurately rather than claiming headers that never applied. Moving
  to Cloudflare Pages or Netlify (both support a `_headers` file) is the only fix.
- **`sitemap.xml` lost its image schemas and per-page priorities** when we moved to
  `jekyll-sitemap`. That was the accepted trade for not maintaining it by hand; neither is a
  ranking factor Google documents using.
