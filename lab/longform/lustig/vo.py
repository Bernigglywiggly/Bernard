"""The narration track: the thirteen Imogen takes (src/vo_XX.wav) joined into one read, with the long TTS pauses
capped (an ellipsis could leave five seconds of air), a held breath between chapters for the title cards, and every
Whisper word timing carried through. Writes build/voice.wav, build/words.json, build/chapters.json, build/sentences.json.

    python3 vo.py
"""
import json
import os
import sys

import numpy as np
import soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import script  # noqa: E402

SR = 48000
CAP = 0.85          # the longest pause kept inside a take (s)
JOIN = 0.75         # between two takes of one chapter
CARD = 3.2          # between chapters: the title card's breath
LEAD = 1.2          # before the first word
TAIL = 20.0         # the end screen after the last word
# Re-reads spliced over a take from a word to the end of its chapter: (chapter, the word it starts on, take, its words).
# 2 Oct: the certificate's occupation field reads "Apprentice Salesman & Counterfeiter"; the first read said only
# "apprentice salesman".
PATCHES = [("rock", "Occupation,", "vo_11_fix.wav", "words_11_fix.json")]


def squeeze(y, cap=CAP, thresh_db=-42.0):
    """y with every silence longer than cap cut down to cap, and the map from old seconds to new."""
    hop = int(0.01 * SR)
    n = len(y) // hop
    rms = np.sqrt((y[: n * hop].reshape(n, hop) ** 2).mean(1) + 1e-12)
    silent = 20 * np.log10(rms / (np.abs(y).max() + 1e-9)) < thresh_db
    voiced = np.nonzero(~silent)[0]
    a, b = voiced[0] * hop, min(len(y), (voiced[-1] + 1) * hop)
    keep, cuts, i = [], [], voiced[0]
    while i <= voiced[-1]:
        if silent[i]:
            j = i
            while j < n and silent[j]:
                j += 1
            if (j - i) * 0.01 > cap:
                half = int(cap / 2 * SR)
                cuts.append((i * hop + half, j * hop - half))
            i = j
        else:
            i += 1
    pieces, pos, marks = [], a, []          # marks: (old start, new start) of each kept piece
    new = 0
    for c0, c1 in cuts:
        pieces.append(y[pos:c0]); marks.append((pos, new)); new += c0 - pos; pos = c1
    pieces.append(y[pos:b]); marks.append((pos, new))
    out = []
    for k, p in enumerate(pieces):           # 5 ms fades at each join (the joins sit in silence anyway)
        p = p.copy()
        f = min(len(p), int(0.005 * SR))
        if k:
            p[:f] *= np.linspace(0, 1, f)
        if k < len(pieces) - 1:
            p[len(p) - f:] *= np.linspace(1, 0, f)
        out.append(p)
    lens = [len(p) for p in pieces]

    def tmap(t):
        s = t * SR
        for (o, nw), ln in zip(marks, lens):
            if s < o:
                return nw / SR
            if s <= o + ln:
                return (nw + s - o) / SR
        return (marks[-1][1] + lens[-1]) / SR
    return np.concatenate(out).astype(np.float32), tmap


def main():
    parts = script.parts()
    titles = {c["id"]: c["title"] for c in script.CHAPTERS}
    t, chunks, words, chapters, last = LEAD, [], [], [], None
    for i, (cid, k, _) in enumerate(parts):
        y, sr = sf.read(os.path.join(HERE, "src", f"vo_{i:02d}.wav"), dtype="float32")
        y = y if y.ndim == 1 else y.mean(1)
        assert sr == SR
        y, tmap = squeeze(y)
        if last is not None:
            t += CARD if cid != last else JOIN
        if cid != last:
            chapters.append(dict(id=cid, title=titles[cid], card=round(t - (CARD if last else LEAD), 3), v0=round(t, 3)))
        chunks.append((t, y))
        for w, a, b in json.load(open(os.path.join(HERE, "src", f"words_{i:02d}.json"))):
            words.append([w, round(t + tmap(a), 3), round(t + tmap(b), 3), cid])
        t += len(y) / SR
        chapters[-1]["v1"] = round(t, 3)
        last = cid
    total = t + TAIL
    out = np.zeros(int(total * SR) + 1, np.float32)
    for s, y in chunks:
        i = int(round(s * SR))
        out[i: i + len(y)] += y
    for cid, word, take, wfile in PATCHES:
        ch = next(c for c in chapters if c["id"] == cid)
        start = next(w[1] for w in words if w[3] == cid and w[0] == word)
        y, sr = sf.read(os.path.join(HERE, "src", take), dtype="float32")
        y = y if y.ndim == 1 else y.mean(1)
        assert sr == SR and start + len(y) / SR <= ch["v1"] + 0.6, (take, start + len(y) / SR, ch["v1"])
        i0, i1 = int((start - 0.12) * SR), int(ch["v1"] * SR)
        old = out[i0:i1]
        y = y * (np.sqrt((old ** 2).mean()) / (np.sqrt((y ** 2).mean()) + 1e-9) if len(old) else 1.0)
        out[i0:i1] = 0.0
        j = int(start * SR)
        out[j: j + len(y)] = y
        words = [w for w in words if not (w[3] == cid and w[1] >= start - 0.01)]
        words += [[x[0], round(start + x[1], 3), round(start + x[2], 3), cid] for x in json.load(open(os.path.join(HERE, "src", wfile)))]
        words.sort(key=lambda w: w[1])
    os.makedirs(os.path.join(HERE, "build"), exist_ok=True)
    sf.write(os.path.join(HERE, "build", "voice.wav"), out, SR, subtype="PCM_24")
    json.dump(words, open(os.path.join(HERE, "build", "words.json"), "w"))
    json.dump(dict(total=round(total, 3), end_voice=round(t, 3), chapters=chapters),
              open(os.path.join(HERE, "build", "chapters.json"), "w"), indent=1)
    sents, cur = [], []
    for w in words:
        cur.append(w)
        if w[0][-1] in ".?!":
            sents.append(dict(t0=cur[0][1], t1=cur[-1][2], ch=cur[0][3], text=" ".join(x[0] for x in cur)))
            cur = []
    if cur:
        sents.append(dict(t0=cur[0][1], t1=cur[-1][2], ch=cur[0][3], text=" ".join(x[0] for x in cur)))
    json.dump(sents, open(os.path.join(HERE, "build", "sentences.json"), "w"), indent=0)
    print(f"voice ends {t:.1f}s ({t / 60:.1f} min), film {total:.1f}s; {len(words)} words, {len(sents)} sentences")
    for c in chapters:
        print(f"  {c['card']:7.2f} {c['v0']:7.2f}-{c['v1']:7.2f} {c['title']}")


if __name__ == "__main__":
    main()
