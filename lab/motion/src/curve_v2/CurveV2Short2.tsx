import { Audio, Video } from "@remotion/media";
import type React from "react";
import { AbsoluteFill, Easing, Img, interpolate, Sequence, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { CLAMP, EASE_IN_OUT, EASE_OUT } from "../lib/anim";
import { keyline } from "./HybridC";
import { v2 } from "./palette";
import { VO_S2_CAPTIONS } from "./voS2Captions";

// Roadster Short 2 (for Mon 19 Oct): "The Tesla Roadster's 0.81 Second Launch". 1080x1920, 30 fps.
// Footage: Tesla's 4K "The 0-60" upload, RIFE 8x slow motion with a pan that follows the car (public/shorts/s2_launch_8x.mp4).
// Every number on screen: TESLA_ROADSTER_FACTS.md P4 (0.81 s, Tesla's own timing), C5 (Rimac Nevera R 1.66 s, Dewesoft-
// verified), P1 19:00 (production car "will actually do better"); 3.4 g is our sum (26.82 m/s / 0.81 s / 9.81), labelled.
// Narration lab/curve_v2/shorts/vo/s2_chris_v4.mp3 (29.4 s). The last frame is frame 0, so the replay has no seam.

export const SHORT2_FRAMES = 897;

const F = { launchEnd: 182, lanes: 182, watch: 364, musk: 519, gee: 618, outro: 717, back: 868, hold0: 894 };

const HEAD: React.CSSProperties = { fontFamily: v2.fonts.heavy, fontWeight: 900, letterSpacing: "-0.02em", lineHeight: 0.9 };
const HEADC: React.CSSProperties = { ...HEAD, fontVariationSettings: "'wdth' 82", whiteSpace: "nowrap" };
const BG = "radial-gradient(ellipse at 50% 38%, #1B0B3A 0%, #0A0418 55%, #000000 100%)";
const fill: React.CSSProperties = { width: "100%", height: "100%", filter: "saturate(1.1) contrast(1.06) brightness(1.05)" };

const Footage: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const push = interpolate(frame, [0, F.launchEnd], [1, 1.04], CLAMP);
  const backIn = interpolate(frame, [F.back, F.back + 14], [0, 1], { ...CLAMP, easing: EASE_IN_OUT });
  return (
    <AbsoluteFill style={{ backgroundColor: v2.colors.black }}>
      <Sequence durationInFrames={F.launchEnd} premountFor={fps}>
        <AbsoluteFill style={{ scale: push, transformOrigin: "50% 48%" }}>
          <Video src={staticFile("shorts/s2_launch_8x.mp4")} muted style={fill} />
        </AbsoluteFill>
      </Sequence>
      <Sequence from={F.lanes} durationInFrames={F.musk - F.lanes}>
        <AbsoluteFill style={{ background: BG }} />
      </Sequence>
      <Sequence from={F.musk} durationInFrames={F.outro - F.musk}>
        <Img src={staticFile("shorts/s2_mid.png")} style={{ ...fill, filter: "brightness(0.38) saturate(0.9) blur(2px)" }} />
      </Sequence>
      <Sequence from={F.outro}>
        <AbsoluteFill style={{ background: BG }} />
        {/* back to the opening picture, so the last frame is frame 0 */}
        <AbsoluteFill style={{ opacity: backIn }}>
          <Img src={staticFile("shorts/s2_frame0.png")} style={fill} />
        </AbsoluteFill>
      </Sequence>
    </AbsoluteFill>
  );
};

