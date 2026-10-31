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
import { Callout, Clip, Iris, keyline, PushThrough, Word } from "./HybridC";
import { v2 } from "./palette";

// Style trial C with the REAL footage (Tesla's own clips of the 15 Oct 2026 Roadster demo, short and credited,
// under our narration and graphics). Timings follow the narration's pauses (vo_c_real_chris.mp3):
// S1 0.00-2.30 · S2 2.84-6.30 · S3 7.06-9.34 · S4 10.05-11.90 (seconds).

export const RealClip: React.FC<{ src: string; trimBeforeSec: number; rate: number; push: [number, number]; frames: number;
  objectPosition?: (f: number) => string }> = ({
  src,
  trimBeforeSec,
  rate,
  push,
  frames,
  objectPosition,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill style={{ overflow: "hidden", backgroundColor: v2.colors.black }}>
      <Video
        src={staticFile(src)}
        muted
        trimBefore={Math.round(trimBeforeSec * fps)}
        playbackRate={rate}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
          objectPosition: objectPosition ? objectPosition(frame) : "50% 50%",
          filter: "saturate(1.15) contrast(1.08) brightness(1.05)",
          scale: interpolate(frame, [0, frames], push, CLAMP),
        }}
      />
    </AbsoluteFill>
  );
};

const HookReal: React.FC<{ u: number }> = ({ u }) => {
  const frame = useCurrentFrame();
  const { fps, height } = useVideoConfig();
  const out = interpolate(frame, [2.15 * fps, 2.45 * fps], [0, 1], { ...CLAMP, easing: Easing.in(Easing.cubic) });
  // Negative delays: the words have already landed by frame 0, so frame 0 is a finished composition.
  return (
    <div style={{ position: "absolute", left: 110 * u, top: 0.56 * height, fontFamily: v2.fonts.heavy,
      translate: `0 ${-out * 160 * u}px`, opacity: 1 - out }}>
      <div>
        <Word text="WHY" delay={-12} color={v2.colors.ink} size={128 * u} />
        <Word text="ISN'T" delay={-10} color={v2.colors.ink} size={128 * u} />
        <Word text="IT" delay={-8} color={v2.colors.ink} size={128 * u} />
      </div>
      <div>
        <Word text="FALLING?" delay={-5} color={v2.colors.magenta} size={168 * u} glow={v2.colors.magenta} />
      </div>
    </div>
  );
};

const Counter081: React.FC<{ u: number }> = ({ u }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const inS = spring({ frame, fps, config: { damping: 16, stiffness: 160 } });
  const lockAt = 1.25 * fps;
  const locked = frame >= lockAt;
  const roll = (i: number) => Math.floor(random(`r${i}-${frame}`) * 10);
  const digits = locked ? "0.81" : `${roll(0)}.${roll(1)}${roll(2)}`;
  const pop = spring({ frame: frame - lockAt, fps, config: { damping: 9, stiffness: 240 } });
  const tag = spring({ frame: frame - lockAt - 4, fps, config: { damping: 11, stiffness: 220 } });
  const out = interpolate(frame, [2.0 * fps, 2.2 * fps], [0, 1], { ...CLAMP, easing: Easing.in(Easing.cubic) });
  return (
    <div style={{ position: "absolute", left: "50%", bottom: 120 * u,
      translate: `-50% ${interpolate(inS, [0, 1], [240 * u, 0]) + out * 280 * u}px`,
      display: "flex", alignItems: "center", gap: 34 * u, padding: `${22 * u}px ${44 * u}px`,
      backgroundColor: "rgba(10, 4, 24, 0.84)", borderLeft: `${12 * u}px solid ${v2.colors.magenta}`,
      boxShadow: `0 ${16 * u}px ${60 * u}px rgba(0,0,0,0.6)`, fontFamily: v2.fonts.heavy }}>
      <div style={{ color: v2.colors.cyan, fontSize: 52 * u, fontWeight: 800, lineHeight: 1 }}>0–60 MPH</div>
      <div style={{ color: locked ? v2.colors.acid : v2.colors.ink, fontSize: 140 * u, fontWeight: 900,
        fontVariantNumeric: "tabular-nums", lineHeight: 1, filter: locked ? "none" : `blur(${5 * u}px)`,
        scale: locked ? interpolate(pop, [0, 1], [1.35, 1]) : 1,
        textShadow: locked ? `0 0 ${36 * u}px ${v2.colors.acid}` : undefined }}>
        {digits}
        <span style={{ fontSize: 64 * u, marginLeft: 10 * u }}>s</span>
      </div>
      <div style={{ position: "absolute", right: -30 * u, top: -58 * u, padding: `${8 * u}px ${18 * u}px`,
        backgroundColor: v2.colors.ink, color: v2.colors.black, fontSize: 32 * u, fontWeight: 900,
        rotate: `${interpolate(tag, [0, 1], [-20, 3])}deg`, scale: tag }}>
        TESLA'S OWN TIMING
      </div>
    </div>
  );
};

