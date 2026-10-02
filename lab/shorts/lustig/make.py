"""MONEY CRIMES · short 01: "He sold the Eiffel Tower. Twice." (Victor Lustig, 1925). The flagship AI short (2 Oct).

Narration: Higgsfield Seed Audio, preset voice Imogen, read in one take (src/voice.wav), word timings by Whisper
(src/words.json). Pictures: 17 GPT Image 2.5 stills (src/s*.png, two character references so Lustig and Poisson stay
the same people) animated by Kling 3.0 Pro and, for the opening, Google Veo 3.1 (clips/c*.mp4). Score: beds.caper
(src/bed_caper.wav). Facts: Wikipedia, Victor Lustig (the Capone story is told as "the story goes").

    python3 shorts/lustig/make.py          -> shorts/lustig/out/lustig_eiffel_9x16.mp4
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import reel  # noqa: E402

S, C = os.path.join(HERE, "src"), os.path.join(HERE, "clips")
clip = lambda n: os.path.join(C, f"c{n:02d}.mp4")
still = lambda n: os.path.join(S, f"s{n:02d}.png")
opening = clip(1) if os.path.exists(clip(1)) else None

SPEC = dict(
    VOICE=os.path.join(S, "voice.wav"), WORDS=os.path.join(S, "words.json"), BED=os.path.join(S, "bed_caper.wav"),
    FIX={"tons": "tonnes", "Andre": "André", "Grand": "grand"},
    END=63.4,
    SHOTS=[
        (0.00, "clip", opening) if opening else (0.00, "still", still(1), dict(s0=1.0, s1=1.16, dy=-40)),
        (4.00, "clip", clip(2)),       # Lustig: smoke, the smile
        (8.70, "clip", clip(4)),       # the newspaper
        (11.70, "clip", clip(5)),      # the rusting tower
        (14.70, "clip", clip(6)),      # the forged letterhead
        (16.85, "clip", clip(7)),      # the hotel
        (19.55, "clip", clip(8)),      # the secret meeting
        (23.55, "still", still(9), dict(s0=1.02, s1=1.14)),   # the blueprint, crossed out
        (26.30, "clip", clip(10)),     # the dealers lean in
        (31.15, "clip", clip(11)),     # André Poisson
        (35.00, "clip", clip(12)),     # the francs
        (37.95, "clip", clip(13)),     # the train
        (39.70, "clip", clip(14)),     # Poisson's shame
        (43.25, "clip", clip(15)),     # he came back
        (46.45, "clip", clip(16)),     # the police
        (49.25, "clip", clip(17)),     # America
        (51.40, "clip", clip(18)),     # the speakeasy
        (54.85, "clip", clip(19)),     # the tower today
        (57.70, "still", still(1), dict(s0=1.08, s1=1.2, sepia=True)),   # sold twice
        (59.55, "clip", clip(21)),     # a single bolt
    ],
    OVERLAYS=[
        dict(kind="label", t0=0.0, t1=3.6, text="AI REENACTMENT", y=150, size=26),
        dict(kind="label", t0=0.3, t1=3.8, text="PARIS · 1925", y=230, size=40, align="center", color=0xFFFFC83D),
        dict(kind="name", t0=6.75, t1=8.65, title="VICTOR LUSTIG", sub="CON ARTIST · 1890-1947", y=250),
        dict(kind="redx", t0=25.55, t1=26.30, lines=[((300, 520), (800, 1420)), ((800, 520), (300, 1420))]),
        dict(kind="stamp", t0=26.36, t1=30.9, text="7,000 TONNES", y=430, rot=-5),
        dict(kind="name", t0=32.35, t1=34.95, title="ANDRÉ POISSON", sub="SCRAP-METAL DEALER", y=250),
        dict(kind="stamp", t0=35.66, t1=37.9, text="70,000 FRANCS", y=400, rot=4, size=140),
        dict(kind="stamp", t0=57.88, t1=59.55, text="VENDU", y=620, rot=-12, size=190),
        dict(kind="stamp", t0=58.10, t1=59.55, text="VENDU", y=980, rot=9, size=190, dx=40),
    ],
    SFX=[(0.0, "sub_drop", -4), (4.05, "whoosh", -10), (8.70, "paper", -8), (14.70, "clack", -8), (19.6, "chatter", -16),
         (25.55, "paper", -6), (26.36, "thock", -2), (35.66, "thock", -2), (35.7, "coin", -10), (37.95, "whoosh", -8),
         (46.45, "latch", -6), (49.25, "whoosh", -10), (54.85, "swell", -10), (57.88, "thock", 0), (58.10, "thock", 0),
         (59.68, "sub_drop", -8)],
)

CAPER_PLAN = [("intro", 2), ("a", 8), ("b", 9), ("break", 2), ("a", 7), ("out", 4)]   # the swing lands on "Then he sold it again"

if __name__ == "__main__":
    if not os.path.exists(SPEC["BED"]):                       # the score is re-made, not stored (python3 fetch.py gets the rest)
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "music"))
        import beds  # noqa: E402
        reel.fx.save(SPEC["BED"], beds.caper(118, CAPER_PLAN), mp3=False)
    out = os.path.join(HERE, "out")
    os.makedirs(out, exist_ok=True)
    reel.render(SPEC, os.path.join(HERE, "build"), os.path.join(out, "lustig_eiffel_9x16.mp4"))