// The readout: "0-60 MPH / 0.81 s". It is the hook at frame 0, leaves at 6 s, and returns in the outro to become the
// hook again in the last frame.
const Readout: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const at = (s: number) => Math.round(s * fps);
  const inOpening = frame < F.lanes;
  const inOutro = frame >= F.outro && frame < F.hold0;
  if (!inOpening && !inOutro) return null;
  const out = interpolate(frame, [F.lanes - 8, F.lanes], [0, 1], { ...CLAMP, easing: Easing.in(Easing.cubic) });
  const outroIn = spring({ frame: frame - F.outro, fps, config: { damping: 14, stiffness: 190 } });
  const shown = inOpening ? 1 - out : outroIn;
  const labelShown = inOpening ? 1 - out : interpolate(frame, [F.back, F.back + 12], [0, 1], { ...CLAMP, easing: EASE_OUT });
  const tag = spring({ frame: frame - at(5.0), fps, config: { damping: 10, stiffness: 230 } });
  const tagOut = interpolate(frame, [F.lanes - 8, F.lanes], [1, 0], CLAMP);
  const pulse = inOutro ? interpolate(frame, [at(26.4), at(26.6), at(26.9)], [1, 1.08, 1], CLAMP) : 1;
  return (
    <div style={{ position: "absolute", left: 64, top: 132, ...HEADC, opacity: interpolate(shown, [0, 0.3], [0, 1], CLAMP),
      translate: `0 ${(1 - shown) * -60}px` }}>
      <div style={{ fontSize: 96, color: v2.colors.cyan, opacity: labelShown, ...keyline(0.64, 10) }}>0–60 MPH</div>
      <div style={{ fontSize: 300, color: v2.colors.acid, lineHeight: 0.86, scale: pulse, transformOrigin: "0% 50%", ...keyline(2, 10) }}>
        0.81<span style={{ fontSize: 150, marginLeft: 12 }}>s</span>
      </div>
      {inOpening ? (
        <div style={{ display: "inline-block", marginTop: 18, padding: "8px 18px 10px", backgroundColor: v2.colors.ink, color: v2.colors.black,
          fontSize: 54, border: `4px solid ${v2.colors.black}`, scale: tag * tagOut, rotate: `${interpolate(tag, [0, 1], [-14, -2])}deg`,
          transformOrigin: "0% 50%" }}>
          TESLA'S OWN TIMING
        </div>
      ) : null}
    </div>
  );
};

