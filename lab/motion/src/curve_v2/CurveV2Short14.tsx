import { Audio, Video } from "@remotion/media";
import type React from "react";
import { AbsoluteFill, interpolate, Sequence, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { CLAMP, EASE_IN_OUT, EASE_OUT } from "../lib/anim";
import { Bed, C, CaptionTrack, Credit, HEADC, keyline, MONO, pop, Sfx, Tag } from "./kit";
import { makePages } from "./pager";
import { VO_S14 } from "./voS14Captions";

// Curve Short 14 (PRE-BUILT Sat 31 Oct 2026; uploads the day Starship Flight 15 gets a date or flies): "How SpaceX Will
// Catch a Falling Starship". 1080x1920, 30 fps. Built by account A. Script lab/curve_v2/shorts/short14.py; facts
// lab/research/STARSHIP_FLIGHT15_FACTS.md. Pictures: SpaceX's own video of the first tower catch (Flight 5, 13 Oct 2024)
// in a band (clips from prep/s14_clips.sh), and our own drawings: the catch scoreboard, the belly-first fall, the flip
// into the arms, the no-legs trade, the verdict. Playbook rules (RUNBOOK §8b) as on Short 13.
// LAUNCH DAY: change DATE_STAMP to SpaceX's own date (and DATE_PHRASE in the script, then re-voice that line).
const DATE_STAMP = "EXPECTED NOV 2026";

const PAGES = makePages(VO_S14);
const FPS = 30;
const bare = (s: string) => s.replace(/¶/g, "").trim().toLowerCase().replace(/[^a-z0-9%']/g, "");
const cue = (word: string, nth = 1, edge: "start" | "end" = "start") => {
  let seen = 0;
  for (const c of VO_S14) {
    if (bare(c.text) === word) {
      seen += 1;
      if (seen === nth) return Math.round(((edge === "start" ? c.startMs : c.endMs) / 1000) * FPS);
    }
  }
  throw new Error(`Short 14 cue: "${word}" #${nth} not found`);
};
const LAST_MS = VO_S14[VO_S14.length - 1].endMs;
const LOOP = 30; // the last second: back to frame 0's picture
export const SHORT14_FRAMES = Math.round((LAST_MS / 1000) * FPS) + 30 + LOOP;

const T = {
  three: cue("three"), shipX2: cue("ship"), next: cue("next"), flight: cue("flight"), november: cue("november"),
  shipFalls: cue("ship", 2), belly: cue("belly"), flaps: cue("flaps"), near: cue("near"), light: cue("light"), upright: cue("upright"),
  drops: cue("drops"), arms: cue("arms"), no: cue("no"), legs: cue("legs"), carry: cue("carry"), musk: cue("musk"), under: cue("under", 2),
  hour: cue("hour", 1, "end"), our: cue("our"), hold: cue("hold"), thrown: cue("thrown"), airliner: cue("airliner"), subscribe: cue("subscribe"),
};
// the bed is 124 BPM and starts on a beat: scene cuts move onto the next kick
const BEAT = (FPS * 60) / 124;
const beatAfter = (f: number) => Math.round(Math.ceil(f / BEAT - 1e-6) * BEAT);
// steam: never later than the catch clip (98 frames) runs
const S = {
  steam: Math.min(beatAfter(T.three - 40), Math.floor(97 / BEAT) * BEAT), plan: beatAfter(T.next - 6), fall: beatAfter(T.shipFalls - 8), flip: beatAfter(T.near - 8),
  legs: beatAfter(T.no - 8), verdict: beatAfter(T.our - 6), promise: T.subscribe - 6, loop: SHORT14_FRAMES - LOOP,
};
const DARK: React.CSSProperties = { position: "absolute", inset: 0, background: "radial-gradient(ellipse at 50% 40%, #1A1036 0%, #0A0718 55%, #020208 100%)" };
const between = (f: number, a: number, b: number) => f >= a && f < b;
const grow = (f: number, a: number, dur = 18) => interpolate(f, [a, a + dur], [0, 1], { ...CLAMP, easing: EASE_OUT });
const DIM = "#B8B2D6";
const PANEL = "#2A1F5C";
const STEEL = "#C9CCD8";
const TILE = "#14121C";
const Label: React.FC<{ children: React.ReactNode; left: number; top: number; size?: number; color?: string; opacity?: number;
  width?: number; align?: "left" | "center"; mono?: boolean }> = ({ children, left, top, size = 64, color = C.ink, opacity = 1, width, align = "left", mono }) => (
  <div style={{ position: "absolute", left, top, width, textAlign: align, ...(mono ? MONO : HEADC), whiteSpace: width ? "normal" : "nowrap", fontSize: size,
    lineHeight: 1, color, opacity, ...keyline(size / 140, 10) }}>{children}</div>
);

// ------------------------------------------------------------------------------------------------ the footage band
// SpaceX's video sits in a full-width 1.16:1 band; everything around it is ours.
const BAND = { y: 330, h: 930 };
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
// the drawn ring sits on the tower's arms where the booster lands: measured on frames 0, 50 and 97 of s14_catch.mp4
const TRACK: [number, number, number][] = [[0, 622, 389], [50, 610, 379], [97, 622, 357]];
const Ring: React.FC<{ k: number; opacity?: number }> = ({ k, opacity = 1 }) => {
  const keys = TRACK.map((t) => t[0]);
  const x = interpolate(k, keys, TRACK.map((t) => t[1]), CLAMP);
  const y = interpolate(k, keys, TRACK.map((t) => t[2]), CLAMP);
  const r = 112;
  return (
    <svg width={1080} height={BAND.h} style={{ position: "absolute", left: 0, top: BAND.y, opacity, overflow: "visible" }}>
      <ellipse cx={x} cy={y} rx={r * 1.25} ry={r * 0.8} fill="none" stroke={C.acid} strokeWidth={10} strokeDasharray={`${r * 6.2} 40`}
        strokeLinecap="round" transform={`rotate(-8 ${x} ${y})`} />
    </svg>
  );
};

// ------------------------------------------------------------------------------------------------ x1: frame 0
const Kicker: React.FC<{ s?: number }> = ({ s = 1 }) => (
  <div style={{ position: "absolute", left: 60, top: 96, scale: s, transformOrigin: "0% 0%" }}>
    <Label left={0} top={0} size={100}>NOW CATCH</Label>
    <Label left={0} top={106} size={100} color={C.acid}>THE SHIP?</Label>
  </div>
);
// our scoreboard on a plate in the band's lower edge: tower catches so far (facts row 3, section 0), the same on frame 0
// and the loop end. A drawn ship hangs above the real tower with a dashed drop line to the arms (our drawing from frame 0).
const Score: React.FC<{ f: number; shipQ?: boolean }> = ({ f, shipQ = false }) => {
  const box = (x: number, y: number, on: boolean, col: string, i: number) => {
    const pulse = f >= T.three + i * 4 && f < T.three + i * 4 + 10 ? 1.18 : 1;
    return <rect key={`${x}-${y}`} x={x} y={y} width={68} height={68} rx={10} fill={on ? col : "none"} stroke={on ? C.ink : shipQ ? C.acid : C.ink}
      strokeWidth={6} transform={`translate(${x + 34} ${y + 34}) scale(${on ? pulse : 1}) translate(${-(x + 34)} ${-(y + 34)})`} />;
  };
  return (
    <>
      <div style={{ position: "absolute", left: 0, top: 1000, width: 720, height: 254, backgroundColor: "rgba(4,3,12,0.72)" }} />
      <Label left={60} top={1012} size={68} color={DIM}>CAUGHT SO FAR</Label>
      <Label left={60} top={1094} size={68} color={C.cyan}>BOOSTERS</Label>
      <Label left={60} top={1176} size={68} color={C.acid}>SHIPS</Label>
      <svg width={1080} height={1920} style={{ position: "absolute", left: 0, top: 0 }}>
        {[0, 1, 2].map((i) => box(440 + i * 92, 1092, true, C.cyan, i))}
        {box(440, 1174, false, C.acid, 0)}
      </svg>
      <Label left={440} top={1176} size={68} width={68} align="center" color={C.acid}>?</Label>
    </>
  );
};
const Ghost: React.FC = () => (
  <svg width={1080} height={1920} style={{ position: "absolute", left: 0, top: 0 }}>
    <path d="M 850 690 Q 820 760 700 700" fill="none" stroke={C.acid} strokeWidth={7} strokeDasharray="18 14" strokeLinecap="round" />
    <path d="M 712 684 L 694 702 L 718 714" fill="none" stroke={C.acid} strokeWidth={7} strokeLinecap="round" strokeLinejoin="round" />
    <g transform="translate(850 520) scale(0.4)" opacity={0.95}><Ship /></g>
  </svg>
);
const Hook: React.FC = () => {
  const frame = useCurrentFrame();
  if (frame >= S.plan) return null;
  return (
    <AbsoluteFill>
      <BandEdges />
      {frame < S.steam ? <Ring k={frame} opacity={interpolate(frame, [S.steam - 6, S.steam], [1, 0], CLAMP)} /> : null}
      {frame < S.steam ? <Ghost /> : null}
      <Kicker />
      <Score f={frame} shipQ={frame >= T.shipX2} />
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ our Starship drawing
// drawn upright, nose up, centred on (0, 0), 600 tall; the heat shield is the left half, so rotate(-90) puts it face-down.
// pins near the top are what the arms catch (facts row 20: "hardware on its sides")
const Ship: React.FC<{ flap?: number; flame?: number; glow?: number; legs?: boolean; legsX?: number }> = ({ flap = 0, flame = 0, glow = 0, legs = false, legsX = 0 }) => (
  <g>
    {flame > 0 ? <path d={`M -40 300 L 0 ${300 + 160 * flame} L 40 300 Z`} fill={C.warn} stroke={C.acid} strokeWidth={4} /> : null}
    {glow > 0 ? <rect x={-70} y={-240} width={30} height={530} rx={14} fill={C.warn} opacity={0.5 * glow} /> : null}
    <path d="M -55 300 L -55 -170 Q -55 -280 0 -300 Q 55 -280 55 -170 L 55 300 Z" fill={STEEL} stroke={C.black} strokeWidth={6} />
    <path d="M -55 300 L -55 -170 Q -55 -280 0 -300 L 0 300 Z" fill={TILE} stroke={C.black} strokeWidth={6} />
    {/* forward flaps (small) and aft flaps (big); they twitch as it steers */}
    <path d="M -55 -200 L -100 -170 L -100 -110 L -55 -120 Z" fill="#8A8EA0" stroke={C.black} strokeWidth={5} transform={`rotate(${-flap * 10} -55 -160)`} />
    <path d="M 55 -200 L 100 -170 L 100 -110 L 55 -120 Z" fill="#8A8EA0" stroke={C.black} strokeWidth={5} transform={`rotate(${flap * 10} 55 -160)`} />
    <path d="M -55 140 L -120 180 L -120 290 L -55 290 Z" fill="#8A8EA0" stroke={C.black} strokeWidth={5} transform={`rotate(${flap * 8} -55 215)`} />
    <path d="M 55 140 L 120 180 L 120 290 L 55 290 Z" fill="#8A8EA0" stroke={C.black} strokeWidth={5} transform={`rotate(${-flap * 8} 55 215)`} />
    <rect x={-80} y={-238} width={26} height={18} fill={C.acid} stroke={C.black} strokeWidth={3} />
    <rect x={54} y={-238} width={26} height={18} fill={C.acid} stroke={C.black} strokeWidth={3} />
    {legs ? (
      <g>
        <path d="M -55 270 L -110 340 M 55 270 L 110 340" stroke={DIM} strokeWidth={12} strokeLinecap="round" />
        {legsX > 0 ? <path d="M -150 220 L 150 380 M 150 220 L -150 380" stroke={C.warn} strokeWidth={16 * legsX} strokeLinecap="round" opacity={legsX} /> : null}
      </g>
    ) : null}
  </g>
);

// ------------------------------------------------------------------------------------------------ x2: next, the ship too; Flight 15
const Stamp14: React.FC<{ children: React.ReactNode; at: number; left: number; top: number; color?: string; size?: number; rot?: number }> = ({
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
const Plan: React.FC = () => {
  const frame = useCurrentFrame();
  if (!between(frame, S.plan, S.fall)) return null;
  const drop = interpolate(frame, [S.plan, S.plan + 22], [-520, 0], { ...CLAMP, easing: EASE_OUT });
  const bob = frame > S.plan + 22 ? Math.sin((frame - S.plan) / 9) * 6 : 0;
  const tick = grow(frame, S.plan + 6, 10);
  const q = 1 + 0.12 * Math.max(0, Math.sin((frame - S.plan) / 5));
  return (
    <AbsoluteFill style={{ scale: interpolate(frame, [S.plan, S.fall], [1, 1.035], CLAMP), transformOrigin: "50% 45%" }}>
      <div style={DARK} />
      <Label left={60} top={150} size={96}>NEXT:</Label>
      <Label left={60} top={256} size={96} color={C.acid} opacity={grow(frame, S.plan + 4, 8)}>THE SHIP TOO</Label>
      <svg width={1080} height={1920} style={{ position: "absolute", left: 0, top: 0 }}>
        <g transform="translate(270 930)">
          <rect x={-80} y={-330} width={160} height={660} rx={8} fill={STEEL} stroke={C.black} strokeWidth={6} />
          {[-250, -140].map((y) => <path key={y} d={`M -80 ${y} L -124 ${y + 20} L -124 ${y + 70} L -80 ${y + 60} Z`} fill="#8A8EA0" stroke={C.black} strokeWidth={4} />)}
        </g>
        <g transform={`translate(720 ${930 + drop + bob})`}>
          <Ship flap={Math.sin(frame / 7) * 0.4} />
        </g>
        <rect x={120} y={1290} width={68} height={68} rx={10} fill={C.cyan} stroke={C.ink} strokeWidth={6} />
        <path d="M 134 1324 L 150 1342 L 176 1306" stroke={C.black} strokeWidth={10} fill="none" strokeLinecap="round" strokeDasharray={80} strokeDashoffset={80 * (1 - tick)} />
        <rect x={570} y={1290} width={68} height={68} rx={10} fill="none" stroke={C.acid} strokeWidth={6}
          transform={`translate(604 1324) scale(${q}) translate(-604 -1324)`} />
      </svg>
      <Label left={570} top={1292} size={68} width={68} align="center" color={C.acid}>?</Label>
      <Label left={210} top={1292} size={68} color={C.cyan}>BOOSTER</Label>
      <Label left={660} top={1292} size={68} color={C.acid}>SHIP</Label>
      <Label left={540} top={410} size={68} color={DIM} opacity={grow(frame, S.plan + 8, 8)}>NOT TO SCALE</Label>
      <Stamp14 at={Math.min(T.flight - 2, S.fall - 60)} left={60} top={400} size={72} rot={-3} color={C.warn}>FLIGHT 15</Stamp14>
      <Label left={60} top={516} size={68} color={C.ink} opacity={grow(frame, Math.min(T.november - 6, S.fall - 50), 8)}>{DATE_STAMP}</Label>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ x3: belly-first fall
const Fall: React.FC = () => {
  const frame = useCurrentFrame();
  if (!between(frame, S.fall, S.flip)) return null;
  const j = frame - S.fall;
  const flap = frame >= T.flaps - 4 ? Math.sin(j / 4) : Math.sin(j / 10) * 0.3;
  return (
    <AbsoluteFill style={{ scale: interpolate(frame, [S.fall, S.flip], [1, 1.035], CLAMP) }}>
      <div style={DARK} />
      <Label left={60} top={150} size={72} color={C.acid}>THE FALL</Label>
      <svg width={1080} height={1920} style={{ position: "absolute", left: 0, top: 0 }}>
        {/* air streaks rush up past the falling ship */}
        {Array.from({ length: 14 }).map((_, i) => {
          const x = 80 + ((i * 71) % 900);
          const y = 1350 - ((j * 34 + i * 137) % 1100);
          return <line key={i} x1={x} y1={y} x2={x} y2={y + 120} stroke={DIM} strokeWidth={5} opacity={0.45} strokeLinecap="round" />;
        })}
        <g transform={`translate(540 ${760 + Math.sin(j / 8) * 10}) rotate(${-90 + Math.sin(j / 11) * 4})`}>
          <Ship flap={flap} glow={grow(frame, T.belly - 4, 10)} />
        </g>
        {/* the belly faces the air: heat glow under it */}
        <path d="M 260 880 Q 540 960 820 880" fill="none" stroke={C.warn} strokeWidth={10} opacity={grow(frame, T.belly - 4, 10) * 0.8} />
      </svg>
      <Tag at={T.belly} left={60} top={980} bg={C.warn} size={72} rot={[-5, -3]}>BELLY FIRST</Tag>
      <Tag at={Math.min(T.flaps, S.flip - 44)} left={60} top={1090} bg={C.acid} size={72} rot={[-4, -2]}>FLAPS STEER</Tag>
      <Label left={60} top={252} size={68} color={DIM} opacity={grow(frame, S.fall + 4, 8)}>OUR DRAWING</Label>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ x4: flip and catch
const TOWER = { x: 800, w: 130, top: 600, bottom: 1330 };
const ARM_Y = 680; // the arms' height; the ship's pins land here
const PIN = 0.85 * 229; // ship centre below the arms when its pins (scale 0.85) sit on them
const Tower: React.FC = () => (
  <g>
    <rect x={TOWER.x} y={TOWER.top} width={TOWER.w} height={TOWER.bottom - TOWER.top} fill="#1C1830" stroke={C.ink} strokeWidth={6} />
    {Array.from({ length: Math.floor((TOWER.bottom - TOWER.top) / 83) }).map((_, i) => {
      const y = TOWER.top + i * 83;
      return <path key={i} d={`M ${TOWER.x} ${y} L ${TOWER.x + TOWER.w} ${y + 83} M ${TOWER.x + TOWER.w} ${y} L ${TOWER.x} ${y + 83}`} stroke={DIM} strokeWidth={3} opacity={0.6} />;
    })}
    <line x1={60} y1={TOWER.bottom} x2={1020} y2={TOWER.bottom} stroke={C.ink} strokeWidth={8} />
  </g>
);
const shipY = (f: number) =>
  interpolate(f, [S.flip, T.light, T.upright + 10, T.arms - 6], [480, 500, 520, ARM_Y + PIN], { ...CLAMP, easing: EASE_IN_OUT });
// the two arms side on: the back one (darker) and the front one, both swinging in from the tower (short, seen end-on)
// to full length around the ship
const Arms: React.FC<{ close: number; lit?: boolean }> = ({ close, lit = false }) => {
  const len = interpolate(close, [0, 1], [110, TOWER.x - 510]);
  return (
    <g>
      <rect x={TOWER.x - len} y={ARM_Y - 46} width={len + 10} height={30} rx={8} fill={lit ? "#9AA82E" : "#3A3E50"} stroke={C.black} strokeWidth={5} />
      <rect x={TOWER.x - len - 20} y={ARM_Y - 16} width={len + 30} height={36} rx={8} fill={lit ? C.acid : "#5A5F74"} stroke={C.black} strokeWidth={5} />
    </g>
  );
};
const Flip: React.FC = () => {
  const frame = useCurrentFrame();
  if (!between(frame, S.flip, S.legs)) return null;
  const rot = interpolate(frame, [T.upright - 10, T.upright + 10], [-90, 0], { ...CLAMP, easing: EASE_IN_OUT });
  const flame = frame >= T.light - 2 && frame < T.arms - 6 ? 0.7 + 0.3 * Math.sin(frame * 1.7) : 0;
  const close = interpolate(frame, [T.arms - 14, T.arms - 4], [0, 1], { ...CLAMP, easing: EASE_OUT });
  return (
    <AbsoluteFill style={{ scale: interpolate(frame, [S.flip, S.legs], [1, 1.03], CLAMP), transformOrigin: "50% 50%" }}>
      <div style={DARK} />
      <Label left={60} top={150} size={72} color={C.acid}>THE CATCH</Label>
      <svg width={1080} height={1920} style={{ position: "absolute", left: 0, top: 0 }}>
        <Tower />
        <g transform={`translate(640 ${shipY(frame)}) rotate(${rot}) scale(0.85)`}>
          <Ship flame={flame} flap={rot < -5 ? Math.sin(frame / 5) * 0.6 : 0} />
        </g>
        <Arms close={close} lit={close > 0.5} />
      </svg>
      <Tag at={T.light} left={60} top={900} bg={C.warn} size={68} rot={[-5, -3]}>ENGINES ON</Tag>
      <Tag at={T.upright} left={60} top={1000} bg={C.cyan} size={68} rot={[-4, -2]}>SWINGS<br />UPRIGHT</Tag>
      <Tag at={Math.min(T.arms - 10, S.legs - 44)} left={60} top={1170} bg={C.acid} size={68} rot={[-4, -2]}>ARMS CLOSE</Tag>
      <Label left={60} top={240} size={68} color={DIM} opacity={grow(frame, S.flip, 8)}>SPACEX'S PLAN,</Label>
      <Label left={60} top={314} size={68} color={DIM} opacity={grow(frame, S.flip, 8)}>DRAWN BY US</Label>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ x5: no legs, under an hour
const Legs: React.FC = () => {
  const frame = useCurrentFrame();
  if (!between(frame, S.legs, S.verdict)) return null;
  const x = grow(frame, T.legs, 8);
  const sweep = interpolate(frame, [T.under - 4, T.hour], [0, 330], { ...CLAMP, easing: EASE_IN_OUT });
  const clockIn = grow(frame, T.musk - 6, 10);
  const a = ((sweep - 90) * Math.PI) / 180;
  const CX = 760;
  // clock sits right of the ship
  const CY = 760;
  return (
    <AbsoluteFill style={{ scale: interpolate(frame, [S.legs, S.verdict], [1, 1.035], CLAMP) }}>
      <div style={DARK} />
      <Label left={60} top={150} size={72} color={C.acid}>WHY CATCH IT?</Label>
      <svg width={1080} height={1920} style={{ position: "absolute", left: 0, top: 0 }}>
        <g transform={`translate(280 ${760 + Math.sin((frame - S.legs) / 9) * 8}) scale(1.05)`}>
          <Ship legs legsX={x} />
        </g>
        <g opacity={clockIn}>
          <circle cx={CX} cy={CY} r={170} fill={PANEL} stroke={C.ink} strokeWidth={8} />
          <path d={`M ${CX} ${CY} L ${CX} ${CY - 160} A 160 160 0 ${sweep > 180 ? 1 : 0} 1 ${CX + 160 * Math.cos(a)} ${CY + 160 * Math.sin(a)} Z`}
            fill={C.cyan} opacity={0.35} />
          {Array.from({ length: 12 }).map((_, i) => {
            const t = (i * 30 * Math.PI) / 180;
            return <line key={i} x1={CX + 140 * Math.sin(t)} y1={CY - 140 * Math.cos(t)} x2={CX + 164 * Math.sin(t)} y2={CY - 164 * Math.cos(t)} stroke={C.ink} strokeWidth={i % 3 === 0 ? 8 : 4} />;
          })}
          <line x1={CX} y1={CY} x2={CX + 130 * Math.cos(a)} y2={CY + 130 * Math.sin(a)} stroke={C.acid} strokeWidth={12} strokeLinecap="round" />
          <circle cx={CX} cy={CY} r={16} fill={C.acid} stroke={C.black} strokeWidth={4} />
        </g>
      </svg>
      <Tag at={Math.min(T.carry, S.verdict - 60)} left={60} top={1080} bg={C.warn} size={68} rot={[-4, -2]}>NO LEGS =<br />LESS TO CARRY</Tag>
      <Label left={600} top={960} size={68} opacity={clockIn}>MUSK'S GOAL</Label>
      <Label left={600} top={1040} size={68} color={C.cyan} opacity={grow(frame, T.under - 4, 8)}>FLY AGAIN IN</Label>
      <Label left={600} top={1120} size={68} color={C.cyan} opacity={grow(frame, T.under + 4, 8)}>UNDER 1 HOUR</Label>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ x6: the verdict
const Verdict: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (!between(frame, S.verdict, S.loop)) return null;
  const rows: [string, string, string, number][] = [
    ["CAUGHT SO FAR →", "3 BOOSTERS", C.cyan, S.verdict + 2],
    ["NEXT →", "THE SHIP", C.acid, T.hold - 4],
    ["OUR TAKE →", "LIKE AN AIRLINER", C.ink, T.airliner - 6],
  ];
  return (
    <AbsoluteFill style={{ scale: interpolate(frame, [S.verdict, S.loop], [1, 1.03], CLAMP) }}>
      <div style={DARK} />
      {rows.map(([a, b, col, at], i) => (
        <div key={b} style={{ position: "absolute", left: 60, top: 150 + i * 196, opacity: frame >= at ? 1 : 0, scale: pop(frame, at, fps, 230, 24), transformOrigin: "0% 50%" }}>
          <Label left={0} top={0} size={68}>{a}</Label>
          <Label left={0} top={76} size={b.length > 12 ? 88 : 100} color={col}>{b}</Label>
        </div>
      ))}
      <svg width={1080} height={1920} style={{ position: "absolute", left: 0, top: 0, opacity: grow(frame, S.verdict + 4, 10) }}>
        <g transform="translate(100 417) scale(0.75)">
          <Tower />
          <g transform={`translate(640 ${interpolate(frame, [S.verdict, T.hold], [ARM_Y - 260, ARM_Y + PIN], { ...CLAMP, easing: EASE_IN_OUT })}) scale(0.85)`}><Ship /></g>
          <Arms close={grow(frame, T.hold - 8, 10)} lit={frame >= T.hold} />
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
  // the band plays the catch clip's first second backwards, so its last frame is frame 0; the ring runs back with it
  // and the kicker eases (not springs) to exactly scale 1, as on frame 0
  const j = frame - S.loop;
  const k = interpolate(frame, [S.loop + 14, S.loop + 24], [0, 1], { ...CLAMP, easing: EASE_OUT });
  return (
    <AbsoluteFill>
      <BandEdges />
      <Ring k={Math.max(0, LOOP - 1 - j)} />
      <Ghost />
      {frame >= S.loop + 14 ? <Kicker s={interpolate(k, [0, 1], [1.2, 1])} /> : null}
      <Score f={0} />
    </AbsoluteFill>
  );
};

export const CurveV2Short14: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: C.black }}>
    <div style={DARK} />
    <BandClip src="shorts/s14_catch.mp4" from={0} dur={S.steam} />
    <BandClip src="shorts/s14_steam.mp4" from={S.steam} dur={S.plan - S.steam} />
    <BandClip src="shorts/s14_loop.mp4" from={S.loop} dur={LOOP} />
    <Hook />
    <Plan />
    <Fall />
    <Flip />
    <Legs />
    <Verdict />
    <ChannelPromise />
    <LoopEnd />
    <Credit text="SPACEX · FLIGHT 5 · SLOWED" show={[[0, S.plan], [S.loop, SHORT14_FRAMES]]} top={BAND.y + 10} size={56} />
    <CaptionTrack pages={PAGES} hide={[[0, 4], [S.promise, SHORT14_FRAMES]]} top={1410} width={860} />
    <Sequence><Audio src={staticFile("shorts/s14_vo.mp3")} /></Sequence>
    <Bed total={SHORT14_FRAMES} level={0.085} />
    <Sfx at={T.three} name="thock" volume={0.4} />
    <Sfx at={S.steam} name="whoosh" volume={0.3} />
    <Sfx at={S.plan} name="whoosh" volume={0.3} />
    <Sfx at={T.flight - 2} name="thock" volume={0.35} />
    <Sfx at={S.plan + 6} name="thock" volume={0.3} />
    <Sfx at={T.upright - 10} name="whoosh" volume={0.25} />
    <Sfx at={T.hold} name="thock" volume={0.35} />
    <Sfx at={S.fall} name="whoosh" volume={0.3} />
    <Sfx at={T.belly - 2} name="hiss" volume={0.3} />
    <Sfx at={S.flip} name="whoosh" volume={0.3} />
    <Sfx at={T.light - 2} name="riser" volume={0.3} />
    <Sfx at={T.arms} name="thock" volume={0.45} />
    <Sfx at={S.legs} name="whoosh" volume={0.3} />
    <Sfx at={T.legs} name="thock" volume={0.35} />
    <Sfx at={T.under - 4} name="tick_run" volume={0.3} />
    <Sfx at={S.verdict} name="whoosh" volume={0.3} />
    <Sfx at={S.loop} name="rewind" volume={0.35} />
  </AbsoluteFill>
);
