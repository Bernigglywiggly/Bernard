import { Audio, Video } from "@remotion/media";
import type React from "react";
import {
  AbsoluteFill,
  Easing,
  Img,
  interpolate,
  Sequence,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { CLAMP, EASE_IN_OUT, EASE_OUT, unitFor } from "../lib/anim";
import { keyline } from "./HybridC";
import { v2 } from "./palette";
import { VO_S1_CAPTIONS } from "./voS1Captions";

// Roadster Short 1 (18 Oct 2026): "How the Tesla Roadster Hangs Upside Down". 1080x1920, 30 fps.
// Built natively in 9:16 from Tesla's 4K Ramp upload (crop 1215x2160 at x 1450, so no upscale). RIFE v4.6 makes the
// 20x slow motion and turns the 23.976 fps drop into true 30 fps (no duplicate frames). Fixes from CRITIC_C_v2.md:
// the inversion is named at frame 0, no bordered card, labels at 48 px cap height or more, outlines instead of
// glows, the landing plays before the rewind, and the last frame is frame 0, so the loop has no seam.
// Narration lab/curve_v2/shorts/vo/s1_chris_v4.mp3 (27.0 s). Facts: TESLA_ROADSTER_FACTS.md P1 P2 P10 S3 S5.

export const SHORT1_FRAMES = 817;

const F = {
  hookOut: 60, // "vacuumed" at 2.12 s
  diag: 114, // "Fans" at 3.80 s
  holdFrom: 125, // the 20x clip ends; its last frame (source frame 11) is the drop's first frame
  diagOut: 570,
  drop: 580, // "Then" at 19.32 s, on the bed's downbeat
  rewind: 734, // the drop clip ends (5.13 s); "lands" at 24.28-24.65 s
  hookRev: 765,
  hookBack: 798, // "without falling" 26.30-27.09 s
  hold0: 815,
};

const ORIGIN_HOOK = "42% 47%";
const ORIGIN_DROP = "40% 58%";

// One camera for every clip, driven by the absolute frame, so cuts between clips of the same framing are invisible.
const camera = (f: number) => {
  if (f < F.diag) return { s: interpolate(f, [0, F.diag], [1.25, 1.29], CLAMP), ty: 40, o: ORIGIN_HOOK };
  if (f < F.diagOut) {
    const k = interpolate(f, [F.diag, F.diag + 18], [0, 1], { ...CLAMP, easing: EASE_IN_OUT });
    const push = interpolate(f, [F.diag + 18, F.diagOut], [1, 1.05], CLAMP);
    return { s: interpolate(k, [0, 1], [1.29, 1]) * push, ty: interpolate(k, [0, 1], [40, -384]), o: ORIGIN_HOOK };
  }
  if (f < F.drop) {
    const k = interpolate(f, [F.diagOut, F.drop], [0, 1], { ...CLAMP, easing: EASE_IN_OUT });
    return { s: interpolate(k, [0, 1], [1.05, 1]), ty: interpolate(k, [0, 1], [-384, 0]), o: ORIGIN_HOOK };
  }
  if (f < F.rewind) return { s: interpolate(f, [F.drop, F.rewind], [1, 1.06], CLAMP), ty: 0, o: ORIGIN_DROP };
  if (f < F.hookRev) return { s: interpolate(f, [F.rewind, F.hookRev], [1.06, 1], CLAMP), ty: 0, o: ORIGIN_DROP };
  const k = interpolate(f, [F.hookRev, F.hold0], [0, 1], { ...CLAMP, easing: EASE_IN_OUT });
  return { s: interpolate(k, [0, 1], [1, 1.25]), ty: interpolate(k, [0, 1], [0, 40]), o: ORIGIN_HOOK };
};

const GRADE = "saturate(1.12) contrast(1.06) brightness(1.06)";
const fill: React.CSSProperties = { width: "100%", height: "100%", filter: GRADE };

const Footage: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const c = camera(frame);
  return (
    <AbsoluteFill style={{ overflow: "hidden", backgroundColor: v2.colors.black }}>
      <AbsoluteFill style={{ scale: c.s, translate: `0 ${c.ty}px`, transformOrigin: c.o }}>
        <Sequence durationInFrames={F.holdFrom} premountFor={fps}>
          <Video src={staticFile("shorts/s1_hook_20x.mp4")} muted style={fill} />
        </Sequence>
        <Sequence from={F.holdFrom} durationInFrames={F.drop - F.holdFrom}>
          <Img src={staticFile("shorts/s1_hook_last.png")} style={fill} />
        </Sequence>
        <Sequence from={F.drop} durationInFrames={F.rewind - F.drop} premountFor={fps}>
          <Video src={staticFile("shorts/s1_drop.mp4")} muted style={fill} />
        </Sequence>
        <Sequence from={F.rewind} durationInFrames={F.hookRev - F.rewind} premountFor={fps}>
          <Video src={staticFile("shorts/s1_drop_rev5x.mp4")} muted style={fill} />
        </Sequence>
        <Sequence from={F.hookRev} durationInFrames={F.hold0 - F.hookRev} premountFor={fps}>
          <Video src={staticFile("shorts/s1_hook_20x_rev.mp4")} muted playbackRate={2.5} style={fill} />
        </Sequence>
        {/* the exact frame-0 picture under the last frames: the replay starts on the same image */}
        <Sequence from={F.hold0}>
          <Img src={staticFile("shorts/s1_frame0.png")} style={fill} />
        </Sequence>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

const HEAD: React.CSSProperties = { fontFamily: v2.fonts.heavy, fontWeight: 900, letterSpacing: "-0.02em", lineHeight: 0.9 };
// Archivo's width axis (62-125): big words run condensed so they fit the 9:16 frame on one line.
const HEADC: React.CSSProperties = { ...HEAD, fontVariationSettings: "'wdth' 82", whiteSpace: "nowrap" };

// Frame 0 and the last frame: the claim and the mystery in five words. Landed at frame 0 (it is the fallback
// thumbnail); it leaves on "vacuumed" and rebuilds on "without falling", ending exactly as it began.
const Hook: React.FC = () => {
  const frame = useCurrentFrame();
  if (frame > F.hookOut + 8 && frame < F.hookBack) return null;
  const lines: { text: string; size: number; color: string }[] = [
    { text: "UPSIDE DOWN", size: 146, color: v2.colors.ink },
    { text: "AND NOT", size: 146, color: v2.colors.ink },
    { text: "FALLING?", size: 170, color: v2.colors.magenta },
  ];
  return (
    <div style={{ position: "absolute", left: 60, top: 128, ...HEADC }}>
      {lines.map((ln, i) => {
        const out = interpolate(frame, [F.hookOut - 4 + i * 2, F.hookOut + 4 + i * 2], [0, 1], { ...CLAMP, easing: Easing.in(Easing.cubic) });
        const back = interpolate(frame, [F.hookBack + i * 3, F.hookBack + 11 + i * 3], [0, 1], { ...CLAMP, easing: EASE_OUT });
        const shown = frame >= F.hookBack ? back : 1 - out;
        return (
          <div key={ln.text} style={{ fontSize: ln.size, color: ln.color, opacity: interpolate(shown, [0, 0.35], [0, 1], CLAMP),
            translate: `${(1 - shown) * -90}px ${(1 - shown) * -30}px`, ...keyline(ln.size / 150, 10) }}>
            {ln.text}
          </div>
        );
      })}
    </div>
  );
};

const Vacuumed: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame, fps, config: { damping: 11, stiffness: 220 } });
  const out = interpolate(frame, [F.diag - F.hookOut - 8, F.diag - F.hookOut], [0, 1], { ...CLAMP, easing: Easing.in(Easing.cubic) });
  return (
    <div style={{ position: "absolute", left: 0, right: 0, top: 250, textAlign: "center", ...HEADC, fontSize: 178,
      color: v2.colors.magenta, scale: interpolate(s, [0, 1], [1.7, 1]), opacity: interpolate(s, [0, 0.2], [0, 1], CLAMP) * (1 - out),
      translate: `0 ${-out * 120}px`, rotate: `${interpolate(s, [0, 1], [-7, -3])}deg`, ...keyline(1.25, 11) }}>
      VACUUMED
    </div>
  );
};

