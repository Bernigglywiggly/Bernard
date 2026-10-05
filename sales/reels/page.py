#!/usr/bin/env python3
"""Build the Walk-in Reels page (sales/reels/index.html) from build/reels/manifest.json and print the files map.

    python3 sales/reels/page.py [town]      # default Stone
"""
import html
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MONTHS = "January February March April May June July August September October November December".split()
TRACKER = "https://claude.ai/artifact/2f7kucmy3ptWePJ4UPgNUU"


def month(d):
    y, m, _ = d.split("-")
    return f"{MONTHS[int(m) - 1]} {y}"


def card(r):
    e = html.escape
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
    <h2>{e(r['name'])}</h2>
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


def build(town="Stone"):
    rows = [r for r in json.load(open(os.path.join(HERE, "build", "reels", "manifest.json"))) if r["town"] == town]
    cards = "\n".join(card(r) for r in rows)
    page = f"""<title>Walk-in Reels · {town}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=Atkinson+Hyperlegible:wght@400;700&family=IBM+Plex+Mono:wght@500&display=swap">
<style>
/* One column you can thumb through on a doorstep: the visit script on a ticket, then one card per shop in walking order. */
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
h1 {{ font-family: var(--display); font-weight: 400; font-size: clamp(42px, 11vw, 72px); line-height: .9; margin: 0;
     text-transform: uppercase; letter-spacing: .01em; text-wrap: balance; }}
h1 span {{ color: var(--green); }}
.lede {{ margin: 0; color: var(--ink2); max-width: 60ch; }}
.me {{ display: flex; gap: 10px; align-items: center; flex-wrap: wrap; font-size: 15px; }}
.me input {{ font: inherit; color: var(--ink); background: var(--card); border: 1px solid var(--line); border-radius: 8px;
            padding: 8px 10px; min-height: 40px; width: 12em; max-width: 100%; }}
.ticket {{ background: var(--paper); border: 1px dashed var(--line); border-radius: 4px; padding: 14px 16px;
          font-family: var(--mono); font-size: 14px; display: grid; gap: 10px; }}
.ticket h2 {{ font-family: var(--mono); font-size: 13px; letter-spacing: .12em; text-transform: uppercase; margin: 0; color: var(--ink2); }}
.ticket ol {{ margin: 0; padding-left: 1.4em; display: grid; gap: 8px; }}
.ticket q {{ font-family: var(--body); font-size: 15.5px; }}
.ticket .price {{ color: var(--red); }}
.list {{ display: grid; gap: 14px; }}
.wrap > *, .list > * {{ min-width: 0; }}
.shop {{ background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: 12px;
        display: grid; grid-template-columns: minmax(0, 9fr) minmax(0, 11fr); gap: 14px; align-items: start; }}
.shop video {{ width: 100%; aspect-ratio: 9 / 16; max-width: 100%; border-radius: 8px; background: #0F1215; display: block; }}
.info {{ display: grid; gap: 8px; min-width: 0; }}
.stub {{ margin: 0; font-family: var(--mono); font-size: 12px; letter-spacing: .08em; text-transform: uppercase; color: var(--ink2); }}
.shop h2 {{ font-family: var(--display); font-weight: 400; font-size: clamp(24px, 6vw, 34px); line-height: 1; margin: 0;
           text-transform: uppercase; text-wrap: balance; overflow-wrap: anywhere; }}
.addr {{ margin: 0; font-size: 14.5px; color: var(--ink2); }}
.chip {{ margin: 0; justify-self: start; font-family: var(--mono); font-size: 12px; padding: 3px 9px; border-radius: 999px;
        background: var(--green-soft); color: var(--green); }}
.acts {{ display: flex; flex-wrap: wrap; gap: 8px; }}
button {{ font: inherit; font-weight: 700; font-size: 14.5px; min-height: 42px; padding: 8px 14px; border-radius: 8px; cursor: pointer;
         border: 1px solid var(--ink); background: var(--ink); color: var(--on-ink); }}
button.ghost {{ background: transparent; color: var(--ink); border-color: var(--line); }}
button:disabled {{ opacity: .6; cursor: progress; }}
button:focus-visible, input:focus-visible {{ outline: 2px solid var(--green); outline-offset: 2px; }}
.msg {{ display: none; }}
.done {{ font-size: 14px; color: var(--ink2); display: flex; gap: 8px; align-items: center; }}
.done input {{ width: 20px; height: 20px; accent-color: var(--green); }}
.shop.is-done {{ opacity: .55; }}
.note {{ margin: 0; font-size: 13.5px; color: var(--ink2); min-height: 1.2em; }}
footer {{ font-size: 13.5px; color: var(--ink2); display: grid; gap: 6px; }}
footer p {{ margin: 0; max-width: 64ch; }}
a {{ color: var(--green); text-underline-offset: 3px; }}
@media (max-width: 380px) {{ .shop {{ grid-template-columns: 1fr; }} .shop video {{ max-width: 260px; }} }}
@media (prefers-reduced-motion: reduce) {{ * {{ scroll-behavior: auto; }} }}
</style>
<div class="wrap">
  <header>
    <h1>Walk-in Reels · <span>{town}</span></h1>
  </header>
  <p class="lede">{len(rows)} places in {town} rated 5 for food hygiene, in walking order. Each one has an 8-second Reel
    made from its own public record: its name, its rating and its street. You walk in with something already made for them.</p>
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
  <div class="list">{cards}
  </div>
  <footer>
    <p>Ratings come from the Food Standards Agency register (pulled September 2026, Open Government Licence). Check the sticker in their window matches before you play it.</p>
    <p>These Reels are for the owners to post. Don't post them on our own accounts.</p>
  </footer>
</div>
<script>
const dlp = (window.claude && window.claude.use) ? window.claude.use("downloads") : Promise.resolve(null);
const say = (el, s) => {{ if (el) el.textContent = s; }};
const me = document.getElementById("me");
try {{ me.value = localStorage.getItem("wr-me") || ""; }} catch (e) {{}}
me.addEventListener("input", () => {{ try {{ localStorage.setItem("wr-me", me.value.trim()); }} catch (e) {{}} }});
const text = id => {{
  const t = document.getElementById("m" + id).dataset.tpl;
  return t.replace("{{me}}", me.value.trim() || "me");
}};
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
    out = os.path.join(HERE, "index.html")
    open(out, "w").write(page)
    files = {}
    for r in rows:
        files[f"reels/{r['file']}"] = os.path.relpath(os.path.join(HERE, "build", "reels", r["file"]), os.getcwd())
        files[f"reels/{r['poster']}"] = os.path.relpath(os.path.join(HERE, "build", "reels", r["poster"]), os.getcwd())
    total = sum(os.path.getsize(os.path.join(os.getcwd(), p)) for p in files.values()) / 1e6
    print(out, len(rows), "Reels,", round(total, 1), "MB")
    print(json.dumps(files))


if __name__ == "__main__":
    build(*(sys.argv[1:2] or ["Stone"]))
