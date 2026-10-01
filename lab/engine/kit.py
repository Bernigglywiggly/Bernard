"""The posting kit (a phone-first page): every episode's shorts with a preview, the caption and hashtags to copy and a
Save button (the page's downloads capability; plain download links don't work inside an artifact), each episode as
the parts that make the whole film, then its highlights, with a suggested posting order.

    python3 -m engine.kit      # page 1 (EP03-EP05): lab/<ep>/build/shorts/kit.json -> lab/shorts/index.html
    python3 -m engine.kit 2    # page 2 (EP06-EP08) -> lab/shorts2/index.html
                               # publish each with media/<slug>/<file> -> lab/<ep>/build/shorts/<file>

Two pages because an artifact version holds at most 256 MiB, and the shorts at George's own pace (29 Sep) come to
more than that together.
"""
import datetime
import html
import json
import os

import engine  # noqa: F401  (paths)

LAB = engine.LAB
PAGES = {1: dict(title="The Curve Shorts", out=os.path.join(LAB, "shorts", "index.html"), slugs=("ep05", "ep08", "ep04"),
                 url="https://claude.ai/artifact/GgTivRE2Kt7UbrafqUJFrE"),
         2: dict(title="The Curve Shorts II", out=os.path.join(LAB, "shorts2", "index.html"), slugs=("ep06", "ep07", "ep03", "ep09", "ep10"),
                 url=None)}
# The upload order (30 Sep, "lets just get it done and posted"): EP05 first (Google's Suncatcher launches 1 Oct), then a
# new film every two days; the shorts run one a day from day 1 in the same order.
START = datetime.date(2026, 10, 1)
FILMS = ("ep05", "ep08", "ep04", "ep06", "ep07", "ep03", "ep09", "ep10")
EPISODES = [
    dict(dir="ep03s", slug="ep03", title="EP03 · The Shovel Sellers", sub="AI, gold rushes and who really gets rich",
         full="ep03s/build/ep03_full.mp4", thumb="ep03s/build/ep03_thumb.jpg",
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
    dict(dir="ep09", slug="ep09", title="EP09 · The Laundry Problem", sub="Moravec's paradox: why the easy things are hardest for robots",
         full="ep09/build/ep09.mp4", thumb="ep09/build/ep09_thumb.jpg",
         yt=("Why Robots Can Pass Exams but Can't Fold Your Shirt",
             "In July 2025, an AI scored gold at the International Mathematical Olympiad. Years earlier, a company raised about "
             "$89 million to build a machine that folds laundry, and went bankrupt before it shipped. Why is the exam easy and "
             "the laundry hard?\n\nIn this video: Moravec's paradox (1988), why seeing and gripping are hundreds of millions of "
             "years old and written numbers about 5,000, the 17,000 touch nerve fibres in the palm side of your hand, chess in "
             "1997 against towels in 2025, a $16,000 laundry machine in Big Macs, and a labelled what-if: the first robot that "
             "moves like a toddler."),
         schedule=[("", "part1", "olympiad"), ("", "part2", "day"), ("", "part3", "hand"), ("", "toddler", None)]),
    dict(dir="ep10", slug="ep10", title="EP10 · Counting Sums", sub="The 10^25 line: why the law counts calculations, not danger",
         full="ep10/build/ep10.mp4", thumb="ep10/build/ep10_thumb.jpg",
         yt=("The Number That Decides Which AI Gets Watched",
             "In Europe, one number decides which AI models get the closest watch: ten to the power of twenty-five. Not a test "
             "score: the number of calculations it took to train the model.\n\nIn this video: why the law counts sums instead "
             "of danger, how big 10^25 really is (everyone on Earth doing a sum a second for about 39 million years), "
             "California's line ten times higher, why the compute for the same result keeps halving, Goodhart's law, and a "
             "labelled what-if: thinking rationed like carbon."),
         schedule=[("", "part1", "size"), ("", "part2", "dinosaur"), ("", "part3", "halves")]),
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
  try{await navigator.clipboard.writeText(text);note(n,(b.dataset.what||(b.dataset.copy==='hook'?'Title':b.dataset.copy==='post'&&card.classList.contains('wide')?'Description':'Caption'))+' copied.');}
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
    path = os.path.join(LAB, ep["full"]).replace("_720.mp4", ".mp4")        # the 1080p film (the 720p copies went stale)
    if not os.path.exists(path):
        path = os.path.join(LAB, ep["full"])
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                             capture_output=True, text=True, check=True).stdout)
    title, blurb = ep["yt"]
    desc = blurb + "\n\nSources:\n" + "\n".join("• " + x for x in sources(ep))
    th = ep.get("thumb") and os.path.exists(os.path.join(LAB, ep["thumb"]))
    tsrc = f"media/{ep['slug']}/{os.path.basename(ep['thumb'])}" if th else ""
    pic = f'<img class="thumb" src="{e(tsrc)}" alt="{e(title)}: the YouTube thumbnail" loading="lazy">' if th else ""
    tbtn = f'\n      <button type="button" data-save="{e(tsrc)}">Save thumbnail</button>' if th else ""
    import engine.brand as br
    pin = br.PINNED.get(ep["slug"], "")
    pinp = f'\n    <p class="pin">{e(pin)}</p>' if pin else ""
    pinb = '\n      <button type="button" data-copy="pin" data-what="Pinned comment">Copy pinned comment</button>' if pin else ""
    return f"""<article class="card wide" id="{e(ep['slug'])}-full">
  {pic}
  <div class="body">
    <div class="meta"><span class="chip">THE FULL FILM · YOUTUBE · {film_day(ep['slug']):%a %-d %b}</span><span>{int(d // 60)}:{int(d % 60):02d} · 16:9 · the 1080p file is in the chat</span></div>
    <p class="hook">{e(title)}</p>
    <p class="post">{e(desc)}</p>
{pinp}
    <div class="row"><button class="main" type="button" data-copy="hook">Copy title</button>
      <button class="main" type="button" data-copy="post">Copy description</button>{tbtn}{pinb}</div>
    <p class="note" aria-live="polite"></p>
  </div>
</article>"""


