import { loadFont } from "@remotion/fonts";
import { staticFile } from "remotion";

// The Curve v2 look (Oct 2026 style reboot): the thumbnails' palette and type carried into the films, so a viewer
// who clicks a colourful thumbnail lands in the same world. Source of truth for the thumbnail side:
// lab/tools/thumbs_v2.py ("curve" palette, Archivo 900).
loadFont({ family: "Archivo", url: staticFile("fonts/Archivo-var.ttf"), weight: "100 900" });

export const v2 = {
  colors: {
    cyan: "#3DFFF2",
    magenta: "#FF2BD6",
    acid: "#E6FF2E",
    warn: "#FF4A2A",
    ink: "#FFFFFF",
    black: "#000000",
    night: "#14052E",
  },
  fonts: {
    heavy: '"Archivo", sans-serif',
    mono: '"IBM Plex Mono", monospace',
  },
} as const;
