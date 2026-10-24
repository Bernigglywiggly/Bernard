import { Video } from "@remotion/media";
import type React from "react";
import { AbsoluteFill, Easing, interpolate, Sequence, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { CLAMP, EASE_IN_OUT, EASE_OUT } from "../../lib/anim";
import { BG_NIGHT, C, Credit, HEADC, keyline, MONO, pop, Sfx, Stamp, Tag } from "../kit";
import { cue } from "./util";

// Roadster film, segment S5 ("The fan car", 38.6 s). A camera travels one long night track that is also the timeline:
// the 1978 Brabham BT46B, back to 1970 for the Chaparral 2J, a whip past the decades to the 2025 McMurtry Spéirling on
// its rig. On "So" a lineup board sums it up (fan suction: all four; let go and land: only 2026), then the camera
// pushes into the 2026 car hanging from its ceiling and cuts on the drop to our own Blender illustration
// (public/film/blender_drop.mp4, slowed 2x with RIFE into s5_drop_2x.mp4, labelled "3D ILLUSTRATION").
// Every car is drawn for this film: generic silhouettes, no liveries, no logos.
// Facts: TESLA_ROADSTER_FACTS.md §13.2 (BT46B raced once and won, Swedish GP 17 Jun 1978, declared as engine cooling,
// withdrawn; 2J 1970 Can-Am, 4 entries 0 wins, two fans on a separate two-stroke engine, banned after the 1970 season;
// Spéirling twin fans, 2,000 kg of downforce at 0 mph, drove upside down on a rotating rig, Apr 2025).

const S = "S5";
const Q = {
  y1978: cue(S, "1978"), formula: cue(S, "Formula"), giant: cue(S, "giant"), won: cue(S, "won"), said: cue(S, "said"),
  cool: cue(S, "cool"), sucking: cue(S, "sucking"), withdrew: cue(S, "withdrew"), never: cue(S, "never"),
  eight: cue(S, "Eight"), american: cue(S, "American"), two: cue(S, "two"), separate: cue(S, "separate"),
  nothing: cue(S, "nothing"), banned: cue(S, "banned"), y2025: cue(S, "2025"), british: cue(S, "British"),
  fans2: cue(S, "fans", 2), drive: cue(S, "drive"), upside: cue(S, "upside"), rotating: cue(S, "rotating"),
  so: cue(S, "So"), invent: cue(S, "invent"), added: cue(S, "added"), where: cue(S, "where"), lets: cue(S, "lets"),
  lands: cue(S, "lands"),
};

// ------------------------------------------------------------------------------------------------ shared drawing kit
// (exported: S6 and S7 draw the same Roadster, fans, arrows and jets)
export const GREY = "#C3CAD2";
export const BODY = "#F2F3F5";
export const BODY2 = "#DCE0E5";
export const TYRE = "#23272E";
export const RIM = "#B9C2CC";
export const GLASS = "#3B4A61";
export const STEEL = "#8F99A3";
export const DARK = "#3A414B";
export const WS: React.CSSProperties = { wordSpacing: "0.14em" }; // Archivo condensed caps need a wider word space
const SK = 5; // body outline width

export const Wheel: React.FC<{ x: number; y: number; r: number; angle?: number }> = ({ x, y, r, angle = 0 }) => (
  <g transform={`translate(${x} ${y})`}>
    <circle r={r} fill={TYRE} stroke={C.black} strokeWidth={SK} />
    <circle r={r * 0.62} fill={RIM} stroke={C.black} strokeWidth={4} />
    <g transform={`rotate(${angle})`}>
      {[0, 72, 144, 216, 288].map((a) => (
        <rect key={a} x={-r * 0.075} y={-r * 0.58} width={r * 0.15} height={r * 0.44} rx={r * 0.05} fill="#6E7782" transform={`rotate(${a})`} />
      ))}
    </g>
    <circle r={r * 0.17} fill="#6E7782" stroke={C.black} strokeWidth={3} />
  </g>
);

// A fan seen at an angle (squash < 1 = facing backwards, seen from the side). Blades smear when it spins fast.
export const Fan: React.FC<{ x: number; y: number; r: number; angle: number; speed?: number; squash?: number; blades?: number; dim?: boolean }> = ({
  x, y, r, angle, speed = 0, squash = 1, blades = 5, dim = false,
}) => {
  const blade = `M 0 0 C ${r * 0.3} ${-r * 0.28}, ${r * 0.3} ${-r * 0.7}, ${r * 0.06} ${-r * 0.86} C ${-r * 0.14} ${-r * 0.6}, ${-r * 0.22} ${-r * 0.3}, 0 0 Z`;
  const set = (off: number, op: number) => (
    <g transform={`rotate(${angle - off})`} opacity={op}>
      {Array.from({ length: blades }).map((_, i) => (
        <path key={i} d={blade} fill={dim ? "#6FB7B2" : C.cyan} transform={`rotate(${(i * 360) / blades})`} />
      ))}
    </g>
  );
  const smear = Math.min(1, speed / 24);
  return (
    <g transform={`translate(${x} ${y}) scale(${squash} 1)`}>
      <circle r={r} fill="#0B1A20" stroke={C.black} strokeWidth={SK / squash} />
      <circle r={r - 7} fill="none" stroke={dim ? "#4E8F8B" : C.cyan} strokeWidth={6 / squash} opacity={0.9} />
      {smear > 0.05 ? set(speed * 0.66, 0.22 * smear) : null}
      {smear > 0.05 ? set(speed * 0.33, 0.4 * smear) : null}
      {set(0, 1 - 0.25 * smear)}
      <circle r={r * 0.17} fill={dim ? "#4E8F8B" : C.cyan} stroke={C.black} strokeWidth={3 / squash} />
    </g>
  );
};

export const Arrow: React.FC<{ x: number; y1: number; y2: number; p: number; color: string; w: number; head?: number }> = ({ x, y1, y2, p, color, w, head = 40 }) => {
  if (p <= 0.001) return null;
  const y = y1 + (y2 - y1) * p;
  const dir = Math.sign(y2 - y1);
  return (
    <g>
      <line x1={x} y1={y1} x2={x} y2={y - dir * head * 0.6} stroke={C.black} strokeWidth={w + 10} strokeLinecap="round" />
      <line x1={x} y1={y1} x2={x} y2={y - dir * head * 0.6} stroke={color} strokeWidth={w} strokeLinecap="round" />
      <polygon points={`${x},${y} ${x - head * 0.62},${y - dir * head} ${x + head * 0.62},${y - dir * head}`} fill={color} stroke={C.black} strokeWidth={5} strokeLinejoin="round" />
    </g>
  );
};

// A cold-gas jet: a cone that widens and fades along its length, with shock diamonds near the nozzle. From (x, y)
// along `deg` (0 = straight down in local space). `seed` keeps each jet's gradient id unique.
export const Jet: React.FC<{ x: number; y: number; len: number; w: number; deg?: number; frame: number; seed?: number; op?: number }> = ({
  x, y, len, w, deg = 0, frame, seed = 0, op = 1,
}) => {
  if (op <= 0.01 || len <= 2) return null;
  const flick = 1 + 0.06 * Math.sin(frame * 1.7 + seed * 2.1) + 0.04 * Math.sin(frame * 3.1 + seed);
  const L = len * flick;
  const id = `jet-g-${seed}`;
  const diamonds = [0.1, 0.22, 0.34, 0.46].filter((d) => d * L < L - 10);
  return (
    <g transform={`translate(${x} ${y}) rotate(${deg})`} opacity={op}>
      <defs>
        <linearGradient id={id} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#E9FFFD" stopOpacity={0.95} />
          <stop offset="35%" stopColor={C.cyan} stopOpacity={0.55} />
          <stop offset="100%" stopColor={C.cyan} stopOpacity={0} />
        </linearGradient>
      </defs>
      <polygon points={`${-w * 0.36},0 ${w * 0.36},0 ${w * 1.7},${L} ${-w * 1.7},${L}`} fill={`url(#${id})`} opacity={0.45} />
      <polygon points={`${-w * 0.3},0 ${w * 0.3},0 ${w * 0.75},${L * 0.8} ${-w * 0.75},${L * 0.8}`} fill={`url(#${id})`} />
      {diamonds.map((d, i) => (
        <polygon key={i} points={`0,${d * L - w * 0.4} ${w * 0.24},${d * L} 0,${d * L + w * 0.4} ${-w * 0.24},${d * L}`} fill={C.ink} opacity={0.95 - i * 0.18} />
      ))}
    </g>
  );
};

// The 2026 Roadster, drawn for this film (a generic two-seat shape, not a trace). Local units: ground y = 0, nose +x,
// about 1,000 long; wheels r 74 at x = 316 and -306; rear nozzle at (-500, -64).
export const ROADSTER_NOZZLE = { x: -500, y: -64 };
export const Roadster: React.FC<{ wheelAngle?: number; body?: number; tint?: string }> = ({ wheelAngle = 0, body = 0, tint = BODY }) => (
  <g>
    <g transform={`translate(0 ${body})`}>
      <path d="M 486 -40 C 504 -46, 510 -72, 498 -88 C 470 -120, 400 -150, 318 -164 C 250 -174, 190 -178, 140 -182 C 80 -222, 20 -246, -60 -250 C -140 -254, -200 -246, -250 -230 C -330 -204, -420 -178, -476 -158 C -496 -150, -504 -136, -502 -118 L -500 -48 C -498 -40, -490 -38, -476 -38 L -392 -38 A 86 86 0 0 1 -220 -38 L 230 -38 A 86 86 0 0 1 402 -38 Z"
        fill={tint} stroke={C.black} strokeWidth={SK} strokeLinejoin="round" />
      <path d="M 120 -186 C 72 -218, 22 -236, -46 -238 C -104 -240, -146 -232, -176 -218 L -166 -198 L 106 -180 Z" fill={GLASS} stroke={C.black} strokeWidth={4} strokeLinejoin="round" />
      <path d="M 60 -206 C 20 -222, -30 -228, -100 -228" fill="none" stroke="#7F93AE" strokeWidth={5} strokeLinecap="round" />
      <path d="M 472 -102 C 300 -114, -200 -124, -490 -132" fill="none" stroke={GREY} strokeWidth={3} />
      <path d="M -184 -196 C -178 -160, -174 -100, -178 -52" fill="none" stroke={GREY} strokeWidth={2.5} />
      <rect x={-220} y={-52} width={450} height={14} fill="#2A2F36" />
      <path d="M 497 -92 C 482 -104, 456 -112, 428 -116" fill="none" stroke={C.cyan} strokeWidth={8} strokeLinecap="round" />
      <path d="M -501 -128 L -476 -146" fill="none" stroke={C.warn} strokeWidth={8} strokeLinecap="round" />
      <ellipse cx={ROADSTER_NOZZLE.x + 2} cy={ROADSTER_NOZZLE.y} rx={7} ry={12} fill="#11141A" />
    </g>
    <Wheel x={316} y={-74} r={74} angle={wheelAngle} />
    <Wheel x={-306} y={-74} r={74} angle={wheelAngle} />
  </g>
);

// Integral of a speed curve (deg per frame): how far a fan or wheel has turned by `frame`.
export const spin = (frame: number, speed: (f: number) => number) => {
  let a = 0;
  for (let i = 0; i < frame; i++) a += speed(i);
  return a;
};

// ------------------------------------------------------------------------------------------------ the other cars
// Brabham BT46B: open wheels (front r 74, rear r 88), one big fan in a shroud at the tail, skirts between the wheels.
const BT46B: React.FC<{ fan: number; fanSpeed: number; squat?: number }> = ({ fan, fanSpeed, squat = 0 }) => (
  <g>
    <g transform={`translate(0 ${squat})`}>
      <rect x={-606} y={-222} width={176} height={184} rx={22} fill={DARK} stroke={C.black} strokeWidth={SK} />
      <path d="M 612 -38 C 606 -28, 596 -26, 578 -26 L -420 -26 L -440 -40 L -440 -126 L -300 -134 L -160 -156 L -100 -186 L -60 -186 L -30 -156 L -10 -122 L 150 -124 L 178 -128 L 200 -100 L 250 -86 L 380 -66 L 520 -50 Z"
        fill={BODY} stroke={C.black} strokeWidth={SK} strokeLinejoin="round" />
      <path d="M 612 -38 L 520 -50 L 380 -66 L 250 -86 L 250 -66 L 380 -48 L 520 -38 Z" fill={C.warn} />
      <path d="M -30 -156 L -60 -186 L -100 -186 L -160 -156 L -300 -134 L -440 -126 L -440 -104 L -300 -112 L -160 -132 L -30 -132 Z" fill={C.warn} />
      <path d="M 150 -26 L 150 -82 L -240 -90 L -290 -74 L -290 -26 Z" fill={BODY2} stroke={C.black} strokeWidth={3} strokeLinejoin="round" />
      <circle cx={62} cy={-140} r={28} fill={BODY} stroke={C.black} strokeWidth={4} />
      <path d="M 66 -148 L 90 -148 L 90 -133 L 70 -131 Z" fill={GLASS} stroke={C.black} strokeWidth={3} strokeLinejoin="round" />
      <path d="M 36 -157 C 50 -170, 74 -170, 88 -157" fill="none" stroke={C.cyan} strokeWidth={5} />
      <rect x={470} y={-36} width={152} height={12} fill={DARK} stroke={C.black} strokeWidth={3} />
      <path d="M 576 -78 L 614 -78 L 618 -20 L 576 -20 Z" fill={DARK} stroke={C.black} strokeWidth={3} strokeLinejoin="round" />
      <rect x={-248} y={-26} width={530} height={26} fill={C.magenta} stroke={C.black} strokeWidth={4} />
      <line x1={250} y1={-66} x2={356} y2={-74} stroke={C.black} strokeWidth={6} />
      <line x1={250} y1={-38} x2={356} y2={-74} stroke={C.black} strokeWidth={6} />
      <line x1={-240} y1={-70} x2={-336} y2={-88} stroke={C.black} strokeWidth={6} />
      <Fan x={-518} y={-130} r={88} angle={fan} speed={fanSpeed} squash={0.56} blades={6} />
    </g>
    <Wheel x={356} y={-74} r={74} />
    <Wheel x={-336} y={-88} r={88} />
  </g>
);

// Chaparral 2J: enclosed wheels (r 86 / 90), slab sides, a tall rear box with two fans on its back face.
const BODY_2J = "M 604 -40 L 612 -96 L 540 -122 L 440 -176 L 330 -168 L 250 -154 L 176 -208 L 80 -214 L 44 -228 L -570 -236 L -594 -222 L -598 -46 L -572 -38 L -428 -38 A 98 98 0 0 1 -232 -38 L 302 -38 A 98 98 0 0 1 498 -38 Z";
const Chaparral2J: React.FC<{ fan: number; fanSpeed: number; xray: number; belt: number }> = ({ fan, fanSpeed, xray, belt }) => (
  <g>
    <defs>
      <clipPath id="s5-2j"><path d={BODY_2J} /></clipPath>
    </defs>
    <Wheel x={400} y={-86} r={86} />
    <Wheel x={-330} y={-90} r={90} />
    <path d={BODY_2J} fill={BODY} stroke={C.black} strokeWidth={SK} strokeLinejoin="round" />
    <path d="M 250 -154 L 176 -208 L 136 -208 L 196 -154 Z" fill={GLASS} stroke={C.black} strokeWidth={3} strokeLinejoin="round" />
    <circle cx={100} cy={-226} r={23} fill={BODY} stroke={C.black} strokeWidth={4} />
    <path d="M 104 -234 L 122 -234 L 122 -221 L 106 -219 Z" fill={GLASS} />
    <line x1={-560} y1={-96} x2={590} y2={-90} stroke={GREY} strokeWidth={3} />
    <line x1={20} y1={-222} x2={14} y2={-40} stroke={GREY} strokeWidth={2.5} />
    {/* x-ray: the rear box opens to show the little engine that drives the fans */}
    <g clipPath="url(#s5-2j)" opacity={xray}>
      <rect x={-596} y={-236} width={360} height={198} fill="#0B0F17" />
      <rect x={-444} y={-196} width={132} height={82} rx={8} fill="#5E6670" stroke={C.acid} strokeWidth={6} />
      {[0, 1, 2, 3, 4].map((i) => <line key={i} x1={-436} y1={-184 + i * 14} x2={-320} y2={-184 + i * 14} stroke="#2A2F36" strokeWidth={4} />)}
      <circle cx={-458} cy={-155} r={18} fill={STEEL} stroke={C.black} strokeWidth={3} />
      <line x1={-458} y1={-173} x2={-592} y2={-158} stroke={C.acid} strokeWidth={6} strokeDasharray="14 10" strokeDashoffset={-belt} />
      <line x1={-458} y1={-137} x2={-592} y2={-112} stroke={C.acid} strokeWidth={6} strokeDasharray="14 10" strokeDashoffset={belt} />
    </g>
    <path d={BODY_2J} fill="none" stroke={C.black} strokeWidth={SK} strokeLinejoin="round" />
    <rect x={-232} y={-38} width={534} height={38} fill={C.magenta} stroke={C.black} strokeWidth={4} />
    <rect x={498} y={-38} width={106} height={38} fill={C.magenta} stroke={C.black} strokeWidth={4} />
    <rect x={-572} y={-38} width={144} height={38} fill={C.magenta} stroke={C.black} strokeWidth={4} />
    <Fan x={-582} y={-148} r={64} angle={fan + 30} speed={fanSpeed} squash={0.5} blades={5} dim />
    <Fan x={-606} y={-134} r={64} angle={fan} speed={fanSpeed} squash={0.5} blades={5} />
  </g>
);

// McMurtry Spéirling: tiny, bubble canopy, two fans at the tail. Wheels r 62 / 64.
const Speirling: React.FC<{ fan: number; fanSpeed: number; wheel: number }> = ({ fan, fanSpeed, wheel }) => (
  <g>
    <Wheel x={232} y={-62} r={62} angle={wheel} />
    <Wheel x={-224} y={-64} r={64} angle={wheel} />
    <path d="M 346 -32 L 354 -66 L 300 -96 L 200 -118 L 118 -128 L -146 -160 L -250 -144 L -338 -126 L -352 -46 L -332 -32 L -298 -32 A 74 74 0 0 1 -150 -32 L 158 -32 A 74 74 0 0 1 306 -32 Z"
      fill={BODY} stroke={C.black} strokeWidth={SK} strokeLinejoin="round" />
    <path d="M 130 -128 C 100 -196, -56 -224, -152 -160 Z" fill={GLASS} stroke={C.black} strokeWidth={4} strokeLinejoin="round" />
    <path d="M 74 -164 C 44 -186, -6 -194, -60 -188" fill="none" stroke="#7F93AE" strokeWidth={4} strokeLinecap="round" />
    <path d="M 330 -76 L -336 -84" fill="none" stroke={C.cyan} strokeWidth={6} />
    <Fan x={-340} y={-104} r={44} angle={fan + 40} speed={fanSpeed} squash={0.5} blades={5} dim />
    <Fan x={-358} y={-92} r={44} angle={fan} speed={fanSpeed} squash={0.5} blades={5} />
  </g>
);

// A chequered flag on a pole; the cloth waves more towards its free end.
const Flag: React.FC<{ x: number; ground: number; frame: number; up: number }> = ({ x, ground, frame, up }) => {
  if (up <= 0.01) return null;
  const top = ground - 300 * up;
  const cols = 5;
  const rows = 4;
  const cw = 22;
  const ch = 22;
  const wave = (i: number) => 9 * Math.sin(frame * 0.32 - i * 0.9) * (i / cols);
  const cells: React.ReactNode[] = [];
  for (let i = 0; i < cols; i++) {
    for (let j = 0; j < rows; j++) {
      const x0 = x + 6 + i * cw;
      const x1 = x0 + cw;
      const pts = `${x0},${top + j * ch + wave(i)} ${x1},${top + j * ch + wave(i + 1)} ${x1},${top + (j + 1) * ch + wave(i + 1)} ${x0},${top + (j + 1) * ch + wave(i)}`;
      cells.push(<polygon key={`${i}-${j}`} points={pts} fill={(i + j) % 2 === 0 ? BODY : "#111"} />);
    }
  }
  return (
    <g>
      <line x1={x} y1={ground} x2={x} y2={top - 6} stroke={GREY} strokeWidth={8} />
      {cells}
      <polyline points={`${x + 6},${top} ${x + 6 + cols * cw},${top + wave(cols)} ${x + 6 + cols * cw},${top + rows * ch + wave(cols)} ${x + 6},${top + rows * ch}`}
        fill="none" stroke={C.black} strokeWidth={3} />
    </g>
  );
};

// Air thrown out of the back of a fan: streamlines that fade with distance.
const Plume: React.FC<{ x: number; y: number; frame: number; speed: number; spread?: number; id: string }> = ({ x, y, frame, speed, spread = 1, id }) => {
  const k = Math.min(1, speed / 14);
  if (k <= 0.02) return null;
  return (
    <g opacity={k}>
      <defs>
        <linearGradient id={id} gradientUnits="userSpaceOnUse" x1={x} y1={0} x2={x - 420} y2={0}>
          <stop offset="0%" stopColor={C.cyan} stopOpacity={0.95} /><stop offset="100%" stopColor={C.cyan} stopOpacity={0} />
        </linearGradient>
      </defs>
      {[-78, -40, 0, 40, 78].map((dy, i) => (
        <path key={dy} d={`M ${x} ${y + dy * 0.55} C ${x - 120} ${y + dy * 0.75 * spread}, ${x - 240} ${y + dy * 1.05 * spread}, ${x - 420} ${y + dy * 1.6 * spread}`}
          fill="none" stroke={`url(#${id})`} strokeWidth={i === 2 ? 8 : 6} strokeLinecap="round" strokeDasharray="56 34" strokeDashoffset={frame * 16 + i * 23} />
      ))}
    </g>
  );
};

// ------------------------------------------------------------------------------------------------ world + camera
const GROUND = 880;
const K = 1.2; // world scale of the cars
const X = { c70: 0, b78: 2200, m25: 5200 };
const NUM_P = 0.92; // year numerals sit on a far wall, so they slide a little slower than the cars
const RULER_P = 1.25; // the timeline ruler is in the foreground
const FAR_P = 0.35;

type Cam = { x: number; y: number; z: number };
type Key = Cam & { f: number; e?: (t: number) => number };
const SINE = Easing.inOut(Easing.sin);
const FAN78 = { x: X.b78 - 960 + 960 - 518 * K, y: GROUND - 130 * K };
const KEYS: Key[] = [
  { f: 0, x: 2160, y: 540, z: 1 },
  { f: Q.giant - 8, x: 2200, y: 540, z: 1.03, e: SINE },
  { f: Q.giant + 22, x: FAN78.x + 560, y: 548, z: 1.15 },
  { f: Q.won - 10, x: FAN78.x + 570, y: 548, z: 1.165, e: SINE },
  { f: Q.won + 14, x: 2230, y: 540, z: 1 },
  { f: Q.sucking - 20, x: 2235, y: 540, z: 1.02, e: SINE },
  { f: Q.sucking + 14, x: 2170, y: 580, z: 1.06 },
  { f: Q.withdrew - 14, x: 2172, y: 580, z: 1.065, e: SINE },
  { f: Q.withdrew + 6, x: 2190, y: 540, z: 1 },
  { f: Q.eight - 3, x: 2190, y: 540, z: 1.035, e: SINE },
  { f: Q.eight + 34, x: -20, y: 540, z: 1 },
  { f: Q.separate - 10, x: 10, y: 540, z: 1.03, e: SINE },
  { f: Q.separate + 14, x: -90, y: 552, z: 1.12 },
  { f: Q.nothing - 14, x: -84, y: 552, z: 1.13, e: SINE },
  { f: Q.nothing + 6, x: -10, y: 540, z: 1 },
  { f: Q.y2025 - 14, x: -10, y: 540, z: 1.03, e: SINE },
  { f: Q.y2025 + 34, x: 5200, y: 540, z: 1 },
  { f: Q.drive, x: 5196, y: 540, z: 1.02, e: SINE },
  { f: Q.so, x: 5196, y: 548, z: 1.04, e: SINE },
  { f: Q.so + 14, x: 5196, y: 548, z: 0.5, e: Easing.in(Easing.cubic) },
];
const DIPS: [number, number, number][] = [[Q.eight - 3, Q.eight + 34, 0.1], [Q.y2025 - 14, Q.y2025 + 34, 0.16]];
const HITS = [Q.withdrew + 2, Q.banned + 2];
const CUT = Q.so + 14; // world -> lineup board

const camAt = (f: number): Cam => {
  let c: Cam = KEYS[KEYS.length - 1];
  if (f <= KEYS[0].f) c = KEYS[0];
  for (let i = 1; i < KEYS.length; i++) {
    const a = KEYS[i - 1];
    const b = KEYS[i];
    if (f > a.f && f <= b.f) {
      const t = (b.e ?? EASE_IN_OUT)((f - a.f) / (b.f - a.f));
      c = { x: a.x + (b.x - a.x) * t, y: a.y + (b.y - a.y) * t, z: Math.exp(Math.log(a.z) + (Math.log(b.z) - Math.log(a.z)) * t) };
      break;
    }
  }
  let z = c.z;
  for (const [a, b, d] of DIPS) if (f > a && f < b) z *= 1 - d * Math.sin((Math.PI * (f - a)) / (b - a));
  let shake = 0;
  for (const h of HITS) if (f >= h && f < h + 12) shake += 7 * Math.exp(-(f - h) / 3) * Math.sin((f - h) * 2.4);
  return { x: c.x + shake, y: c.y + shake * 0.6, z };
};

// A layer at depth p (1 = the cars): it slides p times as far and zooms less the further back it sits.
const layer = (cam: Cam, p: number): React.CSSProperties => {
  const z = cam.z >= 1 ? 1 + (cam.z - 1) * p : cam.z;
  const cy = 540 + (cam.y - 540) * p;
  return {
    position: "absolute", left: 0, top: 0, width: 10, height: 10, transformOrigin: "0px 0px",
    translate: `${960 - cam.x * p * z}px ${540 - cy * z}px`, scale: String(z),
  };
};

// A station: children are laid out in 1920x1080 "rest" coordinates (what the screen shows when the camera is home).
const Station: React.FC<{ x: number; cam: Cam; children: React.ReactNode }> = ({ x, cam, children }) => {
  if (Math.abs(cam.x - x) > 960 / cam.z + 1300) return null;
  return <div style={{ position: "absolute", left: x - 960, top: 0, width: 1920, height: 1080 }}>{children}</div>;
};

const Svg: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <svg width={1920} height={1080} viewBox="0 0 1920 1080" style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }}>{children}</svg>
);

