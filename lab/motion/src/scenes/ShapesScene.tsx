import { Circle, Rect, Star, Triangle } from "@remotion/shapes";
import type React from "react";
import {
  AbsoluteFill,
  interpolate,
  Interactive,
  type InteractivitySchema,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { Background } from "../components/Background";
import { Chip } from "../components/Chip";
import { PulseRing } from "../components/PulseRing";
import { CLAMP, SPRING, unitFor } from "../lib/anim";
import { useBass } from "../lib/audio";
import { theme } from "../theme";

type ShapesSceneProps = {
  readonly accent?: string;
  readonly style?: React.CSSProperties;
};

// Shapes spring in one by one and turn slowly; the star in the middle breathes with the music.
const ShapesSceneInner: React.FC<ShapesSceneProps> = ({ accent = theme.colors.accent, style }) => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();
  const u = unitFor(width, height);
  const bass = useBass();
  const landscape = width >= height;
  const pop = (i: number) =>
    interpolate(frame, [i * 5, i * 5 + 0.6 * fps], [0, 1], {
      ...CLAMP,
      easing: SPRING,
      output: "perceptual-scale",
    });
  const turn = (speed: number) => `${(frame / fps) * speed}deg`;
  const stroke = { fill: "none", stroke: accent, strokeWidth: 5 * u };

  return (
    <AbsoluteFill style={style}>
      <Background accent={accent} />
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
        <PulseRing size={520 * u} color={accent} />
        <Star
          name="Star"
          points={5}
          outerRadius={170 * u}
          innerRadius={(78 + bass * 34) * u}
          fill={accent}
          style={{ scale: pop(0), rotate: turn(24), filter: `drop-shadow(0 0 ${24 * u}px ${accent})` }}
        />
      </AbsoluteFill>
      <AbsoluteFill
        style={{
          flexDirection: landscape ? "row" : "column",
          justifyContent: "space-between",
          alignItems: "center",
          padding: landscape ? `0 ${150 * u}px` : `${260 * u}px 0`,
        }}
      >
        <div style={{ display: "flex", flexDirection: landscape ? "column" : "row", gap: 120 * u, alignItems: "center" }}>
          <Circle name="Circle" radius={70 * u} {...stroke} style={{ scale: pop(1) }} />
          <Rect name="Square" width={130 * u} height={130 * u} cornerRadius={18 * u} {...stroke} style={{ scale: pop(2), rotate: turn(-30) }} />
        </div>
        <div style={{ display: "flex", flexDirection: landscape ? "column" : "row", gap: 120 * u, alignItems: "center" }}>
          <Triangle name="Triangle" length={150 * u} direction="up" {...stroke} style={{ scale: pop(3), rotate: turn(40) }} />
          <Circle name="Dot" radius={26 * u} fill={theme.colors.gold} style={{ scale: pop(4) }} />
        </div>
      </AbsoluteFill>
      <Chip
        name="Section"
        accent={accent}
        premountFor={fps}
        style={{ position: "absolute", left: 100 * u, top: 100 * u, fontSize: 30 * u }}
      >
        SHAPES · PATHS · AUDIO-REACTIVE
      </Chip>
    </AbsoluteFill>
  );
};

const shapesSceneSchema = {
  accent: { type: "color", default: theme.colors.accent, description: "Accent colour" },
} as const satisfies InteractivitySchema;

export const ShapesScene = Interactive.withSchema({
  Component: ShapesSceneInner,
  componentName: "<ShapesScene>",
  schema: shapesSceneSchema,
  wrapInSequence: true,
});