def fresh(ep):
    """The shorts were cut after the current voice (so never a cut from an older pace or score)."""
    b = os.path.join(LAB, ep["dir"], "build")
    k, v = os.path.join(b, "shorts", "kit.json"), os.path.join(b, "lines.json")
    return os.path.exists(k) and os.path.exists(v) and os.path.getmtime(k) > os.path.getmtime(v)


def day(n):
    return START + datetime.timedelta(days=n - 1)


def film_day(slug):
    """A new full film every two days, in FILMS order."""
    return day(1 + 2 * FILMS.index(slug))


def first_day(slug):
    """The shorts' first day: the day the film goes up, so each film's shorts drive people to it (films two days
    apart and four to six days of shorts each overlap: two to four shorts a day)."""
    return 1 + 2 * FILMS.index(slug)


def episodes(page=1):
    by = {ep["slug"]: ep for ep in EPISODES}
    out = []
    for slug in PAGES[page]["slugs"]:
        ep = by[slug]
        if fresh(ep):
            out.append(dict(ep, kit={k["name"]: k for k in json.load(open(os.path.join(LAB, ep["dir"], "build", "shorts", "kit.json")))}))
    return out


BRAND = os.path.join(LAB, "out", "brand")
BRAND_FILES = ("banner.jpg", "avatar.png", "watermark.png", "facebook_cover.jpg", "x_header.jpg", "highlight_films.png",
               "highlight_space.png", "highlight_robots.png", "highlight_money.png")


