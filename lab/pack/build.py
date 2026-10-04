"""The upload pack: a page per batch with everything needed to post each film, ready on a phone.

An artifact holds 15 MB per file and 256 MiB per version, and films are bigger than a file, so each video is cut into
fragmented-MP4 pieces (an HLS rendition: init.mp4 + seg_###.mp4 + index.txt, the playlist: artifacts don't serve .m3u8). The page streams them with hls.js for a
preview, and its Download button fetches the pieces in order and saves them as one .mp4 (init + segments joined byte for
byte is a complete fragmented MP4, which YouTube, TikTok and phones accept).

    cd lab && python3 pack/build.py season1          # -> pack/build/season1/{index.html, media/...} + files.json
    cd lab && python3 pack/build.py new              # EP09-EP12 (each film, its thumbnails, shorts)
Publish: the Artifact tool with file_path=<dir>/index.html and files from files.json (64 MB per publish: batch it).
"""
import html
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.dirname(HERE)
sys.path.insert(0, LAB)
from engine import kit  # noqa: E402

MAX_SEG = 14_000_000


def segment(src, dst_dir, hls_time=30):
    """src -> dst_dir/{init.mp4, seg_###.mp4, index.txt}; shortens the target if any piece would pass 14 MB. The playlist
    is index.txt because artifacts don't serve .m3u8; hls.js reads it by its contents, not its name."""
    for ht in (hls_time, 15, 8, 4):
        if os.path.isdir(dst_dir):
            shutil.rmtree(dst_dir)
        os.makedirs(dst_dir)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-c", "copy", "-f", "hls", "-hls_time", str(ht),
                        "-hls_playlist_type", "vod", "-hls_segment_type", "fmp4", "-hls_fmp4_init_filename", "init.mp4",
                        "-hls_segment_filename", os.path.join(dst_dir, "seg_%03d.mp4"), os.path.join(dst_dir, "index.m3u8")],
                       check=True)
        segs = sorted(f for f in os.listdir(dst_dir) if f.startswith("seg_"))
        if max(os.path.getsize(os.path.join(dst_dir, f)) for f in segs) <= MAX_SEG:
            os.replace(os.path.join(dst_dir, "index.m3u8"), os.path.join(dst_dir, "index.txt"))
            return ["init.mp4"] + segs
    raise RuntimeError(f"{src}: a piece stays over {MAX_SEG} bytes")


def joined_ok(dst_dir, files, expect_s):
    """Join the pieces the way the page does and check the result decodes to the right length."""
    tmp = os.path.join(dst_dir, "_joined.mp4")
    with open(tmp, "wb") as out:
        for f in files:
            with open(os.path.join(dst_dir, f), "rb") as inp:
                shutil.copyfileobj(inp, out)
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", tmp],
                       capture_output=True, text=True)
    dur = float(r.stdout.strip() or 0)
    os.remove(tmp)
    return abs(dur - expect_s) < 1.0, dur


def probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                       capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


def mb(path):
    return os.path.getsize(path) / 1e6


def esc(s):
    return html.escape(s, quote=True)


def copy_block(label, text, rows=None):
    tid = "t" + str(abs(hash((label, text))) % 10**9)
    area = (f'<textarea id="{tid}" readonly rows="{rows}">{esc(text)}</textarea>' if rows else
            f'<input id="{tid}" readonly value="{esc(text)}">')
    return (f'<div class="copy"><div class="copy-head"><span class="lab">{esc(label)}</span>'
            f'<button class="btn ghost" type="button" data-copy="{tid}">Copy</button></div>{area}</div>')


