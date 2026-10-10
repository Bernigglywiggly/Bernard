"""AI pictures for a Curve long-form film (3 Oct 2026). A film's `shots.py` lists STILLS [(id, prompt)] and CLIPS
{clip id: (still id, motion)}. The stills are made to be turned into characters (engine.look): one bright subject on
pure black, hard rim light, nothing in the background. GPT Image 2.5 (medium, 1 credit), Kling 3.0 Pro for clips.

    python3 ../assets.py <film> stills N      # request JSON for batch N (12 a batch) -> generate_image_batch
    python3 ../assets.py <film> clips         # request JSON for the clips whose start still has finished
    python3 ../assets.py <film> track '<batch response JSON>'   # record job ids (src/jobs.json)
    python3 ../assets.py <film> fetch '<jobs_wait JSON>'        # download finished jobs -> src/ai/<id>.png|mp4
    python3 ../assets.py <film> todo          # what still needs submitting or fetching
"""
import importlib.util
import json
import os
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
STYLE = (". High-contrast cinematic photograph: the subject brightly lit by hard white rim light against a pure black "
         "background, deep black shadows, no background detail, crisp edges, monochrome, no text, no logos.")


def shots(film_dir):
    s = importlib.util.spec_from_file_location("shots", os.path.join(film_dir, "shots.py"))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def _jobs(film_dir):
    p = os.path.join(film_dir, "src", "jobs.json")
    return p, (json.load(open(p)) if os.path.exists(p) else {})


def stills_batch(film_dir, i, size=12):
    m = shots(film_dir)
    _, jobs = _jobs(film_dir)
    todo = [s for s in m.STILLS if s[0] not in jobs]
    reqs = []
    for k, (sid, prompt) in enumerate(todo[i * size:(i + 1) * size]):
        idx = [s[0] for s in m.STILLS].index(sid)
        reqs.append(dict(index=idx, params=dict(model="gpt_image_2_5", prompt=prompt + STYLE, aspect_ratio="16:9",
                                                resolution="2k", quality="medium")))
    return reqs


def clips_batch(film_dir):
    m = shots(film_dir)
    _, jobs = _jobs(film_dir)
    reqs = []
    for k, (cid, (sid, motion)) in enumerate(m.CLIPS.items()):
        if cid in jobs or sid not in jobs or not os.path.exists(os.path.join(film_dir, "src", "ai", sid + ".png")):
            continue
        reqs.append(dict(index=100 + k, params=dict(
            model="kling3_0", prompt=motion + " Slow, smooth camera motion, cinematic, no cuts.", duration=5, mode="pro",
            sound="off", aspect_ratio="16:9", declined_preset_id="24bae836-2c4a-48e0-89b6-49fcc0b21612",
            medias=[dict(value=jobs[sid], role="start_image")])))
    return reqs


def track(film_dir, resp):
    m = shots(film_dir)
    p, jobs = _jobs(film_dir)
    clips = list(m.CLIPS)
    for x in resp.get("jobs", resp if isinstance(resp, list) else []):
        if x.get("job_id"):
            k = m.STILLS[x["index"]][0] if x["index"] < 100 else clips[x["index"] - 100]
            jobs[k] = x["job_id"]
    os.makedirs(os.path.dirname(p), exist_ok=True)
    json.dump(jobs, open(p, "w"), indent=1)
    return jobs


def fetch(film_dir, resp):
    p, jobs = _jobs(film_dir)
    rev = {v: k for k, v in jobs.items()}
    ap = os.path.join(film_dir, "assets_ai.json")
    urls = json.load(open(ap)) if os.path.exists(ap) else {}
    os.makedirs(os.path.join(film_dir, "src", "ai"), exist_ok=True)
    for x in resp["jobs"]:
        k = rev.get(x["job_id"])
        if not k:
            continue
        if x["status"] == "completed":
            dest = os.path.join(film_dir, "src", "ai", k + os.path.splitext(x["result_url"].split("?")[0])[1])
            if not os.path.exists(dest):
                open(dest, "wb").write(urllib.request.urlopen(x["result_url"], timeout=180).read())
            urls[k] = x["result_url"]
        elif x["status"] in ("failed", "nsfw", "canceled", "cancelled"):
            jobs.pop(k, None)
            print("FAILED", k, x["status"])
    json.dump(jobs, open(p, "w"), indent=1)
    json.dump(dict(sorted(urls.items())), open(ap, "w"), indent=1)