// ---------------------------------------------------------------------------------------- the diagram (3.8-19.3 s)
// Side view, car upside down under the ramp. No card or border: the lower half of the frame darkens into it.
const CEIL = { x0: 30, x1: 1050, y0: 800, y1: 840 };
const CAR = { x0: 250, x1: 830, floor: 900, belly: 990, roof: 1052 };
const GAP = { x0: CAR.x0, x1: CAR.x1, y0: CEIL.y1, y1: CAR.floor };
const FANS = [482, 604];

const Arrow: React.FC<{ x: number; y1: number; y2: number; p: number; color: string; w: number }> = ({ x, y1, y2, p, color, w }) => {
  if (p <= 0.001) return null;
  const y = y1 + (y2 - y1) * p;
  const dir = Math.sign(y2 - y1);
  const hs = 40;
  return (
    <g>
      <line x1={x} y1={y1} x2={x} y2={y - dir * hs * 0.6} stroke={v2.colors.black} strokeWidth={w + 10} strokeLinecap="round" />
      <line x1={x} y1={y1} x2={x} y2={y - dir * hs * 0.6} stroke={color} strokeWidth={w} strokeLinecap="round" />
      <polygon points={`${x},${y} ${x - hs * 0.62},${y - dir * hs} ${x + hs * 0.62},${y - dir * hs}`} fill={color}
        stroke={v2.colors.black} strokeWidth={5} strokeLinejoin="round" />
    </g>
  );
};

