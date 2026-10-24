import type React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { CLAMP, EASE_OUT } from "../../lib/anim";
import { BG_NIGHT, C, ClipScene, HEADC, Headline, keyline, MONO, pop, Sfx, slowPush, Tag } from "../kit";
import { Disclose, HoldStill, M, Shade, TeslaCredit } from "./fx";
import { cue, segFrames } from "./util";

// Roadster film S2 "The jets". Facts: TESLA_ROADSTER_FACTS.md §4 (two COPVs based on Falcon hardware, 600 L, about
// 250 kg of air; 10 nozzles = 4 rear + 4 corner pointing down + 2 front for yaw; valves from Optimus, "micro adjustments
// within a fraction of a second"; rear nozzles "over 80 kN", "roughly the same thrust as a fighter jet"; supersonic
// exhaust with Mach diamonds). Tesla footage: kick_side_slow, kick_close_slow, ramp_overhead_slow. Our 3D: blender_xray,
// blender_drop.
const D = segFrames("S2");
const T = {
  second: cue("S2", "second"), gas: cue("S2", "gas"), tanks: cue("S2", "tanks"), spacex: cue("S2", "spacex"), quarter: cue("S2", "quarter"),
  it: cue("S2", "it", 3), ten: cue("S2", "10"), up: cue("S2", "up", 2), down: cue("S2", "down,"), side: cue("S2", "sideways"),
  fraction: cue("S2", "fraction"), rear: cue("S2", "rear"), n80: cue("S2", "80"), fighter: cue("S2", "fighter"),
  faster: cue("S2", "faster"), diamond: cue("S2", "diamond"), so: cue("S2", "so", 2), rocket: cue("S2", "rocket", 2), nothing: cue("S2", "nothing"),
  falling: cue("S2", "falling"), landing: cue("S2", "landing"),
};
const X = { xray: T.gas - 6, hold: T.gas - 6 + 180, map: T.it, thrust: T.rear - 6, sound: T.faster - 26, rocket: T.so };

const Opening: React.FC = () => {
  const frame = useCurrentFrame();
  if (frame >= X.xray) return null;
  return (
    <AbsoluteFill>
      <Shade from="left" strength={0.7} />
      <Headline at={T.second - 4} left={M} top={230} lines={[{ text: "A SECOND MACHINE", size: 140 }, { text: "HIDDEN INSIDE", size: 140, color: C.acid }]} />
    </AbsoluteFill>
  );
};

const Tanks: React.FC = () => {
  const frame = useCurrentFrame();
  if (frame < X.xray || frame >= X.map) return null;
  return (
    <AbsoluteFill>
      <Shade from="left" strength={0.6} />
      <Tag at={T.tanks} left={M} top={170} bg={C.acid} size={72}>TWO CARBON-WRAPPED TANKS</Tag>
      <Tag at={T.spacex} left={M} top={290} bg={C.ink} size={56}>THE KIND SPACEX FLIES ON FALCON</Tag>
      <Tag at={T.quarter} left={M} top={760} bg={C.cyan} size={110} rot={[-8, -2]}>≈250 KG OF GAS</Tag>
    </AbsoluteFill>
  );
};

// the ten nozzles, top view: 4 rear (thrust), 4 corners pointing down (lift), 2 front (yaw)
const NOZ: { x: number; y: number; kind: "rear" | "corner" | "front" }[] = [
  { x: 690, y: 470, kind: "rear" }, { x: 690, y: 530, kind: "rear" }, { x: 690, y: 590, kind: "rear" }, { x: 690, y: 650, kind: "rear" },
  { x: 800, y: 405, kind: "corner" }, { x: 800, y: 715, kind: "corner" }, { x: 1250, y: 405, kind: "corner" }, { x: 1250, y: 715, kind: "corner" },
  { x: 1390, y: 470, kind: "front" }, { x: 1390, y: 650, kind: "front" },
];
const KCOL = { rear: C.cyan, corner: C.magenta, front: C.acid };

