import type React from "react";
import { AbsoluteFill, Easing, interpolate, random, useCurrentFrame, useVideoConfig } from "remotion";
import { CLAMP, EASE_IN_OUT, EASE_OUT } from "../../lib/anim";
import { theme } from "../../theme";
import { BG_NIGHT, C, HEADC, keyline, MONO, pop, slowPush, Tag } from "../kit";
import { EvidenceStamp, Sfx } from "./fx";
import { BODY, GREY, Jet, Roadster, ROADSTER_NOZZLE, WS } from "./S5FanCar";
import { cue } from "./util";

// Roadster film, segment S7 ("The deposit", 30.1 s). The money, then what it buys: a counter climbs from the $5,000 paid
// today to the $250,000 paid within ten days; a timeline from the 2017 promise (a 2020 launch) to 2028; Tesla's US
// contract with "or if it will be delivered" marked (the UK version drops "or if"); a range road that shrinks from
// 620 to about 315 miles and drags the car back with it; then the car joins a queue under a split-flap board whose
// numbers won't sit still, and the board flips to the payoff: $250,000 for a place in a queue.
// Facts: TESLA_ROADSTER_FACTS.md §3 (Thrust US reservation $5,000 + $245,000 = $250,000; production 2028; range about
// 310-320 mi per Moravy to Top Gear, 620 mi promised in 2017; no price announced), §13.1 rows 1-3 and 17 (US clause 4
// "we cannot guarantee when your vehicle will actually be delivered or if it will be delivered", stamped
// US v.20261015; the UK clause ends "...will actually be delivered."; the 2017 deal promised a 2020 launch).
// v2 (critic round 1): the refund clause (§13.1 #6-7: refundable, no interest, no escrow) is stamped under the money, and
// the board carries the filing's status for the car, "Design development" (TESLA_Q3_2026_FACTS.md, capacity table).

const S = "S7";
const Q = {
  reserve: cue(S, "reserve"), thrusters: cue(S, "thrusters"), quarter: cue(S, "quarter"), dollars: cue(S, "dollars"),
  upfront: cue(S, "upfront"), refundable: cue(S, "refundable"), interest: cue(S, "interest"), escrow: cue(S, "escrow"), car: cue(S, "car"), y2028: cue(S, "2028"), after: cue(S, "after"), promised: cue(S, "promised"),
  y2020: cue(S, "2020"), but: cue(S, "But"), american: cue(S, "American"), guarantee: cue(S, "guarantee"),
  delivered: cue(S, "delivered"), all: cue(S, "all"), range: cue(S, "range"), shrunk: cue(S, "shrunk"),
  m620: cue(S, "620"), half: cue(S, "half"), so: cue(S, "So"), deposit: cue(S, "deposit"), place: cue(S, "place"),
  queue: cue(S, "queue"), numbers: cue(S, "numbers"), moving: cue(S, "moving"), thats: cue(S, "That's"),
  quarter2: cue(S, "quarter", 2), place2: cue(S, "place", 2), queue2: cue(S, "queue", 2),
};
const T1 = Q.car + 12; // money -> timeline (v2: holds NO ESCROW ~1 s longer)
const T2 = Q.but - 4; // timeline -> contract
const T3 = Q.range + 26; // contract -> range
const T4 = Q.place - 14; // range -> queue (the car drops into its slot on "place in the queue")
const T5 = Q.thats + 6; // board -> payoff

const ease = (f: number, a: number, b: number) => interpolate(f, [a, b], [0, 1], { ...CLAMP, easing: EASE_OUT });
const money = (v: number) => `$${Math.round(v).toLocaleString("en-US")}`;

const Rise: React.FC<{ at: number; left: number; top: number; size: number; color: string; children: React.ReactNode; frame: number; fps: number; font?: React.CSSProperties; stroke?: number; until?: number }> = ({
  at, left, top, size, color, children, frame, fps, font, stroke = 9, until = Infinity,
}) => {
  if (frame < at || frame >= until) return null;
  const s = pop(frame, at, fps, 210, 15);
  return (
    <div style={{ position: "absolute", left, top, ...(font ?? { ...HEADC, ...WS }), fontSize: size, color, opacity: interpolate(s, [0, 0.3], [0, 1], CLAMP),
      translate: `0 ${(1 - s) * 34}px`, ...(font ? {} : keyline(size / 150, stroke)) }}>{children}</div>
  );
};