const ease = (frame: number, a: number, b: number) => interpolate(frame, [a, b], [0, 1], { ...CLAMP, easing: EASE_OUT });

// Year numerals on the far wall.
const Numeral: React.FC<{ text: string; x: number; frame: number; punchAt?: number; fps: number }> = ({ text, x, frame, punchAt, fps }) => {
  const p = punchAt === undefined ? 0 : pop(frame, punchAt, fps, 260, 10);
  const s = punchAt !== undefined && frame >= punchAt ? interpolate(p, [0, 1], [1.12, 1]) : 1;
  return (
    <div style={{ position: "absolute", left: x * NUM_P - 960 + 146, top: 86, ...HEADC, fontSize: 262, color: C.acid, lineHeight: 0.86,
      scale: String(s), transformOrigin: "0% 100%", ...keyline(2, 10) }}>{text}</div>
  );
};

const Name: React.FC<{ at: number; name: string; sub: string; extra?: string; frame: number; fps: number; size?: number }> = ({ at, name, sub, extra, frame, fps, size = 96 }) => {
  if (frame < at) return null;
  const a = pop(frame, at, fps, 200, 15);
  const b = pop(frame, at + 5, fps, 200, 15);
  const c = pop(frame, at + 10, fps, 200, 15);
  return (
    <div style={{ position: "absolute", left: 150, top: 318 }}>
      <div style={{ ...HEADC, ...WS, fontSize: size, color: C.ink, opacity: interpolate(a, [0, 0.3], [0, 1], CLAMP), translate: `0 ${(1 - a) * 36}px`, ...keyline(size / 150, 10) }}>{name}</div>
      <div style={{ ...HEADC, ...WS, fontSize: 54, color: C.cyan, marginTop: 12, opacity: interpolate(b, [0, 0.3], [0, 1], CLAMP), translate: `0 ${(1 - b) * 30}px`, ...keyline(0.36, 8) }}>{sub}</div>
      {extra ? <div style={{ ...MONO, fontSize: 44, color: C.ink, marginTop: 10, opacity: interpolate(c, [0, 0.3], [0, 1], CLAMP), translate: `0 ${(1 - c) * 24}px` }}>{extra}</div> : null}
    </div>
  );
};

