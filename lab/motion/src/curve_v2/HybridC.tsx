import { Video } from "@remotion/media";
import { evolvePath } from "@remotion/paths";
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
import { CLAMP, EASE_IN_OUT, EASE_OUT, unitFor } from "../lib/anim";
import { v2 } from "./palette";

// Style trial C (Oct 2026 reboot): real footage underneath, The Curve v2 graphics on top.
// The clips here are AI stand-ins; in the film they are swapped for short, commented cuts of the real livestream.

export const keyline = (u: number, w = 10): React.CSSProperties => ({
  WebkitTextStroke: `${w * u}px ${v2.colors.black}`,
  paintOrder: "stroke fill",
});

// --------------------------------------------------------------------------------------------- background clips
export const Clip: React.FC<{ src: string; frames: number; push?: [number, number] }> = ({ src, frames, push = [1, 1.06] }) => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{ overflow: "hidden", backgroundColor: v2.colors.black }}>
      <Video
        src={staticFile(src)}
        muted
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
          filter: "saturate(1.2) contrast(1.06)",
          scale: interpolate(frame, [0, frames], push, CLAMP),
        }}
      />
    </AbsoluteFill>
  );
};

// --------------------------------------------------------------------------------------------- hook text
export const Word: React.FC<{ text: string; delay: number; color: string; size: number; glow?: string }> = ({
  text,
  delay,
  color,
  size,
  glow,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame: frame - delay, fps, config: { damping: 12, stiffness: 180, mass: 0.7 } });
  return (
    <span
      style={{
        display: "inline-block",
        marginRight: size * 0.22,
        color,
        fontSize: size,
        fontWeight: 900,
        letterSpacing: "-0.02em",
        lineHeight: 0.92,
        translate: `0 ${interpolate(s, [0, 1], [size * 0.9, 0])}px`,
        rotate: `${interpolate(s, [0, 1], [-8, 0])}deg`,
        scale: interpolate(s, [0, 1], [0.6, 1]),
        opacity: interpolate(s, [0, 0.2], [0, 1], CLAMP),
        textShadow: glow ? `0 0 ${size * 0.35}px ${glow}` : undefined,
        ...keyline(size / 150),
      }}
    >
      {text}
    </span>
  );
};

const Hook: React.FC<{ u: number }> = ({ u }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const out = interpolate(frame, [1.05 * fps, 1.3 * fps], [0, 1], { ...CLAMP, easing: Easing.in(Easing.cubic) });
  return (
    <div
      style={{
        position: "absolute",
        left: 110 * u,
        top: 90 * u,
        fontFamily: v2.fonts.heavy,
        translate: `0 ${-out * 160 * u}px`,
        opacity: 1 - out,
      }}
    >
      <div>
        <Word text="IT" delay={0} color={v2.colors.ink} size={150 * u} />
        <Word text="HAS" delay={2} color={v2.colors.ink} size={150 * u} />
      </div>
      <div>
        <Word text="ROCKETS?" delay={5} color={v2.colors.magenta} size={190 * u} glow={v2.colors.magenta} />
      </div>
    </div>
  );
};

// --------------------------------------------------------------------------------------------- callout
export const Ring: React.FC<{ x: number; y: number; color: string; u: number; start: number }> = ({ x, y, color, u, start }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const period = Math.round(0.8 * fps);
  const t = ((frame - start) % period + period) % period;
  const born = interpolate(frame, [start, start + 0.25 * fps], [0, 1], { ...CLAMP, easing: EASE_OUT });
  return (
    <>
      {[0, 0.5].map((off) => {
        const p = ((t / period + off) % 1);
        return (
          <div
            key={off}
            style={{
              position: "absolute",
              left: x - 60 * u,
              top: y - 60 * u,
              width: 120 * u,
              height: 120 * u,
              borderRadius: "50%",
              border: `${5 * u}px solid ${color}`,
              boxShadow: `0 0 ${24 * u}px ${color}`,
              scale: born * interpolate(p, [0, 1], [0.35, 1.6]),
              opacity: born * interpolate(p, [0, 0.15, 1], [0, 1, 0]),
            }}
          />
        );
      })}
      <div
        style={{
          position: "absolute",
          left: x - 11 * u,
          top: y - 11 * u,
          width: 22 * u,
          height: 22 * u,
          borderRadius: "50%",
          backgroundColor: color,
          boxShadow: `0 0 ${30 * u}px ${color}`,
          scale: born,
        }}
      />
    </>
  );
};

