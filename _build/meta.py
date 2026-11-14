"""Write the description / Open Graph block into every page, plus sitemap.xml and robots.txt. Safe to re-run."""
import re, pathlib
root = pathlib.Path(__file__).parent.parent
SITE = "https://matt-jones.org"
PAGES = {
    "": "Matt Jones — a website about nothing. Small tools built on Claude, support work, and baseball math.",
    "about": "About Matt Jones: utility player who builds small tools on Claude, writes the occasional post, and keeps score.",
    "portfolio": "The full lineup: software toys, support work, and baseball math by Matt Jones.",
    "llmadness": "LLMAdness: a humor bracket for Grok, Claude, Gemini and ChatGPT. Same prompt, both models, you call the games.",
    "cry-wolf": "Cry Wolf: a circle-vs-polygon geofencing sandbox. Run a truck past a warehouse and see which fence cries wolf.",
    "the-bullzen": "The Bullzen: calm from the bullpen. A breathing pacer built around a reliever's warm-up routine.",
    "windhover": "Windhover: a geofence QA/QC simulator. Fly over a plat and catch the fences that will lie to you.",
    "magic-number": "Magic Number: how close is clinched? A calculator for the pennant race.",
    "black-ink": "Black Ink: tally a hitter's league-leading seasons into a Bill James Black Ink score.",
    "scouting-report": "Scouting Report: the 20-80 scale explained with a five-tool sample report.",
    "box-score": "Box Score: the support work that keeps the operation running, told the way a box score tells a game.",
    "calendar": "Book a time with Matt Jones: pick a day and a window, and the email writes itself.",
    "hibob": "Matt Jones for HiBob Customer Experience: Follow the Sun, an interactive map of five CX pods sharing one queue.",
}
for slug, desc in PAGES.items():
    f = root / slug / "index.html"; s = f.read_text()
    title = re.search(r"<title>(.*?)</title>", s).group(1)
    url = f"{SITE}/{slug + '/' if slug else ''}"
    block = ("<!--meta-->"
        f'<meta name="description" content="{desc}">'
        f'<link rel="canonical" href="{url}">'
        f'<meta property="og:type" content="website"><meta property="og:site_name" content="Matt Jones">'
        f'<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">'
        f'<meta property="og:url" content="{url}"><meta property="og:image" content="{SITE}/assets/og.png">'
        '<meta name="twitter:card" content="summary_large_image">'
        "<!--/meta-->")
    s = re.sub(r"<!--meta-->.*?<!--/meta-->", "", s, flags=re.S)
    s = re.sub(r'\n?<meta name="description"[^>]*>', "", s)
    s = s.replace("</title>", "</title>" + block, 1)
    f.write_text(s)
urls = "\n".join(f"  <url><loc>{SITE}/{slug + '/' if slug else ''}</loc></url>" for slug in PAGES if slug != "hibob")
(root / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n')
(root / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
print("meta written for", len(PAGES), "pages")