const Label: React.FC<{ at: number; until?: number; left: number; top: number; size: number; color: string; children: React.ReactNode; frame: number; fps: number; mono?: boolean }> = ({
  at, until = Infinity, left, top, size, color, children, frame, fps, mono,
}) => {
  if (frame < at || frame >= until) return null;
  const s = pop(frame, at, fps, 220, 14);
  return (
    <div style={{ position: "absolute", left, top, ...(mono ? { ...MONO, fontSize: size } : { ...HEADC, ...WS, fontSize: size, ...keyline(size / 150, 9) }), color,
      opacity: interpolate(s, [0, 0.3], [0, 1], CLAMP), translate: `${(1 - s) * -30}px 0` }}>{children}</div>
  );
};

// A thin leader line that draws itself from the label to the part.
const Leader: React.FC<{ pts: [number, number][]; p: number; color?: string }> = ({ pts, p, color = C.ink }) => {
  if (p <= 0.01) return null;
  const d = pts.map(([x, y], i) => `${i === 0 ? "M" : "L"} ${x} ${y}`).join(" ");
  let len = 0;
  for (let i = 1; i < pts.length; i++) len += Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]);
  return (
    <g>
      <path d={d} fill="none" stroke={C.black} strokeWidth={11} strokeLinecap="round" strokeLinejoin="round" strokeDasharray={len} strokeDashoffset={len * (1 - p)} />
      <path d={d} fill="none" stroke={color} strokeWidth={5} strokeLinecap="round" strokeLinejoin="round" strokeDasharray={len} strokeDashoffset={len * (1 - p)} />
      {p > 0.98 ? <circle cx={pts[pts.length - 1][0]} cy={pts[pts.length - 1][1]} r={9} fill={color} stroke={C.black} strokeWidth={4} /> : null}
    </g>
  );
};