export const Label: React.FC<{ text: string; color: string; u: number; x: number; y: number; start: number }> = ({
  text,
  color,
  u,
  x,
  y,
  start,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame: frame - start, fps, config: { damping: 14, stiffness: 200 } });
  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y,
        padding: `${16 * u}px ${30 * u}px`,
        backgroundColor: color,
        color: v2.colors.black,
        fontFamily: v2.fonts.heavy,
        fontWeight: 850,
        fontSize: 56 * u,
        letterSpacing: "0.02em",
        boxShadow: `0 ${10 * u}px ${40 * u}px rgba(0,0,0,0.55)`,
        transformOrigin: "left center",
        scale: `${interpolate(s, [0, 1], [0, 1])} 1`,
        rotate: `${interpolate(s, [0, 1], [-4, 0])}deg`,
      }}
    >
      <span style={{ opacity: interpolate(s, [0.5, 1], [0, 1], CLAMP) }}>{text}</span>
    </div>
  );
};

export const Leader: React.FC<{ d: string; color: string; u: number; start: number }> = ({ d, color, u, start }) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const p = interpolate(frame, [start, start + 0.35 * fps], [0, 1], { ...CLAMP, easing: EASE_OUT });
  const { strokeDasharray, strokeDashoffset } = evolvePath(p, d);
  return (
    <svg style={{ position: "absolute", inset: 0 }} width={width} height={height} viewBox={`0 0 ${width} ${height}`}>
      <path d={d} fill="none" stroke={v2.colors.black} strokeWidth={14 * u} strokeLinecap="round"
        strokeDasharray={strokeDasharray} strokeDashoffset={strokeDashoffset} />
      <path d={d} fill="none" stroke={color} strokeWidth={6 * u} strokeLinecap="round"
        strokeDasharray={strokeDasharray} strokeDashoffset={strokeDashoffset}
        style={{ filter: `drop-shadow(0 0 ${8 * u}px ${color})` }} />
    </svg>
  );
};

// A label that points at a (possibly moving) target and leaves fast.
export const Callout: React.FC<{
  text: string;
  color: string;
  u: number;
  target: (f: number) => [number, number];
  label: [number, number];
  start: number;
  end: number;
}> = ({ text, color, u, target, label, start, end }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const [tx, ty] = target(frame);
  const out = interpolate(frame, [end - 0.2 * fps, end], [1, 0], CLAMP);
  const lx = label[0];
  const ly = label[1];
  const elbowX = tx;
  const d = `M ${lx + 20 * u} ${ly + 70 * u} L ${elbowX} ${ly + 70 * u} L ${tx} ${ty - 14 * u}`;
  return (
    <AbsoluteFill style={{ opacity: out }}>
      <Leader d={d} color={color} u={u} start={start + 0.1 * fps} />
      <Ring x={tx} y={ty} color={color} u={u} start={start} />
      <Label text={text} color={color} u={u} x={lx} y={ly} start={start} />
    </AbsoluteFill>
  );
};

