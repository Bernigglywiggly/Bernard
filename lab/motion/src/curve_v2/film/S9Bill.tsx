import { evolvePath } from "@remotion/paths";
import type React from "react";
import { AbsoluteFill, Easing, Img, interpolate, Sequence, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Video } from "@remotion/media";
import { CLAMP, EASE_IN_OUT, EASE_OUT } from "../../lib/anim";
import { BG_NIGHT, C, ClipScene, Credit, FILL, HEAD, HEADC, Headline, keyline, MONO, pop, Sfx, slowPush, Tag } from "../kit";
import { cue, segFrames } from "./util";

// Roadster film, segment S9 ("The bill", 31.7 s). Tesla's Q3 2026 Update (8-K exhibit 99.1, 21 Oct 2026), rows 6, 7, 11
// and 14 of lab/research/TESLA_Q3_2026_FACTS.md, the "Profitability" sentence word for word, and the capacity table's
// Roadster row. Footage: Tesla / YouTube (0-60 launch, kickflip), under half the runtime. The kickflip freezes over
// the Semi and turns into cyan line-work traced from that frame (public/film/s9_freeze.png); S8 opens on the same
// drawing, so the two segments join on one picture.

const SEG = "S9";
const W = (word: string, nth = 1) => cue(SEG, word, nth);
const T = {
  six: W("Six"), after: W("after"), show: W("show"), reported: W("reported"), results: W("results"),
  profit: W("profit"), fallen: W("fallen"), p43: W("43%"),
  its: W("its", 3), gross: W("gross"), whats: W("what's"), left: W("left"), after2: W("after", 2), making: W("making"), what: W("what"),
  it: W("it"), sells: W("sells"), had: W("had", 2), risen: W("risen"), p9: W("9%"),
  drop: W("drop"), spending: W("spending"), research: W("research"), p70: W("70%"),
  and2: W("and", 2), stock: W("stock"), pay: W("pay"), including: W("including"), musks: W("Musk's"), y2025: W("2025"), award: W("award"),
  and3: W("and", 3), filing: W("filing"), roadsters: W("Roadster's"), status: W("status"), two: W("two"), design: W("design"),
  development: W("development"),
  so: W("So"), trucks: W("trucks"), on: W("on"), paper: W("paper"), still: W("still"), drawing: W("drawing"),
};

const F = {
  gross: T.its - 4,      // 214: gross profit
  spend: T.drop - 8,     // 388: research spending
  quote: T.and2 - 5,     // 500: Tesla's sentence
  table: T.and3 - 5,     // 608: the capacity table
  pay: T.so - 4,         // 773: the kickflip
  freeze: T.trucks + 8,  // 840: frozen over the Semi
  end: segFrames(SEG),   // 950
};
// kick_side_slow.mp4 frame 120 (the car inverted over the Semi) lands exactly on F.freeze; s9_freeze.png is that frame.
const KICK_FREEZE_FRAME = 120;
const KICK_TRIM = KICK_FREEZE_FRAME - (F.freeze - F.pay);

const SOURCE = "SOURCE: TESLA Q3 2026 UPDATE";
const FOOTAGE = "FOOTAGE: TESLA / YOUTUBE · SLOWED DOWN";
const DIM = "rgba(255,255,255,0.62)";
const CREDIT_TOP = 958;
const CREDIT_LOW = 1010; // under the row of cars in the payoff

const ease = (frame: number, a: number, b: number, easing = EASE_OUT) => interpolate(frame, [a, b], [0, 1], { ...CLAMP, easing });

// ------------------------------------------------------------------------------------------------- the blueprint
// Line-work traced by hand from kick_side_slow.mp4 frame 120 (1920x1080 coordinates): the inverted Roadster, the Semi,
// the four cars beside it, the ground and the power line. `span` is when each group draws inside a
// 0-1 progress, so S9 can draw it on and S8 can wind it back.
type BpGroup = { span: [number, number]; width: number; paths: string[] };
const circle = (cx: number, cy: number, r: number, ry = r) => `M ${cx - r} ${cy} A ${r} ${ry} 0 1 0 ${cx + r} ${cy} A ${r} ${ry} 0 1 0 ${cx - r} ${cy}`;
const hatch = Array.from({ length: 59 }, (_, i) => `M ${150 + i * 28} 1004 L ${138 + i * 28} 1017`).join(" ");

