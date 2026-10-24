import type React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { CLAMP, EASE_OUT } from "../../lib/anim";
import { BG_NIGHT, C, ClipScene, HEADC, Headline, keyline, MONO, pop, Sfx, slowPush, Stamp, Tag } from "../kit";
import { M, Shade, TeslaCredit } from "./fx";
import { cue, segFrames } from "./util";

// Roadster film S3 "0.81 seconds" (Short 2's story in 16:9). Facts: TESLA_ROADSTER_FACTS.md P4 (0.81 s, Tesla's own
// timing), §3 (Performance under 1.6 s, claimed), C5 (Rimac Nevera R 1.66 s, Dewesoft-verified), P1 19:00-19:04 (Musk:
// production car quicker; the limit is not detaching the driver's retinas). Lanes on one true distance scale: from rest
// to 60 mph at constant acceleration the Roadster covers 10.9 m and the Rimac 22.3 m.
const D = segFrames("S3");
const T = {
  t081: cue("S3", "0.81"), version: cue("S3", "the", 2), gap: cue("S3", "gap"), compressed: cue("S3", "compressed"), half: cue("S3", "half"),
  rimac: cue("S3", "rematz"), indep: cue("S3", "independently"), but: cue("S3", "but"), nobody: cue("S3", "nobody"), musk: cue("S3", "musk"),
  quicker: cue("S3", "quicker"), retinas: cue("S3", "retinas."), so: cue("S3", "so", 2), attached: cue("S3", "attached."),
};
const X = { bars: T.version, race: T.half - 10, watch: T.but, musk: T.musk, payoff: T.so };

const Watch: React.FC<{ secs: number; r: number }> = ({ secs, r }) => {
  const a = secs * 2 * Math.PI;
  const sector = secs <= 0 ? "" : `M 0 0 L 0 ${-(r - 20)} A ${r - 20} ${r - 20} 0 ${secs > 0.5 ? 1 : 0} 1 ${Math.sin(a) * (r - 20)} ${-Math.cos(a) * (r - 20)} Z`;
  return (
    <g>
      <rect x={-r * 0.13} y={-r * 1.32} width={r * 0.26} height={r * 0.2} rx={r * 0.04} fill="#C9CFD6" stroke="#000" strokeWidth={6} />
      <circle r={r * 1.08} fill="#C9CFD6" stroke="#000" strokeWidth={8} />
      <circle r={r} fill="#0B0F17" stroke="#000" strokeWidth={6} />
      {Array.from({ length: 20 }).map((_, i) => {
        const t = (i / 20) * Math.PI * 2 - Math.PI / 2;
        const long = i % 5 === 0;
        return <line key={i} x1={Math.cos(t) * r * (long ? 0.8 : 0.88)} y1={Math.sin(t) * r * (long ? 0.8 : 0.88)} x2={Math.cos(t) * r * 0.96} y2={Math.sin(t) * r * 0.96}
          stroke={long ? C.ink : "#7C8794"} strokeWidth={long ? 8 : 5} />;
      })}
      {sector ? <path d={sector} fill={C.acid} opacity={0.22} /> : null}
      <line x1={0} y1={0} x2={Math.sin(a) * r * 0.86} y2={-Math.cos(a) * r * 0.86} stroke={C.acid} strokeWidth={Math.max(8, r * 0.05)} strokeLinecap="round" />
      <circle r={Math.max(12, r * 0.07)} fill={C.acid} stroke="#000" strokeWidth={5} />
    </g>
  );
};

