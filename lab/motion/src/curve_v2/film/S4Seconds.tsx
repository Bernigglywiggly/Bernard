import type React from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { CLAMP } from "../../lib/anim";
import { BG_NIGHT, C, ClipScene, HEADC, Headline, keyline, MONO, pop, slowPush, Stamp, Tag } from "../kit";
import { Disclose, EvidenceStamp, HoldStill, M, SAFE_TOP, Sfx, Shade, TeslaCredit } from "./fx";
import { cue, segFrames } from "./util";

// Roadster film S4 "Seconds, then hours" (Short 3's story in 16:9). Facts: TESLA_ROADSTER_FACTS.md §4-§5: two COPVs
// 600 L (about 250 kg of air); OUR ESTIMATE: 80 kN / ~600 m/s exhaust = ~130 kg/s, so ~2 s at full rear thrust;
// Thrust version: one launch per fill, ~5 s of push (Moravy to Top Gear, S1); refill 2-6 h from a high-pressure
// nitrogen rig today, target under 30 min (S1); Musk on stage: the car can refill its own tank (P1 12:30).
// v2 (critic round 1): the opening is brightened and pushed into the hover; the Thrust quote plays over real footage,
// not the Rocket's two tanks; the refill is our Blender shot of the tanks filling (lab/curve_v2/trials/B_blender/v2,
// --shot refill), with an hours counter; the payoff is a fresh 4K cut of the landing (prep_v2_clips.sh).
const D = segFrames("S4");
const T = {
  handful: cue("S4", "handful"), squeezed: cue("S4", "squeezed"), by: cue("S4", "by"), empty: cue("S4", "empty"), two: cue("S4", "two"),
  tesla: cue("S4", "tesla", 2), single: cue("S4", "single"), five: cue("S4", "five"), but: cue("S4", "but"), lars: cue("S4", "lars"),
  hours: cue("S4", "hours"), target: cue("S4", "target"), elon: cue("S4", "elon"), refill: cue("S4", "refill", 2), long: cue("S4", "long"),
  so: cue("S4", "so"), seconds: cue("S4", "seconds", 3), waits: cue("S4", "waits"),
};
const X = { drain: T.by, quote: T.tesla, clock: T.but, split: T.elon, payoff: T.so };

const Opening: React.FC = () => {
  const frame = useCurrentFrame();
  if (frame >= X.drain) return null;
  return (
    <AbsoluteFill>
      <Shade from="bottom" strength={0.8} />
      <Headline at={T.handful - 6} left={M} top={600} lines={[{ text: "A HANDFUL OF", size: 124 }, { text: "SECONDS IN THE AIR", size: 124, color: C.acid }]} />
      <Tag at={T.squeezed} left={M} top={850} bg={C.cyan} size={64}>ITS FUEL: A TANK OF SQUEEZED GAS</Tag>
    </AbsoluteFill>
  );
};

// both tanks drain in about two real seconds at full rear thrust (OUR ESTIMATE)
const Drain: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < X.drain || frame >= X.quote) return null;
  const level = interpolate(frame, [T.empty, T.empty + 2 * fps], [1, 0], CLAMP);
  const done = pop(frame, T.empty + 2 * fps, fps, 240, 10);
  const tank = (y: number, label: string, w: number) => (
    <div style={{ position: "absolute", left: M, top: y }}>
      <div style={{ ...HEADC, fontSize: 60, color: C.ink, ...keyline(0.42, 8) }}>{label}</div>
      <div style={{ marginTop: 12, width: w, height: 120, borderRadius: 60, border: "7px solid #000", backgroundColor: "rgba(255,255,255,0.12)", overflow: "hidden" }}>
        <div style={{ width: `${level * 100}%`, height: "100%", backgroundColor: level > 0.25 ? C.cyan : C.warn }} />
      </div>
    </div>
  );
  return (
    <AbsoluteFill style={{ background: BG_NIGHT, scale: slowPush(frame, X.drain, X.quote, 1.04), transformOrigin: "40% 50%" }}>
      <Headline at={X.drain + 2} left={M} top={SAFE_TOP} lines={[{ text: "REAR NOZZLES AT FULL POWER", size: 88 }]} />
      {tank(250, "SEAT TANK · 400 L", 1100)}
      {tank(500, "REAR TANK · 200 L", 550)}
      <div style={{ position: "absolute", right: M, top: 260, textAlign: "right" }}>
        <div style={{ ...HEADC, fontSize: 200, color: level > 0 ? C.ink : C.warn, fontVariantNumeric: "tabular-nums", ...keyline(1.3, 11) }}>
          {(2 * (1 - level)).toFixed(1)} s
        </div>
      </div>
      <div style={{ position: "absolute", left: M, top: 730, ...HEADC, fontSize: 84, color: C.warn, opacity: interpolate(done, [0, 0.3], [0, 1], CLAMP),
        scale: interpolate(done, [0, 1], [1.3, 1]), transformOrigin: "0% 50%", ...keyline(0.6, 10) }}>EMPTY IN ABOUT TWO SECONDS</div>
      <EvidenceStamp kind="ours" at={T.empty} left={M} top={840} note="80 kN ÷ ≈600 m/s GAS SPEED ≈ 130 kg A SECOND, FROM ≈250 kg" />
    </AbsoluteFill>
  );
};