export const BLUEPRINT: BpGroup[] = [
  { // the Roadster, upside down, jets pointing at the sky
    span: [0, 0.42], width: 3.4, paths: [
      "M 716 404 L 752 400 L 1000 400 C 1010 401 1017 403 1021 406 L 1021 428 C 995 438 955 450 905 457 C 880 461 850 459 825 453 C 795 447 750 441 716 426 Z",
      "M 807 445 C 835 439 900 437 938 446 C 915 453 880 457 852 455 C 835 453 818 450 807 445 Z",
      "M 800 396 L 938 382",
      circle(778, 407, 17, 25), circle(778, 407, 7),
      circle(961, 397, 25), circle(961, 397, 8),
      "M 985 414 L 1003 410",
      "M 812 380 L 812 292 M 800 306 L 812 290 L 824 306",
      "M 1000 376 L 1000 292 M 988 306 L 1000 290 L 1012 306",
    ] },
  { // the Semi, head-on
    span: [0.14, 0.56], width: 3, paths: [
      "M 897 744 Q 897 733 909 733 L 1034 733 Q 1046 733 1046 745 L 1052 880 Q 1053 892 1060 900 Q 1069 912 1070 932 L 1071 998 L 871 998 L 872 932 Q 873 912 882 900 Q 889 892 890 880 Z",
      "M 893 815 Q 894 800 908 800 L 1035 800 Q 1049 800 1050 815 L 1050 866 Q 1010 876 971 876 Q 932 876 893 866 Z",
      "M 856 823 L 870 821 L 872 862 L 857 864 Z M 872 858 L 891 866",
      "M 1068 821 L 1083 823 L 1084 864 L 1069 862 Z M 1068 858 L 1051 866",
      "M 884 898 L 1058 898", "M 880 926 L 1062 926", "M 873 968 L 1069 968", "M 954 950 L 986 950 L 986 964 L 954 964 Z",
    ] },
  { // the row of cars either side
    span: [0.24, 0.7], width: 2.6, paths: [
      "M 348 998 L 348 968 Q 350 956 368 952 L 400 934 Q 420 913 446 910 L 534 910 Q 552 912 563 928 L 584 950 Q 590 958 590 972 L 590 998",
      "M 414 934 L 446 917 L 532 917 L 556 940 Q 480 944 414 934 Z", "M 440 962 L 502 962", circle(515, 984, 16), circle(370, 982, 14),
      "M 592 998 L 592 958 Q 594 941 612 934 L 628 902 Q 632 896 642 896 L 742 896 Q 752 896 756 904 L 770 934 Q 776 942 776 958 L 776 998",
      "M 634 932 L 647 904 L 738 904 L 751 932 Z", "M 604 956 L 764 956", "M 602 980 L 766 980",
      "M 1150 998 L 1150 918 L 1172 882 L 1288 880 L 1346 926 L 1348 998", "M 1186 921 L 1197 890 L 1282 889 L 1322 921 Z", "M 1192 931 L 1342 931",
      "M 1372 998 L 1372 960 Q 1376 940 1396 932 L 1416 914 Q 1424 908 1438 908 L 1500 908 Q 1514 908 1524 918 L 1556 950 Q 1590 956 1598 968 L 1600 998",
      "M 1420 944 L 1435 918 L 1500 916 L 1534 944 Z", "M 1438 971 L 1572 971", circle(1390, 984, 15), circle(1568, 984, 15),
    ] },
  { // ground line with drafting hatch
    span: [0.4, 0.82], width: 3, paths: ["M 120 1001 L 1800 1001", hatch] },
  { // the power line over the Semi
    span: [0.5, 0.92], width: 2, paths: [
      "M 921 618 L 921 733", "M 902 624 L 946 624",
      "M 0 478 Q 470 556 902 622", "M 0 494 Q 470 570 902 628", "M 0 596 Q 470 626 902 638",
      "M 946 624 Q 1130 648 1310 686", "M 946 630 Q 1130 656 1310 694", "M 946 638 Q 1130 664 1310 700",
    ] },
];

export const BlueprintLines: React.FC<{ draw: number; under?: number }> = ({ draw, under = 0 }) => (
  <svg width={1920} height={1080} viewBox="0 0 1920 1080" style={{ position: "absolute", left: 0, top: 0 }}>
    {BLUEPRINT.map((g, gi) => {
      const p = interpolate(draw, g.span, [0, 1], { ...CLAMP, easing: EASE_IN_OUT });
      if (p <= 0.001) return null;
      return g.paths.map((d, i) => {
        const ev = evolvePath(p, d);
        return (
          <g key={`${gi}-${i}`}>
            {under > 0 ? <path d={d} fill="none" stroke={C.black} strokeOpacity={under} strokeWidth={g.width + 5} strokeLinecap="round"
              strokeLinejoin="round" strokeDasharray={ev.strokeDasharray} strokeDashoffset={ev.strokeDashoffset} /> : null}
            <path d={d} fill="none" stroke={C.cyan} strokeWidth={g.width} strokeLinecap="round" strokeLinejoin="round"
              strokeDasharray={ev.strokeDasharray} strokeDashoffset={ev.strokeDashoffset} />
          </g>
        );
      });
    })}
  </svg>
);

