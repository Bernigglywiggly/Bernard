"""ElevenLabs text-to-speech for our scripts: George (the "first British guy" from A01) by default, at his own speed (1.0).

Every line is cached by (text, voice, model, speed) as lossless FLAC plus the character timings, in
lab/voice/cache/eleven/. So credits are only spent once per line, and the cache can be made on any machine that
can reach ElevenLabs (the Mac session, or this cloud session once the key and domain are allowed) and pushed to
the repo for the others to build from.

    ELEVENLABS_API_KEY=... python3 tools/eleven_tts.py ep03              # every line of lab/ep03/script.py
    python3 tools/eleven_tts.py ep03 --dry-run                         # what it would send, and what's cached
    python3 tools/eleven_tts.py ep03 --speed 1.0 --voice JBFqnCBsd6RMkjVDRZzb

voice_build.py uses the cache automatically when it has every line (VOICE_ENGINE=eleven forces it).
"""
import argparse
import base64
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request

import numpy as np
import soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.join(HERE, "..")
CACHE = os.path.join(LAB, "voice", "cache", "eleven")
API = "https://api.elevenlabs.io/v1"
GEORGE = "JBFqnCBsd6RMkjVDRZzb"           # ElevenLabs' premade "George": warm British storyteller
MODEL = "eleven_multilingual_v2"
SETTINGS = dict(stability=0.42, similarity_boost=0.8, style=0.18, use_speaker_boost=True)
FORMATS = ("pcm_44100", "mp3_44100_192", "mp3_44100_128")   # best first; the API refuses what the plan can't use


def key_of(text, voice, model, speed):
    return hashlib.sha1(json.dumps([text, voice, model, round(speed, 3), SETTINGS], sort_keys=True).encode()).hexdigest()[:16]


def cached(text, voice=GEORGE, model=MODEL, speed=1.0):
    """(audio float32 mono at 44.1 kHz or None, alignment dict or None)."""
    k = key_of(text, voice, model, speed)
    fl, js = os.path.join(CACHE, k + ".flac"), os.path.join(CACHE, k + ".json")
    if os.path.exists(fl):
        y, sr = sf.read(fl, dtype="float32")
        meta = json.load(open(js)) if os.path.exists(js) else {}
        return (y, sr), meta.get("alignment")
    return None, None


def _post(url, body, key):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST",
                                 headers={"xi-api-key": key, "Content-Type": "application/json", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.loads(r.read())


def synth(text, key, voice=GEORGE, model=MODEL, speed=1.0, prev=None, nxt=None):
    """Calls the API (with timestamps) and caches the result. Returns ((audio, sr), alignment)."""
    hit = cached(text, voice, model, speed)
    if hit[0] is not None:
        return hit
    body = dict(text=text, model_id=model, voice_settings=dict(SETTINGS, speed=speed))
    if prev:
        body["previous_text"] = prev          # keeps the delivery continuous across lines
    if nxt:
        body["next_text"] = nxt
    last = None
    for fmt in FORMATS:
        try:
            d = _post(f"{API}/text-to-speech/{voice}/with-timestamps?output_format={fmt}", body, key)
            break
        except urllib.error.HTTPError as e:
            last = f"{e.code} {e.read()[:300]!r}"
            if e.code in (401, 404):
                raise SystemExit(f"ElevenLabs refused the request ({last}). Check the key and the voice id.")
            continue
    else:
        raise SystemExit(f"ElevenLabs refused every output format: {last}")
    raw = base64.b64decode(d["audio_base64"])
    if fmt.startswith("pcm_"):
        sr = int(fmt.split("_")[1])
        y = np.frombuffer(raw, "<i2").astype(np.float32) / 32768.0
    else:
        p = subprocess.run(["ffmpeg", "-v", "error", "-i", "pipe:0", "-ac", "1", "-ar", "44100", "-f", "f32le", "-"],
                           input=raw, capture_output=True, check=True)
        y, sr = np.frombuffer(p.stdout, np.float32), 44100
    os.makedirs(CACHE, exist_ok=True)
    k = key_of(text, voice, model, speed)
    sf.write(os.path.join(CACHE, k + ".flac"), y, sr, subtype="PCM_24")
    json.dump(dict(text=text, voice=voice, model=model, speed=speed, format=fmt, alignment=d.get("alignment")),
              open(os.path.join(CACHE, k + ".json"), "w"))
    return (y, sr), d.get("alignment")


def words_from_alignment(al, text):
    """Character timings -> [(word, start, end)] for exact caption highlighting."""
    if not al:
        return None
    chars, st, en = al.get("characters", []), al.get("character_start_times_seconds", []), al.get("character_end_times_seconds", [])
    out, cur, t0 = [], "", None
    for ch_, a, b in zip(chars, st, en):
        if ch_.isspace():
            if cur:
                out.append((cur, t0, last_end)); cur = ""
            continue
        if not cur:
            t0 = a
        cur += ch_; last_end = b
    if cur:
        out.append((cur, t0, last_end))
    return out


def script_lines(ep):
    spec = importlib.util.spec_from_file_location("script", os.path.join(LAB, ep, "script.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.LINES


def spoken(ln, slots):
    if ln.get("slot") and (slots.get(ln["slot"]) or "").strip():
        return slots[ln["slot"]].strip()
    return ln.get("say", ln["text"])


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("ep")
    ap.add_argument("--voice", default=GEORGE)
    ap.add_argument("--model", default=MODEL)
    ap.add_argument("--speed", type=float, default=1.0)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    slots_p = os.path.join(LAB, a.ep, "build", "slots.json")
    slots = json.load(open(slots_p)) if os.path.exists(slots_p) else {}
    L = script_lines(a.ep)
    texts = [spoken(x, slots) for x in L]
    todo = [t for t in texts if cached(t, a.voice, a.model, a.speed)[0] is None]
    print(f"{a.ep}: {len(texts)} lines, {len(texts) - len(todo)} cached, {len(todo)} to make, "
          f"{sum(len(t) for t in todo)} characters of credit")
    if a.dry_run or not todo:
        sys.exit(0)
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        raise SystemExit("No ELEVENLABS_API_KEY in the environment.")
    for i, t in enumerate(texts):
        (y, sr), al = synth(t, key, a.voice, a.model, a.speed,
                            prev=texts[i - 1] if i else None, nxt=texts[i + 1] if i + 1 < len(texts) else None)
        print(f"{i:2d} {len(y) / sr:5.2f}s {t[:70]}")
