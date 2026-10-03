import type React from "react";
import {
  AbsoluteFill,
  Interactive,
  type InteractivitySchema,
  useVideoConfig,
} from "remotion";
import { Background } from "../components/Background";
import { KineticTitle } from "../components/KineticTitle";
import { LowerThird } from "../components/LowerThird";
import { TypeOn } from "../components/TypeOn";
import { unitFor } from "../lib/anim";
import { theme } from "../theme";

type OutroSceneProps = {
  readonly title: string;
  readonly accent?: string;
  readonly style?: React.CSSProperties;
};

// End card: a closing headline, the commands typed out, and a lower third.
const OutroSceneInner: React.FC<OutroSceneProps> = ({
  title,
  accent = theme.colors.accent,
  style,
}) => {
  const { width, height, fps } = useVideoConfig();
  const u = unitFor(width, height);

  return (
    <AbsoluteFill style={style}>
      <Background accent={accent} drift={0.5} />
      <AbsoluteFill
        style={{
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          gap: 50 * u,
          padding: 100 * u,
        }}
      >
        <KineticTitle name="Title" accent={accent} accentWord={2} premountFor={fps} style={{ fontSize: 110 * u }}>
          {title}
        </KineticTitle>
        <TypeOn name="Commands" from={Math.round(0.8 * fps)} premountFor={fps} style={{ fontSize: 40 * u }}>
          npm run dev · npm run render:sample
        </TypeOn>
      </AbsoluteFill>
      <LowerThird
        name="Credit"
        from={Math.round(1.2 * fps)}
        detail="lab/motion · Remotion 4"
        accent={accent}
        premountFor={fps}
        style={{ left: 100 * u, bottom: 100 * u, scale: u, transformOrigin: "bottom left" }}
      >
        Motion Lab
      </LowerThird>
    </AbsoluteFill>
  );
};

const outroSceneSchema = {
  title: { type: "text-content", default: "", description: "Title" },
  accent: { type: "color", default: theme.colors.accent, description: "Accent colour" },
} as const satisfies InteractivitySchema;

export const OutroScene = Interactive.withSchema({
  Component: OutroSceneInner,
  componentName: "<OutroScene>",
  schema: outroSceneSchema,
  wrapInSequence: true,
});