const Readout: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame >= X.bars && frame < X.payoff) return null;
  const n = pop(frame, frame < X.bars ? T.t081 : X.payoff + 4, fps, 220, 12);
  const clip = pop(frame, T.attached - 6, fps, 240, 9);
  const secs = frame >= X.payoff ? interpolate(frame, [T.attached - 30, T.attached - 6], [0, 0.81], CLAMP) : 0;
  return (
    <AbsoluteFill>
      <Shade from="left" strength={0.7} />
      <div style={{ position: "absolute", left: M, top: 230, opacity: interpolate(n, [0, 0.3], [0, 1], CLAMP), translate: `0 ${(1 - n) * -40}px` }}>
        <div style={{ ...HEADC, fontSize: 90, color: C.cyan, ...keyline(0.6, 9) }}>0–60 MPH</div>
        <div style={{ ...HEADC, fontSize: 330, color: C.acid, lineHeight: 0.86, ...keyline(2.2, 12) }}>0.81<span style={{ fontSize: 170, marginLeft: 14 }}>s</span></div>
        <div style={{ display: "inline-block", marginTop: 16, padding: "8px 18px 10px", backgroundColor: C.ink, color: C.black, ...HEADC, fontSize: 56,
          border: "4px solid #000" }}>{frame >= X.payoff ? "A PROMISE WITH A STOPWATCH ATTACHED" : "TESLA'S OWN TIMING"}</div>
      </div>
      {frame >= X.payoff ? (
        <svg width={1920} height={1080} style={{ position: "absolute", inset: 0 }}>
          <g transform={`translate(${interpolate(clip, [0, 1], [1500, 980])} ${interpolate(clip, [0, 1], [560, 330])}) rotate(${interpolate(clip, [0, 1], [0, 14])}) scale(${interpolate(clip, [0, 1], [1, 0.6])})`}>
            <Watch secs={secs} r={170} />
          </g>
        </svg>
      ) : null}
    </AbsoluteFill>
  );
};

// with thrusters vs without: the gap is the gas
const Bars: React.FC = () => {
  const frame = useCurrentFrame();
  if (frame < X.bars || frame >= X.race) return null;
  const k = interpolate(frame, [X.bars + 10, X.bars + 40], [0, 1], { ...CLAMP, easing: EASE_OUT });
  const g = interpolate(frame, [T.gap, T.gap + 12], [0, 1], { ...CLAMP, easing: EASE_OUT });
  const W = 1000; // px for 1.6 s
  const row = (y: number, label: string, sub: string, secs: number, color: string, txt: string) => (
    <div style={{ position: "absolute", left: M, top: y }}>
      <div style={{ ...HEADC, fontSize: 72, color, ...keyline(0.5, 8) }}>{label}</div>
      <div style={{ ...MONO, fontSize: 32, color: "#D2CBE3", marginTop: 4 }}>{sub}</div>
      <div style={{ display: "flex", alignItems: "center", gap: 24, marginTop: 14 }}>
        <div style={{ width: (W * secs * k) / 1.6, height: 90, backgroundColor: color, border: "6px solid #000" }} />
        <div style={{ ...HEADC, fontSize: 110, color, opacity: k, ...keyline(0.8, 10) }}>{txt}</div>
      </div>
    </div>
  );
  return (
    <AbsoluteFill style={{ background: BG_NIGHT, scale: slowPush(frame, X.bars, X.race, 1.04), transformOrigin: "40% 50%" }}>
      <Headline at={X.bars + 2} left={M} top={80} lines={[{ text: "WITH THE GAS AND WITHOUT IT", size: 100 }]} />
      {row(260, "WITH THRUSTERS", "THE DEMO, TESLA'S OWN TIMING", 0.81, C.acid, "0.81 s")}
      {row(560, "WITHOUT THRUSTERS", "THE PERFORMANCE VERSION, TESLA'S CLAIM", 1.6, "#8FA3B8", "<1.6 s")}
      <div style={{ position: "absolute", left: M + (W * 0.81) / 1.6, top: 800, width: W - (W * 0.81) / 1.6, height: 30, borderBottom: `6px solid ${C.cyan}`,
        borderLeft: `6px solid ${C.cyan}`, borderRight: `6px solid ${C.cyan}`, opacity: g }} />
      <div style={{ position: "absolute", left: M + (W * 0.81) / 1.6 + 20, top: 860, ...HEADC, fontSize: 80, color: C.cyan, opacity: g, ...keyline(0.55, 9) }}>
        THE GAP = COMPRESSED GAS
      </div>
      <div style={{ position: "absolute", left: M + (W * 0.81) / 1.6 + 24, top: 960, ...MONO, fontSize: 30, color: "#D2CBE3", opacity: g }}>OUR READING OF TESLA&apos;S NUMBERS</div>
    </AbsoluteFill>
  );
};

