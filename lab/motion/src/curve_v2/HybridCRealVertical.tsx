import { createTikTokStyleCaptions } from "@remotion/captions";
import { Audio, Video } from "@remotion/media";
import type React from "react";
import {
  AbsoluteFill,
  Easing,
  interpolate,
  random,
  Sequence,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { CLAMP, unitFor } from "../lib/anim";
import { Callout, keyline, PushThrough, Word } from "./HybridC";
import { v2 } from "./palette";
import { VO_C_REAL_CAPTIONS } from "./voCRealCaptions";

// The same segment cut for Shorts (1080x1920): a true reframe that follows the car (no blurred letterbox),
// burned-in captions from whisper word timings, and graphics kept out of the Shorts UI zones
// (top ~6%, right-hand buttons, bottom ~20%).

type Seg = { from: number; dur: number; trim: number; rate: number; push: [number, number]; cx: (f: number) => number };

const placeOf = (seg: Seg, f: number, width: number, height: number) => {
  const vw = height * (16 / 9);
  const left = Math.min(0, Math.max(width - vw, width / 2 - seg.cx(f) * vw));
  const s = interpolate(f, [0, seg.dur], seg.push, CLAMP);
  return { vw, left, s };
};

// Screen position of a point given in source-frame fractions (16:9 clip), at local frame f of a segment.
const toScreen = (seg: Seg, f: number, xs: number, ys: number, width: number, height: number): [number, number] => {
  const { vw, left, s } = placeOf(seg, f, width, height);
  return [left + vw / 2 + (xs * vw - vw / 2) * s, height / 2 + (ys * height - height / 2) * s];
};

const VClip: React.FC<{ src: string; seg: Seg }> = ({ src, seg }) => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();
  const { vw, left, s } = placeOf(seg, frame, width, height);
  return (
    <AbsoluteFill style={{ overflow: "hidden", backgroundColor: v2.colors.black }}>
      <div style={{ position: "absolute", left, top: 0, width: vw, height, scale: s }}>
        <Video
          src={staticFile(src)}
          muted
          trimBefore={Math.round(seg.trim * fps)}
          playbackRate={seg.rate}
          style={{ width: "100%", height: "100%", filter: "saturate(1.15) contrast(1.08) brightness(1.05)" }}
        />
      </div>
    </AbsoluteFill>
  );
};

const Centered: React.FC<{ top: number; children: React.ReactNode; style?: React.CSSProperties }> = ({ top, children, style }) => (
  <div style={{ position: "absolute", left: 0, right: 0, top, display: "flex", flexDirection: "column",
    alignItems: "center", textAlign: "center", fontFamily: v2.fonts.heavy, ...style }}>
    {children}
  </div>
);

const HookV: React.FC<{ u: number }> = ({ u }) => {
  const frame = useCurrentFrame();
  const { fps, height } = useVideoConfig();
  const out = interpolate(frame, [2.15 * fps, 2.45 * fps], [0, 1], { ...CLAMP, easing: Easing.in(Easing.cubic) });
  return (
    <Centered top={0.085 * height} style={{ translate: `0 ${-out * 140 * u}px`, opacity: 1 - out }}>
      <div>
        <Word text="WHY" delay={-12} color={v2.colors.ink} size={112 * u} />
        <Word text="ISN'T" delay={-10} color={v2.colors.ink} size={112 * u} />
        <Word text="IT" delay={-8} color={v2.colors.ink} size={112 * u} />
      </div>
      <div>
        <Word text="FALLING?" delay={-5} color={v2.colors.magenta} size={168 * u} glow={v2.colors.magenta} />
      </div>
    </Centered>
  );
};

const Captions: React.FC<{ u: number }> = ({ u }) => {
  const frame = useCurrentFrame();
  const { fps, height } = useVideoConfig();
  const ms = (frame / fps) * 1000;
  const { pages } = createTikTokStyleCaptions({ captions: VO_C_REAL_CAPTIONS, combineTokensWithinMilliseconds: 750 });
  const page = pages.find((p, i) => ms >= p.startMs && ms < (pages[i + 1]?.startMs ?? p.startMs + p.durationMs + 400));
  if (!page) return null;
  const local = ms - page.startMs;
  const pop = interpolate(local, [0, 90, 160], [0.88, 1.06, 1], CLAMP);
  return (
    <Centered top={0.585 * height} style={{ paddingLeft: 90 * u, paddingRight: 150 * u }}>
      <div style={{ fontSize: 92 * u, fontWeight: 900, lineHeight: 1.05, scale: pop, textTransform: "uppercase" }}>
        {page.tokens.map((t, i) => {
          // exactly one lit word: the latest token that has started (whisper token windows overlap)
          const startedIdx = page.tokens.reduce((acc, tk, j) => (tk.fromMs <= ms ? j : acc), -1);
          const active = i === startedIdx;
          return (
            <span key={t.fromMs} style={{ color: active ? v2.colors.acid : v2.colors.ink, ...keyline(u, 11),
              textShadow: active ? `0 0 ${26 * u}px ${v2.colors.acid}` : "none" }}>
              {t.text}
            </span>
          );
        })}
      </div>
    </Centered>
  );
};

