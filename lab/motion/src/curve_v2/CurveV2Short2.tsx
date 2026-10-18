import { Audio, Video } from "@remotion/media";
import type React from "react";
import { AbsoluteFill, Img, interpolate, Sequence, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { CLAMP, EASE_OUT } from "../lib/anim";
import { keyline } from "./HybridC";
import { makePages } from "./pager";
import { v2 } from "./palette";
import { VO_S2_CAPTIONS } from "./voS2Captions";

// Roadster Short 2, v2 (for Mon 19 Oct): "The Tesla Roadster's 0.81 Second Launch". 1080x1920, 30 fps.
// v2 applies critic round 1 (shorts/out/critic_s2/round1.md): the crop holds still on the car's rear so the gas jets and
// plume are on screen under "gas jets fire"; "Nevera" re-voiced (Ree-mats Neh-VEH-rah, whisper hears "Nevera"); the race
// on one true distance scale (0-60 at constant acceleration: Roadster 10.9 m, Rimac 22.3 m); stopwatches sweep in real
// time; Tesla's claimed times by version instead of a bare "< 0.81 s"; hard cuts; a filled payoff; the bed never dips.
// Numbers: TESLA_ROADSTER_FACTS.md P4 (0.81 s, Tesla's own timing), C5 (Rimac 1.66 s, Dewesoft), §3 (Rocket <0.59 s,
// Performance <1.6 s; tesla.com: Thrust under 1 s), P1 19:00; 3.4 g = 26.82 m/s / 0.81 s / 9.81 [EST], labelled.
// Narration lab/curve_v2/shorts/vo/s2_chris_v4_v2.mp3 (29.6 s). Last frame = frame 0.

export const SHORT2_FRAMES = 897;

const F = { lanes: 182, race: 189, watch: 369, own: 412, stamp: 440, trims: 524, gee: 623, outro: 722, sweep: 783, attach: 865, back: 883 };

const HEAD: React.CSSProperties = { fontFamily: v2.fonts.heavy, fontWeight: 900, letterSpacing: "-0.02em", lineHeight: 0.9 };
const HEADC: React.CSSProperties = { ...HEAD, fontVariationSettings: "'wdth' 82", whiteSpace: "nowrap" };
const BG = "radial-gradient(ellipse at 50% 38%, #1B0B3A 0%, #0A0418 55%, #000000 100%)";
const fill: React.CSSProperties = { width: "100%", height: "100%", filter: "saturate(1.1) contrast(1.06) brightness(1.05)" };
const slowPush = (frame: number, a: number, b: number, to = 1.04) => interpolate(frame, [a, b], [1, to], CLAMP);

const Footage: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill style={{ backgroundColor: v2.colors.black }}>
      <Sequence durationInFrames={F.lanes} premountFor={fps}>
        <AbsoluteFill style={{ scale: slowPush(frame, 0, F.lanes), transformOrigin: "50% 48%" }}>
          <Video src={staticFile("shorts/s2_launch_8x_v2.mp4")} muted style={fill} />
        </AbsoluteFill>
      </Sequence>
      <Sequence from={F.lanes} durationInFrames={F.back - F.lanes}>
        <AbsoluteFill style={{ background: BG }} />
      </Sequence>
      {/* hard cut back to the opening picture: the readout stays put, only the background changes */}
      <Sequence from={F.back}>
        <Img src={staticFile("shorts/s2_frame0_v2.png")} style={fill} />
      </Sequence>
    </AbsoluteFill>
  );
};