// one true distance scale: Roadster 10.9 m to 60 mph, Rimac 22.3 m; 1 s of real time = 2.4 s on screen
const Car: React.FC<{ color: string }> = ({ color }) => (
  <svg width={300} height={100} viewBox="0 0 190 64">
    <path d="M 8 44 C 10 30, 40 24, 70 20 C 92 8, 128 8, 150 22 C 170 26, 184 32, 184 44 Z" fill={color} stroke="#000" strokeWidth={5} strokeLinejoin="round" />
    <circle cx={50} cy={46} r={14} fill="#15181D" stroke="#000" strokeWidth={4} />
    <circle cx={146} cy={46} r={14} fill="#15181D" stroke="#000" strokeWidth={4} />
  </svg>
);
const Race: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < X.race || frame >= X.watch) return null;
  const v = 26.82;
  const x0 = 260, x1 = 1700;
  const xOf = (d: number) => x0 + ((x1 - x0) * d) / 22.3;
  const real = Math.max(0, (frame - (X.race + 16)) / fps / 2.4);
  const lanes = [
    { name: "TESLA ROADSTER", t: 0.81, color: C.ink, tcol: C.acid, note: "TESLA'S OWN TIMING", y: 230 },
    { name: "RIMAC NEVERA R", t: 1.66, color: "#8FA3B8", tcol: C.ink, note: "INDEPENDENTLY TIMED (DEWESOFT)", y: 600 },
  ];
  return (
    <AbsoluteFill style={{ background: BG_NIGHT, scale: slowPush(frame, X.race, X.watch, 1.03), transformOrigin: "50% 50%" }}>
      <Headline at={X.race + 2} left={M} top={70} lines={[{ text: "ABOUT HALF THE TIME", size: 100, color: C.acid }]} />
      {lanes.map((ln) => {
        const a = v / ln.t;
        const flag = 0.5 * v * ln.t;
        const d = real <= ln.t ? 0.5 * a * real * real : flag + v * (real - ln.t);
        const done = real >= ln.t;
        return (
          <div key={ln.name} style={{ position: "absolute", left: 0, top: ln.y, width: 1920, height: 330 }}>
            <div style={{ position: "absolute", left: M, top: 0, ...HEADC, fontSize: 64, color: ln.color, ...keyline(0.45, 8) }}>{ln.name}</div>
            <div style={{ position: "absolute", left: M, top: 210, width: 1720, height: 8, backgroundColor: "rgba(255,255,255,0.3)" }} />
            <div style={{ position: "absolute", left: xOf(flag) - 5, top: 110, width: 10, height: 108, backgroundColor: C.magenta, border: "3px solid #000" }} />
            <div style={{ position: "absolute", left: xOf(flag) - 80, top: 72, width: 160, textAlign: "center", ...HEADC, fontSize: 36, color: C.magenta, ...keyline(0.24, 7) }}>60 MPH</div>
            <div style={{ position: "absolute", left: Math.min(xOf(d), 1900) - 300, top: 116 }}><Car color={ln.color} /></div>
            <div style={{ position: "absolute", left: M, top: 236, ...HEADC, fontSize: 84, color: done ? ln.tcol : "rgba(255,255,255,0.75)", fontVariantNumeric: "tabular-nums",
              ...keyline(0.6, 9) }}>{Math.min(real, ln.t).toFixed(2)} s</div>
            <div style={{ position: "absolute", left: 420, top: 262, ...HEADC, fontSize: 44, color: ln.tcol, opacity: done ? 1 : 0, ...keyline(0.3, 7) }}>{ln.note}</div>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

const StopwatchScene: React.FC = () => {
  const frame = useCurrentFrame();
  if (frame < X.watch || frame >= X.musk) return null;
  const secs = interpolate(frame, [X.watch + 6, X.watch + 30], [0, 0.81], CLAMP);
  return (
    <AbsoluteFill style={{ background: BG_NIGHT, scale: slowPush(frame, X.watch, X.musk, 1.05), transformOrigin: "35% 50%" }}>
      <svg width={1920} height={1080} style={{ position: "absolute", inset: 0 }}><g transform="translate(560 560)"><Watch secs={secs} r={300} /></g></svg>
      <Tag at={X.watch + 10} left={960} top={220} bg={C.ink} size={70}>TESLA&apos;S OWN STOPWATCH</Tag>
      <Stamp at={T.nobody} left={960} top={460} size={92}>NOT INDEPENDENTLY<br />TIMED</Stamp>
    </AbsoluteFill>
  );
};

const MuskQuote: React.FC = () => {
  const frame = useCurrentFrame();
  if (frame < X.musk || frame >= X.payoff) return null;
  const q1 = interpolate(frame, [T.quicker - 6, T.quicker + 6], [0, 1], CLAMP);
  const q2 = interpolate(frame, [T.retinas - 30, T.retinas - 18], [0, 1], CLAMP);
  return (
    <AbsoluteFill>
      <Shade from="left" strength={0.85} />
      <div style={{ position: "absolute", left: M, top: 170, ...MONO, fontSize: 40, color: "#D2CBE3" }}>ELON MUSK, ON STAGE, 15 OCT</div>
      <div style={{ position: "absolute", left: M, top: 250, width: 1500, ...HEADC, whiteSpace: "normal", fontSize: 110, color: C.ink, lineHeight: 1.0, opacity: q1,
        ...keyline(0.8, 10) }}>“THE PRODUCTION CAR WILL BE QUICKER STILL”</div>
      <div style={{ position: "absolute", left: M, top: 600, width: 1500, ...HEADC, whiteSpace: "normal", fontSize: 96, color: C.acid, lineHeight: 1.0, opacity: q2,
        ...keyline(0.7, 10) }}>THE REAL LIMIT: NOT DETACHING THE DRIVER&apos;S RETINAS</div>
    </AbsoluteFill>
  );
};

export const S3Launch: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: C.black }}>
    <ClipScene src="film/zero60_slow.mp4" from={0} dur={X.bars} push={[1, 1.06]} origin="40% 60%" />
    <ClipScene src="film/zero60_slow.mp4" from={X.musk} dur={X.payoff - X.musk} trimBefore={120} rate={0.5} push={[1.05, 1.1]} />
    <ClipScene src="film/zero60_slow.mp4" from={X.payoff} dur={D - X.payoff} push={[1.02, 1.05]} origin="40% 60%" />
    <Readout />
    <Bars />
    <Race />
    <StopwatchScene />
    <MuskQuote />
    <TeslaCredit show={[[0, X.bars], [X.musk, D]]} />
    <Sfx at={T.t081} name="thock" volume={0.6} />
    <Sfx at={X.bars} name="whoosh" volume={0.35} />
    <Sfx at={X.race} name="whoosh" volume={0.35} />
    <Sfx at={X.race + 16} name="tick_run" volume={0.25} dur={130} />
    <Sfx at={X.watch} name="whoosh" volume={0.35} />
    <Sfx at={T.nobody} name="thock" volume={0.75} />
    <Sfx at={X.musk} name="whoosh" volume={0.3} />
    <Sfx at={X.payoff} name="whoosh" volume={0.35} />
    <Sfx at={T.attached - 6} name="thock" volume={0.6} />
  </AbsoluteFill>
);