// Drafting grid: 40 px minor, 200 px major, cyan on the night gradient.
export const BlueprintGrid: React.FC<{ opacity: number }> = ({ opacity }) => (
  <AbsoluteFill style={{ opacity, backgroundImage: [
    "linear-gradient(rgba(61,255,242,0.17) 2px, transparent 2px)", "linear-gradient(90deg, rgba(61,255,242,0.17) 2px, transparent 2px)",
    "linear-gradient(rgba(61,255,242,0.07) 1px, transparent 1px)", "linear-gradient(90deg, rgba(61,255,242,0.07) 1px, transparent 1px)",
  ].join(", "), backgroundSize: "200px 200px, 200px 200px, 40px 40px, 40px 40px", backgroundPosition: "-40px -20px" }} />
);

export const FREEZE_SRC = "film/s9_freeze.png";
export const PAY_SCALE_END = 1.07;
export const PAY_ORIGIN = "50% 86%";

// ------------------------------------------------------------------------------------------------- 1. the launch
const DAYS = [15, 16, 17, 18, 19, 20, 21];
const DAY_STEPS = [24, 30, 36, 42, 48, 54]; // the highlight walks 15 -> 21 under "six days after the show"

const DayStrip: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame >= T.profit + 4) return null;
  const active = DAY_STEPS.filter((st) => frame >= st).length;
  const fade = 1 - ease(frame, T.profit - 12, T.profit + 2, Easing.in(Easing.cubic));
  const res = pop(frame, T.reported, fps, 220, 13);
  const cell = 150;
  const bar = interpolate(frame, [DAY_STEPS[0] - 6, DAY_STEPS[5]], [0, 6], CLAMP);
  return (
    <div style={{ position: "absolute", left: 100, top: 92, opacity: fade, translate: `0 ${(1 - fade) * -30}px` }}>
      <div style={{ position: "relative", height: 146, width: cell * 7 }}>
        {DAYS.map((d, i) => {
          const isActive = i === active;
          const s = i === 0 ? 1 : pop(frame, DAY_STEPS[i - 1], fps, 320, 14);
          const last = i === 6 && isActive;
          return (
            <div key={d} style={{ position: "absolute", left: i * cell, top: 0, width: cell - 10, height: 146,
              backgroundColor: isActive ? (last ? C.warn : C.acid) : "transparent", border: isActive ? `5px solid ${C.black}` : "none",
              scale: isActive ? interpolate(s, [0, 1], [1.25, 1]) : 1, display: "flex", alignItems: "center", justifyContent: "center" }}>
              <div style={{ ...HEADC, fontSize: 124, color: isActive ? (last ? C.ink : C.black) : i < active ? "rgba(255,255,255,0.5)" : C.ink,
                ...(isActive ? {} : keyline(0.6, 9)) }}>{d}</div>
            </div>
          );
        })}
        <div style={{ position: "absolute", left: cell * 7 + 14, top: 6, ...MONO, fontSize: 44, lineHeight: 1.1, color: DIM }}>OCT<br />2026</div>
        <div style={{ position: "absolute", left: (cell - 10) / 2, top: 158, height: 12, width: bar * cell, backgroundColor: C.acid,
          border: `3px solid ${C.black}` }} />
      </div>
      <div style={{ position: "relative", height: 56, marginTop: 34 }}>
        <div style={{ position: "absolute", left: 0, ...MONO, fontSize: 48, color: C.cyan, backgroundColor: "rgba(0,0,0,0.55)", padding: "0 8px" }}>THE SHOW</div>
        <div style={{ position: "absolute", left: cell * 7 - 10 - 340, width: 340, textAlign: "right", ...MONO, fontSize: 48, color: C.ink,
          opacity: interpolate(res, [0, 0.4], [0, 1], CLAMP), translate: `0 ${(1 - res) * 18}px` }}>
          <span style={{ backgroundColor: "rgba(0,0,0,0.55)", padding: "0 8px" }}>Q3 RESULTS</span>
        </div>
      </div>
    </div>
  );
};

