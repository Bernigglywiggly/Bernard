#!/usr/bin/env python3
"""Build the Walk-in Reels page (sales/reels/index.html) from build/reels/manifest.json and print the files map.

    python3 sales/reels/page.py                 # every town with rendered Reels, plus the monthly sample
    python3 sales/reels/page.py --files Stone   # print only that town's files (publishes are capped at 64 MB)
    python3 sales/reels/page.py --towns Stone,Tamworth   # list only these towns (one still rendering stays off)
"""
import html
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MONTHS = "January February March April May June July August September October November December".split()
TRACKER = "https://claude.ai/artifact/2f7kucmy3ptWePJ4UPgNUU"
TOWNS = ["Stone", "Newcastle-under-Lyme", "Tamworth"]           # the walking order of the towns
e = html.escape


def month(d):
    y, m, _ = d.split("-")
    return f"{MONTHS[int(m) - 1]} {y}"


def anchor(town):
    return town.split("-")[0].lower()


def card(r):
    street = ", ".join(p.strip() for p in r["address"].split(",") if p.strip().lower() not in ("staffordshire",))
    msg = (f"Hi, it's {{me}}. Here's the Reel I made for {r['name']}. It's yours to post on Instagram, Facebook or "
           f"TikTok, and it shows your 5 for food hygiene from {month(r['fsaDate'])}. If you'd like four a month like "
           f"this with your own dishes, just reply here.")
    return f"""
<article class="shop" id="r{r['id']}" data-id="{r['id']}">
  <video controls playsinline preload="none" poster="reels/{e(r['poster'])}" src="reels/{e(r['file'])}"
         aria-label="Demo Reel for {e(r['name'])}"></video>
  <div class="info">
    <p class="stub">No. {r['order']} on the route</p>
    <h3>{e(r['name'])}</h3>
    <p class="addr">{e(street)}</p>
    <p class="chip">Food hygiene 5 · inspected {month(r['fsaDate'])}</p>
    <div class="acts">
      <button type="button" data-save="reels/{e(r['file'])}" data-name="{e(r['file'])}">Save video</button>
      <button type="button" class="ghost" data-copy="{r['id']}">Copy message</button>
    </div>
    <p class="msg" id="m{r['id']}" data-tpl="{e(msg)}"></p>
    <label class="done"><input type="checkbox" id="v{r['id']}"> Visited</label>
    <p class="note" aria-live="polite"></p>
  </div>
</article>"""


def load(only=None):
    rows = json.load(open(os.path.join(HERE, "build", "reels", "manifest.json")))
    towns = [t for t in TOWNS if any(r["town"] == t for r in rows) and (not only or t in only)]
    sample = next((r for r in rows if r["town"] == "Sample"), None)
    return rows, towns, sample