def film_card(item, media_rel):
    v = item["video"]
    thumbs = "".join(
        f'<figure class="thumb"><img src="{esc(media_rel + t["file"])}" alt="{esc(t["alt"])}" loading="lazy">'
        f'<figcaption><span>{esc(t["label"])}</span><button class="btn ghost" type="button" data-save="{esc(media_rel + t["file"])}" '
        f'data-name="{esc(t["name"])}">Save</button></figcaption></figure>' for t in item["thumbs"])
    titles = "".join(copy_block(("Title " + chr(65 + i)) + (" (recommended)" if i == 0 else ""), t) for i, t in enumerate(item["titles"]))
    steps = "".join(f"<li>{s}</li>" for s in item["steps"])
    return f"""
<section class="film" id="{esc(item['slug'])}">
  <div class="film-head">
    <p class="eyebrow">{esc(item['eyebrow'])}</p>
    <h2>{esc(item['name'])}</h2>
    <p class="meta">{esc(item['meta'])}</p>
  </div>
  <div class="film-grid">
    <div class="col-media">
      <div class="player{' tall' if item.get('vertical') else ''}"><video controls playsinline preload="none" poster="{esc(media_rel + item['thumbs'][0]['file'])}"
        data-hls="{esc(media_rel + v['dir'] + '/index.txt')}"></video></div>
      <div class="dl">
        <button class="btn primary" type="button" data-video="{esc(media_rel + v['dir'] + '/')}" data-files="{esc(json.dumps(v['files']))}"
          data-name="{esc(v['name'])}">Download the 1080p {'short' if item.get('vertical') else 'film'} · {v['mb']:.0f} MB</button>
        <div class="bar" hidden><div class="fill"></div></div>
        <p class="note" aria-live="polite"></p>
      </div>
      <div class="thumbs">{thumbs}</div>
    </div>
    <div class="col-copy">
      {copy_block("TikTok / Reels caption", item['caption'], 4) if item.get('caption') else ''}
      {titles}
      {copy_block("Description (with chapters and sources)", item['description'], 9)}
      {copy_block("Pinned comment", item['pinned'])}
      <div class="steps"><p class="lab">In YouTube Studio</p><ol>{steps}</ol></div>
    </div>
  </div>
  {shorts_block(item, media_rel)}
</section>"""


def shorts_block(item, media_rel):
    if not item.get("shorts"):
        return ""
    cards = "".join(
        f'<div class="short"><video controls playsinline preload="none" src="{esc(media_rel + s["file"])}"></video>'
        f'<div class="short-copy"><p class="lab">{esc(s["when"])}</p><p class="hook">{esc(s["hook"])}</p>'
        f'<button class="btn ghost" type="button" data-copytext="{esc(s["caption"])}">Copy caption</button> '
        f'<button class="btn ghost" type="button" data-save="{esc(media_rel + s["file"])}" data-name="{esc(s["name"])}">Save</button></div></div>'
        for s in item["shorts"])
    return f'<div class="shorts"><p class="lab">Shorts · TikTok, Reels, YouTube Shorts, Facebook</p><div class="short-grid">{cards}</div></div>'


CSS = """
:root{
  /* layout: one column of film sheets; each sheet = media column (player, download, thumbnails) + copy column */
  --bg:#06090A; --panel:#0D1415; --line:#1B2829; --ink:#E4EEEC; --muted:#8FA4A1; --accent:#35D6C6; --accent-ink:#04110F;
  --display:"Michroma","Eurostile",ui-sans-serif,system-ui,sans-serif;
  --body:"Inter Tight",ui-sans-serif,system-ui,-apple-system,sans-serif;
  --mono:"IBM Plex Mono",ui-monospace,SFMono-Regular,Menlo,monospace;
  color-scheme:dark}
body{background:var(--bg);color:var(--ink);font:15px/1.55 var(--body);margin:0}
.wrap{max-width:1120px;margin:0 auto;padding-inline:16px;padding-block:28px 64px;display:grid;gap:40px}
header{display:grid;gap:10px}
h1{font:400 clamp(26px,5vw,40px)/1.15 var(--display);letter-spacing:.02em;margin:0;text-wrap:balance}
h2{font:400 clamp(20px,3.6vw,28px)/1.2 var(--display);margin:0;text-wrap:balance}
.lede{color:var(--muted);max-width:68ch;margin:0}
.eyebrow,.lab{font:500 11.5px/1.3 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--accent);margin:0}
.meta{color:var(--muted);margin:0;font-variant-numeric:tabular-nums}
.order{display:flex;flex-wrap:wrap;gap:8px;margin:0;padding:0;list-style:none}
.order li{font:500 12.5px/1.2 var(--mono);border:1px solid var(--line);border-radius:999px;padding:7px 12px;color:var(--ink)}
.order b{color:var(--accent);font-weight:500}
.film{display:grid;gap:18px;border-top:1px solid var(--line);padding-top:28px}
.film-head{display:grid;gap:6px}
.film-grid{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);gap:24px}
@media (max-width:820px){.film-grid{grid-template-columns:minmax(0,1fr)}}
.col-media,.col-copy{display:grid;gap:14px;align-content:start;min-width:0}
.player{aspect-ratio:16/9;max-width:100%;background:#000;border:1px solid var(--line);border-radius:10px;overflow:hidden}
.player video{width:100%;height:100%;display:block;background:#000}
.player.tall{aspect-ratio:9/16;max-width:420px;margin:0 auto}
.dl{display:grid;gap:8px}
.btn{font:500 14px/1 var(--body);border-radius:8px;padding:11px 14px;cursor:pointer;border:1px solid var(--line);
  background:transparent;color:var(--ink)}
.btn.primary{background:var(--accent);color:var(--accent-ink);border-color:var(--accent);font-weight:600}
.btn.ghost{padding:7px 10px;font-size:13px}
.btn:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.btn:disabled{opacity:.6;cursor:progress}
.bar{height:6px;border-radius:999px;background:var(--line);overflow:hidden}
.fill{height:100%;width:0;background:var(--accent);transition:width .2s}
.note{margin:0;color:var(--muted);font-size:13px;min-height:1.2em}
.thumbs{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px}
.thumb{margin:0;display:grid;gap:6px}
.thumb img{border-radius:6px;border:1px solid var(--line);aspect-ratio:16/9;object-fit:cover;width:100%}
.thumb figcaption{display:flex;justify-content:space-between;align-items:center;gap:8px;font:12px/1.3 var(--mono);color:var(--muted)}
.copy{display:grid;gap:6px}
.copy-head{display:flex;justify-content:space-between;align-items:center;gap:10px}
.copy input,.copy textarea{width:100%;box-sizing:border-box;background:var(--panel);color:var(--ink);border:1px solid var(--line);
  border-radius:8px;padding:10px 12px;font:13.5px/1.5 var(--body);resize:vertical}
.steps ol{margin:6px 0 0;padding-left:20px;display:grid;gap:4px;color:var(--ink)}
.steps li{padding-left:2px}
.shorts{display:grid;gap:10px}
.short-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:12px}
.short{display:grid;gap:8px;align-content:start;min-width:0}
.short video{aspect-ratio:9/16;width:100%;max-width:100%;background:#000;border-radius:8px;border:1px solid var(--line)}
.short-copy{display:grid;gap:6px}
.hook{margin:0;font-size:13.5px}
footer{color:var(--muted);font-size:13px;border-top:1px solid var(--line);padding-top:18px}
@media (prefers-reduced-motion:reduce){.fill{transition:none}}
"""