// ------------------------------------------------------------------------------------------------ the stations
const CX = 960; // car centre in station coordinates
const Station78: React.FC<{ frame: number; fps: number; fan: number; fanSpeed: number }> = ({ frame, fps, fan, fanSpeed }) => {
  const suck = ease(frame, Q.sucking, Q.sucking + 14);
  const arrowsOut = interpolate(frame, [Q.withdrew - 6, Q.withdrew + 4], [1, 0], CLAMP);
  const flag = spring({ frame: frame - (Q.won - 2), fps, config: { damping: 13, stiffness: 160 } });
  const fx = CX - 518 * K;
  const fy = GROUND - 130 * K;
  return (
    <>
      <Svg>
        <ellipse cx={CX} cy={GROUND} rx={820} ry={74} fill="url(#s5-pool)" />
        <Flag x={1742} ground={GROUND} frame={frame} up={flag} />
        <Plume x={fx - 40} y={fy} frame={frame} speed={fanSpeed} id="s5-pl78" />
        {/* air pulled from under the floor to the fan */}
        <path d={`M ${CX + 340 * K} ${GROUND - 13} L ${CX - 400 * K} ${GROUND - 13} C ${CX - 450 * K} ${GROUND - 13}, ${CX - 470 * K} ${GROUND - 40}, ${fx + 20} ${fy + 50}`}
          fill="none" stroke={C.cyan} strokeWidth={7} strokeDasharray="34 24" strokeDashoffset={frame * 9} opacity={suck} />
        <g transform={`translate(${CX} ${GROUND}) scale(${K})`}><BT46B fan={fan} fanSpeed={fanSpeed} squat={7 * suck} /></g>
        <g opacity={arrowsOut}>
          {[1190, 1335, 1480].map((ax, i) => (
            <Arrow key={ax} x={ax} y1={560} y2={676} p={ease(frame, Q.sucking + 2 + i * 3, Q.sucking + 16 + i * 3)} color={C.cyan} w={16} />
          ))}
        </g>
        <Leader pts={[[320, 586], [fx - 8, fy - 92]]} p={frame < Q.said ? ease(frame, Q.giant + 8, Q.giant + 16) : 0} />
      </Svg>
      <Name at={Q.formula - 6} name="BRABHAM BT46B" sub="FORMULA 1 FAN CAR" frame={frame} fps={fps} />
      <Label at={Q.giant + 2} until={Q.said} left={156} top={506} size={78} color={C.ink} frame={frame} fps={fps}>GIANT FAN</Label>
      <Label at={Q.said + 2} left={158} top={496} size={44} color={C.cyan} frame={frame} fps={fps} mono>BRABHAM&apos;S STORY:</Label>
      <Label at={Q.cool - 6} left={156} top={548} size={64} color={C.ink} frame={frame} fps={fps}>ENGINE COOLING</Label>
      <Label at={Q.sucking + 2} left={752} top={548} size={64} color={C.acid} frame={frame} fps={fps}>+ SUCTION</Label>
      <Tag at={Q.won} until={Q.never} left={1130} top={150} bg={C.acid} size={66} style={WS}>WON ON DEBUT</Tag>
      <Tag at={Q.never} left={1130} top={150} bg={C.acid} size={66} rot={[6, -2]} style={WS}>WON ITS ONLY RACE</Tag>
      <Label at={Q.won + 8} left={1136} top={254} size={44} color={C.ink} frame={frame} fps={fps} mono>SWEDISH GRAND PRIX</Label>
      <Label at={Q.won + 12} left={1136} top={306} size={44} color={C.ink} frame={frame} fps={fps} mono>17 JUNE 1978</Label>
      <Stamp at={Q.withdrew} left={1140} top={384} size={94} rot={-6}>WITHDRAWN</Stamp>
    </>
  );
};

