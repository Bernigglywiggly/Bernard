import type React from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { CLAMP, EASE_OUT } from "../../lib/anim";
import { theme } from "../../theme";
import { BG_NIGHT, C, ClipScene, HEADC, Headline, keyline, MONO, pop, slowPush, Tag } from "../kit";
import { Disclose, EvidenceStamp, HoldStill, M, SAFE_TOP, Sfx, Shade, TeslaCredit } from "./fx";
import { cue, segFrames } from "./util";

// Roadster film S1 "The hang", re-cut for the film in v2 (critic round 1: 0:00-0:26 was Short 1 frame for frame).
// Frame 0 pushes 1.6x into the ramp lip with the words clear of the car; a promise beat after the hook names the
// film's three payoffs in three hard cuts (Tesla's 0.81 s, our ~2 s of gas, Tesla's contract that can't guarantee
// delivery); no loop-back at the end. Facts: TESLA_ROADSTER_FACTS.md §2 (fans + skirts, "up to 2 G's", "even when
// stationary"), P2 (the ramp), P4 (0.81 s, Tesla's timing), §5 [EST] (~2 s of gas), §13.1 #1 (US clause 4).
// Tesla footage: hang_slow8 (8x slower), zero60_slow, drop, ramp_leave_top. Our 3D: blender_gauge, blender_hang.
const D = segFrames("S1");
const T = {
  vac: cue("S1", "vacuumed"), time: cue("S1", "time"), count: cue("S1", "count"), read: cue("S1", "read"), fans: cue("S1", "fans"),
  skirts: cue("S1", "skirts"), pins: cue("S1", "pins"), twice: cue("S1", "twice"), wing: cue("S1", "unlike"), still: cue("S1", "standing"),
  go: cue("S1", "then", 2), jets: cue("S1", "jets"),
};
// the promise beat: three hard cuts, each landing just before its words
const P = { launch: T.time - 3, gas: T.count - 3, contract: T.read - 3 };
const X = { blender: T.fans - 2, hold: T.fans - 2 + 180, bars: T.wing, drop: T.go, landing: T.go + 111 };

const Hook: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame >= P.launch) return null;
  const vac = pop(frame, T.vac, fps, 240, 10);
  return (
    <AbsoluteFill>
      <Shade from="left" strength={0.8} />
      <div style={{ position: "absolute", left: M, top: 190 }}>
        <div style={{ ...HEADC, fontSize: 150, color: C.ink, ...keyline(1, 11) }}>UPSIDE DOWN</div>
        <div style={{ ...HEADC, fontSize: 150, color: C.acid, ...keyline(1, 11) }}>AND NOT</div>
        <div style={{ ...HEADC, fontSize: 150, color: C.acid, ...keyline(1, 11) }}>FALLING?</div>
        {frame >= T.vac ? (
          <div style={{ ...HEADC, fontSize: 190, color: C.magenta, marginTop: 14, scale: interpolate(vac, [0, 1], [1.6, 1]),
            opacity: interpolate(vac, [0, 0.25], [0, 1], CLAMP), transformOrigin: "0% 50%", rotate: "-3deg", ...keyline(1.3, 12) }}>VACUUMED</div>
        ) : null}
      </div>
    </AbsoluteFill>
  );
};

// promise 1: the launch, on Tesla's own stopwatch
const PromiseLaunch: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < P.launch || frame >= P.gas) return null;
  const n = pop(frame, P.launch, fps, 260, 12);
  return (
    <AbsoluteFill>
      <Shade from="left" strength={0.75} />
      <div style={{ position: "absolute", left: M, top: SAFE_TOP + 20, scale: interpolate(n, [0, 1], [1.25, 1]), transformOrigin: "0% 30%",
        opacity: interpolate(n, [0, 0.2], [0, 1], CLAMP) }}>
        <div style={{ ...HEADC, fontSize: 84, color: C.cyan, ...keyline(0.6, 9) }}>0–60 MPH</div>
        <div style={{ ...HEADC, fontSize: 320, color: C.acid, lineHeight: 0.86, ...keyline(2.1, 12) }}>0.81<span style={{ fontSize: 160, marginLeft: 14 }}>s</span></div>
      </div>
      <EvidenceStamp kind="tesla" at={P.launch + 4} left={M} top={600} text="TESLA'S OWN TIMING" />
    </AbsoluteFill>
  );
};

