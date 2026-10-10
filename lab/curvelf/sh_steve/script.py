"""THE CURVE · SHORT · TWO GAMES, ONE SCREEN (prototype, written 10 Oct 2026; not voiced).

The viral "Minecraft's hero in GTA V" clip, corrected: it isn't an AI that reverse-engineered or dreamed a game. Two
unmodified games run side by side and a bridge, written by Claude Code in about two days with one person directing it,
passes camera, ground and pictures between them every frame. Every claim is in FACTS.md (S1-S5); the 400-block cap is
one source (VGTimes) and must be confirmed before render. Concept #1 in IDEAS.md.

Authorship line (CRAFT s.1): "in my view that glue is the whole trick". Loop (CRAFT s.6): the last words, "two other
games running at once", lead back into the first line, and the last picture is frame 0's torn screen.

Pictures h01-h05 are drawn in code by diagrams.py: our own cube-headed robot and a city of type. No game footage,
characters, logos or maps (third-party IP).

    P=~/youtube/.venv/bin/python
    $P flow.py sh_steve est
    FLOW_VERT=1 $P flow.py sh_steve still 0.2 3.5 ...
"""
TITLE = "IT'S TWO GAMES, NOT ONE"
TAG = "THE CURVE  ·  TWO GAMES, ONE SCREEN"
ILLUS = "DIAGRAM  ·  DRAWN FOR THIS SHORT"
LEAD = 0.4
OPEN_RESOLVED = True
FIX = {}

CHAPTERS = [
    dict(id="two", title="", beats=[
        (("You've seen Steve walking around GTA V. The trick is two games running at once.",
          "You've seen Steve walking around GTA Five. The trick is two games running at once."),
         ("img", "h01", "TWO GAMES · ONE SCREEN")),
        ("An AI coding agent wrote the bridge between them in about two days.",
         ("num", "~2 DAYS", "CLAUDE CODE + ONE PERSON · FIELD NOTE, 30 SEP 2026")),
        ("The city sends over its camera and the shape of its streets.",
         ("img", "h02", "CAMERA + GROUND")),
        ("The block world fills them with invisible blocks, so he walks on ground he can't see.",
         ("img", "h03", "AN INVISIBLE FLOOR")),
        ("His picture comes back with depth, so a lamp post can hide him.",
         ("img", "h04", "DEPTH DECIDES")),
        ("Nobody fused any code, and in my view that glue is the whole trick.",
         ("img", "h05", "GLUE, NOT FUSION")),
        ("You need both games, a Windows PC, and a build from source.",
         ("list", ["BOTH GAMES, YOUR OWN", "A WINDOWS PC", "STORY MODE ONLY", "BUILD IT YOURSELF"], "TO PLAY IT")),
        ("And it's open source, so the next clip could be two other games running at once.",
         ("img", "h01", "TWO GAMES · ONE SCREEN")),          # same label as frame 0: the loop seam matches (critic v1)
    ]),
]
