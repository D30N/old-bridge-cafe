# -*- coding: utf-8 -*-
"""Old Bridge Cafe menu site generator: grid homepage + one details page per category."""
import os, json

CATS = [
    ("lime", "LIME", "🍋", "#2e9e4f", False, [("Soda Lime",25),("Fresh Lime",30),("Blue Lime",50),("Mint Lime",50)], None),
    ("shake", "SHAKE", "🥤", "#ec407a", False, [("Sharjah",70),("Butter Scotch",70),("Strawberry",70),("Pistha",70),("Mango",70),("Vanilla",70),("Chikoo",70),("Chocolate",80),("Oreo",80),("Tender Coconut",80),("Kitkat",80),("Dairy Milk",80)], None),
    ("mojito", "MOJITO", "🌿", "#43a047", False, [("Passion Fruit",70),("Blue Curaçao",70),("Green Apple",70),("Watermelon",70),("Mango",70),("Strawberry",70),("Lichi",70),("Black Currant",70),("Grape",70),("Mint Lime",70)], None),
    ("juice", "JUICE", "🧃", "#f39c2c", False, [("Watermelon",60),("Pineapple",70),("Orange",80),("Shamam",80),("Apple",80),("Grapes",80),("Papaya",80),("Anar",90),("Musambi",100)], None),
    ("lassi", "LASSI", "🥛", "#1e88c7", False, [("Normal",60),("Mango",80),("Butter Scotch",80),("Chocolate",80)], None),
    ("falooda", "FALOODA", "🍨", "#8e44ad", False, [("Normal",130),("Classic",130),("Royal",150),("Mumbai",150)], None),
    ("tea", "TEA", "🍵", "#6d4c41", False, [("Normal Tea",15),("Black Tea",10),("Coffee",20),("Black Coffee",12),("Mint Tea",12),("Lemon Tea",12),("Ginger Tea",12),("—split—",0),("Badam Tea",20),("Chocolate Tea",20)], None),
    ("fruit-salad", "FRUIT SALAD", "🍓", "#e53935", False, [("Cutfruit",90),("Normal",100),("Normal with Ice Cream",120),("Royal Special",150)], None),
    ("kannur-cocktail", "KANNUR COCKTAIL", "🍹", "#fdd835", True, [], 80),
    ("aval-milk", "AVAL MILK", "🥣", "#29a8d8", False, [], 80),
    ("cold-coffee", "COLD COFFEE", "🧋", "#5d4037", False, [("Cold Coffee",70),("Cold Boost",70),("Cold Horlicks",70)], None),
    ("kulukki", "KULUKKI", "🍸", "#f06292", False, [], 40),
]