const StopwatchGlyph: React.FC<{ secs: number; r: number }> = ({ secs, r }) => {
  const ang = secs * 360; // one revolution = 1 second
  const rad = (ang * Math.PI) / 180;
  const R = r;
  const sector = ang <= 0 ? "" : `M 0 0 L 0 ${-(R - 20)} A ${R - 20} ${R - 20} 0 ${ang > 180 ? 1 : 0} 1 ${Math.sin(rad) * (R - 20)} ${-Math.cos(rad) * (R - 20)} Z`;
  return (
    <g>
      <rect x={-R * 0.13} y={-R - R * 0.26} width={R * 0.26} height={R * 0.19} rx={R * 0.04} fill="#C9CFD6" stroke="#000" strokeWidth={6} />
      <circle r={R + R * 0.08} fill="#C9CFD6" stroke="#000" strokeWidth={8} />
      <circle r={R} fill="#0B0F17" stroke="#000" strokeWidth={6} />
      {Array.from({ length: 20 }).map((_, i) => {
        const a = (i / 20) * Math.PI * 2 - Math.PI / 2;
        const long = i % 5 === 0;
        return <line key={i} x1={Math.cos(a) * (R - (long ? R * 0.17 : R * 0.1))} y1={Math.sin(a) * (R - (long ? R * 0.17 : R * 0.1))}
          x2={Math.cos(a) * (R - R * 0.04)} y2={Math.sin(a) * (R - R * 0.04)} stroke={long ? v2.colors.ink : "#7C8794"} strokeWidth={long ? 8 : 5} />;
      })}
      {sector ? <path d={sector} fill={v2.colors.acid} opacity={0.22} /> : null}
      <line x1={0} y1={0} x2={Math.sin(rad) * (R - R * 0.12)} y2={-Math.cos(rad) * (R - R * 0.12)} stroke={v2.colors.acid} strokeWidth={Math.max(8, R * 0.05)} strokeLinecap="round" />
      <circle r={Math.max(12, R * 0.07)} fill={v2.colors.acid} stroke="#000" strokeWidth={5} />
    </g>
  );
};

// The readout is the hook at frame 0 and returns, in the same place, for the payoff, so the hard cut back to frame 0
// only swaps the background.
const Readout: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const at = (s: number) => Math.round(s * fps);
  const inOpening = frame < F.lanes || frame >= F.back;
  const inOutro = frame >= F.outro && frame < F.back;
  if (!inOpening && !inOutro) return null;
  const outroIn = spring({ frame: frame - F.outro, fps, config: { damping: 14, stiffness: 190 } });
  const shown = inOpening ? 1 : outroIn;
  const tag = spring({ frame: frame - at(5.0), fps, config: { damping: 10, stiffness: 230 } });
  const showTag = frame < F.lanes;
  return (
    <div style={{ position: "absolute", left: 64, top: 132, ...HEADC, opacity: interpolate(shown, [0, 0.3], [0, 1], CLAMP), translate: `0 ${(1 - shown) * -60}px` }}>
      <div style={{ fontSize: 96, color: v2.colors.cyan, ...keyline(0.64, 10) }}>0–60 MPH</div>
      <div style={{ fontSize: 300, color: v2.colors.acid, lineHeight: 0.86, ...keyline(2, 10) }}>
        0.81<span style={{ fontSize: 150, marginLeft: 12 }}>s</span>
      </div>
      {showTag ? (
        <div style={{ display: "inline-block", marginTop: 18, padding: "8px 18px 10px", backgroundColor: v2.colors.ink, color: v2.colors.black,
          fontSize: 54, border: `4px solid ${v2.colors.black}`, scale: tag, rotate: `${interpolate(tag, [0, 1], [-14, -2])}deg`, transformOrigin: "0% 50%" }}>
          TESLA'S OWN TIMING
        </div>
      ) : null}
    </div>
  );
};

// One true distance scale: from standstill to 60 mph at constant acceleration the Roadster covers 10.9 m in 0.81 s and
// the Rimac 22.3 m in 1.66 s. After its flag the Roadster carries on at 60 mph. 1 s of real time = 2.4 s on screen.
const CarGlyph: React.FC<{ color: string }> = ({ color }) => (
  <svg width={300} height={100} viewBox="0 0 190 64">
    <path d="M 8 44 C 10 30, 40 24, 70 20 C 92 8, 128 8, 150 22 C 170 26, 184 32, 184 44 Z" fill={color} stroke="#000" strokeWidth={5} strokeLinejoin="round" />
    <circle cx={50} cy={46} r={14} fill="#15181D" stroke="#000" strokeWidth={4} />
    <circle cx={146} cy={46} r={14} fill="#15181D" stroke="#000" strokeWidth={4} />
  </svg>
);

