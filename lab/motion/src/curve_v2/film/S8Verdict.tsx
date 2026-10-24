import { Video } from "@remotion/media";
import { evolvePath } from "@remotion/paths";
import type React from "react";
import { AbsoluteFill, Easing, Img, interpolate, Sequence, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { CLAMP, EASE_IN_OUT, EASE_OUT } from "../../lib/anim";
import { BG_NIGHT, C, ClipScene, Credit, FILL, HEADC, Headline, keyline, MONO, pop, Sfx, slowPush, Stamp, Tag } from "../kit";
import { BlueprintGrid, BlueprintLines, FREEZE_SRC, PAY_ORIGIN, PAY_SCALE_END } from "./S9Bill";
import { cue, segFrames } from "./util";

// Roadster film, segment S8 ("Verdict", 41.8 s), the film's last word before the end card. Facts:
// lab/research/TESLA_ROADSTER_FACTS.md §2 (over 2 g with the fans vs about 1.26 g on tyres, Tesla's figures), §4 (refill
// 2-6 h, Moravy to Top Gear; 10 nozzles on Rocket, 4 on Thrust; COPV tanks based on Falcon hardware), §5 (about 2 s at
// full thrust: our estimate), §0 (SpaceX's McGregor test site), P10 (Rocket "not approved for public road use").
// Opens on S9's last picture (the kickflip as line-work) winding back into Tesla's footage; ends on the hang with the
// film's opening question answered. Tesla footage < half the runtime; the 3D shots are ours (labelled).

const SEG = "S8";
const W = (word: string, nth = 1) => cue(SEG, word, nth);
const T = {
  so: W("So"), actually: W("actually"), tesla2: W("Tesla", 2), fans: W("fans"), corner: W("corner"), g2: W("2G"), tires: W("tires"),
  one: W("one"), quarter: W("quarter"),
  that: W("That"), grip: W("grip"), speed: W("speed"), real: W("real"), could: W("could"),
  thrusters: W("thrusters"), spectacle: W("spectacle"), seconds: W("seconds"), gas: W("gas"), hours: W("hours"), replace: W("replace"),
  version: W("version"), carries: W("carries"), most: W("most"), isnt: W("isn't"), roads: W("roads"),
  almost: W("Almost"), came: W("came"), spacex: W("SpaceX"), tanks: W("tanks"), test: W("test"), flew: W("flew"),
  so2: W("So", 2), roadster: W("Roadster"), two: W("two"), machines: W("machines"), body: W("body"), brilliant: W("brilliant"),
  // "and" occurs six times: 284, 408, 632, 1046 ("cleaner and a very"), 1092 ("And for now"), 1205 ("and not fall")
  vacuum: W("vacuum"), and3: W("and", 4), very: W("very"), rocket: W("rocket"),
  for: W("for"), impressive: W("impressive"), hang: W("hang"), upside: W("upside"), and4: W("and", 6), fall: W("fall"),
};
const F = {
  grip: T.tesla2 - 6,      // 100: the g-meter
  real: T.that - 6,        // 304: the real engineering (aerial)
  spec: T.thrusters - 10,  // 471: the spectacle (3D x-ray)
  legal: T.version - 10,   // 630: Rocket, not road legal
  spacex: T.almost - 5,    // 740: the SpaceX parts
  two: T.so2 - 4,          // 912: two machines in one body
  final: T.for - 8,        // 1091: the hang
  end: segFrames(SEG),     // 1254
};

const DIM = "rgba(255,255,255,0.62)";
const CREDIT_TOP = 958;
const CREDIT_LOW = 1010; // under the row of cars in the kickflip
const FOOTAGE = "FOOTAGE: TESLA / YOUTUBE · SLOWED DOWN";
const OURS = "3D ILLUSTRATION · THE CURVE";
const ease = (frame: number, a: number, b: number, easing = EASE_OUT) => interpolate(frame, [a, b], [0, 1], { ...CLAMP, easing });

// ------------------------------------------------------------------------------------------------- 1. the question
// Frame 0 is S9's last picture (the kickflip as line-work). The lines wind back, the photo returns, and the clip plays
// on from the frozen frame: what actually happened in Texas.
const RESUME = 22;
const Open: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame >= F.grip + 2) return null;
  const pull = interpolate(frame, [0, 30], [PAY_SCALE_END, 1], { ...CLAMP, easing: EASE_IN_OUT });
  const drift = slowPush(frame, 30, F.grip, 1.035);
  const unDraw = interpolate(frame, [4, 24], [1, 0], { ...CLAMP, easing: EASE_IN_OUT });
  const photo = ease(frame, 4, 22, EASE_IN_OUT);
  const out = ease(frame, F.grip - 10, F.grip + 2, EASE_IN_OUT);
  return (
    <AbsoluteFill style={{ opacity: 1 - out }}>
      <AbsoluteFill style={{ scale: pull * drift, transformOrigin: PAY_ORIGIN }}>
        <BlueprintGrid opacity={1 - ease(frame, 2, 20)} />
        {frame <= RESUME ? <Img src={staticFile(FREEZE_SRC)} style={{ ...FILL, opacity: photo, filter: `brightness(${0.45 + photo * 0.6})` }} /> : null}
        <Sequence from={RESUME} durationInFrames={F.grip + 2 - RESUME} premountFor={fps}>
          <Video src={staticFile("film/kick_side_slow.mp4")} muted trimBefore={120} style={FILL} />
        </Sequence>
        {unDraw > 0.001 ? <BlueprintLines draw={unDraw} under={0.55 * photo} /> : null}
      </AbsoluteFill>
      <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(0,0,0,0.5) 0%, rgba(0,0,0,0) 38%)" }} />
      <Headline at={T.so - 2} left={100} top={96} lines={[{ text: "SO WHAT DID TESLA", size: 104 }]} />
      <Headline at={T.actually - 2} left={100} top={196} lines={[{ text: "ACTUALLY SHOW?", size: 150, color: C.acid }]} />
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------- 2. the g-meter
const G = { cx: 960, cy: 920, r: 700, band: 80, max: 2.5 };
const gPt = (v: number, r: number) => {
  const th = Math.PI - (v / G.max) * Math.PI;
  return [G.cx + r * Math.cos(th), G.cy - r * Math.sin(th)] as const;
};
const ARC = `M ${G.cx - G.r} ${G.cy} A ${G.r} ${G.r} 0 0 1 ${G.cx + G.r} ${G.cy}`;
const TYRES = 1.26;
const FANS = 2.06; // "more than two g": the pointer settles just past 2