def files(page=1):
    """The artifact files map: media/<slug>/<file> -> the mp4 on disk (and the channel art on page 1)."""
    out = {}
    if page == 1:
        for f in BRAND_FILES:
            if os.path.exists(os.path.join(BRAND, f)):
                out[f"media/brand/{f}"] = os.path.join(BRAND, f)
    for ep in episodes(page):
        for key in ("thumb",):
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
    d0 = first_day(slug)
    plan = "".join(f'<div class="day"><b>Day {d0 + i} · {day(d0 + i):%a %-d %b}</b><span>{html.escape(name(a))}</span>' +
                   (f'<span class="plus">{html.escape(name(b))}</span>' if b and b in kit else "") + "</div>"
                   for i, (_, a, b) in enumerate(ep["schedule"]) if a in kit)
    return f"""<section id="{slug}" class="ep">
  <div><span class="eyebrow">{html.escape(ep['title'])}</span><h2 class="ep-title">{html.escape(ep['sub'])}</h2></div>
  {full_card(ep) if ep.get("thumb") and os.path.exists(os.path.join(LAB, ep["thumb"])) else ""}
  <h3>Suggested order</h3>
  <div class="plan">{plan}</div>
  <h3>The whole film, in {len(parts)} parts</h3>
  <div class="grid">{''.join(card(k, slug) for k in parts)}</div>
  <h3>Highlights</h3>
  <div class="grid">{''.join(card(k, slug) for k in highs)}</div>
</section>"""


def start(page):
    """The upload checklist at the top: today's film, then the rhythm."""
    by = {ep["slug"]: ep for ep in EPISODES}
    films = "".join(f'<li><b>{film_day(sl):%a %-d %b}</b> {html.escape(by[sl]["title"])}'
                    f'{"" if sl in PAGES[page]["slugs"] else " <span class=muted>(on the other page)</span>"}</li>' for sl in FILMS)
    first = FILMS[0]
    today = (f"""<h2>First: {html.escape(by[first]["title"])} on YouTube</h2>
  <ol class="steps">
    <li>Google's Suncatcher satellite is set to launch on 1 Oct, so this one goes up first, while it's news. The 1080p
      file and the thumbnail are in the chat.</li>
    <li>YouTube app → Create (+) → Upload a video. Copy the title and description from the film's card below and add the
      thumbnail (Save thumbnail). Custom thumbnails need the channel verified once: YouTube → Settings → verify by phone.</li>
    <li>Audience: not made for kids. Altered or synthetic content: tick Yes (the narrator is an AI voice); it only adds a label.</li>
    <li>Then its Part 1 on TikTok, Instagram Reels, YouTube Shorts and Facebook: Save video, Copy caption, post. On TikTok,
      switch on "AI-generated content" under More options.</li>
  </ol>""" if first in PAGES[page]["slugs"] else "")
    setup = ""
    if page == 1 and os.path.exists(os.path.join(BRAND, "banner.jpg")):
        import engine.brand as br
        e = html.escape
        saves = "".join(f'<button type="button" data-save="media/brand/{f}">{n}</button>' for f, n in (
            ("banner.jpg", "YouTube banner"), ("avatar.png", "Profile picture (all)"), ("watermark.png", "YouTube watermark"),
            ("facebook_cover.jpg", "Facebook cover"), ("x_header.jpg", "X header"), ("highlight_films.png", "IG highlight: Films"),
            ("highlight_space.png", "IG highlight: Space"), ("highlight_robots.png", "IG highlight: Robots"),
            ("highlight_money.png", "IG highlight: Money")))
        texts = "".join(f"""<div class="txt"><b>{e(k)}</b><p class="t{i}">{e(v)}</p>
        <button type="button" data-copy="t{i}" data-what="{e(k)}">Copy</button></div>""" for i, (k, v) in enumerate((
            ("YouTube description", br.ABOUT), ("YouTube keywords", br.KEYWORDS), ("TikTok and Facebook bio", br.BIO),
            ("Instagram and X bio", br.IG_BIO), ("Instagram name field", "The Curve · AI explained"))))
        setup = f"""<h3>Set up the channel once</h3>
  <article class="card wide brand">
    <img class="thumb" src="media/brand/banner.jpg" alt="The Curve: the YouTube banner" loading="lazy">
    <div class="body">
      <div class="meta"><span class="chip">NAME: THE CURVE</span><span>handles to try, in order: @thecurve, @thecurveai, @thecurve.explained, @curveexplains (the same everywhere)</span></div>
      <div class="row">{saves}</div>
      {texts}
      <details><summary>The full set-up guide, platform by platform</summary><p class="post">{e(br.SETUP)}</p></details>
      <p class="note" aria-live="polite"></p>
    </div>
  </article>"""
    return f"""<section class="start" aria-label="Start here">
  <span class="eyebrow">Start here</span>
  {setup}
  {today}
  <h3>Then keep the rhythm</h3>
  <p>A new full film every two days. Its shorts start the same day: each day, post what the plans below list for that
    day (a part and a highlight per film, so two to four shorts a day), the same file on every platform, and pin each Part 1.</p>
  <ul class="films">{films}</ul>
  <p class="muted">Save time: schedule a week in one sitting. YouTube Studio schedules videos and Shorts; TikTok schedules from a
    computer up to 10 days ahead; Meta Business Suite schedules Reels to Instagram and Facebook together.</p>
</section>"""


