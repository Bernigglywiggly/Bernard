"""The Curve: the Tesla Roadster film (v2 style). Script v1, 17 Oct 2026.

Shape (ZACK_D_SKELETON.md §11, varied): eight segments, each opening on its own impact line and closing on its own
payoff, so each one cuts out as a Short with no editing. Two forward teases sit between segments (CRAFT §2, §9.7).
Narration: calm, long sentences joined by So / But / Then (CRAFT §2 professor voice; Zack D rhythm, about 2.7 words a
second). Every claim points at TESLA_ROADSTER_FACTS.md by source code; `check=True` lines wait on the 17 Oct facts
update (§13) and must not be voiced before it lands.

Lint before voicing:  python3 .claude/skills/film-critic/script_lint.py lab/curve_v2/film_roadster/script.py
Shot kinds: REAL = Tesla's own clip (3-7 s, credited, our narration on top, ZACK_D_SKELETON §12) · 3D = Blender ·
GFX = Remotion graphics. Facts codes: lab/research/TESLA_ROADSTER_FACTS.md §12.
"""

TITLE_WORKING = "How the Tesla Roadster Really Flies"

SEGMENTS = [
    dict(id="S1", name="The hang", short="How the Tesla Roadster Hangs Upside Down"),
    dict(id="S2", name="The roll", short="How the Tesla Roadster Flips in Mid-Air"),
    dict(id="S3", name="0.81 seconds", short="The Tesla Roadster's 0.81 Second Launch"),
    dict(id="S4", name="Seconds, then hours", short="How Long Can the Tesla Roadster Fly?"),
    dict(id="S5", name="The fan car", short="The Fan Car That Won Once and Vanished"),
    dict(id="S6", name="Is it legal?", short="Is the Flying Tesla Roadster Legal?"),
    dict(id="S7", name="The deposit", short="What $250,000 Buys You at Tesla"),
    dict(id="S8", name="Verdict", short=None),
]

