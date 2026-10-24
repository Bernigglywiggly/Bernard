import type React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { CLAMP, EASE_OUT } from "../../lib/anim";
import { BG_NIGHT, C, ClipScene, HEADC, Headline, keyline, MONO, pop, Sfx, slowPush, Stamp, Tag } from "../kit";
import { Disclose, HoldStill, M, Shade, TeslaCredit } from "./fx";
import { cue, segFrames } from "./util";

// Roadster film S4 "Seconds, then hours" (Short 3's story in 16:9). Facts: TESLA_ROADSTER_FACTS.md §4-§5: two COPVs
// 600 L (about 250 kg of air); OUR ESTIMATE: 80 kN / ~600 m/s exhaust = ~130 kg/s, so ~2 s at full rear thrust;
// Thrust version: one launch per fill, ~5 s of push (Moravy to Top Gear, S1); refill 2-6 h from a high-pressure
// nitrogen rig today, target under 30 min (S1); Musk on stage: the car can refill its own tank (P1 12:30).
const D = segFrames("S4");
const T = {
  handful: cue("S4", "handful"), squeezed: cue("S4", "squeezed"), by: cue("S4", "by"), empty: cue("S4", "empty"), two: cue("S4", "two"),
  tesla: cue("S4", "tesla", 2), single: cue("S4", "single"), five: cue("S4", "five"), but: cue("S4", "but"), lars: cue("S4", "lars"),
  hours: cue("S4", "hours"), target: cue("S4", "target"), elon: cue("S4", "elon"), refill: cue("S4", "refill", 2), long: cue("S4", "long"),
  so: cue("S4", "so"), seconds: cue("S4", "seconds", 3), waits: cue("S4", "waits"),
};
const X = { drain: T.by, quote: T.tesla, clock: T.but, split: T.elon, payoff: T.so };

const Opening: React.FC = () => {
  const frame = useCurrentFrame();
  if (frame >= X.drain) return null;
  return (
    <AbsoluteFill>
      <Shade from="left" strength={0.7} />
      <Headline at={T.handful - 6} left={M} top={230} lines={[{ text: "A HANDFUL OF", size: 140 }, { text: "SECONDS IN THE AIR", size: 140, color: C.acid }]} />
      <Tag at={T.squeezed} left={M} top={600} bg={C.cyan} size={72}>ITS FUEL: A TANK OF SQUEEZED GAS</Tag>
    </AbsoluteFill>
  );
};

// both tanks drain in about two real seconds at full rear thrust (OUR ESTIMATE)
const Drain: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < X.drain || frame >= X.quote) return null;
  const level = interpolate(frame, [T.empty, T.empty + 2 * fps], [1, 0], CLAMP);
  const done = pop(frame, T.empty + 2 * fps, fps, 240, 10);
  const tank = (y: number, label: string, w: number) => (
    <div style={{ position: "absolute", left: M, top: y }}>
      <div style={{ ...HEADC, fontSize: 60, color: C.ink, ...keyline(0.42, 8) }}>{label}</div>
      <div style={{ marginTop: 12, width: w, height: 120, borderRadius: 60, border: "7px solid #000", backgroundColor: "rgba(255,255,255,0.12)", overflow: "hidden" }}>
        <div style={{ width: `${level * 100}%`, height: "100%", backgroundColor: level > 0.25 ? C.cyan : C.warn }} />
      </div>
    </div>
  );
  return (
    <AbsoluteFill style={{ background: BG_NIGHT, scale: slowPush(frame, X.drain, X.quote, 1.04), transformOrigin: "40% 50%" }}>
      <Headline at={X.drain + 2} left={M} top={70} lines={[{ text: "REAR NOZZLES AT FULL POWER", size: 92 }]} />
      {tank(250, "SEAT TANK · 400 L", 1100)}
      {tank(500, "REAR TANK · 200 L", 550)}
      <div style={{ position: "absolute", right: M, top: 260, textAlign: "right" }}>
        <div style={{ ...HEADC, fontSize: 200, color: level > 0 ? C.ink : C.warn, fontVariantNumeric: "tabular-nums", ...keyline(1.3, 11) }}>
          {(2 * (1 - level)).toFixed(1)} s
        </div>
      </div>
      <div style={{ position: "absolute", left: M, top: 760, ...HEADC, fontSize: 84, color: C.warn, opacity: interpolate(done, [0, 0.3], [0, 1], CLAMP),
        scale: interpolate(done, [0, 1], [1.3, 1]), transformOrigin: "0% 50%", ...keyline(0.6, 10) }}>EMPTY IN ABOUT TWO SECONDS</div>
      <div style={{ position: "absolute", left: M, top: 880, ...MONO, fontSize: 32, color: "#D2CBE3" }}>OUR ESTIMATE: 80 kN ÷ ≈600 m/s GAS SPEED ≈ 130 kg A SECOND, FROM ≈250 kg</div>
    </AbsoluteFill>
  );
};