CSS = """
  * { margin:0; padding:0; box-sizing:border-box; }
  body { font-family:'Poppins',system-ui,sans-serif; background:#FFF9EF; color:#2a2320; padding-bottom:40px; }
  header { text-align:center; padding:30px 16px 22px; background:linear-gradient(160deg,#ffdf9e 0%,#ffc98a 45%,#ffb59e 100%); }
  .wave { display:block; width:100%; height:44px; margin-top:-1px; }
  header .cafe { font-family:'Pacifico',cursive; font-size:clamp(34px,8vw,52px); line-height:1.1; color:#3b2314; }
  header .cafe span { color:inherit; }
  header .tagline { margin-top:2px; font-size:13px; letter-spacing:2.5px; text-transform:uppercase; color:#7c4a21; }
  .info { margin-top:14px; font-size:13.5px; color:#6b4423; font-weight:500; }
  .info a.loc { display:inline-block; margin-top:5px; color:#8a4b12; font-weight:700; text-decoration:underline; text-underline-offset:2px; }
  a { text-decoration:none; color:inherit; }
  .back { display:inline-block; margin:14px 0 0 14px; font-size:14px; font-weight:600; color:#5b4632; background:#fff; border:1.5px solid #e8dcc8; padding:7px 14px; border-radius:999px; }
  body { background:radial-gradient(600px 300px at 15% -40px, #ffe9c9 0, transparent 60%), radial-gradient(700px 340px at 90% -60px, #ffd9e2 0, transparent 55%), #FFF9EF; }
  main { max-width:1060px; margin:0 auto; padding:16px 14px 0; }
  .grid { display:grid; grid-template-columns:repeat(3,1fr); gap:10px; }
  @media (min-width:720px){ .grid { gap:14px; } }
  .tile { background:#fff; border-radius:15px; padding:0; overflow:hidden; text-align:center; box-shadow:0 6px 18px color-mix(in srgb, var(--c) 26%, transparent); border:1px solid #f1e6d2; display:flex; flex-direction:column; transition:transform .25s ease, box-shadow .25s ease; }
  @media (min-width:720px){ .tile { border-radius:18px; } }
  .tile:active { transform:scale(.98); }
  .tile:hover { transform:translateY(-4px); box-shadow:0 14px 30px color-mix(in srgb, var(--c) 40%, transparent); }
  .tile .phwrap { position:relative; height:150px; display:flex; align-items:center; justify-content:center; background:#fff; border-bottom:1px solid #f1e6d2; overflow:hidden; }
  .tile img.ph { width:100%; height:100%; object-fit:contain; display:block; transition:transform .45s ease; }
  .tile:hover img.ph { transform:scale(1.04); }
  .tile .nm { margin-top:7px; font-weight:700; font-size:12.5px; letter-spacing:.2px; padding:0 4px; }
  @media (min-width:720px){ .tile .phwrap { height:215px; } .tile .nm { margin-top:10px; font-size:16.5px; letter-spacing:.4px; padding:0 8px; } }
  @keyframes rise { from { opacity:0; transform:translateY(18px); } to { opacity:1; transform:none; } }
  .js .tile { opacity:0; }
  .js .tile.in { animation:rise .6s cubic-bezier(.2,.7,.3,1) forwards; animation-delay:var(--d,0ms); }
  header .cafe { animation:rise .7s ease both; }
  section.card { animation:rise .55s ease both; }
  li { animation:rise .5s ease both; animation-delay:var(--d,0ms); }
  .herowrap { display:flex; align-items:center; justify-content:center; border-radius:16px; margin-bottom:14px; background:#fff; border:3px solid var(--c); box-shadow:0 16px 36px color-mix(in srgb, var(--c) 34%, transparent); padding:10px; }
  .hero { max-width:min(100%,440px); max-height:320px; object-fit:contain; display:block; }
  @media (prefers-reduced-motion: reduce) { * { animation:none !important; transition:none !important; } .js .tile { opacity:1; } }
  .tile .meta { margin-top:2px; font-size:10.5px; color:#8a6d4b; padding:0 3px; }
  @media (min-width:720px){ .tile .meta { margin-top:3px; font-size:13px; } }
  .tile .tbody { flex:1; padding:3px 0 11px; background:color-mix(in srgb, var(--c) 10%, #ffffff); border-top:1px solid #f1e6d2; }
  .insta { display:inline-flex; align-items:center; gap:8px; margin-top:14px; padding:9px 20px; color:#fff; font-size:15.5px; font-weight:700; background:linear-gradient(45deg,#f09433,#dc2743,#bc1888); border-radius:999px; box-shadow:0 4px 14px rgba(188,24,136,.35); }
  .insta svg { flex:none; }
  .insta:active { opacity:.85; }
  .tile .price { position:absolute; top:7px; right:7px; background:#c22e2e; color:#fff; font-size:11px; font-weight:700; padding:3px 9px; border-radius:999px; box-shadow:0 2px 6px rgba(0,0,0,.25); }
  .search { max-width:1060px; margin:18px auto 0; padding:0 14px; }
  .search input { width:100%; padding:13px 18px; border-radius:999px; border:1.5px solid #e8dcc8; font-size:15px; font-family:inherit; background:#fff; outline:none; }
  .search input:focus { border-color:#e0a458; }
  .noresults { display:none; text-align:center; color:#8a6d4b; font-size:14px; padding:26px 0 6px; }
  .res { display:none; margin-top:10px; }
  .res a { display:flex; align-items:baseline; gap:8px; background:#fff; border:1px solid #f1e6d2; border-radius:12px; padding:10px 14px; margin-bottom:8px; font-size:15px; box-shadow:0 2px 8px rgba(90,60,20,.06); }
  .res .cat { color:#8a6d4b; font-size:12px; white-space:nowrap; }
  .res .dots { flex:1; border-bottom:2px dotted #ddd0ba; transform:translateY(-3px); }
  .res b { color:#c22e2e; white-space:nowrap; }
  section.card { background:#fff; border-radius:18px; padding:20px 18px 14px; box-shadow:0 3px 14px rgba(90,60,20,.08); border:1px solid #f1e6d2; max-width:640px; margin:0 auto; }
  .banner { display:inline-block; font-weight:700; letter-spacing:1px; font-size:20px; color:#fff; padding:5px 18px 6px; border-radius:6px; transform:rotate(-1.2deg); margin-bottom:12px; box-shadow:0 2px 6px rgba(0,0,0,.15); }
  .dark { color:#4a3200; }
  ul { list-style:none; }
  li { display:flex; align-items:baseline; gap:8px; padding:5px 0; font-size:16px; }
  li .dots { flex:1; border-bottom:2px dotted #ddd0ba; transform:translateY(-3px); }
  li b { background:#fdecec; color:#c22e2e; font-weight:700; font-size:.92em; padding:2.5px 11px; border-radius:999px; white-space:nowrap; }
  .rs { font-family:Roboto,'Noto Sans',Arial,system-ui,sans-serif; font-size:.9em; font-weight:600; vertical-align:baseline; margin-right:2px; letter-spacing:0; }
  .split { border-top:2px dashed #cdbd9d; margin:8px 0 4px; }
  .single { text-align:center; padding:10px 0 8px; }
  .single .price { font-size:38px; font-weight:700; color:#c22e2e; }
  .single .note { font-size:13px; color:#8a6d4b; }
  .pn { display:flex; justify-content:space-between; gap:10px; max-width:640px; margin:16px auto 0; }
  .pn a { font-size:14px; font-weight:600; color:#5b4632; background:#fff; border:1.5px solid #e8dcc8; padding:8px 14px; border-radius:999px; }
  footer { text-align:center; margin-top:28px; font-size:13px; color:#a08b6c; padding:0 16px; }
  footer .imgnote { display:block; font-style:italic; }
  .revbtn { display:inline-flex; align-items:center; gap:7px; margin-bottom:14px; padding:9px 18px; background:#fff; border:1.5px solid #e8dcc8; border-radius:999px; font-size:14px; font-weight:600; color:#5b4632; box-shadow:0 3px 10px rgba(90,60,20,.08); }
  .revbtn:active { opacity:.7; }
  footer .copy { margin-top:12px; }
"""

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Pacifico&family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{css}</style>
</head>
<body>
"""

HEADER_HTML = """
<header>
  <div class="cafe">Old <span>Bridge</span> Cafe</div>
  <div class="tagline">Fresh • Juices • Shakes • Snacks</div>
  <a class="insta" href="https://www.instagram.com/oldbridge_cafe/" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" width="21" height="21" fill="none" stroke="#fff" stroke-width="2"><rect x="2.5" y="2.5" width="19" height="19" rx="5.5"/><circle cx="12" cy="12" r="4.2"/><circle cx="17.6" cy="6.4" r="1.4" fill="#fff" stroke="none"/></svg>Follow us on Instagram</a>
  <div class="info">🕚 Open Daily · 11:00 AM – 11:00 PM<br><a class="loc" href="https://maps.app.goo.gl/h8bwZFAta8rJe4m89?g_st=ac" target="_blank" rel="noopener">📍 Oldbridge, Murinjapuzha</a></div>
