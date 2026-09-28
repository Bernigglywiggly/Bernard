"""The posting kit (a phone-first page): every episode's shorts with a preview, the caption and hashtags to copy and a
Save button (the page's downloads capability; plain download links don't work inside an artifact), each episode as
the parts that make the whole film, then its highlights, with a suggested posting order.

    python3 -m engine.kit      # every lab/<ep>/build/shorts/kit.json -> lab/shorts/index.html
                               # publish it with media/<slug>/<file> -> lab/<ep>/build/shorts/<file>
"""
import html
import json
import os

import engine  # noqa: F401  (paths)

LAB = engine.LAB
OUT = os.path.join(LAB, "shorts", "index.html")
EPISODES = [
    dict(dir="ep03s", slug="ep03", title="EP03 · The Shovel Sellers", sub="AI, gold rushes and who really gets rich",
         schedule=[("Day 1", "part1", "bigmac"), ("Day 2", "part2", "romans"), ("Day 3", "part3", "nvidia"),
                   ("Day 4", "part4", "openai"), ("Day 5", "railway", None), ("Day 6", "scarce", None)]),
    dict(dir="ep04", slug="ep04", title="EP04 · The Man in the Machine", sub="Robots, war and the person still inside",
         schedule=[("Day 7", "part1", "cagefight"), ("Day 8", "part2", "tesla"), ("Day 9", "part3", "patriot"),
                   ("Day 10", "part4", "boxing"), ("Day 11", "price", "ukraine"), ("Day 12", "loop", None)]),
]

CSS = """
:root{--ground:#F2F6F5;--surface:#FFFFFF;--ink:#0B1414;--muted:#51625F;--accent:#0B8A7E;--line:#D3E0DD;--chip:#E3F1EE;
color-scheme:light}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--ground:#070A0B;--surface:#0E1416;--ink:#E6F0EF;
--muted:#8EA3A1;--accent:#35D6C6;--line:#1B2729;--chip:#0F2524;color-scheme:dark}}
:root[data-theme="dark"]{--ground:#070A0B;--surface:#0E1416;--ink:#E6F0EF;--muted:#8EA3A1;--accent:#35D6C6;--line:#1B2729;
--chip:#0F2524;color-scheme:dark}
body{background:var(--ground);color:var(--ink);font:16px/1.55 "Inter Tight",system-ui,sans-serif;margin:0}
.wrap{max-width:1080px;margin:0 auto;padding-inline:16px;padding-block:28px 64px}
.eyebrow{font:500 12px/1.4 "IBM Plex Mono",ui-monospace,monospace;letter-spacing:.14em;text-transform:uppercase;color:var(--accent)}
h1{font:400 clamp(28px,6vw,44px)/1.1 Michroma,"Inter Tight",sans-serif;letter-spacing:.02em;margin:.35em 0 .3em;text-wrap:balance}
h2{font:400 18px/1.3 Michroma,"Inter Tight",sans-serif;letter-spacing:.04em;margin:0;text-wrap:balance}
.lede{color:var(--muted);max-width:62ch;margin:0}
section{margin-top:36px;display:grid;gap:16px}
.plan{display:grid;gap:8px;grid-template-columns:repeat(auto-fill,minmax(150px,1fr))}
.day{border:1px solid var(--line);border-radius:10px;padding:10px 12px;background:var(--surface)}
.day b{font:500 12px/1.4 "IBM Plex Mono",monospace;letter-spacing:.1em;color:var(--accent);display:block}
.day span{font-size:14px}
.grid{display:grid;gap:18px;grid-template-columns:repeat(auto-fill,minmax(300px,1fr))}
.card{background:var(--surface);border:1px solid var(--line);border-radius:14px;overflow:hidden;display:grid;grid-template-rows:auto 1fr}
video{width:100%;aspect-ratio:9/16;max-height:72vh;background:#000;display:block;object-fit:contain}
.body{padding:14px 16px 16px;display:grid;gap:10px;align-content:start}
.meta{display:flex;gap:8px;flex-wrap:wrap;align-items:center;font:500 12px/1.3 "IBM Plex Mono",monospace;color:var(--muted)}
.chip{background:var(--chip);color:var(--accent);border-radius:999px;padding:3px 9px;letter-spacing:.06em}
.hook{font-weight:600;font-size:17px;line-height:1.35;margin:0;text-wrap:balance}
.post{font-size:14px;color:var(--muted);margin:0;white-space:pre-wrap;overflow-wrap:anywhere}
.row{display:flex;gap:8px;flex-wrap:wrap}
button{font:600 14px/1 "Inter Tight",sans-serif;border-radius:10px;padding:11px 14px;border:1px solid var(--line);
background:var(--ground);color:var(--ink);cursor:pointer}
button.main{background:var(--accent);border-color:var(--accent);color:var(--ground)}
button:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.note{font-size:13px;color:var(--muted);min-height:1.2em;margin:0}
footer{margin-top:44px;font-size:13px;color:var(--muted);max-width:62ch}
@media (prefers-reduced-motion:reduce){*{scroll-behavior:auto}}
"""

