# website

Matt Jones' personal site: a home page, about and portfolio pages, and one page per software or
baseball project. Every page is a single self-contained HTML file (inline CSS and JavaScript, no
build step, no dependencies), set up for GitHub Pages.

These pages formerly served matt-jones.org from this repository's `main` branch. Since then:

- matt-jones.org serves the Matt Jones, LLC company site from
  [Matt-Jones-LLC/matt-jones.org](https://github.com/Matt-Jones-LLC/matt-jones.org).
- This repository was renamed to
  [matt-jones-org/cool-matt-games](https://github.com/matt-jones-org/cool-matt-games) (the old
  `matt-jones-org/website` URL redirects), and its `main` branch is now the
  [coolmatt.games](https://coolmatt.games) arcade.

So the personal site lives on this branch, and nothing deploys it from here. The `CNAME` file
still says `matt-jones.org` from the old setup.

## Pages

| URL                | File                         | Source artifact                                      |
|--------------------|------------------------------|------------------------------------------------------|
| `/`                | `index.html`                 | https://claude.ai/artifact/TGhtdA8T1X5fsLt4jXsJY4     |
| `/about/`          | `about/index.html`           | https://claude.ai/artifact/JqRqbw3dcAUc5vTABHmDZh     |
| `/portfolio/`      | `portfolio/index.html`       | https://claude.ai/artifact/WuMVcF6xXq8CiN2TXFhn5F     |
| `/llmadness/`      | `llmadness/index.html`       | https://claude.ai/artifact/UVouknyBkNFhi2xJ7BNXG4     |
| `/cry-wolf/`       | `cry-wolf/index.html`        | https://claude.ai/artifact/So6Z9AVdLh8bn3wAcnXend     |
| `/the-bullzen/`    | `the-bullzen/index.html`     | https://claude.ai/artifact/UWu1gzHTaLhJ2v7jcKv8xF     |
| `/windhover/`      | `windhover/index.html`       | https://claude.ai/artifact/7nmwCHQEbXMEfrC3Y3txc4     |
| `/box-score/`      | `box-score/index.html`       | https://claude.ai/artifact/UXTCNygjkXYcrWgoy5waL8     |
| `/magic-number/`   | `magic-number/index.html`    | https://claude.ai/artifact/HznnrVY3diFQ8kEpBujQmP     |
| `/black-ink/`      | `black-ink/index.html`       | https://claude.ai/artifact/KLV6u3oNPKcVYjJmamTFfM     |
| `/scouting-report/`| `scouting-report/index.html` | https://claude.ai/artifact/3Fr6gd1HEpu54tweJqJvbH     |
| `/calendar/`       | `calendar/index.html`        | https://claude.ai/artifact/JsQ4mVArGFjEv2Nu2maNrx     |
| `/hibob/`          | `hibob/index.html`           | Built in the repo (Follow the Sun, HiBob styling)     |
| `/skills/`         | `skills/index.html`          | Built in the repo (scouting-report skills page)       |

All pages share the home page's navigation. Links between pages are root-relative (`/about/`),
and the Software/Baseball menu items go to each project's own page. The Follow the Sun map on the
home page and on `/hibob/` is the same script; change both together.

## Previewing locally

Because links are root-relative, serve the repo root rather than opening files directly:

```sh
python3 -m http.server 8000
# http://localhost:8000/
```

## Deploying

The workflow on this branch, `.github/workflows/pages.yml`, deploys on push to `main` (Settings → Pages → Source:
**GitHub Actions**). It copies everything except `README.md`, `LICENSE`, `dns/` and `.github/`
into `_site` and publishes that. Since `main` is now the arcade, merging this branch there would
replace the arcade; publishing the personal site again needs its own repo or Pages setup.

## Other files

- `CNAME`: left over from when this branch's content served matt-jones.org (see above).
- `.nojekyll`: serve files as-is.
- `favicon.svg`: shared icon.
- `dns/records.md`, `dns/check.sh`: DNS and Google Workspace email records for matt-jones.org,
  written when this repo served the domain, and a script that shows what public DNS returns.