</header>
<svg class="wave" viewBox="0 0 1440 90" preserveAspectRatio="none"><path d="M0,0 L1440,0 L1440,26 C1150,86 900,88 640,52 C420,22 180,58 0,34 Z" fill="#ffb59e"/></svg>
"""

POPULAR = {"shake", "falooda"}

def price_badge(items, single):
    if single: return f"<span class='rs'>₹</span>{single}"
    ps = [p for _, p in items if p]
    if min(ps) == max(ps): return f"<span class='rs'>₹</span>{min(ps)}"
    return f"<span class='rs'>₹</span>{min(ps)}–{max(ps)}"

def tile_meta(items, single):
    if single: return "Special"
    return f"{len(items)} items"

def tile_html(i, cat):
    slug, name, emo, color, dark, items, single = cat
    pop = ''
    search = (name + ' ' + ' '.join(nm for nm, _ in items)).lower()
    return (f'    <a class="tile" style="--d:{i*70}ms;--c:{color}" href="{slug}/" data-search="{search}">'
            f'<div class="phwrap"><img class="ph" src="img/menu/{slug}.jpg?v=2" alt="{name.title()}">{pop}<span class="price">{price_badge(items, single)}</span></div>'
            f'<div class="tbody"><div class="nm">{name}</div><div class="meta">{tile_meta(items, single)}</div></div></a>')

tiles = "\n".join(tile_html(i, cat) for i, cat in enumerate(CATS))

ITEMS = []
for _slug, _name, _emo, _color, _dark, _items, _single in CATS:
    if _single:
        ITEMS.append({"n": _name.title(), "p": _single, "c": _name.title(), "u": _slug + "/"})
    else:
        for _nm, _p in _items:
            if _nm == "—split—": continue
            ITEMS.append({"n": _nm, "p": _p, "c": _name.title(), "u": _slug + "/"})
ITEMS_JS = json.dumps(ITEMS)

index = HEAD.format(title="Old Bridge Cafe — Menu", desc="Old Bridge Cafe menu — shakes, fresh juices, mojitos, falooda, tea and more. Tap a category for details.", css=CSS) + f"""
{HEADER_HTML}
<div class="search"><input id="q" type="search" placeholder="🔍 Search items… try 'falooda'" aria-label="Search menu items"><div class="res" id="res"></div></div>
<main>
  <div class="grid">
{tiles}
  </div>
  <div class="noresults" id="nr">No items found — try another name</div>