const LabelText: React.FC<{ text: string; x: number; y: number; color: string; show: number; size?: number; align?: "left" | "right" }> = ({
  text, x, y, color, show, size = 68, align = "left",
}) => (
  <div style={{ position: "absolute", top: y, ...(align === "left" ? { left: x } : { right: 1080 - x }), ...HEAD, fontSize: size,
    color, opacity: show, translate: `${(1 - show) * (align === "left" ? -24 : 24)}px 0`, ...keyline(size / 150, 9) }}>
    {text}
  </div>
);

const Diagram: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < F.diag || frame >= F.drop) return null;
  const at = (sec: number) => Math.round(sec * fps);
  const ease = (a: number, b: number) => interpolate(frame, [a, b], [0, 1], { ...CLAMP, easing: EASE_OUT });
  const region = interpolate(frame, [F.diag, F.diag + 12, F.diagOut, F.drop], [0, 1, 1, 0], CLAMP);
  const partA = 1 - interpolate(frame, [at(14.72), at(15.0)], [0, 1], CLAMP); // the car diagram, until "And unlike"
  const partB = interpolate(frame, [at(14.9), at(15.2)], [0, 1], CLAMP); // the wing-vs-fans bars

  // car diagram
  const ceil = ease(F.diag, F.diag + 12);
  const car = spring({ frame: frame - F.diag - 3, fps, config: { damping: 14, stiffness: 190 } });
  const spinUp = interpolate(frame, [F.diag, F.diag + 30], [0.15, 1], CLAMP);
  const fanAngle = frame * 26 * spinUp;
  const fansLbl = ease(F.diag + 2, F.diag + 12);
  const outArrows = ease(at(4.78), at(5.1));
  const skirtR = ease(at(7.4), at(7.4) + 8);
  const skirtF = ease(at(7.55), at(7.55) + 8);
  const skirtsLbl = ease(at(7.45), at(7.45) + 10);
  const sealFlash = interpolate(frame, [at(8.82), at(8.82) + 3, at(8.82) + 9], [0, 1, 0], CLAMP);
  const tint = ease(at(9.33), at(9.33) + 10);
  const push = interpolate(frame, [at(10.63), at(11.6)], [0, 1], { ...CLAMP, easing: EASE_OUT });
  const weight = ease(at(12.72), at(12.72) + 9);
  const badge = spring({ frame: frame - at(13.4), fps, config: { damping: 10, stiffness: 230 } });

  // particles: drawn out of the gap by the fans and blown out of the back, until the skirts seal it
  const parts: React.ReactNode[] = [];
  const born0 = at(4.0);
  const lastBorn = at(8.9);
  for (let k = 0; born0 + k * 3 <= lastBorn; k++) {
    const b = born0 + k * 3;
    const life = 30;
    const p = (frame - b) / life;
    if (p < 0 || p > 1) continue;
    const fromFront = k % 2 === 0;
    const lane = GAP.y0 + 12 + ((k * 9) % 36);
    const fx = fromFront ? FANS[1] : FANS[0];
    const ex = fromFront ? GAP.x1 + 40 : GAP.x0 - 40;
    let x: number;
    let y: number;
    if (p < 0.55) {
      x = interpolate(p, [0, 0.55], [ex, fx]);
      y = lane;
    } else if (p < 0.72) {
      x = fx;
      y = interpolate(p, [0.55, 0.72], [lane, CAR.floor + 26]);
    } else {
      x = interpolate(p, [0.72, 1], [fx, CAR.x0 - 120]);
      y = interpolate(p, [0.72, 1], [CAR.floor + 26, CAR.floor + 48]);
    }
    const op = interpolate(p, [0, 0.1, 0.85, 1], [0, 1, 1, 0], CLAMP);
    parts.push(<circle key={k} cx={x} cy={y} r={6} fill="#E4FFFD" opacity={op} />);
  }

  // bars: grip at standstill (shape of the relationship only: a wing's downforce falls with speed squared)
  const mph = Math.round(interpolate(frame, [at(16.8), at(18.12)], [100, 0], { ...CLAMP, easing: EASE_IN_OUT }));
  const wingRow = ease(at(15.35), at(15.35) + 10);
  const fanRow = ease(at(16.42), at(16.42) + 10);
  const lock = spring({ frame: frame - at(18.12), fps, config: { damping: 9, stiffness: 240 } });
  const pulse = frame >= at(18.12) ? interpolate(lock, [0, 1], [1.06, 1]) : 1;
  const track = { x0: 330, x1: 1010, h: 62 };
  const wingW = (track.x1 - track.x0) * 0.55 * (mph / 100) ** 2;

  return (
    <AbsoluteFill style={{ opacity: region }}>
      <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(6,3,18,0) 36%, rgba(6,3,18,0.95) 42.5%, rgba(6,3,18,0.97) 100%)" }} />

      <AbsoluteFill style={{ opacity: partA }}>
        <svg width={1080} height={1920} style={{ position: "absolute", inset: 0 }}>
          {/* the ramp, upside down above the car */}
          <rect x={540 - 510 * ceil} y={CEIL.y0} width={1020 * ceil} height={CEIL.y1 - CEIL.y0} fill="#8F99A3" stroke={v2.colors.black} strokeWidth={4} />
          <line x1={540 - 510 * ceil} y1={CEIL.y0 + 3} x2={540 + 510 * ceil} y2={CEIL.y0 + 3} stroke="#D3DAE0" strokeWidth={3} />
          {/* low-pressure gap */}
          <rect x={GAP.x0} y={GAP.y0} width={GAP.x1 - GAP.x0} height={GAP.y1 - GAP.y0} fill={v2.colors.cyan} opacity={0.24 * tint} />
          <g style={{ translate: `0 ${(1 - car) * 50}px` }} opacity={interpolate(car, [0, 0.3], [0, 1], CLAMP)}>
            {/* wheels touch the ramp */}
            {[372, 712].map((wx) => (
              <g key={wx}>
                <circle cx={wx} cy={CAR.floor - 2} r={58} fill="#3A414B" stroke={v2.colors.black} strokeWidth={5} />
                <circle cx={wx} cy={CAR.floor - 2} r={46} fill="none" stroke="#8C96A2" strokeWidth={4} />
                <circle cx={wx} cy={CAR.floor - 2} r={24} fill="#B9C2CC" stroke={v2.colors.black} strokeWidth={4} />
              </g>
            ))}
            {/* body and cabin, upside down: the floor faces the ramp, the roof faces the ground */}
            <rect x={CAR.x0} y={CAR.floor} width={CAR.x1 - CAR.x0} height={CAR.belly - CAR.floor} rx={30} fill="#EEF0F3" stroke={v2.colors.black} strokeWidth={5} />
            <path d={`M 400 ${CAR.belly - 2} L 700 ${CAR.belly - 2} L 646 ${CAR.roof} L 456 ${CAR.roof} Z`} fill="#3B4A61" stroke={v2.colors.black} strokeWidth={5} strokeLinejoin="round" />
            <path d={`M 414 ${CAR.belly + 3} L 686 ${CAR.belly + 3} L 638 ${CAR.roof - 7} L 462 ${CAR.roof - 7} Z`} fill="none" stroke="#A9B6C6" strokeWidth={3} />
            {/* fans in the floor */}
            {FANS.map((fx) => (
              <g key={fx} transform={`translate(${fx} ${CAR.floor + 8}) rotate(${fanAngle})`}>
                <circle r={32} fill="#0E1B22" stroke={v2.colors.cyan} strokeWidth={6} />
                {[0, 120, 240].map((a) => (
                  <path key={a} d="M 0 0 C 8 -10, 8 -23, 0 -28 C -5 -18, -8 -9, 0 0 Z" fill={v2.colors.cyan} transform={`rotate(${a})`} />
                ))}
              </g>
            ))}
          </g>
          {parts}
          {/* air leaving through the back */}
          {[CAR.floor + 22, CAR.floor + 54].map((ay, i) => (
            <g key={ay} opacity={outArrows} style={{ translate: `${(1 - outArrows) * 30}px 0` }}>
              <line x1={CAR.x0 - 22} y1={ay} x2={CAR.x0 - 110 + i * 10} y2={ay} stroke={v2.colors.black} strokeWidth={14} strokeLinecap="round" />
              <line x1={CAR.x0 - 22} y1={ay} x2={CAR.x0 - 110 + i * 10} y2={ay} stroke={v2.colors.cyan} strokeWidth={7} strokeLinecap="round" />
              <polygon points={`${CAR.x0 - 128 + i * 10},${ay} ${CAR.x0 - 104 + i * 10},${ay - 14} ${CAR.x0 - 104 + i * 10},${ay + 14}`} fill={v2.colors.cyan} stroke={v2.colors.black} strokeWidth={4} />
            </g>
          ))}
          {/* skirts seal the gap at both ends */}
          {[{ x: GAP.x0, p: skirtR }, { x: GAP.x1, p: skirtF }].map((sk) => (
            <rect key={sk.x} x={sk.x - 7} y={CAR.floor - (CAR.floor - GAP.y0) * sk.p} width={14} height={(CAR.floor - GAP.y0) * sk.p}
              fill={sealFlash > 0.5 ? v2.colors.ink : v2.colors.magenta} stroke={v2.colors.black} strokeWidth={3} />
          ))}
          {/* leaders */}
          <line x1={206} y1={(GAP.y0 + GAP.y1) / 2} x2={206 + (FANS[0] - 34 - 206) * fansLbl} y2={(GAP.y0 + GAP.y1) / 2} stroke={v2.colors.black} strokeWidth={12} strokeLinecap="round" opacity={fansLbl} />
          <line x1={206} y1={(GAP.y0 + GAP.y1) / 2} x2={206 + (FANS[0] - 34 - 206) * fansLbl} y2={(GAP.y0 + GAP.y1) / 2} stroke={v2.colors.cyan} strokeWidth={5} strokeLinecap="round" opacity={fansLbl} />
          <polyline points={`${GAP.x1 + 24},${1062} ${GAP.x1 + 24},${1062 - (1062 - (GAP.y0 + GAP.y1) / 2) * skirtsLbl} ${GAP.x1 + 8},${1062 - (1062 - (GAP.y0 + GAP.y1) / 2) * skirtsLbl}`}
            fill="none" stroke={v2.colors.magenta} strokeWidth={5} opacity={skirtsLbl} />
          {/* forces: the outside air pushes the car up into the ramp at twice the length of its weight */}
          <Arrow x={560} y1={1292} y2={CAR.roof + 4} p={push} color={v2.colors.cyan} w={22} />
          <Arrow x={352} y1={CAR.belly + 6} y2={CAR.belly + 126} p={weight} color={v2.colors.warn} w={18} />
        </svg>
        <LabelText text="FANS" x={30} y={(GAP.y0 + GAP.y1) / 2 - 34} color={v2.colors.cyan} show={fansLbl} />
        <LabelText text="SKIRTS" x={1046} y={1066} color={v2.colors.magenta} show={skirtsLbl} align="right" />
        <LabelText text="WEIGHT" x={322} y={1074} color={v2.colors.warn} show={weight} align="right" />
        <div style={{ position: "absolute", left: 604, top: 1128, padding: "10px 22px 12px", backgroundColor: v2.colors.acid,
          border: `5px solid ${v2.colors.black}`, ...HEAD, color: v2.colors.black, textAlign: "left",
          scale: badge, rotate: `${interpolate(badge, [0, 1], [-16, -3])}deg`, transformOrigin: "0% 50%" }}>
          <div style={{ fontSize: 72 }}>UP TO 2×</div>
          <div style={{ fontSize: 50, marginTop: 6 }}>ITS WEIGHT</div>
        </div>
      </AbsoluteFill>

      <AbsoluteFill style={{ opacity: partB }}>
        <div style={{ position: "absolute", right: 70, top: 800, display: "flex", alignItems: "baseline", gap: 14, ...HEAD }}>
          <span style={{ fontSize: 124, color: mph === 0 ? v2.colors.acid : v2.colors.ink, fontVariantNumeric: "tabular-nums",
            scale: mph === 0 ? interpolate(lock, [0, 1], [1.4, 1]) : 1, display: "inline-block", ...keyline(0.9, 9) }}>{mph}</span>
          <span style={{ fontSize: 58, color: v2.colors.cyan, ...keyline(0.5, 8) }}>MPH</span>
        </div>
        {[
          { label: "WING", color: "#C3CAD2", show: wingRow, w: wingW, top: 960 },
          { label: "FANS", color: v2.colors.cyan, show: fanRow, w: track.x1 - track.x0, top: 1110 },
        ].map((row) => (
          <div key={row.label} style={{ position: "absolute", left: 0, top: row.top, width: 1080, opacity: row.show,
            translate: `${(1 - row.show) * -40}px 0` }}>
            <div style={{ position: "absolute", left: 62, top: 0, ...HEAD, fontSize: 68, color: row.color, ...keyline(0.45, 9) }}>{row.label}</div>
            <div style={{ position: "absolute", left: track.x0, top: 4, width: track.x1 - track.x0, height: track.h, borderRadius: track.h / 2,
              backgroundColor: "rgba(255,255,255,0.10)", border: `4px solid ${v2.colors.black}` }} />
            <div style={{ position: "absolute", left: track.x0, top: 4, width: row.w, height: track.h, borderRadius: track.h / 2,
              backgroundColor: row.color, border: `4px solid ${v2.colors.black}`, transformOrigin: "0% 50%",
              scale: row.label === "FANS" ? `${pulse} ${pulse}` : "1 1" }} />
            {row.label === "FANS" ? (
              <div style={{ position: "absolute", left: track.x1 - 290, top: 12, ...HEAD, fontSize: 46, color: v2.colors.black }}>UP TO 2×</div>
            ) : null}
          </div>
        ))}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------------------------- jets callout (drop)
