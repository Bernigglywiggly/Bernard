import { evolvePath } from "@remotion/paths";
import { AbsoluteFill, useVideoConfig } from "remotion";
import { theme } from "../theme";

type DrawLineProps = {
  readonly d: string;
  readonly progress: number;
  readonly color?: string;
  readonly strokeWidth?: number;
};

// Draws an SVG path from its start to `progress` (0..1). `d` is in composition pixels.
export const DrawLine: React.FC<DrawLineProps> = ({
  d,
  progress,
  color = theme.colors.accent,
  strokeWidth = 4,
}) => {
  const { width, height } = useVideoConfig();
  const { strokeDasharray, strokeDashoffset } = evolvePath(progress, d);

  return (
    <AbsoluteFill>
      <svg width={width} height={height} viewBox={`0 0 ${width} ${height}`}>
        <path
          d={d}
          fill="none"
          stroke={color}
          strokeWidth={strokeWidth}
          strokeLinecap="round"
          strokeDasharray={strokeDasharray}
          strokeDashoffset={strokeDashoffset}
          style={{ filter: `drop-shadow(0 0 10px ${color})` }}
        />
      </svg>
    </AbsoluteFill>
  );
};
