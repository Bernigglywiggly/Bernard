"""A01 v5 hook proof: the shot list. Times are seconds in the voice take (AUDIO).

Every shot names its world (palette) and the register it serves, so the palette
switches follow the script's rhythm instead of feeling random:
    FACT -> W0 core rooms · TRANSLATE -> W1 PRESS · JOKE -> W4 SIGNAL
    DEEP -> W2 CLOUD · PAYOFF -> W3 CHROME · every world carries the amber drift line.
"""
import os

FPS = 24
HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.environ.get("A01_BUILD", os.path.join(HERE, "build"))
FONTS = os.environ.get("A01_FONTS", os.path.join(HERE, "fonts"))
TEX = os.path.join(BUILD, "tex")
AUDIO = os.environ.get("A01_AUDIO", os.path.join(HERE, "audio", "B_COUSIN_roger_x1.12.mp3"))
DURATION = 50.31

SHOTS = [
    dict(id="S01", t0=0.00, t1=2.30, world="W0 · STAIR", reg="FACT", move="worm's-eye crane, line draws itself",
         line="On September 22nd"),
    dict(id="S02", t0=2.30, t1=4.85, world="W0 · STAIR", reg="FACT", move="god's-eye top-down, slow roll",
         line="two AI companies dropped new models", hits=[1.63, 1.81]),
    dict(id="S03", t0=4.85, t1=6.20, world="W1 · PRESS", reg="TRANSLATE", move="top-down on the page",
         line="ninety minutes apart", bloom=0.06, hud="ink"),
    dict(id="S04", t0=6.20, t1=7.60, world="W1 · PRESS", reg="TRANSLATE", move="swing to grazing angle, the 90 stands up",
         line="Ninety minutes.", bloom=0.2, hits=[0.75]),
    dict(id="S05", t0=7.60, t1=12.60, world="W4 · SIGNAL", reg="JOKE", move="shot/reverse, dutch, 4-frame bursts",
         line="that's two exes posting a glow-up on the same night", step=2, post="signal", bloom=0.3, hits=[1.917, 2.917, 3.417, 3.583, 3.75, 3.917, 4.083, 4.25, 4.417, 4.583, 4.75]),
    dict(id="S06", t0=12.60, t1=17.50, world="W0 · LOBBY", reg="FACT", move="low orbit, 88 degrees",
         line="scored fourteen points higher ... on the coding test", hits=[1.0]),
    dict(id="S07", t0=17.50, t1=19.90, world="W3 · CHROME", reg="PAYOFF", move="FPV swoop that lands",
         line="Fourteen points better.", hits=[1.6]),
    dict(id="S08", t0=19.90, t1=22.50, world="W2 · CLOUD", reg="DEEP", move="dolly zoom (vertigo)",
         line="But what does that actually mean?"),
    dict(id="S09", t0=22.50, t1=26.20, world="W1 · PRESS", reg="TRANSLATE", move="dutch truck + rack focus",
         line="most people read that like a phone update", bloom=0.06, hud="ink"),
    dict(id="S10", t0=26.20, t1=28.80, world="W1 · PRESS", reg="JOKE", move="push, then snap zoom on 'cool'",
         line="'oh, fourteen percent faster, cool'", bloom=0.06, hits=[2.083], hud="ink"),
    dict(id="S11", t0=28.80, t1=32.50, world="W4 · SIGNAL", reg="JOKE", move="snap zooms on the beat",
         line="you would not notice, you would not care", step=2, post="signal", bloom=0.3, hits=[1.583, 2.75]),
    dict(id="S12", t0=32.50, t1=33.60, world="W0 · VOID", reg="JOKE", move="snap push + impact shake",
         line="Wrong."),
    dict(id="S13", t0=33.60, t1=34.60, world="W0 · VOID", reg="JOKE", move="worm's-eye dutch",
         line="Not only wrong", hits=[0.0]),
    dict(id="S14", t0=34.60, t1=36.90, world="W0 · VOID", reg="JOKE", move="spiral dive through the words",
         line="completely, embarrassingly wrong",
         overlays=[("TXT_COMPLETELY.png", 0.05, 0.85), ("TXT_EMBARRASSINGLY.png", 0.9, 2.3)], hits=[0.05, 0.9, 1.8]),
    dict(id="S15", t0=36.90, t1=41.70, world="W2 · CLOUD", reg="DEEP", move="long-lens crane, points become the line",
         line="fourteen points on the right test isn't the same job done a bit better"),
    dict(id="S16", t0=41.70, t1=47.50, world="W1 · PRESS", reg="TRANSLATE", move="truck, whip pan on 'hands'",
         line="the one who starts the group project vs the one who hands it in", bloom=0.2, hits=[4.7]),
    dict(id="S17", t0=47.50, t1=DURATION, world="MAP · ALL WORLDS", reg="PAYOFF", move="crane up: one line, many worlds",
         line="Same number. Whole different animal.",
         overlays=[("TXT_SAME.png", 0.45, 99), ("TXT_ANIMAL.png", 1.45, 99)]),
]


# The ending ritual: every video can close in the same place. Slow, warm, hopeful; the HUD steps
# away, the amber stops being a line and becomes the dawn. Rendered as its own 12 s clip.
OUTRO = dict(id="S18", t0=0.0, t1=12.0, world="HOME", reg="HOPE", move="slow glide over still water, tilt up to the sky",
             line="(your closing words)", bloom=0.5, hud_fade=(0.4, 2.6),
             overlays=[("TXT_HOME.png", 6.2, 99)], fade_in=1.2, fade_out=1.4)


def frames(s):
    """Frame count of a shot (cuts land on whole frames of the 24 fps timeline)."""
    return round(s["t1"] * FPS) - round(s["t0"] * FPS)


def lf(s, t):
    """Absolute audio time -> the shot's local frame (1-based)."""
    return round((t - s["t0"]) * FPS) + 1
