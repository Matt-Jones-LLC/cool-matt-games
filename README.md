# Cool Matt Games

The whole of matt-jones.org (www.matt-jones.org redirects to it): a small arcade of free browser games,
plus a page about Matt. Plain HTML, CSS and JavaScript, served by GitHub Pages. No build step, no
frameworks, no third-party requests.

To change the site, edit a file and push to `main`. It's live about a minute later.

| URL                        | File                               | What it is                          |
|----------------------------|------------------------------------|-------------------------------------|
| `/`                        | `index.html`                       | The arcade: featured game and shelf |
| `/about/`                  | `about/index.html`                 | About Matt                          |
| `/games/overnight-shift/`  | `games/overnight-shift/index.html` | Game 1 (`game.js` beside it)        |
| `/games/shapes/`           | `games/shapes/index.html`          | Game 2, an RPG (`shapes.js`, `shp.css`) |
| `/games/corner-shot/`      | `games/corner-shot/index.html`     | Game 3, one button (`game.js`)      |
| `/games/thebomb/`          | `games/thebomb/index.html`         | Game 4, internet-history sim (`game.js`, `bomb.css`) |
| any missing page           | `404.html`                         | Not-found page                      |

Shared by every page: `assets/site.css` (the Frutiger Aero / Y2K look) and `assets/site.js`
(background bubbles and the "games played on this device" counter).

## Adding a game

1. Copy `games/overnight-shift/` to `games/<new-name>/` and replace `game.js`.
2. Add a card to the shelf in `index.html` and a line to `sitemap.xml`.
3. Follow the checklist in `.claude/skills/cool-matt-game/SKILL.md` (touch and mouse input, sound that
   starts on the first tap, pause when the tab is hidden, scores kept in `localStorage`).

## Running it locally

```bash
python3 -m http.server 4175
```

Then open http://localhost:4175. Links are root-relative, so open it through a server, not as a file.

## Deploys

`.github/workflows/pages.yml` publishes on every push to `main` (Settings → Pages → Source: GitHub
Actions). It ships the pages, `CNAME`, `favicon.svg`, `robots.txt` and `sitemap.xml`, and leaves out
`README.md`, `LICENSE`, `dns/`, `.github/` and `.claude/`.

Other files: `CNAME` records the custom domain, `.nojekyll` serves files as-is, and DNS and email
setup is in `dns/records.md`.

The previous site (portfolio, baseball pages, demos) was retired in November 2026. It is still in this
repository's history, before the `cool-matt-games` branch.
