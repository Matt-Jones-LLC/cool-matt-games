"""Rebuild the three demo pages: keeps each page's existing shell (styles, nav, footer)
and swaps in the demo's <main> + script from _build/<page>.html."""
import re, pathlib
here = pathlib.Path(__file__).parent; root = here.parent
css = (here / "demo.css").read_text()
for page in ["llmadness", "the-bullzen", "windhover"]:
    f = root / page / "index.html"; s = f.read_text()
    part = (here / f"{page}.html").read_text()
    style, rest = part.split("</style>\n", 1)
    main, script = rest.split("</main>\n", 1)
    style = style.replace("<style>\n", "<style data-demo>\n" + css) + "</style>\n"
    s = re.sub(r"<style data-demo>.*?</style>\n", "", s, flags=re.S)
    s = re.sub(r"<script data-demo>.*?</script>\n", "", s, flags=re.S)
    s = s.replace('<link rel="stylesheet" href="/assets/site.css">', style + '<link rel="stylesheet" href="/assets/site.css">', 1)
    s = re.sub(r"<main>.*?</main>\n?", lambda m: main + "</main>\n", s, count=1, flags=re.S)
    s = s.replace("</body>", script.replace("<script>", "<script data-demo>", 1) + "</body>", 1)
    f.write_text(s); print("built", page)

# 404 page: the Bullzen page's shell with its own <main>.
s = (root / "the-bullzen" / "index.html").read_text()
part = (here / "404.html").read_text()
style, rest = part.split("</style>\n", 1)
main = rest.split("</main>\n", 1)[0]
s = re.sub(r"<style data-demo>.*?</style>\n", style.replace("<style>", "<style data-demo>") + "</style>\n", s, flags=re.S)
s = re.sub(r"<script data-demo>.*?</script>\n", "", s, flags=re.S)
s = re.sub(r"<main>.*?</main>\n?", lambda m: main + "</main>\n", s, count=1, flags=re.S)
s = re.sub(r"<title>.*?</title>", "<title>Page not found | Matt Jones</title>", s, count=1)
s = re.sub(r'<!--meta-->.*?<!--/meta-->', '<meta name="robots" content="noindex">', s, flags=re.S)
(root / "404.html").write_text(s); print("built 404")
