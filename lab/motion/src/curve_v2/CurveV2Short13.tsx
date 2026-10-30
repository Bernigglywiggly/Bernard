import { Audio, Video } from "@remotion/media";
import type React from "react";
import { AbsoluteFill, interpolate, Sequence, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { CLAMP, EASE_IN_OUT, EASE_OUT } from "../lib/anim";
import { Bed, C, CaptionTrack, Credit, HEADC, keyline, MONO, pop, Sfx, Tag } from "./kit";
import { makePages } from "./pager";
import { VO_S13 } from "./voS13Captions";

// Curve Short 13 (Sat 31 Oct 2026): "How Do Jets Land on Aircraft Carriers?". 1080x1920, 30 fps. Built by account A on
// Fri 30 Oct. Script lab/curve_v2/shorts/short13.py; facts lab/curve_v2/shorts/short13_facts.md. Pictures: U.S. Navy
// video of the F-35C's first landing on the John F. Kennedy (CVN 79), 13 Oct 2026 (public domain), shown as a full-width
// band (clips from prep/s13_clips.sh), and our own drawings: the 150-to-0 dial, the hook-and-wire cross-section, the
// machine below deck, the full-power bolter, the verdict. First Short under the 30 Oct playbook rules (RUNBOOK §8b).
// Scenes are cued by spoken words (single, this, stealth, first, 13th, its, hook, steel, wire #2, machine, below, ship,
// water, electric, tune, pilots, full, misses, flies, our, controlled, clever, subscribe): a missing cue word throws.

const PAGES = makePages(VO_S13);
const FPS = 30;
const bare = (s: string) => s.replace(/¶/g, "").trim().toLowerCase().replace(/[^a-z0-9%']/g, "");
const cue = (word: string, nth = 1, edge: "start" | "end" = "start") => {
  let seen = 0;
  for (const c of VO_S13) {
    if (bare(c.text) === word) {
      seen += 1;
      if (seen === nth) return Math.round(((edge === "start" ? c.startMs : c.endMs) / 1000) * FPS);
    }
  }
  throw new Error(`Short 13 cue: "${word}" #${nth} not found`);
};
const LAST_MS = VO_S13[VO_S13.length - 1].endMs;
const LOOP = 30; // the last second: back to frame 0's picture
export const SHORT13_FRAMES = Math.round((LAST_MS / 1000) * FPS) + 30 + LOOP;

const T = {
  single: cue("single"), thiss: cue("this"), stealth: cue("stealth"), first: cue("first"), oct: cue("13th"),
  its: cue("its"), hook: cue("hook"), steel: cue("steel"), wire: cue("wire", 2), machine: cue("machine"), below: cue("below"),
  ship: cue("ship"), water: cue("water"), electric: cue("electric"), tune: cue("tune"),
  pilots: cue("pilots"), full: cue("full"), misses: cue("misses"), flies: cue("flies"),
  our: cue("our"), controlled: cue("controlled"), clever: cue("clever"), subscribe: cue("subscribe"),
};
// the bed is 124 BPM and starts on a beat: scene cuts move onto the next kick
const BEAT = (FPS * 60) / 124;
const beatAfter = (f: number) => Math.round(Math.ceil(f / BEAT - 1e-6) * BEAT);
const S = {
  side: beatAfter(T.single - 8), first: beatAfter(T.thiss - 6), mech: beatAfter(T.its - 8), aag: beatAfter(T.ship - 12),
  bolter: beatAfter(T.pilots - 8), verdict: beatAfter(T.our - 6), promise: T.subscribe - 6, loop: SHORT13_FRAMES - LOOP,
};
const DARK: React.CSSProperties = { position: "absolute", inset: 0, background: "radial-gradient(ellipse at 50% 40%, #1A1036 0%, #0A0718 55%, #020208 100%)" };
const between = (f: number, a: number, b: number) => f >= a && f < b;
const grow = (f: number, a: number, dur = 18) => interpolate(f, [a, a + dur], [0, 1], { ...CLAMP, easing: EASE_OUT });
const DIM = "#B8B2D6";
const PANEL = "#2A1F5C";
const Label: React.FC<{ children: React.ReactNode; left: number; top: number; size?: number; color?: string; opacity?: number;
  width?: number; align?: "left" | "center"; mono?: boolean }> = ({ children, left, top, size = 64, color = C.ink, opacity = 1, width, align = "left", mono }) => (
  <div style={{ position: "absolute", left, top, width, textAlign: align, ...(mono ? MONO : HEADC), whiteSpace: width ? "normal" : "nowrap", fontSize: size,
    lineHeight: 1, color, opacity, ...keyline(size / 140, 10) }}>{children}</div>
);

// ------------------------------------------------------------------------------------------------ the footage band
// Navy video sits in a full-width 2.31:1 band; everything around it is ours.
const BAND = { y: 430, h: 468 };
const BandClip: React.FC<{ src: string; from: number; dur: number }> = ({ src, from, dur }) => {
  const { fps } = useVideoConfig();
  return (
    <Sequence from={from} durationInFrames={dur} premountFor={fps}>
      <div style={{ position: "absolute", left: 0, top: BAND.y, width: 1080, height: BAND.h, overflow: "hidden" }}>
        <Video src={staticFile(src)} muted objectFit="cover" style={{ width: "100%", height: "100%" }} />
      </div>
    </Sequence>
  );
};
const BandEdges: React.FC = () => (
  <>
    <div style={{ position: "absolute", left: 0, right: 0, top: BAND.y - 6, height: 6, backgroundColor: C.ink }} />
    <div style={{ position: "absolute", left: 0, right: 0, top: BAND.y + BAND.h, height: 6, backgroundColor: C.ink }} />
  </>
);
// the drawn ring follows the jet's main gear, where the hook meets the wire: measured every 10 source frames of the
// head-on shot (x1.5 slow = every 15 frames here), in band pixels
const TRACK: [number, number, number][] = [[0, 439, 274], [15, 450, 288], [30, 495, 297], [45, 529, 304], [60, 619, 308],
  [75, 702, 326], [90, 751, 342], [105, 626, 351], [120, 590, 360]];
const Ring: React.FC<{ k: number; opacity?: number }> = ({ k, opacity = 1 }) => {
  const keys = TRACK.map((t) => t[0]);
  const x = interpolate(k, keys, TRACK.map((t) => t[1]), CLAMP);
  const y = interpolate(k, keys, TRACK.map((t) => t[2]), CLAMP);
  const r = interpolate(k, [0, 120], [70, 104], CLAMP);
  return (
    <svg width={1080} height={BAND.h} style={{ position: "absolute", left: 0, top: BAND.y, opacity, overflow: "visible" }}>
      <ellipse cx={x} cy={y} rx={r * 1.3} ry={r * 0.78} fill="none" stroke={C.acid} strokeWidth={10} strokeDasharray={`${r * 6.4} 40`}
        strokeLinecap="round" transform={`rotate(-8 ${x} ${y})`} />
    </svg>
  );
};

// ------------------------------------------------------------------------------------------------ x1: frame 0
const Kicker: React.FC<{ s?: number }> = ({ s = 1 }) => (
  <div style={{ position: "absolute", left: 60, top: 150, scale: s, transformOrigin: "0% 0%" }}>
    <Label left={0} top={0} size={104}>STOPPED IN</Label>
    <Label left={0} top={112} size={104} color={C.acid}>2 SECONDS?</Label>
  </div>
);
// our speed dial under the band: a TYPICAL landing (facts row 4, MK 7 figures), never this landing's numbers: "ABOUT 150",
// no counting timer; the needle reaches 0 at the x2 cut
const DIAL = { x: 300, y: 1230, r: 200 };
const Dial: React.FC<{ mph: number; time: boolean }> = ({ mph, time }) => {
  const a = Math.PI * (1 - mph / 150);
  const tip = { x: DIAL.x + (DIAL.r - 26) * Math.cos(a), y: DIAL.y - (DIAL.r - 26) * Math.sin(a) };
  return (
    <>
      <svg width={1080} height={1920} style={{ position: "absolute", left: 0, top: 0 }}>
        <path d={`M ${DIAL.x - DIAL.r} ${DIAL.y} A ${DIAL.r} ${DIAL.r} 0 0 1 ${DIAL.x + DIAL.r} ${DIAL.y}`} fill="none" stroke={DIM} strokeWidth={14} />
        {[0, 25, 50, 75, 100, 125, 150].map((v) => {
          const t = Math.PI * (1 - v / 150);
          return <line key={v} x1={DIAL.x + (DIAL.r - 30) * Math.cos(t)} y1={DIAL.y - (DIAL.r - 30) * Math.sin(t)} x2={DIAL.x + DIAL.r * Math.cos(t)}
            y2={DIAL.y - DIAL.r * Math.sin(t)} stroke={C.ink} strokeWidth={v % 50 === 0 ? 8 : 4} />;
        })}
        <line x1={DIAL.x} y1={DIAL.y} x2={tip.x} y2={tip.y} stroke={C.acid} strokeWidth={14} strokeLinecap="round" />
        <circle cx={DIAL.x} cy={DIAL.y} r={22} fill={C.acid} stroke={C.black} strokeWidth={5} />
      </svg>
      <Label left={650} top={950} size={68} color={DIM}>ABOUT</Label>
      <Label left={650} top={1014} size={140}>{Math.round(mph)}</Label>
      <Label left={650} top={1152} size={68} color={DIM}>MPH</Label>
      {time ? <Label left={60} top={1322} size={68} color={C.cyan}>ABOUT 2 S</Label> : null}
      <Label left={60} top={1256} size={68} color={DIM}>TYPICAL LANDING</Label>
    </>
  );
};
const dialAt = (f: number) => ({ mph: interpolate(f, [T.single, S.first - 2], [150, 0], CLAMP), time: f >= T.single });
const Hook: React.FC = () => {
  const frame = useCurrentFrame();
  if (frame >= S.first) return null;
  const d = dialAt(frame);
  return (
    <AbsoluteFill>
      <BandEdges />
      {frame < S.side ? <Ring k={frame} opacity={interpolate(frame, [S.side - 6, S.side], [1, 0], CLAMP)} /> : null}
      <Kicker />
      <Dial mph={d.mph} time={d.time} />
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ x2: the first landing
// our drawing of the ship in profile, a jet dropping onto its stern on "first"
const Carrier: React.FC<{ f: number }> = ({ f }) => {
  const p = interpolate(f, [T.first - 12, T.first + 14], [0, 1], { ...CLAMP, easing: EASE_OUT });
  const jx = interpolate(p, [0, 1], [-40, 150]);
  const jy = interpolate(p, [0, 1], [930, 1004]);
  return (
    <svg width={1080} height={1920} style={{ position: "absolute", left: 0, top: 0 }}>
      <path d="M 70 1030 L 880 1030 L 930 1010 L 900 1100 L 110 1100 Z" fill={PANEL} stroke={C.ink} strokeWidth={6} />
      <rect x={40} y={1008} width={890} height={22} fill="#3B2C7A" stroke={C.ink} strokeWidth={5} />
      <rect x={640} y={930} width={70} height={78} fill="#3B2C7A" stroke={C.ink} strokeWidth={5} />
      <line x1={676} y1={930} x2={676} y2={880} stroke={C.ink} strokeWidth={6} />
      <path d={`M ${jx} ${jy} l 70 -6 l 10 6 l -70 8 Z`} fill={C.acid} stroke={C.black} strokeWidth={3} />
    </svg>
  );
};
// The kit's Stamp lands from 1.8x about its centre, which ran it off the left edge (critic round 2): from 1.3x in 4 frames,
// scaled from its left edge.
const Stamp13: React.FC<{ children: React.ReactNode; at: number; left: number; top: number; color?: string; size?: number; rot?: number }> = ({
  children, at, left, top, color = C.warn, size = 96, rot = -7 }) => {
  const frame = useCurrentFrame();
  if (frame < at) return null;
  return (
    <div style={{ position: "absolute", left, top, padding: "10px 26px 14px", border: `10px solid ${color}`, color, ...HEADC, fontSize: size,
      textAlign: "center", lineHeight: 0.95, backgroundColor: "rgba(0,0,0,0.55)", rotate: `${rot}deg`, transformOrigin: "0% 50%",
      scale: interpolate(frame, [at, at + 4], [1.3, 1], { ...CLAMP, easing: EASE_OUT }), opacity: interpolate(frame, [at, at + 2], [0, 1], CLAMP) }}>
      {children}
    </div>
  );
};

const First: React.FC = () => {
  const frame = useCurrentFrame();
  if (!between(frame, S.first, S.mech)) return null;
  return (
    <AbsoluteFill>
      <BandEdges />
      <Label left={60} top={170} size={96} opacity={grow(frame, S.first, 8)}>THE FIRST JET</Label>
      <Label left={60} top={276} size={96} color={C.acid} opacity={grow(frame, T.first - 4, 8)}>TO LAND HERE</Label>
      <Tag at={T.stealth + 2} left={740} top={186} bg={C.cyan} size={72} rot={[-6, -3]}>F-35C</Tag>
      <Carrier f={frame} />
      <Label left={60} top={1120} size={76} opacity={grow(frame, S.first + 6, 10)}>JOHN F. KENNEDY</Label>
      <Label left={60} top={1206} size={68} color={DIM} opacity={grow(frame, S.first + 10, 10)}>CVN 79 · FORD CLASS</Label>
      <Stamp13 at={Math.min(T.oct - 2, S.mech - 44)} left={60} top={1280} size={64} rot={-3} color={C.warn}>13 OCT 2026</Stamp13>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ the side-view kit
const DECK_Y = 880;
const WIRE_X = 300;
const BOX = { x: 560, y: 960, w: 360, h: 250 };
// our jet in profile, facing right, wheels on y + 124; the hook tip is at (x + 6, y + 120)
const Jet: React.FC<{ x: number; y: number; rot?: number; hook?: string; flame?: number }> = ({ x, y, rot = 0, hook = C.ink, flame = 0 }) => (
  <g transform={`translate(${x} ${y}) rotate(${rot} 150 112)`}>
    {flame > 0 ? <path d={`M 6 56 L ${-40 - 70 * flame} 63 L 6 72 Z`} fill={C.warn} stroke={C.acid} strokeWidth={3} /> : null}
    <path d="M 0 60 L 70 56 L 74 66 L 4 70 Z" fill="#3A3E50" stroke={C.black} strokeWidth={4} />
    <path d="M 0 56 L 40 46 L 160 40 L 260 36 L 330 40 L 372 50 L 404 62 L 372 72 L 260 80 L 120 82 L 18 76 Z" fill="#5A5F74" stroke={C.black} strokeWidth={5} />
    <path d="M 262 38 Q 296 12 344 42 Z" fill="#C9A35B" stroke={C.black} strokeWidth={4} />
    <path d="M 26 48 L 8 4 L 44 4 L 92 44 Z" fill="#4A4E62" stroke={C.black} strokeWidth={4} />
    <path d="M 110 62 L 236 58 L 250 68 L 100 72 Z" fill="#3A3E50" stroke={C.black} strokeWidth={4} />
    <line x1={150} y1={80} x2={150} y2={108} stroke={C.black} strokeWidth={8} />
    <circle cx={150} cy={112} r={12} fill={C.black} stroke={C.ink} strokeWidth={3} />
    <line x1={330} y1={74} x2={330} y2={106} stroke={C.black} strokeWidth={7} />
    <circle cx={330} cy={114} r={10} fill={C.black} stroke={C.ink} strokeWidth={3} />
    <path d="M 40 76 L 6 120 L 0 115" fill="none" stroke={hook} strokeWidth={8} strokeLinecap="round" strokeLinejoin="round" />
  </g>
);
const JET_Y = DECK_Y - 124;
const Deck: React.FC<{ boxDim?: number }> = ({ boxDim = 1 }) => (
  <>
    <rect x={0} y={DECK_Y + 4} width={1080} height={420} fill="#120A28" />
    <line x1={0} y1={DECK_Y} x2={1080} y2={DECK_Y} stroke={C.ink} strokeWidth={10} />
    <circle cx={WIRE_X} cy={DECK_Y} r={14} fill={C.black} stroke={C.ink} strokeWidth={5} />
    <circle cx={WIRE_X} cy={1010} r={14} fill={C.black} stroke={C.ink} strokeWidth={5} />
    <rect x={BOX.x} y={BOX.y} width={BOX.w} height={BOX.h} rx={16} fill={PANEL} stroke={C.ink} strokeWidth={6} opacity={boxDim} />
  </>
);
// before the catch the wire is a raised dot on the deck; after it, the pendant runs to the hook and the purchase cable
// pays out of the machine (the dashes flow up through the deck)
const Wire: React.FC<{ hookX: number | null; payout: number }> = ({ hookX, payout }) => (
  <>
    <path d={`M ${WIRE_X} ${DECK_Y} L ${WIRE_X} 1010 L ${BOX.x} 1010`} fill="none" stroke={C.cyan} strokeWidth={7} strokeDasharray="18 12"
      strokeDashoffset={payout} />
    {hookX === null ? (
      <circle cx={WIRE_X} cy={DECK_Y - 12} r={10} fill={C.cyan} stroke={C.black} strokeWidth={3} />
    ) : (
      <line x1={WIRE_X} y1={DECK_Y - 10} x2={hookX} y2={DECK_Y - 6} stroke={C.cyan} strokeWidth={8} strokeLinecap="round" />
    )}
  </>
);

// ------------------------------------------------------------------------------------------------ x3: the catch
const catchX = (f: number) => {
  if (f < T.wire) return WIRE_X - 6 - 12 * (T.wire - f);
  const p = Math.min(1, (f - T.wire) / 45);
  return WIRE_X - 6 + 270 * (1 - (1 - p) * (1 - p));
};
const Mech: React.FC = () => {
  const frame = useCurrentFrame();
  if (!between(frame, S.mech, S.aag)) return null;
  const x = catchX(frame);
  const caught = frame >= T.wire;
  const q = grow(frame, T.machine - 2, 10);
  return (
    <AbsoluteFill style={{ scale: interpolate(frame, [S.mech, S.aag], [1, 1.035], CLAMP), transformOrigin: "50% 55%" }}>
      <div style={DARK} />
      <Label left={60} top={170} size={72} color={C.acid}>THE CATCH</Label>
      <svg width={1080} height={1920} style={{ position: "absolute", left: 0, top: 0 }}>
        <Deck />
        <Wire hookX={caught ? x + 6 : null} payout={caught ? x - (WIRE_X - 6) : 0} />
        <Jet x={x} y={JET_Y} hook={frame >= T.hook - 2 ? C.acid : C.ink} />
      </svg>
      <div style={{ position: "absolute", left: BOX.x, top: BOX.y + 40, width: BOX.w, textAlign: "center", ...HEADC, fontSize: 150, color: C.acid,
        opacity: q, scale: interpolate(q, [0, 1], [1.3, 1]) }}>?</div>
      <Tag at={T.hook} left={60} top={300} bg={C.acid} size={72} rot={[-5, -3]}>TAIL HOOK</Tag>
      <Tag at={T.steel} left={60} top={410} bg={C.cyan} size={72} rot={[-4, -2]}>STEEL WIRE</Tag>
      <Tag at={Math.min(T.below + 2, S.aag - 44)} left={60} top={1236} bg={C.ink} size={72} rot={[-4, -2]}>BELOW DECK</Tag>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ x4: the machine
const Aag: React.FC = () => {
  const frame = useCurrentFrame();
  if (!between(frame, S.aag, S.bolter)) return null;
  // the drum and the turbine spin down as the jet stops
  const spin = interpolate(frame, [S.aag, S.bolter], [0, 620], { ...CLAMP, easing: EASE_OUT });
  const pull = interpolate(frame, [T.tune - 2, T.tune + 12, T.tune + 30, T.tune + 46], [0.18, 0.34, 0.34, 0.86], { ...CLAMP, easing: EASE_IN_OUT });
  const tIn = grow(frame, T.water - 4, 10);
  const mIn = grow(frame, T.electric - 4, 10);
  return (
    <AbsoluteFill style={{ scale: interpolate(frame, [S.aag, S.bolter], [1, 1.035], CLAMP) }}>
      <div style={DARK} />
      <Label left={60} top={170} size={72} color={C.acid}>BELOW DECK</Label>
      <Tag at={T.ship + 2} left={60} top={268} bg={C.ink} size={68} rot={[-3, -1]}>ADVANCED<br />ARRESTING GEAR</Tag>
      <svg width={1080} height={1920} style={{ position: "absolute", left: 0, top: 0 }}>
        {/* the cable comes down from the deck and wraps the drum */}
        <path d="M 0 500 L 230 500" stroke={C.cyan} strokeWidth={8} strokeDasharray="18 12" strokeDashoffset={-spin * 0.9} fill="none" />
        <g transform={`rotate(${spin} 230 620)`}>
          <circle cx={230} cy={620} r={120} fill={PANEL} stroke={C.ink} strokeWidth={8} />
          {[0, 60, 120].map((a) => <line key={a} x1={230} y1={620} x2={230 + 112 * Math.cos((a * Math.PI) / 180)} y2={620 + 112 * Math.sin((a * Math.PI) / 180)} stroke={DIM} strokeWidth={8} />)}
          {[0, 60, 120].map((a) => <line key={`b${a}`} x1={230} y1={620} x2={230 - 112 * Math.cos((a * Math.PI) / 180)} y2={620 - 112 * Math.sin((a * Math.PI) / 180)} stroke={DIM} strokeWidth={8} />)}
          <circle cx={230} cy={620} r={92} fill="none" stroke={C.cyan} strokeWidth={6} />
        </g>
        <rect x={350} y={608} width={84} height={24} fill={DIM} stroke={C.black} strokeWidth={3} />
        {/* the water turbine: a housing, water swirling, vanes turning */}
        <g opacity={interpolate(tIn, [0, 1], [0.35, 1])}>
          <circle cx={560} cy={620} r={128} fill="#0B2A44" stroke={C.ink} strokeWidth={8} />
          <g transform={`rotate(${-spin * 1.6} 560 620)`}>
            {[0, 90, 180, 270].map((a) => (
              <path key={a} d="M 560 620 Q 610 560 660 600" fill="none" stroke={C.cyan} strokeWidth={10} strokeLinecap="round" transform={`rotate(${a} 560 620)`} />
            ))}
          </g>
          {[0, 1, 2, 3, 4, 5, 6, 7].map((i) => {
            const t = ((spin * 2.2 + i * 45) * Math.PI) / 180;
            const rr = 70 + (i % 3) * 14;
            return <circle key={i} cx={560 + rr * Math.cos(t)} cy={620 + rr * Math.sin(t)} r={8} fill={C.cyan} opacity={0.8} />;
          })}
        </g>
        <rect x={688} y={608} width={52} height={24} fill={DIM} stroke={C.black} strokeWidth={3} />
        {/* the electric motor */}
        <g opacity={interpolate(mIn, [0, 1], [0.35, 1])}>
          <rect x={740} y={540} width={180} height={160} rx={14} fill={PANEL} stroke={C.ink} strokeWidth={8} />
          {[0, 1, 2, 3, 4].map((i) => <line key={i} x1={770 + i * 30} y1={560} x2={750 + i * 30} y2={680} stroke={C.acid} strokeWidth={8} />)}
        </g>
        {/* the pull: tuned for each jet */}
        <rect x={60} y={1100} width={860} height={56} rx={28} fill={PANEL} stroke={C.ink} strokeWidth={6} opacity={grow(frame, T.tune - 6, 8)} />
        <rect x={66} y={1106} width={848 * pull} height={44} rx={22} fill={C.acid} opacity={grow(frame, T.tune - 6, 8)} />
      </svg>
      <Label left={400} top={790} size={68} color={C.cyan} opacity={tIn}>WATER TURBINE</Label>
      <Label left={400} top={874} size={68} color={C.acid} opacity={mIn}>ELECTRIC MOTOR</Label>
      <Label left={60} top={1010} size={72} opacity={grow(frame, T.tune - 6, 8)}>THE PULL</Label>
      <Label left={60} top={1184} size={68} color={DIM} opacity={grow(frame, T.tune, 8)}>LIGHT JET</Label>
      <Label left={600} top={1184} size={68} color={DIM} opacity={grow(frame, Math.min(T.tune + 24, S.bolter - 44), 8)}>HEAVY JET</Label>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ x5: full power, the bolter
const Bolter: React.FC = () => {
  const frame = useCurrentFrame();
  if (!between(frame, S.bolter, S.verdict)) return null;
  const x = WIRE_X - 6 + 10 * (frame - T.misses);
  const down = interpolate(frame, [S.bolter, T.misses - 16], [-90, 0], { ...CLAMP, easing: EASE_OUT });
  const lift = interpolate(frame, [T.flies - 6, S.verdict], [0, 300], { ...CLAMP, easing: EASE_IN_OUT });
  const rot = -interpolate(frame, [T.flies - 6, T.flies + 10], [0, 12], CLAMP);
  const knob = interpolate(frame, [T.full - 4, T.full + 2], [0, 1], CLAMP);
  const flame = frame >= T.full ? 0.7 + 0.3 * Math.sin(frame * 1.7) : 0;
  const spark = frame >= T.misses - 2 && frame < T.misses + 8;
  return (
    <AbsoluteFill style={{ scale: interpolate(frame, [S.bolter, S.verdict], [1, 1.03], CLAMP), transformOrigin: "50% 50%" }}>
      <div style={DARK} />
      <Label left={60} top={170} size={72} color={C.acid}>THE BACKUP PLAN</Label>
      <svg width={1080} height={1920} style={{ position: "absolute", left: 0, top: 0 }}>
        {/* the throttle */}
        <rect x={120} y={300} width={60} height={320} rx={30} fill={PANEL} stroke={C.ink} strokeWidth={6} />
        <rect x={74} y={interpolate(knob, [0, 1], [566, 300])} width={152} height={54} rx={14} fill={frame >= T.full - 4 ? C.acid : DIM} stroke={C.black} strokeWidth={5} />
        <Deck boxDim={0.45} />
        <Wire hookX={null} payout={0} />
        {spark ? (
          <g transform={`translate(${WIRE_X} ${DECK_Y - 16})`}>
            {[0, 45, 90, 135, 180, 225, 270, 315].map((a) => (
              <line key={a} x1={0} y1={0} x2={40 * Math.cos((a * Math.PI) / 180)} y2={40 * Math.sin((a * Math.PI) / 180)} stroke={C.acid} strokeWidth={6} />
            ))}
          </g>
        ) : null}
        <Jet x={x} y={JET_Y + down - lift} rot={rot} flame={flame} />
      </svg>
      <Label left={250} top={300} size={68} opacity={grow(frame, S.bolter, 8)}>FULL</Label>
      <Label left={250} top={560} size={68} color={DIM} opacity={grow(frame, S.bolter, 8)}>IDLE</Label>
      <Tag at={T.full + 2} left={420} top={330} bg={C.acid} size={72} rot={[-5, -3]}>FULL POWER</Tag>
      <Tag at={T.misses + 2} left={60} top={1050} bg={C.warn} size={72} rot={[-4, -2]}>HOOK MISSES</Tag>
      <Tag at={Math.min(T.flies + 2, S.verdict - 44)} left={60} top={1160} bg={C.ink} size={68} rot={[-3, -1]}>BOLTER<br />GO AROUND</Tag>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ x6: the verdict
const Verdict: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (!between(frame, S.verdict, S.loop)) return null;
  const rows: [string, string, string, number][] = [
    ["THE CATCH →", "A STEEL WIRE", C.cyan, S.verdict + 2],
    ["OUR TAKE →", "A CONTROLLED CRASH", C.acid, T.controlled - 4],
    ["THE CLEVER PART →", "BELOW THE DECK", C.ink, T.clever - 4],
  ];
  const ph = (frame - S.verdict) % 75;
  const fx = T.wire - 24 + ph;
  const xm = catchX(fx);
  const fade = interpolate(ph, [0, 6, 66, 75], [0, 1, 1, 0], CLAMP);
  return (
    <AbsoluteFill style={{ scale: interpolate(frame, [S.verdict, S.loop], [1, 1.03], CLAMP) }}>
      <div style={DARK} />
      {rows.map(([a, b, col, at], i) => (
        <div key={b} style={{ position: "absolute", left: 60, top: 170 + i * 196, opacity: frame >= at ? 1 : 0, scale: pop(frame, at, fps, 230, 24), transformOrigin: "0% 50%" }}>
          <Label left={0} top={0} size={68}>{a}</Label>
          <Label left={0} top={76} size={b.length > 14 ? 88 : 100} color={col}>{b}</Label>
        </div>
      ))}
      <svg width={1080} height={1920} style={{ position: "absolute", left: 0, top: 0, opacity: grow(frame, S.verdict + 4, 10) }}>
        <g transform="translate(60 120) scale(0.84)">
          <Deck />
          <g opacity={fade}>
            <Wire hookX={fx >= T.wire ? xm + 6 : null} payout={fx >= T.wire ? xm - (WIRE_X - 6) : 0} />
            <Jet x={xm} y={JET_Y} hook={C.acid} />
          </g>
        </g>
      </svg>
    </AbsoluteFill>
  );
};

// the spoken end line on a plate (playbook rule 5), gone before the loop so the last frame stays frame 0
const ChannelPromise: React.FC = () => {
  const frame = useCurrentFrame();
  if (!between(frame, S.promise, S.loop)) return null;
  return (
    <div style={{ position: "absolute", left: 60, top: 1250, padding: "8px 20px 12px", backgroundColor: C.acid, color: C.black,
      border: `4px solid ${C.black}`, ...HEADC, fontSize: 68, lineHeight: 0.96, opacity: interpolate(frame, [S.promise, S.promise + 6], [0, 1], CLAMP),
      translate: `0 ${interpolate(frame, [S.promise, S.promise + 8], [24, 0], { ...CLAMP, easing: EASE_OUT })}px` }}>
      SUBSCRIBE: ONE MACHINE<br />IN TROUBLE, EXPLAINED,<br />EVERY DAY
    </div>
  );
};

const LoopEnd: React.FC = () => {
  const frame = useCurrentFrame();
  if (frame < S.loop) return null;
  // the band plays the head-on clip's first second backwards, so its last frame is frame 0; the ring runs back with it
  // and the kicker eases (not springs) to exactly scale 1, as on frame 0
  const j = frame - S.loop;
  const k = interpolate(frame, [S.loop + 14, S.loop + 24], [0, 1], { ...CLAMP, easing: EASE_OUT });
  return (
    <AbsoluteFill>
      <BandEdges />
      <Ring k={Math.max(0, LOOP - 1 - j)} />
      {frame >= S.loop + 14 ? <Kicker s={interpolate(k, [0, 1], [1.2, 1])} /> : null}
      <Dial mph={150} time={false} />
    </AbsoluteFill>
  );
};

export const CurveV2Short13: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: C.black }}>
    <div style={DARK} />
    <BandClip src="shorts/s13_head.mp4" from={0} dur={S.side} />
    <BandClip src="shorts/s13_side.mp4" from={S.side} dur={S.first - S.side} />
    <BandClip src="shorts/s13_stern.mp4" from={S.first} dur={S.mech - S.first} />
    <BandClip src="shorts/s13_loop.mp4" from={S.loop} dur={LOOP} />
    <Hook />
    <First />
    <Mech />
    <Aag />
    <Bolter />
    <Verdict />
    <ChannelPromise />
    <LoopEnd />
    <Credit text="U.S. NAVY VIDEO · SLOWED" show={[[0, S.mech], [S.loop, SHORT13_FRAMES]]} top={BAND.y + BAND.h - 80} size={56} />
    <CaptionTrack pages={PAGES} hide={[[0, 4], [S.promise, SHORT13_FRAMES]]} top={1400} />
    <Sequence><Audio src={staticFile("shorts/s13_vo.mp3")} /></Sequence>
    <Bed total={SHORT13_FRAMES} level={0.085} />
    <Sfx at={T.single + 6} name="thock" volume={0.4} />
    <Sfx at={S.first} name="whoosh" volume={0.3} />
    <Sfx at={T.oct - 2} name="thock" volume={0.35} />
    <Sfx at={S.mech} name="whoosh" volume={0.3} />
    <Sfx at={T.wire} name="thock" volume={0.45} />
    <Sfx at={T.machine} name="settle" volume={0.35} />
    <Sfx at={S.aag} name="whoosh" volume={0.3} />
    <Sfx at={T.water - 2} name="hiss" volume={0.3} />
    <Sfx at={T.tune - 2} name="tick_run" volume={0.3} />
    <Sfx at={S.bolter} name="whoosh" volume={0.3} />
    <Sfx at={T.full - 2} name="thock" volume={0.45} />
    <Sfx at={T.flies - 6} name="riser" volume={0.3} />
    <Sfx at={S.verdict} name="whoosh" volume={0.3} />
    <Sfx at={S.loop} name="rewind" volume={0.35} />
  </AbsoluteFill>
);
