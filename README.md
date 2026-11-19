# Cool Matt Games

The whole of matt-jones.org (www.matt-jones.org redirects to it): a small portal of games, tools, toys and widgets
by Matt Jones. Plain HTML, CSS and JavaScript, served by GitHub Pages. Pushing to `main` deploys it a minute later.

## Changing the site

Don't edit the pages at the top level by hand. They are written by the build:

```bash
python3 _build/site.py
```

| To change…                         | Edit                                                    |
|------------------------------------|---------------------------------------------------------|
| A game, tool, toy or widget        | `_build/src/pieces/<slug>.html`                         |
| The home page                      | `_build/src/home.html`                                  |
| The about page, the 404 page       | `_build/src/about.html`, `_build/src/404.html`          |
| What's on the site, names, blurbs  | the `PIECES` list at the top of `_build/site.py`        |
| Header, footer, page metadata      | `_build/site.py`                                        |
| Colours, type, shared components   | `assets/site.css`                                       |
| The light/dark switch              | `assets/site.js`                                        |

A piece file is an optional `<style>`, then markup, then a `<script>`. The build wraps it in the shared header
and footer and adds its title and description from `PIECES`. The first line can be `<!--lede: … -->` to set the
paragraph under the title.

To add a piece: write `_build/src/pieces/<slug>.html`, add a row to `PIECES`, run the build, then retake the
thumbnails (below). The home page shelves, the sitemap and the "next" links all follow from `PIECES`.

## What's here

| Shelf   | Pieces                                                        |
|---------|---------------------------------------------------------------|
| Games   | Slick Shift, Goldfish, Second Opinion, LLMAdness              |
| Tools   | Context Budget, Cry Wolf, Windhover                           |
| Toys    | Thermostat, Downhill, Breather                                |
| Widgets | Follow the Sun, Book a time (`/calendar/`)                    |

`/hibob/` is a standalone page with its own styles. It isn't built by `site.py` and isn't in the sitemap.

Old addresses (`/box-score/`, `/the-bullzen/`, `/portfolio/`, `/magic-number/`, `/black-ink/`,
`/scouting-report/`) are redirect stubs, listed in `REDIRECTS` in `_build/site.py`.

## Slick Shift levels

The twelve levels are chosen by a program, not drawn by hand:

```bash
node _build/levels.js
```

It makes thousands of random floor plans per level, solves each with the game's own solver, keeps the one with
the longest shortest solution, and writes the result into `_build/src/pieces/slick-shift.html`. The level list
(sizes, ingredients, target length) is `SPEC` at the top of that script. The random numbers are seeded, so the
same levels come out each time unless `SPEC` or the seed changes.

## Thumbnails and share image

Home-page thumbnails are screenshots of the real pieces in `assets/shots/`. To retake them (needs Playwright):

```bash
python3 -m http.server 8123 &
```

```bash
node _build/shots.js
```

`assets/og.png` is the image shown when a link is shared. `assets/apple-touch-icon.png` and `favicon.svg` are the icons.

## Checks and deploys

`python3 _build/check.py` checks every internal link, anchor and page's metadata. It runs on each pull request
(`.github/workflows/check.yml`), which also fails if a built page doesn't match what `_build/site.py` produces.

Deploys run from `.github/workflows/pages.yml` on every push to `main` (Settings → Pages → Source: **GitHub Actions**).

Other files: `CNAME` (the custom domain), `.nojekyll` (serve files as-is), `dns/records.md` (DNS and email setup).