const CounterV: React.FC<{ u: number }> = ({ u }) => {
  const frame = useCurrentFrame();
  const { fps, height } = useVideoConfig();
  const inS = spring({ frame, fps, config: { damping: 16, stiffness: 160 } });
  const lockAt = 1.25 * fps;
  const locked = frame >= lockAt;
  const roll = (i: number) => Math.floor(random(`v${i}-${frame}`) * 10);
  const pop = spring({ frame: frame - lockAt, fps, config: { damping: 9, stiffness: 240 } });
  const tag = spring({ frame: frame - lockAt - 4, fps, config: { damping: 11, stiffness: 220 } });
  const out = interpolate(frame, [2.0 * fps, 2.2 * fps], [0, 1], { ...CLAMP, easing: Easing.in(Easing.cubic) });
  return (
    <Centered top={0.12 * height} style={{ translate: `0 ${interpolate(inS, [0, 1], [-260 * u, 0]) - out * 300 * u}px` }}>
      <div style={{ position: "relative", padding: `${22 * u}px ${40 * u}px`, backgroundColor: "rgba(10,4,24,0.86)",
        borderLeft: `${12 * u}px solid ${v2.colors.magenta}`, boxShadow: `0 ${16 * u}px ${60 * u}px rgba(0,0,0,0.6)` }}>
        <div style={{ color: v2.colors.cyan, fontSize: 50 * u, fontWeight: 800 }}>0–60 MPH</div>
        <div style={{ color: locked ? v2.colors.acid : v2.colors.ink, fontSize: 170 * u, fontWeight: 900, lineHeight: 1,
          fontVariantNumeric: "tabular-nums", filter: locked ? "none" : `blur(${5 * u}px)`,
          scale: locked ? interpolate(pop, [0, 1], [1.35, 1]) : 1,
          textShadow: locked ? `0 0 ${36 * u}px ${v2.colors.acid}` : undefined }}>
          {locked ? "0.81" : `${roll(0)}.${roll(1)}${roll(2)}`}
          <span style={{ fontSize: 76 * u, marginLeft: 10 * u }}>s</span>
        </div>
        <div style={{ position: "absolute", right: -24 * u, top: -46 * u, padding: `${8 * u}px ${16 * u}px`,
          backgroundColor: v2.colors.ink, color: v2.colors.black, fontSize: 34 * u, fontWeight: 900,
          rotate: `${interpolate(tag, [0, 1], [-20, 3])}deg`, scale: tag }}>
          TESLA'S OWN TIMING
        </div>
      </div>
    </Centered>
  );
};

const KickV: React.FC<{ u: number }> = ({ u }) => {
  const frame = useCurrentFrame();
  const { fps, height } = useVideoConfig();
  const s = spring({ frame, fps, config: { damping: 10, stiffness: 200 } });
  const out = interpolate(frame, [0.75 * fps, 0.95 * fps], [1, 0], CLAMP);
  return (
    <Centered top={0.1 * height} style={{ opacity: out }}>
      <div style={{ fontWeight: 900, fontSize: 132 * u, color: v2.colors.acid, lineHeight: 0.95,
        rotate: `${interpolate(s, [0, 1], [14, -4])}deg`, scale: interpolate(s, [0, 1], [0.4, 1]),
        textShadow: `0 0 ${30 * u}px ${v2.colors.acid}`, ...keyline(u, 10) }}>
        AND A<br />KICKFLIP
      </div>
    </Centered>
  );
};

const EndV: React.FC<{ u: number }> = ({ u }) => {
  const frame = useCurrentFrame();
  const { fps, height } = useVideoConfig();
  const s = spring({ frame, fps, config: { damping: 13, stiffness: 170 } });
  return (
    <Centered top={0.1 * height} style={{ translate: `0 ${interpolate(s, [0, 1], [-200 * u, 0])}px`,
      opacity: interpolate(s, [0, 0.3], [0, 1], CLAMP) }}>
      <div style={{ fontWeight: 900, fontSize: 124 * u, lineHeight: 0.95, color: v2.colors.ink, ...keyline(u, 10) }}>
        STUCK UP
        <br />
        THERE BY
        <br />
        <span style={{ color: v2.colors.magenta, textShadow: `0 0 ${40 * u}px ${v2.colors.magenta}` }}>WHAT?</span>
      </div>
    </Centered>
  );
};

const CreditV: React.FC<{ u: number; text: string }> = ({ u, text }) => {
  const { height } = useVideoConfig();
  return (
    <div style={{ position: "absolute", left: 70 * u, top: 0.745 * height, fontFamily: v2.fonts.mono, fontSize: 26 * u,
      letterSpacing: "0.06em", color: "rgba(255,255,255,0.85)", textShadow: "0 0 8px rgba(0,0,0,0.9)" }}>
      {text}
    </div>
  );
};