def refetch(film_dir):
    """A fresh checkout: download every recorded result again (assets_ai.json keeps the picture URLs, assets_vo.json the
    narration takes), and rebuild archive pictures from src/arch (shots.ARCH_FILES)."""
    ap = os.path.join(film_dir, "assets_ai.json")
    for k, u in (json.load(open(ap)) if os.path.exists(ap) else {}).items():
        dest = os.path.join(film_dir, "src", "ai", k + os.path.splitext(u.split("?")[0])[1])
        if not os.path.exists(dest):
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            open(dest, "wb").write(urllib.request.urlopen(u, timeout=180).read())
    vp = os.path.join(film_dir, "assets_vo.json")
    for rel, u in (json.load(open(vp)) if os.path.exists(vp) else {}).items():
        dest = os.path.join(film_dir, rel)
        if not os.path.exists(dest):
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            open(dest, "wb").write(urllib.request.urlopen(u, timeout=180).read())
    join_halves(film_dir)
    for k, f in getattr(shots(film_dir), "ARCH_FILES", {}).items():
        dest = os.path.join(film_dir, "src", "ai", k + ".png")
        if not os.path.exists(dest):
            import cv2
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            cv2.imwrite(dest, cv2.imread(os.path.join(film_dir, "src", "arch", f)))


def join_halves(film_dir, gap=0.5):
    """A take the voice model kept rejecting, generated in two halves (src/vo_07a.wav + vo_07b.wav): join each pair into
    the take kit.py reads (src/vo_07.wav), with a short pause between."""
    import numpy as np
    import soundfile as sf
    src = os.path.join(film_dir, "src")
    for f in sorted(os.listdir(src)) if os.path.isdir(src) else []:
        if f.startswith("vo_") and f.endswith("a.wav"):
            a, b, out = os.path.join(src, f), os.path.join(src, f[:-5] + "b.wav"), os.path.join(src, f[:-5] + ".wav")
            if os.path.exists(b) and not os.path.exists(out):
                x, sr = sf.read(a)
                y, _ = sf.read(b)
                pad = np.zeros((int(gap * sr),) + x.shape[1:])
                sf.write(out, np.concatenate([x, pad, y]), sr)
                print("joined", os.path.basename(out))


def todo(film_dir):
    m = shots(film_dir)
    _, jobs = _jobs(film_dir)
    have = set(os.path.splitext(f)[0] for f in os.listdir(os.path.join(film_dir, "src", "ai"))) \
        if os.path.isdir(os.path.join(film_dir, "src", "ai")) else set()
    ids = [s[0] for s in m.STILLS] + list(m.CLIPS)
    return dict(unsubmitted=[i for i in ids if i not in jobs], pending=[i for i in ids if i in jobs and i not in have],
                jobs={i: jobs[i] for i in ids if i in jobs and i not in have})


if __name__ == "__main__":
    d = os.path.join(HERE, sys.argv[1])
    cmd = sys.argv[2]
    if cmd == "stills":
        print(json.dumps(stills_batch(d, int(sys.argv[3]))))
    elif cmd == "clips":
        print(json.dumps(clips_batch(d)))
    elif cmd == "track":
        print(len(track(d, json.loads(sys.argv[3]))), "recorded")
    elif cmd == "fetch":
        fetch(d, json.loads(sys.argv[3]))
        print(json.dumps(todo(d)))
    elif cmd == "refetch":
        refetch(d)
    else:
        print(json.dumps(todo(d)))
