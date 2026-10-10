import json, html, re, datetime, os
os.chdir('/home/user/Bernard')
OUT = '/tmp/claude-0/-home-user-Bernard/d77e81c6-c1a0-5f1c-94ca-c50fd63a0957/scratchpad/tq'
p = json.load(open('channel/uploads.json'))
IDX = [0,1,3,4,6,7,9,10,11,12,13,16,17,18,19,20,21,23,24,25,26,27,28,31,32,33,34]
ACC = {"curve": ("The Curve", "was issolaurent", "c"), "crimes": ("Money Crimes", "new account", "m"),
       "profit": ("How They Profit", "was archivepearls", "p")}
ORDER = {"profit": 0, "curve": 1, "crimes": 2}
e = html.escape
def caption(d):
    d = d.replace("(linked)", "on YouTube")
    return d.strip()
days = {}
for i in IDX:
    x = p[i]
    t = datetime.datetime.fromisoformat(x["publish_at"].replace("Z", "+00:00"))
    day = t.date()
    late = t.hour >= 17
    days.setdefault(day, []).append((ORDER[x["channel"]] + (5 if late else 0), i, x, "21:00" if late else "18:00"))
cards = []
for day in sorted(days):
    rows = []
    for _, i, x, tm in sorted(days[day]):
        name, was, k = ACC[x["channel"]]
        cap = caption(x["description"])
        fn = f"{i:02d}.mp4"
        save = re.sub(r"[^a-z0-9]+", "_", x["title"].lower()).strip("_")[:40] + ".mp4"
        rows.append(f'''<article class="post" data-id="{i}">
  <video controls playsinline preload="metadata" src="media/{fn}#t=1.5"></video>
  <div class="info">
    <p class="who"><span class="chip {k}">{e(name)}</span><span class="was">{e(was)}</span><span class="time">{tm} UK</span></p>
    <h3>{e(x["title"])}</h3>
    <textarea id="cap{i}" readonly rows="5">{e(cap)}</textarea>
    <div class="acts">
      <button class="btn primary" type="button" data-save="media/{fn}" data-name="{e(save)}">Save video</button>
      <button class="btn" type="button" data-copy="cap{i}">Copy caption</button>
      <label class="done"><input type="checkbox" id="done{i}"> Scheduled</label>
    </div>
    <p class="note" aria-live="polite"></p>
  </div>
</article>''')
    cards.append(f'<section class="day"><h2>{day:%a %-d %b}</h2><div class="posts">{"".join(rows)}</div></section>')
page = open(f"{OUT}/shell.html").read().replace("%%DAYS%%", "\n".join(cards)).replace("%%N%%", str(len(IDX)))
open(f"{OUT}/index.html", "w").write(page)
print(len(IDX), "posts")
