import { Audio } from "@remotion/media";
import { evolvePath } from "@remotion/paths";
import type React from "react";
import { AbsoluteFill, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { CLAMP, EASE_OUT } from "../lib/anim";
import { C, CaptionTrack, ClipScene, Credit, HEADC, keyline, MONO, pop, Sfx, Stamp, Tag } from "./kit";
import { makePages } from "./pager";
import { TRIPOD_TRACK, WRONG_TRACK } from "./s7Tracks";
import { VO_S7 } from "./voS7Captions";

// Curve Short 7 v2 (for Sun 25 Oct 2026): "How Did This Robot Duck Learn to Get Back Up? (Microduck)". 1080x1920, 30 fps.
// v2 applies critic round 1 (lab/curve_v2/shorts/out/critic_s7/round1.md): frame 0 is the duck flat on the floor with a
// question; the get-up reward is the end pose (fact 14); the simulator is ~50 visibly different ducks toppling and
// resetting (no counter, not Short 4's grid); the five wrong bodies are one continuous Blender take whose changes land on
// the spoken words and stay; the ending is Pollen's real shove, playing forward into frame 0, so the Short loops without
// a rewind. One text layer at a time. Our 3D duck: lab/curve_v2/shorts/blender/s7_duck.py (Pollen's meshes are never
// shown). Facts: lab/research/MICRODUCK_FACTS.md. Footage: Pollen Robotics, YouTube, 27 Aug 2026 (RAtzEyGBGFU,
// szW7N_7B3tU), RIFE to 30 fps. Narration s7_chris_v2_tight.mp3 (31.6 s).

export const SHORT7_FRAMES = 1005;

const F = { slowmo: 58, split: 116, crowd: 262, tripod: 414, wrong: 552, end: 803, hold0: 978 };
// wrong-body changes, in Short frames (Blender cue frame - 1 + F.wrong): heavier, off balance, slippery, low battery, shoved
const W = { heavy: 653, off: 674, slip: 703, batt: 728, shove: 760, hit: 766 };
const PAGES = makePages(VO_S7);
const DARKEN: React.CSSProperties = { position: "absolute", left: 0, right: 0, top: 0, height: 900,
  background: "linear-gradient(180deg, rgba(1,4,14,0.86) 0%, rgba(1,4,14,0.55) 62%, rgba(1,4,14,0) 100%)" };
const DISCLOSE: React.CSSProperties = { position: "absolute", left: 64, top: 140, ...MONO, fontSize: 44, color: "#D2D9E4" };
const between = (frame: number, a: number, b: number) => frame >= a && frame < b;

// ------------------------------------------------------------------------------------------------ pictures
const Footage: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: C.black }}>
    <ClipScene src="shorts/s7_hook2.mp4" from={0} dur={F.slowmo} push={[1, 1.02]} origin="55% 80%" />
    <ClipScene src="shorts/s7_slowmo.mp4" from={F.slowmo} dur={F.split - F.slowmo} rate={77 / (F.split - F.slowmo - 1)} push={[1.02, 1.08]} origin="50% 70%" />
    <ClipScene src="shorts/s7_split2.mp4" from={F.split} dur={F.crowd - F.split} push={[1, 1]} />
    <ClipScene src="shorts/s7_crowd.mp4" from={F.crowd} dur={F.tripod - F.crowd} push={[1, 1]} />
    {/* no push on the tracked Blender shots: the overlays are drawn on their pixels */}
    <ClipScene src="shorts/s7_tripod.mp4" from={F.tripod} dur={F.wrong - F.tripod} rate={149 / (F.wrong - F.tripod)} push={[1, 1]} />
    <ClipScene src="shorts/s7_wrong.mp4" from={F.wrong} dur={F.end - F.wrong} push={[1, 1]} />
    {/* Pollen's shove plays forward and ends on the frame just before frame 0: the Short loops on its own */}
    <ClipScene src="shorts/s7_end.mp4" from={F.end} dur={SHORT7_FRAMES - F.end} push={[1, 1]} />
  </AbsoluteFill>
);

