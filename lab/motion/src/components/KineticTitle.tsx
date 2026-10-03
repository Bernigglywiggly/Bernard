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

type KineticTitleProps = {
  readonly children: string;
  readonly accent?: string;
  readonly accentWord?: number;
  readonly stagger?: number;
  readonly style?: React.CSSProperties;
};

// A headline whose words rise out of a mask one after another.
const KineticTitleInner: React.FC<KineticTitleProps> = ({
  children,
  accent = theme.colors.accent,
  accentWord = -1,
  stagger = 4,
  style,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <div
      style={{
        display: "flex",
        flexWrap: "wrap",
        justifyContent: "center",
        columnGap: "0.3em",
        fontFamily: theme.fonts.display,
        fontSize: 120,
        lineHeight: 1.12,
        color: theme.colors.ink,
        textAlign: "center",
        ...style,
      }}
    >
      {children.split(" ").map((word, i) => {
        const start = i * stagger;
        const p = interpolate(frame, [start, start + 0.7 * fps], [0, 1], {
          ...CLAMP,
          easing: EASE_OUT,
        });
        return (
          <span
            key={i}
            style={{ display: "inline-block", overflow: "hidden", paddingBottom: "0.06em" }}
          >
            <span
              style={{
                display: "inline-block",
                translate: `0 ${(1 - p) * 105}%`,
                color: i === accentWord ? accent : undefined,
              }}
            >
              {word}
            </span>
          </span>
        );
      })}
    </div>
  );
};

const kineticTitleSchema = {
  children: { type: "text-content", default: "", description: "Title" },
  accent: { type: "color", default: theme.colors.accent, description: "Accent colour" },
  accentWord: {
    type: "number",
    hiddenFromList: false,
    default: -1,
    min: -1,
    step: 1,
    integer: true,
    description: "Word in the accent colour (-1: none)",
  },
  stagger: {
    type: "number",
    hiddenFromList: false,
    default: 4,
    min: 0,
    max: 30,
    step: 1,
    description: "Frames between words",
  },
  ...Interactive.textSchema,
} as const satisfies InteractivitySchema;

export const KineticTitle = Interactive.withSchema({
  Component: KineticTitleInner,
  componentName: "<KineticTitle>",
  schema: kineticTitleSchema,
  wrapInSequence: true,
});
