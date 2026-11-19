"""Build Cool Matt Games (matt-jones.org). Run:  python3 _build/site.py

Every page is written from a source file in _build/src/ wrapped in the shared header and footer below.
The catalogue (PIECES) is the single list of what is on the site: the home page shelves, the nav,
each piece's page, the sitemap and the redirects all come from it."""
import html, pathlib, re

here = pathlib.Path(__file__).parent
root = here.parent
src = here / "src"
SITE = "https://matt-jones.org"
EMAIL = "mscottjones24@gmail.com"
LINKEDIN = "https://www.linkedin.com/in/mattjoneshtx"

KINDS = {
    "games":   ("Games",   "Play", "Things with a score. Each one takes a couple of minutes."),
    "tools":   ("Tools",   "Open", "Things that do a job: check a boundary, plan a prompt, find a time."),
    "toys":    ("Toys",    "Poke", "Nothing to win. Move a slider and see what happens."),
    "widgets": ("Widgets", "Open", "Small, single-purpose, and happy to sit in a corner of a screen."),
}

# slug, kind, title, one line for the shelf, description for search and sharing
PIECES = [
    ("slick-shift", "games", "Slick Shift",
     "A sliding-robot puzzle on a freshly waxed floor. Twelve levels, seven kinds of trouble.",
     "Slick Shift: a sliding-robot puzzle game with twelve levels. Collect the batteries, dodge the pits, reach the charger."),
    ("goldfish", "games", "Goldfish",
     "You are a model with a very short memory. Words stream past; say which ones you still hold.",
     "Goldfish: a memory game about context windows. Words stream past and you say which ones are still in context."),
    ("second-opinion", "games", "Second Opinion",
     "Grade nine support replies, then see how a reviewer graded the same ones.",
     "Second Opinion: a calibration game. Grade nine customer support replies, then compare your calls with a reviewer's."),
    ("llmadness", "games", "LLMAdness",
     "A four-model comedy bracket. Same prompt to both sides, and you pick the funnier answer.",
     "LLMAdness: a humor bracket for Grok, Claude, Gemini and ChatGPT. Same prompt, both models, you pick the winner."),
    ("context-budget", "tools", "Context Budget",
     "Plan what goes into a context window and see how many turns fit before it fills up.",
     "Context Budget: plan a model's context window. Split it between prompt, tools, documents and history, and see when it fills."),
    ("cry-wolf", "tools", "Cry Wolf",
     "Drive a truck past a warehouse and compare what a circle fence and a polygon fence report.",
     "Cry Wolf: a circle-versus-polygon geofencing sandbox. Run a truck past a warehouse and see which fence raises false alarms."),
    ("windhover", "tools", "Windhover",
     "Six geofences on a map, four checks each. Drag the corners until every fence passes.",
     "Windhover: a geofence quality checker. Six fences on a plat, four checks each, and handles to fix the ones that fail."),
    ("thermostat", "toys", "Thermostat",
     "A tiny language model with a temperature dial. Turn it up and watch the sentences come apart.",
     "Thermostat: a tiny next-word model with a temperature dial. See how sampling temperature reshapes the odds."),
    ("downhill", "toys", "Downhill",
     "Drop marbles on a bumpy surface and watch gradient descent roll them into the valleys.",
     "Downhill: drop marbles on a loss surface and watch gradient descent find the valleys. Learning rate and momentum included."),
    ("breather", "toys", "Breather",
     "A breathing pacer with three patterns. Follow the circle for a minute.",
     "Breather: a breathing pacer with three patterns. Follow the circle in, hold, and out."),
    ("follow-the-sun", "widgets", "Follow the Sun",
     "Five support teams in five time zones. Drag the clock to see who is on shift and when work changes hands.",
     "Follow the Sun: a live map of five support teams across time zones, showing who is on shift and where the handoffs fall."),
    ("calendar", "widgets", "Book a time",
     "Pick a day and a window, and the email to me writes itself.",
     "Book a time with Matt Jones: pick a day and a window, and the email writes itself."),
]
BY_SLUG = {p[0]: p for p in PIECES}

# Old addresses that moved or were retired.
REDIRECTS = {
    "box-score": "/second-opinion/", "the-bullzen": "/breather/", "portfolio": "/",
    "magic-number": "/", "black-ink": "/", "scouting-report": "/",
}

SUN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z"/></svg>'


def head(title, desc, path, noindex=False):
    url = f"{SITE}{path}"
    meta = '<meta name="robots" content="noindex">' if noindex else (
        f'<meta name="description" content="{html.escape(desc)}">'
        f'<link rel="canonical" href="{url}">'
        '<meta property="og:type" content="website"><meta property="og:site_name" content="Cool Matt Games">'
        f'<meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}">'
        f'<meta property="og:url" content="{url}"><meta property="og:image" content="{SITE}/assets/og.png">'
        '<meta name="twitter:card" content="summary_large_image">')
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
{meta}
<meta name="theme-color" content="#ECEEF8" media="(prefers-color-scheme: light)"><meta name="theme-color" content="#121130" media="(prefers-color-scheme: dark)">
<link rel="icon" href="/favicon.svg"><link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<script>try{{var t=localStorage.getItem('mj-theme');if(t)document.documentElement.dataset.theme=t}}catch(e){{}}</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Recursive:slnt,wght,CASL,CRSV,MONO@-15..0,300..1000,0..1,0..1,0..1&display=swap">
<link rel="stylesheet" href="/assets/site.css">
<script src="/assets/site.js" defer></script>
"""


def bar(current=""):
    links = "".join(
        f'<a href="/#{k}" data-kind="{k}"{" aria-current=\"true\"" if current == k else ""}>{v[0]}</a>' for k, v in KINDS.items())
    about = f'<a href="/about/"{" aria-current=\"page\"" if current == "about" else ""}>About</a>'
    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="bar"><div class="wrap">
  <a class="mark" href="/">Cool Matt Games</a>
  <nav aria-label="Site">{links}{about}<a class="book" href="/calendar/">Book a time</a></nav>
  <button class="theme" type="button" aria-label="Switch colours">{SUN}</button>
</div></header>
"""