// --------------------------------------------------------------------------------------------- curiosity counter
const Counter: React.FC<{ u: number }> = ({ u }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const inS = spring({ frame, fps, config: { damping: 16, stiffness: 160 } });
  const locked = frame > 0.9 * fps;
  const roll = (i: number) => Math.floor(random(`d${i}-${frame}`) * 10);
  const digits = locked ? "?.??" : `${roll(0)}.${roll(1)}${roll(2)}`;
  const tag = spring({ frame: frame - 0.95 * fps, fps, config: { damping: 10, stiffness: 220 } });
  const out = interpolate(frame, [1.45 * fps, 1.65 * fps], [0, 1], { ...CLAMP, easing: Easing.in(Easing.cubic) });
  return (
    <div
      style={{
        position: "absolute",
        left: "50%",
        bottom: 110 * u,
        translate: `-50% ${interpolate(inS, [0, 1], [220 * u, 0]) + out * 260 * u}px`,
        display: "flex",
        alignItems: "center",
        gap: 34 * u,
        padding: `${22 * u}px ${44 * u}px`,
        backgroundColor: "rgba(10, 4, 24, 0.82)",
        borderLeft: `${12 * u}px solid ${v2.colors.magenta}`,
        boxShadow: `0 ${16 * u}px ${60 * u}px rgba(0,0,0,0.6)`,
        fontFamily: v2.fonts.heavy,
      }}
    >
      <div style={{ color: v2.colors.cyan, fontSize: 52 * u, fontWeight: 800, lineHeight: 1 }}>0–60 MPH</div>
      <div
        style={{
          color: v2.colors.ink,
          fontSize: 132 * u,
          fontWeight: 900,
          fontVariantNumeric: "tabular-nums",
          lineHeight: 1,
          filter: locked ? "none" : `blur(${5 * u}px)`,
        }}
      >
        {digits}
        <span style={{ fontSize: 64 * u, marginLeft: 10 * u }}>s</span>
      </div>
      <div
        style={{
          position: "absolute",
          right: -30 * u,
          top: -54 * u,
          padding: `${8 * u}px ${18 * u}px`,
          backgroundColor: v2.colors.acid,
          color: v2.colors.black,
          fontSize: 34 * u,
          fontWeight: 900,
          rotate: `${interpolate(tag, [0, 1], [-20, 4])}deg`,
          scale: tag,
        }}
      >
        LATER IN THE VIDEO
      </div>
    </div>
  );
};

// --------------------------------------------------------------------------------------------- "?" push-through
export const PushThrough: React.FC<{ u: number }> = ({ u }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const grow = interpolate(frame, [0, 0.45 * fps], [0.15, 28], {
    ...CLAMP,
    easing: Easing.in(Easing.cubic),
    output: "perceptual-scale",
  } as Parameters<typeof interpolate>[3]);
  const disc = interpolate(frame, [0.1 * fps, 0.4 * fps], [0, 1], { ...CLAMP, easing: EASE_IN_OUT });
  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
      <div
        style={{
          position: "absolute",
          width: 2600 * u,
          height: 2600 * u,
          borderRadius: "50%",
          backgroundColor: v2.colors.magenta,
          scale: disc,
        }}
      />
      <div
        style={{
          fontFamily: v2.fonts.heavy,
          fontWeight: 900,
          fontSize: 300 * u,
          color: v2.colors.acid,
          scale: grow,
          ...keyline(u, 6),
        }}
      >
        ?
      </div>
    </AbsoluteFill>
  );
};

export const Iris: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const r = interpolate(frame, [0, 0.45 * fps], [0, 80], { ...CLAMP, easing: EASE_OUT });
  return <AbsoluteFill style={{ clipPath: `circle(${r}% at 50% 50%)` }}>{children}</AbsoluteFill>;
};

// --------------------------------------------------------------------------------------------- end title
const EndTitle: React.FC<{ u: number }> = ({ u }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame, fps, config: { damping: 13, stiffness: 170 } });
  return (
    <div
      style={{
        position: "absolute",
        left: 110 * u,
        bottom: 120 * u,
        fontFamily: v2.fonts.heavy,
        fontWeight: 900,
        fontSize: 112 * u,
        lineHeight: 0.95,
        color: v2.colors.ink,
        translate: `${interpolate(s, [0, 1], [-200 * u, 0])}px 0`,
        opacity: interpolate(s, [0, 0.3], [0, 1], CLAMP),
        ...keyline(u, 9),
      }}
    >
      HOW DOES <span style={{ color: v2.colors.cyan, textShadow: `0 0 ${40 * u}px ${v2.colors.cyan}` }}>AIR</span>
      <br />
      FLIP A CAR?
    </div>
  );
};

