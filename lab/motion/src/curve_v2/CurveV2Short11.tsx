import { Audio } from "@remotion/media";
import type React from "react";
import { AbsoluteFill, interpolate, Sequence, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { CLAMP, EASE_IN_OUT, EASE_OUT } from "../lib/anim";
import { Bed, C, CaptionTrack, ClipScene, Credit, HEADC, keyline, MONO, pop, Sfx, Stamp, Tag } from "./kit";
import { makePages } from "./pager";
import { VO_S11 } from "./voS11Captions";

// Curve Short 11 (Thu 29 Oct 2026): "Touchscreen MacBook: Why It Took 16 Years" (branch T). 1080x1920, 30 fps.
// Script lab/curve_v2/shorts/short11.py; facts lab/research/APPLE_PRO_AND_TELL_FACTS.md. Pre-built by account B on Wed
// 28 Oct before Apple's 17:00 announcement, then revised after an early critic pass (lab/curve_v2/shorts/out/critic_s11/
// scaffold_review.md, ledger.md): the timeline (rows 40, 43, 44), the capacitive grid (60-62) and the hinge torque (70-71)
// are ours and don't depend on the launch. Still to do after the launch (the 17:40 run): PRODUCT_2026 from slot 100,
// EXTRA_SOURCE from slot 104, HOOK_CLIP/LOOP_CLIP/FIX_CLIP from Apple's own film (add Short 8's CapScrim behind the
// captions if the footage is bright), the x5 scene from Apple's words (slots 103-104), HAS_VO with the real take. Jobs's
// words on screen are copied from two recordings of the 2010 event: lab/curve_v2/footage/apple_2026-10-28/JOBS_2010_QUOTE.md.
// 28 Oct ~18:00: launch filled in (Apple's film hnZI5uUSdEo for the hook, x5 and the loop; x5 labels in Apple's words).
// Scenes are cued by spoken words (apple, work, bosses, no, sixteen, years, reaching, tires, under, grid, finger, changes,
// cross, but, hangs, hinge, top, twice, halfway, down, hinge #2, pinch, swipe, drag, jobs, touch, reach, quicker): a new take retimes them, and a missing
// cue word throws, so update T when a line changes.

const HAS_VO = true; // true once public/shorts/s11_vo.mp3 and the real voS11Captions.ts exist
const HOOK_CLIP: string | null = "shorts/s11_touch.mp4"; // e.g. "shorts/s11_touch.mp4": Apple's finger-on-screen shot (slot 108), credited
const LOOP_CLIP: string | null = "shorts/s11_loop.mp4"; // e.g. "shorts/s11_loop.mp4": HOOK_CLIP's first 30 frames reversed
const FIX_CLIP: string | null = "shorts/s11_fix.mp4"; // e.g. "shorts/s11_fix.mp4": Apple's film of the touch features (slot 104)
const PRODUCT_2026 = "TOUCH ON MAC"; // slot 100: Apple's exact name for the touch model, 17 characters or fewer
const EXTRA_SOURCE = "APPLE, 2026 →"; // rows 24, 82 (REPORTED); "APPLE, 2026 →" only if slot 104 says touch is optional

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
  changes: cue("changes"), cross: cue("cross"), but: cue("but"), hangs: cue("hangs"), hinge: cue("hinge"), top: cue("top"),
  twice: cue("twice"), halfway: cue("halfway"), down: cue("down", 1, "end"), jobs: cue("jobs"), touch: cue("touch"),
  reach: cue("reach"), quicker: cue("quicker"),
  hinge2: cue("hinge", 2), pinch: cue("pinch"), swipe: cue("swipe"), drag: cue("drag"),
};
// the bed is 124 BPM and starts on a beat: scene cuts move onto the next kick
const BEAT = (FPS * 60) / 124;
const beatAfter = (f: number) => Math.round(Math.ceil(f / BEAT - 1e-6) * BEAT);
const S = {
  timeline: beatAfter(T.bosses - 6), arm: beatAfter(T.reaching - 4), grid: beatAfter(T.under - 4), hinge: beatAfter(T.but - 4),
  fix: beatAfter(T.down + 4), verdict: beatAfter(T.jobs - 4), promise: T.quicker - 14, loop: SHORT11_FRAMES - LOOP,
};
const DARK: React.CSSProperties = { position: "absolute", inset: 0, background: "radial-gradient(ellipse at 50% 40%, #1A1036 0%, #0A0718 55%, #020208 100%)" };
const SHADE_TOP: React.CSSProperties = { position: "absolute", left: 0, right: 0, top: 0, height: 900,
  background: "linear-gradient(180deg, rgba(2,2,10,0.9) 0%, rgba(2,2,10,0.6) 55%, rgba(2,2,10,0) 100%)" };
