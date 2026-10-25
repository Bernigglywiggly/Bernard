import type React from "react";
import { AbsoluteFill, Img, interpolate, Sequence, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { CLAMP } from "../../lib/anim";
import { C, FILL, HEADC, keyline, MONO, pop, Sfx as KitSfx } from "../kit";

// Shared pieces for the Roadster film's own segments (1920x1080).
export const M = 100; // edge margin
export const SAFE_TOP = 140; // nothing important above this: YouTube's hover title covers the top of the frame

// Critic round 1: 27 effect hits reached the ceiling, 5-6 dB above the voice. Every film effect plays 5 dB lower.
export const SFX_GAIN = 0.56;
export const Sfx: typeof KitSfx = (p) => <KitSfx {...p} volume={(p.volume ?? 0.45) * SFX_GAIN} />;

// Evidence stamps: whose claim a number is, in the same colour all film long (the film's signature, critic round 1).
// SHOWN LIVE = it happened on camera; TESLA SAYS = Tesla's claim, unchecked; OUR MATHS = our own sum; UNPROVEN = nobody
// outside the company has checked it; CHECKED = independently measured. `text` overrides the wording, `note` names
// the source under it. 54 px type, always placed inside title-safe.
export type Evidence = "live" | "tesla" | "ours" | "unproven" | "checked";
const EV: Record<Evidence, { bg: string; fg: string; text: string }> = {
  live: { bg: C.cyan, fg: C.black, text: "SHOWN LIVE" },
  tesla: { bg: C.magenta, fg: C.ink, text: "TESLA SAYS" },
  ours: { bg: C.acid, fg: C.black, text: "OUR MATHS" },
  unproven: { bg: C.warn, fg: C.ink, text: "UNPROVEN" },
  checked: { bg: C.ink, fg: C.black, text: "INDEPENDENTLY TIMED" },
};
const Glyph: React.FC<{ kind: Evidence; color: string; s: number }> = ({ kind, color, s }) => (
  <svg width={s} height={s} viewBox="0 0 40 40" style={{ flexShrink: 0 }}>
    {kind === "live" ? <><circle cx={20} cy={20} r={11} fill={color} /><circle cx={20} cy={20} r={17} fill="none" stroke={color} strokeWidth={3.5} /></> : null}
    {kind === "tesla" ? <path d="M6 30 L6 20 Q6 9 15 7 L16 11 Q11 13 11 18 L16 18 L16 30 Z M23 30 L23 20 Q23 9 32 7 L33 11 Q28 13 28 18 L33 18 L33 30 Z" fill={color} /> : null}
    {kind === "ours" ? <><rect x={6} y={11} width={28} height={6} fill={color} /><rect x={6} y={23} width={28} height={6} fill={color} /></> : null}
    {kind === "unproven" ? <path d="M13 14 Q13 6 20.5 6 Q28 6 28 13.5 Q28 18 23 20.5 Q22 21.5 22 24 L22 26 L18 26 L18 23 Q18 19 21.5 17 Q24 15.5 24 13.5 Q24 10 20.5 10 Q17 10 17 14 Z M18 29 L22 29 L22 34 L18 34 Z" fill={color} /> : null}
    {kind === "checked" ? <path d="M6 21 L11 16 L17 22 L30 8 L35 13 L17 32 Z" fill={color} /> : null}
  </svg>
);
export const EvidenceStamp: React.FC<{ kind: Evidence; at: number; left: number; top: number; text?: string; note?: string;
  until?: number; size?: number }> = ({ kind, at, left, top, text, note, until = Infinity, size = 54 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < at || frame >= until) return null;
  const s = pop(frame, at, fps, 260, 11);
  const ev = EV[kind];
  return (
    <div style={{ position: "absolute", left, top: Math.max(top, SAFE_TOP), transformOrigin: "0% 50%", scale: interpolate(s, [0, 1], [1.35, 1]),
      opacity: interpolate(s, [0, 0.25], [0, 1], CLAMP), rotate: `${interpolate(s, [0, 1], [-5, -1.5])}deg` }}>
      <div style={{ display: "inline-flex", alignItems: "center", gap: size * 0.3, padding: `${size * 0.16}px ${size * 0.4}px ${size * 0.2}px ${size * 0.26}px`,
        backgroundColor: ev.bg, color: ev.fg, border: `5px solid ${C.black}`, boxShadow: `8px 8px 0 ${C.black}` }}>
        <Glyph kind={kind} color={ev.fg} s={size * 0.95} />
        <div style={{ ...HEADC, fontSize: size, lineHeight: 1 }}>{text ?? ev.text}</div>
      </div>
      {note ? <div style={{ ...MONO, fontSize: 36, color: C.ink, marginTop: 12, padding: "4px 12px", backgroundColor: "rgba(0,0,0,0.72)", display: "table" }}>{note}</div> : null}
    </div>
  );
};

// "FOOTAGE: TESLA / YOUTUBE" strip, bottom-left, whenever Tesla's footage is on screen.
export const TeslaCredit: React.FC<{ show: [number, number][]; text?: string }> = ({ show, text = "FOOTAGE: TESLA / YOUTUBE" }) => {
  const frame = useCurrentFrame();
  if (!show.some(([a, b]) => frame >= a && frame < b)) return null;
  return (
    <div style={{ position: "absolute", left: 0, bottom: 60, padding: "10px 24px 10px 100px", backgroundColor: "rgba(0,0,0,0.72)", ...MONO,
      fontSize: 34, color: C.ink }}>{text}</div>
  );
};

// "3D ILLUSTRATION" disclosure, top-left, whenever our Blender renders are on screen.
export const Disclose: React.FC<{ show: [number, number][]; text?: string }> = ({ show, text = "OUR 3D ILLUSTRATION" }) => {
  const frame = useCurrentFrame();
  if (!show.some(([a, b]) => frame >= a && frame < b)) return null;
  // bottom-right, clear of YouTube's hover title and of the footage credit (bottom-left)
  return (
    <div style={{ position: "absolute", right: 0, bottom: 60, padding: "10px 100px 10px 24px", backgroundColor: "rgba(0,0,0,0.72)", ...MONO, fontSize: 34,
      color: "#D2CBE3" }}>{text}</div>
  );
};

// A still with a slow push (for holding the last frame of a render under an overlay).
export const HoldStill: React.FC<{ src: string; from: number; dur: number; push?: [number, number]; origin?: string }> = ({ src, from, dur,
  push = [1, 1.05], origin = "50% 50%" }) => {
  const frame = useCurrentFrame();
  return (
    <Sequence from={from} durationInFrames={dur}>
      <AbsoluteFill style={{ scale: interpolate(frame, [from, from + dur], push, CLAMP), transformOrigin: origin }}>
        <Img src={staticFile(src)} style={FILL} />
      </AbsoluteFill>
    </Sequence>
  );
};

// A bottom-to-top darkening so type reads over footage.
export const Shade: React.FC<{ from?: "left" | "bottom" | "top"; strength?: number }> = ({ from = "left", strength = 0.8 }) => {
  const dir = from === "left" ? "90deg" : from === "bottom" ? "0deg" : "180deg";
  return <AbsoluteFill style={{ background: `linear-gradient(${dir}, rgba(5,1,12,${strength}) 0%, rgba(5,1,12,${strength * 0.6}) 40%, rgba(5,1,12,0) 75%)` }} />;
};

export const Big: React.FC<{ children: React.ReactNode; size: number; color?: string; style?: React.CSSProperties }> = ({ children, size,
  color = C.ink, style }) => (
  <div style={{ ...HEADC, fontSize: size, color, ...keyline(size / 150, 10), ...style }}>{children}</div>
);