const Station70: React.FC<{ frame: number; fps: number; fan: number; fanSpeed: number }> = ({ frame, fps, fan, fanSpeed }) => {
  const xray = ease(frame, Q.separate - 4, Q.separate + 8);
  const row = (at: number) => pop(frame, at, fps, 220, 14);
  const r1 = row(Q.nothing - 8);
  const r2 = row(Q.nothing);
  const fx = CX - 606 * K;
  const fy = GROUND - 134 * K;
  const ex = CX - 378 * K;
  const ey = GROUND - 196 * K;
  return (
    <>
      <Svg>
        <ellipse cx={CX} cy={GROUND} rx={820} ry={74} fill="url(#s5-pool)" />
        <Plume x={fx - 30} y={fy} frame={frame} speed={fanSpeed} id="s5-pl70" />
        <g transform={`translate(${CX} ${GROUND}) scale(${K})`}><Chaparral2J fan={fan} fanSpeed={fanSpeed} xray={xray} belt={frame * 6} /></g>
        <Leader pts={[[330, 574], [fx + 10, fy - 84]]} p={ease(frame, Q.two + 4, Q.two + 12)} />
        <Leader pts={[[640, 578], [ex, ey + 4]]} p={ease(frame, Q.separate + 6, Q.separate + 14)} color={C.acid} />
      </Svg>
      <Name at={Q.american - 4} name="CHAPARRAL 2J" sub="CAN-AM, USA" frame={frame} fps={fps} />
      <Label at={Q.two} left={156} top={496} size={78} color={C.ink} frame={frame} fps={fps}>TWO FANS</Label>
      <Label at={Q.separate} left={582} top={446} size={44} color={C.ink} frame={frame} fps={fps} mono>DRIVEN BY A SEPARATE</Label>
      <Label at={Q.separate + 4} left={580} top={508} size={68} color={C.acid} frame={frame} fps={fps}>2-STROKE ENGINE</Label>
      {frame >= Q.nothing - 8 ? (
        <div style={{ position: "absolute", left: 1130, top: 128, width: 560 }}>
          {[{ k: r1, label: "ENTRIES", v: "4", c: C.ink }, { k: r2, label: "WINS", v: "0", c: C.warn }].map((r, i) => (
            <div key={r.label} style={{ position: "absolute", left: 0, top: i * 112, width: 560, display: "flex", justifyContent: "space-between", alignItems: "baseline",
              opacity: interpolate(r.k, [0, 0.3], [0, 1], CLAMP), translate: `${(1 - r.k) * 40}px 0` }}>
              <span style={{ ...HEADC, fontSize: 72, color: C.ink, ...keyline(0.48, 9) }}>{r.label}</span>
              <span style={{ ...HEADC, fontSize: 132, color: r.c, fontVariantNumeric: "tabular-nums", ...keyline(0.88, 10) }}>{r.v}</span>
            </div>
          ))}
        </div>
      ) : null}
      <Stamp at={Q.banned} left={1150} top={386} size={140} rot={-7}>BANNED</Stamp>
      <Label at={Q.banned + 8} left={1250} top={598} size={44} color={C.ink} frame={frame} fps={fps} mono>AFTER THE 1970 SEASON</Label>
    </>
  );
};