const JetCallout: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const at = (sec: number) => Math.round(sec * fps);
  const a = at(20.92);
  const b = at(22.32);
  if (frame < a || frame > b) return null;
  const keys = [a, at(21.52), at(22.02), b];
  const tx = interpolate(frame, keys, [565, 525, 500, 480], CLAMP);
  const ty = interpolate(frame, keys, [1290, 1370, 1440, 1470], CLAMP);
  const inn = interpolate(frame, [a, a + 7], [0, 1], { ...CLAMP, easing: EASE_OUT });
  const out = interpolate(frame, [b - 6, b], [1, 0], CLAMP);
  const t = ((frame - a) % 24) / 24;
  const lx = 60;
  const ly = 1180;
  return (
    <AbsoluteFill style={{ opacity: inn * out }}>
      <svg width={1080} height={1920} style={{ position: "absolute", inset: 0 }}>
        <polyline points={`${lx + 150},${ly + 92} ${lx + 150},${ty} ${tx - 58},${ty}`} fill="none" stroke={v2.colors.black} strokeWidth={13} strokeLinejoin="round" />
        <polyline points={`${lx + 150},${ly + 92} ${lx + 150},${ty} ${tx - 58},${ty}`} fill="none" stroke={v2.colors.cyan} strokeWidth={6} strokeLinejoin="round" />
        <circle cx={tx} cy={ty} r={52} fill="none" stroke={v2.colors.black} strokeWidth={14} />
        <circle cx={tx} cy={ty} r={52} fill="none" stroke={v2.colors.cyan} strokeWidth={7} />
        <circle cx={tx} cy={ty} r={52 + 40 * t} fill="none" stroke={v2.colors.cyan} strokeWidth={4} opacity={1 - t} />
      </svg>
      <div style={{ position: "absolute", left: lx, top: ly, ...HEAD, fontSize: 70, color: v2.colors.cyan, ...keyline(0.47, 9) }}>GAS JETS</div>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------------------------- captions
// Pages of up to 3 words that never run across a sentence or comma (createTikTokStyleCaptions joined "THE GAP. TESLA").
type Page = { startMs: number; durationMs: number; tokens: { text: string; fromMs: number; toMs: number }[] };
const PAGES: Page[] = (() => {
  const words: { text: string; fromMs: number; toMs: number }[] = [];
  for (const c of VO_S1_CAPTIONS) {
    const glued = !c.text.startsWith(" ") && words.length > 0;
    if (glued) {
      const w = words[words.length - 1];
      w.text += c.text;
      w.toMs = c.endMs;
    } else {
      words.push({ text: c.text, fromMs: c.startMs, toMs: c.endMs });
    }
  }
  const out: Page[] = [];
  let cur: Page | null = null;
  for (const w of words) {
    const len = cur ? cur.tokens.map((t) => t.text).join("").trim().length : 0;
    if (!cur || cur.tokens.length >= 3 || len + w.text.length > 16) {
      cur = { startMs: w.fromMs, durationMs: 0, tokens: [] };
      out.push(cur);
    }
    cur.tokens.push(w);
    cur.durationMs = w.toMs - cur.startMs;
    if (/[.,!?]$/.test(w.text.trim())) cur = null;
  }
  return out;
})();

const Captions: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < F.diag || frame >= F.hookBack) return null;
  const ms = (frame / fps) * 1000;
  const pages = PAGES;
  const page = pages.find((p, i) => ms >= p.startMs && ms < (pages[i + 1]?.startMs ?? p.startMs + p.durationMs + 400));
  if (!page) return null;
  const local = ms - page.startMs;
  const pop = interpolate(local, [0, 90, 160], [0.9, 1.05, 1], CLAMP);
  const top = frame < F.drop ? 1318 : 410;
  const startedIdx = page.tokens.reduce((acc, tk, j) => (tk.fromMs <= ms ? j : acc), -1);
  return (
    <div style={{ position: "absolute", left: 70, right: 140, top, textAlign: "center", ...HEAD, fontVariationSettings: "'wdth' 88", fontSize: 88, lineHeight: 1.04,
      textTransform: "uppercase", scale: pop }}>
      {page.tokens.map((t, i) => (
        <span key={t.fromMs} style={{ color: i === startedIdx ? v2.colors.acid : v2.colors.ink, ...keyline(0.6, 11) }}>{t.text}</span>
      ))}
    </div>
  );
};