const QuoteScene: React.FC = () => {
  const frame = useCurrentFrame();
  if (frame < X.quote || frame >= X.clock) return null;
  const a = interpolate(frame, [T.single - 6, T.single + 6], [0, 1], CLAMP);
  const b = interpolate(frame, [T.five - 6, T.five + 6], [0, 1], CLAMP);
  return (
    <AbsoluteFill>
      <Shade from="bottom" strength={0.85} />
      <EvidenceStamp kind="tesla" at={X.quote + 2} left={M} top={500} text="TESLA TO TOP GEAR" note="ON THE THRUST VERSION" />
      <div style={{ position: "absolute", left: M, top: 650, ...HEADC, fontSize: 150, color: C.ink, opacity: a, translate: `0 ${(1 - a) * 30}px`, ...keyline(1.0, 11) }}>
        ONE LAUNCH PER FILL
      </div>
      <div style={{ position: "absolute", left: M, top: 800, ...HEADC, fontSize: 110, color: C.acid, opacity: b, translate: `0 ${(1 - b) * 30}px`, ...keyline(0.8, 10) }}>
        ≈5 SECONDS OF PUSH
      </div>
    </AbsoluteFill>
  );
};

// the refill: our 3D tanks fill (Blender --shot refill, 8 s, starting empty) while an hours counter runs; the render's
// fill follows EASE_IO over its frames 8-230, so the counter uses the same curve
const FILL_EASE = Easing.bezier(0.65, 0, 0.35, 1);
const Refill: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < X.clock || frame >= X.split) return null;
  const p = FILL_EASE(interpolate(frame - X.clock + 1, [8, 230], [0, 1], CLAMP));
  const mins = Math.round(p * 360);
  const tgt = pop(frame, T.target, fps, 220, 12);
  return (
    <AbsoluteFill>
      <Shade from="bottom" strength={0.85} />
      <div style={{ position: "absolute", right: M, top: SAFE_TOP + 10, textAlign: "right", padding: "10px 24px 14px", backgroundColor: "rgba(0,0,0,0.62)" }}>
        <div style={{ ...MONO, fontSize: 40, color: "#D2CBE3" }}>{p >= 1 ? "FULL" : "REFILLING…"}</div>
        <div style={{ ...HEADC, fontSize: 120, color: p >= 1 ? C.warn : C.ink, fontVariantNumeric: "tabular-nums", ...keyline(0.8, 10) }}>
          {Math.floor(mins / 60)} h {String(mins % 60).padStart(2, "0")} m
        </div>
      </div>
      <EvidenceStamp kind="tesla" at={T.lars - 2} left={M} top={560} text="TESLA'S ENGINEER, TO TOP GEAR" note="LARS MORAVY, VEHICLE ENGINEERING" />
      <div style={{ position: "absolute", left: M, top: 720, ...HEADC, fontSize: 72, color: C.ink, ...keyline(0.5, 9) }}>REFILL FROM A NITROGEN RIG</div>
      <div style={{ position: "absolute", left: M, top: 800, ...HEADC, fontSize: 170, color: C.warn, lineHeight: 0.9,
        opacity: interpolate(frame, [T.hours - 6, T.hours + 4], [0, 1], CLAMP), ...keyline(1.1, 11) }}>2–6 HOURS</div>
      <div style={{ position: "absolute", left: 900, top: 838, padding: "8px 20px 10px", backgroundColor: C.cyan, color: C.black, border: "4px solid #000", ...HEADC,
        fontSize: 64, scale: tgt, transformOrigin: "0% 50%" }}>HIS TARGET: UNDER 30 MIN</div>
    </AbsoluteFill>
  );
};