// Two lanes race to 60 mph at true relative speed (1 s of real time = 2.4 s on screen).
const CarGlyph: React.FC<{ color: string }> = ({ color }) => (
  <svg width={190} height={64} viewBox="0 0 190 64">
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
  const t0 = at(6.3);
  const scale = 2.4;
  const enter = interpolate(frame, [F.lanes, F.lanes + 10], [0, 1], { ...CLAMP, easing: EASE_OUT });
  const leave = interpolate(frame, [F.watch - 8, F.watch], [0, 1], CLAMP);
  const lanes = [
    { name: "TESLA ROADSTER", time: 0.81, color: v2.colors.ink, timeColor: v2.colors.acid, note: "TESLA'S OWN TIMING", top: 600 },
    { name: "RIMAC NEVERA R", time: 1.66, color: "#8FA3B8", timeColor: v2.colors.ink, note: "DEWESOFT-VERIFIED", top: 930 },
  ];
  const x0 = 70;
  const x1 = 820;
  return (
    <AbsoluteFill style={{ opacity: enter * (1 - leave) }}>
      <div style={{ position: "absolute", left: 64, top: 420, ...HEADC, fontSize: 96, color: v2.colors.cyan, ...keyline(0.64, 10) }}>0–60 MPH</div>
      {lanes.map((ln, i) => {
        const real = Math.max(0, (frame - t0) / fps / scale); // real seconds since the start
        const p = Math.min(1, (real / ln.time) ** 2); // constant acceleration: distance grows with time squared
        const done = real >= ln.time;
        const shownTime = Math.min(real, ln.time);
        const noteIn = interpolate(frame, [at(i === 0 ? 8.4 : 10.75), at(i === 0 ? 8.4 : 10.75) + 8], [0, 1], { ...CLAMP, easing: EASE_OUT });
        return (
          <div key={ln.name} style={{ position: "absolute", left: 0, top: ln.top, width: 1080, translate: `${(1 - enter) * (i ? 60 : -60)}px 0` }}>
            <div style={{ position: "absolute", left: x0, top: 0, ...HEADC, fontSize: 64, color: ln.color, ...keyline(0.43, 9) }}>{ln.name}</div>
            <div style={{ position: "absolute", left: x0, top: 170, width: x1 - x0 + 120, height: 8, backgroundColor: "rgba(255,255,255,0.35)" }} />
            <div style={{ position: "absolute", left: x1 + 96, top: 92, width: 10, height: 92, backgroundColor: v2.colors.magenta, border: "3px solid #000" }} />
            <div style={{ position: "absolute", left: x0 + (x1 - x0) * p, top: 106 }}>
              <CarGlyph color={ln.color} />
            </div>
            <div style={{ position: "absolute", left: x0, top: 196, ...HEADC, fontSize: 104, color: done ? ln.timeColor : "rgba(255,255,255,0.75)",
              fontVariantNumeric: "tabular-nums", ...keyline(0.7, 10) }}>
              {shownTime.toFixed(2)} s
            </div>
            <div style={{ position: "absolute", left: x0 + 330, top: 222, ...HEADC, fontSize: 46, color: ln.timeColor, opacity: noteIn,
              ...keyline(0.31, 8) }}>{ln.note}</div>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

const Stopwatch: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < F.watch || frame >= F.musk) return null;
  const at = (s: number) => Math.round(s * fps);
  const enter = spring({ frame: frame - F.watch, fps, config: { damping: 15, stiffness: 180 } });
  const leave = interpolate(frame, [F.musk - 8, F.musk], [0, 1], CLAMP);
  const sweep = interpolate(frame, [F.watch + 4, F.watch + 28], [0, 0.81], { ...CLAMP, easing: EASE_OUT });
  const ang = (sweep / 1) * 360; // one revolution = 1 second
  const own = spring({ frame: frame - at(13.55), fps, config: { damping: 11, stiffness: 220 } });
  const stamp = spring({ frame: frame - at(14.5), fps, config: { damping: 9, stiffness: 260 } });
  const cx = 540;
  const cy = 800;
  const r = 270;
  return (
    <AbsoluteFill style={{ opacity: 1 - leave }}>
      <svg width={1080} height={1920} style={{ position: "absolute", inset: 0, scale: interpolate(enter, [0, 1], [0.7, 1]),
        transformOrigin: `${cx}px ${cy}px`, opacity: interpolate(enter, [0, 0.3], [0, 1], CLAMP) }}>
        <rect x={cx - 34} y={cy - r - 70} width={68} height={50} rx={10} fill="#C9CFD6" stroke="#000" strokeWidth={6} />
        <circle cx={cx} cy={cy} r={r + 22} fill="#C9CFD6" stroke="#000" strokeWidth={8} />
        <circle cx={cx} cy={cy} r={r} fill="#0B0F17" stroke="#000" strokeWidth={6} />
        {Array.from({ length: 20 }).map((_, i) => {
          const a = (i / 20) * Math.PI * 2 - Math.PI / 2;
          const long = i % 5 === 0;
          return (
            <line key={i} x1={cx + Math.cos(a) * (r - (long ? 46 : 28))} y1={cy + Math.sin(a) * (r - (long ? 46 : 28))}
              x2={cx + Math.cos(a) * (r - 10)} y2={cy + Math.sin(a) * (r - 10)} stroke={long ? v2.colors.ink : "#7C8794"} strokeWidth={long ? 8 : 5} />
          );
        })}
        <path d={`M ${cx} ${cy} L ${cx} ${cy - r + 20} A ${r - 20} ${r - 20} 0 ${ang > 180 ? 1 : 0} 1 ${cx + Math.sin((ang * Math.PI) / 180) * (r - 20)} ${cy - Math.cos((ang * Math.PI) / 180) * (r - 20)} Z`}
          fill={v2.colors.acid} opacity={0.22} />
        <line x1={cx} y1={cy} x2={cx + Math.sin((ang * Math.PI) / 180) * (r - 34)} y2={cy - Math.cos((ang * Math.PI) / 180) * (r - 34)}
          stroke={v2.colors.acid} strokeWidth={14} strokeLinecap="round" />
        <circle cx={cx} cy={cy} r={20} fill={v2.colors.acid} stroke="#000" strokeWidth={5} />
      </svg>
      <div style={{ position: "absolute", left: 0, right: 0, top: cy + 70, textAlign: "center", ...HEADC, fontSize: 96, color: v2.colors.acid,
        opacity: enter, ...keyline(0.64, 10) }}>{sweep.toFixed(2)} s</div>
      <div style={{ position: "absolute", left: 70, top: 380, padding: "8px 18px 10px", backgroundColor: v2.colors.ink, color: v2.colors.black,
        ...HEADC, fontSize: 60, border: "4px solid #000", scale: own, rotate: `${interpolate(own, [0, 1], [-12, -3])}deg`, transformOrigin: "0% 50%" }}>
        TESLA'S OWN STOPWATCH
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 1040, display: "flex", justifyContent: "center" }}>
        <div style={{ padding: "12px 26px 14px", border: `10px solid ${v2.colors.warn}`, color: v2.colors.warn, ...HEADC, fontSize: 76,
          textAlign: "center", lineHeight: 0.95, backgroundColor: "rgba(0,0,0,0.55)", scale: interpolate(stamp, [0, 1], [1.8, 1]),
          opacity: interpolate(stamp, [0, 0.2], [0, 1], CLAMP), rotate: "-6deg" }}>
          NOT INDEPENDENTLY<br />TIMED
        </div>
      </div>
    </AbsoluteFill>
  );
};

const Musk: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < F.musk || frame >= F.outro) return null;
  const at = (s: number) => Math.round(s * fps);
  const a = spring({ frame: frame - (F.musk + 4), fps, config: { damping: 14, stiffness: 190 } });
  const aOut = interpolate(frame, [F.gee - 8, F.gee], [0, 1], CLAMP);
  const g = spring({ frame: frame - F.gee, fps, config: { damping: 12, stiffness: 200 } });
  const leave = interpolate(frame, [F.outro - 8, F.outro], [0, 1], CLAMP);
  const quick = spring({ frame: frame - at(19.24), fps, config: { damping: 10, stiffness: 230 } });
  return (
    <AbsoluteFill style={{ opacity: 1 - leave }}>
      <div style={{ position: "absolute", left: 64, top: 360, ...HEADC, opacity: a * (1 - aOut), translate: `${(1 - a) * -60}px 0` }}>
        <div style={{ fontSize: 70, color: v2.colors.ink, lineHeight: 1, ...keyline(0.47, 9) }}>MUSK: THE PRODUCTION CAR</div>
        <div style={{ fontSize: 70, color: v2.colors.ink, lineHeight: 1, ...keyline(0.47, 9) }}>WILL BE QUICKER</div>
        <div style={{ fontSize: 250, color: v2.colors.acid, marginTop: 20, scale: interpolate(quick, [0, 1], [0.6, 1]), transformOrigin: "0% 50%",
          opacity: interpolate(quick, [0, 0.2], [0, 1], CLAMP), ...keyline(1.6, 10) }}>&lt; 0.81 s</div>
      </div>
      <div style={{ position: "absolute", left: 64, top: 380, ...HEADC, opacity: interpolate(g, [0, 0.3], [0, 1], CLAMP),
        translate: `0 ${(1 - g) * 50}px` }}>
        <div style={{ fontSize: 300, color: v2.colors.acid, lineHeight: 0.86, ...keyline(2, 10) }}>≈3.4 g</div>
        <div style={{ fontSize: 62, color: v2.colors.ink, marginTop: 24, lineHeight: 1.05, ...keyline(0.42, 9) }}>THE AVERAGE PUSH OF</div>
        <div style={{ fontSize: 62, color: v2.colors.ink, lineHeight: 1.05, ...keyline(0.42, 9) }}>0–60 IN 0.81 s</div>
        <div style={{ display: "inline-block", marginTop: 22, padding: "6px 16px 8px", backgroundColor: v2.colors.cyan, color: v2.colors.black,
          fontSize: 48, border: "4px solid #000" }}>OUR MATH</div>
      </div>
    </AbsoluteFill>
  );
};