const Lanes: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < F.lanes || frame >= F.watch) return null;
  const at = (s: number) => Math.round(s * fps);
  const scale = 2.4;
  const v = 26.82; // 60 mph in m/s
  const start = 380;
  const end = 932; // x of 22.3 m
  const xOf = (d: number) => start + ((end - start) * d) / 22.3;
  const real = Math.max(0, (frame - F.race) / fps / scale);
  const lanes = [
    { name: "TESLA ROADSTER", time: 0.81, color: v2.colors.ink, timeColor: v2.colors.acid, note: "TESLA'S OWN TIMING", top: 560, noteAt: at(8.4) },
    { name: "RIMAC NEVERA R", time: 1.66, color: "#8FA3B8", timeColor: v2.colors.ink, note: "DEWESOFT-VERIFIED", top: 960, noteAt: at(10.86) },
  ];
  return (
    <AbsoluteFill style={{ scale: slowPush(frame, F.lanes, F.watch), transformOrigin: "50% 45%" }}>
      <div style={{ position: "absolute", left: 64, top: 400, ...HEADC, fontSize: 96, color: v2.colors.cyan, ...keyline(0.64, 10) }}>0–60 MPH</div>
      {lanes.map((ln) => {
        const a = v / ln.time;
        const flagD = 0.5 * v * ln.time;
        const d = real <= ln.time ? 0.5 * a * real * real : flagD + v * (real - ln.time);
        const done = real >= ln.time;
        const noteIn = interpolate(frame, [ln.noteAt, ln.noteAt + 8], [0, 1], { ...CLAMP, easing: EASE_OUT });
        return (
          <div key={ln.name} style={{ position: "absolute", left: 0, top: ln.top, width: 1080, height: 380 }}>
            <div style={{ position: "absolute", left: 64, top: 0, ...HEADC, fontSize: 64, color: ln.color, ...keyline(0.43, 9) }}>{ln.name}</div>
            <div style={{ position: "absolute", left: 64, top: 186, width: 1016, height: 8, backgroundColor: "rgba(255,255,255,0.35)" }} />
            <div style={{ position: "absolute", left: xOf(flagD) - 5, top: 86, width: 10, height: 108, backgroundColor: v2.colors.magenta, border: "3px solid #000" }} />
            <div style={{ position: "absolute", left: xOf(flagD) - 80, top: 50, width: 160, textAlign: "center", ...HEADC, fontSize: 36, color: v2.colors.magenta, ...keyline(0.24, 7) }}>60 MPH</div>
            <div style={{ position: "absolute", left: xOf(d) - 300, top: 92 }}><CarGlyph color={ln.color} /></div>
            <div style={{ position: "absolute", left: 64, top: 214, ...HEADC, fontSize: 104, color: done ? ln.timeColor : "rgba(255,255,255,0.75)",
              fontVariantNumeric: "tabular-nums", ...keyline(0.7, 10) }}>{Math.min(real, ln.time).toFixed(2)} s</div>
            <div style={{ position: "absolute", left: 400, top: 246, ...HEADC, fontSize: 50, color: ln.timeColor, opacity: noteIn, ...keyline(0.33, 8) }}>{ln.note}</div>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

const Stopwatch: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < F.watch || frame >= F.trims) return null;
  const secs = interpolate(frame, [F.watch + 4, F.watch + 4 + 24], [0, 0.81], CLAMP); // 0.81 s in 24 frames: real time
  const own = spring({ frame: frame - F.own, fps, config: { damping: 11, stiffness: 220 } });
  const stamp = spring({ frame: frame - F.stamp, fps, config: { damping: 9, stiffness: 260 } });
  return (
    <AbsoluteFill style={{ scale: slowPush(frame, F.watch, F.trims, 1.05), transformOrigin: "50% 42%" }}>
      <svg width={1080} height={1920} style={{ position: "absolute", inset: 0 }}>
        <g transform="translate(540 800)"><StopwatchGlyph secs={secs} r={270} /></g>
      </svg>
      <div style={{ position: "absolute", left: 0, right: 0, top: 870, textAlign: "center", ...HEADC, fontSize: 96, color: v2.colors.acid, ...keyline(0.64, 10) }}>
        {secs.toFixed(2)} s
      </div>
      <div style={{ position: "absolute", left: 70, top: 380, padding: "8px 18px 10px", backgroundColor: v2.colors.ink, color: v2.colors.black,
        ...HEADC, fontSize: 60, border: "4px solid #000", scale: own, rotate: `${interpolate(own, [0, 1], [-12, -3])}deg`, transformOrigin: "0% 50%" }}>
        TESLA'S OWN STOPWATCH
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 1060, display: "flex", justifyContent: "center" }}>
        <div style={{ padding: "12px 26px 14px", border: `10px solid ${v2.colors.warn}`, color: v2.colors.warn, ...HEADC, fontSize: 76,
          textAlign: "center", lineHeight: 0.95, backgroundColor: "rgba(0,0,0,0.55)", scale: interpolate(stamp, [0, 1], [1.8, 1]),
          opacity: interpolate(stamp, [0, 0.2], [0, 1], CLAMP), rotate: "-6deg" }}>
          NOT INDEPENDENTLY<br />TIMED
        </div>
      </div>
    </AbsoluteFill>
  );
};

// Musk says the production car will be quicker still: Tesla's own claims, by version (§3).
const Trims: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < F.trims || frame >= F.gee) return null;
  const rows = [
    { name: "ROCKET (OFF-ROAD)", t: "<0.59 s", color: v2.colors.acid },
    { name: "THRUST", t: "<1 s", color: v2.colors.ink },
    { name: "PERFORMANCE", t: "<1.6 s", color: "#C3CAD2" },
  ];
  return (
    <AbsoluteFill style={{ scale: slowPush(frame, F.trims, F.gee), transformOrigin: "30% 40%" }}>
      <div style={{ position: "absolute", left: 64, top: 360, ...HEADC, fontSize: 70, color: v2.colors.cyan, ...keyline(0.47, 9) }}>TESLA'S CLAIMED 0–60</div>
      {rows.map((r, i) => {
        const s = spring({ frame: frame - (F.trims + 6 + i * 8), fps, config: { damping: 14, stiffness: 210 } });
        return (
          <div key={r.name} style={{ position: "absolute", left: 64, right: 150, top: 500 + i * 170, display: "flex", justifyContent: "space-between",
            alignItems: "baseline", ...HEADC, opacity: interpolate(s, [0, 0.3], [0, 1], CLAMP), translate: `${(1 - s) * -60}px 0` }}>
            <span style={{ fontSize: 62, color: r.color, ...keyline(0.42, 9) }}>{r.name}</span>
            <span style={{ fontSize: 112, color: r.color, fontVariantNumeric: "tabular-nums", ...keyline(0.75, 10) }}>{r.t}</span>
          </div>
        );
      })}
      <div style={{ position: "absolute", left: 64, top: 1030, ...HEADC, fontSize: 46, color: "#C3CAD2", ...keyline(0.3, 7) }}>ALL SELF-REPORTED BY TESLA</div>
    </AbsoluteFill>
  );
};

