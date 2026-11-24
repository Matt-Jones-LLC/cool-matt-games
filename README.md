# Cool Matt Games

Free browser games at **[coolmatt.games](https://coolmatt.games)**. No ads, no sign-up, no feed.
Made by Matt Jones in Houston, Texas.

It is a nod to the math-games site that got a lot of us through the school day: somewhere you go on
purpose, play for five minutes, and leave feeling a little better. This repository is the whole site:
plain HTML, CSS and JavaScript with no build step. Run it with `python3 -m http.server 4175`; every
push to `main` deploys to GitHub Pages.

## The games

| Game | What you do | Play |
|------|-------------|------|
| **Overnight Shift** | You are the only support agent online. Pop every ticket before it floats away and hold the queue until 8 AM. | [coolmatt.games/games/overnight-shift](https://coolmatt.games/games/overnight-shift/) |
| **SHAPES** | An RPG where you start as a dot. Fight, level up, and recruit a party that becomes a line, a triangle, a square and a pentagon. | [coolmatt.games/games/shapes](https://coolmatt.games/games/shapes/) |
| **Corner Shot** | A logo bounces around like an old screensaver. Tap the moment it hits a corner. One button. | [coolmatt.games/games/corner-shot](https://coolmatt.games/games/corner-shot/) |
| **TheBomb.com** | Run one website through 1996, 2003, 2012 and 2028. Write the code, answer the messages, get rich, lose it, and take the time machine back. | [coolmatt.games/games/thebomb](https://coolmatt.games/games/thebomb/) |

Every game is original, works with a mouse or a finger, and keeps its scores and saves in your own
browser.

## Who made this

Matt Jones has spent five years on the technical side of customer experience and builds websites
after hours. There is more at [matt-jones.org](https://matt-jones.org/). Overnight Shift
is based on his real job.

## How it is built

Plain HTML, CSS and JavaScript. There is no framework, no build step and no web font. What is in
this repository is exactly what gets served.

The site makes no request to any other server unless a visitor turns on the optional diagnostics
described below.

| Path | What it is |
|------|------------|
| `index.html` | The arcade: featured game and the shelf of all games |
| `about/index.html` | A redirect to the About section at matt-jones.org |
| `games/<name>/index.html` | One game per folder, with its script (and stylesheet, if it has one) beside it |
| `404.html` | The not-found page |
| `assets/site.css` | The shared look: Frutiger Aero sky and glass, with Y2K window chrome |
| `assets/site.js` | Background bubbles, the "games played on this device" counter, and the shared sound player (`CMG.sfx`) |
| `assets/gifs/` | The moving pixel art, each with a still image for visitors who ask for reduced motion |
| `assets/sounds/` | Recorded sound effects for the games. Each game falls back to its own synthesized beeps if a file has not loaded |
| `credits/index.html` | Who made each sound, with its license and source |
| `assets/monitoring.js`, `assets/monitoring-config.js` | The optional diagnostics |
| `sitemap.xml`, `robots.txt`, `favicon.svg` | The usual |
| `CNAME`, `.nojekyll` | The custom domain, and "serve these files as they are" |
| `dns/` | DNS notes and a lookup script for matt-jones.org, from before the move to coolmatt.games |

## Optional diagnostics

Every page has a diagnostics control, and it is off until a visitor turns it on.

- Turning it on loads Datadog's browser monitoring and shares page visits, device details, errors
  and game-start counts with Datadog. There is no session replay.
- It stays off, with no way to turn it on, when the browser sends Global Privacy Control or Do Not
  Track.
- It does nothing on preview and local addresses.
- The client token in `assets/monitoring-config.js` is the public kind that is meant to sit in
  browser code. API keys and application keys never belong in this repository.

## Run it locally

```bash
python3 -m http.server 4175
```

Then open http://localhost:4175. Links are root-relative, so use a server and not a file path.

Each game puts a small hook on `window` (`OvernightShift`, `Shapes`, `CornerShot`, `TheBomb`) for
reading state and stepping time by hand from the browser console.

## Add a game

1. Copy `games/overnight-shift/` to `games/<new-name>/` and replace `game.js`.
2. Add a card to the shelf in `index.html`, a line to `sitemap.xml`, and a row to the table above.
3. Check it against the house rules:
   - Original games only. A genre is fine; a copy of someone else's game is not.
   - The rules fit in one "How to play" box, and the first ten seconds teach the game.
   - Mouse, touch and keyboard all work. Every control outside the canvas is a real button.
   - Sound starts on the first tap and can be muted.
   - The game pauses when the tab is hidden.
   - Scores and saves go in `localStorage` under `cmg:<game>:...` and stay in the browser.
   - It fits a phone screen at 375 by 812 with no sideways scroll.

## How it is published

GitHub Pages serves the site from this repository at the custom domain `coolmatt.games`.
`www.coolmatt.games` redirects to it. `coolmattgames.io` is the separate experimental lab.

- Every push to `main` runs `.github/workflows/pages.yml`, which copies the site into the Pages
  artifact and deploys it. It is live about a minute later.
- The workflow leaves out `README.md`, `LICENSE`, `dns/` and `.github/`.
- Pages is set to **Source: GitHub Actions** with **Enforce HTTPS** on (Settings → Pages). With
  that source GitHub takes the custom domain from the Pages setting, not from the `CNAME` file;
  the file is kept so the two say the same thing.

### Renaming or moving the repository

The site does not depend on this repository's name. It was called `website` until November 2026;
the old address still redirects here.

- **Renaming it** changes nothing for visitors. The custom domain stays attached, GitHub redirects
  the old repository address, and DNS stays as it is.
- **Moving it to a different repository** takes four steps, in this order:
  1. Push everything here to the new repository. Nothing is generated, so nothing is left behind.
  2. In the old repository, remove the custom domain (Settings → Pages). A domain can be attached
     to one repository at a time.
  3. In the new repository, set Settings → Pages → Source to GitHub Actions, add `coolmatt.games`
     as the custom domain, and turn on Enforce HTTPS once the certificate is issued.
  4. Push to `main` once to trigger the first deploy.
- DNS only changes if the new repository belongs to a **different GitHub account**. Then the `www`
  record must point at `<that-account>.github.io`. The four `A` and four `AAAA` records stay the
  same either way.

Expect a few minutes where the domain shows GitHub's 404 page between steps 2 and 4.

## History

The site started at matt-jones.org and moved to coolmatt.games in November 2026. matt-jones.org
now carries Matt Jones, LLC's own page, which links here. The earlier matt-jones.org (a portfolio,
baseball pages and tool demos) is still in this repository's history, before the commit "Rebuild
the site as Cool Matt Games".

## License

The code is under the Apache License 2.0; see `LICENSE`.

The recordings in `assets/sounds/` are other people's work, found through Openverse and downloaded
from Freesound. Fifteen are CC0 and four are CC BY 4.0; `credits/index.html` lists every one with
its maker, license and source, and that page must stay published while the CC BY sounds are in use.
