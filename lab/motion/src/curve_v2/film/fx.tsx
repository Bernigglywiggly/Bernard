import type React from "react";
import { AbsoluteFill, Img, interpolate, Sequence, staticFile, useCurrentFrame } from "remotion";
import { CLAMP } from "../../lib/anim";
import { C, FILL, HEADC, keyline, MONO } from "../kit";

// Shared pieces for the Roadster film's own segments (1920x1080).
export const M = 100; // edge margin

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
  return <div style={{ position: "absolute", left: M, top: 70, ...MONO, fontSize: 34, color: "#D2CBE3" }}>{text}</div>;
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
