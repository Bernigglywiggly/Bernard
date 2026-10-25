import type React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { CLAMP } from "../../lib/anim";
import { C, HEADC, Headline, keyline } from "../kit";
import { M, SAFE_TOP, Sfx } from "./fx";
import { cue, segFrames } from "./util";

// Bridge 1 (v2, re-aimed two segments ahead at S5): "In a minute, the Formula One fan car that won its only race and
// was never raced again." A drawn 1978-style single-seater, backlit, in silhouette, filling the frame, its tail fan
// spinning; the name stays hidden until S5. Facts §13.2 (BT46B: raced once, won once, withdrawn).
const D = segFrames("b1");

export const B1Bridge: React.FC = () => {
  const frame = useCurrentFrame();
  const spin = frame * 24;
  const k = (a: number, b: number) => interpolate(frame, [a, b], [0, 1], CLAMP);
  const backlight = k(0, 18);
  const lit = k(cue("b1", "never") - 6, cue("b1", "never") + 6);
  return (
    <AbsoluteFill style={{ backgroundColor: C.black }}>
      {/* the backlight: a bright wash behind the car, so it reads as a silhouette with a cyan rim */}
      <AbsoluteFill style={{ opacity: backlight, background: "radial-gradient(ellipse 55% 42% at 54% 66%, rgba(61,255,242,0.62) 0%, rgba(40,20,90,0.75) 45%, #000 78%)" }} />
      <AbsoluteFill style={{ scale: interpolate(frame, [0, D], [1, 1.06], CLAMP), transformOrigin: "55% 66%" }}>
        <svg width={1920} height={1080} style={{ position: "absolute", inset: 0 }}>
          <g transform="translate(930 700) scale(1.42)">
            {/* low open-wheel racer, side view, in silhouette */}
            <path d="M -520 40 L -380 30 L -180 0 L -60 -40 L 60 -60 L 160 -40 L 330 -10 L 520 0 L 540 40 L -540 60 Z" fill="#05060A" stroke={C.cyan} strokeWidth={5} />
            <path d="M 40 -60 C 60 -110, 140 -110, 160 -50" fill="#05060A" stroke={C.cyan} strokeWidth={5} />
            <circle cx={-380} cy={60} r={72} fill="#05060A" stroke={C.cyan} strokeWidth={5} />
            <circle cx={380} cy={60} r={72} fill="#05060A" stroke={C.cyan} strokeWidth={5} />
            {/* the fan at the tail */}
            <g transform={`translate(560 -10) rotate(${spin})`}>
              <circle r={110} fill="#05060A" stroke={C.magenta} strokeWidth={8} />
              {Array.from({ length: 6 }).map((_, i) => (
                <path key={i} d="M 0 0 L 95 -18 L 95 18 Z" fill={C.magenta} transform={`rotate(${i * 60})`} opacity={0.85} />
              ))}
            </g>
          </g>
        </svg>
      </AbsoluteFill>
      <Headline at={cue("b1", "only") - 6} left={M} top={SAFE_TOP} lines={[{ text: "ONE RACE.", size: 130 }]} />
      <div style={{ position: "absolute", left: M, top: SAFE_TOP + 140, ...HEADC, fontSize: 130, color: C.acid, opacity: lit, ...keyline(0.85, 10) }}>ONE WIN. THEN GONE.</div>
      <Sfx at={0} name="whoosh" volume={0.3} />
    </AbsoluteFill>
  );
};
