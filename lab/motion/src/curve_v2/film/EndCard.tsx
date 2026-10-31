import type React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { CLAMP } from "../../lib/anim";
import { BG_NIGHT, C, HEADC, keyline, MONO } from "../kit";

// End card, 8 s (critic round 1: 12 s with no next video was too long). The channel mark (the same rising curve as
// the banner and avatar, Brand.tsx) and name on the left; the right half stays empty for YouTube's end-screen
// elements (a video and subscribe). A spoken pointer (END in words.ts) sends viewers to the Roadster Shorts.
export const END_FRAMES = 240;

const Mark: React.FC<{ size: number; stroke: number }> = ({ size, stroke }) => (
  <svg width={size} height={size} viewBox="0 0 100 100">
    <defs>
      <linearGradient id="endCurveGrad" x1="0" y1="1" x2="1" y2="0">
        <stop offset="0%" stopColor={C.magenta} />
        <stop offset="100%" stopColor={C.cyan} />
      </linearGradient>
    </defs>
    <path d="M 14 80 C 44 80, 66 66, 78 24" fill="none" stroke="#000" strokeWidth={stroke + 6} strokeLinecap="round" />
    <path d="M 14 80 C 44 80, 66 66, 78 24" fill="none" stroke="url(#endCurveGrad)" strokeWidth={stroke} strokeLinecap="round" />
    <circle cx={78} cy={22} r={stroke * 0.95} fill={C.acid} stroke="#000" strokeWidth={3} />
  </svg>
);

export const EndCard: React.FC = () => {
  const frame = useCurrentFrame();
  const k = interpolate(frame, [0, 18], [0, 1], CLAMP);
  const ptr = interpolate(frame, [40, 58], [0, 1], CLAMP);
  return (
    <AbsoluteFill style={{ background: BG_NIGHT }}>
      <div style={{ position: "absolute", left: 120, top: 250, width: 800, opacity: k, translate: `${(1 - k) * -40}px 0` }}>
        <Mark size={200} stroke={11} />
        <div style={{ ...HEADC, fontSize: 150, color: C.ink, marginTop: 10, ...keyline(1, 10) }}>THE CURVE</div>
        <div style={{ ...HEADC, fontVariationSettings: "'wdth' 88", whiteSpace: "normal", fontSize: 54, lineHeight: 1.05, color: C.acid, marginTop: 12,
          ...keyline(0.4, 8) }}>THE STORY BEHIND THE CLIP EVERYONE&apos;S SHARING</div>
        <div style={{ ...MONO, fontSize: 38, color: "#B9B2CC", marginTop: 30 }}>SOURCES FOR EVERY NUMBER ARE IN THE DESCRIPTION</div>
        <div style={{ ...HEADC, fontSize: 64, color: C.cyan, marginTop: 44, opacity: ptr, translate: `${(1 - ptr) * -30}px 0`, ...keyline(0.45, 8) }}>
          THE ROADSTER SHORTS →
        </div>
      </div>
    </AbsoluteFill>
  );
};
