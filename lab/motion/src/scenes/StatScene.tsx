import type React from "react";
import {
  AbsoluteFill,
  Interactive,
  type InteractivitySchema,
  useVideoConfig,
} from "remotion";
import { Background } from "../components/Background";
import { BarChart } from "../components/BarChart";
import { Chip } from "../components/Chip";
import { CountUp } from "../components/CountUp";
import { TypeOn } from "../components/TypeOn";
import { unitFor } from "../lib/anim";
import { theme } from "../theme";

type StatSceneProps = {
  readonly value: number;
  readonly suffix?: string;
  readonly label: string;
  readonly accent?: string;
  readonly style?: React.CSSProperties;
};

// A headline number counting up beside a bar chart (stacked on vertical formats).
const StatSceneInner: React.FC<StatSceneProps> = ({
  value,
  suffix = "",
  label,
  accent = theme.colors.accent,
  style,
}) => {
  const { width, height, fps } = useVideoConfig();
  const u = unitFor(width, height);
  const landscape = width >= height;

  return (
    <AbsoluteFill style={style}>
      <Background accent={accent} drift={-1} />
      <AbsoluteFill
        style={{
          flexDirection: landscape ? "row" : "column",
          justifyContent: "center",
          alignItems: "center",
          gap: (landscape ? 140 : 90) * u,
          padding: 100 * u,
        }}
      >
        <div style={{ display: "flex", flexDirection: "column", alignItems: landscape ? "flex-start" : "center", gap: 26 * u }}>
          <CountUp
            name="Number"
            to={value}
            suffix={suffix}
            premountFor={fps}
            style={{ fontSize: 230 * u, color: theme.colors.ink }}
          />
          <TypeOn name="Label" from={Math.round(0.6 * fps)} premountFor={fps} style={{ fontSize: 42 * u }}>
            {label}
          </TypeOn>
        </div>
        <BarChart
          name="Chart"
          from={Math.round(0.4 * fps)}
          values={[18, 34, 52, 77, 100]}
          labels={["MON", "TUE", "WED", "THU", "FRI"]}
          color={accent}
          height={460 * u}
          premountFor={fps}
        />
      </AbsoluteFill>
      <Chip
        name="Section"
        accent={accent}
        premountFor={fps}
        style={{ position: "absolute", left: 100 * u, top: 100 * u, fontSize: 30 * u }}
      >
        EXAMPLE · ANIMATED STATS · SAMPLE DATA
      </Chip>
    </AbsoluteFill>
  );
};

const statSceneSchema = {
  value: { type: "number", default: 1000, hiddenFromList: false, description: "Headline number" },
  suffix: { type: "text-content", default: "×", description: "Suffix" },
  label: { type: "text-content", default: "", description: "Label" },
  accent: { type: "color", default: theme.colors.accent, description: "Accent colour" },
} as const satisfies InteractivitySchema;

export const StatScene = Interactive.withSchema({
  Component: StatSceneInner,
  componentName: "<StatScene>",
  schema: statSceneSchema,
  wrapInSequence: true,
});
