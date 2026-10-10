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

type CountUpProps = {
  readonly to: number;
  readonly decimals?: number;
  readonly prefix?: string;
  readonly suffix?: string;
  readonly seconds?: number;
  readonly style?: React.CSSProperties;
};

// A number that counts up and settles. Tabular figures keep it from jittering sideways.
const CountUpInner: React.FC<CountUpProps> = ({
  to,
  decimals = 0,
  prefix = "",
  suffix = "",
  seconds = 1.4,
  style,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const value =
    to *
    interpolate(frame, [0, seconds * fps], [0, 1], { ...CLAMP, easing: EASE_OUT });

  return (
    <div
      style={{
        fontFamily: theme.fonts.display,
        fontSize: 240,
        lineHeight: 1,
        color: theme.colors.ink,
        fontVariantNumeric: "tabular-nums",
        ...style,
      }}
    >
      {prefix}
      {value.toLocaleString("en-US", {
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals,
      })}
      {suffix}
    </div>
  );
};

const countUpSchema = {
  to: { type: "number", default: 100, hiddenFromList: false, description: "Final value" },
  decimals: {
    type: "number",
    hiddenFromList: false,
    default: 0,
    min: 0,
    max: 4,
    step: 1,
    integer: true,
    description: "Decimals",
  },
  prefix: { type: "text-content", default: "", description: "Prefix" },
  suffix: { type: "text-content", default: "", description: "Suffix" },
  seconds: {
    type: "number",
    hiddenFromList: false,
    default: 1.4,
    min: 0.1,
    max: 10,
    step: 0.1,
    description: "Count duration (s)",
  },
  ...Interactive.textSchema,
} as const satisfies InteractivitySchema;

export const CountUp = Interactive.withSchema({
  Component: CountUpInner,
  componentName: "<CountUp>",
  schema: countUpSchema,
  wrapInSequence: true,
});
