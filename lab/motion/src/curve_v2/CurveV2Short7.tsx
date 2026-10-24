import { Audio } from "@remotion/media";
import { evolvePath } from "@remotion/paths";
import type React from "react";
import { AbsoluteFill, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { CLAMP, EASE_OUT } from "../lib/anim";
import { C, CaptionTrack, ClipScene, Credit, HEADC, Headline, keyline, MONO, pop, Sfx, Stamp, Tag } from "./kit";
import { makePages } from "./pager";
import { TRIPOD_TRACK, VARIANT_TRACK } from "./s7Tracks";
import { VO_S7 } from "./voS7Captions";

// Curve Short 7 (for Sun 25 Oct 2026): "How Did This Robot Duck Learn to Get Back Up? (Microduck)". 1080x1920, 30 fps.
// Opens on the visual mystery (a hand shoves the real duck flat and it gets straight back up), per the 24 Oct CRAFT
// lesson. The simulator, the head-tripod loophole and the five deliberately wrong bodies are our own 3D duck
// (lab/curve_v2/shorts/blender/s7_duck.py; Pollen's meshes are non-commercial, so they are never shown). Facts:
// lab/research/MICRODUCK_FACTS.md. Footage: Pollen Robotics, YouTube, 27 Aug 2026 (RAtzEyGBGFU, szW7N_7B3tU), RIFE to
// 30 fps. Narration s7_chris_v1_tight.mp3 (33.4 s). Cuts on the 124 BPM beat. Last frame = frame 0.

export const SHORT7_FRAMES = 1031;

const F = { slowmo: 58, split: 116, sim: 203, grid: 319, tripod: 464, wide: 609, v1: 696, v2: 725, v3: 754, v4: 780, v5: 812,
  real: 856, thousands: 958, rewind: 1001, hold0: 1025 };
const PAGES = makePages(VO_S7);
const DARKEN: React.CSSProperties = { position: "absolute", left: 0, right: 0, top: 0, height: 900,
  background: "linear-gradient(180deg, rgba(1,4,14,0.86) 0%, rgba(1,4,14,0.55) 62%, rgba(1,4,14,0) 100%)" };
const DISCLOSE: React.CSSProperties = { position: "absolute", left: 64, top: 150, ...MONO, fontSize: 40, color: "#C3CCDA" };
const between = (frame: number, a: number, b: number) => frame >= a && frame < b;

// ------------------------------------------------------------------------------------------------ pictures
const Footage: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: C.black }}>
    <ClipScene src="shorts/s7_hook.mp4" from={0} dur={F.slowmo} push={[1, 1.02]} origin="50% 80%" />
    <ClipScene src="shorts/s7_slowmo.mp4" from={F.slowmo} dur={F.split - F.slowmo} rate={77 / (F.split - F.slowmo)} push={[1.02, 1.08]} origin="50% 70%" />
    <ClipScene src="shorts/s7_split.mp4" from={F.split} dur={F.sim - F.split} push={[1, 1]} />
    <ClipScene src="shorts/s7_simwalk.mp4" from={F.sim} dur={F.grid - F.sim} rate={114 / (F.grid - F.sim)} push={[1.04, 1.1]} origin="62% 62%" />
    <ClipScene src="shorts/s7_grid.mp4" from={F.grid} dur={F.tripod - F.grid} rate={129 / (F.tripod - F.grid)} push={[1, 1]} />
    {/* no push on the tracked Blender shots: the overlays are drawn on their pixels */}
    <ClipScene src="shorts/s7_tripod.mp4" from={F.tripod} dur={F.wide - F.tripod} rate={149 / (F.wide - F.tripod)} push={[1, 1]} />
    <ClipScene src="shorts/s7_variants.mp4" from={F.wide} dur={F.v1 - F.wide} rate={59 / (F.v1 - F.wide)} push={[1, 1]} />
    <ClipScene src="shorts/s7_variants.mp4" from={F.v1} dur={F.v2 - F.v1} trimBefore={60} push={[1, 1]} />
    <ClipScene src="shorts/s7_variants.mp4" from={F.v2} dur={F.v3 - F.v2} trimBefore={120} push={[1, 1]} />
    <ClipScene src="shorts/s7_variants.mp4" from={F.v3} dur={F.v4 - F.v3} trimBefore={180} push={[1, 1]} />
    <ClipScene src="shorts/s7_variants.mp4" from={F.v4} dur={F.v5 - F.v4} trimBefore={240} push={[1, 1]} />
    <ClipScene src="shorts/s7_variants.mp4" from={F.v5} dur={F.real - F.v5} trimBefore={300} push={[1, 1]} />
    <ClipScene src="shorts/s7_push.mp4" from={F.real} dur={F.thousands - F.real} rate={107 / (F.thousands - F.real)} push={[1.02, 1.08]} origin="50% 40%" />
    <ClipScene src="shorts/s7_grid.mp4" from={F.thousands} dur={F.rewind - F.thousands} trimBefore={86} push={[1, 1.03]} />
    {/* the rewind lands exactly on the hook's first frame, so the Short loops */}
    <ClipScene src="shorts/s7_hook_rev.mp4" from={F.rewind} dur={SHORT7_FRAMES - F.rewind} rate={59 / (SHORT7_FRAMES - F.rewind - 1)} push={[1, 1]} />
  </AbsoluteFill>
);

