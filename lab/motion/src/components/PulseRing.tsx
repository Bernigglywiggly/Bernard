import { useBass } from "../lib/audio";
import { theme } from "../theme";

type PulseRingProps = {
  readonly size: number;
  readonly color?: string;
};

// A ring that swells with the bass of the music (see AudioLevelProvider).
export const PulseRing: React.FC<PulseRingProps> = ({ size, color = theme.colors.accent }) => {
  const bass = useBass();

  return (
    <div
      style={{
        position: "absolute",
        width: size,
        height: size,
        borderRadius: "50%",
        border: `${Math.max(2, size / 90)}px solid ${color}`,
        scale: 1 + bass * 0.22,
        opacity: 0.25 + bass * 0.75,
        boxShadow: `0 0 ${20 + bass * 60}px color-mix(in srgb, ${color} 60%, transparent), inset 0 0 ${10 + bass * 40}px color-mix(in srgb, ${color} 40%, transparent)`,
      }}
    />
  );
};