const NozzleMap: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < X.map || frame >= X.thrust) return null;
  const lit = (i: number) => frame >= T.ten + i * 6;
  const count = NOZ.filter((_, i) => lit(i)).length;
  const arrow = (at: number) => interpolate(frame, [at, at + 10], [0, 1], { ...CLAMP, easing: EASE_OUT });
  const aUp = arrow(T.up), aDown = arrow(T.down), aSide = arrow(T.side);
  const valves = pop(frame, T.fraction, fps, 220, 11);
  return (
    <AbsoluteFill style={{ background: BG_NIGHT, scale: slowPush(frame, X.map, X.thrust, 1.04), transformOrigin: "55% 55%" }}>
      <Headline at={X.map + 2} left={M} top={70} lines={[{ text: "WHERE THE GAS COMES OUT", size: 96 }]} />
      <svg width={1920} height={1080} style={{ position: "absolute", inset: 0 }}>
        {/* car, top view */}
        <rect x={720} y={380} width={660} height={360} rx={150} fill="#1E2230" stroke={C.ink} strokeWidth={8} />
        <rect x={930} y={440} width={240} height={240} rx={60} fill="#11141B" stroke="#59606E" strokeWidth={5} />
        <text x={1050} y={575} textAnchor="middle" fill="#8C93A3" fontFamily="Archivo" fontWeight={900} fontSize={34}>FRONT →</text>
        {NOZ.map((n, i) => (
          <g key={i} opacity={lit(i) ? 1 : 0.25}>
            <circle cx={n.x} cy={n.y} r={22} fill={lit(i) ? KCOL[n.kind] : "#59606E"} stroke="#000" strokeWidth={5} />
            {n.kind === "rear" && lit(i) ? <path d={`M ${n.x - 26} ${n.y} L ${n.x - 120} ${n.y - 18} L ${n.x - 120} ${n.y + 18} Z`} fill={C.cyan} opacity={0.75} /> : null}
          </g>
        ))}
        {/* forces on a corner and the nose */}
        <g opacity={aUp}><line x1={800} y1={850} x2={800} y2={850 - 120 * aUp} stroke={C.magenta} strokeWidth={18} /><path d="M 782 735 L 800 705 L 818 735 Z" fill={C.magenta} /></g>
        <g opacity={aDown}><line x1={1250} y1={250} x2={1250} y2={250 + 110 * aDown} stroke={C.magenta} strokeWidth={18} /><path d="M 1232 360 L 1250 390 L 1268 360 Z" fill={C.magenta} /></g>
        <g opacity={aSide}><line x1={1420} y1={560} x2={1420 + 150 * aSide} y2={560} stroke={C.acid} strokeWidth={18} /><path d={`M ${1570 * 1} 542 L ${1600} 560 L ${1570} 578 Z`} fill={C.acid} /></g>
      </svg>
      <div style={{ position: "absolute", left: M, top: 300 }}>
        <div style={{ ...HEADC, fontSize: 220, color: C.ink, fontVariantNumeric: "tabular-nums", ...keyline(1.4, 11) }}>{count}</div>
        <div style={{ ...HEADC, fontSize: 70, color: C.ink, ...keyline(0.5, 8) }}>NOZZLES</div>
      </div>
      <div style={{ position: "absolute", left: M, top: 640, ...MONO, fontSize: 36, lineHeight: 1.5, color: C.ink, opacity: count >= 10 ? 1 : 0 }}>
        <span style={{ color: C.cyan }}>●</span> 4 REAR: THRUST<br /><span style={{ color: C.magenta }}>●</span> 4 CORNERS: POINT DOWN<br />
        <span style={{ color: C.acid }}>●</span> 2 FRONT: STEER
      </div>
      <div style={{ position: "absolute", right: M, bottom: 120, textAlign: "right", opacity: interpolate(valves, [0, 0.3], [0, 1], CLAMP),
        translate: `0 ${(1 - valves) * 30}px` }}>
        <div style={{ ...HEADC, fontSize: 84, color: C.acid, ...keyline(0.6, 9) }}>IN A FRACTION OF A SECOND</div>
        <div style={{ ...MONO, fontSize: 32, color: "#D2CBE3", marginTop: 8 }}>VALVES BORROWED FROM TESLA&apos;S OPTIMUS ROBOT</div>
      </div>
    </AbsoluteFill>
  );
};

const Thrust: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < X.thrust || frame >= X.sound) return null;
  const n = pop(frame, T.n80, fps, 230, 10);
  return (
    <AbsoluteFill>
      <Shade from="left" strength={0.75} />
      <div style={{ position: "absolute", left: M, top: 160 }}>
        <div style={{ ...HEADC, fontSize: 70, color: C.ink, ...keyline(0.5, 8) }}>THE FOUR REAR NOZZLES ALONE</div>
        <div style={{ ...HEADC, fontSize: 300, color: C.acid, lineHeight: 0.9, scale: interpolate(n, [0, 1], [1.4, 1]), opacity: interpolate(n, [0, 0.25], [0, 1], CLAMP),
          transformOrigin: "0% 50%", ...keyline(2, 12) }}>&gt;80 kN</div>
      </div>
      <Tag at={T.fighter} left={M} top={720} bg={C.ink} size={70}>≈ A FIGHTER JET&apos;S PUSH</Tag>
      {frame >= T.fighter ? <div style={{ position: "absolute", left: M + 6, top: 830, ...MONO, fontSize: 32, color: C.ink }}>TESLA&apos;S ENGINEERS&apos; COMPARISON</div> : null}
    </AbsoluteFill>
  );
};

