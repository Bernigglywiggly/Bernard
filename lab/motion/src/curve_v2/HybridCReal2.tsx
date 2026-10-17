import { Audio, Video } from "@remotion/media";
import { evolvePath } from "@remotion/paths";
import type React from "react";
import {
  AbsoluteFill,
  Easing,
  interpolate,
  Sequence,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { CLAMP, EASE_OUT, unitFor } from "../lib/anim";
import { Callout, keyline, Word } from "./HybridC";
import { v2 } from "./palette";

// Style trial C, v2 (after CRITIC_C_v1, 5/10): one question, answered with the real footage.
// Narration vo_c_real_v2_chris.mp3 (16.25 s): S1 0-2.6 hang · S2 3.3-7.1 fans + 2x · S3 7.9-11.9 drop, jets, landing ·
// S4 12.6-15.8 "vacuumed" over the opening image again. Footage: Tesla's 4K upload, punched in, slow motion made with
// motion-compensated interpolation (no stutter). Every claim: lab/research/TESLA_ROADSTER_FACTS.md §2, §3, §4.

const Shot: React.FC<{ src: string; frames: number; rate?: number; push: [number, number] }> = ({ src, frames, rate = 1, push }) => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{ overflow: "hidden", backgroundColor: v2.colors.black }}>
      <Video src={staticFile(src)} muted playbackRate={rate}
        style={{ width: "100%", height: "100%", objectFit: "cover",
          filter: "saturate(1.12) contrast(1.08) brightness(1.06)",
          scale: interpolate(frame, [0, frames], push, { ...CLAMP, easing: Easing.inOut(Easing.sin) }) }} />
    </AbsoluteFill>
  );
};

const Hook: React.FC<{ u: number }> = ({ u }) => {
  const frame = useCurrentFrame();
  const { fps, height } = useVideoConfig();
  const out = interpolate(frame, [2.35 * fps, 2.65 * fps], [0, 1], { ...CLAMP, easing: Easing.in(Easing.cubic) });
  return (
    <div style={{ position: "absolute", left: 84 * u, top: 0.28 * height, fontFamily: v2.fonts.heavy,
      translate: `${-out * 200 * u}px 0`, opacity: 1 - out }}>
      <div><Word text="WHY" delay={-12} color={v2.colors.ink} size={132 * u} /></div>
      <div><Word text="ISN'T IT" delay={-9} color={v2.colors.ink} size={132 * u} /></div>
      <div><Word text="FALLING?" delay={-5} color={v2.colors.magenta} size={136 * u} glow={v2.colors.magenta} /></div>
    </div>
  );
};

