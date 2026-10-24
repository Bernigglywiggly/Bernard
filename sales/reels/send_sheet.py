#!/usr/bin/env python3
"""Send sheet for the walk-in Reels: one row per shop with its best public contact channel (contacts.csv), a
first-touch message to copy, and the Reel file to attach. Open sales/reels/send_sheet.html on the Mac; the Reel links
point at build/reels/, so render first. Nothing is sent from here: the user sends each message by hand.

    python3 sales/reels/send_sheet.py            # -> sales/reels/send_sheet.html
"""
import csv
import html
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
TOWNS = ["Stone", "Newcastle-under-Lyme", "Tamworth"]
# First touch: the gift only, no price. {me} is filled in the page from the name box.
MESSAGE = ("Hi, I'm {me}, I'm local and I make short videos for food places. I made this one for {shop} after "
           "seeing your 5 hygiene rating. It's yours to post, no catch. If you'd like more like it, just reply.")
CHANNELS = [("facebook", "Facebook"), ("instagram", "Instagram"), ("email", "Email"), ("phone", "Phone")]


def slug(s):
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")[:32]


def rows():
    shops = {s["id"]: s for s in json.load(open(os.path.join(REPO, "sales", "prospects_routed.json")))}
    out = []
    for c in csv.DictReader(open(os.path.join(HERE, "contacts.csv"))):
        s = shops[c["id"]]
        base = f"{s['town'][:3].lower()}{s['order']:02d}_{slug(s['name'])}"
        best = next((k for k, _ in CHANNELS if c[k].strip()), "")
        out.append(dict(c, order=s["order"], file=base + ".mp4", best=best,
                        rendered=os.path.exists(os.path.join(HERE, "build", "reels", base + ".mp4"))))
    seen = {}
    for r in sorted(out, key=lambda r: r["order"]):     # neighbours get the same design, so never in one batch
        k = (r["town"], street_of(shops[r["id"]]["address"]))
        seen[k] = r["batch"] = seen.get(k, 0) + 1
    out.sort(key=lambda r: (TOWNS.index(r["town"]), r["batch"], r["order"]))
    return out


def street_of(address):
    parts = [p.strip() for p in address.split(",")]
    road = next((p for p in parts if re.search(r"\b(street|road|lane|way|avenue|square|row|place|parade|walk|drive|close|gate|bank|dam)\b", p, re.I)), parts[0])
    return re.sub(r"[^a-z ]", "", road.lower()).strip()


def link(r, key):
    v = r[key].strip()
    if not v:
        return ""
    href = {"email": "mailto:" + v, "phone": "tel:" + v.replace(" ", "")}.get(key, v)
    label = dict(CHANNELS)[key] + (": " + v if key in ("email", "phone") else "")
    cls = "ch best" if key == r["best"] else "ch"
    return f'<a class="{cls}" href="{html.escape(href)}" target="_blank" rel="noopener">{html.escape(label)}</a>'


def card(r):
    e = html.escape
    reel = (f'<a class="reel" href="build/reels/{e(r["file"])}" target="_blank">{e(r["file"])}</a>' if r["rendered"]
            else f'<span class="reel missing">{e(r["file"])} (not rendered yet)</span>')
    note = f'<p class="note">{e(r["note"])}</p>' if r["note"].strip() else ""
    remote = "0" if r["best"] in ("", "phone") else "1"
    return f'''<article class="shop" data-id="{e(r["id"])}" data-town="{e(r["town"])}" data-remote="{remote}">
<header><label><input type="checkbox" class="sent"> <b>{e(r["name"])}</b></label>
<span class="meta">Batch {r["batch"]} · {e(r["town"])} · #{r["order"]} · {e(r["confidence"])} confidence</span></header>
<div class="chs">{"".join(link(r, k) for k, _ in CHANNELS) or '<span class="ch none">no channel found</span>'}</div>
<p class="msg" data-shop="{e(r["name"])}"></p>
<div class="act"><button class="copy">Copy message</button>{reel}</div>{note}
<input class="reply" placeholder="Reply / notes"></article>'''


