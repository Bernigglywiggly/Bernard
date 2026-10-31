"""Word timings for narration takes with faster-whisper: src/vo_XX.wav -> src/words_XX.json [[word, start, end]].
small.en, not conditioned on the previous text (3 Oct: base.en dropped a whole sentence from a take, which put
every picture after it out of step)."""
import json
import os
import sys

from faster_whisper import WhisperModel

model = WhisperModel(os.environ.get("WHISPER", "small.en"), device="cpu", compute_type="int8")
for p in sys.argv[1:]:
    out = p.replace("vo_", "words_").replace(".wav", ".json")
    if os.path.exists(out):
        continue
    segs, _ = model.transcribe(p, word_timestamps=True, vad_filter=False, beam_size=5, condition_on_previous_text=False)
    ws = [[w.word.strip(), round(w.start, 3), round(w.end, 3)] for s in segs for w in s.words]
    json.dump(ws, open(out, "w"))
    print(p, len(ws), "words", ws[-1][2] if ws else 0)