def build(only=None):
    rows, towns, sample = load(only)
    n = sum(1 for r in rows if r["town"] in towns)
    nav = "".join(f'<a href="#{anchor(t)}">{e(t.split("-")[0])} <b>{sum(r["town"] == t for r in rows)}</b></a>' for t in towns)
    sections = "".join(f"""
  <section class="town" id="{anchor(t)}" aria-labelledby="h-{anchor(t)}">
    <h2 id="h-{anchor(t)}">{e(t)}</h2>
    <div class="list">{"".join(card(r) for r in rows if r["town"] == t)}
    </div>
  </section>""" for t in towns)
    monthly = "" if not sample else f"""
  <section class="sample" aria-labelledby="h-monthly">
    <video controls playsinline preload="none" poster="reels/{e(sample['poster'])}" src="reels/{e(sample['file'])}"
           aria-label="Sample of a monthly Reel"></video>
    <div class="info">
      <p class="stub">Sample · not a real shop</p>
      <h2 id="h-monthly">What the monthly ones look like</h2>
      <p>Same kitchen ticket, their content: tonight's special, a new dish, opening hours, the Christmas menu. They send
        a photo or the details by WhatsApp; the Reel comes back ready to post, with the caption written.</p>
      <p class="price">Suggested: £79 a month for four, one a week, cancel any time. Not set until you decide.</p>
    </div>
  </section>"""
    page = f"""<title>Walk-in Reels</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=Atkinson+Hyperlegible:wght@400;700&family=IBM+Plex+Mono:wght@500&display=swap">
<style>
/* One column you can thumb through on a doorstep: the visit script on a ticket, then each town's shops in walking order. */
:root {{
  --bg: #EDF0EE; --card: #FFFFFF; --paper: #F7F4EC; --ink: #17191C; --ink2: #4C5258; --line: #D3D9D6;
  --green: #1E7445; --green-soft: #DDEFE3; --red: #B5372A; --on-ink: #FFFFFF;
  --display: "Anton", "Arial Narrow", Impact, sans-serif;
  --body: "Atkinson Hyperlegible", system-ui, -apple-system, "Segoe UI", sans-serif;
  --mono: "IBM Plex Mono", ui-monospace, Menlo, Consolas, monospace;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
  --bg: #121518; --card: #1A1E22; --paper: #23282C; --ink: #E8ECEE; --ink2: #A7AFB6; --line: #2E353B;
  --green: #5CC98C; --green-soft: #15291E; --red: #FF8273; --on-ink: #121518; color-scheme: dark; }} }}
:root[data-theme="dark"] {{
  --bg: #121518; --card: #1A1E22; --paper: #23282C; --ink: #E8ECEE; --ink2: #A7AFB6; --line: #2E353B;
  --green: #5CC98C; --green-soft: #15291E; --red: #FF8273; --on-ink: #121518; color-scheme: dark; }}
body {{ background: var(--bg); color: var(--ink); font: 16px/1.5 var(--body); margin: 0; }}
.wrap {{ max-width: 760px; margin: 0 auto; padding-inline: 16px; padding-block: 18px 40px; display: grid; gap: 18px; }}
.wrap > *, .list > * {{ min-width: 0; }}
h1 {{ font-family: var(--display); font-weight: 400; font-size: clamp(42px, 11vw, 72px); line-height: .9; margin: 0;
     text-transform: uppercase; letter-spacing: .01em; text-wrap: balance; }}
h1 span {{ color: var(--green); }}
.lede {{ margin: 0; color: var(--ink2); max-width: 60ch; }}
nav.towns {{ position: sticky; top: env(safe-area-inset-top, 0px); z-index: 5; background: var(--bg); display: flex; gap: 8px;
            overflow-x: auto; padding-block: 8px; border-bottom: 1px solid var(--line); scrollbar-width: none; }}
nav.towns a {{ flex: 0 0 auto; text-decoration: none; color: var(--ink); font-weight: 700; font-size: 15px; padding: 7px 14px;
              border-radius: 999px; border: 1px solid var(--line); background: var(--card); }}
nav.towns b {{ font-family: var(--mono); font-weight: 500; color: var(--green); margin-left: 4px; }}
.me {{ display: flex; gap: 10px; align-items: center; flex-wrap: wrap; font-size: 15px; }}
.me input {{ font: inherit; color: var(--ink); background: var(--card); border: 1px solid var(--line); border-radius: 8px;
            padding: 8px 10px; min-height: 40px; width: 12em; max-width: 100%; }}
.ticket {{ background: var(--paper); border: 1px dashed var(--line); border-radius: 4px; padding: 14px 16px;
          font-family: var(--mono); font-size: 14px; display: grid; gap: 10px; }}
.ticket h2 {{ font-family: var(--mono); font-size: 13px; letter-spacing: .12em; text-transform: uppercase; margin: 0; color: var(--ink2); }}
.ticket ol, .ticket ul {{ margin: 0; padding-left: 1.4em; display: grid; gap: 8px; }}
.ticket q {{ font-family: var(--body); font-size: 15.5px; }}
.price {{ color: var(--red); }}
details.ticket summary {{ cursor: pointer; font-family: var(--mono); font-size: 13px; letter-spacing: .12em; text-transform: uppercase;
                         color: var(--ink2); }}
details.ticket dl {{ margin: 0; display: grid; gap: 10px; }}
details.ticket dt {{ font-family: var(--body); font-weight: 700; font-size: 15px; }}
details.ticket dd {{ margin: 2px 0 0; font-family: var(--body); font-size: 15px; color: var(--ink2); }}
.town {{ display: grid; gap: 12px; scroll-margin-top: 64px; }}
.town h2, .sample h2 {{ font-family: var(--display); font-weight: 400; text-transform: uppercase; margin: 0; line-height: 1; }}
.town h2 {{ font-size: clamp(30px, 8vw, 44px); }}
.list {{ display: grid; gap: 14px; }}
.shop, .sample {{ background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: 12px;
        display: grid; grid-template-columns: minmax(0, 9fr) minmax(0, 11fr); gap: 14px; align-items: start; }}
.shop video, .sample video {{ width: 100%; aspect-ratio: 9 / 16; max-width: 100%; border-radius: 8px; background: #0F1215; display: block; }}
.sample h2 {{ font-size: clamp(24px, 6vw, 32px); }}
.sample p {{ margin: 0; font-size: 15px; }}
.info {{ display: grid; gap: 8px; min-width: 0; }}
.stub {{ margin: 0; font-family: var(--mono); font-size: 12px; letter-spacing: .08em; text-transform: uppercase; color: var(--ink2); }}
.shop h3 {{ font-family: var(--display); font-weight: 400; font-size: clamp(24px, 6vw, 34px); line-height: 1; margin: 0;
           text-transform: uppercase; text-wrap: balance; overflow-wrap: anywhere; }}
.addr {{ margin: 0; font-size: 14.5px; color: var(--ink2); }}
.chip {{ margin: 0; justify-self: start; font-family: var(--mono); font-size: 12px; padding: 3px 9px; border-radius: 999px;
        background: var(--green-soft); color: var(--green); }}
.acts {{ display: flex; flex-wrap: wrap; gap: 8px; }}
button {{ font: inherit; font-weight: 700; font-size: 14.5px; min-height: 42px; padding: 8px 14px; border-radius: 8px; cursor: pointer;
         border: 1px solid var(--ink); background: var(--ink); color: var(--on-ink); }}
button.ghost {{ background: transparent; color: var(--ink); border-color: var(--line); }}
button:disabled {{ opacity: .6; cursor: progress; }}
button:focus-visible, input:focus-visible, a:focus-visible, summary:focus-visible {{ outline: 2px solid var(--green); outline-offset: 2px; }}
.msg {{ display: none; }}
.done {{ font-size: 14px; color: var(--ink2); display: flex; gap: 8px; align-items: center; }}
.done input {{ width: 20px; height: 20px; accent-color: var(--green); }}
.shop.is-done {{ opacity: .55; }}
.note {{ margin: 0; font-size: 13.5px; color: var(--ink2); min-height: 1.2em; }}
footer {{ font-size: 13.5px; color: var(--ink2); display: grid; gap: 6px; }}
footer p {{ margin: 0; max-width: 64ch; }}
a {{ color: var(--green); text-underline-offset: 3px; }}
@media (max-width: 380px) {{ .shop, .sample {{ grid-template-columns: 1fr; }} .shop video, .sample video {{ max-width: 260px; }} }}
@media (prefers-reduced-motion: reduce) {{ * {{ scroll-behavior: auto; }} }}
</style>
<div class="wrap">
  <header>
    <h1>Walk-in <span>Reels</span></h1>
  </header>
  <p class="lede">{n} takeaways and cafés rated 5 for food hygiene, town by town in walking order. Each one has an
    8-second Reel made from its own public record: its name, its rating and its street. You walk in with something
    already made for them.</p>
  <nav class="towns" aria-label="Towns">{nav}</nav>
  <div class="me"><label for="me">Your first name, for the messages</label><input id="me" autocomplete="given-name" placeholder="e.g. Sam"></div>
  <section class="ticket" aria-labelledby="how">
    <h2 id="how">The visit, about two minutes</h2>
    <ol>
      <li>Show it. <q>Hi, I make short videos for food places round here. I made this one for you from your hygiene rating. It's eight seconds.</q> Play it with the sound on.</li>
      <li>Give it. <q>It's yours, free. Shall I send it to you?</q> Tap Save, then share it from Photos by WhatsApp or AirDrop. Copy the message to go with it.</li>
      <li>Offer. <q>If you like it, I can make four a month like this with your own dishes, your specials and your Christmas menu.</q>
        <span class="price">Price not set yet: you decide (suggested £79 a month, cancel any time).</span></li>
      <li>Log it in the <a href="{TRACKER}">Takeaway Round tracker</a>: visited, pitched, later or sold.</li>
    </ol>
  </section>
  <details class="ticket">
    <summary>If they say…</summary>
    <dl>
      <div><dt>"How much?"</dt><dd>Say the monthly price once you've set it, then: "The first one's free whatever you decide."</dd></div>
      <div><dt>"I don't really do social media."</dt><dd>"Most of your customers do. I send them ready to post, so it's ten seconds a week. It works on your WhatsApp status too."</dd></div>
      <div><dt>"My son (or nephew) does our Instagram."</dt><dd>"Great, send it to him. If he'd like four a month done for him, he's got my number."</dd></div>
      <div><dt>"Is that real? How did you make it?"</dt><dd>"From your food hygiene rating. It's public on the Food Standards Agency site. I only make them for places rated 5."</dd></div>
      <div><dt>"Leave me your number."</dt><dd>Send the Reel and the message now, so your number arrives with it. Mark them "later" and drop back in three or four days.</dd></div>
      <div><dt>"Not interested."</dt><dd>"No problem, keep the video anyway." Say thanks and go. Mark them "visited".</dd></div>
    </dl>
  </details>
  <section class="ticket" aria-labelledby="before">
    <h2 id="before">Before you go</h2>
    <ul>
      <li>Save the next three or four Reels to Photos first: signal inside shops is often poor.</li>
      <li>Volume up. The stamp and the bell sell it.</li>
      <li>Check the hygiene sticker in the window matches the Reel before you play it.</li>
      <li>Cafés are best mid-afternoon. Takeaways that open at 4 or 5 are best just after opening, before the first rush.</li>
    </ul>
  </section>{monthly}{sections}
  <footer>
    <p>Ratings come from the Food Standards Agency register (pulled September 2026, Open Government Licence).</p>
    <p>These Reels are for the owners to post. Don't post them on our own accounts.</p>
  </footer>
</div>
<script>
const dlp = (window.claude && window.claude.use) ? window.claude.use("downloads") : Promise.resolve(null);
const say = (el, s) => {{ if (el) el.textContent = s; }};
const me = document.getElementById("me");
try {{ me.value = localStorage.getItem("wr-me") || ""; }} catch (e) {{}}
me.addEventListener("input", () => {{ try {{ localStorage.setItem("wr-me", me.value.trim()); }} catch (e) {{}} }});
const text = id => document.getElementById("m" + id).dataset.tpl.replace("{{me}}", me.value.trim() || "me");
document.addEventListener("click", async ev => {{
  const b = ev.target.closest("button"); if (!b) return;
  const out = b.closest(".shop")?.querySelector(".note");
  if (b.dataset.copy) {{
    const s = text(b.dataset.copy);
    try {{ await navigator.clipboard.writeText(s); const t = b.textContent; b.textContent = "Copied"; setTimeout(() => b.textContent = t, 1400); }}
    catch (e) {{ say(out, s); }}
    return;
  }}
  if (b.dataset.save) {{
    b.disabled = true; say(out, "Fetching the video...");
    try {{
      const d = await dlp;
      if (!d) {{ say(out, "Saving works in the Claude app or on claude.ai."); b.disabled = false; return; }}
      const r = await fetch(b.dataset.save); if (!r.ok) throw new Error(r.status);
      await d.save({{ filename: b.dataset.name, data: await r.blob() }}); say(out, "Saved: " + b.dataset.name);
    }} catch (e) {{ say(out, e && e.code === "declined" ? "Not saved." : "Couldn't save. Tap again to retry."); }}
    b.disabled = false;
  }}
}});
document.querySelectorAll(".done input").forEach(c => {{
  const shop = c.closest(".shop"), key = "wr-v-" + shop.dataset.id;
  try {{ c.checked = localStorage.getItem(key) === "1"; }} catch (e) {{}}
  shop.classList.toggle("is-done", c.checked);
  c.addEventListener("change", () => {{ shop.classList.toggle("is-done", c.checked); try {{ localStorage.setItem(key, c.checked ? "1" : "0"); }} catch (e) {{}} }});
}});
</script>
"""
    open(os.path.join(HERE, "index.html"), "w").write(page)
    return rows, towns, sample


def files_for(rows, keep):
    out = {}
    for r in rows:
        if keep(r):
            for k in ("file", "poster"):
                out[f"reels/{r[k]}"] = os.path.relpath(os.path.join(HERE, "build", "reels", r[k]), os.getcwd())
    return out


if __name__ == "__main__":
    only = sys.argv[sys.argv.index("--towns") + 1].split(",") if "--towns" in sys.argv else None
    rows, towns, sample = build(only)
    print(os.path.join(HERE, "index.html"), sum(r["town"] in towns for r in rows), "Reels in", ", ".join(towns),
          "+ sample" if sample else "")
    if "--files" in sys.argv:
        want = [a for a in sys.argv[sys.argv.index("--files") + 1:] if not a.startswith("--")][:2]
        fs = files_for(rows, lambda r: r["town"] in want)
        print(round(sum(os.path.getsize(p) for p in fs.values()) / 1e6, 1), "MB")
        print(json.dumps(fs))