// Side view of the curl: the car under the top of the ramp, weight down, fan suction up at twice the length.
const Diagram: React.FC<{ u: number }> = ({ u }) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const t = (sec: number) => sec * fps;
  const panelIn = spring({ frame, fps, config: { damping: 16, stiffness: 170 } });
  const panelOut = interpolate(frame, [t(3.9), t(4.15)], [0, 1], { ...CLAMP, easing: Easing.in(Easing.cubic) });
  const ramp = interpolate(frame, [t(0.05), t(0.6)], [0, 1], { ...CLAMP, easing: EASE_OUT });
  const carIn = spring({ frame: frame - t(0.45), fps, config: { damping: 12, stiffness: 200 } });
  const wArrow = interpolate(frame, [t(0.6), t(0.9)], [0, 1], { ...CLAMP, easing: EASE_OUT });
  const sArrow = interpolate(frame, [t(1.05), t(1.45)], [0, 1], { ...CLAMP, easing: EASE_OUT });
  const twoX = spring({ frame: frame - t(2.9), fps, config: { damping: 9, stiffness: 230 } });

  // panel geometry (px, composition space)
  const W = 0.31 * width;
  const H = 0.66 * height;
  const cx = W / 2;
  const rampD = `M ${W * 0.92} ${H * 0.98} C ${W * 0.95} ${H * 0.35}, ${W * 0.7} ${H * 0.12}, ${W * 0.38} ${H * 0.16} C ${W * 0.12} ${H * 0.2}, ${W * 0.06} ${H * 0.42}, ${W * 0.1} ${H * 0.55}`;
  const ramp1 = evolvePath(ramp, rampD);
  const carY = H * 0.245;
  const carW = W * 0.34;
  const carH = H * 0.085;
  const arrow = (x1: number, y1: number, x2: number, y2: number, p: number, color: string, w: number) => {
    const x = x1 + (x2 - x1) * p;
    const y = y1 + (y2 - y1) * p;
    const ang = Math.atan2(y2 - y1, x2 - x1);
    const hs = 44 * u;
    return p <= 0.001 ? null : (
      <g>
        <line x1={x1} y1={y1} x2={x} y2={y} stroke={v2.colors.black} strokeWidth={w + 10 * u} strokeLinecap="round" />
        <line x1={x1} y1={y1} x2={x} y2={y} stroke={color} strokeWidth={w} strokeLinecap="round"
          style={{ filter: `drop-shadow(0 0 ${10 * u}px ${color})` }} />
        <polygon points={`${x},${y} ${x - hs * Math.cos(ang - 0.5)},${y - hs * Math.sin(ang - 0.5)} ${x - hs * Math.cos(ang + 0.5)},${y - hs * Math.sin(ang + 0.5)}`}
          fill={color} stroke={v2.colors.black} strokeWidth={4 * u} />
      </g>
    );
  };
  const label = (text: string, x: number, y: number, color: string, show: number, size = 40) => (
    <div style={{ position: "absolute", left: x, top: y, fontFamily: v2.fonts.heavy, fontWeight: 900, fontSize: size * u,
      color, opacity: show, translate: `${(1 - show) * -20 * u}px 0`, ...keyline(u, 7) }}>{text}</div>
  );

  return (
    <div style={{ position: "absolute", left: 0.035 * width, top: 0.15 * height, width: W, height: H,
      backgroundColor: "rgba(8, 4, 22, 0.86)", borderRadius: 22 * u, border: `${3 * u}px solid rgba(61,255,242,0.35)`,
      boxShadow: `0 ${20 * u}px ${70 * u}px rgba(0,0,0,0.7)`,
      translate: `${interpolate(panelIn, [0, 1], [-W - 80 * u, 0]) - panelOut * (W + 120 * u)}px 0` }}>
      <div style={{ position: "absolute", left: 28 * u, top: 22 * u, fontFamily: v2.fonts.heavy, fontWeight: 900,
        fontSize: 40 * u, color: v2.colors.cyan, letterSpacing: "0.04em" }}>SIDE VIEW</div>
      <svg width={W} height={H} style={{ position: "absolute", inset: 0 }}>
        <path d={rampD} fill="none" stroke="#9AA3AD" strokeWidth={26 * u} strokeLinecap="round"
          strokeDasharray={ramp1.strokeDasharray} strokeDashoffset={ramp1.strokeDashoffset} />
        <path d={rampD} fill="none" stroke="#E8EEF2" strokeWidth={4 * u} strokeDasharray={`${18 * u} ${16 * u}`}
          opacity={ramp} />
        {/* car, upside down under the top of the curl */}
        <g transform={`translate(${cx - carW / 2 + W * 0.02}, ${carY}) scale(${carIn})`} style={{ transformOrigin: `${carW / 2}px 0px` }}>
          <rect x={0} y={0} width={carW} height={carH} rx={carH * 0.45} fill="#EDEFF2" stroke={v2.colors.black} strokeWidth={4 * u} />
          <rect x={carW * 0.3} y={carH * 0.8} width={carW * 0.42} height={carH * 0.55} rx={carH * 0.3} fill="#20242B" />
          <circle cx={carW * 0.2} cy={0} r={carH * 0.42} fill="#15181D" stroke="#EDEFF2" strokeWidth={3 * u} />
          <circle cx={carW * 0.8} cy={0} r={carH * 0.42} fill="#15181D" stroke="#EDEFF2" strokeWidth={3 * u} />
        </g>
        {/* free-body view: weight pulls down (left), fan suction pulls up into the ramp (right), drawn twice as long */}
        {arrow(cx - W * 0.1, carY + carH * 1.5, cx - W * 0.1, carY + carH * 1.5 + H * 0.16, wArrow, v2.colors.warn, 16 * u)}
        {arrow(cx + W * 0.14, carY + carH * 1.5 + H * 0.32, cx + W * 0.14, carY + carH * 0.9, sArrow, v2.colors.cyan, 22 * u)}
      </svg>
      {label("WEIGHT", cx - W * 0.42, carY + carH * 1.5 + H * 0.07, v2.colors.warn, wArrow)}
      {label("FAN", cx + W * 0.2, carY + carH * 1.5 + H * 0.12, v2.colors.cyan, sArrow)}
      {label("SUCTION", cx + W * 0.2, carY + carH * 1.5 + H * 0.12 + 44 * u, v2.colors.cyan, sArrow)}
      <div style={{ position: "absolute", left: cx - W * 0.2, top: carY + carH * 1.5 + H * 0.4, padding: `${6 * u}px ${16 * u}px`,
        backgroundColor: v2.colors.acid, color: v2.colors.black, fontFamily: v2.fonts.heavy, fontWeight: 900, fontSize: 64 * u,
        rotate: `${interpolate(twoX, [0, 1], [-25, -6])}deg`, scale: twoX }}>UP TO 2×</div>
    </div>
  );
};