// "PROFIT −43%" slams in on "forty-three", then shrinks into a chip that stays up while gross profit is explained.
const NetSlam: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < T.profit || frame >= F.spend) return null;
  const word = pop(frame, T.profit, fps, 200, 14);
  const slam = pop(frame, T.p43, fps, 260, 11);
  const toChip = ease(frame, F.gross - 10, F.gross + 12, EASE_IN_OUT);
  const gone = ease(frame, F.spend - 12, F.spend - 2, Easing.in(Easing.cubic));
  const sub = interpolate(frame, [T.p43 + 10, T.p43 + 20], [0, 1], CLAMP) * (1 - toChip * 3);
  return (
    <div style={{ position: "absolute", right: 100, top: 360, textAlign: "right", transformOrigin: "100% 0%",
      scale: interpolate(toChip, [0, 1], [1, 0.3]), translate: `0 ${interpolate(toChip, [0, 1], [0, -260])}px`, opacity: 1 - gone }}>
      <div style={{ ...HEADC, fontSize: 160, color: C.ink, opacity: interpolate(word, [0, 0.3], [0, 1], CLAMP),
        translate: `${(1 - word) * 60}px 0`, ...keyline(1.1, 11) }}>PROFIT</div>
      {frame >= T.p43 ? (
        <div style={{ ...HEADC, fontSize: 420, lineHeight: 0.82, color: C.warn, scale: interpolate(slam, [0, 1], [1.9, 1]),
          rotate: `${interpolate(slam, [0, 1], [-8, -2])}deg`, opacity: interpolate(slam, [0, 0.15], [0, 1], CLAMP), transformOrigin: "100% 50%",
          ...keyline(2.6, 11) }}>−43%</div>
      ) : null}
      <div style={{ ...MONO, fontSize: 44, color: C.ink, marginTop: 18, opacity: Math.max(0, sub), backgroundColor: "rgba(0,0,0,0.6)",
        display: "inline-block", padding: "6px 14px" }}>NET INCOME · $1.37B → $0.79B</div>
    </div>
  );
};

