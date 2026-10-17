import type React from "react";
import {
  interpolate,
  Interactive,
  type InteractivitySchema,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { CLAMP, EASE_OUT } from "../lib/anim";
import { theme } from "../theme";

type LowerThirdProps = {
  readonly children: string;
  readonly detail?: string;
  readonly accent?: string;
  readonly style?: React.CSSProperties;
};

// Name-and-detail card: a panel wipes open from the left, then the two lines arrive.
const LowerThirdInner: React.FC<LowerThirdProps> = ({
  children,
  detail = "",
  accent = theme.colors.accent,
  style,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const open = interpolate(frame, [0, 0.5 * fps], [0, 100], { ...CLAMP, easing: EASE_OUT });
  const line1 = interpolate(frame, [0.25 * fps, 0.75 * fps], [0, 1], { ...CLAMP, easing: EASE_OUT });
  const line2 = interpolate(frame, [0.4 * fps, 0.9 * fps], [0, 1], { ...CLAMP, easing: EASE_OUT });

  return (
    <div
      style={{
        position: "absolute",
        left: 120,
        bottom: 120,
        padding: "26px 40px 26px 34px",
        borderLeft: `6px solid ${accent}`,
        backgroundColor: "rgba(5, 8, 10, 0.82)",
        clipPath: `inset(0 ${100 - open}% 0 0)`,
        ...style,
      }}
    >
      <div
        style={{
          fontFamily: theme.fonts.body,
          fontWeight: 600,
          fontSize: 52,
          color: theme.colors.ink,
          opacity: line1,
          translate: `${(1 - line1) * 30}px 0`,
        }}
      >
        {children}
      </div>
      <div
        style={{
          marginTop: 8,
          fontFamily: theme.fonts.mono,
          fontSize: 28,
          letterSpacing: "0.08em",
          color: theme.colors.gold,
          opacity: line2,
          translate: `${(1 - line2) * 30}px 0`,
        }}
      >
        {detail}
      </div>
    </div>
  );
};

const lowerThirdSchema = {
  children: { type: "text-content", default: "", description: "Name" },
  detail: { type: "text-content", default: "", description: "Detail" },
  accent: { type: "color", default: theme.colors.accent, description: "Accent colour" },
} as const satisfies InteractivitySchema;

export const LowerThird = Interactive.withSchema({
  Component: LowerThirdInner,
  componentName: "<LowerThird>",
  schema: lowerThirdSchema,
  wrapInSequence: true,
});