const Split: React.FC = () => {
  const frame = useCurrentFrame();
  if (frame < X.split || frame >= X.payoff) return null;
  const right = interpolate(frame, [T.long - 20, T.long - 8], [0, 1], CLAMP);
  return (
    <AbsoluteFill style={{ background: BG_NIGHT }}>
      <div style={{ position: "absolute", left: 0, top: 0, width: 960, height: 1080, background: "rgba(255,43,214,0.08)" }} />
      <EvidenceStamp kind="tesla" at={X.split + 2} left={M} top={SAFE_TOP + 20} size={50} text="MUSK, ON STAGE" />
      <div style={{ position: "absolute", left: M, top: 290, width: 760 }}>
        <div style={{ ...HEADC, whiteSpace: "normal", fontSize: 110, color: C.ink, lineHeight: 1, ...keyline(0.8, 10) }}>THE CAR REFILLS ITS OWN TANK</div>
      </div>
      {right > 0 ? <EvidenceStamp kind="tesla" at={T.long - 20} left={1060} top={SAFE_TOP + 20} size={50} text="HIS ENGINEER, TO TOP GEAR" /> : null}
      <div style={{ position: "absolute", left: 1060, top: 290, width: 760, opacity: right }}>
        <div style={{ ...HEADC, whiteSpace: "normal", fontSize: 110, color: C.ink, lineHeight: 1, ...keyline(0.8, 10) }}>2–6 HOURS ON A RIG</div>
      </div>
      <div style={{ position: "absolute", left: 930, top: 330, ...HEADC, fontSize: 90, color: C.acid, ...keyline(0.6, 9) }}>VS</div>
      <Stamp at={T.long} left={M} top={640} size={110}>UNPROVEN</Stamp>
    </AbsoluteFill>
  );
};

const Payoff: React.FC = () => {
  const frame = useCurrentFrame();
  if (frame < X.payoff) return null;
  return (
    <AbsoluteFill>
      <Shade from="top" strength={0.7} />
      <Shade from="bottom" strength={0.75} />
      <Headline at={T.seconds - 8} left={M} top={SAFE_TOP} lines={[{ text: "IT FLIES FOR SECONDS", size: 130, color: C.acid }]} />
      <Headline at={T.waits - 4} left={M} top={810} lines={[{ text: "THEN WAITS FOR HOURS", size: 130, color: C.warn }]} />
    </AbsoluteFill>
  );
};

export const S4Seconds: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: C.black }}>
    <ClipScene src="film/kick_under_slow.mp4" from={0} dur={X.drain} push={[1.42, 1.52]} origin="51% 30%"
      style={{ filter: "brightness(1.6) contrast(1.08) saturate(1.1)" }} />
    <ClipScene src="film/ramp4k_flight.mp4" from={X.quote} dur={X.clock - X.quote} push={[1, 1.05]} origin="45% 40%" />
    <ClipScene src="film/blender_refill.mp4" from={X.clock} dur={240} push={[1, 1.02]} />
    <HoldStill src="film/blender_refill_last.png" from={X.clock + 240} dur={Math.max(1, X.split - X.clock - 240)} push={[1.02, 1.05]} />
    <ClipScene src="film/ramp4k_landing.mp4" from={X.payoff} dur={D - X.payoff} push={[1, 1.04]} origin="40% 55%" />
    <Opening />
    <Drain />
    <QuoteScene />
    <Refill />
    <Split />
    <Payoff />
    <Disclose show={[[X.clock, X.split]]} />
    <TeslaCredit show={[[0, X.drain], [X.quote, X.clock], [X.payoff, D]]} />
    <Sfx at={X.drain} name="whoosh" volume={0.35} />
    <Sfx at={T.empty} name="hiss" volume={0.55} dur={60} />
    <Sfx at={T.empty + 60} name="thock" volume={0.6} />
    <Sfx at={X.quote} name="whoosh" volume={0.3} />
    <Sfx at={X.clock} name="whoosh" volume={0.35} />
    <Sfx at={T.hours - 30} name="tick_run" volume={0.25} dur={40} />
    <Sfx at={T.target} name="thock" volume={0.5} />
    <Sfx at={X.split} name="whoosh" volume={0.35} />
    <Sfx at={T.long} name="thock" volume={0.75} />
    <Sfx at={X.payoff} name="whoosh" volume={0.35} />
  </AbsoluteFill>
);