PAGE = '''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Reel Send Sheet</title>
<style>
:root{--bg:#F6F4EF;--card:#fff;--ink:#1C1D20;--ink2:#5A5E64;--line:#DDD8CC;--acc:#1E7445;--warn:#8A5A00;--warnbg:#FFF4D6}
@media (prefers-color-scheme:dark){:root{--bg:#15171A;--card:#1E2125;--ink:#E9EBEE;--ink2:#A3A8AF;--line:#33373D;--acc:#4CC38A;--warn:#F0C36A;--warnbg:#3A2F12}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 system-ui,sans-serif}
main{max-width:860px;margin:0 auto;padding:16px}h1{font-size:22px;margin:8px 0}
.bar{position:sticky;top:0;background:var(--bg);padding:10px 0;border-bottom:1px solid var(--line);display:flex;gap:10px;flex-wrap:wrap;align-items:center;z-index:2}
.bar input[type=text]{padding:8px 10px;border:1px solid var(--line);border-radius:8px;background:var(--card);color:var(--ink);font:inherit;width:150px}
.bar button,.copy{padding:8px 12px;border:1px solid var(--line);border-radius:8px;background:var(--card);color:var(--ink);font:inherit;cursor:pointer}
.bar button.on{background:var(--acc);color:#fff;border-color:var(--acc)}#count{margin-left:auto;font-weight:600}
.shop{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px;margin:12px 0}
.shop.done{opacity:.5}.shop header{display:flex;justify-content:space-between;gap:8px;flex-wrap:wrap}
.meta{color:var(--ink2);font-size:13px}.chs{display:flex;gap:8px;flex-wrap:wrap;margin:8px 0}
.ch{font-size:14px;padding:4px 10px;border:1px solid var(--line);border-radius:999px;color:var(--ink);text-decoration:none}
.ch.best{border-color:var(--acc);color:var(--acc);font-weight:600}.ch.none{color:var(--warn)}
.msg{margin:8px 0;padding:10px;border-left:3px solid var(--line);color:var(--ink2);font-size:15px}
.act{display:flex;gap:12px;align-items:center;flex-wrap:wrap}.reel{font:13px ui-monospace,monospace;color:var(--acc);word-break:break-all}
.reel.missing{color:var(--warn)}.note{background:var(--warnbg);color:var(--warn);font-size:13px;padding:8px 10px;border-radius:8px;margin:10px 0 0}
.reply{width:100%;margin-top:10px;padding:8px 10px;border:1px solid var(--line);border-radius:8px;background:transparent;color:var(--ink);font:inherit}
h2{font-size:17px;margin:22px 0 0}
</style></head><body><main>
<h1>Reel send sheet</h1>
<div class="bar"><input type="text" id="me" placeholder="Your first name">
<button data-f="all" class="on">All</button><button data-f="remote">Can message</button><button data-f="todo">Not sent</button>
<span id="count"></span></div>
__BODY__
</main><script>
const MSG=__MSG__;
const store={get(k){try{return JSON.parse(localStorage.getItem(k))}catch(e){return null}},set(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}}};
const state=store.get("reel_send")||{};const me=document.getElementById("me");me.value=store.get("reel_me")||"";
function fill(){document.querySelectorAll(".msg").forEach(p=>{p.textContent=MSG.replace("{me}",me.value.trim()||"[your name]").replace("{shop}",p.dataset.shop)})}
function count(){const all=[...document.querySelectorAll(".shop")];const n=all.filter(a=>a.querySelector(".sent").checked).length;document.getElementById("count").textContent=n+" / "+all.length+" sent"}
me.addEventListener("input",()=>{store.set("reel_me",me.value);fill()});
document.querySelectorAll(".shop").forEach(a=>{const s=state[a.dataset.id]||{};const cb=a.querySelector(".sent"),rp=a.querySelector(".reply");
cb.checked=!!s.sent;rp.value=s.reply||"";a.classList.toggle("done",cb.checked);
const save=()=>{state[a.dataset.id]={sent:cb.checked,reply:rp.value};store.set("reel_send",state);a.classList.toggle("done",cb.checked);count()};
cb.addEventListener("change",save);rp.addEventListener("input",save);
a.querySelector(".copy").addEventListener("click",ev=>{const t=a.querySelector(".msg").textContent;const b=ev.target;
(navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(()=>{b.textContent="Copied"},()=>{b.textContent="Select the text and copy"});setTimeout(()=>{b.textContent="Copy message"},1500)})});
document.querySelectorAll(".bar button").forEach(b=>b.addEventListener("click",()=>{document.querySelectorAll(".bar button").forEach(x=>x.classList.toggle("on",x===b));const f=b.dataset.f;
document.querySelectorAll(".shop").forEach(a=>{const show=f==="all"||(f==="remote"&&a.dataset.remote==="1")||(f==="todo"&&!a.querySelector(".sent").checked);a.style.display=show?"":"none"})}));
fill();count();
</script></body></html>'''


def main():
    rs = rows()
    body = []
    for t in TOWNS:
        sel = [r for r in rs if r["town"] == t]
        body.append(f'<h2>{html.escape(t)} ({len(sel)})</h2>' + "".join(card(r) for r in sel))
    out = os.path.join(HERE, "send_sheet.html")
    open(out, "w").write(PAGE.replace("__BODY__", "\n".join(body)).replace("__MSG__", json.dumps(MESSAGE)))
    remote = sum(r["best"] in ("facebook", "instagram", "email") for r in rs)
    print(f"{out}: {len(rs)} shops, {remote} messageable, {sum(r['rendered'] for r in rs)} Reels rendered")


if __name__ == "__main__":
    main()
