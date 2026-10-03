"""The score: jazz, one cue per chapter, starting on its title card and running 1.5 s under the next (3 Oct, the user:
"scrap the background music replace with jazz or house jazz for these sorts of vids, futuristic bg music dont match").
Kevin MacLeod's jazz (CC BY 4.0, lab/music/jazz/library.py); the credit lines go in POST.md. Noir for the cons and
Capone, swing for the hustles, the dance-jazz "Cool Blast" for the counterfeiting, acid jazz to close; the last cue is
cut so its own ending lands on the end card. Writes build/beds/<chapter>.wav and build/music.json for film.py.

    python3 music.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, LAB)
sys.path.insert(0, os.path.join(LAB, "music", "jazz"))
import audio_fx as fx  # noqa: E402
import library  # noqa: E402

# chapter -> (track, gain dB, align)
PLAN = {
    "open": ("Covert Affair", 0.0, "start"),
    "boy": ("No Good Layabout", 0.0, "start"),
    "box": ("Spy Glass", -0.5, "start"),
    "tower": ("I Knew a Guy", 0.5, "start"),
    "sale": ("Dances and Dames", 0.0, "start"),
    "back": ("Opportunity Walks", -0.5, "start"),
    "capone": ("On the Cool Side", -0.5, "start"),
    "money": ("Cool Blast", 0.0, "start"),
    "locker": ("Walking Along", 0.5, "start"),
    "escape": ("Faster Does It", -0.5, "start"),
    "rock": ("Night on the Docks - Trumpet", 0.0, "start"),
    "rules": ("Acid Trumpet", 0.0, "end"),
}
XF = 1.5      # seconds a cue runs on under the next one


def main():
    ch = json.load(open(os.path.join(HERE, "build", "chapters.json")))
    cards = [c["card"] for c in ch["chapters"]] + [ch["total"]]
    os.makedirs(os.path.join(HERE, "build", "beds"), exist_ok=True)
    out = []
    for c, t0, t1 in zip(ch["chapters"], cards, cards[1:]):
        track, gain, align = PLAN[c["id"]]
        end = min(ch["total"], t1 + XF)
        path = os.path.join(HERE, "build", "beds", f"{c['id']}.wav")
        fx.save(path, library.section(track, end - t0, align), mp3=False)
        out.append([round(t0, 3), round(end, 3), path, gain])
        print(f"{c['id']:7s} {track:30s} {t0:7.2f}-{end:7.2f}")
    json.dump(out, open(os.path.join(HERE, "build", "music.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
