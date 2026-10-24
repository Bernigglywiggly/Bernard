import glob, json, os, sys
from faster_whisper import WhisperModel
T = "/Users/daestigwood/Bernard/lab/maps/hormuz_es/flow/takes"
O = "/Users/daestigwood/Bernard/lab/maps/hormuz_es/out/critic/transcripts.jsonl"
m = WhisperModel("medium", device="cpu", compute_type="int8")
done = set()
if os.path.exists(O):
    for l in open(O): done.add(json.loads(l)["id"])
with open(O, "a") as f:
    for d in sorted(os.listdir(T)):
        if d in done: continue
        mp3 = glob.glob(f"{T}/{d}/*.mp3")[0]
        segs, info = m.transcribe(mp3, language="es", beam_size=5, word_timestamps=True, vad_filter=False)
        segs = list(segs)
        text = " ".join(s.text.strip() for s in segs)
        words = [[w.word, round(w.start,2), round(w.end,2), round(w.probability,2)] for s in segs for w in s.words]
        f.write(json.dumps({"id": d, "file": mp3, "dur": info.duration, "text": text, "words": words}, ensure_ascii=False) + "\n"); f.flush()
        print(d, text, flush=True)