// promise 2: the gas, by our own sum (over our 3D: the rear jets empty both tanks)
const PromiseGas: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < P.gas || frame >= P.contract) return null;
  const n = pop(frame, P.gas, fps, 260, 12);
  return (
    <AbsoluteFill>
      <Shade from="bottom" strength={0.85} />
      <div style={{ position: "absolute", left: M, top: 560, scale: interpolate(n, [0, 1], [1.25, 1]), transformOrigin: "0% 70%",
        opacity: interpolate(n, [0, 0.2], [0, 1], CLAMP) }}>
        <div style={{ ...HEADC, fontSize: 230, color: C.ink, lineHeight: 0.86, ...keyline(1.6, 12) }}>≈2 SECONDS</div>
        <div style={{ ...HEADC, fontSize: 84, color: C.cyan, ...keyline(0.6, 10) }}>OF GAS AT FULL THRUST</div>
      </div>
      <EvidenceStamp kind="ours" at={P.gas + 4} left={1220} top={850} />
    </AbsoluteFill>
  );
};

// promise 3: the contract (the same clause S7 reads in full, so the paper carries across the film)
const SERIF = theme.fonts.serif;
const INK = "#111318";
const PromiseContract: React.FC = () => {
  const frame = useCurrentFrame();
  if (frame < P.contract || frame >= X.blender) return null;
  const inn = interpolate(frame, [P.contract, P.contract + 8], [1, 0], { ...CLAMP, easing: EASE_OUT });
  const hi = interpolate(frame, [T.read + 30, T.read + 58], [0, 1], { ...CLAMP, easing: Easing.inOut(Easing.quad) });
  return (
    <AbsoluteFill style={{ background: BG_NIGHT }}>
      <AbsoluteFill style={{ translate: `${inn * 900}px 0`, rotate: `${-1.6 + inn * 2}deg`, scale: slowPush(frame, P.contract, X.blender, 1.05),
        transformOrigin: "45% 50%" }}>
        <div style={{ position: "absolute", left: 90, top: 110, width: 1900, height: 1000, backgroundColor: "#FFFFFF", boxShadow: "0 30px 90px rgba(0,0,0,0.7)" }} />
        <div style={{ position: "absolute", left: 190, top: 330, ...MONO, fontSize: 40, color: "#5E6670" }}>TESLA ROADSTER RESERVATION AGREEMENT · US v.20261015</div>
        <div style={{ position: "absolute", left: 190, top: 410, fontFamily: SERIF, fontWeight: 500, fontSize: 64, color: INK }}>4. Delivery</div>
        <div style={{ position: "absolute", left: 190, top: 520, width: 1620, fontFamily: SERIF, fontWeight: 500, fontSize: 66, lineHeight: 1.4, color: INK }}>
          …we cannot guarantee when your vehicle will actually be delivered{" "}
          <span style={{ backgroundImage: `linear-gradient(${C.acid}, ${C.acid})`, backgroundRepeat: "no-repeat", backgroundSize: `${hi * 100}% 100%`,
            boxDecorationBreak: "clone", WebkitBoxDecorationBreak: "clone", padding: "0 4px" }}>or if it will be delivered.</span>
        </div>
      </AbsoluteFill>
      <EvidenceStamp kind="tesla" at={P.contract + 6} left={M} top={SAFE_TOP + 10} text="TESLA'S OWN CONTRACT" note="US RESERVATION AGREEMENT, CLAUSE 4" />
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
      <Tag at={T.fans + 4} left={M} top={SAFE_TOP + 10} bg={C.cyan} size={64}>FANS PULL THE AIR OUT</Tag>
      <Tag at={T.skirts} left={M} top={SAFE_TOP + 120} bg={C.magenta} color={C.ink} size={64}>SKIRTS SEAL THE GAP</Tag>
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
      <div style={{ position: "absolute", left: 960, top: 880, ...HEADC, fontSize: 64, color: C.cyan, opacity: push, ...keyline(0.45, 8) }}>AIR PUSHING UP</div>
      <div style={{ position: "absolute", left: M, top: 700, padding: "12px 26px 16px", backgroundColor: C.acid, color: C.black, border: "5px solid #000",
        ...HEADC, fontSize: 96, scale: badge, rotate: `${interpolate(badge, [0, 1], [-10, -2])}deg`, transformOrigin: "0% 50%" }}>
        UP TO 2× ITS WEIGHT
      </div>
      <EvidenceStamp kind="tesla" at={T.twice + 10} left={M} top={850} />
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
  const row = (y: number, label: string, v: number, color: string, note?: string) => (
    <div style={{ position: "absolute", left: M, top: y }}>
      <div style={{ ...HEADC, fontSize: 84, color, ...keyline(0.6, 9) }}>{label}</div>
      <div style={{ marginTop: 14, width: 1300, height: 90, border: "6px solid #000", backgroundColor: "rgba(255,255,255,0.12)" }}>
        <div style={{ width: `${v * 100}%`, height: "100%", backgroundColor: color }} />
      </div>
      {note ? <div style={{ ...MONO, fontSize: 40, color: "#D2CBE3", marginTop: 10 }}>{note}</div> : null}
    </div>
  );
  return (
    <AbsoluteFill style={{ background: BG_NIGHT, scale: slowPush(frame, X.bars, X.drop, 1.04), transformOrigin: "40% 50%" }}>
      <Headline at={X.bars + 2} left={M} top={SAFE_TOP} lines={[{ text: "GRIP FROM THE AIR AS THE CAR SLOWS", size: 92 }]} />
      <div style={{ position: "absolute", right: M, top: 270, textAlign: "right" }}>
        <div style={{ ...HEADC, fontSize: 230, color: C.ink, fontVariantNumeric: "tabular-nums", ...keyline(1.5, 11) }}>{mph}</div>
        <div style={{ ...HEADC, fontSize: 70, color: "#C3CAD2", ...keyline(0.5, 8) }}>MPH</div>
      </div>
      {row(330, "A WING", wing, "#8FA3B8", "DOWNFORCE FALLS WITH SPEED SQUARED")}
      {row(600, "THE FANS", 1, C.cyan)}
      <EvidenceStamp kind="tesla" at={T.still - 10} left={M} top={812} note="THE FANS WORK “EVEN WHEN STATIONARY”" />
    </AbsoluteFill>
  );
};

const Release: React.FC = () => {
  const frame = useCurrentFrame();
  if (frame < X.drop) return null;
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
    {/* frame 0: 1.6x into the ramp lip, the car on the right half, the words on the left */}
    <ClipScene src="film/hang_slow8.mp4" from={0} dur={P.launch} push={[1.6, 1.72]} origin="26% 55%" />
    <ClipScene src="film/zero60_slow.mp4" from={P.launch} dur={P.gas - P.launch} trimBefore={45} push={[1.05, 1.12]} origin="40% 60%" />
    <ClipScene src="film/blender_gauge.mp4" from={P.gas} dur={P.contract - P.gas} push={[1.02, 1.06]} />
    <ClipScene src="film/blender_hang.mp4" from={X.blender} dur={180} push={[1, 1.03]} />
    <HoldStill src="film/blender_hang_last.png" from={X.hold} dur={X.bars - X.hold} push={[1.03, 1.07]} origin="60% 50%" />
    <ClipScene src="film/drop.mp4" from={X.drop} dur={X.landing - X.drop} push={[1, 1.04]} />
    <ClipScene src="film/ramp_leave_top.mp4" from={X.landing} dur={D - X.landing} trimBefore={250} push={[1.02, 1.06]} />
    <Hook />
    <PromiseLaunch />
    <PromiseGas />
    <PromiseContract />
    <Mechanism />
    <Bars />
    <Release />
    <Disclose show={[[P.gas, P.contract], [X.blender, X.bars]]} />
    <TeslaCredit show={[[0, P.gas], [X.drop, D]]} />
    <Sfx at={T.vac} name="thock" volume={0.7} />
    <Sfx at={P.launch} name="thock" volume={0.6} />
    <Sfx at={P.gas} name="hiss" volume={0.45} dur={50} />
    <Sfx at={P.contract} name="whoosh" volume={0.4} />
    <Sfx at={X.blender} name="whoosh" volume={0.35} />
    <Sfx at={T.twice + 6} name="thock" volume={0.55} />
    <Sfx at={X.bars} name="whoosh" volume={0.35} />
    <Sfx at={X.drop} name="hiss" volume={0.5} dur={110} />
  </AbsoluteFill>
);
