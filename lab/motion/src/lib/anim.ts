import { Easing, useVideoConfig } from "remotion";

// Clamp both ends; spread into interpolate() options.
export const CLAMP = {
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
} as const;

export const EASE_OUT = Easing.bezier(0.16, 1, 0.3, 1);
export const EASE_IN_OUT = Easing.bezier(0.65, 0, 0.35, 1);
export const SPRING = Easing.spring({ damping: 200 });

// Seconds to frames. Time everything in seconds so a new fps keeps the same pace.
export const sec = (seconds: number, fps: number) => Math.round(seconds * fps);

// 1 at 1920x1080 and 1080x1920, 2 at 4K: multiply pixel sizes by it.
export const unitFor = (width: number, height: number) =>
  Math.min(width, height) / 1080;

export const useUnit = () => {
  const { width, height } = useVideoConfig();
  return unitFor(width, height);
};