const Gee: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < F.gee || frame >= F.outro) return null;
  const g = spring({ frame: frame - (F.gee + 2), fps, config: { damping: 12, stiffness: 200 } });
  return (
    <AbsoluteFill style={{ scale: slowPush(frame, F.gee, F.outro, 1.05), transformOrigin: "20% 30%" }}>
      <div style={{ position: "absolute", left: 64, top: 380, ...HEADC, opacity: interpolate(g, [0, 0.3], [0, 1], CLAMP), translate: `0 ${(1 - g) * 50}px` }}>
        <div style={{ fontSize: 300, color: v2.colors.acid, lineHeight: 0.86, ...keyline(2, 10) }}>≈3.4 g</div>
        <div style={{ fontSize: 62, color: v2.colors.ink, marginTop: 24, lineHeight: 1.05, ...keyline(0.42, 9) }}>THE AVERAGE PUSH OF</div>
        <div style={{ fontSize: 62, color: v2.colors.ink, lineHeight: 1.05, ...keyline(0.42, 9) }}>0–60 IN 0.81 s</div>
        <div style={{ display: "inline-block", marginTop: 22, padding: "6px 16px 8px", backgroundColor: v2.colors.cyan, color: v2.colors.black,
          fontSize: 48, border: "4px solid #000" }}>OUR MATH</div>
      </div>
    </AbsoluteFill>
  );
};

// The payoff: a stopwatch beside the number sweeps 0.81 s in real time on "0.81", then clips onto it on "attached".
const Outro: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < F.outro || frame >= F.back) return null;
  const inS = spring({ frame: frame - (F.outro + 6), fps, config: { damping: 13, stiffness: 190 } });
  const secs = interpolate(frame, [F.sweep, F.sweep + 24], [0, 0.81], CLAMP);
  const clip = spring({ frame: frame - F.attach, fps, config: { damping: 9, stiffness: 240 } });
  const x = interpolate(clip, [0, 1], [860, 700]);
  const y = interpolate(clip, [0, 1], [700, 470]);
  const rot = interpolate(clip, [0, 1], [0, 14]);
  return (
    <svg width={1080} height={1920} style={{ position: "absolute", inset: 0, opacity: interpolate(inS, [0, 0.3], [0, 1], CLAMP) }}>
      <g transform={`translate(${x} ${y + (1 - inS) * 120}) rotate(${rot}) scale(${interpolate(clip, [0, 1], [1, 0.62])})`}>
        <StopwatchGlyph secs={secs} r={150} />
      </g>
    </svg>
  );
};