const QuoteScene: React.FC = () => {
  const frame = useCurrentFrame();
  if (frame < X.quote || frame >= X.clock) return null;
  const a = interpolate(frame, [T.single - 6, T.single + 6], [0, 1], CLAMP);
  const b = interpolate(frame, [T.five - 6, T.five + 6], [0, 1], CLAMP);
  return (
    <AbsoluteFill>
      <Shade from="left" strength={0.85} />
      <div style={{ position: "absolute", left: M, top: 180, ...MONO, fontSize: 38, color: "#D2CBE3" }}>TESLA TO TOP GEAR, ON THE THRUST VERSION</div>
      <div style={{ position: "absolute", left: M, top: 260, ...HEADC, fontSize: 170, color: C.ink, opacity: a, translate: `0 ${(1 - a) * 30}px`, ...keyline(1.1, 11) }}>
        ONE LAUNCH PER FILL
      </div>
      <div style={{ position: "absolute", left: M, top: 470, ...HEADC, fontSize: 120, color: C.acid, opacity: b, translate: `0 ${(1 - b) * 30}px`, ...keyline(0.8, 10) }}>
        ≈5 SECONDS OF PUSH
      </div>
    </AbsoluteFill>
  );
};

// the refill: a clock face sweeping two to six hours
const Clock: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < X.clock || frame >= X.split) return null;
  const sweep = interpolate(frame, [T.hours - 30, T.hours + 10], [0, 6], { ...CLAMP, easing: EASE_OUT });
  const tgt = pop(frame, T.target, fps, 220, 12);
  const a = (sweep / 12) * 2 * Math.PI;
  const r = 280;
  const arc = (h0: number, h1: number) => {
    const p = (h: number) => [Math.sin((h / 12) * 2 * Math.PI) * (r - 40), -Math.cos((h / 12) * 2 * Math.PI) * (r - 40)];
    const [x0, y0] = p(h0); const [x1, y1] = p(h1);
    return `M ${x0} ${y0} A ${r - 40} ${r - 40} 0 ${h1 - h0 > 6 ? 1 : 0} 1 ${x1} ${y1}`;
  };
  return (
    <AbsoluteFill style={{ background: BG_NIGHT, scale: slowPush(frame, X.clock, X.split, 1.04), transformOrigin: "30% 50%" }}>
      <svg width={1920} height={1080} style={{ position: "absolute", inset: 0 }}>
        <g transform="translate(480 560)">
          <circle r={r} fill="#0B0F17" stroke={C.ink} strokeWidth={10} />
          {Array.from({ length: 12 }).map((_, i) => {
            const t = (i / 12) * 2 * Math.PI;
            return <line key={i} x1={Math.sin(t) * r * 0.82} y1={-Math.cos(t) * r * 0.82} x2={Math.sin(t) * r * 0.94} y2={-Math.cos(t) * r * 0.94} stroke={C.ink} strokeWidth={8} />;
          })}
          {sweep > 2 ? <path d={arc(2, Math.max(2.01, sweep))} fill="none" stroke={C.warn} strokeWidth={40} opacity={0.85} /> : null}
          <line x1={0} y1={0} x2={Math.sin(a) * r * 0.75} y2={-Math.cos(a) * r * 0.75} stroke={C.acid} strokeWidth={14} strokeLinecap="round" />
          <circle r={18} fill={C.acid} stroke="#000" strokeWidth={5} />
        </g>
      </svg>
      <div style={{ position: "absolute", left: 860, top: 200 }}>
        <div style={{ ...MONO, fontSize: 36, color: "#D2CBE3" }}>LARS MORAVY, TESLA VEHICLE ENGINEERING</div>
        <div style={{ ...HEADC, fontSize: 78, color: C.ink, marginTop: 12, ...keyline(0.6, 9) }}>REFILL FROM A NITROGEN RIG</div>
        <div style={{ ...HEADC, fontSize: 200, color: C.warn, lineHeight: 0.9, opacity: interpolate(frame, [T.hours - 6, T.hours + 4], [0, 1], CLAMP), ...keyline(1.3, 11) }}>2–6 HOURS</div>
        <div style={{ display: "inline-block", marginTop: 26, padding: "8px 20px 10px", backgroundColor: C.cyan, color: C.black, border: "4px solid #000", ...HEADC,
          fontSize: 70, scale: tgt, transformOrigin: "0% 50%" }}>HIS TARGET: UNDER 30 MIN</div>
      </div>
    </AbsoluteFill>
  );
};