// supersonic exhaust: a row of shock diamonds drawn beside the 3D jets
const Sound: React.FC = () => {
  const frame = useCurrentFrame();
  if (frame < X.sound || frame >= X.rocket) return null;
  const d = interpolate(frame, [T.diamond - 10, T.diamond + 20], [0, 1], { ...CLAMP, easing: EASE_OUT });
  return (
    <AbsoluteFill>
      <Shade from="left" strength={0.6} />
      <Headline at={T.faster} left={M} top={170} lines={[{ text: "FASTER THAN SOUND", size: 130, color: C.acid }]} />
      <svg width={1920} height={1080} style={{ position: "absolute", inset: 0, opacity: d }}>
        <rect x={M} y={560} width={60} height={90} fill="#8C93A3" stroke="#000" strokeWidth={4} />
        <path d={`M ${M + 60} 575 L ${M + 60 + 900 * d} 590 L ${M + 60 + 900 * d} 620 L ${M + 60} 635 Z`} fill={C.cyan} opacity={0.25} />
        {Array.from({ length: 6 }).map((_, i) => {
          const cx = M + 150 + i * 145;
          const show = d * 6 > i;
          return show ? <path key={i} d={`M ${cx - 60} 605 L ${cx} 575 L ${cx + 60} 605 L ${cx} 635 Z`} fill="none" stroke={C.cyan} strokeWidth={6} /> : null;
        })}
      </svg>
      <div style={{ position: "absolute", left: M, top: 690, ...HEADC, fontSize: 70, color: C.cyan, opacity: d, ...keyline(0.5, 8) }}>SHOCK DIAMONDS, LIKE BEHIND A ROCKET</div>
    </AbsoluteFill>
  );
};

const Payoff: React.FC = () => {
  const frame = useCurrentFrame();
  if (frame < X.rocket) return null;
  const turn = interpolate(frame, [T.landing - 4, T.landing + 8], [0, 1], CLAMP);
  return (
    <AbsoluteFill>
      <Shade from="left" strength={0.7} />
      <Headline at={T.rocket} left={M} top={190} lines={[{ text: "A ROCKET ENGINE", size: 130 }, { text: "WITH NOTHING BURNING", size: 130, color: C.acid }]} />
      <div style={{ position: "absolute", left: M, top: 560, ...HEADC, fontSize: 96, color: C.ink, opacity: interpolate(frame, [T.falling, T.falling + 8], [0, 1], CLAMP),
        ...keyline(0.7, 10) }}>
        FALLING <span style={{ color: C.warn, opacity: 1 - turn }}>✕</span> → <span style={{ color: C.cyan, opacity: turn }}>LANDING</span>
      </div>
    </AbsoluteFill>
  );
};

export const S2Jets: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: C.black }}>
    <ClipScene src="film/kick_side_slow.mp4" from={0} dur={X.xray} trimBefore={60} push={[1, 1.05]} origin="55% 40%" />
    <ClipScene src="film/blender_xray.mp4" from={X.xray} dur={180} push={[1, 1.03]} />
    <HoldStill src="film/blender_xray_last.png" from={X.hold} dur={X.map - X.hold} push={[1.03, 1.06]} />
    <ClipScene src="film/kick_close_slow.mp4" from={X.thrust} dur={X.sound - X.thrust} trimBefore={30} push={[1, 1.05]} origin="60% 50%" />
    <ClipScene src="film/blender_drop.mp4" from={X.sound} dur={Math.min(150, X.rocket - X.sound)} push={[1, 1.04]} />
    <ClipScene src="film/ramp_overhead_slow.mp4" from={X.rocket} dur={D - X.rocket} trimBefore={40} push={[1, 1.05]} />
    <Opening />
    <Tanks />
    <NozzleMap />
    <Thrust />
    <Sound />
    <Payoff />
    <Disclose show={[[X.xray, X.map], [X.sound, X.rocket]]} />
    <TeslaCredit show={[[0, X.xray], [X.thrust, X.sound], [X.rocket, D]]} />
    <Sfx at={X.xray} name="whoosh" volume={0.35} />
    <Sfx at={T.quarter} name="thock" volume={0.5} />
    <Sfx at={X.map} name="whoosh" volume={0.35} />
    <Sfx at={T.ten} name="tick_run" volume={0.25} dur={60} />
    <Sfx at={X.thrust} name="hiss" volume={0.5} dur={90} />
    <Sfx at={T.n80} name="thock" volume={0.6} />
    <Sfx at={X.sound} name="whoosh" volume={0.35} />
    <Sfx at={X.rocket} name="whoosh" volume={0.35} />
  </AbsoluteFill>
);