const PAGES = makePages(VO_S2_CAPTIONS);

const Captions: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame >= F.back) return null;
  const ms = (frame / fps) * 1000;
  const page = PAGES.find((p, i) => ms >= p.startMs && ms < (PAGES[i + 1]?.startMs ?? p.startMs + p.durationMs + 600));
  if (!page) return null;
  const pop = interpolate(ms - page.startMs, [0, 90, 160], [0.9, 1.05, 1], CLAMP);
  const startedIdx = page.tokens.reduce((acc, tk, j) => (tk.fromMs <= ms ? j : acc), -1);
  return (
    <div style={{ position: "absolute", left: 70, right: 140, top: 1318, textAlign: "center", ...HEAD, fontVariationSettings: "'wdth' 88",
      fontSize: 88, lineHeight: 1.04, textTransform: "uppercase", scale: pop }}>
      {page.tokens.map((t, i) => (
        <span key={t.fromMs} style={{ color: i === startedIdx ? v2.colors.acid : v2.colors.ink, ...keyline(0.6, 11) }}>{t.text}</span>
      ))}
    </div>
  );
};

const Credit: React.FC = () => {
  const frame = useCurrentFrame();
  if (!(frame < F.lanes || frame >= F.back)) return null;
  return (
    <div style={{ position: "absolute", left: 0, top: 1460, padding: "10px 22px 10px 60px", backgroundColor: "rgba(0,0,0,0.74)",
      fontFamily: v2.fonts.mono, fontWeight: 500, fontSize: 40, letterSpacing: "0.02em", color: v2.colors.ink }}>
      FOOTAGE: TESLA / YOUTUBE · 8× SLOWER
    </div>
  );
};

export const CurveV2Short2: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: v2.colors.black }}>
      <Footage />
      <Lanes />
      <Stopwatch />
      <Trims />
      <Gee />
      <Readout />
      <Outro />
      <Captions />
      <Credit />

      <Audio src={staticFile("shorts/s2_chris_v4_v2.mp3")} />
      {/* the bed holds its level to the last frame, so the replay has no dip */}
      <Audio src={staticFile("audio/sample-bed.mp3")} volume={(f) => interpolate(f, [0, 2, SHORT2_FRAMES - 2, SHORT2_FRAMES], [0.06, 0.13, 0.13, 0.06], CLAMP)} />
      <Sequence from={30} durationInFrames={108}><Audio src={staticFile("sfx/hiss.mp3")} volume={0.8} /></Sequence>
      <Sequence from={150}><Audio src={staticFile("sfx/thock.mp3")} volume={0.6} /></Sequence>
      <Sequence from={F.lanes}><Audio src={staticFile("sfx/whoosh.mp3")} volume={0.45} /></Sequence>
      <Sequence from={F.race} durationInFrames={120}><Audio src={staticFile("sfx/tick_run.mp3")} volume={0.25} /></Sequence>
      <Sequence from={F.race + 58}><Audio src={staticFile("sfx/thock.mp3")} volume={0.7} /></Sequence>
      <Sequence from={F.race + 120}><Audio src={staticFile("sfx/thock.mp3")} volume={0.45} /></Sequence>
      <Sequence from={F.watch}><Audio src={staticFile("sfx/whoosh.mp3")} volume={0.4} /></Sequence>
      <Sequence from={F.stamp}><Audio src={staticFile("sfx/thock.mp3")} volume={0.75} /></Sequence>
      <Sequence from={F.trims}><Audio src={staticFile("sfx/whoosh.mp3")} volume={0.4} /></Sequence>
      <Sequence from={F.gee}><Audio src={staticFile("sfx/form.mp3")} volume={0.45} /></Sequence>
      <Sequence from={F.outro}><Audio src={staticFile("sfx/whoosh.mp3")} volume={0.4} /></Sequence>
      <Sequence from={F.sweep} durationInFrames={24}><Audio src={staticFile("sfx/tick_run.mp3")} volume={0.3} /></Sequence>
      <Sequence from={F.attach}><Audio src={staticFile("sfx/thock.mp3")} volume={0.65} /></Sequence>
    </AbsoluteFill>
  );
};
