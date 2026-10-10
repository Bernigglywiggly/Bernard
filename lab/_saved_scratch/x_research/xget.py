import json, sys, urllib.request, os
OUT = os.path.dirname(os.path.abspath(__file__)) + "/arts"
def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return json.load(urllib.request.urlopen(req, timeout=30))
def article_text(a):
    c = a.get("content") or {}
    ents = c.get("entityMap") or {}
    if isinstance(ents, list):
        ents = {str(i): e for i, e in enumerate(ents)}
    out = [f"# {a.get('title')}"]
    for b in c.get("blocks", []):
        t, ty = b.get("text", ""), b.get("type")
        if ty == "atomic":
            for r in b.get("entityRanges", []):
                e = ents.get(str(r.get("key")), {})
                e = e.get("value", e)
                d = e.get("data", {})
                if "markdown" in d: out.append(d["markdown"])
                elif d.get("mediaItems") or d.get("caption"): out.append(f"[media {d.get('caption','')}]")
                elif e.get("type") == "TWEET" or "tweetId" in d: out.append(f"[embedded tweet {d.get('tweetId')}]")
                elif d: out.append(f"[{e.get('type')}: {json.dumps(d)[:300]}]")
            continue
        pre = {"header-one": "# ", "header-two": "## ", "header-three": "### ", "unordered-list-item": "- ",
               "ordered-list-item": "1. ", "blockquote": "> ", "code-block": "    "}.get(ty, "")
        out.append(pre + t)
    return "\n".join(out)
for arg in sys.argv[1:]:
    user, sid = arg.split("/")
    d = get(f"https://api.fxtwitter.com/{user}/status/{sid}")
    t = d.get("tweet") or {}
    parts = [f"=== @{user} {t.get('created_at')} likes={t.get('likes')} views={t.get('views')} https://x.com/{user}/status/{sid}", t.get("text") or ""]
    try:
        th = get(f"https://api.fxtwitter.com/2/thread/{sid}")
        for x in (th.get("thread") or [])[1:]:
            parts.append("--- " + (x.get("text") or ""))
    except Exception as e:
        parts.append(f"[thread fetch failed {e}]")
    if t.get("article"):
        parts.append(article_text(t["article"]))
    txt = "\n".join(parts)
    open(f"{OUT}/{user}_{sid}.md", "w").write(txt)
    print(f"{user}/{sid}: {len(txt.split())} words")
