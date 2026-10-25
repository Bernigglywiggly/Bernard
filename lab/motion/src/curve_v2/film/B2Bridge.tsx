import type React from "react";
import { AbsoluteFill } from "remotion";
import { C, ClipScene, Stamp } from "../kit";
import { M, Sfx, Shade, TeslaCredit } from "./fx";
import { cue, segFrames } from "./util";

// Bridge 2 (v2, re-aimed two segments ahead at S6): "Later on, whether this car counts as an aircraft, and who that
// leaves in charge of it." Tesla's head-on lift over the lineup (unused in v1; RIFE 1.3x slower, prep_v2_clips.sh),
// pushed in so the car reads, under the question S6 answers. Facts: S4 (FAA: not an aircraft), §13.3.
const D = segFrames("b2");

export const B2Bridge: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: C.black }}>
    <ClipScene src="film/kick_headon_slow.mp4" from={0} dur={D} push={[1.5, 1.62]} origin="52% 30%" />
    <Shade from="bottom" strength={0.7} />
    <Stamp at={cue("b2", "aircraft") - 2} left={M} top={620} color={C.magenta} size={130} rot={-6}>AIRCRAFT?</Stamp>
    <Stamp at={cue("b2", "who") - 2} left={1050} top={680} color={C.cyan} size={130} rot={4}>OR CAR?</Stamp>
    <TeslaCredit show={[[0, D]]} />
    <Sfx at={0} name="whoosh" volume={0.3} />
    <Sfx at={cue("b2", "aircraft") - 2} name="thock" volume={0.55} />
    <Sfx at={cue("b2", "who") - 2} name="thock" volume={0.5} />
  </AbsoluteFill>
);
