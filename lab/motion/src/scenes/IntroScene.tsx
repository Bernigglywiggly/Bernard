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
import { DrawLine } from "../components/DrawLine";
import { KineticTitle } from "../components/KineticTitle";
import { TypeOn } from "../components/TypeOn";
import { CLAMP, EASE_OUT, unitFor } from "../lib/anim";
import { theme } from "../theme";

type IntroSceneProps = {
  readonly title: string;
  readonly subtitle: string;
  readonly accent?: string;
  readonly style?: React.CSSProperties;
};

// Title card: the format chip, a headline rising word by word, a line drawing under it, a typed subtitle.
const IntroSceneInner: React.FC<IntroSceneProps> = ({
  title,
  subtitle,
  accent = theme.colors.accent,
  style,
}) => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();
  const u = unitFor(width, height);
  const lineY = height / 2 + (width >= height ? 120 : 210) * u;

  return (
    <AbsoluteFill style={style}>
      <Background accent={accent} />
      <DrawLine
        d={`M ${width * 0.18} ${lineY} L ${width * 0.82} ${lineY}`}
        progress={interpolate(frame, [0.3 * fps, 1.3 * fps], [0, 1], { ...CLAMP, easing: EASE_OUT })}
        color={accent}
        strokeWidth={4 * u}
      />
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", padding: 100 * u }}>
        <KineticTitle
          name="Title"
          accent={accent}
          accentWord={1}
          premountFor={fps}
          style={{ fontSize: 130 * u, translate: `0 ${-40 * u}px` }}
        >
          {title}
        </KineticTitle>
      </AbsoluteFill>
      <AbsoluteFill style={{ alignItems: "center", top: lineY + 46 * u }}>
        <TypeOn name="Subtitle" from={Math.round(0.9 * fps)} premountFor={fps} style={{ fontSize: 44 * u }}>
          {subtitle}
        </TypeOn>
      </AbsoluteFill>
      <Chip
        name="Format"
        from={Math.round(0.2 * fps)}
        accent={accent}
        premountFor={fps}
        style={{ position: "absolute", left: 100 * u, top: 100 * u, fontSize: 30 * u }}
      >
        {`${width} × ${height} · ${fps} FPS`}
      </Chip>
    </AbsoluteFill>
  );
};

const introSceneSchema = {
  title: { type: "text-content", default: "", description: "Title" },
  subtitle: { type: "text-content", default: "", description: "Subtitle" },
  accent: { type: "color", default: theme.colors.accent, description: "Accent colour" },
} as const satisfies InteractivitySchema;

export const IntroScene = Interactive.withSchema({
  Component: IntroSceneInner,
  componentName: "<IntroScene>",
  schema: introSceneSchema,
  wrapInSequence: true,
});