export const HybridCRealVertical: React.FC = () => {
  const { width, height, fps } = useVideoConfig();
  const u = unitFor(width, height);
  const s = (x: number) => Math.round(x * fps);
  const realEnd = s(10.2);
  const xray = s(10.35);

  const segHang: Seg = { from: 0, dur: s(2.84), trim: 0, rate: 0.36, push: [1.03, 1.1], cx: () => 0.505 };
  const segDrop: Seg = { from: s(2.84), dur: s(6.36), trim: 1.02, rate: 1, push: [1.02, 1.06],
    cx: (f) => interpolate(f, [0, s(2.6), s(6.36)], [0.5, 0.485, 0.53], CLAMP) };
  const segKick: Seg = { from: s(9.2), dur: realEnd - s(9.2) + s(0.4), trim: 0.55, rate: 0.85, push: [1.0, 1.04],
    cx: (f) => interpolate(f, [0, s(1.2)], [0.62, 0.45], CLAMP) };
  const segXray: Seg = { from: xray, dur: s(2.6), trim: 0, rate: 1, push: [1.0, 1.04], cx: () => 0.6 };

  return (
    <AbsoluteFill style={{ backgroundColor: v2.colors.black }}>
      <Sequence durationInFrames={segHang.dur} premountFor={fps}><VClip src="trials/ramp_hang_drop.mp4" seg={segHang} /></Sequence>
      <Sequence from={segDrop.from} durationInFrames={segDrop.dur} premountFor={fps}><VClip src="trials/ramp_hang_drop.mp4" seg={segDrop} /></Sequence>
      <Sequence from={segKick.from} durationInFrames={segKick.dur} premountFor={fps}><VClip src="trials/kickflip_side.mp4" seg={segKick} /></Sequence>

      <Sequence durationInFrames={s(2.5)}><HookV u={u} /></Sequence>

      <Sequence from={s(4.0)} durationInFrames={s(1.6)}>
        <Callout
          text="10 GAS THRUSTERS"
          color={v2.colors.cyan}
          u={u}
          target={(f) => {
            const fl = f + s(4.0) - segDrop.from;
            const xs = interpolate(f, [0, s(0.8), s(1.6)], [0.435, 0.44, 0.47], CLAMP);
            const ys = interpolate(f, [0, s(0.8), s(1.6)], [0.535, 0.54, 0.56], CLAMP);
            return toScreen(segDrop, fl, xs, ys, width, height);
          }}
          label={[0.08 * width, 0.4 * height]}
          start={0}
          end={s(1.6)}
        />
      </Sequence>

      <Sequence from={s(7.0)} durationInFrames={s(2.25)}><CounterV u={u} /></Sequence>
      <Sequence from={s(9.25)} durationInFrames={s(1.0)}><KickV u={u} /></Sequence>

      <Sequence from={realEnd - s(0.35)} durationInFrames={s(0.8)}><PushThrough u={u} /></Sequence>
      <Sequence from={xray} premountFor={fps}>
        <AbsoluteFill style={{ clipPath: `circle(${80}% at 50% 50%)` }}>
          <VClip src="trials/a2_xray.mp4" seg={segXray} />
        </AbsoluteFill>
      </Sequence>
      <Sequence from={xray + s(0.6)}><EndV u={u} /></Sequence>

      <Captions u={u} />

      <AbsoluteFill style={{ background: "radial-gradient(ellipse at center, rgba(0,0,0,0) 60%, rgba(0,0,0,0.45) 100%)" }} />
      <Sequence durationInFrames={realEnd}><CreditV u={u} text="FOOTAGE: TESLA · 15 OCT 2026" /></Sequence>
      <Sequence from={xray}><CreditV u={u} text="AI RECONSTRUCTION" /></Sequence>

      <Audio src={staticFile("trials/vo_c_real_chris.mp3")} />
      <Audio src={staticFile("audio/sample-bed.mp3")} volume={(f) => interpolate(f, [0, s(0.6), s(11.9), s(12.7)], [0, 0.16, 0.16, 0], CLAMP)} />
      <Sequence from={s(4.0)}><Audio src={staticFile("sfx/thock.mp3")} volume={0.5} /></Sequence>
      <Sequence from={s(7.05)} durationInFrames={s(1.2)}><Audio src={staticFile("sfx/tick_run.mp3")} volume={0.35} /></Sequence>
      <Sequence from={s(8.25)}><Audio src={staticFile("sfx/thock.mp3")} volume={0.75} /></Sequence>
      <Sequence from={s(9.25)}><Audio src={staticFile("sfx/riser.mp3")} volume={0.4} /></Sequence>
      <Sequence from={realEnd - s(0.35)}><Audio src={staticFile("sfx/whoosh.mp3")} volume={0.7} /></Sequence>
    </AbsoluteFill>
  );
};