const EndWord: React.FC<{ u: number }> = ({ u }) => {
  const frame = useCurrentFrame();
  const { fps, height } = useVideoConfig();
  const s = spring({ frame, fps, config: { damping: 10, stiffness: 210 } });
  return (
    <div style={{ position: "absolute", left: 84 * u, top: 0.4 * height, fontFamily: v2.fonts.heavy, fontWeight: 900,
      fontSize: 112 * u, color: v2.colors.magenta, lineHeight: 1, textShadow: `0 0 ${50 * u}px ${v2.colors.magenta}`,
      scale: interpolate(s, [0, 1], [1.6, 1]), opacity: interpolate(s, [0, 0.25], [0, 1], CLAMP),
      rotate: `${interpolate(s, [0, 1], [-8, -3])}deg`, ...keyline(u, 12) }}>
      VACUUMED.
    </div>
  );
};

const CreditStrip: React.FC<{ u: number }> = ({ u }) => (
  <div style={{ position: "absolute", left: 0, bottom: 52 * u, padding: `${10 * u}px ${22 * u}px ${10 * u}px ${84 * u}px`,
    backgroundColor: "rgba(0,0,0,0.72)", fontFamily: v2.fonts.mono, fontWeight: 500, fontSize: 40 * u,
    letterSpacing: "0.04em", color: v2.colors.ink }}>
    FOOTAGE: TESLA · ROADSTER DEMO, 15 OCT 2026
  </div>
);

export const HybridCReal2: React.FC = () => {
  const { width, height, fps } = useVideoConfig();
  const u = unitFor(width, height);
  const s = (x: number) => Math.round(x * fps);
  const dropFrom = s(7.4);
  const rewindFrom = s(11.55);
  const endFrom = s(12.2);
  const pt = (f: number, keys: [number, number, number][]): [number, number] => [
    interpolate(f, keys.map((k) => k[0]), keys.map((k) => k[1] * width), CLAMP),
    interpolate(f, keys.map((k) => k[0]), keys.map((k) => k[2] * height), CLAMP),
  ];

  return (
    <AbsoluteFill style={{ backgroundColor: v2.colors.black }}>
      <Sequence durationInFrames={dropFrom} premountFor={fps}>
        <Shot src="trials/hang_slow8_punch.mp4" frames={dropFrom} push={[1.02, 1.1]} />
      </Sequence>
      <Sequence from={dropFrom} durationInFrames={rewindFrom - dropFrom} premountFor={fps}>
        <Shot src="trials/drop_punch.mp4" frames={rewindFrom - dropFrom} rate={0.9} push={[1.0, 1.05]} />
      </Sequence>
      <Sequence from={rewindFrom} durationInFrames={endFrom - rewindFrom} premountFor={fps}>
        <Shot src="trials/rewind.mp4" frames={endFrom - rewindFrom} push={[1.05, 1.0]} />
      </Sequence>
      <Sequence from={endFrom} premountFor={fps}>
        <Shot src="trials/hang_slow8_punch.mp4" frames={s(4.4)} push={[1.0, 1.16]} />
      </Sequence>

      <Sequence durationInFrames={s(2.7)}><Hook u={u} /></Sequence>
      <Sequence from={s(3.25)} durationInFrames={s(4.2)}><Diagram u={u} /></Sequence>

      <Sequence from={s(9.2)} durationInFrames={s(1.5)}>
        <Callout text="GAS JETS ROLL IT UPRIGHT" color={v2.colors.cyan} u={u}
          target={(f) => pt(f, [[0, 0.352, 0.525], [s(0.8), 0.355, 0.52], [s(1.5), 0.37, 0.515]])}
          label={[0.06 * width, 0.16 * height]} start={0} end={s(1.5)} />
      </Sequence>

      <Sequence from={s(14.6)}><EndWord u={u} /></Sequence>

      <AbsoluteFill style={{ background: "radial-gradient(ellipse at center, rgba(0,0,0,0) 58%, rgba(0,0,0,0.5) 100%)" }} />
      <CreditStrip u={u} />

      <Audio src={staticFile("trials/vo_c_real_v2_chris.mp3")} />
      <Audio src={staticFile("audio/sample-bed.mp3")} volume={(f) => interpolate(f, [0, s(0.6), s(15.9), s(16.6)], [0, 0.14, 0.14, 0], CLAMP)} />
      <Sequence from={s(3.9)}><Audio src={staticFile("sfx/thock.mp3")} volume={0.45} /></Sequence>
      <Sequence from={s(4.35)}><Audio src={staticFile("sfx/thock.mp3")} volume={0.6} /></Sequence>
      <Sequence from={s(6.15)}><Audio src={staticFile("sfx/form.mp3")} volume={0.45} /></Sequence>
      <Sequence from={dropFrom}><Audio src={staticFile("sfx/whoosh.mp3")} volume={0.55} /></Sequence>
      <Sequence from={s(10.5)}><Audio src={staticFile("sfx/thock.mp3")} volume={0.55} /></Sequence>
      <Sequence from={rewindFrom}><Audio src={staticFile("sfx/rewind.mp3")} volume={0.65} /></Sequence>
      <Sequence from={s(14.6)}><Audio src={staticFile("sfx/thock.mp3")} volume={0.8} /></Sequence>
    </AbsoluteFill>
  );
};