JS = """
const note=(el,msg)=>{el.textContent=msg;};
document.querySelectorAll('[data-copy]').forEach(b=>b.addEventListener('click',async()=>{
  const card=b.closest('.card');const text=card.querySelector('.post').textContent;const n=card.querySelector('.note');
  try{await navigator.clipboard.writeText(text);note(n,'Caption copied.');}
  catch(e){const r=document.createRange();r.selectNodeContents(card.querySelector('.post'));const s=getSelection();
    s.removeAllRanges();s.addRange(r);note(n,'Selected: copy it from the menu.');}
}));
let downloads=null;
const saveButtons=[...document.querySelectorAll('[data-save]')];
saveButtons.forEach(b=>b.hidden=true);
(async()=>{try{downloads=window.claude&&window.claude.use?await window.claude.use('downloads'):null;}catch(e){downloads=null;}
  if(!downloads)return;saveButtons.forEach(b=>b.hidden=false);})();
saveButtons.forEach(b=>b.addEventListener('click',async()=>{
  const n=b.closest('.card').querySelector('.note');const file=b.dataset.save;
  if(!downloads){note(n,'Saving isn\\'t available in this view: it was also sent in the chat.');return;}
  b.disabled=true;note(n,'Getting the video…');
  try{const blob=await (await fetch(file)).blob();await downloads.save({filename:file.split('/').pop(),data:blob});note(n,'Saved.');}
  catch(e){const c=e&&e.code;note(n,c==='declined'?'Not saved.':c==='rate_limited'?'One save at a time: try again in a moment.':
    'Couldn\\'t save here: the file is also in the chat.');}
  finally{b.disabled=false;}
}));
"""



def card(k, slug):
    e = html.escape
    src = f"media/{slug}/{k['file']}"
    return f"""<article class="card" id="{e(slug)}-{e(k['name'])}">
  <video controls playsinline preload="metadata" src="{e(src)}"></video>
  <div class="body">
    <div class="meta"><span class="chip">{e(k['tag'])}</span><span>{k['dur']:.0f} s · 1080×1920</span></div>
    <p class="hook">{e(k['hook'])}</p>
    <p class="post">{e(k['post'])}</p>
    <div class="row"><button class="main" type="button" data-copy>Copy caption</button>
      <button type="button" data-save="{e(src)}">Save video</button></div>
    <p class="note" aria-live="polite"></p>
  </div>
</article>"""


def episodes():
    out = []
    for ep in EPISODES:
        p = os.path.join(LAB, ep["dir"], "build", "shorts", "kit.json")
        if os.path.exists(p):
            out.append(dict(ep, kit={k["name"]: k for k in json.load(open(p))}))
    return out


def files():
    """The artifact files map: media/<slug>/<file> -> the mp4 on disk."""
    return {f"media/{ep['slug']}/{k['file']}": os.path.join(LAB, ep["dir"], "build", "shorts", k["file"])
            for ep in episodes() for k in ep["kit"].values()}


def section(ep):
    kit, slug = ep["kit"], ep["slug"]
    parts = [kit[n] for n in ("part1", "part2", "part3", "part4") if n in kit]
    highs = [k for n, k in kit.items() if not n.startswith("part")]
    name = lambda n: kit[n]["hook"] if n in kit else n
    plan = "".join(f'<div class="day"><b>{d}</b><span>{html.escape(name(a))}</span>' +
                   (f'<span class="plus">{html.escape(name(b))}</span>' if b and b in kit else "") + "</div>"
                   for d, a, b in ep["schedule"] if a in kit)
    return f"""<section id="{slug}" class="ep">
  <div><span class="eyebrow">{html.escape(ep['title'])}</span><h2 class="ep-title">{html.escape(ep['sub'])}</h2></div>
  <h3>Suggested order</h3>
  <div class="plan">{plan}</div>
  <h3>The whole film, in {len(parts)} parts</h3>
  <div class="grid">{''.join(card(k, slug) for k in parts)}</div>
  <h3>Highlights</h3>
  <div class="grid">{''.join(card(k, slug) for k in highs)}</div>
</section>"""


def main():
    eps = episodes()
    n = sum(len(ep["kit"]) for ep in eps)
    nav = "".join(f'<a href="#{ep["slug"]}">{html.escape(ep["title"])}</a>' for ep in eps)
    page = f"""<title>The Curve Shorts</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@500&family=Inter+Tight:wght@400;600&family=Michroma&display=swap">
<style>{CSS}
h3{{font:600 15px/1.3 "Inter Tight",sans-serif;margin:8px 0 0;color:var(--muted);letter-spacing:.02em}}
.ep{{border-top:1px solid var(--line);padding-top:28px}}
.ep-title{{margin-top:6px}}
nav{{display:flex;gap:8px;flex-wrap:wrap;margin-top:18px}}
nav a{{font:500 13px/1 "IBM Plex Mono",monospace;color:var(--accent);text-decoration:none;border:1px solid var(--line);
border-radius:999px;padding:8px 12px;background:var(--surface)}}
nav a:focus-visible{{outline:2px solid var(--accent);outline-offset:2px}}
.day span{{display:block}}
.day .plus{{margin-top:6px;padding-top:6px;border-top:1px dashed var(--line);color:var(--muted)}}
</style>
<div class="wrap">
<header>
  <span class="eyebrow">The Curve · posting kit</span>
  <h1>Shorts, ready to post</h1>
  <p class="lede">{n} vertical cuts from {len(eps)} film{"s" if len(eps) != 1 else ""}, voiced by George, for TikTok, Reels, YouTube Shorts and Facebook. Each film comes as parts that add up to the whole video, plus standalone highlights. Copy the caption, save the video, post. One part and one highlight a day, the same file on every platform, and pin each Part 1.</p>
  <nav>{nav}</nav>
</header>
{''.join(section(ep) for ep in eps)}
<footer>Every figure in these clips is sourced in its full video's end card. The files were also sent in the chat.</footer>
</div>
<script>{JS}</script>
"""
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w").write(page)
    print(OUT, n, "shorts from", len(eps), "films")
    return OUT


if __name__ == "__main__":
    main()
    print(json.dumps(files(), indent=1))
