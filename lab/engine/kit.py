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
         full="page/media/ep03/ep03_full_720.mp4", thumb="ep03s/build/ep03_thumb.jpg",
         yt=("The Shovel Sellers: Who Really Gets Rich in the AI Gold Rush",
             "May 1848: a shopkeeper walks through San Francisco holding up a bottle of gold. He had already bought every "
             "pan and shovel in town. 178 years later, the AI build-out has its own shovel sellers.\n\nIn this video: what "
             "economists found in the gold rush census, the $725 billion big tech plans to spend this year (a million "
             "dollars a day since the Romans invaded Britain), Nvidia's 2,000 Big Macs a second, why OpenAI spends about "
             "$1.65 for every $1 it makes, Britain's railway mania, and a labelled what-if: when intelligence is cheap, "
             "what becomes scarce?"),
         schedule=[("Day 1", "part1", "bigmac"), ("Day 2", "part2", "romans"), ("Day 3", "part3", "nvidia"),
                   ("Day 4", "part4", "openai"), ("Day 5", "railway", None), ("Day 6", "scarce", None)]),
    dict(dir="ep04", slug="ep04", title="EP04 · The Man in the Machine", sub="Robots, war and the person still inside",
         full="ep04/build/ep04_720.mp4", thumb="ep04/build/ep04_thumb.jpg",
         yt=("Who's Really Inside the Robots?",
             "18 September 2026: a man steps into a cage in San Francisco to fight a six-foot humanoid robot. The clips "
             "left one thing out: a person backstage in a VR headset was deciding its every move.\n\nIn this video: Tesla's "
             "2021 robot reveal (a dancer in a bodysuit), China's first humanoid robot boxing, what the machines really "
             "do on their own, a $13,500 humanoid in Big Macs, a robot dog with a rifle, Ukraine's 50,000 ground robots, "
             "a $4.2M Patriot against a drone that costs 3,000 to 8,000 Big Macs, and a labelled what-if: who decides "
             "when the pilot isn't needed?"),
         schedule=[("Day 7", "part1", "cagefight"), ("Day 8", "part2", "tesla"), ("Day 9", "part3", "patriot"),
                   ("Day 10", "part4", "boxing"), ("Day 11", "price", "ukraine"), ("Day 12", "loop", None)]),
    dict(dir="ep05", slug="ep05", title="EP05 · Follow the Sun", sub="AI data centres, leaving the planet",
         full="ep05/build/ep05_720.mp4", thumb="ep05/build/ep05_thumb.jpg",
         yt=("Why AI Is Leaving the Planet",
             "Google has built a satellite to carry four of its AI chips into orbit. Last December, a satellite the size "
             "of a small fridge trained an AI model in space. Why is the AI industry trying to leave Earth?\n\nIn this "
             "video: why industry always goes to its power (a 1771 mill and its water wheel), data centres heading for "
             "as much electricity as Japan, a reactor restarting at Three Mile Island, the orbit where the sun almost "
             "never sets, SpaceX's filing for up to a million satellites, what it costs to launch one Big Mac, Google's "
             "own break-even, and a labelled what-if: who owns the sunlight?"),
         schedule=[("Day 13", "part1", "suncatcher"), ("Day 14", "part2", "bigmac"), ("Day 15", "part3", "million"),
                   ("Day 16", "part4", "shakespeare"), ("Day 17", "japan", "sunlight")]),
    dict(dir="ep06", slug="ep06", title="EP06 · Who's Human Here?", sub="The Turing test, bots and proving you're you",
         full="ep06/build/ep06_720.mp4", thumb="ep06/build/ep06_thumb.jpg",
         yt=("They Picked the AI as the Human",
             "In 2025, 284 people chatted with two strangers at once for five minutes: one a person, one an AI. Their "
             "job was to pick the human. They picked the AI 73% of the time, more often than the real person.\n\nIn this "
             "video: what Alan Turing actually proposed in 1950 and the bar he set, the trick that doubled the AI's score, "
             "why most web traffic is no longer human, the AI agent that clicked \"verify you are human\", the FBI's "
             "low-tech advice for voice scams, and a labelled what-if: when any voice could be synthetic, how do you "
             "prove you're you?"),
         schedule=[("Day 18", "part1", "picked"), ("Day 19", "part2", "persona"), ("Day 20", "part3", "captcha"),
                   ("Day 21", "bots", "secretword")]),
    dict(dir="ep07", slug="ep07", title="EP07 · The Thirty-Year Delay", sub="Why AI hasn't changed productivity (yet)",
         full="ep07/build/ep07_720.mp4", thumb="ep07/build/ep07_thumb.jpg",
         yt=("Why AI Hasn't Made Companies More Productive (Yet)",
             "In February 2026, economists asked 6,000 bosses what AI had done for their companies. Nearly nine in ten "
             "said: nothing. This has happened before, almost exactly.\n\nIn this video: why electricity took decades to "
             "show up in factory productivity (one big motor on the old shaft), the redesign that finally made it pay, "
             "Robert Solow's computer paradox, why 95% of company AI pilots made no measurable return, and a labelled "
             "what-if: an office designed from zero around AI."),
         schedule=[("Day 22", "part1", "nothing"), ("Day 23", "part2", "shaft"), ("Day 24", "part3", "redesign"),
                   ("Day 25", "pilots", "office")]),
    dict(dir="ep08", slug="ep08", title="EP08 · Cheaper Makes More", sub="The Jevons paradox: why cheaper AI means more of it",
         full="ep08/build/ep08_720.mp4", thumb="ep08/build/ep08_thumb.jpg",
         yt=("Why Cheaper AI Means MORE Data Centres, Not Fewer",
             "In 1865, a British economist noticed something strange: steam engines had become far more efficient, so "
             "Britain should have burned less coal. It burned more.\n\nIn this video: the Jevons paradox, light in Britain "
             "(3,000 times cheaper and 40,000 times more used), a million AI tokens falling from about ten Big Macs to a "
             "hundredth of one, Google's 3.2 quadrillion tokens a month, and a labelled what-if: what would we use "
             "thinking for if it got as cheap as light?"),
         schedule=[("Day 26", "part1", "light"), ("Day 27", "part2", "bigmacs"), ("Day 28", "part3", "google"), ("Day 29", "nadella", None)]),
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
  const card=b.closest('.card');const el=card.querySelector('.'+(b.dataset.copy||'post'));const text=el.textContent;const n=card.querySelector('.note');
  try{await navigator.clipboard.writeText(text);note(n,(b.dataset.copy==='hook'?'Title':b.dataset.copy==='post'&&card.classList.contains('wide')?'Description':'Caption')+' copied.');}
  catch(e){const r=document.createRange();r.selectNodeContents(el);const s=getSelection();
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


def sources(ep):
    import importlib.util
    spec = importlib.util.spec_from_file_location("s_" + ep["slug"], os.path.join(LAB, ep["dir"], "script.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, "SOURCES", [])


def full_card(ep):
    import subprocess
    e = html.escape
    path = os.path.join(LAB, ep["full"])
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                             capture_output=True, text=True, check=True).stdout)
    title, blurb = ep["yt"]
    desc = blurb + "\n\nSources:\n" + "\n".join("• " + x for x in sources(ep))
    src = f"media/{ep['slug']}/{os.path.basename(path)}"
    th = ep.get("thumb") and os.path.exists(os.path.join(LAB, ep["thumb"]))
    tsrc = f"media/{ep['slug']}/{os.path.basename(ep['thumb'])}" if th else ""
    poster = f' poster="{e(tsrc)}"' if th else ""
    tbtn = f'\n      <button type="button" data-save="{e(tsrc)}">Save thumbnail</button>' if th else ""
    return f"""<article class="card wide" id="{e(ep['slug'])}-full">
  <video controls playsinline preload="metadata"{poster} src="{e(src)}"></video>
  <div class="body">
    <div class="meta"><span class="chip">THE FULL FILM · YOUTUBE</span><span>{int(d // 60)}:{int(d % 60):02d} · 16:9</span></div>
    <p class="hook">{e(title)}</p>
    <p class="post">{e(desc)}</p>
    <div class="row"><button class="main" type="button" data-copy="hook">Copy title</button>
      <button class="main" type="button" data-copy="post">Copy description</button>
      <button type="button" data-save="{e(src)}">Save 720p preview</button>{tbtn}</div>
    <p class="note" aria-live="polite">The 1080p file for YouTube was sent in the chat.</p>
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
    out = {}
    for ep in episodes():
        for key in ("full", "thumb"):
            if ep.get(key) and os.path.exists(os.path.join(LAB, ep[key])):
                out[f"media/{ep['slug']}/{os.path.basename(ep[key])}"] = os.path.join(LAB, ep[key])
        for k in ep["kit"].values():
            out[f"media/{ep['slug']}/{k['file']}"] = os.path.join(LAB, ep["dir"], "build", "shorts", k["file"])
    return out


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
  {full_card(ep) if ep.get("full") and os.path.exists(os.path.join(LAB, ep["full"])) else ""}
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
.card.wide{{grid-template-rows:auto 1fr}}
.card.wide video{{aspect-ratio:16/9;max-height:none}}
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