def main(page=1):
    eps = episodes(page)
    n = sum(len(ep["kit"]) for ep in eps)
    nav = "".join(f'<a href="#{ep["slug"]}">{html.escape(ep["title"])}</a>' for ep in eps)
    for k, pg in PAGES.items():                                     # the other page, when it has a link
        if k != page and pg["url"]:
            others = " – ".join(s.upper() for s in (pg["slugs"][0], pg["slugs"][-1]))
            nav += f'<a href="{html.escape(pg["url"])}" target="_blank" rel="noopener">{others} → {html.escape(pg["title"])}</a>'
    doc = f"""<title>{PAGES[page]["title"]}</title>
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
.card img.thumb{{width:100%;max-width:100%;aspect-ratio:16/9;object-fit:cover;display:block;background:#000}}
.brand .hook{{font-size:15px;font-weight:600}}
.txt{{border-top:1px solid var(--line);padding-top:10px;display:grid;gap:6px}}
.txt b{{font:500 12px/1.3 "IBM Plex Mono",monospace;letter-spacing:.06em;color:var(--accent);text-transform:uppercase}}
.txt p,.pin{{margin:0;font-size:14px;color:var(--muted);overflow-wrap:anywhere}}
.txt button{{justify-self:start}}
.pin{{border-left:3px solid var(--accent);padding-left:10px}}
details summary{{cursor:pointer;font-weight:600;color:var(--accent)}}
details .post{{margin-top:8px}}
.day .plus{{margin-top:6px;padding-top:6px;border-top:1px dashed var(--line);color:var(--muted)}}
.start{{background:var(--surface);border:1px solid var(--accent);border-radius:14px;padding:18px 18px 20px;gap:10px}}
.start h2{{font-size:17px}}
.start ol,.start ul{{margin:0;padding-left:20px;display:grid;gap:6px;font-size:15px}}
.start p{{margin:0;font-size:15px}}
.muted{{color:var(--muted)}}
.films b{{font:500 12px/1.4 "IBM Plex Mono",monospace;letter-spacing:.06em;color:var(--accent);margin-right:6px}}
</style>
<div class="wrap">
<header>
  <span class="eyebrow">The Curve · posting kit</span>
  <h1>Shorts, ready to post</h1>
  <p class="lede">{n} vertical cuts from {len(eps)} film{"s" if len(eps) != 1 else ""}, voiced by George, for TikTok, Reels, YouTube Shorts and Facebook. Each film comes as parts that add up to the whole video, plus standalone highlights. Copy the caption, save the video, post.</p>
  <nav>{nav}</nav>
</header>
{start(page)}
{''.join(section(ep) for ep in eps)}
<footer>Every figure in these clips is sourced in its full video's end card. The files were also sent in the chat.</footer>
</div>
<script>{JS}</script>
"""
    out = PAGES[page]["out"]
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w").write(doc)
    print(out, n, "shorts from", len(eps), "films")
    return out


if __name__ == "__main__":
    import sys
    pg = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    main(pg)
    print(json.dumps(files(pg), indent=1))
