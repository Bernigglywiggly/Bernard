import { AbsoluteFill } from "remotion";
import { Background } from "../components/Background";
import { theme } from "../theme";

type ThumbnailProps = {
  readonly lines: string[];
  readonly chip: string;
  readonly accent: string;
};

// A still (one frame, no animation) for YouTube thumbnails: render with `npm run still`.
export const Thumbnail: React.FC<ThumbnailProps> = ({ lines, chip, accent }) => {
  return (
    <AbsoluteFill>
      <Background accent={accent} />
      <AbsoluteFill style={{ justifyContent: "center", padding: "0 70px" }}>
        {lines.map((line, i) => (
          <div
            key={i}
            style={{
              fontFamily: theme.fonts.display,
              fontSize: 104,
              lineHeight: 1.12,
              color: i === lines.length - 1 ? accent : theme.colors.ink,
              textShadow: "4px 4px 0 rgba(0, 0, 0, 0.85)",
            }}
          >
            {line}
          </div>
        ))}
      </AbsoluteFill>
      <div
        style={{
          position: "absolute",
          left: 70,
          bottom: 60,
          padding: "10px 20px",
          borderLeft: `5px solid ${accent}`,
          backgroundColor: "rgba(0, 0, 0, 0.55)",
          fontFamily: theme.fonts.mono,
          fontSize: 28,
          letterSpacing: "0.1em",
          color: accent,
        }}
      >
        {chip}
      </div>
    </AbsoluteFill>
  );
};
