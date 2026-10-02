"""Word timings for narration takes with faster-whisper (base.en): src/vo_XX.wav -> src/words_XX.json [[word, start, end]]."""
import json
import os
import sys

from faster_whisper import WhisperModel

model = WhisperModel("base.en", device="cpu", compute_type="int8")
for p in sys.argv[1:]:
    out = p.replace("vo_", "words_").replace(".wav", ".json")
    if os.path.exists(out):
        continue
    segs, _ = model.transcribe(p, word_timestamps=True, vad_filter=False, beam_size=5)
    ws = [[w.word.strip(), round(w.start, 3), round(w.end, 3)] for s in segs for w in s.words]
    json.dump(ws, open(out, "w"))
    print(p, len(ws), "words", ws[-1][2] if ws else 0)