LINES = [
    # S1 The hang = Roadster Short 1 as shipped (lab/curve_v2/shorts/short1.py, comp CurveV2-Short1). Keep in sync.
    dict(id="s1_1", seg="S1", facts="P1 P2",
         text="You're watching a Tesla Roadster being vacuumed to the ceiling.",
         shot="REAL 20x RIFE slow-mo of the car at the lip; hook 'UPSIDE DOWN AND NOT FALLING?' swaps to VACUUMED"),
    dict(id="s1_2", seg="S1", facts="P1 P10",
         text="Fans underneath pull the air out from beneath the car, while skirts around the edges seal the gap.",
         shot="footage tilts up; side-view diagram rises: fans spin, air streams out of the back, skirts seal"),
    dict(id="s1_3", seg="S1", facts="P1",
         text="Tesla says the air outside then pins it to the ramp with up to twice its own weight.",
         shot="cyan push arrow (2L) vs red WEIGHT arrow (L); badge 'UP TO 2x ITS WEIGHT'"),
    dict(id="s1_4", seg="S1", facts="P1 P10 U28",
         text="And unlike a wing, the fans work even when the car is standing still.",
         shot="bars: speed 100 -> 0 MPH, WING bar drains (v squared), FANS bar stays full"),
    dict(id="s1_5", seg="S1", facts="P2 S3 S5",
         text="Then it lets go, and jets of compressed gas roll it the right way up before it lands.",
         shot="REAL drop at 30 fps (RIFE), GAS JETS ring tracks the plume, smoke landing"),
    dict(id="s1_6", seg="S1", facts="P2",
         text="That's how it can hang up there without falling.",
         shot="rewind to the lip; hook rebuilds; last frame = frame 0"),

    # S2 The roll.
    dict(id="s2_1", seg="S2", facts="P2 S3 S5",
         text="As it falls, the Tesla Roadster fires jets of gas that roll it the right way up before it lands.",
         shot="REAL drop_punch at 0.9x: inverted drop, side jets fire, roll; freeze-frame ring on the jet"),
    dict(id="s2_2", seg="S2", facts="P1 S1 S13",
         text="The gas comes from two carbon-wrapped tanks of the kind SpaceX flies on its rockets, holding about a "
              "quarter of a tonne of it.",
         shot="3D X-ray build: rear tank, then the big tank where a passenger seat would be; '≈250 kg' tag"),
    dict(id="s2_3", seg="S2", facts="S1 S11 P10",
         text="It escapes through ten nozzles around the car, so the computer can push any corner up, down or "
              "sideways in a fraction of a second.",
         shot="3D nozzles light in order: rear, corners pointing down, front; counter ticks to 10"),
    dict(id="s2_4", seg="S2", facts="P1 S1 S12",
         text="The rear nozzles alone push with more than eighty kilonewtons, which Tesla's engineers compare to a "
              "fighter jet.",
         shot="GFX thrust bar '80+ kN' beside a generic jet silhouette (drawn, no real aircraft)"),
    dict(id="s2_5", seg="S2", facts="S1 S12",
         text="The gas leaves faster than sound, which is why the jets form the same diamond pattern you see behind "
              "a rocket.",
         shot="3D macro on a rear nozzle: Mach diamonds; label 'OUR 3D' bottom-left"),
    dict(id="s2_6", seg="S2", facts="P1 S1",
         text="So it's a rocket engine with nothing burning inside it, and it's what turns a falling car into a "
              "landing one.",
         shot="REAL the smoke landing (Ramp 0:22-0:25); the car settles on its wheels"),

    # S3 0.81 seconds.
    dict(id="s3_1", seg="S3", facts="P4 P1",
         text="Fired from a standstill, the Tesla Roadster hit sixty miles an hour in zero point eight one seconds.",
         shot="REAL 0-60 clip (Zg9Q56t7bdo), 3 s; big read-out locks at 0.81 s with 'TESLA'S OWN TIMING'"),
    dict(id="s3_2", seg="S3", facts="S14 S5 P10 [EST]",
         text="The version without thrusters is quoted at under one point six, so most of that gap is compressed gas.",
         shot="GFX two lanes race to 60: 'NO THRUSTERS <1.6 s' vs 'WITH GAS 0.81 s'"),
    dict(id="s3_3", seg="S3", facts="C5",
         text="That's about half the time of a Rimac Nevera R, one of the quickest cars ever independently timed.",
         shot="GFX third lane: 'RIMAC NEVERA R 1.66 s · DEWESOFT-VERIFIED'"),
    dict(id="s3_4", seg="S3", facts="P1 P4",
         text="But the stopwatch was Tesla's own, and nobody outside the company has timed the car yet.",
         shot="GFX stopwatch with a Tesla-red strap; 'NOT INDEPENDENTLY TIMED' stamp"),
    dict(id="s3_5", seg="S3", facts="P1 (19:00, 19:04)",
         text="Musk says the production car will be quicker still, and that the real limit is not detaching the "
              "driver's retinas.",
         shot="3D seat and harness, camera pushes in on the headrest; no human face"),
    dict(id="s3_6", seg="S3", facts="P4",
         text="So for now, zero point eight one is a promise with a stopwatch attached.",
         shot="GFX the 0.81 read-out again, the stopwatch clips onto it"),

    dict(id="b1", seg="BRIDGE", facts="-",
         text="In a moment, the number that decides how long this car can actually fly.",
         shot="3D tank gauge needle twitches; push through the gauge glass into S4"),

    # S4 Seconds, then hours. The film's own sum (authorship, CRAFT §1): label it OUR ESTIMATE on screen.
    dict(id="s4_1", seg="S4", facts="[EST §5] P1",
         text="The Tesla Roadster can only stay in the air for a handful of seconds, because its rocket fuel is a "
              "tank of squeezed gas.",
         shot="REAL hover/hop moment from the stream (pick in the clip log), 4 s"),
    dict(id="s4_2", seg="S4", facts="[EST §5] P1 S1",
         text="By our maths, the rear nozzles at full power would empty both tanks in about two seconds.",
         shot="GFX working on screen: 80 kN ÷ ≈600 m/s ≈ 130 kg/s · 250 kg ÷ 130 ≈ 2 s; 'OUR ESTIMATE'"),
    dict(id="s4_3", seg="S4", facts="S1",
         text="Tesla told Top Gear the Thrust version gets a single launch per fill, about five seconds of push.",
         shot="GFX quote card 'ONE LAUNCH PER FILL' · source line 'Lars Moravy to Top Gear'"),
    dict(id="s4_4", seg="S4", facts="S1",
         text="But filling the tanks back up isn't quick.",
         shot="3D gauge needle falls to empty; hard cut"),
    dict(id="s4_5", seg="S4", facts="S1",
         text="Lars Moravy, who runs vehicle engineering at Tesla, said a refill from a high-pressure nitrogen rig "
              "takes hours today.",
         shot="GFX clock face sweeping '2-6 HOURS'"),
    dict(id="s4_6", seg="S4", facts="S1",
         text="His target is under half an hour.",
         shot="GFX the sweep shrinks to a 30-minute wedge, 'TARGET'"),
    dict(id="s4_7", seg="S4", facts="P1 (12:30) S1",
         text="Elon Musk said on stage that the car can refill the tank itself, which is a long way from what his "
              "engineer told Top Gear.",
         shot="GFX split card: 'MUSK, ON STAGE: refills itself' vs 'MORAVY, TOP GEAR: hours, from a rig'"),
    dict(id="s4_8", seg="S4", facts="S1 [EST]",
         text="So the flying car flies for seconds, and then it waits for hours.",
         shot="REAL the landing in smoke, then hold on the parked car as the smoke clears"),

    dict(id="b2", seg="BRIDGE", facts="§13.2 (U11-U15)",
         text="In a minute, the racing car that used this trick in its only race, won it, and was never raced again.",
         shot="3D silhouette of a 1970s single-seater with a fan, lit from behind"),

    # S5 The fan car. Every line waits on §13 (Brabham BT46B, Chaparral 2J verified at two sources each).
    dict(id="s5_1", seg="S5", facts="§13.2 BT46B (Swedish GP, 17 Jun 1978)",
         text="In 1978, a Formula One team bolted a giant fan to the back of its car, and it won the first race it "
              "entered.",
         shot="3D generic 1978 fan car (no livery, no logos) on a track, fan spinning; 'AN F1 CAR, 1978'"),
    dict(id="s5_2", seg="S5", facts="§13.2 BT46B (declared as engine cooling)",
         text="The team said the fan was there to cool the engine, but it was also sucking the car onto the track.",
         shot="3D X-ray of the fan car: cooling arrows, then suction arrows under the floor"),
    dict(id="s5_3", seg="S5", facts="§13.2 BT46B (withdrawn straight after)",
         text="Brabham withdrew it straight after, and it never raced again.",
         shot="GFX 'RACES: 1 · WINS: 1'"),
    dict(id="s5_4", seg="S5", facts="§13.2 Chaparral 2J (1970, 4 entries, 0 wins, banned)",
         text="Eight years earlier, an American team had tried two fans driven by a separate little engine, and that "
              "car won nothing and was banned.",
         shot="3D generic boxy 1970 sports racer with twin rear fans"),
    dict(id="s5_5", seg="S5", facts="C6",
         text="And in 2025, a British car called the McMurtry Spéirling used its fans to drive upside down on a "
              "rotating rig.",
         shot="GFX timeline 1970 · 1978 · 2025 · 2026, each with its silhouette"),
    dict(id="s5_6", seg="S5", facts="C6 P2",
         text="So Tesla didn't invent the vacuum, it added the part where the car lets go of the ceiling and lands "
              "on its wheels.",
         shot="REAL the drop and landing, the 2026 dot on the timeline lights"),

    # S6 Is it legal?
    dict(id="s6_1", seg="S6", facts="S4",
         text="When reporters asked the American aviation regulator about the flying Tesla Roadster, it said the car "
              "isn't an aircraft.",
         shot="GFX statement card, FAA wording as a short fragment with the source line"),
    dict(id="s6_2", seg="S6", facts="S4",
         text="That leaves the road-safety regulator, which said it's up to Tesla to meet the federal safety "
              "standards, and that it will keep watching.",
         shot="GFX second card, NHTSA, 'WILL CONTINUE TO MONITOR'"),
    dict(id="s6_3", seg="S6", facts="P10",
         text="But Tesla's own website says the Rocket version, the one that flies, isn't approved for public roads "
              "at all.",
         shot="GFX recreated spec line from tesla.com with 'NOT APPROVED FOR PUBLIC ROAD USE' circled"),
    dict(id="s6_4", seg="S6", facts="P10 S1",
         text="Even on the Thrust version, which is road legal, the thrusters aren't meant for public roads.",
         shot="3D the Thrust car on a road, nozzles capped/dark; 'ROAD LEGAL · THRUSTERS OFF'"),
    dict(id="s6_4b", seg="S6", facts="S1 S13",
         text="A jet that strong turns loose gravel into projectiles.",
         shot="3D low angle: a thruster fires over a gravel shoulder, stones fly toward camera"),
    dict(id="s6_5", seg="S6", facts="P1 (11:50)",
         text="Musk himself said he isn't sure it's legal everywhere.",
         shot="GFX quote fragment 'not sure it's necessarily legal in all jurisdictions'"),
    dict(id="s6_6", seg="S6", facts="P10 S4",
         text="So the flying car can fly, as long as it's somewhere nobody calls a road.",
         shot="3D wide: the car on a test pad, empty desert, no road markings"),

    # S7 The deposit.
    dict(id="s7_1", seg="S7", facts="P10 S12",
         text="To reserve a Tesla Roadster with thrusters, you pay a quarter of a million dollars up front.",
         shot="GFX deposit counter rolls to $250,000 ('$5,000 NOW + $245,000 IN 10 DAYS' small under it)"),
    dict(id="s7_2", seg="S7", facts="P1 S21",
         text="The car is due in 2028, after a launch that was first promised for 2020.",
         shot="GFX timeline of the promised dates, each struck through, ending at 2028"),
    dict(id="s7_3", seg="S7", facts="§13.1 #1 (U1, US contract clause 4)",
         text="But Tesla's American contract says it can't guarantee the car will be delivered at all.",
         shot="GFX the terms clause, short fragment, highlighted"),
    dict(id="s7_4", seg="S7", facts="S1 S21",
         text="The range has shrunk too, from a promised six hundred and twenty miles to about half that.",
         shot="GFX range bar shrinking from 620 to about 310-320 mi"),
    dict(id="s7_5", seg="S7", facts="S1 P1",
         text="So the deposit holds a place in the queue for a car whose numbers are still moving.",
         shot="GFX spec sheet with values flickering between the quoted figures (power, weight, top speed)"),
    dict(id="s7_6", seg="S7", facts="P10 S12",
         text="That's a quarter of a million dollars for a place in a queue.",
         shot="GFX the $250,000 counter again, a queue of identical car silhouettes behind it"),

    # S8 Verdict (our judgement, CRAFT §1). Ends on the opening picture so the film loops back to frame 0.
    dict(id="s8_1", seg="S8", facts="-",
         text="So what did Tesla actually show in Texas?",
         shot="REAL wide aerial of the ramp run (Ramp 0:35-0:42), 5 s"),
    dict(id="s8_2", seg="S8", facts="P1 (15:09-15:25)",
         text="Tesla says the fans let the car corner at more than two g, where its tyres alone would manage about "
              "one and a quarter.",
         shot="GFX g-meter: needle at 1.26 g (tyres), then fans on, needle past 2"),
    dict(id="s8_3", seg="S8", facts="-",
         text="That grip without speed is the real engineering, and it's the part that could matter on a race track.",
         shot="3D the car through a corner, fan exhaust streaks"),
    dict(id="s8_4", seg="S8", facts="[EST §5] S1",
         text="The thrusters are the spectacle, a few seconds of stored gas that take hours to replace.",
         shot="3D X-ray: tanks and nozzles glow, gauge drains"),
    dict(id="s8_4b", seg="S8", facts="P10",
         text="And the version that carries the most of them isn't allowed on public roads.",
         shot="3D X-ray fades; the Rocket badge area (no logo) dims"),
    dict(id="s8_5", seg="S8", facts="P1 S1",
         text="Almost everything that makes it fly came from SpaceX, from the tanks to the test site where it flew.",
         shot="GFX labels on the X-ray: 'COPV · SPACEX', 'NOZZLES · SPACEX', 'MCGREGOR TEST SITE · SPACEX'"),
    dict(id="s8_6", seg="S8", facts="-",
         text="So the Roadster is two machines in one body, a brilliant vacuum cleaner and a very short rocket.",
         shot="3D the car splits into two ghost layers: fans (cyan) and tanks/nozzles (magenta)"),
    dict(id="s8_7", seg="S8", facts="P2",
         text="And for now, the most impressive thing it does is hang upside down and not fall.",
         shot="REAL the hang, same framing as frame 0; hard stop"),
]