FOOT = f"""<footer class="site"><div class="wrap">
  <div><h2>Made by Matt Jones</h2>
  <p>I'm an AI designer. If you'd like a game, tool or widget like these for your own product, get in touch.</p></div>
  <ul>
    <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
    <li><a href="{LINKEDIN}">LinkedIn</a></li>
    <li><a href="/calendar/">Book a time</a></li>
  </ul>
  <p class="legal">© Matt Jones, 2026. Designed and built with Claude.</p>
</div></footer>
"""


def split(text):
    """A source file is: optional <style>…</style>, markup, optional <script>…</script> blocks at the end."""
    style = "".join(re.findall(r"<style>.*?</style>\n?", text, flags=re.S))
    text = re.sub(r"<style>.*?</style>\n?", "", text, flags=re.S)
    m = re.search(r"<script", text)
    body, script = (text[:m.start()], text[m.start():]) if m else (text, "")
    return style, body.strip(), script.strip()


def write(path, content):
    f = root / path.strip("/") / "index.html" if path != "/404" else root / "404.html"
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(content)


def page(path, title, desc, body, style="", script="", current="", kind="", noindex=False):
    k = f' data-kind="{kind}"' if kind else ""
    write(path, head(title, desc, path, noindex) + style + "</head>\n<body>\n" + bar(current)
          + f'<main id="main"{k}>\n{body}\n</main>\n' + FOOT + (script + "\n" if script else "") + "</body>\n</html>\n")


def shelves():
    out = []
    for k, (name, verb, blurb) in KINDS.items():
        items = []
        for slug, kind, title, line, _ in PIECES:
            if kind != k: continue
            items.append(
                f'<a class="item" href="/{slug}/"><div class="shot"><img src="/assets/shots/{slug}.jpg" alt="" loading="lazy" width="720" height="450"></div>'
                f'<div class="label"><h3>{html.escape(title)}</h3><p>{html.escape(line)}</p></div></a>')
        out.append(f'<section class="shelf wrap" id="{k}" data-kind="{k}"><div class="shelf-head"><h2>{name}</h2><p>{blurb}</p></div>'
                   f'<div class="shelf-grid">{"".join(items)}</div></section>')
    return "\n".join(out)


def build():
    # pieces
    for i, (slug, kind, title, line, desc) in enumerate(PIECES):
        style, body, script = split((src / "pieces" / f"{slug}.html").read_text())
        nxt = PIECES[(i + 1) % len(PIECES)]
        lede = re.search(r"<!--lede:(.*?)-->", body, flags=re.S)
        body = re.sub(r"<!--lede:.*?-->\n?", "", body, flags=re.S)
        full = (f'<div class="wrap">\n<header class="piece-head"><a class="kind" href="/#{kind}">{KINDS[kind][0]}</a>'
                f'<h1>{html.escape(title)}</h1><p class="lede">{lede.group(1).strip() if lede else html.escape(line)}</p></header>\n'
                f'{body}\n<nav class="onward" aria-label="More"><a href="/#{kind}">All {KINDS[kind][0].lower()}</a>'
                f'<a class="next" data-kind="{nxt[1]}" href="/{nxt[0]}/">Next: {html.escape(nxt[2])}</a></nav>\n</div>')
        page(f"/{slug}/", f"{title} | Cool Matt Games", desc, full, style, script, current=kind, kind=kind)

    # home
    style, body, script = split((src / "home.html").read_text())
    counts = {k: sum(1 for p in PIECES if p[1] == k) for k in KINDS}
    for k, n in counts.items(): body = body.replace(f"{{n_{k}}}", str(n))
    page("/", "Cool Matt Games | Games, tools, toys and widgets by Matt Jones",
         "Cool Matt Games: free browser games, tools, toys and widgets designed by Matt Jones with AI. No ads, no sign-up.",
         body.replace("{shelves}", shelves()), style, script)

    # about, 404
    style, body, script = split((src / "about.html").read_text())
    page("/about/", "About | Cool Matt Games", "Cool Matt Games is made by Matt Jones, an AI designer in Texas who builds small interactive things with Claude.",
         body, style, script, current="about")
    style, body, script = split((src / "404.html").read_text())
    page("/404", "Page not found | Cool Matt Games", "", body.replace("{shelves}", shelves()), style, script, noindex=True)

    # redirects for old addresses
    for slug, to in REDIRECTS.items():
        write(f"/{slug}/", f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Moved | Cool Matt Games</title>'
              f'<meta name="robots" content="noindex"><link rel="canonical" href="{SITE}{to}"><meta http-equiv="refresh" content="0; url={to}"></head>'
              f'<body><p>This page moved. <a href="{to}">Go to the new one</a>.</p></body></html>\n')

    urls = ["/", "/about/"] + [f"/{p[0]}/" for p in PIECES]
    (root / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(f"  <url><loc>{SITE}{u}</loc></url>" for u in urls) + "\n</urlset>\n")
    (root / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    print(f"built {len(PIECES)} pieces, home, about, 404, {len(REDIRECTS)} redirects")


if __name__ == "__main__":
    build()
