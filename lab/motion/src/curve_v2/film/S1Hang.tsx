import type React from "react";
import { AbsoluteFill, interpolate, Sequence, useCurrentFrame, useVideoConfig } from "remotion";
import { CLAMP, EASE_OUT } from "../../lib/anim";
import { BG_NIGHT, C, ClipScene, HEADC, Headline, keyline, MONO, pop, Sfx, slowPush, Tag } from "../kit";
import { Disclose, HoldStill, M, Shade, TeslaCredit } from "./fx";
import { cue, segFrames } from "./util";

// Roadster film S1 "The hang" (= Short 1's story, re-cut for 16:9). Facts: TESLA_ROADSTER_FACTS.md §2 (fans + skirts,
// "up to 2 G's", "even when stationary"), P2 (the ramp). Tesla footage: hang_slow8 (8x slower), drop (the release).
// Our 3D: blender_hang (x-ray: fans pull air out, skirts seal, pressure pushes in).
const D = segFrames("S1");
const T = {
  vac: cue("S1", "vacuumed"), fans: cue("S1", "fans"), skirts: cue("S1", "skirts"), pins: cue("S1", "pins"), twice: cue("S1", "twice"),
  wing: cue("S1", "and"), still: cue("S1", "standing"), go: cue("S1", "then", 2), jets: cue("S1", "jets"), lands: cue("S1", "lands."),
  that: cue("S1", "that's"),
};
const X = { blender: T.fans, hold: T.fans + 180, bars: T.wing, drop: T.go, landing: T.go + 111, back: T.that };

const Hook: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const opening = frame < X.blender;
  const ending = frame >= X.back;
  if (!opening && !ending) return null;
  const vac = pop(frame, T.vac, fps, 240, 10);
  const q = opening && frame < T.vac;
  return (
    <AbsoluteFill>
      <Shade from="left" strength={0.75} />
      <div style={{ position: "absolute", left: M, top: 220 }}>
        <div style={{ ...HEADC, fontSize: 150, color: C.ink, ...keyline(1, 11) }}>UPSIDE DOWN</div>
        <div style={{ ...HEADC, fontSize: 150, color: C.acid, ...keyline(1, 11) }}>{ending ? "AND NOT FALLING" : "AND NOT FALLING?"}</div>
        {opening && !q ? (
          <div style={{ ...HEADC, fontSize: 210, color: C.magenta, marginTop: 10, scale: interpolate(vac, [0, 1], [1.6, 1]),
            opacity: interpolate(vac, [0, 0.25], [0, 1], CLAMP), transformOrigin: "0% 50%", rotate: "-3deg", ...keyline(1.4, 12) }}>VACUUMED</div>
        ) : null}
      </div>
    </AbsoluteFill>
  );
};

// fans pull the air out, skirts seal, the outside air pushes up with up to twice the car's weight
const Mechanism: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < X.blender || frame >= X.bars) return null;
  const push = interpolate(frame, [T.twice - 10, T.twice + 14], [0, 1], { ...CLAMP, easing: EASE_OUT });
  const weight = interpolate(frame, [T.pins, T.pins + 14], [0, 1], { ...CLAMP, easing: EASE_OUT });
  const badge = pop(frame, T.twice + 6, fps, 230, 11);
  return (
    <AbsoluteFill>
      <Shade from="bottom" strength={0.6} />
      <Tag at={T.fans + 4} left={M} top={150} bg={C.cyan} size={64}>FANS PULL THE AIR OUT</Tag>
      <Tag at={T.skirts} left={M} top={260} bg={C.magenta} color={C.ink} size={64}>SKIRTS SEAL THE GAP</Tag>
      {/* the balance of forces, drawn over the held x-ray */}
      <svg width={1920} height={1080} style={{ position: "absolute", inset: 0, opacity: weight }}>
        <defs>
          <marker id="headC" markerWidth="6" markerHeight="6" refX="3" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill={C.cyan} /></marker>
          <marker id="headW" markerWidth="6" markerHeight="6" refX="3" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill={C.warn} /></marker>
        </defs>
        <line x1={1300} y1={330} x2={1300} y2={330 + 230 * weight} stroke={C.warn} strokeWidth={26} markerEnd="url(#headW)" />
        <line x1={1480} y1={900} x2={1480} y2={900 - 460 * push} stroke={C.cyan} strokeWidth={26} markerEnd="url(#headC)" />
      </svg>
      <div style={{ position: "absolute", left: 1170, top: 250, ...HEADC, fontSize: 64, color: C.warn, opacity: weight, ...keyline(0.45, 8) }}>WEIGHT</div>
      <div style={{ position: "absolute", left: 1260, top: 920, ...HEADC, fontSize: 64, color: C.cyan, opacity: push, ...keyline(0.45, 8) }}>AIR PUSHING UP</div>
      <div style={{ position: "absolute", left: M, top: 760, padding: "12px 26px 16px", backgroundColor: C.acid, color: C.black, border: "5px solid #000",
        ...HEADC, fontSize: 96, scale: badge, rotate: `${interpolate(badge, [0, 1], [-10, -2])}deg`, transformOrigin: "0% 50%" }}>
        UP TO 2× ITS WEIGHT
      </div>
      {frame >= T.twice ? <div style={{ position: "absolute", left: M + 6, top: 900, ...MONO, fontSize: 34, color: C.ink, opacity: badge }}>TESLA&apos;S CLAIM</div> : null}
    </AbsoluteFill>
  );
};