const between = (f: number, a: number, b: number) => f >= a && f < b;
const grow = (f: number, a: number, dur = 18) => interpolate(f, [a, a + dur], [0, 1], { ...CLAMP, easing: EASE_OUT });
const lerp = (a: number, b: number, t: number) => a + (b - a) * t;
// a point (x, y) turned by deg about (cx, cy), as SVG's rotate() turns it
const turn = (x: number, y: number, cx: number, cy: number, deg: number) => {
  const r = (deg * Math.PI) / 180;
  return { x: cx + (x - cx) * Math.cos(r) - (y - cy) * Math.sin(r), y: cy + (x - cx) * Math.sin(r) + (y - cy) * Math.cos(r) };
};
const DIM = "#B8B2D6";
const SMALL = 68; // labels: 48 px cap height or more (CRAFT 18 Oct)
const SKIN = "#F2EEF8"; // our drawn hand and arm: a plain light glove, nobody's likeness
const Label: React.FC<{ children: React.ReactNode; left: number; top: number; size?: number; color?: string; opacity?: number;
  width?: number; align?: "left" | "center"; mono?: boolean }> = ({ children, left, top, size = 64, color = C.ink, opacity = 1, width, align = "left", mono }) => (
  <div style={{ position: "absolute", left, top, width, textAlign: align, ...(mono ? MONO : HEADC), whiteSpace: width ? "normal" : "nowrap", fontSize: size,
    lineHeight: 1, color, opacity, ...keyline(size / 140, 10) }}>{children}</div>
);
// a fingertip, its tip at (x, y), pointing up-left by default (rot -90 = pointing left): a capsule with a nail
const Finger: React.FC<{ x: number; y: number; s?: number; opacity?: number; rot?: number }> = ({ x, y, s = 1, opacity = 1, rot = -35 }) => (
  <g opacity={opacity} transform={`translate(${x} ${y}) scale(${s}) rotate(${rot})`}>
    <rect x={-46} y={-6} width={92} height={460} rx={46} fill={SKIN} stroke={C.black} strokeWidth={7} />
    <rect x={-26} y={16} width={52} height={62} rx={20} fill="#D9D2EA" stroke={C.black} strokeWidth={4} />
  </g>
);
// the same finger with a palm behind it: a hand seen from the side
const Hand: React.FC<{ x: number; y: number; s?: number; rot?: number }> = ({ x, y, s = 0.42, rot = -90 }) => (
  <g transform={`translate(${x} ${y}) scale(${s}) rotate(${rot})`}>
    <rect x={-100} y={240} width={200} height={260} rx={80} fill={SKIN} stroke={C.black} strokeWidth={8} />
    <rect x={-46} y={-6} width={92} height={330} rx={46} fill={SKIN} stroke={C.black} strokeWidth={8} />
    <rect x={-26} y={16} width={52} height={62} rx={20} fill="#D9D2EA" stroke={C.black} strokeWidth={5} />
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
      <Tag at={T.apple + 2} left={60} top={1130} bg={C.ink} size={60} rot={[-4, -2]}>“IT DOESN’T WORK.”<br />STEVE JOBS, 2010</Tag>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ x2: who said no, then the arm
// Cook's 2012 toaster-and-fridge line was about merging a tablet and a laptop, not touch on a Mac: not on this list.
const ROWS: [string, string, string][] = [
  ["2010", "STEVE JOBS", "APPLE EVENT"],
  ["2014", "CRAIG FEDERIGHI", "CNET"],
  ["2018", "CRAIG FEDERIGHI", "WIRED"],
];
const Timeline: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (!between(frame, S.timeline, S.arm)) return null;
  const rowTop = (i: number) => 300 + i * 170;
  const line = grow(frame, S.timeline, Math.max(10, T.years - S.timeline));
  // the NOs land between "no" and "sixteen"; 2026 lands on "years"
  const stampAt = (i: number) => Math.round(T.no + ((T.sixteen - T.no) * i) / ROWS.length);
  return (
    <AbsoluteFill style={{ scale: interpolate(frame, [S.timeline, S.arm], [1, 1.035], CLAMP) }}>
      <div style={DARK} />
      <Label left={60} top={170} size={72} color={C.acid}>WHO SAID NO</Label>
      <div style={{ position: "absolute", left: 40, top: rowTop(0) + 10, width: 8, height: (rowTop(ROWS.length) - rowTop(0)) * line, backgroundColor: DIM }} />
      {ROWS.map(([yr, who, where], i) => {
        const at = S.timeline + 2 + i * 4;
        if (frame < at) return null;
        const s = pop(frame, at, fps, 230, 13);
        return (
          <div key={yr + where} style={{ position: "absolute", left: 0, top: rowTop(i), scale: interpolate(s, [0, 1], [0.9, 1]), opacity: s, transformOrigin: "0% 50%" }}>
            <Label left={64} top={0} size={84}>{yr}</Label>
            <Label left={310} top={2} size={56}>{who}</Label>
            <Label left={310} top={70} size={48} color={DIM} mono>{where}</Label>
          </div>
        );
      })}
      {ROWS.map(([yr, , where], i) => (
        <Stamp key={`no${yr}${where}`} at={stampAt(i)} left={812} top={rowTop(i) - 6} size={64} rot={-7}>NO</Stamp>
      ))}
      {frame >= T.years - 4 ? (
        <div style={{ position: "absolute", left: 0, top: rowTop(ROWS.length), opacity: grow(frame, T.years - 4, 8) }}>
          <Label left={64} top={0} size={84} color={C.acid}>2026</Label>
          <Label left={310} top={2} size={60} color={C.acid}>APPLE</Label>
          <Label left={310} top={70} size={48} color={DIM} mono>{PRODUCT_2026}</Label>
        </div>
      ) : null}
      <Stamp at={T.years} left={812} top={rowTop(ROWS.length) - 16} size={64} rot={-5} color={C.acid}>YES</Stamp>
    </AbsoluteFill>
  );
};
const Arm: React.FC = () => {
  const frame = useCurrentFrame();
  if (!between(frame, S.arm, S.grid)) return null;
  // the arm tires at a steady rate: the bar fills and the arm sags together, with a tremor that grows
  const tired = interpolate(frame, [T.reaching, S.grid - 2], [0.08, 1], CLAMP);
  const sag = 16 * interpolate(frame, [T.reaching, S.grid - 2], [0, 1], CLAMP);
  const shake = 1.6 * tired * Math.sin(frame * 1.9);
  const rad = (d: number) => (d * Math.PI) / 180;
  const sh = { x: 250, y: 760 };
  const el = { x: sh.x + 300 * Math.cos(rad(8 + sag + shake)), y: sh.y + 300 * Math.sin(rad(8 + sag + shake)) };
  const hd = { x: el.x + 290 * Math.cos(rad(-10 + sag * 1.3 - shake)), y: el.y + 290 * Math.sin(rad(-10 + sag * 1.3 - shake)) };
  const barCol = tired < 0.6 ? C.acid : C.warn;
  const q = grow(frame, S.arm + 2, 8);
  return (
    <AbsoluteFill style={{ scale: interpolate(frame, [S.arm, S.grid], [1, 1.035], CLAMP) }}>
      <div style={DARK} />
      <Label left={60} top={170} size={84} color={C.warn}>GORILLA ARM</Label>
      <Label left={60} top={272} size={SMALL} opacity={q}>“YOUR ARM WANTS</Label>
      <Label left={60} top={344} size={SMALL} opacity={q}>TO FALL OFF.”</Label>
      <Label left={60} top={424} size={52} color={DIM} opacity={q}>STEVE JOBS, 2010</Label>
      <svg width={1080} height={1920} style={{ position: "absolute", left: 0, top: 0 }}>
        <rect x={860} y={500} width={46} height={600} rx={14} fill="#D8D4EA" stroke={C.black} strokeWidth={6} />
        <circle cx={sh.x - 30} cy={sh.y - 150} r={70} fill={SKIN} stroke={C.black} strokeWidth={7} />
        <line x1={sh.x - 20} y1={sh.y - 40} x2={sh.x - 45} y2={sh.y + 280} stroke={SKIN} strokeWidth={70} strokeLinecap="round" />
        <polyline points={`${sh.x},${sh.y} ${el.x},${el.y} ${hd.x},${hd.y}`} fill="none" stroke={C.black} strokeWidth={64} strokeLinecap="round" strokeLinejoin="round" />
        <polyline points={`${sh.x},${sh.y} ${el.x},${el.y} ${hd.x},${hd.y}`} fill="none" stroke={SKIN} strokeWidth={50} strokeLinecap="round" strokeLinejoin="round" />
      </svg>
      <Label left={60} top={1104} size={SMALL}>YOUR ARM</Label>
      <div style={{ position: "absolute", left: 60, top: 1190, width: 860, height: 56, border: `5px solid ${C.ink}` }}>
        <div style={{ width: `${100 * tired}%`, height: "100%", backgroundColor: barCol }} />
      </div>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ x3: the capacitive grid
const G = { left: 160, top: 420, size: 760, n: 8 };
const gx = (i: number) => G.left + ((i + 0.5) * G.size) / G.n;
const gy = (j: number) => G.top + ((j + 0.5) * G.size) / G.n;
const HIT = { i: 5, j: 2 }; // the crossing under the finger: column 6, row 3
const Grid: React.FC = () => {
  const frame = useCurrentFrame();
  if (!between(frame, S.grid, S.hinge)) return null;
  const cx = gx(HIT.i);
  const cy = gy(HIT.j);
  const rows = grow(frame, S.grid + 2, 14);
  const cols = grow(frame, S.grid + 10, 14);
  const scanOn = between(frame, T.grid, T.finger - 2);
  const fin = grow(frame, T.finger - 6, 10);
  const field = grow(frame, T.changes, 14);
  const lit = frame >= T.changes - 2;
  const zoom = interpolate(frame, [T.changes, T.changes + 24], [1, 1.35], { ...CLAMP, easing: EASE_OUT });
  const tip = { x: cx + 8, y: cy + 10 };
  // field lines from the electrodes round the crossing, bowing up into the fingertip as it arrives
  const arcs = ([[-1, 0], [1, 0], [0, -1], [0, 1]] as [number, number][]).map(([dx, dy]) => {
    const s = { x: cx + dx * 90, y: cy + dy * 90 };
    const c = { x: (s.x + tip.x) / 2 + dy * 46, y: (s.y + tip.y) / 2 - dx * 46 };
    return `M ${s.x} ${s.y} Q ${c.x} ${c.y} ${tip.x} ${tip.y}`;
  });
  return (
    <AbsoluteFill style={{ scale: interpolate(frame, [S.grid, S.hinge], [1, 1.035], CLAMP) }}>
      <div style={DARK} />
      <Label left={60} top={160} size={72}>HOW TOUCH WORKS</Label>
      <Label left={60} top={252} size={SMALL} color={C.magenta}>ROWS SEND</Label>
      <Label left={60} top={328} size={SMALL} color={C.cyan}>COLUMNS LISTEN</Label>
      <svg width={1080} height={1920} style={{ position: "absolute", left: 0, top: 0 }}>
        <defs>
          <clipPath id="s11panel">
            <rect x={G.left} y={G.top} width={G.size} height={G.size} rx={18} />
          </clipPath>
        </defs>
        <rect x={G.left} y={G.top} width={G.size} height={G.size} rx={18} fill="#0E0A22" stroke="#3A3460" strokeWidth={4} />
        <g clipPath="url(#s11panel)">
          <g transform={`translate(${cx} ${cy}) scale(${zoom}) translate(${-cx} ${-cy})`}>
            {Array.from({ length: G.n }, (_, j) => (
              <line key={`r${j}`} x1={G.left + 20} y1={gy(j)} x2={G.left + 20 + (G.size - 40) * rows} y2={gy(j)} stroke={C.magenta}
                strokeWidth={lit && j === HIT.j ? 10 : 5} opacity={lit && j !== HIT.j ? 0.4 : 1} />
            ))}
            {Array.from({ length: G.n }, (_, i) => (
              <line key={`c${i}`} x1={gx(i)} y1={G.top + 20} x2={gx(i)} y2={G.top + 20 + (G.size - 40) * cols} stroke={C.cyan}
                strokeWidth={lit && i === HIT.i ? 10 : 5} opacity={lit && i !== HIT.i ? 0.4 : 1} />
            ))}
            {/* the controller checks every crossing in turn: a dot with a fading trail, one crossing a frame */}
            {scanOn
              ? Array.from({ length: 6 }, (_, t) => {
                  const k = Math.floor(frame - T.grid - t);
                  if (k < 0) return null;
                  const kk = k % (G.n * G.n);
                  return <circle key={t} cx={gx(kk % G.n)} cy={gy(Math.floor(kk / G.n))} r={16} fill={C.ink} opacity={(1 - t / 6) * 0.9} />;
                })
              : null}
            {field > 0
              ? arcs.map((d, m) => (
                  <path key={m} d={d} fill="none" stroke={C.acid} strokeWidth={7} strokeLinecap="round" pathLength={1}
                    strokeDasharray={`${field} 1`} />
                ))
              : null}
          </g>
        </g>
        {fin > 0 ? <Finger x={tip.x} y={tip.y} s={interpolate(fin, [0, 1], [1.2, 0.72])} opacity={interpolate(fin, [0, 1], [0, 0.92])} /> : null}
        {lit ? <circle cx={cx} cy={cy} r={24} fill={C.acid} stroke={C.black} strokeWidth={5} /> : null}
      </svg>
      <Label left={cx - 340} top={cy - 150} size={SMALL} color={C.acid} opacity={frame >= T.cross - 2 ? 1 : 0}>X 6 · Y 3</Label>
      <Tag at={T.changes + 4} left={60} top={1200} bg={C.cyan} size={60} rot={[-4, -2]}>PROJECTED CAPACITIVE TOUCH</Tag>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ x4: torque about the hinge
const P = { x: 330, y: 1000 }; // the hinge
const L = 640; // screen length from the hinge, px
const Hinge: React.FC = () => {
  const frame = useCurrentFrame();
  if (!between(frame, S.hinge, S.fix)) return null;
  // the lid opens on "hangs"; a tap pushes the screen back (anticlockwise here) and it rings down. Same push, twice the
  // lever at the top: twice the swing (OUR MATHS, row 71)
  const ring = (at: number, amp: number) => (frame < at ? 0 : -amp * Math.exp(-(frame - at) / 10) * Math.sin(((frame - at) * 2 * Math.PI) / 11));
  const open = interpolate(frame, [T.hangs - 2, T.hangs + 14], [80, -14], { ...CLAMP, easing: EASE_OUT });
  const theta = open + ring(T.top, 7) + ring(T.halfway, 3.5);
  const tap = (d: number, at: number) => {
    if (frame < at - 8 || frame > at + 22) return null;
    const slide = interpolate(frame, [at - 8, at, at + 14, at + 22], [150, 0, 0, 150], { ...CLAMP, easing: EASE_IN_OUT });
    return <Finger x={P.x + 18 + slide} y={P.y - d} s={0.5} rot={-90} />;
  };
  const bar = (d: number, x: number, col: string, k: number) =>
    k > 0 ? (
      <g opacity={k}>
        <line x1={x} y1={P.y} x2={x} y2={P.y - d * k} stroke={col} strokeWidth={12} strokeLinecap="round" />
        <line x1={x - 22} y1={P.y - d * k} x2={x + 22} y2={P.y - d * k} stroke={col} strokeWidth={10} strokeLinecap="round" />
      </g>
    ) : null;
  const ghost = (at: number, amp: number) => {
    if (frame < at || frame > at + 24) return null;
    return (
      <g transform={`rotate(${-14 - amp * 0.8} ${P.x} ${P.y})`} opacity={interpolate(frame, [at, at + 3, at + 24], [0, 0.35, 0], CLAMP)}>
        <rect x={P.x - 14} y={P.y - L} width={28} height={L} rx={10} fill="#D8D4EA" />
      </g>
    );
  };
  // equal radius, 80 degrees vs 40: the swing arcs are exactly 2 to 1
  const arc = (sweep: number, col: string, k: number) => {
    if (k <= 0) return null;
    const r = 120;
    const a0 = (-20 * Math.PI) / 180;
    const a1 = a0 - (sweep * k * Math.PI) / 180;
    return (
      <path d={`M ${P.x + r * Math.cos(a0)} ${P.y + r * Math.sin(a0)} A ${r} ${r} 0 0 0 ${P.x + r * Math.cos(a1)} ${P.y + r * Math.sin(a1)}`}
        fill="none" stroke={col} strokeWidth={14} strokeLinecap="round" />
    );
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
        {ghost(T.top, 7)}
        {ghost(T.halfway, 3.5)}
        <g transform={`rotate(${theta} ${P.x} ${P.y})`}>
          {bar(L, P.x - 44, C.acid, big)}
          {bar(L / 2, P.x - 78, C.cyan, small)}
          <rect x={P.x - 14} y={P.y - L} width={28} height={L} rx={10} fill="#D8D4EA" stroke={C.black} strokeWidth={6} />
          {tap(L - 8, T.top)}
          {tap(L / 2, T.halfway)}
        </g>
        {arc(80, C.acid, big)}
        {arc(40, C.cyan, small)}
        <circle cx={P.x} cy={P.y} r={hingeLit ? 30 : 22} fill={hingeLit ? C.acid : "#8A84A8"} stroke={C.black} strokeWidth={6} />
      </svg>
      <Label left={440} top={400} size={SMALL} color={C.acid} opacity={big}>TAP AT THE TOP</Label>
      <Label left={440} top={476} size={84} color={C.acid} opacity={grow(frame, T.twice - 2, 8)}>2× THE TWIST</Label>
      <Label left={440} top={700} size={SMALL} color={C.cyan} opacity={small}>HALFWAY DOWN</Label>
      <Label left={440} top={776} size={84} color={C.cyan} opacity={small}>1×</Label>
      <Label left={P.x - 40} top={P.y + 56} size={SMALL} opacity={hingeLit ? 1 : 0}>HINGE</Label>
      <Tag at={T.twice + 8} left={60} top={1160} bg={C.acid} size={60} rot={[-4, -2]}>OUR MATHS<br />2× DISTANCE = 2× TWIST</Tag>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ x5: Apple's touch features (⏳)
const Fix: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (!between(frame, S.fix, S.verdict)) return null;
  // Apple's own words only (slots 103-104): the hinge sentence, then "pinch to zoom", "a natural swipe", "drag and drop"
  const words: [string, number, string][] = [["PINCH TO ZOOM", T.pinch, C.acid], ["A NATURAL SWIPE", T.swipe, C.cyan], ["DRAG AND DROP", T.drag, C.acid]];
  return (
    <AbsoluteFill>
      <div style={SHADE_TOP} />
      <Tag at={T.hinge2 - 2} left={60} top={150} bg={C.ink} size={60} rot={[-3, -1]}>“A NEWLY DESIGNED HINGE”<br />APPLE, 28 OCT</Tag>
      {words.map(([w, at, col], i) => (
        <div key={w} style={{ position: "absolute", left: 60, top: 470 + i * 120, opacity: frame >= at ? 1 : 0, scale: pop(frame, at, fps, 230, 12), transformOrigin: "0% 50%" }}>
          <Label left={0} top={0} size={96} color={col}>{w}</Label>
        </div>
      ))}
    </AbsoluteFill>
  );
};

// dark band behind the captions while Apple's bright footage is on screen
const CapScrim: React.FC = () => {
  const frame = useCurrentFrame();
  const w = ([[0, S.timeline], [S.fix, S.verdict], [S.loop, SHORT11_FRAMES + 6]] as [number, number][]).find(([a, b]) => between(frame, a, b));
  if (!w) return null;
  const o = w[0] === 0 ? interpolate(frame, [w[1] - 6, w[1]], [1, 0], CLAMP)
    : Math.min(interpolate(frame, [w[0], w[0] + 6], [0, 1], CLAMP), interpolate(frame, [w[1] - 6, w[1]], [1, 0], CLAMP));
  return (
    <div style={{ position: "absolute", left: 0, right: 0, top: 1180, height: 560, opacity: o,
      background: "linear-gradient(180deg, rgba(6,9,14,0) 0%, rgba(6,9,14,0.74) 32%, rgba(6,9,14,0.74) 76%, rgba(6,9,14,0) 100%)" }} />
  );
};

// ------------------------------------------------------------------------------------------------ x6: the verdict (⏳ slot 104)
const VP = { x: 350, y: 1240 }; // the verdict laptop's hinge
const VL = 420;
const Verdict: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (!between(frame, S.verdict, S.loop)) return null;
  const rows: [string, string, string, number][] = [
    ["JOBS, 2010 →", "TIRED ARMS", C.warn, S.verdict + 2],
    [EXTRA_SOURCE, "TOUCH + TRACKPAD", C.cyan, T.touch - 2],
    ["OUR TAKE →", "WHEN IT’S QUICKER", C.acid, T.quicker - 4],
  ];
  // Jobs's "touch surfaces want to be horizontal": the hand works the trackpad (the cursor follows it), reaches up to
  // the screen on "reach", taps, and comes back down
  const go = interpolate(frame, [T.reach - 8, T.reach + 2], [0, 1], { ...CLAMP, easing: EASE_OUT });
  const back = interpolate(frame, [T.reach + 12, T.reach + 24], [0, 1], { ...CLAMP, easing: EASE_IN_OUT });
  const p = go * (1 - back);
  const slide = 26 * Math.sin((frame - S.verdict) / 9) * (1 - p);
  const touchAt = turn(VP.x + 12, VP.y - 300, VP.x, VP.y, -14);
  const cursor = turn(VP.x + 16, VP.y - 210 - slide * 2.2, VP.x, VP.y, -14);
  const hand = { x: lerp(640 + slide, touchAt.x, p), y: lerp(1222, touchAt.y, p) - 70 * Math.sin(Math.PI * p) };
  const tapping = between(frame, T.reach + 1, T.reach + 14);
  const draw = grow(frame, S.verdict + 6, 10);
  return (
    <AbsoluteFill style={{ scale: interpolate(frame, [S.verdict, S.loop], [1, 1.03], CLAMP) }}>
      <div style={DARK} />
      {rows.map(([a, b, col, at], i) => (
        <div key={b} style={{ position: "absolute", left: 60, top: 200 + i * 180, opacity: frame >= at ? 1 : 0, scale: pop(frame, at, fps, 230, 12), transformOrigin: "0% 50%" }}>
          <Label left={0} top={0} size={60}>{a}</Label>
          <Label left={0} top={68} size={100} color={col}>{b}</Label>
        </div>
      ))}
      <svg width={1080} height={1920} style={{ position: "absolute", left: 0, top: 0, opacity: draw }}>
        <rect x={VP.x - 20} y={VP.y} width={600} height={34} rx={10} fill="#B9B4CC" stroke={C.black} strokeWidth={6} />
        <g transform={`rotate(-14 ${VP.x} ${VP.y})`}>
          <rect x={VP.x - 13} y={VP.y - VL} width={26} height={VL} rx={10} fill="#D8D4EA" stroke={C.black} strokeWidth={6} />
        </g>
        {p < 0.5 ? <circle cx={cursor.x} cy={cursor.y} r={13} fill={C.acid} stroke={C.black} strokeWidth={4} /> : null}
        {tapping
          ? [0, 1].map((m) => {
              const q = ((frame - T.reach - 1) / 14 + m / 2) % 1;
              return <circle key={m} cx={touchAt.x} cy={touchAt.y} r={14 + 64 * q} fill="none" stroke={C.cyan} strokeWidth={6} opacity={1 - q} />;
            })
          : null}
        <Hand x={hand.x} y={hand.y} rot={lerp(-90, -76, p)} />
      </svg>
      <Label left={560} top={820} size={56} color={DIM} opacity={draw}>YOUR ARM</Label>
      <div style={{ position: "absolute", left: 560, top: 886, width: 340, height: 40, border: `4px solid ${C.ink}`, opacity: draw }}>
        <div style={{ width: "10%", height: "100%", backgroundColor: C.acid }} />
      </div>
      <Label left={720} top={1110} size={52} color={DIM} opacity={draw}>TRACKPAD</Label>
    </AbsoluteFill>
  );
};

// the channel's promise, as Short 8 ends (CRAFT 24 Oct): gone before the loop so the last frame stays frame 0
const ChannelPromise: React.FC = () => {
  const frame = useCurrentFrame();
  if (!between(frame, S.promise, S.loop)) return null;
  return (
    <div style={{ position: "absolute", left: 60, top: 1466, padding: "6px 18px 10px", backgroundColor: C.acid, color: C.black,
      border: `4px solid ${C.black}`, ...HEADC, fontSize: 60, lineHeight: 0.92, opacity: interpolate(frame, [S.promise, S.promise + 6], [0, 1], CLAMP),
      translate: `0 ${interpolate(frame, [S.promise, S.promise + 8], [24, 0], { ...CLAMP, easing: EASE_OUT })}px` }}>
      THE STORY BEHIND THE CLIP<br />EVERYONE&apos;S SHARING
    </div>
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
    <CapScrim />
    <Verdict />
    <ChannelPromise />
    <LoopEnd />
    <CaptionTrack pages={PAGES} hide={[[0, 4], [S.promise, SHORT11_FRAMES]]} top={1360} />
    {HOOK_CLIP ? <Credit text="APPLE" show={[[0, S.timeline], [S.loop, SHORT11_FRAMES]]} /> : null}
    {FIX_CLIP ? <Credit text="APPLE" show={[[S.fix, S.verdict]]} /> : null}
    {HAS_VO ? <Sequence from={0}><Audio src={staticFile("shorts/s11_vo.mp3")} /></Sequence> : null}
    <Bed total={SHORT11_FRAMES} level={0.12} />
    <Sfx at={S.timeline} name="whoosh" volume={0.3} />
    <Sfx at={T.no} name="thock" volume={0.4} />
    <Sfx at={S.arm} name="whoosh" volume={0.3} />
    <Sfx at={S.grid} name="whoosh" volume={0.3} />
    <Sfx at={T.changes - 2} name="settle" volume={0.35} />
    <Sfx at={S.hinge} name="whoosh" volume={0.3} />
    <Sfx at={T.top - 2} name="thock" volume={0.45} />
    <Sfx at={S.fix} name="whoosh" volume={0.3} />
    <Sfx at={S.verdict} name="whoosh" volume={0.3} />
    <Sfx at={S.loop} name="rewind" volume={0.35} />
  </AbsoluteFill>
);
