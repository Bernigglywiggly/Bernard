import { Audio } from "@remotion/media";
import type React from "react";
import { AbsoluteFill, interpolate, Sequence, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { CLAMP, EASE_OUT } from "../lib/anim";
import { Bed, C, CaptionTrack, ClipScene, Credit, HEADC, keyline, MONO, pop, Sfx, Stamp, Tag } from "./kit";
import { makePages } from "./pager";
import { VO_S11 } from "./voS11Captions";

// Curve Short 11 (Thu 29 Oct 2026): "Touchscreen MacBook: Why It Took 16 Years" (branch T). 1080x1920, 30 fps.
// Script lab/curve_v2/shorts/short11.py; facts lab/research/APPLE_PRO_AND_TELL_FACTS.md. Pre-built by account B on Wed
// 28 Oct before Apple's 17:00 announcement: the timeline (rows 40-45), the capacitive grid (60-62) and the hinge torque
// (70-71) are ours and don't depend on the launch. Still to do after the launch (the 17:40 run): HOOK_CLIP and FIX_CLIP
// from Apple's own film, the x5 scene's words from Apple's press release (slots 103-104), the verdict rows checked
// against slot 104, HAS_VO with the real take. Scenes are cued by spoken words (cues: apple, work, bosses, no, sixteen,
// years, reaching, tires, under, grid, finger, changes, cross, but, hinge, top, twice, halfway, down, jobs, touch,
// quicker): a new take or a reworded line retimes them, and a missing cue word throws, so update T when a line changes.

const HAS_VO = false; // true once public/shorts/s11_vo.mp3 and the real voS11Captions.ts exist
const HOOK_CLIP: string | null = null; // e.g. "shorts/s11_touch.mp4": Apple's finger-on-screen shot (slot 108), credited
const LOOP_CLIP: string | null = null; // e.g. "shorts/s11_loop.mp4": HOOK_CLIP's first 30 frames reversed
const FIX_CLIP: string | null = null; // e.g. "shorts/s11_fix.mp4": Apple's film of the touch features (slot 104)

const PAGES = makePages(VO_S11);
const FPS = 30;
const bare = (s: string) => s.replace(/¶/g, "").trim().toLowerCase().replace(/[^a-z0-9%']/g, "");
const cue = (word: string, nth = 1, edge: "start" | "end" = "start") => {
  let seen = 0;
  for (const c of VO_S11) {
    if (bare(c.text) === word) {
      seen += 1;
      if (seen === nth) return Math.round(((edge === "start" ? c.startMs : c.endMs) / 1000) * FPS);
    }
  }
  throw new Error(`Short 11 cue: "${word}" #${nth} not found`);
};
const LAST_MS = VO_S11[VO_S11.length - 1].endMs;
const LOOP = 30; // the last second: back to frame 0's picture
export const SHORT11_FRAMES = Math.round((LAST_MS / 1000) * FPS) + 30 + LOOP;

const T = {
  apple: cue("apple"), work: cue("work"), bosses: cue("bosses"), no: cue("no"), sixteen: cue("sixteen"), years: cue("years"),
  reaching: cue("reaching"), tires: cue("tires"), under: cue("under"), grid: cue("grid"), finger: cue("finger"),
  changes: cue("changes"), cross: cue("cross"), but: cue("but"), hinge: cue("hinge"), top: cue("top"), twice: cue("twice"),
  halfway: cue("halfway"), down: cue("down", 1, "end"), jobs: cue("jobs"), touch: cue("touch"), quicker: cue("quicker"),
};
// the bed is 124 BPM and starts on a beat: scene cuts move onto the next kick
const BEAT = (FPS * 60) / 124;
const beatAfter = (f: number) => Math.round(Math.ceil(f / BEAT - 1e-6) * BEAT);
const S = {
  timeline: beatAfter(T.bosses - 6), arm: beatAfter(T.reaching - 4), grid: beatAfter(T.under - 4), hinge: beatAfter(T.but - 4),
  fix: beatAfter(T.down + 4), verdict: beatAfter(T.jobs - 4), loop: SHORT11_FRAMES - LOOP,
};
const DARK: React.CSSProperties = { position: "absolute", inset: 0, background: "radial-gradient(ellipse at 50% 40%, #1A1036 0%, #0A0718 55%, #020208 100%)" };
const SHADE_TOP: React.CSSProperties = { position: "absolute", left: 0, right: 0, top: 0, height: 900,
  background: "linear-gradient(180deg, rgba(2,2,10,0.9) 0%, rgba(2,2,10,0.6) 55%, rgba(2,2,10,0) 100%)" };
const between = (f: number, a: number, b: number) => f >= a && f < b;
const grow = (f: number, a: number, dur = 18) => interpolate(f, [a, a + dur], [0, 1], { ...CLAMP, easing: EASE_OUT });
const DIM = "#B8B2D6";
const SKIN = "#F2EEF8"; // our drawn hand and arm: a plain light glove, nobody's likeness
const Label: React.FC<{ children: React.ReactNode; left: number; top: number; size?: number; color?: string; opacity?: number;
  width?: number; align?: "left" | "center"; mono?: boolean }> = ({ children, left, top, size = 64, color = C.ink, opacity = 1, width, align = "left", mono }) => (
  <div style={{ position: "absolute", left, top, width, textAlign: align, ...(mono ? MONO : HEADC), whiteSpace: width ? "normal" : "nowrap", fontSize: size,
    lineHeight: 1, color, opacity, ...keyline(size / 140, 10) }}>{children}</div>
);
// a fingertip pointing up-left, its tip at (x, y): a capsule with a nail
const Finger: React.FC<{ x: number; y: number; s?: number; opacity?: number }> = ({ x, y, s = 1, opacity = 1 }) => (
  <g opacity={opacity} transform={`translate(${x} ${y}) scale(${s}) rotate(-35)`}>
    <rect x={-46} y={-6} width={92} height={460} rx={46} fill={SKIN} stroke={C.black} strokeWidth={7} />
    <rect x={-26} y={16} width={52} height={62} rx={20} fill="#D9D2EA" stroke={C.black} strokeWidth={4} />
  </g>
);

// ------------------------------------------------------------------------------------------------ x1: frame 0
const Kicker: React.FC<{ s?: number }> = ({ s = 1 }) => (
  <div style={{ position: "absolute", left: 60, top: 150, scale: s, transformOrigin: "0% 0%" }}>
    <Label left={0} top={0} size={84}>APPLE SAID NO</Label>
    <Label left={0} top={92} size={84} color={C.acid}>FOR 16 YEARS</Label>
  </div>
);
// our own drawing of a MacBook with a fingertip on the screen: the picture until Apple's film is in (and the fallback)
const HookDrawing: React.FC<{ t: number }> = ({ t }) => {
  const tx = 650;
  const ty = 860;
  const rings = [0, 12, 24].map((d) => ((t + d) % 36) / 36);
  return (
    <AbsoluteFill style={{ scale: interpolate(t, [0, 120], [1, 1.06], CLAMP), transformOrigin: "55% 45%" }}>
      <div style={DARK} />
      <svg width={1080} height={1920} style={{ position: "absolute", left: 0, top: 0 }}>
        <defs>
          <linearGradient id="s11scr" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0" stopColor="#2B1660" />
            <stop offset="1" stopColor="#0B0620" />
          </linearGradient>
        </defs>
        <rect x={90} y={520} width={900} height={600} rx={36} fill="#05030C" stroke="#D8D4EA" strokeWidth={8} />
        <rect x={122} y={552} width={836} height={536} rx={14} fill="url(#s11scr)" />
        <rect x={170} y={610} width={360} height={220} rx={12} fill="#3A2A70" opacity={0.8} />
        <rect x={560} y={650} width={340} height={300} rx={12} fill="#2C2058" opacity={0.8} />
        <rect x={470} y={526} width={140} height={22} rx={11} fill="#05030C" />
        <path d="M 40 1132 L 1040 1132 L 1000 1182 L 80 1182 Z" fill="#B9B4CC" stroke={C.black} strokeWidth={6} />
        {rings.map((p, i) => (
          <circle key={i} cx={tx} cy={ty} r={26 + 150 * p} fill="none" stroke={C.cyan} strokeWidth={6} opacity={(1 - p) * 0.9} />
        ))}
        <circle cx={tx} cy={ty} r={20} fill={C.cyan} />
        <Finger x={tx} y={ty} />
      </svg>
    </AbsoluteFill>
  );
};
const Hook: React.FC = () => {
  const frame = useCurrentFrame();
  if (frame >= S.timeline) return null;
  return (
    <AbsoluteFill>
      {HOOK_CLIP ? null : <HookDrawing t={frame} />}
      <div style={SHADE_TOP} />
      <Kicker />
      <Tag at={T.apple + 2} left={60} top={1210} bg={C.ink} size={44} rot={[-4, -2]}>STEVE JOBS · APPLE EVENT · 2010</Tag>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ x2: who said no, then the arm
const ROWS: [string, string, string][] = [
  ["2010", "STEVE JOBS", "APPLE EVENT"],
  ["2012", "TIM COOK", "EARNINGS CALL"],
  ["2014", "CRAIG FEDERIGHI", "CNET"],
  ["2018", "CRAIG FEDERIGHI", "WIRED"],
];
const Timeline: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (!between(frame, S.timeline, S.arm)) return null;
  const rowTop = (i: number) => 330 + i * 168;
  const line = grow(frame, S.timeline, Math.max(10, T.years - S.timeline));
  // the four NOs land between "no" and "sixteen"; 2026 lands on "years"
  const stampAt = (i: number) => Math.round(T.no + ((T.sixteen - T.no) * i) / 4);
  return (
    <AbsoluteFill style={{ scale: interpolate(frame, [S.timeline, S.arm], [1, 1.035], CLAMP) }}>
      <div style={DARK} />
      <Label left={60} top={170} size={72} color={C.acid}>WHO SAID NO</Label>
      <div style={{ position: "absolute", left: 40, top: rowTop(0) + 10, width: 8, height: (rowTop(4) - rowTop(0)) * line, backgroundColor: DIM }} />
      {ROWS.map(([yr, who, where], i) => {
        const at = S.timeline + 2 + i * 4;
        if (frame < at) return null;
        const s = pop(frame, at, fps, 230, 13);
        return (
          <div key={yr + where} style={{ position: "absolute", left: 0, top: rowTop(i), scale: interpolate(s, [0, 1], [0.9, 1]), opacity: s, transformOrigin: "0% 50%" }}>
            <Label left={64} top={0} size={84}>{yr}</Label>
            <Label left={310} top={2} size={52}>{who}</Label>
            <Label left={310} top={62} size={44} color={DIM} mono>{where}</Label>
          </div>
        );
      })}
      {ROWS.map(([yr, , where], i) => (
        <Stamp key={`no${yr}${where}`} at={stampAt(i)} left={820} top={rowTop(i) - 4} size={64} rot={-7}>NO</Stamp>
      ))}
      {frame >= T.years - 4 ? (
        <div style={{ position: "absolute", left: 0, top: rowTop(4), opacity: grow(frame, T.years - 4, 8) }}>
          <Label left={64} top={0} size={84} color={C.acid}>2026</Label>
          <Label left={310} top={2} size={52} color={C.acid}>APPLE</Label>
          <Label left={310} top={62} size={44} color={DIM} mono>MACBOOK PRO</Label>
        </div>
      ) : null}
      <Stamp at={T.years} left={800} top={rowTop(4) - 4} size={64} rot={-5} color={C.acid}>YES</Stamp>
    </AbsoluteFill>
  );
};
const Arm: React.FC = () => {
  const frame = useCurrentFrame();
  if (!between(frame, S.arm, S.grid)) return null;
  const sag = interpolate(frame, [T.tires, S.grid], [0, 16], { ...CLAMP, easing: EASE_OUT }); // degrees the arm sags as it tires
  const tired = grow(frame, T.reaching, Math.max(8, S.grid - T.reaching - 2));
  const rad = (d: number) => (d * Math.PI) / 180;
  const sh = { x: 250, y: 700 };
  const el = { x: sh.x + 300 * Math.cos(rad(8 + sag)), y: sh.y + 300 * Math.sin(rad(8 + sag)) };
  const hd = { x: el.x + 290 * Math.cos(rad(-10 + sag * 1.3)), y: el.y + 290 * Math.sin(rad(-10 + sag * 1.3)) };
  const barCol = tired < 0.6 ? C.acid : C.warn;
  return (
    <AbsoluteFill style={{ scale: interpolate(frame, [S.arm, S.grid], [1, 1.035], CLAMP) }}>
      <div style={DARK} />
      <Label left={60} top={170} size={84} color={C.warn}>GORILLA ARM</Label>
      <svg width={1080} height={1920} style={{ position: "absolute", left: 0, top: 0 }}>
        <rect x={860} y={380} width={46} height={700} rx={14} fill="#D8D4EA" stroke={C.black} strokeWidth={6} />
        <circle cx={sh.x - 30} cy={sh.y - 150} r={70} fill={SKIN} stroke={C.black} strokeWidth={7} />
        <line x1={sh.x - 20} y1={sh.y - 40} x2={sh.x - 50} y2={sh.y + 330} stroke={SKIN} strokeWidth={70} strokeLinecap="round" />
        <polyline points={`${sh.x},${sh.y} ${el.x},${el.y} ${hd.x},${hd.y}`} fill="none" stroke={C.black} strokeWidth={64} strokeLinecap="round" strokeLinejoin="round" />
        <polyline points={`${sh.x},${sh.y} ${el.x},${el.y} ${hd.x},${hd.y}`} fill="none" stroke={SKIN} strokeWidth={50} strokeLinecap="round" strokeLinejoin="round" />
      </svg>
      <Label left={60} top={1130} size={44} color={DIM} mono>YOUR ARM</Label>
      <div style={{ position: "absolute", left: 60, top: 1185, width: 860, height: 56, border: `5px solid ${C.ink}` }}>
        <div style={{ width: `${100 * tired}%`, height: "100%", backgroundColor: barCol }} />
      </div>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ x3: the capacitive grid
const G = { left: 120, top: 360, size: 840, n: 8 };
const gx = (i: number) => G.left + ((i + 0.5) * G.size) / G.n;
const gy = (j: number) => G.top + ((j + 0.5) * G.size) / G.n;
const HIT = { i: 5, j: 2 }; // the crossing under the finger: column 6, row 3
const Grid: React.FC = () => {
  const frame = useCurrentFrame();
  if (!between(frame, S.grid, S.hinge)) return null;
  const rows = grow(frame, S.grid + 2, 14);
  const cols = grow(frame, S.grid + 10, 14);
  const scanOn = between(frame, T.grid, T.finger - 2);
  const k = Math.floor((frame - T.grid) * 1.5) % (G.n * G.n);
  const fin = grow(frame, T.finger - 6, 10);
  const field = grow(frame, T.changes, 12);
  const hit = frame >= T.cross - 2;
  const pulse = ((frame - T.changes) % 24) / 24;
  return (
    <AbsoluteFill style={{ scale: interpolate(frame, [S.grid, S.hinge], [1, 1.035], CLAMP) }}>
      <div style={DARK} />
      <Label left={60} top={170} size={72}>HOW TOUCH WORKS</Label>
      <Label left={G.left} top={270} size={44} color={C.magenta}>ROWS SEND</Label>
      <Label left={G.left + 470} top={270} size={44} color={C.cyan}>COLUMNS LISTEN</Label>
      <svg width={1080} height={1920} style={{ position: "absolute", left: 0, top: 0 }}>
        <rect x={G.left} y={G.top} width={G.size} height={G.size} rx={18} fill="#0E0A22" stroke="#3A3460" strokeWidth={4} />
        {Array.from({ length: G.n }, (_, j) => (
          <line key={`r${j}`} x1={G.left + 20} y1={gy(j)} x2={G.left + 20 + (G.size - 40) * rows} y2={gy(j)} stroke={C.magenta}
            strokeWidth={hit && j === HIT.j ? 10 : 5} opacity={hit && j !== HIT.j ? 0.45 : 1} />
        ))}
        {Array.from({ length: G.n }, (_, i) => (
          <line key={`c${i}`} x1={gx(i)} y1={G.top + 20} x2={gx(i)} y2={G.top + 20 + (G.size - 40) * cols} stroke={C.cyan}
            strokeWidth={hit && i === HIT.i ? 10 : 5} opacity={hit && i !== HIT.i ? 0.45 : 1} />
        ))}
        {scanOn ? <circle cx={gx(k % G.n)} cy={gy(Math.floor(k / G.n))} r={18} fill={C.ink} opacity={0.9} /> : null}
        {field > 0
          ? [0, 1, 2].map((m) => {
              const p = (pulse + m / 3) % 1;
              return <circle key={m} cx={gx(HIT.i)} cy={gy(HIT.j)} r={20 + 90 * p} fill="none" stroke={C.acid} strokeWidth={6} opacity={(1 - p) * field} />;
            })
          : null}
        {hit ? <circle cx={gx(HIT.i)} cy={gy(HIT.j)} r={22} fill={C.acid} stroke={C.black} strokeWidth={4} /> : null}
        {fin > 0 ? <Finger x={gx(HIT.i) + 6} y={gy(HIT.j) + 8} s={interpolate(fin, [0, 1], [1.3, 0.8])} opacity={interpolate(fin, [0, 1], [0, 0.92])} /> : null}
      </svg>
      <Label left={gx(HIT.i) - 330} top={gy(HIT.j) - 120} size={64} color={C.acid} opacity={hit ? 1 : 0}>X 6 · Y 3</Label>
      <Tag at={T.changes + 4} left={60} top={1230} bg={C.cyan} size={44} rot={[-4, -2]}>PROJECTED CAPACITIVE TOUCH</Tag>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ x4: torque about the hinge
const P = { x: 330, y: 1040 }; // the hinge
const L = 680; // screen length from the hinge, px
const Hinge: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (!between(frame, S.hinge, S.fix)) return null;
  // a tap pushes the screen back (anticlockwise here), then it rings down; the top tap has twice the lever, twice the swing
  const ring = (at: number, amp: number) => (frame < at ? 0 : -amp * Math.exp(-(frame - at) / 10) * Math.sin(((frame - at) * 2 * Math.PI) / 11));
  const theta = -14 + ring(T.top, 7) + ring(T.halfway, 3.5);
  const arrow = (d: number, at: number, col: string) => {
    if (frame < at - 4) return null;
    const s = pop(frame, at - 4, fps, 240, 14);
    const y = P.y - d;
    return (
      <g opacity={Math.min(1, s)}>
        <line x1={P.x + 40 + 180 * s} y1={y} x2={P.x + 40} y2={y} stroke={col} strokeWidth={14} strokeLinecap="round" />
        <path d={`M ${P.x + 22} ${y} L ${P.x + 62} ${y - 24} L ${P.x + 62} ${y + 24} Z`} fill={col} />
        <line x1={P.x - 44} y1={P.y} x2={P.x - 44} y2={y} stroke={col} strokeWidth={6} strokeDasharray="14 10" />
      </g>
    );
  };
  const arc = (r: number, sweep: number, col: string, k: number) => {
    if (k <= 0) return null;
    const a0 = (-80 * Math.PI) / 180;
    const a1 = a0 - ((sweep * k) * Math.PI) / 180;
    const p0 = { x: P.x + r * Math.cos(a0), y: P.y + r * Math.sin(a0) };
    const p1 = { x: P.x + r * Math.cos(a1), y: P.y + r * Math.sin(a1) };
    return <path d={`M ${p0.x} ${p0.y} A ${r} ${r} 0 ${sweep * k > 180 ? 1 : 0} 0 ${p1.x} ${p1.y}`} fill="none" stroke={col} strokeWidth={12} strokeLinecap="round" />;
  };
  const big = grow(frame, T.top, 12);
  const small = grow(frame, T.halfway, 12);
  const hingeLit = frame >= T.hinge - 2;
  return (
    <AbsoluteFill style={{ scale: interpolate(frame, [S.hinge, S.fix], [1, 1.035], CLAMP) }}>
      <div style={DARK} />
      <Label left={60} top={170} size={60} opacity={grow(frame, T.top - 6, 10)}>TORQUE = FORCE × DISTANCE</Label>
      <svg width={1080} height={1920} style={{ position: "absolute", left: 0, top: 0 }}>
        <rect x={P.x - 30} y={P.y + 6} width={640} height={34} rx={12} fill="#B9B4CC" stroke={C.black} strokeWidth={6} />
        <g transform={`rotate(${theta} ${P.x} ${P.y})`}>
          <rect x={P.x - 14} y={P.y - L} width={28} height={L} rx={10} fill="#D8D4EA" stroke={C.black} strokeWidth={6} />
          {arrow(L - 30, T.top, C.acid)}
          {arrow(L / 2, T.halfway, C.cyan)}
        </g>
        {arc(130, 120, C.acid, big)}
        {arc(90, 60, C.cyan, small)}
        <circle cx={P.x} cy={P.y} r={hingeLit ? 30 : 22} fill={hingeLit ? C.acid : "#8A84A8"} stroke={C.black} strokeWidth={6} />
      </svg>
      <Label left={440} top={400} size={52} color={C.acid} opacity={big}>TAP AT THE TOP</Label>
      <Label left={440} top={466} size={84} color={C.acid} opacity={grow(frame, T.twice - 2, 8)}>2× THE TWIST</Label>
      <Label left={440} top={720} size={52} color={C.cyan} opacity={small}>HALFWAY DOWN</Label>
      <Label left={440} top={786} size={84} color={C.cyan} opacity={small}>1×</Label>
      <Label left={P.x + 60} top={P.y - 60} size={44} color={C.ink} opacity={hingeLit ? 1 : 0}>HINGE</Label>
      <Tag at={T.twice + 8} left={60} top={1230} bg={C.acid} size={44} rot={[-4, -2]}>OUR MATHS · 2× THE DISTANCE, 2× THE TWIST</Tag>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ x5: Apple's touch features (⏳)
const Fix: React.FC = () => {
  const frame = useCurrentFrame();
  if (!between(frame, S.fix, S.verdict)) return null;
  if (FIX_CLIP) return null; // the clip itself is placed in the root; its labels go here from Apple's own wording (slot 104)
  return (
    <AbsoluteFill>
      <div style={DARK} />
      <Label left={60} top={600} width={960} size={84} color={C.warn}>⏳ APPLE FILM: THE TOUCH FEATURES</Label>
      <Label left={60} top={820} width={960} size={44} color={C.warn} mono>PLACEHOLDER · THE 17:40 RUN REPLACES THIS SCENE</Label>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ x6: the verdict (⏳ slot 104)
const Verdict: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (!between(frame, S.verdict, S.loop)) return null;
  const rows: [string, string, string, number][] = [
    ["JOBS, 2010 →", "TIRED ARMS", C.warn, S.verdict + 2],
    ["APPLE, 2026 →", "TOUCH AS AN EXTRA", C.cyan, T.touch - 2],
    ["FOR WHEN IT’S", "QUICKER", C.acid, T.quicker - 4],
  ];
  return (
    <AbsoluteFill style={{ scale: interpolate(frame, [S.verdict, S.loop], [1, 1.03], CLAMP) }}>
      <div style={DARK} />
      {rows.map(([a, b, col, at], i) => (
        <div key={a} style={{ position: "absolute", left: 60, top: 260 + i * 220, opacity: frame >= at ? 1 : 0, scale: pop(frame, at, fps, 230, 12), transformOrigin: "0% 50%" }}>
          <Label left={0} top={0} size={60}>{a}</Label>
          <Label left={0} top={68} size={100} color={col}>{b}</Label>
        </div>
      ))}
    </AbsoluteFill>
  );
};

const LoopEnd: React.FC = () => {
  const frame = useCurrentFrame();
  if (frame < S.loop) return null;
  // eased, not sprung: the kicker must sit at exactly scale 1 on the last frame, as on frame 0
  const k = interpolate(frame, [S.loop + 14, S.loop + 24], [0, 1], { ...CLAMP, easing: EASE_OUT });
  return (
    <AbsoluteFill>
      {/* the drawing runs backwards into its frame 0 state, so the last frame is frame 0 */}
      {HOOK_CLIP ? null : <HookDrawing t={SHORT11_FRAMES - 1 - frame} />}
      <div style={{ ...SHADE_TOP, opacity: interpolate(frame, [S.loop, S.loop + 10], [0, 1], CLAMP) }} />
      {frame >= S.loop + 14 ? <Kicker s={interpolate(k, [0, 1], [1.25, 1])} /> : null}
    </AbsoluteFill>
  );
};

export const CurveV2Short11: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: C.black }}>
    {/* pictures: Apple's own film once it's in (frame 0, x5, the loop); our drawings carry the rest */}
    {HOOK_CLIP ? <ClipScene src={HOOK_CLIP} from={0} dur={S.timeline} push={[1, 1.08]} origin="55% 45%" /> : null}
    {FIX_CLIP ? <ClipScene src={FIX_CLIP} from={S.fix} dur={S.verdict - S.fix} push={[1.02, 1.07]} origin="50% 45%" /> : null}
    {LOOP_CLIP ? <ClipScene src={LOOP_CLIP} from={S.loop} dur={LOOP} push={[1.08, 1]} origin="55% 45%" /> : null}
    <Hook />
    <Timeline />
    <Arm />
    <Grid />
    <Hinge />
    <Fix />
    <Verdict />
    <LoopEnd />
    <CaptionTrack pages={PAGES} hide={[[0, 4], [S.loop, SHORT11_FRAMES]]} top={1360} />
    {HOOK_CLIP ? <Credit text="APPLE" show={[[0, S.timeline], [S.loop, SHORT11_FRAMES]]} /> : null}
    {FIX_CLIP ? <Credit text="APPLE" show={[[S.fix, S.verdict]]} /> : null}
    {HAS_VO ? <Sequence from={0}><Audio src={staticFile("shorts/s11_vo.mp3")} /></Sequence> : null}
    <Bed total={SHORT11_FRAMES} level={0.12} />
    <Sfx at={S.timeline} name="whoosh" volume={0.3} />
    <Sfx at={T.no} name="thock" volume={0.4} />
    <Sfx at={S.arm} name="whoosh" volume={0.3} />
    <Sfx at={S.grid} name="whoosh" volume={0.3} />
    <Sfx at={T.cross - 2} name="settle" volume={0.35} />
    <Sfx at={S.hinge} name="whoosh" volume={0.3} />
    <Sfx at={T.top - 2} name="thock" volume={0.45} />
    <Sfx at={S.fix} name="whoosh" volume={0.3} />
    <Sfx at={S.verdict} name="whoosh" volume={0.3} />
    <Sfx at={S.loop} name="rewind" volume={0.35} />
  </AbsoluteFill>
);
