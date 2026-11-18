# website

The whole of matt-jones.org (www.matt-jones.org redirects to it). Every page is a plain HTML file in this repo, served by
GitHub Pages. To change the site, edit a file and push to `main`. It's live a minute later.

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

All pages share the home page's navigation. Links between pages are root-relative (`/about/`),
and the Software/Baseball menu items go to each project's own page.

Deploys run from `.github/workflows/pages.yml` on every push to `main`
(Settings → Pages → Source: **GitHub Actions**).

Every page loads `assets/site.css` and `assets/site.js`: the theme toggle, the phone menu, the current-page
highlight, the scroll progress bar and shared polish. Change those two files to change all pages at once.

The LLMAdness, Bullzen and Windhover demos are edited in `_build/<page>.html` and written into their pages
with `python3 _build/build.py`, which also writes `404.html`. Black Ink and Scouting Report came from the `calendar` repo.

`python3 _build/meta.py` writes each page's description and share tags (edit the text in that file), plus
`sitemap.xml` and `robots.txt`. `/hibob/` is left out of the sitemap. `assets/og.png` is the share image.

Other files: `CNAME` (records the custom domain; the live setting is in Settings → Pages), `.nojekyll` (serve files as-is),
`favicon.svg`. DNS and email setup is in `dns/records.md`.

`python3 _build/check.py` checks every internal link, anchor and page's metadata. It runs on each pull request
(`.github/workflows/check.yml`), which also fails if a generated page was edited by hand instead of through `_build/`.