// --------------------------------------------------------------------------------------------- composition
export const HybridC: React.FC = () => {
  const { width, height, fps } = useVideoConfig();
  const u = unitFor(width, height);
  const s = (x: number) => Math.round(x * fps);
  const lerp2 = (f: number, f0: number, f1: number, a: [number, number], b: [number, number]): [number, number] => [
    interpolate(f, [f0, f1], [a[0], b[0]], CLAMP),
    interpolate(f, [f0, f1], [a[1], b[1]], CLAMP),
  ];
  const xray = s(5.35);

  return (
    <AbsoluteFill style={{ backgroundColor: v2.colors.black }}>
      <Sequence durationInFrames={s(5.8)} premountFor={fps}>
        <Clip src="trials/a1_hero.mp4" frames={s(5.8)} />
      </Sequence>

      <Sequence durationInFrames={s(1.35)}>
        <Hook u={u} />
      </Sequence>

      <Sequence from={s(2.55)} durationInFrames={s(1.7)}>
        <Counter u={u} />
      </Sequence>

      <Sequence from={s(3.95)} durationInFrames={s(1.1)}>
        <Callout
          text="COLD-GAS THRUSTERS"
          color={v2.colors.cyan}
          u={u}
          target={(f) => lerp2(f, 0, s(1.1), [0.335 * width, 0.25 * height], [0.33 * width, 0.24 * height])}
          label={[0.42 * width, 0.08 * height]}
          start={0}
          end={s(1.1)}
        />
      </Sequence>

      <Sequence from={s(5.0)} durationInFrames={s(0.8)}>
        <PushThrough u={u} />
      </Sequence>

      <Sequence from={xray} premountFor={fps}>
        <Iris>
          <Clip src="trials/a2_xray.mp4" frames={s(3.7)} push={[1, 1.04]} />
        </Iris>
      </Sequence>

      <Sequence from={xray + s(0.55)} durationInFrames={s(1.9)}>
        <Callout
          text="HIGH-PRESSURE TANK"
          color={v2.colors.cyan}
          u={u}
          target={(f) => lerp2(f, 0, s(1.9), [0.6 * width, 0.42 * height], [0.645 * width, 0.41 * height])}
          label={[0.34 * width, 0.12 * height]}
          start={0}
          end={s(1.9)}
        />
      </Sequence>
      <Sequence from={xray + s(1.25)} durationInFrames={s(1.2)}>
        <Callout
          text="NOZZLES"
          color={v2.colors.acid}
          u={u}
          target={(f) => lerp2(f, 0, s(1.2), [0.69 * width, 0.66 * height], [0.73 * width, 0.67 * height])}
          label={[0.74 * width, 0.36 * height]}
          start={0}
          end={s(1.2)}
        />
      </Sequence>

      <Sequence from={xray + s(2.45)}>
        <EndTitle u={u} />
      </Sequence>

      <AbsoluteFill
        style={{
          background: "radial-gradient(ellipse at center, rgba(0,0,0,0) 55%, rgba(0,0,0,0.55) 100%)",
          pointerEvents: "none",
        }}
      />
      <div
        style={{
          position: "absolute",
          left: 110 * u,
          bottom: 44 * u,
          fontFamily: v2.fonts.mono,
          fontSize: 26 * u,
          letterSpacing: "0.08em",
          color: "rgba(255,255,255,0.8)",
        }}
      >
        STAND-IN CLIP · AI TRIAL (REAL LIVESTREAM CUTS GO HERE)
      </div>
    </AbsoluteFill>
  );
};