const KickWord: React.FC<{ u: number }> = ({ u }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame, fps, config: { damping: 10, stiffness: 200 } });
  const out = interpolate(frame, [0.75 * fps, 0.95 * fps], [1, 0], CLAMP);
  return (
    <div style={{ position: "absolute", right: 110 * u, top: 110 * u, fontFamily: v2.fonts.heavy, fontWeight: 900,
      fontSize: 120 * u, color: v2.colors.acid, opacity: out,
      rotate: `${interpolate(s, [0, 1], [18, -4])}deg`, scale: interpolate(s, [0, 1], [0.4, 1]),
      textShadow: `0 0 ${30 * u}px ${v2.colors.acid}`, ...keyline(u, 9) }}>
      AND A KICKFLIP
    </div>
  );
};

const EndReal: React.FC<{ u: number }> = ({ u }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame, fps, config: { damping: 13, stiffness: 170 } });
  return (
    <div style={{ position: "absolute", left: 110 * u, bottom: 130 * u, fontFamily: v2.fonts.heavy, fontWeight: 900,
      fontSize: 120 * u, lineHeight: 0.95, color: v2.colors.ink,
      translate: `${interpolate(s, [0, 1], [-220 * u, 0])}px 0`, opacity: interpolate(s, [0, 0.3], [0, 1], CLAMP),
      ...keyline(u, 9) }}>
      STUCK UP THERE
      <br />
      BY <span style={{ color: v2.colors.magenta, textShadow: `0 0 ${40 * u}px ${v2.colors.magenta}` }}>WHAT?</span>
    </div>
  );
};

const Credit: React.FC<{ u: number; text: string }> = ({ u, text }) => (
  <div style={{ position: "absolute", left: 110 * u, bottom: 44 * u, fontFamily: v2.fonts.mono, fontSize: 28 * u,
    letterSpacing: "0.08em", color: "rgba(255,255,255,0.85)", textShadow: "0 0 8px rgba(0,0,0,0.9)" }}>
    {text}
  </div>
);

