import type React from "react";
import { AbsoluteFill } from "remotion";
import { BG_NIGHT, C, HEADC, keyline } from "../kit";

// Roadster film, segment S2 ("The jets"). PLACEHOLDER: replace with the real scene. Timeline is segment-relative:
// frame 0 = LEAD frames before the first word (see util.ts); cue("S2", "word") gives a word's frame.
export const S2Jets: React.FC = () => (
  <AbsoluteFill style={{ background: BG_NIGHT, alignItems: "center", justifyContent: "center" }}>
    <div style={{ ...HEADC, fontSize: 120, color: C.ink, ...keyline(0.8, 10) }}>S2 · THE JETS</div>
  </AbsoluteFill>
);
