import type React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { CLAMP } from "../../lib/anim";
import { BG_NIGHT, C, HEADC, Headline, keyline, Sfx } from "../kit";
import { M } from "./fx";
import { cue, segFrames } from "./util";

// Bridge 2: "In a minute, the racing car that used this trick in its only race, won it, and was never raced again."
// A drawn single-seat racer in silhouette with a big fan at its tail, spinning; the name stays hidden until S5.
const D = segFrames("b2");

export const B2Bridge: React.FC = () => {
  const frame = useCurrentFrame();
  const spin = frame * 24;
  const lit = interpolate(frame, [cue("b2", "won") - 6, cue("b2", "won") + 6], [0, 1], CLAMP);
  return (
    <AbsoluteFill style={{ background: BG_NIGHT, scale: interpolate(frame, [0, D], [1, 1.05], CLAMP) }}>
      <svg width={1920} height={1080} style={{ position: "absolute", inset: 0 }}>
        <g transform="translate(980 640)">
          {/* low open-wheel racer, side view, in silhouette */}
          <path d="M -520 40 L -380 30 L -180 0 L -60 -40 L 60 -60 L 160 -40 L 330 -10 L 520 0 L 540 40 L -540 60 Z" fill="#0C0E14" stroke={C.cyan} strokeWidth={6} />
          <path d="M 40 -60 C 60 -110, 140 -110, 160 -50" fill="#0C0E14" stroke={C.cyan} strokeWidth={6} />
          <circle cx={-380} cy={60} r={72} fill="#0C0E14" stroke={C.cyan} strokeWidth={6} />
          <circle cx={380} cy={60} r={72} fill="#0C0E14" stroke={C.cyan} strokeWidth={6} />
          {/* the fan at the tail */}
          <g transform={`translate(560 -10) rotate(${spin})`}>
            <circle r={110} fill="#0C0E14" stroke={C.magenta} strokeWidth={8} />
            {Array.from({ length: 6 }).map((_, i) => (
              <path key={i} d="M 0 0 L 95 -18 L 95 18 Z" fill={C.magenta} transform={`rotate(${i * 60})`} opacity={0.8} />
            ))}
          </g>
        </g>
      </svg>
      <Headline at={cue("b2", "racing") - 6} left={M} top={110} lines={[{ text: "ONE RACE.", size: 120 }]} />
      <div style={{ position: "absolute", left: M, top: 260, ...HEADC, fontSize: 120, color: C.acid, opacity: lit, ...keyline(0.8, 10) }}>ONE WIN. THEN GONE.</div>
      <Sfx at={0} name="whoosh" volume={0.3} />
    </AbsoluteFill>
  );
};
