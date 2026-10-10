import type React from "react";
import {
  AbsoluteFill,
  Composition,
  Easing,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { Background } from "../components/Background";
import { KineticTitle } from "../components/KineticTitle";
import { unitFor } from "../lib/anim";
import { theme } from "../theme";

type __NAME__Props = {
  readonly title: string;
};

export const __NAME__: React.FC<__NAME__Props> = ({ title }) => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();
  const u = unitFor(width, height);

  return (
    <AbsoluteFill>
      <Background />
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", padding: 100 * u }}>
        <KineticTitle
          name="Title"
          premountFor={fps}
          style={{
            fontSize: 120 * u,
            opacity: interpolate(frame, [0, 0.5 * fps], [0, 1], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
              easing: Easing.bezier(0.16, 1, 0.3, 1),
            }),
          }}
        >
          {title}
        </KineticTitle>
      </AbsoluteFill>
      <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center", paddingBottom: 100 * u }}>
        <div style={{ fontFamily: theme.fonts.mono, fontSize: 30 * u, color: theme.colors.gold }}>
          src/compositions/__NAME__.tsx
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

export const __NAME__Composition: React.FC = () => (
  <Composition
    id="__NAME__"
    component={__NAME__}
    width={__WIDTH__}
    height={__HEIGHT__}
    fps={__FPS__}
    durationInFrames={__FRAMES__}
    defaultProps={{ title: "__TITLE__" }}
  />
);