JS = """
const dlp = (window.claude && window.claude.use) ? window.claude.use("downloads") : Promise.resolve(null);
function note(el, s){ if(el) el.textContent = s; }
async function saveBlob(blob, name, out){
  const d = await dlp;
  if(!d){ note(out, "Saving isn't available in this view. Open the page in the Claude app or claude.ai."); return; }
  try { await d.save({filename:name, data:blob}); note(out, "Saved: " + name); }
  catch(e){ note(out, e && e.code === "declined" ? "Not saved." : (e && e.code === "too_large" ? "Too large for this app: open the page on claude.ai in a browser." : "Couldn't save (" + (e && e.code || "error") + ").")); }
}
document.addEventListener("click", async (ev) => {
  const b = ev.target.closest("button"); if(!b) return;
  if(b.dataset.copy || b.dataset.copytext !== undefined){
    const el = b.dataset.copy ? document.getElementById(b.dataset.copy) : null;
    const text = el ? el.value : b.dataset.copytext;
    try { await navigator.clipboard.writeText(text); const t=b.textContent; b.textContent="Copied"; setTimeout(()=>b.textContent=t,1400); }
    catch(e){ if(el){ el.focus(); el.select(); } }
    return;
  }
  if(b.dataset.save){
    const out = b.closest(".film, .short")?.querySelector(".note");
    try { const r = await fetch(b.dataset.save); if(!r.ok) throw new Error(r.status); await saveBlob(await r.blob(), b.dataset.name, out); }
    catch(e){ note(out, "Couldn't fetch the file."); }
    return;
  }
  if(b.dataset.video){
    const box = b.closest(".dl"), bar = box.querySelector(".bar"), fill = box.querySelector(".fill"), out = box.querySelector(".note");
    const files = JSON.parse(b.dataset.files); const parts = [];
    b.disabled = true; bar.hidden = false;
    try {
      for(let i = 0; i < files.length; i++){
        const r = await fetch(b.dataset.video + files[i]); if(!r.ok) throw new Error(files[i] + " " + r.status);
        parts.push(await r.blob());
        fill.style.width = Math.round(100 * (i + 1) / files.length) + "%";
        note(out, "Fetching " + (i + 1) + " of " + files.length + " pieces...");
      }
      await saveBlob(new Blob(parts, {type:"video/mp4"}), b.dataset.name, out);
    } catch(e){ note(out, "A piece didn't load (" + e.message + "). Tap again to retry."); }
    b.disabled = false;
  }
});
function attach(v){
  const src = v.dataset.hls; if(!src || v.dataset.ready) return; v.dataset.ready = "1";
  if(v.canPlayType("application/vnd.apple.mpegurl")){ v.src = src; return; }
  if(window.Hls && window.Hls.isSupported()){ const h = new Hls({maxBufferLength:20}); h.loadSource(src); h.attachMedia(v); }
}
document.querySelectorAll("video[data-hls]").forEach(v => {
  v.addEventListener("play", () => attach(v), {once:true});
  v.addEventListener("click", () => attach(v), {once:true});
  v.closest(".player").addEventListener("pointerdown", () => attach(v), {once:true});
});
"""


