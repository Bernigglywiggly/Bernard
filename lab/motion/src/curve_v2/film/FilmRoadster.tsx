import { Audio } from "@remotion/media";
import type React from "react";
import { AbsoluteFill, interpolate, Sequence, Series, staticFile } from "remotion";
import { CLAMP } from "../../lib/anim";
import { C } from "../kit";
import { B1Bridge } from "./B1Bridge";
import { B2Bridge } from "./B2Bridge";
import { EndCard, END_FRAMES } from "./EndCard";
import { S1Hang } from "./S1Hang";
import { S2Jets } from "./S2Jets";
import { S3Launch } from "./S3Launch";
import { S4Seconds } from "./S4Seconds";
import { S5FanCar } from "./S5FanCar";
import { S6Legal } from "./S6Legal";
import { S7Deposit } from "./S7Deposit";
import { S8Verdict } from "./S8Verdict";
import { LEAD, segFrames } from "./util";
import { VO_SECONDS } from "./words";

// "How the Flying Tesla Roadster Actually Works" (The Curve, long form, 1920x1080, 30 fps). Script:
// lab/curve_v2/film_roadster/script.py (v2 pickups 25 Oct 2026); facts: TESLA_ROADSTER_FACTS.md.
// v2 (critic round 1): S9 "the bill" is cut, the narration is lab/curve_v2/film_roadster/vo/v2 (vo_v2.py), and the end
// card speaks a pointer to the Roadster Shorts. Each segment still opens on its own hook and closes on its own payoff.
export const FILM_ORDER: [string, React.FC][] = [
  ["S1", S1Hang], ["S2", S2Jets], ["S3", S3Launch], ["b1", B1Bridge], ["S4", S4Seconds], ["b2", B2Bridge],
  ["S5", S5FanCar], ["S6", S6Legal], ["S7", S7Deposit], ["S8", S8Verdict],
];
export const FILM_FRAMES = FILM_ORDER.reduce((a, [s]) => a + segFrames(s), 0) + END_FRAMES;
const END_AT = FILM_FRAMES - END_FRAMES;
const END_VO_DONE = END_AT + LEAD + Math.ceil(VO_SECONDS.END * 30);

export const FilmRoadster: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: C.black }}>
    <Series>
      {FILM_ORDER.map(([seg, Comp]) => (
        <Series.Sequence key={seg} durationInFrames={segFrames(seg)} premountFor={30}>
          <Comp />
          <Sequence from={LEAD}><Audio src={staticFile(`film/v2/vo_${seg}.mp3`)} /></Sequence>
        </Series.Sequence>
      ))}
      <Series.Sequence durationInFrames={END_FRAMES}>
        <EndCard />
        <Sequence from={LEAD}><Audio src={staticFile("film/v2/vo_END.mp3")} /></Sequence>
      </Series.Sequence>
    </Series>
    {/* one bed under the whole film, ducked under the narration (the end card's pointer included), up a little after it */}
    <Audio src={staticFile("audio/sample-bed.mp3")} loop
      volume={(f) => interpolate(f, [0, 15, END_VO_DONE, END_VO_DONE + 15, FILM_FRAMES - 30, FILM_FRAMES], [0, 0.09, 0.09, 0.2, 0.2, 0], CLAMP)} />
  </AbsoluteFill>
);
