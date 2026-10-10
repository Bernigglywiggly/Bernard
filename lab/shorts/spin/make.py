"""WHAT IF · short 01: "What if Earth stopped spinning for one second?" (2 Oct).

Narration: Higgsfield Seed Audio, preset voice Zoe, one take (src/voice.wav), Whisper word timings (src/words.json).
Pictures: 12 GPT Image 2.5 stills animated by Kling 3.0 Pro, the orbit opener by Google Veo 3.1. Score: beds.arena (dark
hybrid orchestral) with the arrival on "stopped?". Facts: equatorial spin ~1,670 km/h (faster than sound, ~1,235 km/h);
strongest recorded winds ~408 km/h (gust) to ~486 km/h (tornado, radar), so "over three times"; airliners cruise
~900 km/h; the day lengthens by ~1.7-2.3 ms a century. A thought experiment, labelled as an AI visualisation.

    python3 shorts/spin/make.py          -> shorts/spin/out/spin_9x16.mp4
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import reel  # noqa: E402

S, C = os.path.join(HERE, "src"), os.path.join(HERE, "clips")
clip = lambda n: os.path.join(C, f"c{n:02d}.mp4")
still = lambda n: os.path.join(S, f"s{n:02d}.png")
pic = lambda n, **o: (("clip", clip(n)) if os.path.exists(clip(n)) else ("still", still(n), dict(s0=1.0, s1=1.14, **o)))

SPEC = dict(
    VOICE=os.path.join(S, "voice.wav"), WORDS=os.path.join(S, "words.json"), BED=os.path.join(S, "bed_arena.wav"),
    BED_DB=-19.0, DUCK_DB=-9.0,
    FIX={"kilometers": "kilometres"},
    END=66.5,
    SHOTS=[(t,) + pic(n) for t, n in ((0.0, 1), (6.1, 2), (12.4, 3), (18.5, 4), (23.5, 5), (28.6, 6), (32.8, 7), (38.5, 8),
                                       (45.8, 9), (51.2, 10), (56.2, 11), (61.8, 12))],
    OVERLAYS=[
        dict(kind="label", t0=0.0, t1=4.0, text="AI VISUALISATION · A THOUGHT EXPERIMENT", y=150, size=24),
        dict(kind="name", t0=6.2, t1=9.0, title="THE EQUATOR", sub="EARTH'S FASTEST SPIN", y=250),
        dict(kind="stamp", t0=8.0, t1=11.6, text="1,670 KM/H", y=560, rot=-4, color=0xFFFFC83D),
        dict(kind="stamp", t0=14.28, t1=16.6, text="1 SECOND", y=560, rot=3, color=0xFFFFC83D, size=160),
        dict(kind="stamp", t0=26.2, t1=28.6, text="3× RECORD WIND", y=520, rot=-5, size=130),
        dict(kind="name", t0=48.1, t1=50.9, title="THE POLES", sub="THE SLOWEST SPIN ON EARTH", y=250),
        dict(kind="stamp", t0=59.0, t1=61.6, text="+2 MS A CENTURY", y=520, rot=-3, color=0xFFFFC83D, size=120),
    ],
    SFX=[(0.0, "swell", -10), (8.0, "thock", -4), (12.6, "riser", -6), (14.28, "thock", -4), (16.8, "sub_drop", 0),
         (18.5, "hydraulic", -8), (23.5, "vortex", -8), (26.2, "thock", -4), (32.8, "sub_drop", -6), (38.5, "whoosh", -6),
         (45.8, "swell", -12), (59.0, "tick_run", -10), (61.8, "swell", -12)],
)

ARENA_PLAN = [("intro", 5), ("break", 2), ("b", 12), ("a", 4), ("out", 5)]   # the braam lands on "stopped?" (16.8 s)

if __name__ == "__main__":
    if not os.path.exists(SPEC["BED"]):
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "music"))
        import beds  # noqa: E402
        reel.fx.save(SPEC["BED"], beds.arena(100, ARENA_PLAN), mp3=False)
    out = os.path.join(HERE, "out")
    os.makedirs(out, exist_ok=True)
    reel.render(SPEC, os.path.join(HERE, "build"), os.path.join(out, "spin_9x16.mp4"))