const Split: React.FC = () => {
  const frame = useCurrentFrame();
  if (frame < X.split || frame >= X.payoff) return null;
  const right = interpolate(frame, [T.long - 20, T.long - 8], [0, 1], CLAMP);
  return (
    <AbsoluteFill style={{ background: BG_NIGHT }}>
      <div style={{ position: "absolute", left: 0, top: 0, width: 960, height: 1080, background: "rgba(255,43,214,0.08)" }} />
      <div style={{ position: "absolute", left: M, top: 230, width: 760 }}>
        <div style={{ ...MONO, fontSize: 38, color: "#D2CBE3" }}>MUSK, ON STAGE</div>
        <div style={{ ...HEADC, whiteSpace: "normal", fontSize: 110, color: C.ink, lineHeight: 1, marginTop: 14, ...keyline(0.8, 10) }}>THE CAR REFILLS ITS OWN TANK</div>
      </div>
      <div style={{ position: "absolute", left: 1060, top: 230, width: 760, opacity: right }}>
        <div style={{ ...MONO, fontSize: 38, color: "#D2CBE3" }}>HIS ENGINEER, TO TOP GEAR</div>
        <div style={{ ...HEADC, whiteSpace: "normal", fontSize: 110, color: C.ink, lineHeight: 1, marginTop: 14, ...keyline(0.8, 10) }}>2–6 HOURS ON A RIG</div>
      </div>
      <div style={{ position: "absolute", left: 930, top: 300, ...HEADC, fontSize: 90, color: C.acid, ...keyline(0.6, 9) }}>VS</div>
      <Stamp at={T.long} left={M} top={640} size={110}>UNPROVEN</Stamp>
    </AbsoluteFill>
  );
};

const Payoff: React.FC = () => {
  const frame = useCurrentFrame();
  if (frame < X.payoff) return null;
  return (
    <AbsoluteFill>
      <Shade from="left" strength={0.75} />
      <Headline at={T.seconds - 8} left={M} top={250} lines={[{ text: "IT FLIES FOR SECONDS", size: 150, color: C.acid }]} />
      <Headline at={T.waits - 4} left={M} top={470} lines={[{ text: "THEN WAITS FOR HOURS", size: 150, color: C.warn }]} />
    </AbsoluteFill>
  );
};

export const S4Seconds: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: C.black }}>
    <ClipScene src="film/kick_under_slow.mp4" from={0} dur={X.drain} push={[1, 1.06]} />
    <HoldStill src="film/blender_xray_last.png" from={X.quote} dur={X.clock - X.quote} push={[1.02, 1.07]} />
    <ClipScene src="film/hang_slow8.mp4" from={X.payoff} dur={D - X.payoff} push={[1.02, 1.06]} origin="45% 40%" />
    <Opening />
    <Drain />
    <QuoteScene />
    <Clock />
    <Split />
    <Payoff />
    <Disclose show={[[X.quote, X.clock]]} />
    <TeslaCredit show={[[0, X.drain], [X.payoff, D]]} />
    <Sfx at={X.drain} name="whoosh" volume={0.35} />
    <Sfx at={T.empty} name="hiss" volume={0.55} dur={60} />
    <Sfx at={T.empty + 60} name="thock" volume={0.6} />
    <Sfx at={X.quote} name="whoosh" volume={0.3} />
    <Sfx at={X.clock} name="whoosh" volume={0.35} />
    <Sfx at={T.hours - 30} name="tick_run" volume={0.25} dur={40} />
    <Sfx at={T.target} name="thock" volume={0.5} />
    <Sfx at={X.split} name="whoosh" volume={0.35} />
    <Sfx at={T.long} name="thock" volume={0.75} />
    <Sfx at={X.payoff} name="whoosh" volume={0.35} />
  </AbsoluteFill>
);