const Launch: React.FC = () => {
  const frame = useCurrentFrame();
  if (frame >= F.gross + 2) return null;
  const k = frame - T.p43;
  const shake = k >= 0 && k < 16 ? Math.sin(k * 2.6) * 18 * Math.exp(-k / 4) : 0;
  const dim = interpolate(frame, [T.p43 - 2, T.p43 + 4], [0, 0.32], CLAMP);
  const out = ease(frame, F.gross - 14, F.gross + 2, EASE_IN_OUT);
  return (
    <AbsoluteFill style={{ translate: `${shake}px ${shake * 0.45}px`, opacity: 1 - out }}>
      <ClipScene src="film/zero60_slow.mp4" from={0} dur={F.gross + 2} push={[1, 1.07]} origin="42% 55%" />
      <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(0,0,0,0.55) 0%, rgba(0,0,0,0) 34%)" }} />
      <AbsoluteFill style={{ backgroundColor: C.black, opacity: dim }} />
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------- 2. gross profit
const DEF_WORDS: [string, number][] = [["WHAT'S", T.whats], ["LEFT", T.left], ["AFTER", T.after2], ["MAKING", T.making], ["WHAT", T.what],
  ["IT", T.it], ["SELLS", T.sells]];

const GrossBars: React.FC = () => {
  const frame = useCurrentFrame();
  const x0 = 360, maxW = 1080, max = 5.494; // this year's bar 1080 px, both from zero
  const rows = [
    { label: "Q3 2025", v: 5.054, at: T.sells - 2, solid: false, top: 470 },
    { label: "Q3 2026", v: 5.494, at: T.had, solid: true, top: 640 },
  ];
  const mark = ease(frame, T.risen + 6, T.risen + 18);
  return (
    <>
      {rows.map((r) => {
        const k = ease(frame, r.at, r.at + 26);
        const w = (maxW * r.v * k) / max;
        return (
          <div key={r.label} style={{ opacity: interpolate(frame, [r.at - 6, r.at], [0, 1], CLAMP) }}>
            <div style={{ position: "absolute", left: 100, top: r.top + 26, ...HEADC, fontSize: 64, color: r.solid ? C.acid : C.ink, ...keyline(0.45, 9) }}>
              {r.label}
            </div>
            <div style={{ position: "absolute", left: x0, top: r.top, width: Math.max(10, w), height: 116,
              backgroundColor: r.solid ? C.acid : "rgba(255,255,255,0.16)", border: `6px solid ${r.solid ? C.black : C.ink}` }} />
            <div style={{ position: "absolute", left: x0 + w + 28, top: r.top + 4, ...HEADC, fontSize: 112, color: r.solid ? C.acid : C.ink,
              fontVariantNumeric: "tabular-nums", ...keyline(0.8, 10) }}>${(r.v * k).toFixed(2)}B</div>
          </div>
        );
      })}
      {/* last year's end, carried down onto this year's bar: the extra is what "risen" means */}
      <div style={{ position: "absolute", left: x0 + (maxW * 5.054) / max - 3, top: 470, width: 6, height: 300 * mark,
        backgroundImage: `repeating-linear-gradient(180deg, ${C.ink} 0 14px, transparent 14px 24px)` }} />
    </>
  );
};

const Gross: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < F.gross || frame >= F.spend) return null;
  return (
    <AbsoluteFill style={{ scale: slowPush(frame, F.gross, F.spend, 1.04), transformOrigin: "30% 55%" }}>
      <Headline at={F.gross + 2} left={100} top={100} lines={[{ text: "GROSS PROFIT", size: 150, color: C.acid }]} />
      <div style={{ position: "absolute", left: 100, top: 262, display: "flex", gap: 18 }}>
        {DEF_WORDS.map(([w, at]) => {
          const s = pop(frame, at - 2, fps, 240, 15);
          return (
            <div key={w + at} style={{ ...HEADC, fontSize: 64, color: C.ink, opacity: interpolate(s, [0, 0.35], [0, 1], CLAMP),
              translate: `0 ${(1 - s) * 26}px`, ...keyline(0.45, 9) }}>{w}</div>
          );
        })}
      </div>
      <GrossBars />
      <Tag at={T.p9} left={1470} top={800} bg={C.acid} size={140} rot={[-10, -3]}>+9%</Tag>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------- 3. research
const Spend: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < F.spend || frame >= F.quote) return null;
  const base = 900, maxH = 560, maxV = 3;
  const cols = [
    { label: "Q3 2025", v: 1.63, x: 1120, at: T.spending + 6, solid: false },
    { label: "Q3 2026", v: 2.761, x: 1460, at: T.research + 2, solid: true },
  ];
  const rd = pop(frame, T.research - 2, fps, 220, 15);
  return (
    <AbsoluteFill style={{ scale: slowPush(frame, F.spend, F.quote, 1.04), transformOrigin: "40% 60%" }}>
      <Headline at={T.drop - 2} left={100} top={120} lines={[{ text: "THE DROP CAME FROM", size: 84 }]} stroke={9} />
      <Headline at={T.spending - 2} left={92} top={214} lines={[{ text: "SPENDING", size: 236, color: C.magenta }]} />
      <div style={{ position: "absolute", left: 100, top: 476, ...HEADC, fontSize: 60, color: C.ink, opacity: interpolate(rd, [0, 0.35], [0, 1], CLAMP),
        translate: `0 ${(1 - rd) * 26}px`, ...keyline(0.45, 9) }}>RESEARCH AND DEVELOPMENT</div>
      <Tag at={T.p70} left={100} top={590} bg={C.magenta} color={C.ink} size={150} rot={[-10, -3]}>+69%</Tag>
      {cols.map((c) => {
        const k = ease(frame, c.at, c.at + 26, Easing.bezier(0.16, 1, 0.3, 1));
        const h = (maxH * c.v * k) / maxV;
        return (
          <div key={c.label} style={{ opacity: interpolate(frame, [c.at - 4, c.at + 2], [0, 1], CLAMP) }}>
            <div style={{ position: "absolute", left: c.x, top: base - h, width: 250, height: h,
              backgroundColor: c.solid ? C.magenta : "rgba(255,255,255,0.16)", border: `6px solid ${c.solid ? C.black : C.ink}` }} />
            <div style={{ position: "absolute", left: c.x - 40, width: 330, top: base - h - 116, textAlign: "center", ...HEADC, fontSize: 100,
              color: c.solid ? C.magenta : C.ink, fontVariantNumeric: "tabular-nums", ...keyline(0.75, 10) }}>${(c.v * k).toFixed(2)}B</div>
            <div style={{ position: "absolute", left: c.x - 40, width: 330, top: base + 18, textAlign: "center", ...HEADC, fontSize: 56,
              color: C.ink, ...keyline(0.4, 8) }}>{c.label}</div>
          </div>
        );
      })}
      <div style={{ position: "absolute", left: 1090, top: base, width: 650, height: 6, backgroundColor: C.ink,
        scale: `${ease(frame, F.spend + 4, F.spend + 20)} 1`, transformOrigin: "0% 50%" }} />
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------- 4. Tesla's sentence
// Word for word from P1 "Profitability"; the causes light up word by word as the narration names them.
type QW = { w: string; at?: number };
const QUOTE: QW[] = [
  { w: "an" }, { w: "increase" }, { w: "in" }, { w: "operating" }, { w: "expenses" }, { w: "driven" }, { w: "by" },
  { w: "SI", at: F.quote + 8 }, { w: "and", at: F.quote + 10 }, { w: "other", at: F.quote + 12 }, { w: "R&D", at: F.quote + 14 },
  { w: "projects,", at: F.quote + 16 },
  { w: "SBC", at: T.stock }, { w: "(including", at: T.including }, { w: "2025", at: T.y2025 - 4 }, { w: "CEO", at: T.y2025 + 4 },
  { w: "Performance", at: T.y2025 + 10 }, { w: "Award)", at: T.award - 2 },
  { w: "and" }, { w: "SG&A" },
];

const Quote: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < F.quote || frame >= F.table) return null;
  const inQ = pop(frame, F.quote + 3, fps, 180, 15);
  const g1 = interpolate(frame, [F.quote + 14, F.quote + 24], [0, 1], CLAMP);
  const g2 = interpolate(frame, [T.stock + 4, T.stock + 14], [0, 1], CLAMP);
  return (
    <AbsoluteFill style={{ scale: slowPush(frame, F.quote, F.table, 1.03), transformOrigin: "20% 40%" }}>
      <Tag at={F.quote + 1} left={100} top={100} size={56}>TESLA&apos;S OWN EXPLANATION</Tag>
      <div style={{ position: "absolute", left: 100, right: 100, top: 232, ...HEAD, fontVariationSettings: "'wdth' 88", fontWeight: 800,
        fontSize: 100, lineHeight: 1.15, color: C.ink, opacity: interpolate(inQ, [0, 0.3], [0, 1], CLAMP), translate: `0 ${(1 - inQ) * 40}px` }}>
        <span style={{ color: C.acid, ...keyline(0.5, 8) }}>“…</span>
        {QUOTE.map((q, i) => {
          const t = q.at === undefined ? 0 : interpolate(frame, [q.at, q.at + 6], [0, 1], CLAMP);
          const next = QUOTE[i + 1];
          const joined = next?.at !== undefined && q.at !== undefined; // highlight the space too, so a phrase reads as one run
          const tn = joined ? interpolate(frame, [next.at as number, (next.at as number) + 3], [0, 1], CLAMP) : 0;
          return (
            <span key={i}>
              <span style={{ color: t > 0.55 ? C.black : C.ink, backgroundImage: `linear-gradient(${C.acid}, ${C.acid})`, backgroundRepeat: "no-repeat",
                backgroundSize: `${t * 100}% 100%`, padding: "0 6px", margin: "0 -6px" }}>{q.w}</span>
              {i < QUOTE.length - 1 ? <span style={{ backgroundColor: tn > 0.5 ? C.acid : "transparent" }}> </span> : null}
            </span>
          );
        })}
        <span style={{ color: C.acid, ...keyline(0.5, 8) }}>”</span>
      </div>
      <div style={{ position: "absolute", left: 100, top: 770, ...MONO, fontSize: 48, color: C.cyan, opacity: g2 }}>
        SBC = STOCK-BASED PAY: $663M → $1,165M
      </div>
      <div style={{ position: "absolute", left: 100, top: 842, ...MONO, fontSize: 44, color: DIM, opacity: g1 }}>
        R&amp;D = RESEARCH AND DEVELOPMENT
      </div>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------- 5. capacity table
// Typeset like the filing's table (rows as given in the brief: Cybercab, Tesla Semi, Roadster), then a push onto the
// Roadster row and an acid marker on its status.
const ROWS = [
  { model: "Cybercab", cap: ">125,000", status: "Production" },
  { model: "Tesla Semi", cap: "25,000", status: "Production" },
  { model: "Roadster", cap: "–", status: "Design development" },
];
const TB = { left: 245, top: 300, rowH: 124, colCap: 420, colStatus: 900, width: 1430 };

const CapacityTable: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < F.table || frame >= F.pay) return null;
  const focus = ease(frame, T.roadsters - 2, T.roadsters + 10);
  const push = ease(frame, T.status, T.design - 4, EASE_IN_OUT);
  const d1 = interpolate(frame, [T.design, T.design + 7], [0, 1], CLAMP);
  const d2 = interpolate(frame, [T.development, T.development + 12], [0, 1], CLAMP);
  const rowY = (i: number) => TB.top + 96 + i * TB.rowH;
  // push about the Roadster row's centre: at 1.2x the whole row still sits inside the 100 px margins
  const origin = `${TB.left + TB.width / 2}px ${rowY(2) + TB.rowH / 2}px`;
  const mk = (t: number): React.CSSProperties => ({
    backgroundImage: `linear-gradient(${C.acid}, ${C.acid})`, backgroundRepeat: "no-repeat", backgroundSize: `${t * 100}% 100%`,
    color: t > 0.5 ? C.black : C.ink, padding: "0 8px", margin: "0 -8px",
  });
  return (
    <AbsoluteFill>
      <Tag at={F.table + 1} left={100} top={100} size={56}>SAME FILING · PRODUCTION CAPACITY</Tag>
      <AbsoluteFill style={{ scale: interpolate(push, [0, 1], [1, 1.18]) * slowPush(frame, T.design, F.pay, 1.015), transformOrigin: origin }}>
        <div style={{ position: "absolute", left: TB.left, top: TB.top, width: TB.width,
          opacity: interpolate(frame, [F.table, F.table + 8], [0, 1], CLAMP) * interpolate(focus, [0, 1], [1, 0.22]) }}>
          <div style={{ position: "absolute", left: 0, ...MONO, fontSize: 44, color: DIM }}>MODEL</div>
          <div style={{ position: "absolute", left: TB.colCap, ...MONO, fontSize: 44, color: DIM, lineHeight: 1.05 }}>INSTALLED ANNUAL<br />CAPACITY</div>
          <div style={{ position: "absolute", left: TB.colStatus, ...MONO, fontSize: 44, color: DIM }}>STATUS</div>
        </div>
        {ROWS.map((r, i) => {
          const s = pop(frame, F.table + 6 + i * 6, fps, 200, 16);
          const isRoad = i === 2;
          const op = interpolate(s, [0, 0.35], [0, 1], CLAMP) * (isRoad ? 1 : interpolate(focus, [0, 1], [1, 0.28]));
          return (
            <div key={r.model} style={{ position: "absolute", left: TB.left, top: rowY(i), width: TB.width, height: TB.rowH, opacity: op,
              translate: `0 ${(1 - s) * 40}px` }}>
              <div style={{ position: "absolute", left: 0, top: 0, width: TB.width, height: 3, backgroundColor: "rgba(255,255,255,0.35)" }} />
              {isRoad ? <div style={{ position: "absolute", left: -40, top: 18, width: 12, height: TB.rowH - 36, backgroundColor: C.cyan,
                scale: `1 ${focus}`, transformOrigin: "50% 50%" }} /> : null}
              {[r.model, r.cap, r.status].map((txt, c) => (
                <div key={c} style={{ position: "absolute", left: [0, TB.colCap, TB.colStatus][c], top: 30, ...HEAD, fontWeight: c === 0 ? 700 : 500,
                  fontVariationSettings: "'wdth' 92", fontSize: 64, lineHeight: 1, whiteSpace: "nowrap", color: C.ink }}>
                  {isRoad && c === 2 ? (<><span style={mk(d1)}>Design</span> <span style={mk(d2)}>development</span></>) : txt}
                </div>
              ))}
              {i === ROWS.length - 1 ? <div style={{ position: "absolute", left: 0, top: TB.rowH, width: TB.width, height: 3,
                backgroundColor: "rgba(255,255,255,0.35)" }} /> : null}
            </div>
          );
        })}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------- 6. still a drawing
const Payoff: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < F.pay) return null;
  const scale = interpolate(frame, [F.pay, F.end], [1, PAY_SCALE_END], CLAMP);
  const snap = frame >= F.freeze ? interpolate(frame - F.freeze, [0, 3, 12], [1.025, 1.012, 1], CLAMP) : 1;
  const draw = interpolate(frame, [F.freeze + 6, F.freeze + 66], [0, 1], CLAMP);
  const photoDim = ease(frame, F.freeze + 6, F.freeze + 40, EASE_IN_OUT);
  const photoOut = ease(frame, F.freeze + 40, F.freeze + 72, EASE_IN_OUT);
  const grid = ease(frame, F.freeze + 34, F.freeze + 66, EASE_IN_OUT);
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ scale: scale * snap, transformOrigin: PAY_ORIGIN }}>
        <Sequence from={F.pay} durationInFrames={F.freeze - F.pay} premountFor={fps}>
          <Video src={staticFile("film/kick_side_slow.mp4")} muted trimBefore={KICK_TRIM} style={FILL} />
        </Sequence>
        {frame >= F.freeze ? (
          <>
            <BlueprintGrid opacity={grid} />
            <Img src={staticFile(FREEZE_SRC)} style={{ ...FILL, opacity: 1 - photoOut,
              filter: `saturate(${1.1 - photoDim * 0.8}) contrast(1.06) brightness(${1.05 - photoDim * 0.6})` }} />
            <BlueprintLines draw={draw} under={0.55 * (1 - photoOut)} />
          </>
        ) : null}
      </AbsoluteFill>
      <Callout />
      <Headline at={T.on - 2} left={100} top={96} lines={[{ text: "ON PAPER,", size: 104 }]} />
      <Headline at={T.still - 2} left={100} top={196} stagger={4} lines={[{ text: "STILL A", size: 136, color: C.acid },
        { text: "DRAWING", size: 136, color: C.acid }]} />
    </AbsoluteFill>
  );
};