export const HybridCReal: React.FC = () => {
  const { width, height, fps } = useVideoConfig();
  const u = unitFor(width, height);
  const s = (x: number) => Math.round(x * fps);
  const realEnd = s(10.2);
  const xray = s(10.35);
  const pt = (f: number, keys: [number, number, number][]): [number, number] => [
    interpolate(f, keys.map((k) => k[0]), keys.map((k) => k[1] * width), CLAMP),
    interpolate(f, keys.map((k) => k[0]), keys.map((k) => k[2] * height), CLAMP),
  ];

  return (
    <AbsoluteFill style={{ backgroundColor: v2.colors.black }}>
      {/* S1: the hang, slowed so "then it lets go" lands on the drop */}
      <Sequence durationInFrames={s(2.84)} premountFor={fps}>
        <RealClip src="trials/ramp_hang_drop.mp4" trimBeforeSec={0} rate={0.36} push={[1.04, 1.12]} frames={s(2.84)} />
      </Sequence>
      {/* S2 + S3: the drop, the jets, the smoke landing at normal speed */}
      <Sequence from={s(2.84)} durationInFrames={s(6.36)} premountFor={fps}>
        <RealClip src="trials/ramp_hang_drop.mp4" trimBeforeSec={1.02} rate={1} push={[1.02, 1.07]} frames={s(6.0)} />
      </Sequence>
      {/* the escalation beat before the question */}
      <Sequence from={s(9.2)} durationInFrames={realEnd - s(9.2) + s(0.4)} premountFor={fps}>
        <RealClip src="trials/kickflip_side.mp4" trimBeforeSec={0.55} rate={0.85} push={[1.0, 1.05]} frames={s(1.8)} />
      </Sequence>

      <Sequence durationInFrames={s(2.5)}>
        <HookReal u={u} />
      </Sequence>

      <Sequence from={s(4.0)} durationInFrames={s(1.6)}>
        <Callout
          text="10 GAS THRUSTERS"
          color={v2.colors.cyan}
          u={u}
          target={(f) => pt(f, [[0, 0.435, 0.535], [s(0.8), 0.44, 0.54], [s(1.6), 0.47, 0.56]])}
          label={[0.07 * width, 0.14 * height]}
          start={0}
          end={s(1.6)}
        />
      </Sequence>

      <Sequence from={s(7.0)} durationInFrames={s(2.25)}>
        <Counter081 u={u} />
      </Sequence>

      <Sequence from={s(9.25)} durationInFrames={s(1.0)}>
        <KickWord u={u} />
      </Sequence>

      <Sequence from={realEnd - s(0.35)} durationInFrames={s(0.8)}>
        <PushThrough u={u} />
      </Sequence>
      <Sequence from={xray} premountFor={fps}>
        <Iris>
          <Clip src="trials/a2_xray.mp4" frames={s(2.6)} push={[1, 1.04]} />
        </Iris>
      </Sequence>
      <Sequence from={xray + s(0.6)}>
        <EndReal u={u} />
      </Sequence>

      <AbsoluteFill style={{ background: "radial-gradient(ellipse at center, rgba(0,0,0,0) 55%, rgba(0,0,0,0.5) 100%)" }} />
      <Sequence durationInFrames={realEnd}>
        <Credit u={u} text="FOOTAGE: TESLA · ROADSTER DEMO, 15 OCT 2026" />
      </Sequence>
      <Sequence from={xray}>
        <Credit u={u} text="AI RECONSTRUCTION · NOT THE REAL CAR" />
      </Sequence>

      <Audio src={staticFile("trials/vo_c_real_chris.mp3")} />
      {/* bed under the voice, ducked; in-house synthesised audio (nothing for Content ID to claim) */}
      <Audio src={staticFile("audio/sample-bed.mp3")} volume={(f) => interpolate(f, [0, s(0.6), s(11.9), s(12.7)], [0, 0.16, 0.16, 0], CLAMP)} />
      <Sequence from={s(4.0)}><Audio src={staticFile("sfx/thock.mp3")} volume={0.5} /></Sequence>
      <Sequence from={s(7.05)} durationInFrames={s(1.2)}><Audio src={staticFile("sfx/tick_run.mp3")} volume={0.35} /></Sequence>
      <Sequence from={s(8.25)}><Audio src={staticFile("sfx/thock.mp3")} volume={0.75} /></Sequence>
      <Sequence from={s(9.25)}><Audio src={staticFile("sfx/riser.mp3")} volume={0.4} /></Sequence>
      <Sequence from={realEnd - s(0.35)}><Audio src={staticFile("sfx/whoosh.mp3")} volume={0.7} /></Sequence>
    </AbsoluteFill>
  );
};