// The outro: the stopwatch clips onto the readout on "stopwatch attached", then falls away as frame 0 returns.
const Attach: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const at = (s: number) => Math.round(s * fps);
  const a = at(28.2);
  if (frame < a - 2 || frame >= F.back + 14) return null;
  const clip = spring({ frame: frame - a, fps, config: { damping: 9, stiffness: 240 } });
  const fall = interpolate(frame, [F.back, F.back + 14], [0, 1], { ...CLAMP, easing: Easing.in(Easing.quad) });
  return (
    <svg width={1080} height={1920} style={{ position: "absolute", inset: 0 }}>
      <g transform={`translate(${interpolate(clip, [0, 1], [1180, 850])} ${360 + fall * 900}) rotate(${interpolate(clip, [0, 1], [40, 12]) + fall * 60})`}
        opacity={1 - fall}>
        <rect x={-14} y={-112} width={28} height={26} rx={6} fill="#C9CFD6" stroke="#000" strokeWidth={5} />
        <circle r={88} fill="#C9CFD6" stroke="#000" strokeWidth={6} />
        <circle r={72} fill="#0B0F17" stroke="#000" strokeWidth={4} />
        <line x1={0} y1={0} x2={52} y2={-34} stroke={v2.colors.acid} strokeWidth={10} strokeLinecap="round" />
      </g>
    </svg>
  );
};