// The drawing's label, in the drafting style: a leader from the car to the filing's two words (drawing coordinates,
// so it rides the same push as the line-work).
const LEADER = "M 1026 420 L 1112 520 L 1600 520";
const Callout: React.FC = () => {
  const frame = useCurrentFrame();
  const at = F.freeze + 50;
  if (frame < at - 2) return null;
  const lead = ease(frame, at - 2, at + 14, EASE_IN_OUT);
  const ev = evolvePath(lead, LEADER);
  const txt = ease(frame, at + 8, at + 20);
  const scale = interpolate(frame, [F.pay, F.end], [1, PAY_SCALE_END], CLAMP);
  return (
    <AbsoluteFill style={{ scale, transformOrigin: PAY_ORIGIN }}>
      <svg width={1920} height={1080} style={{ position: "absolute", left: 0, top: 0 }}>
        <path d={LEADER} fill="none" stroke={C.cyan} strokeWidth={3} strokeDasharray={ev.strokeDasharray} strokeDashoffset={ev.strokeDashoffset} />
        <circle cx={1026} cy={420} r={7 * lead} fill={C.cyan} />
      </svg>
      <div style={{ position: "absolute", left: 1124, top: 446, opacity: txt, translate: `${(1 - txt) * 20}px 0`, ...HEADC, fontSize: 68,
        color: C.cyan, ...keyline(0.5, 9) }}>ROADSTER</div>
      <div style={{ position: "absolute", left: 1124, top: 534, opacity: txt, ...MONO, fontSize: 44, lineHeight: 1.12, color: C.ink }}>
        STATUS:<br />DESIGN DEVELOPMENT
      </div>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------- the segment
export const S9Bill: React.FC = () => (
  <AbsoluteFill style={{ background: BG_NIGHT, overflow: "hidden" }}>
    <Launch />
    <DayStrip />
    <Gross />
    <Spend />
    <Quote />
    <CapacityTable />
    <Payoff />
    <NetSlam />
    <Credit text={FOOTAGE} top={CREDIT_TOP} show={[[0, F.gross - 6]]} />
    <Credit text={SOURCE} top={CREDIT_TOP} show={[[F.gross - 6, F.pay]]} />
    <Credit text={FOOTAGE} top={CREDIT_LOW} show={[[F.pay, F.freeze + 70]]} />
    <Credit text={`DRAWING: THE CURVE · ${SOURCE}`} top={CREDIT_LOW} show={[[F.freeze + 70, F.end]]} />

    <Sfx at={18} name="hiss" volume={0.42} dur={110} />
    <Sfx at={DAY_STEPS[0]} name="tick_run" volume={0.3} dur={34} />
    <Sfx at={T.reported} name="settle" volume={0.3} />
    <Sfx at={T.profit} name="whoosh" volume={0.3} />
    <Sfx at={T.p43} name="thock" volume={0.75} />
    <Sfx at={F.gross} name="whoosh" volume={0.38} />
    <Sfx at={T.sells - 2} name="form" volume={0.32} />
    <Sfx at={T.p9} name="thock" volume={0.6} />
    <Sfx at={F.spend} name="whoosh" volume={0.38} />
    <Sfx at={T.research - 4} name="form" volume={0.32} />
    <Sfx at={T.p70} name="thock" volume={0.6} />
    <Sfx at={F.quote} name="whoosh" volume={0.32} />
    <Sfx at={T.stock} name="settle" volume={0.3} />
    <Sfx at={F.table} name="whoosh" volume={0.36} />
    <Sfx at={T.design} name="thock" volume={0.5} />
    <Sfx at={F.pay} name="whoosh" volume={0.38} />
    <Sfx at={F.freeze} name="thock" volume={0.55} />
    <Sfx at={F.freeze + 6} name="form" volume={0.3} />
    <Sfx at={T.still} name="thock" volume={0.5} />
  </AbsoluteFill>
);
