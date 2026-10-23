import type React from "react";
import { AbsoluteFill } from "remotion";
import { BG_NIGHT, C, HEADC, keyline } from "../kit";

// Roadster film, segment S5 ("The fan car"). PLACEHOLDER: replace with the real scene. Timeline is segment-relative:
// frame 0 = LEAD frames before the first word (see util.ts); cue("S5", "word") gives a word's frame.
export const S5FanCar: React.FC = () => (
  <AbsoluteFill style={{ background: BG_NIGHT, alignItems: "center", justifyContent: "center" }}>
    <div style={{ ...HEADC, fontSize: 120, color: C.ink, ...keyline(0.8, 10) }}>S5 · THE FAN CAR</div>
  </AbsoluteFill>
);
