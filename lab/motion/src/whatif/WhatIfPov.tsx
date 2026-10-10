import { Audio, Video } from "@remotion/media";
import {
  AbsoluteFill,
  interpolate,
  Series,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { CLAMP, EASE_OUT, unitFor } from "../lib/anim";
import { theme } from "../theme";
import { FILMS } from "./films";

type WhatIfPovProps = {
  readonly film: string;
};

const INK = "#F4EFE6";
const SHADOW = "0 2px 18px rgba(0, 0, 0, 0.9), 0 0 4px rgba(0, 0, 0, 0.7)";

// The "What if" POV layout: one continuous first-person shot built from chained clips, a live readout top left,
// the question as a title, then one short italic line per beat. Each film's data lives in src/whatif/<film>.ts.
export const WhatIfPov: React.FC<WhatIfPovProps> = ({ film }) => {
  const f = FILMS[film];
  const frame = useCurrentFrame();
  const { fps, width, height, durationInFrames } = useVideoConfig();
  const t = frame / fps;
  const u = unitFor(width, height);
  const clipFrames = Math.round(f.clipSeconds * fps);
  const r = f.readout(t);
  const end = durationInFrames / fps;

  return (
    <AbsoluteFill style={{ backgroundColor: "black" }}>
      <AbsoluteFill style={{ scale: interpolate(frame, [0, durationInFrames], [1, 1.06]) }}>
        <Series>
          {f.clips.map((src) => (
            <Series.Sequence key={src} durationInFrames={clipFrames} premountFor={fps}>
              <Video src={staticFile(src)} muted objectFit="cover" style={{ width: "100%", height: "100%" }} />
            </Series.Sequence>
          ))}
        </Series>
      </AbsoluteFill>
      <AbsoluteFill
        style={{ background: "radial-gradient(ellipse at center, transparent 55%, rgba(0, 0, 0, 0.5) 100%)" }}
      />
      <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(0, 0, 0, 0.5) 0%, transparent 24%)" }} />

      <div
        style={{
          position: "absolute",
          left: 80 * u,
          top: 170 * u,
          opacity: r.opacity,
          color: INK,
          textShadow: SHADOW,
        }}
      >
        <div style={{ fontFamily: theme.fonts.mono, fontSize: 27 * u, letterSpacing: "0.22em", opacity: 0.8 }}>
          {r.label}
        </div>
        <div
          style={{
            fontFamily: theme.fonts.serif,
            fontWeight: 500,
            fontSize: 74 * u,
            lineHeight: 1.15,
            fontVariantNumeric: "tabular-nums",
          }}
        >
          {r.value}
        </div>
        <div style={{ fontFamily: theme.fonts.mono, fontSize: 28 * u, letterSpacing: "0.12em", opacity: 0.85 }}>
          {r.sub}
        </div>
      </div>

      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", padding: `0 ${110 * u}px` }}>
        <div
          style={{
            marginTop: -260 * u,
            fontFamily: theme.fonts.serif,
            fontStyle: "italic",
            fontSize: 80 * u,
            lineHeight: 1.18,
            textAlign: "center",
            color: INK,
            textShadow: SHADOW,
            opacity: interpolate(t, [0.3, 1.1, 4.2, 5.0], [0, 1, 1, 0], CLAMP),
            translate: `0 ${interpolate(t, [0.3, 1.4], [18 * u, 0], { ...CLAMP, easing: EASE_OUT })}px`,
          }}
        >
          {f.title}
        </div>
      </AbsoluteFill>

      {f.captions.map((c) => (
        <div
          key={c.text}
          style={{
            position: "absolute",
            left: 110 * u,
            right: 110 * u,
            top: height * 0.665,
            padding: `${18 * u}px ${24 * u}px`,
            background: "radial-gradient(closest-side, rgba(0, 0, 0, 0.55), rgba(0, 0, 0, 0))",
            fontFamily: theme.fonts.serif,
            fontStyle: "italic",
            fontSize: 54 * u,
            lineHeight: 1.25,
            textAlign: "center",
            color: INK,
            textShadow: SHADOW,
            opacity: interpolate(t, [c.from, c.from + 0.5, c.to - 0.5, c.to], [0, 1, 1, 0], CLAMP),
            translate: `0 ${interpolate(t, [c.from, c.from + 0.8], [14 * u, 0], { ...CLAMP, easing: EASE_OUT })}px`,
          }}
        >
          {c.text}
        </div>
      ))}

      <AbsoluteFill
        style={{ backgroundColor: "black", opacity: interpolate(t, [end - 1.6, end - 0.1], [0, 1], CLAMP) }}
      />
      <Audio name="Sound" src={staticFile(f.sound)} />
    </AbsoluteFill>
  );
};