const GMeter: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < F.grip || frame >= F.real) return null;
  const frameIn = ease(frame, F.grip, F.grip + 26, EASE_IN_OUT);
  const sweep = interpolate(frame, [T.fans - 2, T.g2], [0, 1], { ...CLAMP, easing: Easing.bezier(0.45, 0, 0.2, 1) });
  const lock = pop(frame, T.g2, fps, 240, 9);
  const v = frame < T.g2 ? sweep * 2 : 2 + (FANS - 2) * lock;
  const tyre = ease(frame, T.tires - 2, T.tires + 10);
  const tyreNum = pop(frame, T.one - 2, fps, 230, 12);
  const band = evolvePath(frameIn, ARC);
  const fill = evolvePath(Math.min(1, v / G.max), ARC);
  const white = evolvePath(TYRES / G.max, ARC);
  const [px, py] = gPt(v, G.r + G.band / 2 + 6);
  const ang = 90 - (v / G.max) * 180; // pointer rotation (deg): 90 at 0 g, -90 at 2.5 g
  const ticks = Array.from({ length: 11 }, (_, i) => i * 0.25);
  const labels: [number, string][] = [[0, "0"], [0.5, "0.5"], [2, "2"], [2.5, "2.5"]];
  const [tx1, ty1] = gPt(TYRES, G.r - G.band / 2 - 8);
  const [tx2, ty2] = gPt(TYRES, G.r + G.band / 2 + 8);
  return (
    <AbsoluteFill style={{ scale: slowPush(frame, F.grip, F.real, 1.04), transformOrigin: "50% 70%" }}>
      <svg width={1920} height={1080} style={{ position: "absolute", left: 0, top: 0 }}>
        <path d={ARC} fill="none" stroke="rgba(255,255,255,0.14)" strokeWidth={G.band} strokeDasharray={band.strokeDasharray} strokeDashoffset={band.strokeDashoffset} />
        {v > 0.001 ? <path d={ARC} fill="none" stroke={C.cyan} strokeWidth={G.band - 14} strokeDasharray={fill.strokeDasharray} strokeDashoffset={fill.strokeDashoffset} /> : null}
        {tyre > 0 ? <path d={ARC} fill="none" stroke={C.ink} strokeOpacity={tyre} strokeWidth={G.band - 14} strokeDasharray={white.strokeDasharray}
          strokeDashoffset={white.strokeDashoffset} /> : null}
        {ticks.map((t) => {
          const [ax, ay] = gPt(t, G.r - G.band / 2 - 6);
          const [bx, by] = gPt(t, G.r - G.band / 2 - (t % 0.5 === 0 ? 40 : 24));
          return <line key={t} x1={ax} y1={ay} x2={bx} y2={by} stroke={C.ink} strokeWidth={t % 0.5 === 0 ? 6 : 3} opacity={frameIn} />;
        })}
        {tyre > 0 ? <line x1={tx1} y1={ty1} x2={tx2} y2={ty2} stroke={C.ink} strokeWidth={10} opacity={tyre} /> : null}
        {v > 0.001 ? (
          <g transform={`translate(${px} ${py}) rotate(${-ang})`}>
            <polygon points="0,0 -22,-46 22,-46" fill={C.cyan} stroke={C.black} strokeWidth={5} strokeLinejoin="round" transform="rotate(180)" />
          </g>
        ) : null}
      </svg>
      {labels.map(([t, txt]) => {
        const [lx, ly] = gPt(t, G.r - G.band / 2 - 92);
        return (
          <div key={txt} style={{ position: "absolute", left: lx - 80, top: ly - 34, width: 160, textAlign: "center", ...HEADC, fontSize: 60,
            color: t === 2 ? C.cyan : C.ink, opacity: frameIn, ...keyline(0.4, 8) }}>{txt}</div>
        );
      })}
      {/* tyres alone: the white marker's label, under the top of the dial */}
      <div style={{ position: "absolute", left: G.cx - 300, width: 600, top: 356, textAlign: "center", opacity: tyre, translate: `0 ${(1 - tyre) * 20}px` }}>
        <div style={{ ...HEADC, fontSize: 64, color: C.ink, ...keyline(0.45, 9) }}>TYRES ALONE</div>
        <div style={{ ...HEADC, fontSize: 104, color: C.ink, marginTop: 6, scale: interpolate(tyreNum, [0, 1], [0.6, 1]),
          opacity: interpolate(tyreNum, [0, 0.3], [0, 1], CLAMP), ...keyline(0.75, 10) }}>≈1.26 g</div>
      </div>
      {/* the read-out counts with the sweep, then locks on "more than two" */}
      <div style={{ position: "absolute", left: G.cx - 500, width: 1000, top: 592, textAlign: "center", opacity: interpolate(frame, [T.fans - 4, T.fans + 4], [0, 1], CLAMP) }}>
        <div style={{ ...HEADC, fontSize: 230, color: C.cyan, fontVariantNumeric: "tabular-nums", scale: frame >= T.g2 ? interpolate(lock, [0, 1], [1.25, 1]) : 1,
          ...keyline(1.5, 11) }}>{frame >= T.g2 ? ">2 g" : `${(sweep * 2).toFixed(2)} g`}</div>
        <div style={{ ...MONO, fontSize: 44, color: C.ink, marginTop: 14 }}>CORNERING WITH THE FANS ON</div>
      </div>
      <Tag at={F.grip + 4} left={100} top={100} size={60}>TESLA SAYS</Tag>
      <div style={{ position: "absolute", right: 100, top: 100, textAlign: "right", opacity: frameIn, translate: `${(1 - frameIn) * 30}px 0` }}>
        <div style={{ ...HEADC, fontSize: 84, color: C.ink, ...keyline(0.6, 9) }}>CORNERING GRIP</div>
        <div style={{ ...MONO, fontSize: 44, color: DIM, marginTop: 10 }}>IN g · 1 g = GRAVITY</div>
      </div>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------- 3. the real engineering
// Tesla's wide aerial; the curled ramp where the fans held the car is traced in cyan (video pixel coordinates).
const CURL = "M 1300 470 C 1380 464 1480 424 1534 384 C 1584 346 1618 292 1630 200 C 1636 140 1622 88 1592 50 C 1566 28 1530 22 1505 24";
const RealEngineering: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < F.real || frame >= F.spec + 2) return null;
  const curl = ease(frame, T.grip, T.grip + 22, EASE_IN_OUT);
  const ev = evolvePath(curl, CURL);
  const lab = ease(frame, T.grip + 14, T.grip + 26);
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ scale: interpolate(frame, [F.real, F.spec], [1, 1.05], CLAMP), transformOrigin: "62% 38%" }}>
        <Sequence from={F.real} durationInFrames={F.spec + 2 - F.real} premountFor={fps}>
          <Video src={staticFile("film/ramp_aerial_wide.mp4")} muted trimBefore={40} style={FILL} />
        </Sequence>
        <svg width={1920} height={1080} style={{ position: "absolute", left: 0, top: 0 }}>
          <path d={CURL} fill="none" stroke={C.black} strokeOpacity={0.6} strokeWidth={16} strokeLinecap="round" strokeDasharray={ev.strokeDasharray}
            strokeDashoffset={ev.strokeDashoffset} />
          <path d={CURL} fill="none" stroke={C.cyan} strokeWidth={8} strokeLinecap="round" strokeDasharray={ev.strokeDasharray} strokeDashoffset={ev.strokeDashoffset} />
        </svg>
        <div style={{ position: "absolute", left: 1290, top: 492, opacity: lab, translate: `0 ${(1 - lab) * 16}px`, ...HEADC, fontSize: 60, color: C.cyan,
          ...keyline(0.5, 9) }}>IT HUNG HERE</div>
      </AbsoluteFill>
      <AbsoluteFill style={{ background: "linear-gradient(90deg, rgba(0,0,0,0.62) 0%, rgba(0,0,0,0.25) 45%, rgba(0,0,0,0) 62%)" }} />
      <Headline at={T.grip - 2} left={100} top={96} stagger={6} lines={[{ text: "GRIP WITHOUT", size: 124, color: C.cyan }, { text: "SPEED", size: 200, color: C.cyan }]} />
      <Stamp at={T.real - 2} left={104} top={500} color={C.cyan} size={84} rot={-5}>THE REAL<br />ENGINEERING</Stamp>
      <Headline at={T.could - 2} left={100} top={790} lines={[{ text: "AND IT COULD MATTER ON A RACE TRACK", size: 62 }]} stroke={9} />
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------- 4. the spectacle
// Our 3D x-ray (tanks, then the nozzles lighting). The 2 s counter runs in real time.
const Spectacle: React.FC = () => {
  const frame = useCurrentFrame();
  if (frame < F.spec || frame >= F.legal + 2) return null;
  const t0 = T.seconds - 2;
  const run = interpolate(frame, [t0, t0 + 60], [0, 1], CLAMP);
  const refill = interpolate(frame, [T.hours, F.legal], [0, 0.035], CLAMP);
  const level = frame < T.hours ? 1 - run : refill;
  const hrs = ease(frame, T.hours - 2, T.hours + 12);
  const timerIn = ease(frame, t0 - 8, t0 + 2);
  return (
    <AbsoluteFill>
      <ClipScene src="film/blender_xray.mp4" from={F.spec} dur={F.legal + 2 - F.spec} push={[1, 1.05]} origin="66% 50%" />
      <AbsoluteFill style={{ background: "linear-gradient(90deg, rgba(10,4,24,0.94) 0%, rgba(10,4,24,0.8) 40%, rgba(10,4,24,0) 64%)" }} />
      <Headline at={T.thrusters - 2} left={100} top={96} lines={[{ text: "THE THRUSTERS ARE", size: 84 }]} stroke={9} />
      <Stamp at={T.spectacle - 2} left={104} top={198} color={C.magenta} size={112} rot={-5}>THE SPECTACLE</Stamp>
      <div style={{ position: "absolute", left: 100, top: 420, opacity: timerIn }}>
        <div style={{ ...HEADC, fontSize: 190, color: C.magenta, fontVariantNumeric: "tabular-nums", ...keyline(1.2, 11) }}>
          {(run * 2).toFixed(1)} S
        </div>
        <div style={{ ...MONO, fontSize: 44, color: C.ink, marginTop: 10 }}>OF FULL THRUST · OUR ESTIMATE</div>
        <div style={{ position: "relative", marginTop: 22, width: 640, height: 40, border: `5px solid ${C.ink}`, borderRadius: 22, overflow: "hidden" }}>
          <div style={{ position: "absolute", left: 0, top: 0, bottom: 0, width: `${level * 100}%`, backgroundColor: frame < T.hours ? C.magenta : C.acid }} />
        </div>
      </div>
      <div style={{ position: "absolute", left: 100, top: 776, opacity: hrs, translate: `0 ${(1 - hrs) * 24}px` }}>
        <div style={{ ...HEADC, fontSize: 84, color: C.acid, ...keyline(0.6, 9) }}>THEN 2–6 HOURS TO REFILL</div>
        <div style={{ ...MONO, fontSize: 44, color: DIM, marginTop: 10 }}>LARS MORAVY, TESLA, TO TOP GEAR</div>
      </div>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------- 5. not for roads
// Top-down outlines (nose right): Thrust has 4 rear nozzles; Rocket has 10 (4 rear, 4 corners pointing down, 2 front).
const BODY = "M 52 120 C 52 58 92 24 170 20 L 470 20 C 548 22 604 56 626 120 C 604 184 548 218 470 220 L 170 220 C 92 216 52 182 52 120 Z";
const GLASS = "M 300 50 C 352 40 420 40 466 56 C 486 90 486 150 466 184 C 420 200 352 200 300 190 C 288 150 288 90 300 50 Z";
const DECK = "M 196 40 C 186 90 186 150 196 200";
const WHEELS = "M 118 6 L 188 6 L 188 20 L 118 20 Z M 118 220 L 188 220 L 188 234 L 118 234 Z M 470 6 L 540 6 L 540 20 L 470 20 Z M 470 220 L 540 220 L 540 234 L 470 234 Z";
type Noz = { x: number; y: number; dir: "rear" | "down" | "up" | "dn" };
const REAR: Noz[] = [72, 100, 140, 168].map((y) => ({ x: 52, y, dir: "rear" as const }));
const ROCKET_NOZ: Noz[] = [...REAR, { x: 130, y: 44, dir: "down" }, { x: 130, y: 196, dir: "down" }, { x: 512, y: 44, dir: "down" },
  { x: 512, y: 196, dir: "down" }, { x: 592, y: 70, dir: "up" }, { x: 592, y: 170, dir: "dn" }];

const TopCar: React.FC<{ x: number; y: number; nozzles: Noz[]; lit: number; fire: number; color: string; draw: number }> = ({ x, y, nozzles, lit, fire, color, draw }) => (
  <svg width={760} height={400} viewBox="-90 -80 760 400" style={{ position: "absolute", left: x - 90, top: y - 80 }}>
    {[BODY, GLASS, DECK, WHEELS].map((d, i) => {
      const ev = evolvePath(draw, d);
      return <path key={i} d={d} fill="none" stroke={C.ink} strokeWidth={i === 0 ? 5 : 3} strokeLinejoin="round" strokeDasharray={ev.strokeDasharray} strokeDashoffset={ev.strokeDashoffset} />;
    })}
    {nozzles.map((n, i) => {
      const on = interpolate(lit, [i / nozzles.length, (i + 1) / nozzles.length], [0, 1], CLAMP);
      if (on <= 0) return null;
      const L = 70 * fire;
      const plume = n.dir === "rear" ? `M ${n.x - 2} ${n.y - 9} L ${n.x - 2 - L} ${n.y} L ${n.x - 2} ${n.y + 9} Z`
        : n.dir === "up" ? `M ${n.x - 9} ${n.y} L ${n.x} ${n.y - L} L ${n.x + 9} ${n.y} Z`
          : n.dir === "dn" ? `M ${n.x - 9} ${n.y} L ${n.x} ${n.y + L} L ${n.x + 9} ${n.y} Z` : "";
      return (
        <g key={i} opacity={on}>
          {plume ? <path d={plume} fill={color} fillOpacity={0.75} stroke={C.black} strokeWidth={2} /> : null}
          {n.dir === "down" ? <circle cx={n.x} cy={n.y} r={12 + 10 * fire} fill="none" stroke={color} strokeWidth={4} opacity={0.9} /> : null}
          <circle cx={n.x} cy={n.y} r={9} fill={color} stroke={C.black} strokeWidth={3} />
        </g>
      );
    })}
  </svg>
);

const NotForRoads: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < F.legal || frame >= F.spacex) return null;
  const draw = ease(frame, F.legal, F.legal + 18, EASE_IN_OUT);
  const dimA = ease(frame, T.most - 4, T.most + 8);
  const fire = ease(frame, T.most - 2, T.most + 12);
  const rowIn = (at: number) => pop(frame, at, fps, 210, 15);
  const a = rowIn(F.legal + 4);
  const b = rowIn(F.legal + 10);
  return (
    <AbsoluteFill style={{ scale: slowPush(frame, F.legal, F.spacex, 1.04), transformOrigin: "40% 55%" }}>
      <Headline at={F.legal + 2} left={100} top={96} lines={[{ text: "THE VERSION WITH THE MOST THRUSTERS", size: 72 }]} stroke={9} />
      <div style={{ opacity: interpolate(a, [0, 0.3], [0, 1], CLAMP) * (1 - dimA * 0.68) }}>
        <div style={{ position: "absolute", left: 100, top: 290, ...HEADC, fontSize: 96, color: C.ink, ...keyline(0.7, 10) }}>THRUST</div>
        <div style={{ position: "absolute", left: 100, top: 392, ...MONO, fontSize: 44, color: DIM }}>4 NOZZLES</div>
        <TopCar x={600} y={250} nozzles={REAR} lit={ease(frame, F.legal + 10, F.legal + 22)} fire={0.35} color={C.magenta} draw={draw} />
      </div>
      <div style={{ opacity: interpolate(b, [0, 0.3], [0, 1], CLAMP) }}>
        <div style={{ position: "absolute", left: 100, top: 616, ...HEADC, fontSize: 96, color: C.magenta, ...keyline(0.7, 10) }}>ROCKET</div>
        <div style={{ position: "absolute", left: 100, top: 718, ...MONO, fontSize: 44, color: C.ink }}>10 NOZZLES</div>
        <TopCar x={600} y={580} nozzles={ROCKET_NOZ} lit={ease(frame, T.carries - 4, T.most + 4)} fire={0.35 + 0.65 * fire} color={C.magenta} draw={draw} />
      </div>
      <Stamp at={T.isnt} left={1270} top={560} color={C.warn} size={72} rot={-6}>NOT APPROVED<br />FOR PUBLIC<br />ROAD USE</Stamp>
      <div style={{ position: "absolute", left: 1290, top: 852, ...MONO, fontSize: 44, color: C.ink, opacity: ease(frame, T.isnt + 10, T.isnt + 20) }}>
        TESLA.COM, ON ROCKET
      </div>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------- 6. made by SpaceX
const ICON_TANK = [
  "M -130 -50 L 100 -50 A 50 50 0 0 1 100 50 L -130 50 A 50 50 0 0 1 -130 -50 Z",
  ...[-100, -60, -20, 20, 60].map((x) => `M ${x - 22} -46 L ${x + 22} 46`),
  ...[-100, -60, -20, 20, 60].map((x) => `M ${x + 22} -46 L ${x - 22} 46`),
  "M 150 0 L 178 0 M 178 -16 L 178 16",
];
const ICON_NOZZLE = [
  "M -22 -112 L 22 -112 L 22 -80 L 10 -62 C 34 -22 70 28 92 68 L -92 68 C -70 28 -34 -22 -10 -62 L -22 -80 Z",
  "M -56 90 L -74 128", "M 0 90 L 0 136", "M 56 90 L 74 128",
];
const ICON_PIN = [
  "M 0 58 C -20 28 -68 -12 -68 -56 A 68 68 0 1 1 68 -56 C 68 -12 20 28 0 58 Z",
  "M -24 -56 A 24 24 0 1 0 24 -56 A 24 24 0 1 0 -24 -56",
  "M -92 82 A 92 22 0 1 0 92 82 A 92 22 0 1 0 -92 82",
  "M -146 82 A 146 36 0 1 0 146 82 A 146 36 0 1 0 -146 82",
];
const PARTS = [
  { x: 400, icon: ICON_TANK, title: "THE TANKS", sub: ["CARBON-WRAPPED,", "BASED ON FALCON"], at: T.tanks - 6 },
  { x: 960, icon: ICON_NOZZLE, title: "THE NOZZLES", sub: ["COLD-GAS,", "SPACEX-DERIVED"], at: T.tanks + 6 },
  { x: 1520, icon: ICON_PIN, title: "THE TEST SITE", sub: ["SPACEX, McGREGOR,", "TEXAS"], at: T.test - 2 },
];

const FromSpaceX: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < F.spacex || frame >= F.two) return null;
  return (
    <AbsoluteFill style={{ scale: slowPush(frame, F.spacex, F.two, 1.04), transformOrigin: "50% 60%" }}>
      <Headline at={T.almost - 2} left={100} top={96} lines={[{ text: "ALMOST EVERYTHING THAT MAKES IT FLY", size: 72 }]} stroke={9} />
      <Headline at={T.came - 2} left={96} top={186} lines={[{ text: "CAME FROM SPACEX", size: 150, color: C.magenta }]} />
      {PARTS.map((p, pi) => {
        // a faint pencil row is up from the start ("what makes it fly"); each part inks in when the narration names it
        const ghost = ease(frame, F.spacex + 8 + pi * 10, F.spacex + 44 + pi * 10, EASE_IN_OUT);
        const d = ease(frame, p.at, p.at + 18, EASE_IN_OUT);
        const t = pop(frame, p.at + 10, fps, 220, 14);
        return (
          <div key={p.title}>
            <svg width={420} height={300} viewBox="-210 -150 420 300" style={{ position: "absolute", left: p.x - 210, top: 400 }}>
              {p.icon.map((path, i) => {
                const g = evolvePath(ghost, path);
                return <path key={`g${i}`} d={path} fill="none" stroke={C.ink} strokeOpacity={0.22} strokeWidth={i === 0 ? 6 : 3} strokeLinecap="round"
                  strokeLinejoin="round" strokeDasharray={g.strokeDasharray} strokeDashoffset={g.strokeDashoffset} />;
              })}
              {d > 0 ? p.icon.map((path, i) => {
                const ev = evolvePath(d, path);
                return <path key={i} d={path} fill="none" stroke={i === 0 ? C.magenta : C.ink} strokeWidth={i === 0 ? 8 : 4} strokeLinecap="round"
                  strokeLinejoin="round" strokeDasharray={ev.strokeDasharray} strokeDashoffset={ev.strokeDashoffset} />;
              }) : null}
            </svg>
            <div style={{ position: "absolute", left: p.x - 120, width: 240, top: 690, height: 4, backgroundColor: "rgba(255,255,255,0.22)",
              scale: `${ghost} 1`, opacity: 1 - interpolate(t, [0, 0.3], [0, 1], CLAMP) }} />
            <div style={{ position: "absolute", left: p.x - 300, width: 600, top: 722, textAlign: "center", opacity: interpolate(t, [0, 0.3], [0, 1], CLAMP),
              translate: `0 ${(1 - t) * 24}px` }}>
              <div style={{ ...HEADC, fontSize: 68, color: C.ink, ...keyline(0.5, 9) }}>{p.title}</div>
              <div style={{ ...MONO, fontSize: 44, lineHeight: 1.12, color: DIM, marginTop: 12 }}>{p.sub[0]}<br />{p.sub[1]}</div>
            </div>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------- 7. two machines
// One side-view outline splits into two layers: the vacuum cleaner (fans, skirts, the air pressing down) and the very
// short rocket (two tanks, plumes). Each then becomes its band of our 3D: blender_hang above, blender_drop below.
const SIDE = {
  body: "M 30 238 C 26 214 40 196 80 186 C 170 168 300 150 420 128 C 470 96 540 64 620 58 C 700 52 790 60 860 84 C 960 116 1080 150 1150 176 L 1172 188 L 1168 238 L 1010 246 A 80 80 0 0 0 850 246 L 310 246 A 80 80 0 0 0 150 246 Z",
  window: "M 450 128 C 520 84 580 70 640 68 C 720 66 790 76 828 98 L 806 128 Z",
  line: "M 560 204 C 700 200 820 192 920 166",
  wheels: "M 868 238 A 62 62 0 1 0 992 238 A 62 62 0 1 0 868 238 M 168 238 A 62 62 0 1 0 292 238 A 62 62 0 1 0 168 238",
  hubs: "M 908 238 A 22 22 0 1 0 952 238 A 22 22 0 1 0 908 238 M 208 238 A 22 22 0 1 0 252 238 A 22 22 0 1 0 208 238",
};
const SIDE_PATHS = [SIDE.body, SIDE.window, SIDE.line, SIDE.wheels, SIDE.hubs];
const arrow = (x: number, y0: number, y1: number) => `M ${x} ${y0} L ${x} ${y1} M ${x - 16} ${y1 - 20} L ${x} ${y1} L ${x + 16} ${y1 - 20}`;
const VAC = [
  "M 434 262 A 46 12 0 1 0 526 262 A 46 12 0 1 0 434 262", "M 644 262 A 46 12 0 1 0 736 262 A 46 12 0 1 0 644 262",
  "M 312 250 L 312 292 L 848 292 L 848 250",
  arrow(300, 20, 120), arrow(520, -50, 50), arrow(740, -64, 36), arrow(960, 0, 94),
];
const ROCK = [
  "M 600 118 L 720 118 A 36 36 0 0 1 720 190 L 600 190 A 36 36 0 0 1 600 118 Z",
  "M 880 150 L 1010 150 A 28 28 0 0 1 1010 206 L 880 206 A 28 28 0 0 1 880 150 Z",
];
const PLUMES = ["M 1170 200 L 1330 214 L 1170 228 Z", "M 104 246 L 118 372 L 132 246 Z", "M 1028 246 L 1042 372 L 1056 246 Z"];

const Side: React.FC<{ color: string; draw: number; extra?: string[]; extraDraw?: number; plumes?: number; width?: number }> = ({ color, draw, extra = [],
  extraDraw = 0, plumes = 0, width = 5 }) => (
  <svg width={1400} height={560} viewBox="-100 -120 1400 560" style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }}>
    {plumes > 0 ? PLUMES.map((d, i) => <path key={`p${i}`} d={d} fill={color} fillOpacity={0.55 * plumes} stroke={color} strokeWidth={3} opacity={plumes} />) : null}
    {SIDE_PATHS.map((d, i) => {
      const ev = evolvePath(draw, d);
      return <path key={i} d={d} fill="none" stroke={color} strokeWidth={i === 0 ? width : width - 2} strokeLinejoin="round" strokeLinecap="round"
        strokeDasharray={ev.strokeDasharray} strokeDashoffset={ev.strokeDashoffset} />;
    })}
    {extra.map((d, i) => {
      const ev = evolvePath(extraDraw, d);
      return <path key={`e${i}`} d={d} fill="none" stroke={color} strokeWidth={4} strokeLinejoin="round" strokeLinecap="round"
        strokeDasharray={ev.strokeDasharray} strokeDashoffset={ev.strokeDashoffset} />;
    })}
  </svg>
);

const TwoMachines: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < F.two || frame >= F.final) return null;
  const draw = ease(frame, F.two + 2, T.roadster + 14, EASE_IN_OUT);
  const split = ease(frame, T.two - 2, T.two + 22, EASE_IN_OUT);
  const vacFeat = ease(frame, T.machines, T.machines + 18, EASE_IN_OUT);
  const rockFeat = ease(frame, T.machines + 8, T.machines + 26, EASE_IN_OUT);
  const topBand = ease(frame, T.brilliant - 10, T.brilliant + 2, EASE_IN_OUT);
  const botBand = ease(frame, T.and3 - 4, T.and3 + 8, EASE_IN_OUT);
  const sc = interpolate(split, [0, 1], [1, 0.78]);
  // the outline is 1200 x 300 (plus arrows and plumes); centre it, then send the layers to the two bands
  const place = (dy: number): React.CSSProperties => ({ position: "absolute", left: 960 - 600, top: 540 - 160, width: 1200, height: 320,
    scale: sc, translate: `${split * 160}px ${(dy - 22) * split}px`, transformOrigin: "50% 50%" });
  return (
    <AbsoluteFill>
      {/* the bands of 3D, each arriving with its line of narration */}
      <div style={{ position: "absolute", left: 0, top: 0, width: 1920, height: 536, overflow: "hidden", opacity: topBand }}>
        <Sequence from={T.brilliant - 10} premountFor={fps}>
          <Video src={staticFile("film/blender_hang.mp4")} muted trimBefore={88} objectFit="cover"
            style={{ width: 1920, height: 1080, position: "absolute", top: -300, scale: interpolate(frame, [T.brilliant - 10, F.final], [1, 1.05], CLAMP) }} />
        </Sequence>
        <AbsoluteFill style={{ background: "linear-gradient(90deg, rgba(10,4,24,0.85) 0%, rgba(10,4,24,0.35) 50%, rgba(10,4,24,0) 70%)" }} />
      </div>
      <div style={{ position: "absolute", left: 0, top: 544, width: 1920, height: 536, overflow: "hidden", opacity: botBand }}>
        <Sequence from={T.and3 - 4} premountFor={fps}>
          <Video src={staticFile("film/blender_drop.mp4")} muted trimBefore={6} objectFit="cover"
            style={{ width: 1920, height: 1080, position: "absolute", top: -170 }} />
        </Sequence>
        <AbsoluteFill style={{ background: "linear-gradient(90deg, rgba(10,4,24,0.85) 0%, rgba(10,4,24,0.35) 50%, rgba(10,4,24,0) 70%)" }} />
      </div>
      {split > 0 ? <div style={{ position: "absolute", left: 0, top: 536, width: 1920 * split, height: 8, backgroundColor: C.black }} /> : null}

      {/* the outline: white, then two coloured layers pulling apart */}
      <div style={{ ...place(0), opacity: 1 - split }}><Side color={C.ink} draw={draw} /></div>
      {split > 0 ? (
        <>
          <div style={{ ...place(-240), opacity: interpolate(split, [0, 0.3], [0, 1], CLAMP) * (1 - topBand * 0.85) }}>
            <Side color={C.cyan} draw={1} extra={VAC} extraDraw={vacFeat} />
          </div>
          <div style={{ ...place(240), opacity: interpolate(split, [0, 0.3], [0, 1], CLAMP) * (1 - botBand * 0.85) }}>
            <Side color={C.magenta} draw={1} extra={ROCK} extraDraw={rockFeat} plumes={rockFeat} />
          </div>
        </>
      ) : null}

      <Tag at={T.machines - 2} until={T.brilliant - 6} left={760} top={500} bg={C.acid} size={64} rot={[-6, -2]}>TWO MACHINES · ONE BODY</Tag>
      <Headline at={T.brilliant - 2} left={100} top={250} lines={[{ text: "A BRILLIANT", size: 72 }, { text: "VACUUM CLEANER", size: 132, color: C.cyan }]} />
      <Headline at={T.very - 4} left={100} top={720} lines={[{ text: "A VERY SHORT", size: 72 }, { text: "ROCKET", size: 160, color: C.magenta }]} />
      <div style={{ position: "absolute", right: 100, top: 100, ...MONO, fontSize: 44, color: C.ink, opacity: topBand }}>FANS · SKIRTS</div>
      <div style={{ position: "absolute", right: 100, top: 590, ...MONO, fontSize: 44, color: C.ink, opacity: botBand }}>TANKS · NOZZLES</div>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------- 8. upside down
// The film's last image: the hang, and the question Short 1 opened on ("UPSIDE DOWN AND NOT FALLING?") answered.
// A side view of the curl beside it, so the picture reads as a ceiling, not a wall (CRAFT, 18 Oct).
const CURL_SIDE = "M 40 282 C 250 282 372 252 424 164 C 466 94 452 30 384 18 C 324 8 276 38 266 84";
// the car hangs under the top of the curl: wheels up against the ramp, roof towards the ground
const CAR_INV = "M 322 40 L 438 40 L 436 54 L 420 58 Q 412 76 396 76 L 364 76 Q 348 76 342 58 L 326 54 Z";
const CAR_GLASS = "M 356 60 L 406 60 Q 400 70 392 70 L 368 70 Q 360 70 356 60 Z";
const CAR_WHEELS = "M 338 30 A 11 11 0 1 0 360 30 A 11 11 0 1 0 338 30 M 400 30 A 11 11 0 1 0 422 30 A 11 11 0 1 0 400 30";

const Finale: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < F.final) return null;
  const fall = pop(frame, T.fall - 2, fps, 170, 7);
  const swapAt = T.fall + 14;
  const swap = pop(frame, swapAt, fps, 260, 10);
  const diag = ease(frame, T.impressive - 4, T.impressive + 26, EASE_IN_OUT);
  const carIn = ease(frame, T.hang - 8, T.hang + 4);
  return (
    <AbsoluteFill style={{ backgroundColor: C.black }}>
      <AbsoluteFill style={{ scale: interpolate(frame, [F.final, F.end], [1, 1.07], CLAMP), transformOrigin: "72% 46%" }}>
        <Sequence from={F.final} durationInFrames={F.end - F.final} premountFor={fps}>
          <Video src={staticFile("film/hang_slow8.mp4")} muted trimBefore={14} style={{ ...FILL, translate: "240px 0" }} />
        </Sequence>
      </AbsoluteFill>
      <AbsoluteFill style={{ background: "linear-gradient(90deg, rgba(0,0,0,0.55) 0%, rgba(0,0,0,0) 45%)" }} />
      <Tag at={T.for - 2} left={100} top={100} size={56}>FOR NOW,</Tag>
      <div style={{ position: "absolute", left: 100, top: 196, ...HEADC }}>
        {[
          { text: "UPSIDE DOWN", at: T.upside - 2, size: 140, color: C.ink },
          { text: "AND NOT", at: T.and4 - 2, size: 140, color: C.ink },
        ].map((ln) => {
          const s = pop(frame, ln.at, fps, 200, 14);
          if (frame < ln.at) return <div key={ln.text} style={{ height: ln.size * 0.9 }} />;
          return (
            <div key={ln.text} style={{ fontSize: ln.size, color: ln.color, opacity: interpolate(s, [0, 0.3], [0, 1], CLAMP),
              translate: `${(1 - s) * -80}px ${(1 - s) * -24}px`, ...keyline(ln.size / 150, 10) }}>{ln.text}</div>
          );
        })}
        {frame >= T.fall - 2 ? (
          <div style={{ fontSize: 180, color: C.magenta, translate: `0 ${(1 - fall) * -90}px`, rotate: `${interpolate(fall, [0, 1], [-6, -2])}deg`,
            opacity: interpolate(fall, [0, 0.2], [0, 1], CLAMP), transformOrigin: "0% 50%", ...keyline(1.2, 11) }}>
            FALLING<span style={{ display: "inline-block", scale: frame >= swapAt ? interpolate(swap, [0, 1], [1.8, 1]) : 1,
              color: frame >= swapAt ? C.acid : C.magenta }}>{frame >= swapAt ? "." : "?"}</span>
          </div>
        ) : null}
      </div>
      {/* side view of the curl: where "down" is */}
      <svg width={624} height={372} viewBox="-20 -20 520 310" style={{ position: "absolute", left: 76, top: 636, opacity: diag > 0 ? 1 : 0 }}>
        {(() => {
          const ev = evolvePath(diag, CURL_SIDE);
          return <path d={CURL_SIDE} fill="none" stroke={C.cyan} strokeWidth={10} strokeLinecap="round" strokeDasharray={ev.strokeDasharray} strokeDashoffset={ev.strokeDashoffset} />;
        })()}
        <g opacity={carIn}>
          <path d={CAR_INV} fill={C.ink} stroke={C.black} strokeWidth={3} strokeLinejoin="round" />
          <path d={CAR_GLASS} fill={C.black} />
          <path d={CAR_WHEELS} fill={C.black} stroke={C.ink} strokeWidth={3} />
        </g>
        <path d="M -10 290 L 300 290" stroke="rgba(255,255,255,0.5)" strokeWidth={3} strokeDasharray="10 10" opacity={diag} />
      </svg>
      <div style={{ position: "absolute", left: 640, top: 868, ...MONO, fontSize: 44, lineHeight: 1.1, color: C.cyan, opacity: diag }}>THE RAMP,<br />SIDE VIEW</div>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------- the segment
export const S8Verdict: React.FC = () => (
  <AbsoluteFill style={{ background: BG_NIGHT, overflow: "hidden" }}>
    <Open />
    <GMeter />
    <RealEngineering />
    <Spectacle />
    <NotForRoads />
    <FromSpaceX />
    <TwoMachines />
    <Finale />
    <Credit text={FOOTAGE} top={CREDIT_LOW} show={[[4, F.grip]]} />
    <Credit text={FOOTAGE} top={CREDIT_TOP} show={[[F.real, F.spec]]} />
    <Credit text={FOOTAGE} top={CREDIT_LOW} show={[[F.final, F.end]]} />
    <Credit text="SOURCE: TESLA ROADSTER EVENT, 15 OCT 2026" top={CREDIT_TOP} show={[[F.grip, F.real]]} />
    <Credit text={OURS} top={CREDIT_TOP} show={[[F.spec, F.legal], [T.brilliant - 10, F.final]]} />
    <Credit text="SOURCES: TESLA.COM · TESLA EVENT · TOP GEAR" top={CREDIT_TOP} show={[[F.legal, F.two]]} />

    <Sfx at={2} name="rewind" volume={0.3} />
    <Sfx at={RESUME} name="whoosh" volume={0.28} />
    <Sfx at={F.grip} name="whoosh" volume={0.38} />
    <Sfx at={F.grip + 2} name="form" volume={0.32} />
    <Sfx at={T.fans - 2} name="riser" volume={0.22} dur={T.g2 - T.fans + 2} />
    <Sfx at={T.g2} name="thock" volume={0.65} />
    <Sfx at={T.tires} name="settle" volume={0.35} />
    <Sfx at={F.real} name="whoosh" volume={0.38} />
    <Sfx at={T.real - 2} name="thock" volume={0.55} />
    <Sfx at={F.spec} name="whoosh" volume={0.38} />
    <Sfx at={T.spectacle - 2} name="thock" volume={0.6} />
    <Sfx at={T.seconds - 2} name="tick_run" volume={0.3} dur={60} />
    <Sfx at={T.hours} name="settle" volume={0.35} />
    <Sfx at={F.legal} name="whoosh" volume={0.38} />
    <Sfx at={T.most - 2} name="hiss" volume={0.3} dur={40} />
    <Sfx at={T.isnt} name="thock" volume={0.7} />
    <Sfx at={F.spacex} name="whoosh" volume={0.38} />
    <Sfx at={T.tanks - 6} name="form" volume={0.3} />
    <Sfx at={T.tanks + 6} name="form" volume={0.3} />
    <Sfx at={T.test - 2} name="form" volume={0.3} />
    <Sfx at={F.two} name="whoosh" volume={0.36} />
    <Sfx at={T.two - 2} name="form" volume={0.34} />
    <Sfx at={T.brilliant - 10} name="whoosh" volume={0.3} />
    <Sfx at={T.and3 - 4} name="whoosh" volume={0.3} />
    <Sfx at={T.rocket - 6} name="hiss" volume={0.42} dur={50} />
    <Sfx at={F.final} name="whoosh" volume={0.36} />
    <Sfx at={T.impressive} name="riser" volume={0.2} dur={T.fall - T.impressive} />
    <Sfx at={T.fall - 2} name="thock" volume={0.75} />
    <Sfx at={T.fall + 14} name="settle" volume={0.4} />
  </AbsoluteFill>
);