def page(title, lede, order, items, media_rel="media/"):
    order_li = "".join(f"<li><b>{esc(a)}</b> {esc(b)}</li>" for a, b in order)
    body = "".join(film_card(it, media_rel) for it in items)
    return f"""<title>{esc(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Inter+Tight:wght@400;500;600&family=Michroma&display=swap">
<style>{CSS}</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/hls.js/1.5.13/hls.min.js"></script>
<div class="wrap">
<header>
  <p class="eyebrow">The Curve · upload pack</p>
  <h1>{esc(title)}</h1>
  <p class="lede">{esc(lede)}</p>
  <ul class="order">{order_li}</ul>
</header>
{body}
<footer>Tap a player to preview. Download joins the film's pieces into one 1080p .mp4 on your device: on a phone, keep the page open until it says Saved.
The narrator is an AI voice, so tick "Altered or synthetic content" on every upload.</footer>
</div>
<script>{JS}</script>
"""


def write(name, title, lede, order, items, extra_files):
    out = os.path.join(HERE, "build", name)
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, "index.html"), "w").write(page(title, lede, order, items))
    files = {}
    for it in items:
        for f in it["video"]["files"] + ["index.txt"]:
            files[f"media/{it['video']['dir']}/{f}"] = os.path.join(out, "media", it["video"]["dir"], f)
    files.update(extra_files)
    json.dump(files, open(os.path.join(out, "files.json"), "w"), indent=1)
    total = sum(os.path.getsize(p) for p in files.values())
    print(out, len(files), "files", round(total / 2**20, 1), "MiB")
    return out


def video_entry(src, out_media, name, dirname):
    files = segment(src, os.path.join(out_media, dirname))
    ok, dur = joined_ok(os.path.join(out_media, dirname), files, probe(src))
    assert ok, (src, dur)
    return dict(dir=dirname, files=files, name=name, mb=mb(src), dur=dur)


STEPS_FILM = [
    "Upload the .mp4. Paste the title, description and thumbnail.",
    "Audience: not made for kids. Altered or synthetic content: Yes (the narrator is an AI voice).",
    "Playlists: Every film, plus the topic playlist. Category: Education.",
    "End screen (last 15 s): Subscribe + Best for viewer.",
    "Publish or schedule, then post the pinned comment and pin it.",
]


SEASON_PAGES = {
    "1": dict(name="The Curve: Season One", films="five", day="the day after the fifth film",
              titles=["What the AI Headlines Don't Tell You ({mins}-Minute Documentary)",
                      "5 Hidden Forces Behind the AI Boom | The Curve: Season One",
                      "Why AI Is Leaving the Planet, and 4 Other Things the Headlines Miss"],
              pinned="Which of the five surprised you most? Every figure is sourced in the description.",
              first="Post the five films on their days"),
    "2": dict(name="The Curve: Season Two", films="four", day="Tue 20 Oct, the day after EP12",
              titles=["How AI Really Works: 4 Hidden Mechanisms ({mins}-Minute Documentary)",
                      "Why AI Makes Things Up, and 3 Other Things the Headlines Miss",
                      "Robots, Rules, Wrong Answers and 16-Hour Tasks | The Curve: Season Two"],
              pinned="Which of the four changed your mind? Every figure is sourced in the description.",
              first="Post EP09 to EP12 on their days (13 to 19 Oct)"),
}


def season2():
    season1("2")


