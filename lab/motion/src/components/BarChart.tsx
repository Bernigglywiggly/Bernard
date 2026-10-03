import type React from "react";
import {
  interpolate,
  Interactive,
  type InteractivitySchema,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { CLAMP, EASE_OUT, useUnit } from "../lib/anim";
import { theme } from "../theme";

type BarChartProps = {
  readonly values: readonly number[];
  readonly labels?: readonly string[];
  readonly color?: string;
  readonly stagger?: number;
  readonly height?: number;
  readonly style?: React.CSSProperties;
};

// Bars that grow from the baseline one after another, each with its value on top.
const BarChartInner: React.FC<BarChartProps> = ({
  values,
  labels = [],
  color = theme.colors.accent,
  stagger = 5,
  height = 420,
  style,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const u = useUnit();
  const max = Math.max(...values, 1);

  return (
    <div
      style={{
        display: "flex",
        alignItems: "flex-end",
        gap: 28 * u,
        height,
        fontFamily: theme.fonts.mono,
        ...style,
      }}
    >
      {values.map((v, i) => {
        const p = interpolate(frame, [i * stagger, i * stagger + 0.8 * fps], [0, 1], {
          ...CLAMP,
          easing: EASE_OUT,
        });
        return (
          <div
            key={i}
            style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 14 * u }}
          >
            <div style={{ fontSize: 34 * u, color: theme.colors.ink, opacity: p }}>
              {Math.round(v * p)}
            </div>
            <div
              style={{
                width: 84 * u,
                height: (v / max) * (height - 120 * u) * p,
                borderRadius: `${10 * u}px ${10 * u}px ${2 * u}px ${2 * u}px`,
                background: `linear-gradient(180deg, ${color}, color-mix(in srgb, ${color} 35%, transparent))`,
                boxShadow: `0 0 30px color-mix(in srgb, ${color} 35%, transparent)`,
              }}
            />
            <div style={{ fontSize: 28 * u, color: theme.colors.gold, letterSpacing: "0.1em", opacity: p }}>
              {labels[i] ?? ""}
            </div>
          </div>
        );
      })}
    </div>
  );
};

const barChartSchema = {
  values: {
    type: "array",
    item: { type: "number", min: 0, step: 1 },
    default: [30, 55, 80, 100],
    newItemDefault: 50,
    description: "Values",
  },
  color: { type: "color", default: theme.colors.accent, description: "Bar colour" },
  stagger: {
    type: "number",
    hiddenFromList: false,
    default: 5,
    min: 0,
    max: 30,
    step: 1,
    description: "Frames between bars",
  },
} as const satisfies InteractivitySchema;

export const BarChart = Interactive.withSchema({
  Component: BarChartInner,
  componentName: "<BarChart>",
  schema: barChartSchema,
  wrapInSequence: true,
});