const HUB = { x: 1424, y: 500 };
const RIG_K = 0.95;
const Station25: React.FC<{ frame: number; fps: number; fan: number; fanSpeed: number }> = ({ frame, fps, fan, fanSpeed }) => {
  const rot = interpolate(frame, [Q.drive, Q.upside + 26], [0, 180], { ...CLAMP, easing: EASE_IN_OUT });
  const roll = interpolate(frame, [Q.upside + 30, Q.so + 10], [0, 150], { ...CLAMP, easing: Easing.inOut(Easing.quad) });
  const wheel = (roll / (2 * Math.PI * 62)) * 360;
  const arc = interpolate(frame, [Q.drive - 2, Q.drive + 6, Q.upside + 26, Q.upside + 40], [0, 1, 1, 0], CLAMP);
  const suck = Math.min(1, fanSpeed / 12);
  const legL = HUB.x - 130;
  const legR = HUB.x + 130;
  return (
    <>
      <Svg>
        <ellipse cx={HUB.x} cy={GROUND} rx={640} ry={66} fill="url(#s5-pool)" />
        {/* the rig's tower stands behind the platform */}
        {[0.28, 0.52, 0.76].map((k) => (
          <line key={k} x1={legL + (HUB.x - 16 - legL) * k} y1={GROUND + (HUB.y - GROUND) * k} x2={legR - (legR - HUB.x - 16) * k} y2={GROUND + (HUB.y - GROUND) * k}
            stroke={DARK} strokeWidth={10} />
        ))}
        <line x1={legL} y1={GROUND} x2={HUB.x - 16} y2={HUB.y} stroke={C.black} strokeWidth={30} strokeLinecap="round" />
        <line x1={legL} y1={GROUND} x2={HUB.x - 16} y2={HUB.y} stroke={DARK} strokeWidth={22} strokeLinecap="round" />
        <line x1={legR} y1={GROUND} x2={HUB.x + 16} y2={HUB.y} stroke={C.black} strokeWidth={30} strokeLinecap="round" />
        <line x1={legR} y1={GROUND} x2={HUB.x + 16} y2={HUB.y} stroke={DARK} strokeWidth={22} strokeLinecap="round" />
        <rect x={HUB.x - 180} y={GROUND - 18} width={360} height={18} fill={DARK} stroke={C.black} strokeWidth={4} />
        <g transform={`translate(${HUB.x} ${HUB.y}) rotate(${rot}) scale(${RIG_K})`}>
          <rect x={-390} y={-16} width={780} height={32} fill="#5E6670" stroke={C.black} strokeWidth={5} />
          <line x1={-370} y1={-9} x2={370} y2={-9} stroke={GREY} strokeWidth={4} strokeDasharray="40 30" />
          <g transform={`translate(${-20 + roll} -16)`}>
            {[-150, -40, 70, 180].map((ax, i) => (
              <Arrow key={ax} x={ax} y1={-210} y2={-110} p={suck * ease(frame, Q.fans2 - 10 + i * 2, Q.fans2 + 4 + i * 2)} color={C.cyan} w={10} head={26} />
            ))}
            <Speirling fan={fan} fanSpeed={fanSpeed} wheel={wheel} />
          </g>
        </g>
        <circle cx={HUB.x} cy={HUB.y} r={22} fill={STEEL} stroke={C.black} strokeWidth={5} />
        <g opacity={arc}>
          <path d={`M ${HUB.x + 70} ${HUB.y - 60} A 92 92 0 1 1 ${HUB.x - 84} ${HUB.y - 40}`} fill="none" stroke={C.black} strokeWidth={16} />
          <path d={`M ${HUB.x + 70} ${HUB.y - 60} A 92 92 0 1 1 ${HUB.x - 84} ${HUB.y - 40}`} fill="none" stroke={C.acid} strokeWidth={8} />
          <polygon points={`${HUB.x - 102},${HUB.y - 32} ${HUB.x - 70},${HUB.y - 56} ${HUB.x - 70},${HUB.y - 22}`} fill={C.acid} stroke={C.black} strokeWidth={4} />
        </g>
      </Svg>
      <Name at={Q.british - 2} name="McMURTRY SPÉIRLING" size={84} sub="BRITISH FAN CAR" extra="2,000 KG DOWNFORCE AT 0 MPH" frame={frame} fps={fps} />
      <Tag at={Q.upside} left={150} top={612} bg={C.acid} size={72} style={WS}>UPSIDE DOWN</Tag>
      <Label at={Q.rotating} left={156} top={728} size={64} color={C.ink} frame={frame} fps={fps}>ON A ROTATING RIG</Label>
    </>
  );
};

// ------------------------------------------------------------------------------------------------ track, ruler, far stand
const Track: React.FC<{ cam: Cam }> = ({ cam }) => {
  const x0 = Math.floor((cam.x - 960 / cam.z - 200) / 70) * 70;
  const x1 = cam.x + 960 / cam.z + 200;
  const kerbs: React.ReactNode[] = [];
  for (let x = x0; x < x1; x += 70) {
    kerbs.push(<rect key={x} x={x} y={GROUND} width={70} height={14} fill={Math.round(x / 70) % 2 === 0 ? C.warn : BODY} />);
  }
  return (
    <svg style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }} width={10} height={10}>
      <rect x={x0} y={GROUND} width={x1 - x0} height={600} fill="url(#s5-asphalt)" />
      {kerbs}
      <rect x={x0} y={GROUND} width={x1 - x0} height={14} fill="none" stroke={C.black} strokeWidth={3} />
      <line x1={x0} y1={GROUND - 1} x2={x1} y2={GROUND - 1} stroke={BODY} strokeOpacity={0.5} strokeWidth={2} />
    </svg>
  );
};

const RULER_MARKS: { x: number; label: string; big: boolean }[] = [
  { x: X.c70, label: "1970", big: true },
  ...[1, 2, 3, 4, 5, 6, 7].map((k) => ({ x: X.c70 + (k * (X.b78 - X.c70)) / 8, label: "", big: false })),
  { x: X.b78, label: "1978", big: true },
  { x: 3300, label: "1990", big: false }, { x: 3800, label: "2000", big: false }, { x: 4300, label: "2010", big: false },
  { x: X.m25, label: "2025", big: true },
];
const Ruler: React.FC<{ cam: Cam }> = ({ cam }) => {
  const y = 1004;
  const x0 = (cam.x - 960 / cam.z) * RULER_P - 400;
  const x1 = (cam.x + 960 / cam.z) * RULER_P + 400;
  const ticks: React.ReactNode[] = [];
  for (let x = Math.floor(x0 / 60) * 60; x < x1; x += 60) ticks.push(<line key={x} x1={x} y1={y} x2={x} y2={y + 12} stroke={C.ink} strokeOpacity={0.25} strokeWidth={3} />);
  const brk = (bx: number) => (
    <g key={bx}>
      <rect x={bx - 26} y={y - 30} width={52} height={60} fill="#06020E" />
      <line x1={bx - 22} y1={y + 26} x2={bx - 2} y2={y - 26} stroke={C.ink} strokeOpacity={0.7} strokeWidth={5} />
      <line x1={bx + 2} y1={y + 26} x2={bx + 22} y2={y - 26} stroke={C.ink} strokeOpacity={0.7} strokeWidth={5} />
    </g>
  );
  return (
    <svg style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }} width={10} height={10}>
      <line x1={x0} y1={y} x2={x1} y2={y} stroke={C.ink} strokeOpacity={0.45} strokeWidth={4} />
      {ticks}
      {RULER_MARKS.map((m) => (
        <g key={`${m.x}-${m.label}`}>
          <line x1={m.x * RULER_P} y1={y - (m.big ? 26 : 14)} x2={m.x * RULER_P} y2={y + (m.big ? 26 : 14)} stroke={m.big ? C.acid : C.ink} strokeOpacity={m.big ? 1 : 0.6} strokeWidth={m.big ? 8 : 4} />
          {m.label ? <text x={m.x * RULER_P + 16} y={y - 14} fill={m.big ? C.ink : "#9C93B3"} style={{ ...MONO, fontSize: 44 }}>{m.label}</text> : null}
        </g>
      ))}
      {brk(2850 * RULER_P)}
      {brk(4750 * RULER_P)}
    </svg>
  );
};