def season1(n="1"):
    os.environ["SEASON"] = n
    cfg = SEASON_PAGES[n]
    sys.path.insert(0, os.path.join(LAB, "season1"))
    import make as s1
    out = os.path.join(HERE, "build", f"season{n}")
    media = os.path.join(out, "media")
    os.makedirs(media, exist_ok=True)
    meta = json.load(open(os.path.join(s1.BUILD, f"season{n}.json")))
    word = {"1": "One", "2": "Two"}[n]
    v = video_entry(s1.OUT, media, f"The_Curve_Season_{word}_1080p.mp4", f"season{n}")
    thumbs, extra = [], {}
    for k, label in zip("abc", ("A", "B", "C")):
        src = os.path.join(s1.BUILD, f"thumb_{k}.jpg")
        if os.path.exists(src):
            shutil.copy(src, os.path.join(media, f"thumb_{k}.jpg"))
            extra[f"media/thumb_{k}.jpg"] = os.path.join(media, f"thumb_{k}.jpg")
            thumbs.append(dict(file=f"thumb_{k}.jpg", label=f"Thumbnail {label}", alt=f"Season {word} thumbnail option {label}",
                               name=f"The_Curve_Season_{word}_thumbnail_{label}.jpg"))
    m, s = divmod(int(round(meta["duration"])), 60)
    mins = int(meta["duration"] // 60)                       # "14-minute" for 14:06: a title never rounds up
    item = dict(
        slug=f"season-{word.lower()}", eyebrow=f"Long-form · {m}:{s:02d} · 1080p", name=cfg["name"],
        meta=f"The {cfg['films']} films as one documentary, with chapters. Long videos earn watch hours and, past 8 minutes, mid-roll ads.",
        video=v, thumbs=thumbs,
        titles=[t_.format(mins=mins) for t_ in cfg["titles"]],
        description=open(os.path.join(s1.BUILD, "description.txt")).read(),
        pinned=cfg["pinned"],
        steps=STEPS_FILM[:2] + ["Playlists: Every film. Category: Education. Chapters come from the timestamps in the description.",
                                "Monetisation (once the channel is in the Partner Programme): put mid-roll ads at the chapter breaks.",
                                STEPS_FILM[3], STEPS_FILM[4]],
        shorts=[])
    lede = (f"Season {word} is the {cfg['films']} films in one {mins}-minute documentary, ready to upload: the 1080p file, three "
            "thumbnails, titles, a description with chapters and every source, and the settings to tick.")
    order = [("1", cfg["first"]), ("2", f"Then Season {word}, {cfg['day']}"),
             ("3", "Shorts keep running daily, pointing back to the films")]
    write(f"season{n}", cfg["name"], lede, order, [item], extra)


ALT_TITLES = {
    "ep09": ["AI Won Gold at the Maths Olympiad. It Still Can't Fold a Towel.",
             "The Laundry Problem: Why the Easy Things Are Hardest for Robots"],
    "ep10": ["10^25: The Number Europe Uses to Watch AI", "Why AI Law Counts Calculations, Not Danger"],
    "ep11": ["Why AI Is Confidently Wrong (and When It Isn't)", "The Library of Every Book: What AI Keeps from What It Reads"],
    "ep12": ["From 2 Seconds to 16 Hours: How Fast AI Is Really Moving", "The Ruler Is Running Out: AI's 16-Hour Tasks"],
    "ep13": ["The AI Price War, Explained in 3 Minutes", "Why AI Gets Cheaper Every Month: The Red Queen Race"],
    "ep14": ["The Yes Machine: Why AI Tells You What You Want to Hear", "A Thumbs-Up Button Taught ChatGPT to Flatter"],
}


STEPS_SHORT = [
    "Upload the .mp4 to TikTok, YouTube Shorts and Instagram Reels: the same file works on all three.",
    "Turn on the AI label everywhere (TikTok: AI-generated content; YouTube: altered or synthetic content: Yes).",
    "Upload the cover image as the cover, then paste the caption (TikTok, Reels) or the title and description (YouTube).",
    "YouTube: audience not made for kids.",
    "Post the pinned comment and pin it.",
]
SHORTS = [("lustig", "Money crimes · Short 01"), ("spin", "What if · Short 01")]


def post_copy(path):
    """POST.md -> caption, YouTube title, description, pinned comment."""
    t = open(path).read()
    cut = lambda a, b: t.split(a, 1)[1].split(b, 1)[0].strip() if a in t else ""
    one = lambda x: " ".join(x.split())
    return dict(caption=cut("**TikTok / Reels caption**", "**YouTube Shorts title:**"),
                title=one(cut("**YouTube Shorts title:**", "\n")), description=one(cut("**Description:**", "**Pinned comment:**")),
                pinned=one(t.split("**Pinned comment:**", 1)[1]) if "**Pinned comment:**" in t else "")


def shorts_page(name="shorts", title="AI shorts: Money crimes and What if"):
    """The AI shorts (lab/shorts/<slug>/out): each 1080x1920 master, its cover, caption, YouTube copy and pinned comment."""
    out = os.path.join(HERE, "build", name)
    media = os.path.join(out, "media")
    os.makedirs(media, exist_ok=True)
    items, extra, order = [], {}, []
    for slug, channel in SHORTS:
        d = os.path.join(LAB, "shorts", slug)
        master = [os.path.join(d, "out", f) for f in sorted(os.listdir(os.path.join(d, "out"))) if f.endswith("_9x16.mp4")][0]
        pc = post_copy(os.path.join(d, "POST.md"))
        v = video_entry(master, media, f"{slug}_9x16_1080p.mp4", slug)
        f = f"{slug}_cover.jpg"
        shutil.copy(os.path.join(d, "out", "cover.jpg"), os.path.join(media, f))
        extra[f"media/{f}"] = os.path.join(media, f)
        items.append(dict(slug=slug, eyebrow=f"{channel} · {int(round(v['dur']))} s · 9:16", name=pc["title"], vertical=True,
                          meta="Made with AI: GPT Image 2.5 stills, Kling 3.0 and Veo 3.1 motion, a Higgsfield voice; our own edit and sound (music credits are in the description).",
                          video=v, thumbs=[dict(file=f, label="Cover", alt=pc["title"] + " cover", name=f)], caption=pc["caption"],
                          titles=[pc["title"]], description=pc["description"], pinned=pc["pinned"], steps=STEPS_SHORT, shorts=[]))
        order.append((channel.split(" · ")[0], pc["title"]))
    lede = ("Cinematic AI shorts for TikTok, YouTube Shorts and Reels: photoreal AI scenes, a narrator, kinetic captions, an "
            "score. Each has its 1080x1920 file, cover, caption, YouTube copy and pinned comment.")
    write(name, title, lede, order, items, extra)


LONGFORM = {
    "lustig": ("Money crimes · Long-form 01", "Money_Crimes_01_The_Man_Who_Sold_the_Eiffel_Tower"),
    "ponzi": ("Money crimes · Long-form 02", "Money_Crimes_02_The_Original_Ponzi_Scheme", None, None,
              "Money Crimes' second long-form film, ready to upload"),
    "lf01_escape": ("The Curve · Long-form 01", "The_Curve_01_The_AI_That_Escaped", "curvelf",
                    "The channel's look at full length: AI pictures and big numbers turned into characters, typed labels, "
                    "live captions and a house score. Past 8 minutes, YouTube allows mid-roll ads.",
                    "The Curve's first long-form film, ready to upload"),
    "lf02_price": ("The Curve · Long-form 02", "The_Curve_02_The_Price_of_Thinking", "curvelf",
                   "The channel's look at full length: AI pictures and big numbers turned into characters, typed labels, "
                   "live captions and a house score. Past 8 minutes, YouTube allows mid-roll ads.",
                   "The Curve's second long-form film, ready to upload"),
    "lf03_held": ("The Curve · Long-form 03", "The_Curve_03_Too_Dangerous_to_Release", "curvelf",
                  "The channel's look at full length: AI pictures and big numbers turned into characters, typed labels, "
                  "live captions and a house score. Past 8 minutes, YouTube allows mid-roll ads.",
                  "The Curve's third long-form film, ready to upload"),
    "ep01": ("How They Profit · Film 01", "How_They_Profit_01_Banks_With_Wings", "ch2",
             "The channel's ledger look: every figure on screen with its source, a calm narrator and an original score. "
             "The last 15 seconds are the end card, clear for YouTube's end-screen elements.",
             "How They Profit's first film, ready to upload"),
}


def longform_page(slug="lustig"):
    """A long-form film (lab/longform/<slug> or lab/curvelf/<slug>): the 1080p file, three thumbnails, titles, the
    description with chapters and credits, the pinned comment and the upload settings, all from its POST.md."""
    channel, fname = LONGFORM[slug][:2]
    where, meta, lede_1 = (LONGFORM[slug] + (None,) * 3)[2:5]
    d = os.path.join(LAB, where or "longform", slug)
    post = open(os.path.join(d, "POST.md")).read()
    sec = lambda h: post.split(f"## {h}\n", 1)[1].split("\n## ", 1)[0].strip()
    title_block = sec("Title")
    titles = [title_block.split("**")[1]] + [ln[2:].strip() for ln in title_block.splitlines() if ln.startswith("- ")]
    out = os.path.join(HERE, "build", slug)
    media = os.path.join(out, "media")
    os.makedirs(media, exist_ok=True)
    v = video_entry(os.path.join(d, "out", f"{slug}_1080p.mp4"), media, f"{fname}_1080p.mp4", slug)
    DEF_META = ("A documentary with chapters: AI reconstructions (labelled on screen), real archive photographs, maps and "
                "a jazz score. Past 8 minutes, YouTube allows mid-roll ads.")
    thumbs, extra = [], {}
    for k, label in zip("abc", ("A", "B", "C")):
        src = os.path.join(d, "out", f"thumb_{k}.jpg")
        if os.path.exists(src):
            shutil.copy(src, os.path.join(media, f"thumb_{k}.jpg"))
            extra[f"media/thumb_{k}.jpg"] = os.path.join(media, f"thumb_{k}.jpg")
            thumbs.append(dict(file=f"thumb_{k}.jpg", label=f"Thumbnail {label}", alt=f"{titles[0]}: thumbnail {label}",
                               name=f"{fname}_thumbnail_{label}.jpg"))
    m, s_ = divmod(int(round(v["dur"])), 60)
    steps = [ln[2:].replace("**", "") for ln in sec("Upload settings").splitlines() if ln.startswith("- ")]
    item = dict(slug=slug, eyebrow=f"{channel} · {m}:{s_:02d} · 1080p", name=titles[0],
                meta=meta or DEF_META,
                video=v, thumbs=thumbs, titles=titles, description=sec("Description"), pinned=sec("Pinned comment"),
                steps=["Upload the .mp4 and paste the title and description (the chapters come from its timestamps)."] + steps +
                      ["Put all three thumbnails in Test & Compare.", "Publish, then post the pinned comment and pin it."],
                shorts=[])
    lede = (lede_1 or "The first long-form film, ready to upload") + (
        f": {m}:{s_:02d} at 1080p, three thumbnails to test against each other, titles, a description with chapters, "
        "sources and credits, and the settings to tick.")
    order = [("1", "Upload this film: long-form is the money product"),
             ("2", "Then post its shorts (shorts page) as trailers, each linked to this film"),
             ("3", "Pin the comment, and add the end screen")]
    write(slug, titles[0], lede, order, [item], extra)


def film_shorts_page(slug="lustig"):
    """The vertical shorts cut from a long-form film (lab/longform/<slug>/out/short_*_9x16.mp4, copy in its shorts.py)."""
    import importlib.util
    sys.path.insert(0, os.path.join(LAB, "music", "jazz"))
    import library as jazz
    d = os.path.join(LAB, (LONGFORM[slug] + (None,) * 3)[2] or "longform", slug)
    spec = importlib.util.spec_from_file_location("film_shorts", os.path.join(d, "shorts.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    channel = LONGFORM[slug][0].split(" · ")[0]
    name = f"{slug}_shorts"
    out = os.path.join(HERE, "build", name)
    media = os.path.join(out, "media")
    os.makedirs(media, exist_ok=True)
    items, order, extra = [], [], {}
    for key, sp in mod.SHORTS.items():
        src = os.path.join(d, "out", f"short_{key}_9x16.mp4")
        if not os.path.exists(src):
            continue
        v = video_entry(src, media, f"{slug}_{key}_9x16.mp4", f"{slug}_{key}")
        cover = f"{slug}_{key}_cover.jpg"                    # a frame from the short's opening, as its cover
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "2.5", "-i", src, "-frames:v", "1", "-q:v", "3",
                        os.path.join(media, cover)], check=True)
        extra[f"media/{cover}"] = os.path.join(media, cover)
        items.append(dict(slug=f"{slug}-{key}", eyebrow=f"{channel} · Short from the film · {int(round(v['dur']))} s · 9:16",
                          name=sp["title"], vertical=True,
                          meta=f"Cut from the long-form film \"{sp['film']}\": its picture, narration and score, with captions and an end card that sends viewers to the full film.",
                          video=v, thumbs=[dict(file=cover, label="Cover", alt=sp["title"] + " cover", name=cover)],
                          caption=sp["caption"], titles=[sp["title"]],
                          description=f"{sp['caption']} Full story: {sp['film']} (linked)." + (
                              "\n\n" + jazz.credit_line(sp["music"]) if sp.get("music") else ""), pinned=sp["pinned"],
                          steps=STEPS_SHORT[:2] + ["YouTube: set the full film as this Short's related video, so viewers can tap through to it.",
                                                   "TikTok and Reels: pin a comment naming the full film on YouTube."] + STEPS_SHORT[3:],
                          shorts=[]))
        order.append(("Short", sp["title"]))
    lede = ("Shorts cut from the long-form film, for TikTok, YouTube Shorts and Reels: each is a stretch of the film with its "
            "narration, a headline, live captions and an end card that sends people to the full documentary.")
    write(name, f"{LONGFORM[slug][0].split(' · ')[0]}: shorts from the film", lede, order, items, extra)


def new(slugs=("ep09", "ep10", "ep11", "ep12"), name="new", title="The Curve: EP09 to EP12"):
    """The next four films: each film's 1080p file, two thumbnails, titles, description with sources, pinned comment and
    its shorts with captions and posting days."""
    import datetime
    import engine.brand as br
    out = os.path.join(HERE, "build", name)
    media = os.path.join(out, "media")
    os.makedirs(media, exist_ok=True)
    by = {e["slug"]: e for e in kit.EPISODES}
    items, extra, order = [], {}, []
    for slug in slugs:
        ep = by[slug]
        b = os.path.join(LAB, ep["dir"], "build")
        master = os.path.join(b, f"{slug}.mp4")
        if not os.path.exists(master):
            print("skip", slug, "(no master yet)")
            continue
        v = video_entry(master, media, f"The_Curve_{ep['title'].split(' · ')[0]}_1080p.mp4", slug)
        fday = kit.film_day(slug)
        thumbs = []
        for k in "ab":
            src = os.path.join(b, f"{slug}_thumb_{k}.jpg")
            if os.path.exists(src):
                f = f"{slug}_thumb_{k}.jpg"
                shutil.copy(src, os.path.join(media, f))
                extra[f"media/{f}"] = os.path.join(media, f)
                thumbs.append(dict(file=f, label=f"Thumbnail {k.upper()}", alt=f"{ep['title']} thumbnail {k.upper()}",
                                   name=f"{slug}_thumbnail_{k.upper()}.jpg"))
        shorts = []
        kp = os.path.join(b, "shorts", "kit.json")
        if os.path.exists(kp):
            for i, k in enumerate(json.load(open(kp))):
                src = os.path.join(b, "shorts", k["file"])
                f = f"{slug}_{k['file']}"
                if os.path.getsize(src) > 15_000_000:
                    continue
                shutil.copy(src, os.path.join(media, f))
                extra[f"media/{f}"] = os.path.join(media, f)
                when = fday + datetime.timedelta(days=i)
                shorts.append(dict(file=f, when=f"{when:%a %-d %b} · {k['tag']}", hook=k["hook"], caption=k["post"],
                                   name=f"{slug}_{k['file']}"))
        title_main, blurb = ep["yt"]
        desc = (blurb + "\n\nSources:\n" + "\n".join("• " + x for x in kit.sources(ep)) +
                "\n\nThe narrator is an AI voice (ElevenLabs). Labelled what-ifs are imagined, not forecasts.")
        d = v["dur"]
        items.append(dict(
            slug=slug, eyebrow=f"Film · {int(d // 60)}:{int(d % 60):02d} · goes up {fday:%a %-d %b}", name=ep["title"],
            meta=ep["sub"], video=v, thumbs=thumbs or [dict(file="", label="", alt="", name="")],
            titles=[title_main] + ALT_TITLES.get(slug, []), description=desc, pinned=br.PINNED.get(slug, ""),
            steps=STEPS_FILM, shorts=shorts))
        order.append((f"{fday:%-d %b}", ep["title"].split(" · ")[1]))
    lede = ("The next films on the calendar, finished: George at his own pace over house and garage beds, captions burned in, -14 LUFS. "
            "Each has its 1080p file, thumbnails, titles, a description with every source, the pinned comment, and its "
            "shorts with captions and posting days.")
    write(name, title, lede, order, items, extra)


if __name__ == "__main__":
    {"season1": season1, "season2": season2, "new": new, "shorts": shorts_page, "lustig": longform_page,
     "lustig_shorts": film_shorts_page,
     "lf01": lambda: longform_page("lf01_escape"), "lf01_shorts": lambda: film_shorts_page("lf01_escape"),
     "lf02": lambda: longform_page("lf02_price"), "lf02_shorts": lambda: film_shorts_page("lf02_price"),
     "lf03": lambda: longform_page("lf03_held"), "lf03_shorts": lambda: film_shorts_page("lf03_held"),
     "htp01": lambda: longform_page("ep01"),
     "ponzi": lambda: longform_page("ponzi"), "ponzi_shorts": lambda: film_shorts_page("ponzi"),
     # EP04-EP08 with their shorts are ~310 MiB, over one artifact version's 256 MiB: two pages, in upload order
     "films1": lambda: new(("ep05", "ep08", "ep04"), "films1", "The Curve: EP05, EP08, EP04"),
     "films2": lambda: new(("ep06", "ep07"), "films2", "The Curve: EP06, EP07")}[sys.argv[1]]()
