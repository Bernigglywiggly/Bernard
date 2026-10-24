import type React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { CLAMP } from "../../lib/anim";
import { BG_NIGHT, C, HEADC, keyline, MONO } from "../kit";

// End card: 12 s for YouTube's end-screen elements (subscribe + two videos). Keep the centre-right clear for them.
export const END_FRAMES = 360;

export const EndCard: React.FC = () => {
  const frame = useCurrentFrame();
  const k = interpolate(frame, [0, 18], [0, 1], CLAMP);
  return (
    <AbsoluteFill style={{ background: BG_NIGHT }}>
      <div style={{ position: "absolute", left: 120, top: 380, opacity: k, translate: `${(1 - k) * -40}px 0` }}>
        <div style={{ ...HEADC, fontSize: 150, color: C.ink, ...keyline(1, 10) }}>THE CURVE</div>
        <div style={{ ...HEADC, fontVariationSettings: "'wdth' 88", fontSize: 54, color: C.acid, marginTop: 12, ...keyline(0.4, 8) }}>
          THE STORY BEHIND THE CLIP EVERYONE&apos;S SHARING
        </div>
        <div style={{ ...MONO, fontSize: 34, color: "#B9B2CC", marginTop: 30 }}>SOURCES FOR EVERY NUMBER ARE IN THE DESCRIPTION</div>
      </div>
    </AbsoluteFill>
  );
};
