"""Site checks, run locally and in CI: every internal link and asset resolves, every in-page
anchor exists, and every page has a title, description and the shared assets."""
import pathlib, re, sys
root = pathlib.Path(__file__).parent.parent
pages = [root / "index.html", root / "404.html"] + sorted(p for p in root.glob("*/index.html") if p.parent.name != "_build")
pages = [p for p in pages if 'http-equiv="refresh"' not in p.read_text()]   # skip the redirect stubs
STANDALONE = {"hibob"}   # carries its own styles instead of the shared ones
errors = []

def target(url):
    path = url.split("#")[0].split("?")[0]
    f = root / path.lstrip("/")
    return f / "index.html" if path.endswith("/") or f.is_dir() else f

ids = {p: set(re.findall(r'\bid="([^"]+)"', p.read_text())) for p in pages}
for p in pages:
    s = p.read_text(); name = str(p.relative_to(root))
    if not re.search(r"<title>[^<]+</title>", s): errors.append(f"{name}: no <title>")
    if p.name != "404.html" and 'name="description"' not in s: errors.append(f"{name}: no meta description")
    if p.parent.name not in STANDALONE:
        for asset in ("/assets/site.css", "/assets/site.js"):
            if asset not in s: errors.append(f"{name}: does not load {asset}")
    for attr, url in re.findall(r'\b(href|src)="([^"]+)"', s):
        if url.startswith(("http:", "https:", "mailto:", "tel:", "data:", "javascript:")): continue
        if url.startswith("#"):
            if len(url) > 1 and url[1:] not in ids[p] and url[1:] != "main": errors.append(f"{name}: missing anchor {url}")
            continue
        if not url.startswith("/"): errors.append(f"{name}: relative link {url} (use a root-relative path)"); continue
        t = target(url)
        if not t.exists(): errors.append(f"{name}: broken link {url}"); continue
        frag = url.split("#")[1] if "#" in url else ""
        if frag and t in ids and frag not in ids[t]: errors.append(f"{name}: {url} has no such anchor")
for line in errors: print("FAIL", line)
print(f"checked {len(pages)} pages: {len(errors)} problem(s)")
sys.exit(1 if errors else 0)
