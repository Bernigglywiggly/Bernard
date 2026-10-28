"""Curve Short 11 (Thu 29 Oct 2026, publishes 17:00 UK): "Touchscreen MacBook: Why It Took 16 Years" (branch T).

DRAFT by account B, Wed 28 Oct 16:00 UK, before Apple's 17:00 announcement: not voiced. Lines marked ⏳ depend on what
Apple's press release says (facts §5 slots 100-110); the scheduled 17:40 run (task b-thu-apple-short) fills the slots,
rewrites those lines from Apple's own words, lints, voices and builds. If Apple shows no touchscreen Mac, this script is
dropped for branch N1 or N2 (facts §6, task brief). Facts: lab/research/APPLE_PRO_AND_TELL_FACTS.md (rows).

Frame 0: Apple's own shot of a finger on the new MacBook Pro's screen (slot 108, credited "APPLE"), kicker "APPLE SAID
NO / FOR 16 YEARS". Our diagrams carry the argument and most of the runtime (CRAFT 18 Oct: borrowed footage under half):
the "said no" timeline (rows 40-45), the capacitive grid under a fingertip (60-62), torque about the hinge (70-71).
Verdict (our point of view): Jobs was right about tired arms, so touch became an extra (keep only if slot 104 or rows 24-25
hold). Jobs's words in quote marks only as copied from the 2010 recordings (footage/apple_2026-10-28/JOBS_2010_QUOTE.md). Loop: the verdict
cuts back to frame 0's touch shot.
"""
TITLE = "Touchscreen MacBook: Why It Took 16 Years"
LINES = [
    dict(id="x1", facts="40, 41 (Jobs, Back to the Mac, 20 Oct 2010: words copied from two recordings, footage/apple_2026-10-28/JOBS_2010_QUOTE.md); ⏳ 101 (touch confirmed)",
         text="In 2010, Apple said touchscreen Macs don't work.",
         cap="In 2010, / Apple said / touchscreen Macs / don't work.",
         shot="frame 0 = Apple's film, a finger on the new MacBook Pro's screen (⏳ slot 108; until then our line drawing); "
              "kicker 'APPLE SAID NO / FOR 16 YEARS'; tag '“IT DOESN’T WORK.” · STEVE JOBS, 2010'"),
    dict(id="x2", facts="40, 42, 43, 44 (Jobs 2010, Cook 2012, Federighi 2014 and 2018); 80-81 (arm fatigue); OUR MATHS 2026 - 2010 = 16",
         text="Its bosses kept saying no for sixteen years, because reaching up to a screen tires your arm.",
         cap="Its bosses / kept saying no / for sixteen years, / because reaching up / to a screen / tires your arm.",
         shot="timeline 2010 JOBS, 2012 COOK, 2014 FEDERIGHI, 2018 FEDERIGHI, each stamped NO, then 2026 TOUCH; on 'reaching' "
              "an arm reaches a vertical screen and a fatigue bar fills; 'GORILLA ARM' with Jobs's “YOUR ARM WANTS TO FALL OFF.”"),
    dict(id="x3", facts="60, 61, 62 (projected capacitive grid: one set of lines sends, the other receives, each crossing a tiny capacitor)",
         text="Under the glass is a grid of invisible wires, and your finger changes the electric field where two of them cross.",
         cap="Under the glass / is a grid / of invisible wires, / and your finger / changes the electric field / where two of them cross.",
         shot="our grid: rows SEND, columns RECEIVE, a scan sweeps the crossings; a fingertip lands, the field at one crossing "
              "bends, the crossing lights, readout 'X 6 · Y 3'; tag 'PROJECTED CAPACITIVE TOUCH'"),
    dict(id="x4", facts="70, 71 (torque = force x lever arm; OUR MATHS: twice the distance from the hinge, twice the twist)",
         text="But a laptop screen hangs on a hinge, so a tap at the top twists it twice as hard as one halfway down.",
         cap="But a laptop screen / hangs on a hinge, / so a tap at the top / twists it twice as hard / as one / halfway down.",
         shot="side view: base, hinge, screen; a tap at the top swings a big torque arc round the hinge and the screen "
              "wobbles; a tap halfway down swings half the arc; 'TORQUE = FORCE × DISTANCE', tag 'OUR MATHS · 2×'"),
    dict(id="x5", facts="⏳ 103, 104 (Apple's own words on the hinge and the touch features); else 24-26 with REPORTED on screen",
         text="⏳ So Apple stiffened the hinge, and menus now open around your finger.",
         cap="⏳ So Apple / stiffened the hinge, / and menus now open / around your finger.",
         shot="⏳ Apple's film of the touch features (a menu opening round a fingertip), credited 'APPLE'; label from Apple's "
              "wording only"),
    dict(id="x6", facts="verdict (our point of view); ⏳ keep only if slot 104 or rows 24-25 hold up",
         text="Jobs was right about tired arms, so Apple made touch the thing you reach for only when it's quicker.",
         cap="Jobs was right / about tired arms, / so Apple made touch / the thing you reach for / only when / it's quicker.",
         shot="verdict rows: TIRED ARMS → JOBS WAS RIGHT, TOUCH → AN EXTRA, TRACKPAD → STILL FIRST; hard cut to frame 0's "
              "touch shot (loop)"),
]
