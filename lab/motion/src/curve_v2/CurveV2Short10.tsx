import { Audio } from "@remotion/media";
import type React from "react";
import { AbsoluteFill, interpolate, Sequence, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { CLAMP, EASE_OUT } from "../lib/anim";
import { Bed, C, CaptionTrack, ClipScene, Credit, HEADC, keyline, MONO, pop, Sfx, Stamp, Tag } from "./kit";
import { makePages } from "./pager";
import { VO_S10 } from "./voS10Captions";

// Curve Short 10 (Wed 28 Oct 2026): "How SpaceX Really Makes Money". 1080x1920, 30 fps.
// Script lab/curve_v2/shorts/short10.py; facts lab/research/SPACEX_MONEY_FACTS.md §0 (every number read in SpaceX's Q3
// 2026 SEC filings). Frame 0 is SpaceX's own shot of a booster held in the tower's arms (Flight 5, credited); the
// segment bars carry the argument: AI revenue 7,560 is bigger than Starlink 5,248 + rockets 1,767 (row 67), AI grew
// 9x in a year (row 66, on screen only), rockets are 12 cents of every dollar and lost $7M (rows 60, 0d), one unnamed
// customer paid 34.5% (row 0j: never name it), Starlink keeps 45 cents of operating profit per dollar (row 63), and the
// AI arm's Q3 capex 16,444 dwarfs its revenue (row 0h). Every scene is cued by a spoken word, so a new take retimes it.

const PAGES = makePages(VO_S10);
const FPS = 30;
const bare = (s: string) => s.replace(/¶/g, "").trim().toLowerCase().replace(/[^a-z0-9%']/g, "");
const cue = (word: string, nth = 1, edge: "start" | "end" = "start") => {
  let seen = 0;
  for (const c of VO_S10) {
    if (bare(c.text) === word) {
      seen += 1;
      if (seen === nth) return Math.round(((edge === "start" ? c.startMs : c.endMs) / 1000) * FPS);
    }
  }
  throw new Error(`Short 10 cue: "${word}" #${nth} not found`);
};
const LAST_MS = VO_S10[VO_S10.length - 1].endMs;
const LOOP = 30; // the last second: back into the catch, landing on frame 0's picture
export const SHORT10_FRAMES = Math.round((LAST_MS / 1000) * FPS) + 16 + LOOP;

const T = {
  ai: cue("ai"), starlink: cue("starlink"), its: cue("its", 2), seven: cue("seven"), rockets: cue("rockets", 2),
  twelve: cue("twelve"), lost: cue("lost"), customer: cue("customer"), third: cue("third"), profit: cue("profit"),
  starlink2: cue("starlink", 2), fortyfive: cue("fortyfive"), so: cue("so"), headlines: cue("headlines"),
  starlink3: cue("starlink", 3), ai3: cue("ai", 3), bets: cue("bets"),
};
// the bed is 124 BPM and starts on a beat: scene cuts move onto the next kick
const BEAT = (FPS * 60) / 124;
const beatAfter = (f: number) => Math.round(Math.ceil(f / BEAT - 1e-6) * BEAT);
const S = {
  growth: beatAfter(T.its - 3), rockets: beatAfter(T.rockets - 3), customer: beatAfter(T.customer - 8),
  starlink: beatAfter(T.profit - 6), verdict: beatAfter(T.so - 3), loop: SHORT10_FRAMES - LOOP,
};
const DARK: React.CSSProperties = { position: "absolute", inset: 0, background: "radial-gradient(ellipse at 50% 40%, #1A1036 0%, #0A0718 55%, #020208 100%)" };
const SHADE_TOP: React.CSSProperties = { position: "absolute", left: 0, right: 0, top: 0, height: 1000,
  background: "linear-gradient(180deg, rgba(2,2,10,0.9) 0%, rgba(2,2,10,0.6) 55%, rgba(2,2,10,0) 100%)" };
const between = (f: number, a: number, b: number) => f >= a && f < b;
const grow = (f: number, a: number, dur = 18) => interpolate(f, [a, a + dur], [0, 1], { ...CLAMP, easing: EASE_OUT });
const AI = C.acid;
const LINK = C.cyan;
const ROCK = C.magenta;

// a pie slice of fraction p (0-1), starting at 12 o'clock, clockwise
const slice = (cx: number, cy: number, r: number, p: number) => {
  if (p >= 0.999) return `M ${cx} ${cy - r} A ${r} ${r} 0 1 1 ${cx - 0.01} ${cy - r} Z`;
  const a = p * Math.PI * 2;
  const x = cx + r * Math.sin(a);
  const y = cy - r * Math.cos(a);
  return `M ${cx} ${cy} L ${cx} ${cy - r} A ${r} ${r} 0 ${p > 0.5 ? 1 : 0} 1 ${x} ${y} Z`;
};
const money = (v: number) => `$${v.toFixed(2)}B`;
const Label: React.FC<{ children: React.ReactNode; left: number; top: number; size?: number; color?: string; opacity?: number;
  width?: number; align?: "left" | "center" }> = ({ children, left, top, size = 64, color = C.ink, opacity = 1, width, align = "left" }) => (
  <div style={{ position: "absolute", left, top, width, textAlign: align, ...HEADC, whiteSpace: width ? "normal" : "nowrap", fontSize: size,
    lineHeight: 1, color, opacity, ...keyline(size / 140, 10) }}>{children}</div>
);

// ------------------------------------------------------------------------------------------------ x1: frame 0 + the bars
const Hook: React.FC = () => {
  const frame = useCurrentFrame();
  if (frame >= S.growth) return null;
  const k = grow(frame, T.ai - 4, 20); // the two bars race in on "AI"
  const head = interpolate(frame, [T.ai - 8, T.ai - 2], [1, 0], CLAMP);
  const W = 860;
  const max = 7.56;
  return (
    <AbsoluteFill>
      <div style={SHADE_TOP} />
      {/* frame 0: the promise, readable as a thumbnail */}
      <div style={{ position: "absolute", left: 60, top: 190, opacity: head }}>
        <Label left={0} top={0} size={104}>SPACEX’S BIGGEST</Label>
        <Label left={0} top={112} size={104} color={AI}>BUSINESS ISN’T</Label>
        <Label left={0} top={224} size={104} color={AI}>ROCKETS</Label>
      </div>
      {k > 0 ? (
        <div style={{ position: "absolute", left: 60, top: 210 }}>
          <Label left={0} top={0} size={56}>AI</Label>
          <div style={{ position: "absolute", left: 0, top: 66, width: (W * 7.56 * k) / max, height: 96, backgroundColor: AI, border: `5px solid ${C.black}` }} />
          <Label left={0} top={176} size={72} color={AI}>{money(7.56 * k)}</Label>
          <Label left={0} top={300} size={56}>STARLINK + ROCKETS</Label>
          <div style={{ position: "absolute", left: 0, top: 366, width: (W * 5.25 * k) / max, height: 96, backgroundColor: LINK, border: `5px solid ${C.black}` }} />
          <div style={{ position: "absolute", left: (W * 5.25 * k) / max, top: 366, width: (W * 1.77 * k) / max, height: 96, backgroundColor: ROCK, border: `5px solid ${C.black}` }} />
          <Label left={0} top={476} size={72} color={LINK}>{money((5.25 + 1.77) * k)}</Label>
        </div>
      ) : null}
      <Tag at={T.ai + 10} left={60} top={800} bg={C.ink} size={44} rot={[-5, -2]}>REVENUE · Q3 2026 · SEC FILING</Tag>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ x2: 9x in a year
const Growth: React.FC = () => {
  const frame = useCurrentFrame();
  if (!between(frame, S.growth, S.rockets)) return null;
  const a = grow(frame, S.growth + 2, 14);
  const b = grow(frame, T.seven - 10, 26);
  const W = 860;
  return (
    <AbsoluteFill>
      <div style={DARK} />
      <Label left={60} top={200} size={72}>SPACEX’S AI ARM</Label>
      <Label left={60} top={290} size={44} color="#B8B2D6">REVENUE IN ONE QUARTER</Label>
      <Label left={60} top={420} size={52}>Q3 2025</Label>
      <div style={{ position: "absolute", left: 60, top: 486, width: Math.max(10, (W * 0.813 * a) / 7.56), height: 110, backgroundColor: "#7A6FA8", border: `5px solid ${C.black}` }} />
      <Label left={60 + (W * 0.813) / 7.56 + 24} top={500} size={72} color="#C9C2EE" opacity={a}>{money(0.81 * a)}</Label>
      <Label left={60} top={660} size={52}>Q3 2026</Label>
      <div style={{ position: "absolute", left: 60, top: 726, width: Math.max(10, W * b), height: 110, backgroundColor: AI, border: `5px solid ${C.black}` }} />
      <Label left={60} top={860} size={120} color={AI} opacity={b > 0.02 ? 1 : 0}>{money(7.56 * b)}</Label>
      <Tag at={T.seven + 18} left={60} top={1010} bg={C.acid} size={48} rot={[-5, -2]}>OUR MATHS · 9× IN A YEAR</Tag>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ x3: 12 cents, and a loss
const Rockets: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (!between(frame, S.rockets, S.customer)) return null;
  const lit = grow(frame, T.twelve - 4, 12);
  const s = pop(frame, S.rockets + 4, fps, 180, 14);
  const cx = 300;
  const cy = 560;
  const r = 210;
  return (
    <AbsoluteFill>
      <div style={SHADE_TOP} />
      <Label left={60} top={180} size={64}>EVERY $1 SPACEX TOOK</Label>
      <svg width={1080} height={1920} style={{ position: "absolute", left: 0, top: 0 }}>
        <g style={{ transform: `scale(${s})`, transformOrigin: `${cx}px ${cy}px` }}>
          <circle cx={cx} cy={cy} r={r} fill="#2A2440" stroke={C.black} strokeWidth={8} />
          <path d={slice(cx, cy, r, 0.121)} fill={ROCK} opacity={0.35 + 0.65 * lit} stroke={C.black} strokeWidth={6}
            style={{ transform: `translate(${14 * lit}px, ${-22 * lit}px)` }} />
        </g>
      </svg>
      <Label left={560} top={400} size={150} color={ROCK} opacity={lit}>12¢</Label>
      <Label left={560} top={560} size={52} opacity={lit}>ROCKETS</Label>
      <Label left={560} top={624} size={40} color="#E5DDFF" opacity={lit}>OUR MATHS</Label>
      <Label left={560} top={672} size={40} color="#E5DDFF" opacity={lit}>$1.77B ÷ $14.58B</Label>
      <Stamp at={T.lost - 2} left={250} top={880} size={92} rot={-6}>LOST $7M</Stamp>
      <Tag at={T.lost + 14} left={290} top={1060} bg={C.ink} size={40} rot={[-4, -2]}>SPACE SEGMENT · Q3 2026 · SEC</Tag>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ x4: the unnamed customer
const Customer: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (!between(frame, S.customer, S.starlink)) return null;
  const card = pop(frame, S.customer + 2, fps, 200, 13);
  const q = pop(frame, T.customer + 6, fps, 240, 9);
  const third = grow(frame, T.third - 10, 18);
  const cx = 760;
  const cy = 980;
  const r = 170;
  return (
    <AbsoluteFill>
      <div style={DARK} />
      <div style={{ position: "absolute", left: 60, top: 230, width: 960, padding: "34px 38px", backgroundColor: "#F4F0E6", color: C.black,
        border: `6px solid ${C.black}`, scale: card, rotate: `${interpolate(card, [0, 1], [-4, -1.5])}deg`, transformOrigin: "0% 50%" }}>
        <div style={{ ...MONO, fontSize: 36, color: "#4A4560" }}>SEC 10-Q · Q3 2026</div>
        <div style={{ ...HEADC, fontSize: 84, marginTop: 14, lineHeight: 1 }}>CUSTOMER B</div>
        <div style={{ ...HEADC, fontSize: 84, lineHeight: 1, color: C.warn }}>34.5% OF REVENUE</div>
      </div>
      <div style={{ position: "absolute", left: 80, top: 760, width: 440, height: 300, border: `8px dashed ${C.ink}`, borderRadius: 24,
        display: "flex", alignItems: "center", justifyContent: "center", ...HEADC, fontSize: 230, color: C.ink, scale: q }}>?</div>
      <Label left={80} top={1090} size={44} color="#B8B2D6">NAME: NOT GIVEN</Label>
      <svg width={1080} height={1920} style={{ position: "absolute", left: 0, top: 0 }}>
        <circle cx={cx} cy={cy} r={r} fill="#2A2440" stroke={C.black} strokeWidth={8} />
        <path d={slice(cx, cy, r, 0.345 * third)} fill={C.warn} stroke={C.black} strokeWidth={6} />
      </svg>
      <Label left={600} top={1170} size={56} color={C.warn} opacity={third}>≈ A THIRD</Label>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ x5: Starlink's margin
const Starlink: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (!between(frame, S.starlink, S.verdict)) return null;
  const s = pop(frame, S.starlink + 2, fps, 190, 13);
  const lit = grow(frame, T.fortyfive - 6, 16);
  const cx = 540;
  const cy = 700;
  const r = 250;
  return (
    <AbsoluteFill>
      <div style={DARK} />
      <Label left={60} top={180} size={72} color={LINK}>STARLINK</Label>
      <Label left={60} top={270} size={44} color="#B8B2D6">EVERY $1 OF STARLINK REVENUE</Label>
      <svg width={1080} height={1920} style={{ position: "absolute", left: 0, top: 0 }}>
        <g style={{ transform: `scale(${s})`, transformOrigin: `${cx}px ${cy}px` }}>
          <circle cx={cx} cy={cy} r={r} fill="#2A2440" stroke={C.black} strokeWidth={8} />
          <path d={slice(cx, cy, r, 0.45 * Math.max(0.001, lit))} fill={LINK} stroke={C.black} strokeWidth={6} />
        </g>
      </svg>
      <Label left={0} top={990} width={1080} align="center" size={130} color={LINK} opacity={lit}>45¢ PROFIT</Label>
      <Tag at={T.fortyfive + 16} left={60} top={1170} bg={C.cyan} size={42} rot={[-4, -2]}>OUR MATHS · $2.37B ÷ $5.25B · Q3 2026</Tag>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ x6: headlines, profit, bets
const Verdict: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (!between(frame, S.verdict, S.loop)) return null;
  const row = (at: number) => pop(frame, at, fps, 230, 12);
  const capex = grow(frame, T.ai3 + 6, 16);
  const rows: [string, string, string, number][] = [
    ["ROCKETS", "HEADLINES", ROCK, T.headlines - 6],
    ["STARLINK", "PROFIT", LINK, T.starlink3 + 8],
    ["AI", "BETS", AI, T.ai3 - 2],
  ];
  return (
    <AbsoluteFill>
      <div style={DARK} />
      {rows.map(([a, b, col, at], i) => (
        <div key={a} style={{ position: "absolute", left: 60, top: 190 + i * 170, opacity: frame >= at ? 1 : 0, scale: row(at), transformOrigin: "0% 50%" }}>
          <Label left={0} top={0} size={60}>{a} →</Label>
          <Label left={0} top={64} size={92} color={col}>{b}</Label>
        </div>
      ))}
      {frame >= T.ai3 + 4 ? (
        <div style={{ position: "absolute", left: 60, top: 760 }}>
          <Label left={0} top={0} size={44} color="#B8B2D6">THE AI ARM, Q3 2026</Label>
          <Label left={0} top={70} size={44}>REVENUE</Label>
          <div style={{ position: "absolute", left: 250, top: 62, width: (460 * 7.56) / 16.44, height: 64, backgroundColor: AI, border: `5px solid ${C.black}` }} />
          <Label left={250 + (460 * 7.56) / 16.44 + 18} top={70} size={48} color={AI}>$7.56B</Label>
          <Label left={0} top={170} size={44}>SPENT ON KIT</Label>
          <div style={{ position: "absolute", left: 250, top: 162, width: Math.max(8, 460 * capex), height: 64, backgroundColor: C.warn, border: `5px solid ${C.black}` }} />
          <Label left={250 + 460 * capex + 18} top={170} size={48} color={C.warn} opacity={capex}>$16.4B</Label>
          <Tag at={T.ai3 + 14} left={0} top={270} bg={C.ink} size={38} rot={[-4, -2]}>CAPITAL SPENDING · SEC 10-Q</Tag>
        </div>
      ) : null}
    </AbsoluteFill>
  );
};

export const CurveV2Short10: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: C.black }}>
    {/* pictures: SpaceX's own booster held in the tower (frame 0 and the loop), and its burn down to the tower */}
    <ClipScene src="shorts/s10_catch.mp4" from={0} dur={S.growth} push={[1, 1.05]} origin="50% 40%" />
    <ClipScene src="shorts/s10_descent.mp4" from={S.rockets} dur={S.customer - S.rockets} push={[1.02, 1.08]} origin="50% 45%" />
    <ClipScene src="shorts/s10_loop.mp4" from={S.loop} dur={LOOP} push={[1.05, 1]} origin="50% 40%" />
    <Hook />
    <Growth />
    <Rockets />
    <Customer />
    <Starlink />
    <Verdict />
    <CaptionTrack pages={PAGES} hide={[[0, T.ai + 24], [S.loop, SHORT10_FRAMES]]} top={1360} />
    <Credit text="SPACEX · YOUTUBE" show={[[0, S.growth], [S.rockets, S.customer], [S.loop, SHORT10_FRAMES]]} />
    <Sequence from={0}><Audio src={staticFile("shorts/s10_vo.mp3")} /></Sequence>
    <Bed total={SHORT10_FRAMES} level={0.12} />
    <Sfx at={T.ai - 4} name="whoosh" volume={0.3} />
    <Sfx at={S.growth} name="whoosh" volume={0.3} />
    <Sfx at={S.rockets} name="whoosh" volume={0.3} />
    <Sfx at={T.lost - 2} name="thock" volume={0.45} />
    <Sfx at={S.customer} name="whoosh" volume={0.3} />
    <Sfx at={S.starlink} name="whoosh" volume={0.3} />
    <Sfx at={S.verdict} name="whoosh" volume={0.3} />
    <Sfx at={S.loop} name="rewind" volume={0.35} />
  </AbsoluteFill>
);