// a wing needs speed, the fans don't: speed falls to zero, the wing's grip drains (v squared), the fans' holds
const Bars: React.FC = () => {
  const frame = useCurrentFrame();
  if (frame < X.bars || frame >= X.drop) return null;
  const k = interpolate(frame, [X.bars + 20, T.still + 10], [0, 1], { ...CLAMP, easing: EASE_OUT });
  const mph = Math.round(100 * (1 - k));
  const wing = (1 - k) * (1 - k);
  const row = (y: number, label: string, v: number, color: string, note: string) => (
    <div style={{ position: "absolute", left: M, top: y }}>
      <div style={{ ...HEADC, fontSize: 84, color, ...keyline(0.6, 9) }}>{label}</div>
      <div style={{ marginTop: 14, width: 1300, height: 90, border: "6px solid #000", backgroundColor: "rgba(255,255,255,0.12)" }}>
        <div style={{ width: `${v * 100}%`, height: "100%", backgroundColor: color }} />
      </div>
      <div style={{ ...MONO, fontSize: 34, color: "#D2CBE3", marginTop: 10 }}>{note}</div>
    </div>
  );
  return (
    <AbsoluteFill style={{ background: BG_NIGHT, scale: slowPush(frame, X.bars, X.drop, 1.04), transformOrigin: "40% 50%" }}>
      <Headline at={X.bars + 2} left={M} top={90} lines={[{ text: "GRIP FROM THE AIR AS THE CAR SLOWS", size: 92 }]} />
      <div style={{ position: "absolute", right: M, top: 260, textAlign: "right" }}>
        <div style={{ ...HEADC, fontSize: 230, color: C.ink, fontVariantNumeric: "tabular-nums", ...keyline(1.5, 11) }}>{mph}</div>
        <div style={{ ...HEADC, fontSize: 70, color: "#C3CAD2", ...keyline(0.5, 8) }}>MPH</div>
      </div>
      {row(330, "A WING", wing, "#8FA3B8", "DOWNFORCE FALLS WITH SPEED SQUARED")}
      {row(620, "THE FANS", 1, C.cyan, "TESLA: WORKS \"EVEN WHEN STATIONARY\"")}
    </AbsoluteFill>
  );
};

const Release: React.FC = () => {
  const frame = useCurrentFrame();
  if (frame < X.drop || frame >= X.back) return null;
  return (
    <AbsoluteFill>
      <Shade from="left" strength={0.55} />
      <Headline at={X.drop + 4} left={M} top={200} lines={[{ text: "THEN IT LETS GO", size: 120 }]} />
      <Tag at={T.jets} left={M} top={360} bg={C.ink} size={70}>COMPRESSED-GAS JETS ROLL IT UPRIGHT</Tag>
    </AbsoluteFill>
  );
};

export const S1Hang: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: C.black }}>
    <ClipScene src="film/hang_slow8.mp4" from={0} dur={X.blender} push={[1, 1.06]} origin="45% 40%" />
    <ClipScene src="film/blender_hang.mp4" from={X.blender} dur={180} push={[1, 1.03]} />
    <HoldStill src="film/blender_hang_last.png" from={X.hold} dur={X.bars - X.hold} push={[1.03, 1.07]} origin="60% 50%" />
    <ClipScene src="film/drop.mp4" from={X.drop} dur={X.landing - X.drop} push={[1, 1.04]} />
    <ClipScene src="film/ramp_leave_top.mp4" from={X.landing} dur={X.back - X.landing} trimBefore={250} push={[1.02, 1.06]} />
    <ClipScene src="film/hang_slow8.mp4" from={X.back} dur={D - X.back} trimBefore={120} push={[1.03, 1.06]} origin="45% 40%" />
    <Hook />
    <Mechanism />
    <Bars />
    <Release />
    <Disclose show={[[X.blender, X.bars]]} />
    <TeslaCredit show={[[0, X.blender], [X.drop, D]]} />
    <Sequence ><Sfx at={T.vac} name="thock" volume={0.7} /></Sequence>
    <Sfx at={X.blender} name="whoosh" volume={0.35} />
    <Sfx at={T.twice + 6} name="thock" volume={0.55} />
    <Sfx at={X.bars} name="whoosh" volume={0.35} />
    <Sfx at={X.drop} name="hiss" volume={0.5} dur={110} />
    <Sfx at={X.back} name="whoosh" volume={0.3} />
  </AbsoluteFill>
);
