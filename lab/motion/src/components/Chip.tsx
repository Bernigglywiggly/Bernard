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

type ChipProps = {
  readonly children: string;
  readonly accent?: string;
  readonly style?: React.CSSProperties;
};

// A small mono label with an accent bar; the bar draws down, then the label slides in.
const ChipInner: React.FC<ChipProps> = ({ children, accent = theme.colors.accent, style }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const bar = interpolate(frame, [0, 0.35 * fps], [0, 1], { ...CLAMP, easing: EASE_OUT });
  const text = interpolate(frame, [0.15 * fps, 0.6 * fps], [0, 1], {
    ...CLAMP,
    easing: EASE_OUT,
  });

  return (
    <div
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: 18,
        padding: "12px 22px 12px 0",
        backgroundColor: "rgba(0, 0, 0, 0.55)",
        fontFamily: theme.fonts.mono,
        fontSize: 30,
        letterSpacing: "0.12em",
        color: accent,
        ...style,
      }}
    >
      <div style={{ width: 5, alignSelf: "stretch", backgroundColor: accent, scale: `1 ${bar}` }} />
      <span style={{ opacity: text, translate: `${(1 - text) * -16}px 0` }}>{children}</span>
    </div>
  );
};

const chipSchema = {
  children: { type: "text-content", default: "", description: "Label" },
  accent: { type: "color", default: theme.colors.accent, description: "Accent colour" },
} as const satisfies InteractivitySchema;

export const Chip = Interactive.withSchema({
  Component: ChipInner,
  componentName: "<Chip>",
  schema: chipSchema,
  wrapInSequence: true,
});