type Page = { startMs: number; durationMs: number; tokens: { text: string; fromMs: number; toMs: number }[] };
const PAGES: Page[] = (() => {
  const words: { text: string; fromMs: number; toMs: number }[] = [];
  for (const c of VO_S2_CAPTIONS) {
    if (!c.text.startsWith(" ") && words.length > 0) {
      const w = words[words.length - 1];
      w.text += c.text;
      w.toMs = c.endMs;
    } else {
      words.push({ text: c.text, fromMs: c.startMs, toMs: c.endMs });
    }
  }
  const out: Page[] = [];
  let cur: Page | null = null;
  for (const w of words) {
    const len = cur ? cur.tokens.map((t) => t.text).join("").trim().length : 0;
    if (!cur || cur.tokens.length >= 3 || len + w.text.length > 16) {
      cur = { startMs: w.fromMs, durationMs: 0, tokens: [] };
      out.push(cur);
    }
    cur.tokens.push(w);
    cur.durationMs = w.toMs - cur.startMs;
    if (/[,!?]$/.test(w.text.trim()) || (/\.$/.test(w.text.trim()) && !/^\s*\d+\.$/.test(w.text))) cur = null;
  }
  return out;
})();

const Captions: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame >= F.back) return null;
  const ms = (frame / fps) * 1000;
  const page = PAGES.find((p, i) => ms >= p.startMs && ms < (PAGES[i + 1]?.startMs ?? p.startMs + p.durationMs + 400));
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
  const show = frame < F.lanes || (frame >= F.back && frame < F.hold0);
  if (!show) return null;
  return (
    <div style={{ position: "absolute", left: 0, top: 1460, padding: "10px 22px 10px 60px", backgroundColor: "rgba(0,0,0,0.74)",
      fontFamily: v2.fonts.mono, fontWeight: 500, fontSize: 40, letterSpacing: "0.03em", color: v2.colors.ink }}>
      FOOTAGE: TESLA · 8× SLOWER
    </div>
  );
};

export const CurveV2Short2: React.FC = () => {
  const { fps } = useVideoConfig();
  const at = (s: number) => Math.round(s * fps);
  return (
    <AbsoluteFill style={{ backgroundColor: v2.colors.black }}>
      <Footage />
      <Lanes />
      <Stopwatch />
      <Musk />
      <Readout />
      <Attach />
      <Captions />
      <Credit />
      <Sequence from={F.hold0}>
        <Img src={staticFile("shorts/s2_frame0.png")} style={fill} />
        <Readout />
        <Credit />
      </Sequence>

      <Audio src={staticFile("shorts/s2_chris_v4.mp3")} />
      <Audio src={staticFile("audio/sample-bed.mp3")}
        volume={(f) => interpolate(f, [0, 9, SHORT2_FRAMES - 12, SHORT2_FRAMES], [0, 0.13, 0.13, 0], CLAMP)} />
      <Sequence from={at(1.0)} durationInFrames={at(3.6)}><Audio src={staticFile("sfx/hiss.mp3")} volume={0.8} /></Sequence>
      <Sequence from={at(5.0)}><Audio src={staticFile("sfx/thock.mp3")} volume={0.6} /></Sequence>
      <Sequence from={F.lanes}><Audio src={staticFile("sfx/whoosh.mp3")} volume={0.45} /></Sequence>
      <Sequence from={at(6.3)} durationInFrames={at(4.0)}><Audio src={staticFile("sfx/tick_run.mp3")} volume={0.25} /></Sequence>
      <Sequence from={at(8.25)}><Audio src={staticFile("sfx/thock.mp3")} volume={0.7} /></Sequence>
      <Sequence from={at(10.3)}><Audio src={staticFile("sfx/thock.mp3")} volume={0.45} /></Sequence>
      <Sequence from={F.watch}><Audio src={staticFile("sfx/whoosh.mp3")} volume={0.4} /></Sequence>
      <Sequence from={at(14.5)}><Audio src={staticFile("sfx/thock.mp3")} volume={0.75} /></Sequence>
      <Sequence from={F.musk}><Audio src={staticFile("sfx/whoosh.mp3")} volume={0.4} /></Sequence>
      <Sequence from={F.gee}><Audio src={staticFile("sfx/form.mp3")} volume={0.45} /></Sequence>
      <Sequence from={F.outro}><Audio src={staticFile("sfx/whoosh.mp3")} volume={0.4} /></Sequence>
      <Sequence from={at(28.2)}><Audio src={staticFile("sfx/thock.mp3")} volume={0.6} /></Sequence>
    </AbsoluteFill>
  );
};
