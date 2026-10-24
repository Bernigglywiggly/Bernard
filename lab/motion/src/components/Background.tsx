import { noise2D } from "@remotion/noise";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { theme } from "../theme";

type BackgroundProps = {
  readonly accent?: string;
  readonly drift?: number;
};

// Drifting grid, a slow glow that wanders on noise, and a vignette. Sits behind every scene.
export const Background: React.FC<BackgroundProps> = ({
  accent = theme.colors.accent,
  drift = 1,
}) => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();
  const t = frame / fps;
  const cell = Math.round(Math.min(width, height) / 12);
  const glowX = width / 2 + noise2D("glow-x", t * 0.12 * drift, 0) * width * 0.3;
  const glowY = height / 2 + noise2D("glow-y", 0, t * 0.12 * drift) * height * 0.3;
  const mask = "radial-gradient(ellipse at center, black 25%, transparent 75%)";

  return (
    <AbsoluteFill style={{ backgroundColor: theme.colors.bg }}>
      <AbsoluteFill
        style={{
          backgroundImage: `linear-gradient(${theme.colors.grid} 1px, transparent 1px), linear-gradient(90deg, ${theme.colors.grid} 1px, transparent 1px)`,
          backgroundSize: `${cell}px ${cell}px`,
          backgroundPosition: `${(t * 18 * drift) % cell}px ${(t * 10 * drift) % cell}px`,
          maskImage: mask,
          WebkitMaskImage: mask,
        }}
      />
      <AbsoluteFill
        style={{
          background: `radial-gradient(circle at ${glowX}px ${glowY}px, color-mix(in srgb, ${accent} 22%, transparent) 0%, transparent ${Math.max(width, height) * 0.42}px)`,
        }}
      />
      <AbsoluteFill
        style={{
          background:
            "radial-gradient(ellipse at center, transparent 50%, rgba(0, 0, 0, 0.7) 100%)",
        }}
      />
    </AbsoluteFill>
  );
};