// ------------------------------------------------------------------------------------------------ hook (frame 0 and the end)
const Hook: React.FC = () => {
  const frame = useCurrentFrame();
  if (!(frame < F.split || frame >= F.hold0)) return null;
  const punch = frame < F.split ? interpolate(frame, [0, F.split], [1, 1.04], CLAMP) : 1;
  return (
    <>
      <div style={{ ...DARKEN, height: 760 }} />
      <div style={{ position: "absolute", left: 64, top: 250, scale: punch, transformOrigin: "0% 50%" }}>
        <div style={{ ...HEADC, fontSize: 96, color: C.ink, ...keyline(0.66, 11) }}>NOBODY SHOWED IT</div>
        <div style={{ ...HEADC, fontSize: 120, color: C.acid, lineHeight: 0.92, marginTop: 8, ...keyline(0.85, 11) }}>HOW TO GET UP</div>
      </div>
    </>
  );
};

// ------------------------------------------------------------------------------------------------ the simulator, beside the real duck
const Split: React.FC = () => {
  const frame = useCurrentFrame();
  if (!between(frame, F.split, F.sim)) return null;
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", left: 0, right: 0, top: 955, height: 10, backgroundColor: C.black }} />
      <Tag at={F.split + 3} left={64} top={120} bg={C.cyan} size={60}>SIMULATOR</Tag>
      <Tag at={F.split + 14} left={64} top={1000} bg={C.acid} size={60}>REAL ROBOT</Tag>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ points for good walking
const REWARDS: [number, string][] = [[211, "STAY UPRIGHT"], [242, "FOLLOW THE JOYSTICK"], [281, "LIFT YOUR FEET"]];
const Rewards: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (!between(frame, F.sim, F.grid)) return null;
  return (
    <AbsoluteFill>
      <div style={DARKEN} />
      <Tag at={F.sim + 2} left={64} top={170} bg={C.ink} size={54}>POINTS FOR</Tag>
      {REWARDS.map(([at, text], i) => {
        const s = pop(frame, at, fps, 220, 12);
        if (frame < at) return null;
        return (
          <div key={text} style={{ position: "absolute", left: 64, top: 300 + i * 130, display: "flex", alignItems: "center", gap: 22,
            opacity: interpolate(s, [0, 0.3], [0, 1], CLAMP), translate: `${(1 - s) * -70}px 0` }}>
            <div style={{ ...HEADC, fontSize: 70, color: C.black, backgroundColor: C.acid, border: `5px solid ${C.black}`, padding: "2px 16px 6px",
              lineHeight: 1 }}>+1</div>
            <div style={{ ...HEADC, fontSize: 74, color: C.ink, ...keyline(0.52, 10) }}>{text}</div>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ thousands at once
const Grid: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (!between(frame, F.grid, F.tripod)) return null;
  const count = Math.round(interpolate(frame, [F.grid + 8, F.grid + 64], [1, 4096], { ...CLAMP, easing: EASE_OUT }));
  const landed = pop(frame, F.grid + 64, fps, 260, 9);
  return (
    <AbsoluteFill>
      <div style={DARKEN} />
      <div style={DISCLOSE}>OUR 3D ILLUSTRATION OF THE SIMULATOR</div>
      <div style={{ position: "absolute", left: 64, top: 220 }}>
        <div style={{ ...HEADC, fontSize: 240, color: C.acid, lineHeight: 0.86, fontVariantNumeric: "tabular-nums", ...keyline(1.6, 11),
          scale: frame >= F.grid + 64 ? interpolate(landed, [0, 1], [1.12, 1]) : 1, transformOrigin: "0% 100%" }}>{count.toLocaleString("en-GB")}</div>
        <div style={{ ...HEADC, fontSize: 76, color: C.ink, marginTop: 40, ...keyline(0.52, 9),
          opacity: interpolate(frame, [F.grid + 14, F.grid + 24], [0, 1], CLAMP) }}>VIRTUAL DUCKS AT ONCE</div>
      </div>
      <Tag at={F.grid + 70} left={64} top={600} bg={C.cyan} size={46}>POLLEN&apos;S TRAINING COMMAND: 4096 ENVS</Tag>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ the head-tripod loophole
const TRI_RATE = 149 / (F.wide - F.tripod);
const Tripod: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (!between(frame, F.tripod, F.wide)) return null;
  const i = Math.min(TRIPOD_TRACK.length - 1, Math.max(0, Math.floor((frame - F.tripod) * TRI_RATE)));
  const [head, fl, fr] = TRIPOD_TRACK[i];
  const headIn = pop(frame, 562, fps, 240, 11);
  const draw = interpolate(frame, [580, 594], [0, 1], { ...CLAMP, easing: EASE_OUT });
  const d = `M ${head[0]} ${head[1]} L ${fl[0]} ${fl[1]} L ${fr[0]} ${fr[1]} Z`;
  const ev = evolvePath(draw, d);
  const ring = (p: number[], k: number, color: string) => (
    <ellipse cx={p[0]} cy={p[1]} rx={58 * k} ry={20 * k} fill="none" stroke={color} strokeWidth={7} />
  );
  const footIn = interpolate(frame, [580, 588], [0, 1], CLAMP);
  return (
    <AbsoluteFill>
      <div style={DARKEN} />
      <div style={DISCLOSE}>OUR 3D ILLUSTRATION</div>
      <Tag at={467} left={64} top={230} bg={C.acid} size={64}>AND THEY CHEAT</Tag>
      <Headline at={493} top={350} lines={[{ text: "TOLD TO STAND,", size: 112 }]} />
      <Headline at={524} top={470} lines={[{ text: "ONE DID THIS", size: 112, color: C.acid }]} />
      <div style={{ position: "absolute", left: 64, top: 610, ...MONO, fontSize: 40, lineHeight: 1.3, color: C.ink, backgroundColor: "rgba(0,0,0,0.72)",
        padding: "8px 14px", opacity: interpolate(frame, [534, 544], [0, 1], CLAMP) }}>
        POLLEN&apos;S TRAINING NOTES:<br />&quot;HEAD-TRIPOD INSTEAD OF STANDING&quot;
      </div>
      <svg width={1080} height={1920} style={{ position: "absolute", inset: 0 }}>
        {draw > 0 ? <path d={d} fill="rgba(216,255,0,0.12)" stroke={C.acid} strokeWidth={8} strokeLinejoin="round" strokeDasharray={ev.strokeDasharray}
          strokeDashoffset={ev.strokeDashoffset} /> : null}
        {frame >= 562 ? ring(head, headIn, C.acid) : null}
        {footIn > 0 ? <g opacity={footIn}>{ring(fl, 0.8, C.cyan)}{ring(fr, 0.8, C.cyan)}</g> : null}
      </svg>
      {frame >= 562 ? (
        <div style={{ position: "absolute", left: Math.min(head[0] - 90, 760), top: head[1] + 40, ...HEADC, fontSize: 56, color: C.acid, opacity: headIn,
          ...keyline(0.4, 8) }}>HEAD</div>
      ) : null}
      {draw > 0.6 ? (
        <div style={{ position: "absolute", left: 64, top: 1430, ...HEADC, fontSize: 104, color: C.acid, ...keyline(0.75, 10),
          opacity: interpolate(draw, [0.6, 1], [0, 1], CLAMP) }}>= A TRIPOD</div>
      ) : null}
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ five wrong bodies
const Wrong: React.FC = () => {
  const frame = useCurrentFrame();
  if (!between(frame, F.wide, F.real)) return null;
  return (
    <AbsoluteFill>
      <div style={DARKEN} />
      <div style={DISCLOSE}>OUR 3D ILLUSTRATION</div>
      {frame < F.v1 ? (
        <>
          <Headline at={F.wide + 2} top={230} lines={[{ text: "THE REAL TRICK:", size: 100 }]} />
          <Headline at={631} top={350} lines={[{ text: "EVERY COPY GETS", size: 92 }]} />
          <Headline at={658} top={460} stagger={0} lines={[{ text: "A SLIGHTLY", size: 92 }]} />
          <Headline at={676} top={560} lines={[{ text: "WRONG BODY", size: 150, color: C.acid }]} stroke={11} />
        </>
      ) : null}
      <Variant at={F.v1} until={F.v2} word="HEAVIER" spec="MASS ±5%" />
      <Variant at={F.v2} until={F.v3} word="OFF BALANCE" spec="BALANCE POINT ±8 mm" />
      <Variant at={F.v3} until={F.v4} word="SLIPPERY" spec="FOOT GRIP 0.7-1.3×" />
      <Variant at={F.v4} until={F.v5} word="LOW BATTERY" spec="VOLTAGE SAGS" top={1130} />
      <Variant at={F.v5} until={F.real} word="SHOVED" spec="EVERY 3-6 SECONDS" />
      <ComMarker />
    </AbsoluteFill>
  );
};

// top: where the word sits (the low-battery shot keeps its battery icon at the top of frame, so its label goes low)
const Variant: React.FC<{ at: number; until: number; word: string; spec: string; top?: number }> = ({ at, until, word, spec, top = 230 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (!between(frame, at, until)) return null;
  const s = pop(frame, at, fps, 240, 11);
  return (
    <>
      <div style={{ position: "absolute", left: 64, top, ...HEADC, fontSize: word.length > 8 ? 136 : 168, color: C.ink, ...keyline(1.05, 11),
        opacity: interpolate(s, [0, 0.3], [0, 1], CLAMP), translate: `0 ${(1 - s) * 36}px` }}>{word}</div>
      <Tag at={at + 3} left={64} top={top + (word.length > 8 ? 170 : 200)} bg={C.acid} size={58}>{spec}</Tag>
    </>
  );
};

// the off-balance duck: dashed plumb line from the shifted centre of mass to the floor, outside its feet
const ComMarker: React.FC = () => {
  const frame = useCurrentFrame();
  if (!between(frame, F.v2 + 4, F.v3)) return null;
  const e = VARIANT_TRACK[Math.min(179, 120 + (frame - F.v2))];
  return (
    <svg width={1080} height={1920} style={{ position: "absolute", inset: 0 }}>
      <line x1={e.com[0]} y1={e.com[1]} x2={e.floor[0]} y2={e.floor[1]} stroke={C.ink} strokeWidth={5} strokeDasharray="16 12" />
      <ellipse cx={e.floor[0]} cy={e.floor[1]} rx={46} ry={14} fill="none" stroke={C.warn} strokeWidth={6} />
    </svg>
  );
};

// ------------------------------------------------------------------------------------------------ verdict
const Verdict: React.FC = () => {
  const frame = useCurrentFrame();
  if (!between(frame, F.real, F.rewind)) return null;
  if (frame >= F.thousands) {
    return (
      <AbsoluteFill>
        <div style={DARKEN} />
        <div style={DISCLOSE}>OUR 3D ILLUSTRATION</div>
        <Headline at={F.thousands + 2} top={250} lines={[{ text: "IT HAS ALREADY BEATEN", size: 78 }]} />
        <Headline at={968} top={350} lines={[{ text: "THOUSANDS", size: 160, color: C.acid }]} stroke={12} />
      </AbsoluteFill>
    );
  }
  return (
    <AbsoluteFill>
      <div style={{ ...DARKEN, height: 700 }} />
      <Headline at={F.real + 4} top={230} lines={[{ text: "THE REAL DUCK =", size: 112 }]} />
      <Stamp at={906} left={70} top={390} size={104} color={C.acid}>ONE MORE<br />WRONG BODY</Stamp>
    </AbsoluteFill>
  );
};

export const CurveV2Short7: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: C.black }}>
    <Footage />
    <Split />
    <Rewards />
    <Grid />
    <Tripod />
    <Wrong />
    <Verdict />
    <Hook />
    <CaptionTrack pages={PAGES} hide={[[562, F.wide], [F.v1, F.real]]} until={F.rewind} />
    <Credit text="POLLEN ROBOTICS · REAL SPEED" show={[[0, F.slowmo], [F.real, F.thousands], [F.hold0, SHORT7_FRAMES]]} />
    <Credit text="POLLEN ROBOTICS · THEIR SLOW-MO" show={[[F.slowmo, F.split]]} />
    <Credit text="FOOTAGE: POLLEN ROBOTICS" show={[[F.split, F.sim]]} />
    <Credit text="POLLEN'S SIMULATOR · SLOWED 2×" show={[[F.sim, F.grid]]} />
    <Credit text="RANGES: POLLEN'S TRAINING CODE" show={[[F.wide, F.real]]} />

    <Audio src={staticFile("shorts/s7_vo.mp3")} />
    {/* the bed holds one level, drops out just before "The real trick" and lands back on the cut */}
    <Audio src={staticFile("audio/sample-bed.mp3")} volume={(f) => interpolate(f, [0, 2, F.wide - 16, F.wide - 6, F.wide + 1, F.wide + 5,
      SHORT7_FRAMES - 2, SHORT7_FRAMES], [0.06, 0.12, 0.12, 0.0, 0.0, 0.12, 0.12, 0.06], CLAMP)} />
    <Sfx at={F.slowmo} name="whoosh" volume={0.35} />
    <Sfx at={F.split} name="whoosh" volume={0.4} />
    <Sfx at={F.sim} name="whoosh" volume={0.3} />
    <Sfx at={211} name="thock" volume={0.35} />
    <Sfx at={242} name="thock" volume={0.35} />
    <Sfx at={281} name="thock" volume={0.35} />
    <Sfx at={F.grid} name="riser" volume={0.3} />
    <Sfx at={F.grid + 8} name="tick_run" volume={0.22} dur={56} />
    <Sfx at={F.grid + 64} name="thock" volume={0.6} />
    <Sfx at={F.tripod} name="whoosh" volume={0.35} />
    <Sfx at={562} name="thock" volume={0.45} />
    <Sfx at={580} name="form" volume={0.4} />
    <Sfx at={F.wide - 26} name="riser" volume={0.3} />
    <Sfx at={F.wide} name="thock" volume={0.9} />
    <Sfx at={F.wide} name="settle" volume={0.5} />
    <Sfx at={F.v1} name="whoosh" volume={0.3} />
    <Sfx at={F.v2} name="whoosh" volume={0.3} />
    <Sfx at={F.v3} name="whoosh" volume={0.3} />
    <Sfx at={F.v4} name="whoosh" volume={0.3} />
    <Sfx at={F.v5} name="whoosh" volume={0.3} />
    <Sfx at={F.v5 + 11} name="thock" volume={0.7} />
    <Sfx at={F.real} name="whoosh" volume={0.4} />
    <Sfx at={906} name="thock" volume={0.8} />
    <Sfx at={F.thousands} name="whoosh" volume={0.35} />
    <Sfx at={968} name="thock" volume={0.7} />
    <Sfx at={F.rewind} name="rewind" volume={0.45} />
  </AbsoluteFill>
);
