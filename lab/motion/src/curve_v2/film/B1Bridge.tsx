import type React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { CLAMP } from "../../lib/anim";
import { C, Headline, Sfx } from "../kit";
import { Disclose, HoldStill, M, Shade } from "./fx";
import { cue, segFrames } from "./util";

// Bridge 1: "In a moment, the number that decides how long this car can actually fly." Over our x-ray of the tanks,
// a gauge needle sinks towards empty.
const D = segFrames("b1");

export const B1Bridge: React.FC = () => {
  const frame = useCurrentFrame();
  const needle = interpolate(frame, [cue("b1", "number"), D - 10], [70, -60], CLAMP);
  return (
    <AbsoluteFill style={{ backgroundColor: C.black }}>
      <HoldStill src="film/blender_xray_last.png" from={0} dur={D} push={[1.06, 1.12]} origin="60% 50%" />
      <Shade from="left" strength={0.85} />
      <Headline at={cue("b1", "how") - 6} left={M} top={300} lines={[{ text: "HOW LONG CAN IT", size: 140 }, { text: "ACTUALLY FLY?", size: 140, color: C.acid }]} />
      <svg width={1920} height={1080} style={{ position: "absolute", inset: 0 }}>
        <g transform="translate(1500 760)">
          <path d="M -200 0 A 200 200 0 0 1 200 0" fill="none" stroke="#59606E" strokeWidth={26} />
          <path d="M -200 0 A 200 200 0 0 1 -141 -141" fill="none" stroke={C.warn} strokeWidth={26} />
          <line x1={0} y1={0} x2={Math.sin((needle * Math.PI) / 180) * 170} y2={-Math.cos((needle * Math.PI) / 180) * 170} stroke={C.acid} strokeWidth={14} strokeLinecap="round" />
          <circle r={20} fill={C.acid} stroke="#000" strokeWidth={5} />
        </g>
      </svg>
      <Disclose show={[[0, D]]} />
      <Sfx at={0} name="riser" volume={0.3} />
    </AbsoluteFill>
  );
};