// A long grandstand behind the track, far back: it slides slowly and gives the pans their depth.
const FarStand: React.FC<{ cam: Cam }> = ({ cam }) => {
  const c = cam.x * FAR_P;
  const blocks: React.ReactNode[] = [];
  for (let x = Math.floor((c - 1700) / 900) * 900; x < c + 1700; x += 900) {
    const lights: React.ReactNode[] = [];
    for (let lx = x + 30; lx < x + 760; lx += 48) lights.push(<circle key={lx} cx={lx} cy={652} r={3.5} fill={C.ink} opacity={0.45} />);
    blocks.push(
      <g key={x}>
        <polygon points={`${x},${GROUND} ${x},700 ${x + 20},640 ${x + 780},640 ${x + 780},700 ${x + 760},${GROUND}`} fill="#170B33" />
        <polygon points={`${x + 40},${GROUND} ${x + 60},720 ${x + 740},720 ${x + 720},${GROUND}`} fill="#1E1040" />
        {[0, 1, 2, 3].map((r) => <line key={r} x1={x + 64 - r * 5} y1={746 + r * 34} x2={x + 736 + r * 5} y2={746 + r * 34} stroke="#2A1856" strokeWidth={3} />)}
        <rect x={x - 10} y={626} width={800} height={14} fill="#241247" />
        {lights}
        {[x + 120, x + 390, x + 660].map((px) => <line key={px} x1={px} y1={640} x2={px} y2={720} stroke="#241247" strokeWidth={8} />)}
      </g>,
    );
  }
  return (
    <div style={layer(cam, FAR_P)}>
      <svg style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }} width={10} height={10}>{blocks}</svg>
    </div>
  );
};

// ------------------------------------------------------------------------------------------------ lineup board
// On "So": the four cars side by side under our verdict, then two rows of marks. Then a push into the 2026 car.
const LX = [575, 960, 1312, 1648];
const LG = 610; // lineup ground
const P26 = { x: LX[3] - 10, y: 520 }; // where the push ends: the hanging 2026 car
const LineupScene: React.FC<{ frame: number; fps: number; fans: number[]; drop: number }> = ({ frame, fps, fans, drop }) => {
  const mark = (at: number, ok: boolean, x: number, y: number, acid: boolean, key: string) => {
    if (frame < at) return null;
    const s = pop(frame, at, fps, 260, 11);
    return (
      <div key={key} style={{ position: "absolute", left: x - 75, top: y, width: 150, textAlign: "center", ...HEADC, fontSize: 124, lineHeight: 1,
        color: ok ? (acid ? C.acid : C.cyan) : C.warn, scale: String(interpolate(s, [0, 1], [1.6, 1])), opacity: interpolate(s, [0, 0.25], [0, 1], CLAMP),
        ...keyline(0.75, 10) }}>{ok ? "✓" : "✕"}</div>
    );
  };
  const kerbs: React.ReactNode[] = [];
  for (let x = 0; x < 1920; x += 56) kerbs.push(<rect key={x} x={x} y={LG} width={56} height={11} fill={(x / 56) % 2 === 0 ? C.warn : BODY} />);
  const years = ["1970", "1978", "2025", "2026"];
  const row2 = interpolate(frame, [Q.added - 4, Q.added + 4], [0, 1], CLAMP);
  const h1 = pop(frame, Q.invent, fps, 200, 15);
  const h2 = pop(frame, Q.added, fps, 200, 15);
  const ramp = `M ${LX[3] + 168} ${LG} L ${LX[3] + 168} 512 A 46 46 0 0 0 ${LX[3] + 122} 466 L ${LX[3] - 178} 466`;
  return (
    <AbsoluteFill>
      <svg width={1920} height={1080} style={{ position: "absolute", inset: 0 }}>
        <rect x={0} y={LG} width={1920} height={470} fill="url(#s5-asphalt)" />
        {kerbs}
        {LX.map((x) => <ellipse key={x} cx={x} cy={LG} rx={200} ry={24} fill="url(#s5-pool)" />)}
        <g transform={`translate(${LX[0]} ${LG}) scale(0.3)`}><Chaparral2J fan={fans[0]} fanSpeed={20} xray={0} belt={0} /></g>
        <g transform={`translate(${LX[1]} ${LG}) scale(0.3)`}><BT46B fan={fans[1]} fanSpeed={20} /></g>
        {/* 2025: upside down under its rig */}
        <line x1={LX[2] - 44} y1={LG} x2={LX[2] - 4} y2={482} stroke={DARK} strokeWidth={11} />
        <line x1={LX[2] + 44} y1={LG} x2={LX[2] + 4} y2={482} stroke={DARK} strokeWidth={11} />
        <g transform={`translate(${LX[2]} 482) rotate(180) scale(0.4)`}>
          <rect x={-390} y={-16} width={780} height={32} fill="#5E6670" stroke={C.black} strokeWidth={6} />
          <g transform="translate(0 -16)"><Speirling fan={fans[2]} fanSpeed={20} wheel={0} /></g>
        </g>
        <circle cx={LX[2]} cy={482} r={10} fill={STEEL} stroke={C.black} strokeWidth={3} />
        {/* 2026: upside down under the top of its curled ramp */}
        <path d={ramp} fill="none" stroke={C.black} strokeWidth={24} />
        <path d={ramp} fill="none" stroke={STEEL} strokeWidth={16} />
        <g transform={`translate(${P26.x} ${474 + drop}) rotate(180) scale(0.3)`}><Roadster /></g>
      </svg>
      {frame >= Q.invent ? (
        <div style={{ position: "absolute", left: 150, top: 104, ...HEADC, fontSize: 104, color: C.ink, opacity: interpolate(h1, [0, 0.3], [0, 1], CLAMP),
          translate: `0 ${(1 - h1) * 36}px`, ...WS, ...keyline(0.7, 10) }}>THE VACUUM IS OLD.</div>
      ) : null}
      {frame >= Q.added ? (
        <div style={{ position: "absolute", left: 150, top: 214, ...HEADC, fontSize: 104, color: C.acid, opacity: interpolate(h2, [0, 0.3], [0, 1], CLAMP),
          translate: `0 ${(1 - h2) * 36}px`, ...WS, ...keyline(0.7, 10) }}>LETTING GO IS NEW.</div>
      ) : null}
      {years.map((y, i) => (
        <div key={y} style={{ position: "absolute", left: LX[i] - 130, top: 352, width: 260, textAlign: "center", ...HEADC, fontSize: 88,
          color: i === 3 ? C.acid : C.ink, ...keyline(0.6, 10) }}>{y}</div>
      ))}
      <div style={{ position: "absolute", left: 150, top: 706, ...HEADC, ...WS, fontSize: 52, color: C.cyan, ...keyline(0.36, 8) }}>FAN SUCTION</div>
      <div style={{ position: "absolute", left: 150, top: 856, ...HEADC, ...WS, fontSize: 52, color: C.acid, opacity: row2, ...keyline(0.36, 8) }}>LET GO + LAND</div>
      {LX.map((x, i) => mark(Q.invent + 4 + i * 6, true, x, 676, false, `a${i}`))}
      {LX.map((x, i) => mark(i < 3 ? Q.added + 4 + i * 5 : Q.where - 4, i === 3, x, 826, true, `b${i}`))}
    </AbsoluteFill>
  );
};