// ------------------------------------------------------------------------------------------------ hook (frame 0 and the end)
const Hook: React.FC = () => {
  const frame = useCurrentFrame();
  if (!(frame < F.split || frame >= F.hold0)) return null;
  return (
    <>
      <div style={{ ...DARKEN, height: 700 }} />
      <div style={{ position: "absolute", left: 64, top: 250, ...HEADC, fontSize: 132, color: C.ink, lineHeight: 0.92, ...keyline(0.9, 11) }}>WHO TAUGHT</div>
      <div style={{ position: "absolute", left: 64, top: 372, ...HEADC, fontSize: 132, color: C.acid, lineHeight: 0.92, ...keyline(0.9, 11) }}>IT THIS?</div>
    </>
  );
};

// ------------------------------------------------------------------------------------------------ the simulator, beside the real duck
const Split: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (!between(frame, F.split, F.crowd)) return null;
  const chip = pop(frame, 158, fps, 220, 12);
  const plus = pop(frame, 208, fps, 260, 9);
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", left: 0, right: 0, top: 955, height: 10, backgroundColor: C.black }} />
      <Tag at={F.split + 3} left={64} top={120} bg={C.cyan} size={64}>SIMULATOR</Tag>
      <Tag at={F.split + 14} left={64} top={1000} bg={C.acid} size={64}>REAL ROBOT</Tag>
      {frame >= 158 ? (
        <div style={{ position: "absolute", left: 64, top: 760, opacity: interpolate(chip, [0, 0.3], [0, 1], CLAMP), translate: `${(1 - chip) * -60}px 0` }}>
          <div style={{ display: "inline-block", ...HEADC, fontSize: 64, color: C.black, backgroundColor: C.ink, border: `5px solid ${C.black}`, padding: "4px 16px 8px" }}>
            POINTS ONLY FOR
          </div>
          <div style={{ ...HEADC, fontSize: 96, color: C.acid, marginTop: 8, ...keyline(0.7, 10) }}>ENDING UP STANDING</div>
        </div>
      ) : null}
      {frame >= 208 ? (
        <div style={{ position: "absolute", left: 790, top: 600, ...HEADC, fontSize: 130, color: C.acid, ...keyline(0.95, 11),
          scale: interpolate(plus, [0, 1], [1.6, 1]), opacity: interpolate(plus, [0, 0.2], [0, 1], CLAMP) }}>+1</div>
      ) : null}
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ thousands at once
const Crowd: React.FC = () => {
  const frame = useCurrentFrame();
  if (!between(frame, F.crowd, F.tripod)) return null;
  return (
    <AbsoluteFill>
      <div style={DARKEN} />
      <div style={DISCLOSE}>OUR 3D ILLUSTRATION</div>
      <div style={{ position: "absolute", left: 64, top: 220, opacity: interpolate(frame, [F.crowd + 4, F.crowd + 12], [0, 1], CLAMP) }}>
        <div style={{ ...HEADC, fontSize: 200, color: C.acid, lineHeight: 0.86, ...keyline(1.4, 11) }}>4,096</div>
        <div style={{ ...HEADC, fontSize: 92, color: C.ink, marginTop: 30, ...keyline(0.62, 10) }}>AT ONCE</div>
      </div>
      <div style={{ position: "absolute", left: 64, top: 560, ...MONO, fontSize: 40, color: C.ink, backgroundColor: "rgba(0,0,0,0.6)", padding: "6px 12px",
        opacity: interpolate(frame, [F.crowd + 20, F.crowd + 30], [0, 1], CLAMP) }}>IN POLLEN&apos;S TRAINING COMMAND</div>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ the head-tripod loophole
const TRI_RATE = 149 / (F.wrong - F.tripod);
const Tripod: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (!between(frame, F.tripod, F.wrong)) return null;
  const i = Math.min(TRIPOD_TRACK.length - 1, Math.max(0, Math.floor((frame - F.tripod) * TRI_RATE)));
  const [head, fl, fr] = TRIPOD_TRACK[i];
  const headIn = pop(frame, 512, fps, 240, 11);
  const draw = interpolate(frame, [528, 542], [0, 1], { ...CLAMP, easing: EASE_OUT });
  const d = `M ${head[0]} ${head[1]} L ${fl[0]} ${fl[1]} L ${fr[0]} ${fr[1]} Z`;
  const ev = evolvePath(draw, d);
  const ring = (p: number[], k: number, color: string) => <ellipse cx={p[0]} cy={p[1]} rx={58 * k} ry={20 * k} fill="none" stroke={color} strokeWidth={7} />;
  const footIn = interpolate(frame, [528, 536], [0, 1], CLAMP);
  return (
    <AbsoluteFill>
      <div style={DARKEN} />
      <div style={DISCLOSE}>OUR 3D ILLUSTRATION</div>
      <div style={{ position: "absolute", left: 64, top: 230, opacity: interpolate(frame, [446, 456], [0, 1], CLAMP) }}>
        <div style={{ ...MONO, fontSize: 40, color: C.ink }}>POLLEN&apos;S TRAINING NOTES:</div>
        <div style={{ ...HEADC, fontSize: 70, color: C.acid, marginTop: 10, lineHeight: 1, ...keyline(0.5, 9) }}>&quot;HEAD-TRIPOD</div>
        <div style={{ ...HEADC, fontSize: 70, color: C.acid, lineHeight: 1, ...keyline(0.5, 9) }}>INSTEAD OF STANDING&quot;</div>
      </div>
      <svg width={1080} height={1920} style={{ position: "absolute", inset: 0 }}>
        {draw > 0 ? <path d={d} fill="rgba(216,255,0,0.12)" stroke={C.acid} strokeWidth={8} strokeLinejoin="round" strokeDasharray={ev.strokeDasharray}
          strokeDashoffset={ev.strokeDashoffset} /> : null}
        {frame >= 512 ? ring(head, headIn, C.acid) : null}
        {footIn > 0 ? <g opacity={footIn}>{ring(fl, 0.8, C.cyan)}{ring(fr, 0.8, C.cyan)}</g> : null}
      </svg>
      {frame >= 512 ? (
        <div style={{ position: "absolute", left: Math.min(head[0] - 70, 740), top: head[1] + 44, ...HEADC, fontSize: 60, color: C.acid, opacity: headIn,
          ...keyline(0.42, 8) }}>HEAD</div>
      ) : null}
      {draw > 0.6 ? (
        <div style={{ position: "absolute", left: 64, top: 1420, ...HEADC, fontSize: 104, color: C.acid, ...keyline(0.75, 10),
          opacity: interpolate(draw, [0.6, 1], [0, 1], CLAMP) }}>= A TRIPOD</div>
      ) : null}
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ one duck, five wrong bodies
const SPECS: [number, string][] = [[W.heavy, "HEAVIER ±5%"], [W.off, "OFF BALANCE ±8 MM"], [W.slip, "SLIPPERY 0.7-1.3× GRIP"], [W.batt, "LOW BATTERY"],
  [W.shove, "SHOVED EVERY 3-6 s"]];
const Wrong: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (!between(frame, F.wrong, F.end)) return null;
  const e = WRONG_TRACK[Math.min(WRONG_TRACK.length - 1, Math.max(0, frame - F.wrong))];
  const exIn = interpolate(frame, [W.off + 10, W.off + 18], [0, 1], CLAMP);
  return (
    <AbsoluteFill>
      <div style={{ ...DARKEN, height: 760 }} />
      {/* two set lines (critic round 2: the one long line wrapped onto the chip stack) */}
      <div style={{ ...DISCLOSE, top: 128, lineHeight: 1.15 }}>OUR 3D ILLUSTRATION<br />RANGES FROM POLLEN&apos;S CODE</div>
      {SPECS.map(([at, text], k) => {
        if (frame < at) return null;
        const s = pop(frame, at, fps, 230, 12);
        return (
          <div key={text} style={{ position: "absolute", left: 64, top: 246 + k * 90, ...HEADC, fontSize: 64, lineHeight: 1, color: C.black,
            backgroundColor: k === SPECS.length - 1 ? C.acid : C.ink, border: `5px solid ${C.black}`, padding: "4px 16px 8px",
            opacity: interpolate(s, [0, 0.3], [0, 1], CLAMP), translate: `${(1 - s) * -60}px 0` }}>{text}</div>
        );
      })}
      {/* the shifted balance point inside the glass torso: drawn bigger than ±8 mm, and labelled so */}
      {exIn > 0 ? (
        <div style={{ position: "absolute", left: Math.min(e.com[0] + 70, 620), top: e.com[1] - 52, opacity: exIn, ...HEADC, fontSize: 48, lineHeight: 1,
          color: C.acid, ...keyline(0.36, 8) }}>← SHIFT<br />EXAGGERATED</div>
      ) : null}
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ verdict, over the real duck
const Verdict: React.FC = () => {
  const frame = useCurrentFrame();
  if (!between(frame, F.end, F.hold0)) return null;
  return (
    <AbsoluteFill>
      <div style={{ ...DARKEN, height: 700 }} />
      <Stamp at={848} left={70} top={280} size={110} color={C.acid}>ONE MORE<br />WRONG BODY</Stamp>
    </AbsoluteFill>
  );
};

export const CurveV2Short7: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: C.black }}>
    <Footage />
    <Split />
    <Crowd />
    <Tripod />
    <Wrong />
    <Verdict />
    <Hook />
    <CaptionTrack pages={PAGES} hide={[[145, 220], [512, F.wrong], [W.heavy, F.end]]} until={950} />
    <Credit text="POLLEN ROBOTICS · REAL SPEED" show={[[0, F.slowmo], [F.end, SHORT7_FRAMES]]} />
    <Credit text="POLLEN ROBOTICS · THEIR SLOW-MO" show={[[F.slowmo, F.split]]} />
    <Credit text="POLLEN ROBOTICS · SLOWED" show={[[F.split, F.crowd]]} />

    <Audio src={staticFile("shorts/s7_vo.mp3")} />
    {/* the bed holds one level, drops out before "The trick" and lands back on the cut to the one duck */}
    <Audio src={staticFile("audio/sample-bed.mp3")} volume={(f) => interpolate(f, [0, 2, F.wrong - 16, F.wrong - 6, F.wrong + 1, F.wrong + 5,
      SHORT7_FRAMES - 2, SHORT7_FRAMES], [0.12, 0.12, 0.12, 0.0, 0.0, 0.12, 0.12, 0.12], CLAMP)} />
    {/* the whoosh file peaks ~16 frames in, so each one starts 16 frames before its cut */}
    <Sfx at={F.slowmo - 16} name="whoosh" volume={0.35} />
    <Sfx at={F.split - 16} name="whoosh" volume={0.4} />
    <Sfx at={158} name="thock" volume={0.4} />
    <Sfx at={208} name="thock" volume={0.55} />
    <Sfx at={F.crowd - 16} name="whoosh" volume={0.4} />
    <Sfx at={F.tripod - 16} name="whoosh" volume={0.35} />
    <Sfx at={512} name="thock" volume={0.45} />
    <Sfx at={528} name="form" volume={0.4} />
    <Sfx at={F.wrong - 26} name="riser" volume={0.3} />
    <Sfx at={F.wrong} name="thock" volume={0.85} />
    <Sfx at={F.wrong} name="settle" volume={0.45} />
    <Sfx at={W.heavy} name="thock" volume={0.4} />
    <Sfx at={W.off} name="thock" volume={0.4} />
    <Sfx at={W.slip} name="thock" volume={0.4} />
    <Sfx at={W.batt} name="thock" volume={0.4} />
    <Sfx at={W.shove} name="thock" volume={0.4} />
    <Sfx at={W.hit - 16} name="whoosh" volume={0.45} />
    <Sfx at={F.end - 16} name="whoosh" volume={0.4} />
    <Sfx at={848} name="thock" volume={0.8} />
  </AbsoluteFill>
);