// ---------------------------------------------------------------------------------------- credit
const Credit: React.FC = () => {
  const frame = useCurrentFrame();
  const opening = frame < F.diag || frame >= F.hookBack;
  const during = frame >= F.drop && frame < F.hookBack;
  if (!opening && !during) return null;
  const text = opening ? "FOOTAGE: TESLA · 20× SLOWER" : "FOOTAGE: TESLA · 15 OCT 2026";
  const top = opening ? 1342 : 128;
  return (
    <div style={{ position: "absolute", left: 0, top, padding: "10px 22px 10px 60px", backgroundColor: "rgba(0,0,0,0.74)",
      fontFamily: v2.fonts.mono, fontWeight: 500, fontSize: 40, letterSpacing: "0.03em", color: v2.colors.ink }}>
      {text}
    </div>
  );
};

export const CurveV2Short1: React.FC = () => {
  const { width, height, fps } = useVideoConfig();
  const u = unitFor(width, height);
  const at = (sec: number) => Math.round(sec * fps);
  return (
    <AbsoluteFill style={{ backgroundColor: v2.colors.black, fontSize: 40 * u }}>
      <Footage />
      <Diagram />
      <Sequence from={F.hookOut} durationInFrames={F.diag - F.hookOut}><Vacuumed /></Sequence>
      <JetCallout />
      <Hook />
      <Captions />
      <Credit />

      <Audio src={staticFile("shorts/s1_chris_v4.mp3")} />
      <Audio src={staticFile("audio/sample-bed.mp3")}
        volume={(f) => interpolate(f, [0, 9, SHORT1_FRAMES - 12, SHORT1_FRAMES], [0, 0.13, 0.13, 0], CLAMP)} />
      <Sequence from={F.hookOut}><Audio src={staticFile("sfx/thock.mp3")} volume={0.7} /></Sequence>
      <Sequence from={F.diag}><Audio src={staticFile("sfx/whoosh.mp3")} volume={0.4} /></Sequence>
      <Sequence from={at(7.4)}><Audio src={staticFile("sfx/form.mp3")} volume={0.4} /></Sequence>
      <Sequence from={at(8.82)}><Audio src={staticFile("sfx/thock.mp3")} volume={0.5} /></Sequence>
      <Sequence from={at(13.4)}><Audio src={staticFile("sfx/thock.mp3")} volume={0.7} /></Sequence>
      <Sequence from={at(16.8)} durationInFrames={at(1.32)}><Audio src={staticFile("sfx/tick_run.mp3")} volume={0.32} /></Sequence>
      <Sequence from={at(18.12)}><Audio src={staticFile("sfx/thock.mp3")} volume={0.6} /></Sequence>
      <Sequence from={F.drop}><Audio src={staticFile("sfx/whoosh.mp3")} volume={0.55} /></Sequence>
      <Sequence from={at(20.1)} durationInFrames={at(3.6)}><Audio src={staticFile("sfx/hiss.mp3")} volume={0.9} /></Sequence>
      <Sequence from={at(23.85)}><Audio src={staticFile("sfx/settle.mp3")} volume={0.8} /></Sequence>
      <Sequence from={F.rewind}><Audio src={staticFile("sfx/rewind.mp3")} volume={0.6} /></Sequence>
    </AbsoluteFill>
  );
};