</main>
<footer><a class="revbtn" href="https://share.google/u73ZKqA6gACjDoqhO" target="_blank" rel="noopener">⭐ Review us on Google</a><span class="imgnote">Images shown are for illustration only — the actual product may vary slightly.</span><div class="copy">© 2026 Old Bridge Cafe • Fresh &amp; made to order</div></footer>
<script>
document.documentElement.classList.add('js');
var io = new IntersectionObserver(function(es){{ es.forEach(function(e){{ if (e.isIntersecting) {{ e.target.classList.add('in'); io.unobserve(e.target); }} }}); }}, {{ threshold:.12 }});
document.querySelectorAll('.tile').forEach(function(t){{ io.observe(t); }});
var q = document.getElementById('q');
if (q) {{ q.addEventListener('input', function(){{ var v = q.value.toLowerCase().trim(); var n = 0; document.querySelectorAll('.tile').forEach(function(t){{ var show = !v || (t.dataset.search || '').includes(v) || t.textContent.toLowerCase().includes(v); t.style.display = show ? '' : 'none'; if (show) n++; }}); document.getElementById('nr').style.display = n ? 'none' : 'block'; }}); }}
var ITEMS = {ITEMS_JS};
var res = document.getElementById('res');
if (q && res) {{ q.addEventListener('input', function(){{ var v = q.value.toLowerCase().trim(); if (!v) {{ res.style.display = 'none'; res.innerHTML = ''; return; }} var m = ITEMS.filter(function(it){{ return it.n.toLowerCase().includes(v); }}).slice(0, 15); res.innerHTML = m.map(function(it){{ return '<a href="' + it.u + '">' + it.n + ' <span class="cat">' + it.c + '</span><span class="dots"></span><b><span class="rs">₹</span>' + it.p + '</b></a>'; }}).join(''); res.style.display = m.length ? 'block' : 'none'; }}); }}
</script>
</body>
</html>
"""
open("index.html", "w", encoding="utf-8").write(index)

for i, (slug, name, emo, color, dark, items, single) in enumerate(CATS):
    if single:
        body = f'<div class="single"><div class="price"><span class="rs">₹</span>{single}</div><div class="note">{"The house special!" if slug=="kannur-cocktail" else ""}</div></div>'
    else:
        rows = []
        for rn, (nm, p) in enumerate(items):
            if nm == "—split—":
                rows.append('</ul><div class="split"></div><ul>')
            else:
                rows.append(f'<li style="--d:{rn*55}ms">{nm} <span class="dots"></span><b><span class="rs">₹</span>{p}</b></li>')
        body = "<ul>\n" + "\n".join(rows) + "\n</ul>"
    prev = CATS[i-1] if i > 0 else None
    nxt = CATS[i+1] if i < len(CATS)-1 else None
    pn = '<div class="pn">' + (f'<a href="../{prev[0]}/">← {prev[1].title()}</a>' if prev else '<span></span>') + (f'<a href="../{nxt[0]}/">{nxt[1].title()} →</a>' if nxt else '<span></span>') + '</div>'
    page = HEAD.format(title=f"{name.title()} — Old Bridge Cafe", desc=f"{name.title()} at Old Bridge Cafe — items and prices.", css=CSS) + f"""
<a class="back" href="../">← All Categories</a>
{HEADER_HTML}
<main>
  <section class="card">
    <div class="herowrap" style="--c:{color}"><img class="hero" src="../img/menu/{slug}.jpg?v=2" alt="{name.title()}"></div>
    <span class="banner{' dark' if dark else ''}" style="background:{color}">{name} {emo}</span>
    {body}
  </section>
  {pn}
</main>
<footer><a class="revbtn" href="https://share.google/u73ZKqA6gACjDoqhO" target="_blank" rel="noopener">⭐ Review us on Google</a><span class="imgnote">Images shown are for illustration only — the actual product may vary slightly.</span><div class="copy">© 2026 Old Bridge Cafe • Fresh &amp; made to order</div></footer>
</body>
</html>
"""
    os.makedirs(slug, exist_ok=True)
    open(os.path.join(slug, "index.html"), "w", encoding="utf-8").write(page)

print("built index +", len(CATS), "category pages")
