# -*- coding: utf-8 -*-
"""Old Bridge Cafe menu site generator: grid homepage + one details page per category."""
import os

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
  header { text-align:center; padding:30px 16px 4px; }
  header .cafe { font-family:'Pacifico',cursive; font-size:clamp(34px,8vw,52px); line-height:1.1; color:#3b2314; }
  header .cafe span { color:#b33a1f; }
  header .sub { margin-top:4px; font-size:14px; letter-spacing:3px; text-transform:uppercase; color:#8a6d4b; }
  a { text-decoration:none; color:inherit; }
  .back { display:inline-block; margin:14px 0 0 14px; font-size:14px; font-weight:600; color:#5b4632; background:#fff; border:1.5px solid #e8dcc8; padding:7px 14px; border-radius:999px; }
  main { max-width:1060px; margin:0 auto; padding:16px 14px 0; }
  .grid { display:grid; grid-template-columns:repeat(2,1fr); gap:14px; }
  @media (min-width:720px){ .grid { grid-template-columns:repeat(3,1fr); } }
  .tile { background:#fff; border-radius:18px; padding:20px 14px 16px; text-align:center; box-shadow:0 3px 14px rgba(90,60,20,.08); border:1px solid #f1e6d2; display:block; }
  .tile:active { transform:scale(.98); }
  .tile .emo { font-size:40px; }
  .tile .nm { margin-top:8px; font-weight:700; font-size:16.5px; letter-spacing:.4px; }
  .tile .meta { margin-top:3px; font-size:13px; color:#8a6d4b; }
  .tile .bar { height:6px; border-radius:99px; margin-top:12px; }
  section.card { background:#fff; border-radius:18px; padding:20px 18px 14px; box-shadow:0 3px 14px rgba(90,60,20,.08); border:1px solid #f1e6d2; max-width:640px; margin:0 auto; }
  .banner { display:inline-block; font-weight:700; letter-spacing:1px; font-size:20px; color:#fff; padding:5px 18px 6px; border-radius:6px; transform:rotate(-1.2deg); margin-bottom:12px; box-shadow:0 2px 6px rgba(0,0,0,.15); }
  .dark { color:#4a3200; }
  ul { list-style:none; }
  li { display:flex; align-items:baseline; gap:8px; padding:5px 0; font-size:16px; }
  li .dots { flex:1; border-bottom:2px dotted #ddd0ba; transform:translateY(-3px); }
  li b { color:#c22e2e; font-weight:700; white-space:nowrap; }
  .rs { font-size:.72em; font-weight:600; vertical-align:.32em; margin-right:1px; letter-spacing:0; }
  .split { border-top:2px dashed #cdbd9d; margin:8px 0 4px; }
  .single { text-align:center; padding:10px 0 8px; }
  .single .price { font-size:38px; font-weight:700; color:#c22e2e; }
  .single .note { font-size:13px; color:#8a6d4b; }
  .pn { display:flex; justify-content:space-between; gap:10px; max-width:640px; margin:16px auto 0; }
  .pn a { font-size:14px; font-weight:600; color:#5b4632; background:#fff; border:1.5px solid #e8dcc8; padding:8px 14px; border-radius:999px; }
  footer { text-align:center; margin-top:28px; font-size:13px; color:#a08b6c; padding:0 16px; }
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

def price_meta(items, single):
    if single: return f"<span class='rs'>₹</span>{single}"
    ps = [p for _, p in items if p]
    return f"{len(ps)} items • <span class='rs'>₹</span>{min(ps)}–<span class='rs'>₹</span>{max(ps)}"

tiles = "\n".join(
    f'    <a class="tile" href="{slug}/"><div class="emo">{emo}</div><div class="nm">{name}</div><div class="meta">{price_meta(items, single)}</div><div class="bar" style="background:{color}"></div></a>'
    for slug, name, emo, color, dark, items, single in CATS)

index = HEAD.format(title="Old Bridge Cafe — Menu", desc="Old Bridge Cafe menu — shakes, fresh juices, mojitos, falooda, tea and more. Tap a category for details.", css=CSS) + f"""
<header>
  <div class="cafe">Old <span>Bridge</span> Cafe</div>
  <div class="sub">☕ Menu — tap a category</div>
</header>
<main>
  <div class="grid">
{tiles}
  </div>
</main>
<footer>© 2026 Old Bridge Cafe • Fresh &amp; made to order</footer>
</body>
</html>
"""
open("index.html", "w", encoding="utf-8").write(index)

for i, (slug, name, emo, color, dark, items, single) in enumerate(CATS):
    if single:
        body = f'<div class="single"><div class="price"><span class="rs">₹</span>{single}</div><div class="note">{"The house special!" if slug=="kannur-cocktail" else ""}</div></div>'
    else:
        rows = []
        for nm, p in items:
            if nm == "—split—":
                rows.append('</ul><div class="split"></div><ul>')
            else:
                rows.append(f'<li>{nm} <span class="dots"></span><b><span class="rs">₹</span>{p}</b></li>')
        body = "<ul>\n" + "\n".join(rows) + "\n</ul>"
    prev = CATS[i-1] if i > 0 else None
    nxt = CATS[i+1] if i < len(CATS)-1 else None
    pn = '<div class="pn">' + (f'<a href="../{prev[0]}/">← {prev[1].title()}</a>' if prev else '<span></span>') + (f'<a href="../{nxt[0]}/">{nxt[1].title()} →</a>' if nxt else '<span></span>') + '</div>'
    page = HEAD.format(title=f"{name.title()} — Old Bridge Cafe", desc=f"{name.title()} at Old Bridge Cafe — items and prices.", css=CSS) + f"""
<a class="back" href="../">← All Categories</a>
<header>
  <div class="cafe">Old <span>Bridge</span> Cafe</div>
</header>
<main>
  <section class="card">
    <span class="banner{' dark' if dark else ''}" style="background:{color}">{name} {emo}</span>
    {body}
  </section>
  {pn}
</main>
<footer>© 2026 Old Bridge Cafe • Fresh &amp; made to order</footer>
</body>
</html>
"""
    os.makedirs(slug, exist_ok=True)
    open(os.path.join(slug, "index.html"), "w", encoding="utf-8").write(page)

print("built index +", len(CATS), "category pages")