// ------------------------------------------------------------------------------------------------ 1. the money
const Money: React.FC<{ frame: number; fps: number }> = ({ frame, fps }) => {
  if (frame >= T1 + 12) return null;
  const v = interpolate(frame, [Q.quarter, Q.upfront - 2], [5000, 250000], { ...CLAMP, easing: EASE_IN_OUT });
  const shown = frame < Q.quarter ? 5000 : Math.round(v / 1000) * 1000;
  const punch = frame >= Q.upfront - 2 ? interpolate(pop(frame, Q.upfront - 2, fps, 260, 10), [0, 1], [1.08, 1]) : 1;
  const out = interpolate(frame, [T1, T1 + 12], [0, 1], { ...CLAMP, easing: Easing.in(Easing.cubic) });
  const jets = interpolate(frame, [Q.thrusters - 2, Q.thrusters + 4, Q.thrusters + 26, Q.thrusters + 40], [0, 1, 1, 0], CLAMP);
  return (
    <AbsoluteFill style={{ scale: String(slowPush(frame, 0, T1, 1.04)), transformOrigin: "30% 50%", translate: `0 ${-out * 900}px`, opacity: 1 - out * 0.4 }}>
      <svg width={1920} height={1080} style={{ position: "absolute", inset: 0 }}>
        <ellipse cx={1500} cy={928} rx={560} ry={40} fill="#FFFFFF" opacity={0.07} />
        <line x1={980} y1={930} x2={1920} y2={930} stroke={GREY} strokeOpacity={0.35} strokeWidth={3} />
        <g transform="translate(1510 930) scale(0.9)">
          <Jet x={ROADSTER_NOZZLE.x} y={ROADSTER_NOZZLE.y} len={330} w={44} deg={90} frame={frame} seed={11} op={jets} />
          <Roadster />
        </g>
      </svg>
      <div style={{ position: "absolute", left: 150, top: 104, ...HEADC, ...WS, fontSize: 90, color: C.ink, ...keyline(0.6, 10) }}>TO RESERVE A ROADSTER</div>
      <div style={{ position: "absolute", left: 150, top: 200, ...HEADC, ...WS, fontSize: 90, color: C.cyan, ...keyline(0.6, 10) }}>WITH THRUSTERS</div>
      <div style={{ position: "absolute", left: 136, top: 316, ...HEADC, fontSize: 300, lineHeight: 0.86, color: C.acid, fontVariantNumeric: "tabular-nums",
        scale: String(punch), transformOrigin: "0% 50%", ...keyline(2, 10) }}>{money(shown)}</div>
      <Tag at={-30} until={Q.upfront - 2} left={150} top={608} bg={C.ink} size={60} style={WS}>PAID TODAY</Tag>
      <Tag at={Q.upfront - 2} left={150} top={608} bg={C.acid} size={60} rot={[8, -2]} style={WS}>UP FRONT</Tag>
      <Rise at={Q.quarter} until={Q.refundable - 2} left={156} top={716} size={44} color={C.ink} frame={frame} fps={fps} font={MONO}>$5,000 TODAY</Rise>
      <Rise at={Q.quarter + 4} until={Q.refundable - 2} left={156} top={772} size={44} color={C.ink} frame={frame} fps={fps} font={MONO}>+ $245,000 WITHIN 10 DAYS</Rise>
      <Rise at={Q.upfront + 4} until={Q.refundable - 2} left={156} top={828} size={44} color={GREY} frame={frame} fps={fps} font={MONO}>THRUST VERSION, US</Rise>
      <Tag at={Q.refundable - 2} left={150} top={712} bg={C.acid} size={62} rot={[-8, -2]} style={WS}>REFUNDABLE</Tag>
      <Tag at={Q.interest - 2} left={560} top={712} bg={C.warn} color={C.ink} size={62} rot={[8, 2]} style={WS}>NO INTEREST</Tag>
      <Tag at={Q.escrow - 2} left={1000} top={712} bg={C.warn} color={C.ink} size={62} rot={[-8, -1]} style={WS}>NO ESCROW</Tag>
      <EvidenceStamp kind="tesla" at={Q.refundable + 6} left={150} top={836} size={46} text="TESLA'S US AGREEMENT" note="RESERVATION AGREEMENT, CLAUSES 5–6" />
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ 2. the timeline
const AX = { y: 700, x0: 200, step: 136 };
const yx = (year: number) => AX.x0 + (year - 2017) * AX.step;
const Timeline: React.FC<{ frame: number; fps: number }> = ({ frame, fps }) => {
  if (frame < T1 || frame >= T2 + 14) return null;
  const draw = ease(frame, T1 + 2, T1 + 20);
  const arc = ease(frame, Q.promised - 4, Q.promised + 14);
  const gap = ease(frame, Q.y2020 + 8, Q.y2020 + 20);
  const pin = (at: number) => pop(frame, at, fps, 240, 11);
  const p28 = pin(Q.y2028 - 2);
  const p20 = pin(Q.y2020 - 2);
  const p17 = pin(Q.after + 2);
  const cover = interpolate(frame, [T2, T2 + 14], [0, 1], CLAMP);
  const ax = yx(2017) + (yx(2028) - yx(2017)) * draw;
  const arcPath = `M ${yx(2017)} ${AX.y - 16} C ${yx(2017) + 80} ${AX.y - 250}, ${yx(2020) - 80} ${AX.y - 250}, ${yx(2020)} ${AX.y - 24}`;
  return (
    <AbsoluteFill style={{ scale: String(slowPush(frame, T1, T2 + 14, 1.035)), transformOrigin: "50% 60%", opacity: 1 - cover * 0.6 }}>
      <svg width={1920} height={1080} style={{ position: "absolute", inset: 0 }}>
        <line x1={yx(2017)} y1={AX.y} x2={ax} y2={AX.y} stroke={C.black} strokeWidth={16} strokeLinecap="round" />
        <line x1={yx(2017)} y1={AX.y} x2={ax} y2={AX.y} stroke={C.ink} strokeWidth={8} strokeLinecap="round" />
        {Array.from({ length: 12 }).map((_, i) => {
          const x = yx(2017 + i);
          if (x > ax + 1) return null;
          return <line key={i} x1={x} y1={AX.y - 14} x2={x} y2={AX.y + 14} stroke={C.ink} strokeWidth={5} />;
        })}
        {/* the 2017 promise: an arc to a 2020 launch */}
        <path d={arcPath} fill="none" stroke={C.black} strokeWidth={14} strokeDasharray="1000" strokeDashoffset={1000 * (1 - arc)} strokeLinecap="round" />
        <path d={arcPath} fill="none" stroke={C.cyan} strokeWidth={7} strokeDasharray="1000" strokeDashoffset={1000 * (1 - arc)} strokeLinecap="round" />
        {p17 > 0.01 ? <circle cx={yx(2017)} cy={AX.y} r={20 * p17} fill={C.ink} stroke={C.black} strokeWidth={5} /> : null}
        {p20 > 0.01 ? <circle cx={yx(2020)} cy={AX.y} r={22 * p20} fill={C.cyan} stroke={C.black} strokeWidth={5} /> : null}
        {p28 > 0.01 ? (
          <g transform={`translate(${yx(2028)} ${AX.y}) scale(${p28})`}>
            <path d="M 0 0 C -34 -46, -34 -84, 0 -96 C 34 -84, 34 -46, 0 0 Z" fill={C.acid} stroke={C.black} strokeWidth={6} />
            <circle cx={0} cy={-62} r={13} fill={C.black} />
          </g>
        ) : null}
        {/* the gap */}
        {gap > 0.01 ? (
          <g opacity={gap}>
            <polyline points={`${yx(2020)},${AX.y + 104} ${yx(2020)},${AX.y + 124} ${yx(2020) + (yx(2028) - yx(2020)) * gap},${AX.y + 124} ${yx(2020) + (yx(2028) - yx(2020)) * gap},${AX.y + 104}`}
              fill="none" stroke={C.black} strokeWidth={14} />
            <polyline points={`${yx(2020)},${AX.y + 104} ${yx(2020)},${AX.y + 124} ${yx(2020) + (yx(2028) - yx(2020)) * gap},${AX.y + 124} ${yx(2020) + (yx(2028) - yx(2020)) * gap},${AX.y + 104}`}
              fill="none" stroke={C.warn} strokeWidth={7} />
          </g>
        ) : null}
      </svg>
      {Array.from({ length: 12 }).map((_, i) => {
        const yr = 2017 + i;
        const key = yr === 2017 || yr === 2020 || yr === 2028;
        return (
          <div key={yr} style={{ position: "absolute", left: yx(yr) - 60, top: AX.y + 26, width: 120, textAlign: "center", ...MONO, fontSize: 44,
            color: key ? C.ink : "#7E7896", opacity: ease(frame, T1 + 2 + i * 1.4, T1 + 10 + i * 1.4) }}>’{String(yr).slice(2)}</div>
        );
      })}
      <Rise at={Q.y2028 - 2} left={1300} top={350} size={200} color={C.acid} frame={frame} fps={fps} stroke={10}>2028</Rise>
      <Rise at={Q.y2028 + 4} left={1308} top={552} size={60} color={C.acid} frame={frame} fps={fps}>TESLA SAYS</Rise>
      <Rise at={Q.promised - 2} left={200} top={300} size={62} color={C.cyan} frame={frame} fps={fps}>PROMISED IN 2017:</Rise>
      <Rise at={Q.y2020 - 2} left={yx(2020) + 34} top={372} size={170} color={C.cyan} frame={frame} fps={fps} stroke={10}>2020</Rise>
      <Rise at={Q.y2020 + 12} left={(yx(2020) + yx(2028)) / 2 - 380} top={AX.y + 140} size={96} color={C.warn} frame={frame} fps={fps} stroke={10}>8 YEARS LATER</Rise>
      <Rise at={T1 + 6} left={150} top={110} size={96} color={C.ink} frame={frame} fps={fps} stroke={10}>LAUNCH DATE</Rise>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ 3. the contract
const SERIF = theme.fonts.serif;
const INK = "#111318";
const Mark: React.FC<{ p: number; color: string; children: React.ReactNode; text?: string }> = ({ p, color, children, text }) => (
  <span style={{ backgroundImage: `linear-gradient(${color}, ${color})`, backgroundRepeat: "no-repeat", backgroundSize: `${p * 100}% 100%`, color: text,
    boxDecorationBreak: "clone", WebkitBoxDecorationBreak: "clone", padding: "0 4px" }}>{children}</span>
);
const Contract: React.FC<{ frame: number; fps: number }> = ({ frame, fps }) => {
  if (frame < T2 || frame >= T3 + 12) return null;
  const inn = interpolate(frame, [T2, T2 + 12], [1, 0], { ...CLAMP, easing: EASE_OUT });
  const out = interpolate(frame, [T3, T3 + 12], [0, 1], { ...CLAMP, easing: Easing.in(Easing.cubic) });
  const under = ease(frame, Q.guarantee - 6, Q.guarantee + 10);
  const hi = interpolate(frame, [Q.delivered - 2, Q.all + 6], [0, 1], { ...CLAMP, easing: Easing.inOut(Easing.quad) });
  const uk = pop(frame, Q.all - 4, fps, 200, 15);
  return (
    <AbsoluteFill style={{ translate: `${inn * 1500 - out * 2100}px 0`, rotate: `${-1.4 + inn * 3}deg` }}>
      <AbsoluteFill style={{ scale: String(slowPush(frame, T2, T3, 1.04)), transformOrigin: "40% 45%" }}>
        <div style={{ position: "absolute", left: 70, top: 46, width: 2000, height: 1150, backgroundColor: "#FFFFFF", boxShadow: "0 30px 90px rgba(0,0,0,0.7)" }} />
        <div style={{ position: "absolute", left: 170, top: 120, ...MONO, fontSize: 44, color: "#5E6670" }}>TESLA ROADSTER RESERVATION AGREEMENT</div>
        <div style={{ position: "absolute", left: 1330, top: 112, padding: "4px 14px", border: `4px solid ${INK}`, ...MONO, fontSize: 44, color: INK }}>US v.20261015</div>
        <Tag at={Q.american - 2} left={1340} top={196} bg={C.cyan} size={56} style={WS}>THE US VERSION</Tag>
        <div style={{ position: "absolute", left: 170, top: 236, fontFamily: SERIF, fontWeight: 500, fontSize: 64, color: INK }}>4. Delivery</div>
        <div style={{ position: "absolute", left: 170, top: 352, width: 1640, fontFamily: SERIF, fontWeight: 500, fontSize: 60, lineHeight: 1.42, color: INK }}>
          …we <span style={{ textDecoration: under > 0.02 ? "underline" : "none", textDecorationColor: C.warn, textDecorationThickness: 8, textUnderlineOffset: 10 }}>cannot guarantee</span> when your vehicle will<br />
          actually be delivered <Mark p={hi} color={C.acid}>or if it will be delivered.</Mark>
        </div>
        {frame >= Q.all - 4 ? (
          <div style={{ position: "absolute", left: 170, top: 640, opacity: interpolate(uk, [0, 0.3], [0, 1], CLAMP), translate: `0 ${(1 - uk) * 30}px` }}>
            <div style={{ display: "inline-block", padding: "6px 16px 8px", backgroundColor: INK, color: C.ink, ...HEADC, ...WS, fontSize: 52 }}>THE UK VERSION</div>
            <div style={{ fontFamily: SERIF, fontWeight: 500, fontSize: 56, color: INK, marginTop: 28 }}>
              …will actually be delivered.{" "}
              <span style={{ color: "#A9B1BB", textDecoration: "line-through", textDecorationThickness: 5 }}>or if it will be delivered</span>
            </div>
          </div>
        ) : null}
        <Rise at={Q.all + 2} left={176} top={862} size={44} color="#5E6670" frame={frame} fps={fps} font={MONO}>CLAUSE 4, BOTH VERSIONS, ACCESSED 17 OCT 2026</Rise>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ 4. the range, 5-6. the queue
const BAR = { x0: 200, y: 540, h: 88, w: 1500 };
const mi = (m: number) => BAR.x0 + (BAR.w * m) / 620;
const QUEUE_Y = 950;
const SLOTS = 9;
const SLOT_W = 270;
const YOU = 4; // our car's slot in the line
const SLOT0 = -40;
const RangeAndQueue: React.FC<{ frame: number; fps: number }> = ({ frame, fps }) => {
  if (frame < T3) return null;
  const grow = ease(frame, T3 + 4, Q.m620);
  const shrink = interpolate(frame, [Q.half - 4, Q.half + 16], [0, 1], { ...CLAMP, easing: EASE_IN_OUT });
  const range = 620 * grow - (620 - 315) * shrink;
  const toQueue = interpolate(frame, [T4, T4 + 24], [0, 1], { ...CLAMP, easing: EASE_IN_OUT });
  const creep = Math.max(0, frame - (T4 + 24)) * 0.45;
  const endX = mi(range);
  // our car: rides the end of the range road, then drops into its slot in the queue
  const carX0 = endX - 4;
  const slotX = SLOT0 + YOU * SLOT_W + creep;
  const carX = carX0 + (slotX - carX0) * toQueue;
  const carY = BAR.y + (QUEUE_Y - BAR.y) * toQueue;
  const carS = 0.34 + (0.22 - 0.34) * toQueue;
  const travel = frame < Q.half - 4 ? range : 620 - (620 - range) * 1;
  const wheel = (travel * 2.4 + creep * 3) % 360;
  const rangeOp = 1 - toQueue;
  const ticks = [0, 100, 200, 300, 400, 500, 600];
  return (
    <AbsoluteFill>
      <svg width={1920} height={1080} style={{ position: "absolute", inset: 0 }}>
        <g opacity={rangeOp}>
          {/* the 2017 promise stays as a dashed ghost once the road shrinks */}
          {shrink > 0.01 ? <rect x={mi(315)} y={BAR.y} width={mi(620) - mi(315)} height={BAR.h} fill="none" stroke={C.ink} strokeOpacity={0.6} strokeWidth={5} strokeDasharray="20 14" /> : null}
          <rect x={BAR.x0} y={BAR.y} width={Math.max(0, endX - BAR.x0)} height={BAR.h} fill="#241A3A" stroke={C.black} strokeWidth={6} />
          <line x1={BAR.x0 + 20} y1={BAR.y + BAR.h / 2} x2={Math.max(BAR.x0 + 20, endX - 20)} y2={BAR.y + BAR.h / 2} stroke={BODY} strokeWidth={6} strokeDasharray="36 26" />
          <rect x={endX - 10} y={BAR.y - 8} width={10} height={BAR.h + 16} fill={shrink > 0.02 ? C.acid : C.cyan} stroke={C.black} strokeWidth={3} />
          {ticks.map((t) => (
            <g key={t} opacity={ease(frame, T3 + 4 + t / 40, T3 + 14 + t / 40)}>
              <line x1={mi(t)} y1={BAR.y + BAR.h + 10} x2={mi(t)} y2={BAR.y + BAR.h + 30} stroke={C.ink} strokeWidth={4} />
            </g>
          ))}
        </g>
        {/* the queue: everyone else who paid */}
        {Array.from({ length: SLOTS }).map((_, i) => {
          if (i === YOU) return null;
          const k = ease(frame, T4 + 6 + Math.abs(i - YOU) * 2, T4 + 22 + Math.abs(i - YOU) * 2);
          if (k <= 0.01) return null;
          const x = SLOT0 + i * SLOT_W + creep + (1 - k) * (i < YOU ? -300 : 300);
          return <g key={i} transform={`translate(${x} ${QUEUE_Y}) scale(0.22)`} opacity={k}><Roadster tint={GREY} wheelAngle={creep * 3} /></g>;
        })}
        {toQueue > 0.01 ? <line x1={0} y1={QUEUE_Y + 2} x2={1920} y2={QUEUE_Y + 2} stroke={GREY} strokeOpacity={0.35 * toQueue} strokeWidth={3} /> : null}
        <g transform={`translate(${carX} ${carY}) scale(${carS})`}><Roadster tint={toQueue > 0.5 ? C.acid : BODY} wheelAngle={wheel} /></g>
      </svg>
      <div style={{ opacity: interpolate(frame, [T4, T4 + 10], [1, 0], CLAMP), translate: `${-ease(frame, T4, T4 + 12) * 120}px 0` }}>
        <Rise at={T3 + 2} left={150} top={120} size={120} color={C.ink} frame={frame} fps={fps} stroke={10}>RANGE</Rise>
        {ticks.map((t) => (
          <div key={t} style={{ position: "absolute", left: mi(t) - 70, top: BAR.y + BAR.h + 36, width: 140, textAlign: "center", ...MONO, fontSize: 44, color: "#9C93B3",
            opacity: ease(frame, T3 + 4 + t / 40, T3 + 14 + t / 40) }}>{t}</div>
        ))}
        <Rise at={Q.m620 - 2} left={mi(620) - 760} top={BAR.y - 132} size={64} color={C.cyan} frame={frame} fps={fps}>PROMISED IN 2017: 620 MI</Rise>
        <Rise at={Q.half - 2} left={150} top={770} size={92} color={C.acid} frame={frame} fps={fps} stroke={10}>NOW: ABOUT 310–320 MI</Rise>
        <Tag at={Q.half + 8} left={mi(470) - 110} top={BAR.y + 8} bg={C.warn} color={C.ink} size={56} style={WS}>ABOUT HALF</Tag>
        <Rise at={Q.half + 10} left={156} top={892} size={44} color={GREY} frame={frame} fps={fps} font={MONO}>SOURCES: TESLA (2017), TOP GEAR (OCT 2026)</Rise>
      </div>
      <Tag at={T4 + 26} left={slotX - 130} top={QUEUE_Y - 150} bg={C.acid} size={52} rot={[-10, -3]} style={WS}>YOUR PLACE</Tag>
    </AbsoluteFill>
  );
};

// A split-flap tile: cycles through characters, then lands on its own.
const LETTERS = "ABCDEFGHIJKLMNOPRSTUVWXYZ";
const DIGITS = "0123456789";
const Flap: React.FC<{ ch: string; frame: number; land: number; seed: string; w: number; h: number; size: number; color?: string; wobble?: number[]; wpool?: string }> = ({
  ch, frame, land, seed, w, h, size, color = C.ink, wobble = [], wpool,
}) => {
  const moving = wobble.some((m) => frame >= m && frame < m + 7);
  const pool = moving && frame >= land && wpool ? wpool : /[0-9]/.test(ch) ? DIGITS : /[A-Z]/.test(ch) ? LETTERS : "";
  const cycling = (frame < land || moving) && pool !== "";
  const shown = cycling ? pool[Math.floor(random(`${seed}-${Math.floor(frame / 2)}`) * pool.length)] : ch;
  return (
    <div style={{ position: "relative", width: w, height: h, backgroundColor: ch === " " ? "rgba(17,20,26,0.55)" : "#11141A", border: `3px solid ${C.black}`, borderRadius: 6,
      display: "flex", alignItems: "center", justifyContent: "center", ...HEADC, fontSize: size, lineHeight: 1, color: cycling ? "#9AA3AD" : color, fontVariantNumeric: "tabular-nums" }}>
      {shown}
      <div style={{ position: "absolute", left: 0, right: 0, top: h / 2 - 2, height: 3, backgroundColor: "rgba(0,0,0,0.7)" }} />
    </div>
  );
};
const FlapRow: React.FC<{ text: string; frame: number; land: number; seed: string; w: number; h: number; size: number; color?: string; wobble?: number[]; wobbleAt?: number[]; wpool?: string; gap?: number }> = ({
  text, frame, land, seed, w, h, size, color, wobble = [], wobbleAt = [], wpool, gap = 6,
}) => (
  <div style={{ display: "flex", gap }}>
    {text.split("").map((ch, i) => (
      <Flap key={i} ch={ch} frame={frame} land={land + i * 2} seed={`${seed}${i}`} w={w} h={h} size={size} color={color}
        wobble={wobbleAt.includes(i) ? wobble : []} wpool={wpool} />
    ))}
  </div>
);

const ROWS = [
  { label: "LAUNCH", value: "2020 → 2028", c: C.cyan, moving: [10], pool: "89" },
  { label: "RANGE", value: "620 → ~315 MI", c: C.cyan, moving: [9], pool: "0123456789" },
  { label: "PRICE", value: "NOT ANNOUNCED", c: C.ink, moving: [], pool: "" },
  { label: "DELIVERY", value: "NOT GUARANTEED", c: C.warn, moving: [], pool: "" },
  { label: "STATUS", value: "DESIGN DEVELOPMENT", c: C.acid, moving: [], pool: "" },
];
const Board: React.FC<{ frame: number; fps: number }> = ({ frame, fps }) => {
  if (frame < T4 + 12 || frame >= T5 + 10) return null;
  const out = interpolate(frame, [T5, T5 + 10], [0, 1], { ...CLAMP, easing: Easing.in(Easing.cubic) });
  const wob = [Q.numbers, Q.numbers + 10, Q.numbers + 20, Q.moving, Q.moving + 10];
  return (
    <AbsoluteFill style={{ translate: `0 ${-out * 700}px` }}>
      {ROWS.map((r, i) => {
        const at = T4 + 14 + i * 5;
        const k = pop(frame, at, fps, 220, 15);
        return (
          <div key={r.label} style={{ position: "absolute", left: 150, top: 150 + i * 106, display: "flex", alignItems: "center", gap: 36,
            opacity: interpolate(k, [0, 0.3], [0, 1], CLAMP), translate: `${(1 - k) * -50}px 0` }}>
            <div style={{ width: 330, ...HEADC, fontSize: 64, color: C.ink, ...keyline(0.43, 9) }}>{r.label}</div>
            <FlapRow text={r.value} frame={frame} land={at + 6} seed={`r${i}`} w={r.value.length > 15 ? 62 : 70} h={88} size={60} color={r.c} wobble={wob}
              wobbleAt={r.moving} wpool={r.pool || undefined} />
          </div>
        );
      })}
      <Rise at={Q.numbers - 4} left={156} top={688} size={44} color={GREY} frame={frame} fps={fps} font={MONO}>THE NUMBERS ON THE CAR YOU&apos;RE QUEUING FOR</Rise>
      <Rise at={Q.numbers + 4} left={156} top={740} size={40} color={GREY} frame={frame} fps={fps} font={MONO}>STATUS: TESLA&apos;S Q3 2026 UPDATE, 21 OCT</Rise>
    </AbsoluteFill>
  );
};

const Payoff: React.FC<{ frame: number; fps: number }> = ({ frame, fps }) => {
  if (frame < T5) return null;
  const line = pop(frame, Q.place2 - 2, fps, 210, 15);
  return (
    <AbsoluteFill style={{ scale: String(slowPush(frame, T5, T5 + 140, 1.04)), transformOrigin: "30% 40%" }}>
      <div style={{ position: "absolute", left: 150, top: 160 }}>
        <FlapRow text="$250,000" frame={frame} land={Q.quarter2 + 2} seed="pay" w={196} h={262} size={226} color={C.acid} gap={10} />
      </div>
      {frame >= Q.place2 - 2 ? (
        <div style={{ position: "absolute", left: 150, top: 486, opacity: interpolate(line, [0, 0.3], [0, 1], CLAMP), translate: `0 ${(1 - line) * 34}px` }}>
          <div style={{ ...HEADC, ...WS, fontSize: 132, color: C.ink, ...keyline(0.88, 10) }}>FOR A PLACE</div>
          <div style={{ ...HEADC, ...WS, fontSize: 132, color: C.ink, marginTop: 4, ...keyline(0.88, 10) }}>IN A QUEUE</div>
        </div>
      ) : null}
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ the segment
export const S7Deposit: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill style={{ background: BG_NIGHT, overflow: "hidden" }}>
      <Money frame={frame} fps={fps} />
      <Timeline frame={frame} fps={fps} />
      <RangeAndQueue frame={frame} fps={fps} />
      <Board frame={frame} fps={fps} />
      <Payoff frame={frame} fps={fps} />
      <Contract frame={frame} fps={fps} />

      <Sfx at={Q.thrusters - 2} name="hiss" volume={0.35} dur={40} />
      <Sfx at={Q.quarter} name="tick_run" volume={0.3} dur={Q.upfront - Q.quarter} />
      <Sfx at={Q.upfront - 2} name="thock" volume={0.6} />
      <Sfx at={T1} name="whoosh" volume={0.4} />
      <Sfx at={Q.y2028 - 2} name="thock" volume={0.5} />
      <Sfx at={Q.promised - 4} name="form" volume={0.35} />
      <Sfx at={Q.y2020 - 2} name="thock" volume={0.45} />
      <Sfx at={T2} name="whoosh" volume={0.45} />
      <Sfx at={T2 + 10} name="thock" volume={0.5} />
      <Sfx at={Q.delivered - 2} name="tick_run" volume={0.25} dur={26} />
      <Sfx at={T3} name="whoosh" volume={0.4} />
      <Sfx at={Q.half - 4} name="rewind" volume={0.4} />
      <Sfx at={T4} name="settle" volume={0.4} />
      <Sfx at={T4 + 14} name="tick_run" volume={0.25} dur={34} />
      <Sfx at={Q.numbers} name="tick_run" volume={0.25} dur={36} />
      <Sfx at={T5} name="whoosh" volume={0.35} />
      <Sfx at={Q.quarter2} name="tick_run" volume={0.3} dur={24} />
      <Sfx at={Q.place2 - 2} name="thock" volume={0.55} />
    </AbsoluteFill>
  );
};
