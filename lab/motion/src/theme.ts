import { loadFont } from "@remotion/fonts";
import { staticFile } from "remotion";

// The Curve's house fonts, loaded from public/fonts (no network needed to render). loadFont() holds the render
// until each file is ready. To add a font: drop the file in public/fonts and add a line here.
const FONTS = [
  { family: "Michroma", file: "fonts/Michroma-400.ttf", weight: "400" },
  { family: "Inter Tight", file: "fonts/InterTight-400.ttf", weight: "400" },
  { family: "Inter Tight", file: "fonts/InterTight-600.ttf", weight: "600" },
  { family: "IBM Plex Mono", file: "fonts/IBMPlexMono-400.ttf", weight: "400" },
  { family: "IBM Plex Mono", file: "fonts/IBMPlexMono-500.ttf", weight: "500" },
];

for (const font of FONTS) {
  loadFont({ family: font.family, url: staticFile(font.file), weight: font.weight });
}

// The Curve's house look: black, turquoise accent, gold labels.
export const theme = {
  colors: {
    bg: "#05080A",
    ink: "#FFFFFF",
    soft: "#9FB3B8",
    accent: "#3FE6D8",
    gold: "#F2D9A0",
    grid: "rgba(63, 230, 216, 0.09)",
  },
  fonts: {
    display: '"Michroma", sans-serif',
    body: '"Inter Tight", sans-serif',
    mono: '"IBM Plex Mono", monospace',
  },
} as const;