const Lineup: React.FC<{ frame: number; fps: number; fans: number[] }> = ({ frame, fps, fans }) => {
  if (frame < CUT || frame >= Q.lets - 1) return null;
  const settle = interpolate(frame, [CUT, CUT + 12], [1.1, 1], { ...CLAMP, easing: EASE_OUT });
  const t = interpolate(frame, [Q.where + 4, Q.lets - 1], [0, 1], { ...CLAMP, easing: Easing.in(Easing.quad) });
  const s = settle * Math.exp(Math.log(5.4) * t);
  const drop = interpolate(frame, [Q.lets - 12, Q.lets - 2], [0, 16], { ...CLAMP, easing: Easing.in(Easing.quad) });
  const tx = P26.x + (960 - P26.x) * t;
  const ty = P26.y + (540 - P26.y) * t;
  const copy = (k: number, op: number, key: string) => (
    <AbsoluteFill key={key} style={{ transformOrigin: "0px 0px", translate: `${tx - P26.x * s * k}px ${ty - P26.y * s * k}px`, scale: String(s * k), opacity: op }}>
      <LineupScene frame={frame} fps={fps} fans={fans} drop={drop} />
    </AbsoluteFill>
  );
  return (
    <AbsoluteFill>
      {t > 0.08 ? copy(0.9, 0.22 * t, "g2") : null}
      {t > 0.08 ? copy(0.95, 0.35 * t, "g1") : null}
      {copy(1, 1, "main")}
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ the 3D payoff
const DROP_FROM = 16; // first frame of s5_drop_2x.mp4 shown: the car is already falling (cut on action)
const Payoff: React.FC<{ frame: number; fps: number }> = ({ frame, fps }) => {
  const at = Q.lets - 1;
  if (frame < at) return null;
  const go = pop(frame, Q.lets + 2, fps, 200, 14);
  const land = pop(frame, Q.lands - 2, fps, 220, 12);
  return (
    <AbsoluteFill>
      <Sequence from={at} premountFor={fps}>
        <AbsoluteFill style={{ scale: String(interpolate(frame, [at, at + 100], [1.06, 1.0], CLAMP)) }}>
          <Video src={staticFile("film/s5_drop_2x.mp4")} muted trimBefore={DROP_FROM} objectFit="cover"
            style={{ width: "100%", height: "100%", filter: "hue-rotate(30deg) saturate(1.15) contrast(1.24) brightness(0.84)" }} />
        </AbsoluteFill>
      </Sequence>
      <AbsoluteFill style={{ background: "radial-gradient(ellipse at 60% 58%, rgba(20,5,46,0) 34%, rgba(10,4,24,0.72) 100%)" }} />
      <AbsoluteFill style={{ background: "linear-gradient(90deg, rgba(10,4,24,0.72) 0%, rgba(10,4,24,0.35) 34%, rgba(10,4,24,0) 55%)" }} />
      <Tag at={Q.lets - 1} left={110} top={150} bg={C.acid} size={60} style={WS}>TESLA&apos;S NEW PART</Tag>
      <div style={{ position: "absolute", left: 110, top: 262, ...HEADC, fontSize: 150, color: C.ink, opacity: interpolate(go, [0, 0.3], [0, 1], CLAMP),
        translate: `0 ${(1 - go) * 40}px`, ...WS, ...keyline(1, 11) }}>IT LETS GO</div>
      {frame >= Q.lands - 2 ? (
        <div style={{ position: "absolute", left: 110, top: 410, ...HEADC, opacity: interpolate(land, [0, 0.3], [0, 1], CLAMP), translate: `0 ${(1 - land) * 40}px` }}>
          <div style={{ fontSize: 150, color: C.acid, ...WS, ...keyline(1, 11) }}>AND LANDS</div>
          <div style={{ fontSize: 76, color: C.ink, marginTop: 8, ...WS, ...keyline(0.5, 9) }}>ON ITS WHEELS</div>
        </div>
      ) : null}
      <Credit text="3D ILLUSTRATION" show={[[at, 99999]]} top={930} />
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ the segment
export const S5FanCar: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const cam = camAt(frame);
  const prev = camAt(Math.max(0, frame - 1));
  const vx = Math.abs(cam.x - prev.x) * cam.z;
  const blur = Math.min(46, Math.max(0, vx - 6) * 0.3);
  const focus = Math.max(0, cam.z - 1.04) * 26; // rack focus: the far wall softens on push-ins

  // fan speeds (deg per frame) and the angles they integrate to
  const s78 = (f: number) => interpolate(f, [0, Q.giant - 4, Q.giant + 10], [9, 9, 23], CLAMP);
  const s70 = (f: number) => interpolate(f, [0, Q.two - 2, Q.two + 10], [5, 5, 21], CLAMP);
  const s25 = (f: number) => interpolate(f, [0, Q.fans2 - 6, Q.fans2 + 8], [6, 6, 22], CLAMP);
  const fan78 = spin(frame, s78);
  const fan70 = spin(frame, s70);
  const fan25 = spin(frame, s25);
  const blurStyle: React.CSSProperties = blur > 0.5 ? { filter: "url(#s5-mb)" } : {};

  return (
    <AbsoluteFill style={{ background: BG_NIGHT, overflow: "hidden" }}>
      <svg width={0} height={0} style={{ position: "absolute" }}>
        <defs>
          <filter id="s5-mb" x="-5%" y="-5%" width="110%" height="110%"><feGaussianBlur stdDeviation={`${blur.toFixed(1)} 0`} /></filter>
          <radialGradient id="s5-pool"><stop offset="0%" stopColor="#FFFFFF" stopOpacity={0.13} /><stop offset="100%" stopColor="#FFFFFF" stopOpacity={0} /></radialGradient>
          <linearGradient id="s5-asphalt" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor="#1A0D33" /><stop offset="45%" stopColor="#07030F" /><stop offset="100%" stopColor="#000" /></linearGradient>
        </defs>
      </svg>
      {frame < CUT ? (
        <AbsoluteFill style={blurStyle}>
          <AbsoluteFill style={{ filter: focus > 0.3 ? `blur(${focus.toFixed(1)}px)` : undefined }}>
            <FarStand cam={cam} />
            <div style={layer(cam, NUM_P)}>
              <Numeral text="1970" x={X.c70} frame={frame} fps={fps} />
              <Numeral text="1978" x={X.b78} frame={frame} fps={fps} punchAt={Q.y1978} />
              <Numeral text="2025" x={X.m25} frame={frame} fps={fps} punchAt={Q.y2025 + 30} />
            </div>
          </AbsoluteFill>
          <div style={layer(cam, 1)}>
            <Track cam={cam} />
            <Station x={X.c70} cam={cam}><Station70 frame={frame} fps={fps} fan={fan70} fanSpeed={s70(frame)} /></Station>
            <Station x={X.b78} cam={cam}><Station78 frame={frame} fps={fps} fan={fan78} fanSpeed={s78(frame)} /></Station>
            <Station x={X.m25} cam={cam}><Station25 frame={frame} fps={fps} fan={fan25} fanSpeed={s25(frame)} /></Station>
          </div>
          <div style={layer(cam, RULER_P)}><Ruler cam={cam} /></div>
        </AbsoluteFill>
      ) : null}
      <Lineup frame={frame} fps={fps} fans={[fan70, fan78, fan25, fan78 * 1.1]} />
      <Payoff frame={frame} fps={fps} />

      <Sfx at={Q.y1978} name="thock" volume={0.5} />
      <Sfx at={Q.giant} name="hiss" volume={0.3} dur={40} />
      <Sfx at={Q.won} name="form" volume={0.4} />
      <Sfx at={Q.sucking} name="hiss" volume={0.35} dur={45} />
      <Sfx at={Q.withdrew} name="thock" volume={0.65} />
      <Sfx at={Q.never} name="form" volume={0.35} />
      <Sfx at={Q.eight - 4} name="rewind" volume={0.45} />
      <Sfx at={Q.separate} name="form" volume={0.35} />
      <Sfx at={Q.nothing} name="thock" volume={0.45} />
      <Sfx at={Q.banned} name="thock" volume={0.7} />
      <Sfx at={Q.y2025 - 14} name="whoosh" volume={0.5} />
      <Sfx at={Q.drive} name="settle" volume={0.45} />
      <Sfx at={Q.so} name="whoosh" volume={0.4} />
      <Sfx at={Q.invent + 2} name="tick_run" volume={0.25} dur={22} />
      <Sfx at={Q.added + 2} name="tick_run" volume={0.2} dur={14} />
      <Sfx at={Q.where - 6} name="thock" volume={0.45} />
      <Sfx at={Q.where + 2} name="riser" volume={0.3} dur={22} />
      <Sfx at={Q.lets - 1} name="hiss" volume={0.55} dur={40} />
      <Sfx at={Q.lands - 4} name="thock" volume={0.75} />
    </AbsoluteFill>
  );
};
