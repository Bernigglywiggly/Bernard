import { Audio, Video } from "@remotion/media";
import type React from "react";
import { AbsoluteFill, Easing, Img, interpolate, Sequence, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { CLAMP, EASE_IN_OUT, EASE_OUT } from "../lib/anim";
import { keyline } from "./HybridC";
import { v2 } from "./palette";
import { VO_S1_CAPTIONS } from "./voS1Captions";

// Roadster Short 1, v2 (18 Oct 2026): "How the Tesla Roadster Hangs Upside Down". 1080x1920, 30 fps.
// Built natively in 9:16 from Tesla's 4K Ramp upload (crop 1215x2160 at x 1450, no upscale); RIFE v4.6 makes the 20x
// slow motion and the true-30 fps drop. v2 applies critic round 1 (shorts/out/critic/round1.md): no overlap in the
// swipe window and the voice pause cut to 0.2 s (every later cue 10 frames earlier), a sourced second fact as the
// payoff (the Chaparral 2J, banned after 1970), nothing right of x 940 at 45-90% height, bars without invented
// numbers (Moravy's 0-50 mph), footage moving under the diagram, slides instead of crossfades, a ground cue at frame 0.
// The last frame is frame 0, so the replay has no seam. Narration: shorts/vo/s1_chris_v4_cut.mp3 (31.8 s).
// Facts: TESLA_ROADSTER_FACTS.md P1 P2 P10 S3 S5, §13.1 #24 (U28), §13.2 (Chaparral 2J).

export const SHORT1_FRAMES = 988;

const SHIFT = 10; // frames cut from the pause after line 1
const F = {
  hookOut: 58,
  vac: 60, // "vacuumed" 2.02 s
  diag: 103, // "Fans" 3.44 s
  diagOut: 560,
  drop: 570, // "Then" 19.00 s, on the bed's downbeat
  dropEnd: 724, // the drop clip ends (154 frames)
  card: 735, // "Racing" 24.50 s
  banned: 764, // "banned" 25.48 s
  sucks: 891, // "used fans" 29.71 s
  rewind: 905, // on the beat
  hookRev: 936,
  hookBack: 966,
  hold0: 986,
};

const ORIGIN_HOOK = "42% 30%";
const ORIGIN_DROP = "40% 58%";
const S0 = 1.45; // frame-0 scale: the car fills about 26% of the width and sits below the hook

const camera = (f: number) => {
  if (f < F.diag) return { s: interpolate(f, [0, F.diag], [S0, S0 + 0.04], CLAMP), ty: 0, o: ORIGIN_HOOK };
  if (f < F.diagOut) {
    const k = interpolate(f, [F.diag, F.diag + 16], [0, 1], { ...CLAMP, easing: EASE_IN_OUT });
    const push = interpolate(f, [F.diag + 16, F.diagOut], [1, 1.05], CLAMP);
    return { s: interpolate(k, [0, 1], [S0 + 0.04, 1]) * push, ty: interpolate(k, [0, 1], [0, -384]), o: ORIGIN_HOOK };
  }
  if (f < F.drop) {
    const k = interpolate(f, [F.diagOut, F.drop], [0, 1], { ...CLAMP, easing: EASE_IN_OUT });
    return { s: interpolate(k, [0, 1], [1.05, 1]), ty: interpolate(k, [0, 1], [-384, 0]), o: ORIGIN_HOOK };
  }
  if (f < F.card) return { s: interpolate(f, [F.drop, F.dropEnd], [1, 1.06], CLAMP), ty: 0, o: ORIGIN_DROP };
  if (f < F.hookRev) return { s: 1, ty: 0, o: ORIGIN_DROP };
  const k = interpolate(f, [F.hookRev, F.hold0], [0, 1], { ...CLAMP, easing: EASE_IN_OUT });
  return { s: interpolate(k, [0, 1], [1, S0]), ty: 0, o: ORIGIN_HOOK };
};

const GRADE = "saturate(1.12) contrast(1.06) brightness(1.06)";
const fill: React.CSSProperties = { width: "100%", height: "100%", filter: GRADE };
const BG = "radial-gradient(ellipse at 50% 40%, #1B0B3A 0%, #0A0418 55%, #000000 100%)";

const Footage: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const c = camera(frame);
  const ping = F.drop - 125;
  return (
    <AbsoluteFill style={{ overflow: "hidden", backgroundColor: v2.colors.black }}>
      <AbsoluteFill style={{ scale: c.s, translate: `0 ${c.ty}px`, transformOrigin: c.o }}>
        <Sequence durationInFrames={125} premountFor={fps}>
          <Video src={staticFile("shorts/s1_hook_20x.mp4")} muted style={fill} />
        </Sequence>
        {/* under the diagram: the 20x hang plays back and forth and ends on the drop's first frame */}
        <Sequence from={125} durationInFrames={ping} premountFor={fps}>
          <Video src={staticFile("shorts/s1_hook_pingpong.mp4")} muted playbackRate={500 / ping} style={fill} />
        </Sequence>
        <Sequence from={F.drop} durationInFrames={F.dropEnd - F.drop} premountFor={fps}>
          <Video src={staticFile("shorts/s1_drop.mp4")} muted style={fill} />
        </Sequence>
        <Sequence from={F.dropEnd} durationInFrames={F.card - F.dropEnd}>
          <Img src={staticFile("shorts/s1_drop_last.png")} style={fill} />
        </Sequence>
        <Sequence from={F.rewind} durationInFrames={F.hookRev - F.rewind} premountFor={fps}>
          <Video src={staticFile("shorts/s1_drop_rev5x.mp4")} muted style={fill} />
        </Sequence>
        <Sequence from={F.hookRev} durationInFrames={F.hold0 - F.hookRev} premountFor={fps}>
          <Video src={staticFile("shorts/s1_hook_20x_rev.mp4")} muted playbackRate={2.5} style={fill} />
        </Sequence>
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

// shown: 1 at frame 0, gone by frame 58 (before VACUUMED), rebuilt from frame 966 so the last frame is frame 0
const openingShown = (frame: number, stagger: number) => {
  if (frame >= F.hookBack) {
    return interpolate(frame, [F.hookBack + stagger * 3, F.hookBack + 11 + stagger * 3], [0, 1], { ...CLAMP, easing: EASE_OUT });
  }
  return 1 - interpolate(frame, [F.hookOut - 10 + stagger * 2, F.hookOut - 4 + stagger * 2], [0, 1], { ...CLAMP, easing: Easing.in(Easing.cubic) });
};

const Hook: React.FC = () => {
  const frame = useCurrentFrame();
  if (frame >= F.hookOut && frame < F.hookBack) return null;
  const lines = [
    { text: "UPSIDE DOWN", size: 146, color: v2.colors.ink },
    { text: "AND NOT", size: 146, color: v2.colors.ink },
    { text: "FALLING?", size: 170, color: v2.colors.magenta },
  ];
  return (
    <div style={{ position: "absolute", left: 60, top: 128, ...HEADC }}>
      {lines.map((ln, i) => {
        const shown = openingShown(frame, i);
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

// Which way is down: without it the car reads as stuck sideways on a wall (critic round 1).
const GroundCue: React.FC = () => {
  const frame = useCurrentFrame();
  if (frame >= F.hookOut && frame < F.hookBack) return null;
  const shown = openingShown(frame, 2);
  return (
    <div style={{ position: "absolute", left: 690, top: 930, opacity: interpolate(shown, [0, 0.35], [0, 1], CLAMP),
      translate: `0 ${(1 - shown) * 40}px`, display: "flex", flexDirection: "column", alignItems: "center" }}>
      <svg width={80} height={190} viewBox="0 0 80 190">
        <line x1={40} y1={6} x2={40} y2={150} stroke={v2.colors.black} strokeWidth={22} strokeLinecap="round" />
        <line x1={40} y1={6} x2={40} y2={150} stroke={v2.colors.ink} strokeWidth={11} strokeLinecap="round" />
        <polygon points="40,186 10,136 70,136" fill={v2.colors.ink} stroke={v2.colors.black} strokeWidth={6} strokeLinejoin="round" />
      </svg>
      <div style={{ ...HEADC, fontSize: 56, color: v2.colors.ink, marginTop: 4, ...keyline(0.4, 9) }}>GROUND</div>
    </div>
  );
};

const Vacuumed: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame, fps, config: { damping: 11, stiffness: 220 } });
  const out = interpolate(frame, [F.diag - F.vac - 8, F.diag - F.vac], [0, 1], { ...CLAMP, easing: Easing.in(Easing.cubic) });
  return (
    <div style={{ position: "absolute", left: 0, right: 0, top: 250, textAlign: "center", ...HEADC, fontSize: 178,
      color: v2.colors.magenta, scale: interpolate(s, [0, 1], [1.7, 1]), opacity: interpolate(s, [0, 0.2], [0, 1], CLAMP) * (1 - out),
      translate: `0 ${-out * 120}px`, rotate: `${interpolate(s, [0, 1], [-7, -3])}deg`, ...keyline(1.25, 11) }}>
      VACUUMED
    </div>
  );
};

// ---------------------------------------------------------------------------------------- the diagram (3.4-19.0 s)
const CEIL = { y0: 800, y1: 840 };
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
  <div style={{ position: "absolute", top: y, ...(align === "left" ? { left: x } : { right: 1080 - x }), ...HEADC, fontSize: size,
    color, opacity: show, translate: `${(1 - show) * (align === "left" ? -24 : 24)}px 0`, ...keyline(size / 150, 9) }}>
    {text}
  </div>
);

const FanGlyph: React.FC<{ x: number; y: number; angle: number; r?: number }> = ({ x, y, angle, r = 32 }) => (
  <g transform={`translate(${x} ${y}) rotate(${angle})`}>
    <circle r={r} fill="#0E1B22" stroke={v2.colors.cyan} strokeWidth={6} />
    {[0, 120, 240].map((a) => (
      <path key={a} d={`M 0 0 C ${r * 0.25} ${-r * 0.31}, ${r * 0.25} ${-r * 0.72}, 0 ${-r * 0.88} C ${-r * 0.16} ${-r * 0.56}, ${-r * 0.25} ${-r * 0.28}, 0 0 Z`}
        fill={v2.colors.cyan} transform={`rotate(${a})`} />
    ))}
  </g>
);

const Diagram: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < F.diag || frame >= F.drop) return null;
  const cue = (sec: number) => Math.round(sec * fps) - SHIFT; // cue times written in the v1 narration's seconds
  const ease = (a: number, b: number) => interpolate(frame, [a, b], [0, 1], { ...CLAMP, easing: EASE_OUT });
  // slides, not crossfades: the region rises with the camera tilt and drops away before the cut to the drop
  const rise = interpolate(frame, [F.diag, F.diag + 10], [1, 0], { ...CLAMP, easing: EASE_OUT });
  const sink = interpolate(frame, [F.diagOut, F.drop], [0, 1], { ...CLAMP, easing: Easing.in(Easing.cubic) });
  const swap = frame >= cue(14.72); // hard cut from the car diagram to the bars on "And unlike"

  const ceil = ease(F.diag, F.diag + 12);
  const car = spring({ frame: frame - F.diag - 3, fps, config: { damping: 14, stiffness: 190 } });
  const spinUp = interpolate(frame, [F.diag, F.diag + 30], [0.15, 1], CLAMP);
  const fanAngle = frame * 26 * spinUp;
  const fansLbl = ease(F.diag + 2, F.diag + 12);
  const outArrows = ease(cue(4.78), cue(5.1));
  const skirtR = ease(cue(7.4), cue(7.4) + 8);
  const skirtF = ease(cue(7.55), cue(7.55) + 8);
  const skirtsLbl = ease(cue(7.45), cue(7.45) + 10);
  const sealFlash = interpolate(frame, [cue(8.82), cue(8.82) + 3, cue(8.82) + 9], [0, 1, 0], CLAMP);
  const tint = ease(cue(9.33), cue(9.33) + 10);
  const push = interpolate(frame, [cue(10.63), cue(11.6)], [0, 1], { ...CLAMP, easing: EASE_OUT });
  const weight = ease(cue(12.72), cue(12.72) + 9);
  const badge = spring({ frame: frame - cue(13.4), fps, config: { damping: 10, stiffness: 230 } });

  const parts: React.ReactNode[] = [];
  const born0 = cue(4.0);
  const lastBorn = cue(8.9);
  for (let k = 0; born0 + k * 3 <= lastBorn; k++) {
    const b = born0 + k * 3;
    const p = (frame - b) / 30;
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
    parts.push(<circle key={k} cx={x} cy={y} r={6} fill="#E4FFFD" opacity={interpolate(p, [0, 0.1, 0.85, 1], [0, 1, 1, 0], CLAMP)} />);
  }

  // bars: grip at standstill. Moravy: from 0 to 50 mph "wings do nothing" while the fans hold over 2 g (U28).
  // Shapes only, no scale: a wing's downforce falls with speed squared, the fans don't care.
  const mph = Math.round(interpolate(frame, [cue(16.8), cue(18.12)], [50, 0], { ...CLAMP, easing: EASE_IN_OUT }));
  const wingRow = ease(cue(15.35), cue(15.35) + 10);
  const fanRow = ease(cue(16.42), cue(16.42) + 10);
  const lock = spring({ frame: frame - cue(18.12), fps, config: { damping: 9, stiffness: 240 } });
  const pulse = frame >= cue(18.12) ? interpolate(lock, [0, 1], [1.06, 1]) : 1;
  const track = { x0: 330, x1: 930, h: 62 };
  const wingW = (track.x1 - track.x0) * 0.07 * (mph / 50) ** 2;

  return (
    <AbsoluteFill style={{ translate: `0 ${(rise + sink) * 1100}px` }}>
      <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(6,3,18,0) 36%, rgba(6,3,18,0.95) 42.5%, rgba(6,3,18,0.97) 100%)" }} />

      {!swap ? (
        <AbsoluteFill>
          <svg width={1080} height={1920} style={{ position: "absolute", inset: 0 }}>
            <rect x={540 - 510 * ceil} y={CEIL.y0} width={1020 * ceil} height={CEIL.y1 - CEIL.y0} fill="#8F99A3" stroke={v2.colors.black} strokeWidth={4} />
            <line x1={540 - 510 * ceil} y1={CEIL.y0 + 3} x2={540 + 510 * ceil} y2={CEIL.y0 + 3} stroke="#D3DAE0" strokeWidth={3} />
            <rect x={GAP.x0} y={GAP.y0} width={GAP.x1 - GAP.x0} height={GAP.y1 - GAP.y0} fill={v2.colors.cyan} opacity={0.24 * tint} />
            <g style={{ translate: `0 ${(1 - car) * 50}px` }} opacity={interpolate(car, [0, 0.3], [0, 1], CLAMP)}>
              {[372, 712].map((wx) => (
                <g key={wx}>
                  <circle cx={wx} cy={CAR.floor - 2} r={58} fill="#3A414B" stroke={v2.colors.black} strokeWidth={5} />
                  <circle cx={wx} cy={CAR.floor - 2} r={46} fill="none" stroke="#8C96A2" strokeWidth={4} />
                  <circle cx={wx} cy={CAR.floor - 2} r={24} fill="#B9C2CC" stroke={v2.colors.black} strokeWidth={4} />
                </g>
              ))}
              <rect x={CAR.x0} y={CAR.floor} width={CAR.x1 - CAR.x0} height={CAR.belly - CAR.floor} rx={30} fill="#EEF0F3" stroke={v2.colors.black} strokeWidth={5} />
              <path d={`M 400 ${CAR.belly - 2} L 700 ${CAR.belly - 2} L 646 ${CAR.roof} L 456 ${CAR.roof} Z`} fill="#3B4A61" stroke={v2.colors.black} strokeWidth={5} strokeLinejoin="round" />
              <path d={`M 414 ${CAR.belly + 3} L 686 ${CAR.belly + 3} L 638 ${CAR.roof - 7} L 462 ${CAR.roof - 7} Z`} fill="none" stroke="#A9B6C6" strokeWidth={3} />
              {FANS.map((fx) => <FanGlyph key={fx} x={fx} y={CAR.floor + 8} angle={fanAngle} />)}
            </g>
            {parts}
            {[CAR.floor + 22, CAR.floor + 54].map((ay, i) => (
              <g key={ay} opacity={outArrows} style={{ translate: `${(1 - outArrows) * 30}px 0` }}>
                <line x1={CAR.x0 - 22} y1={ay} x2={CAR.x0 - 110 + i * 10} y2={ay} stroke={v2.colors.black} strokeWidth={14} strokeLinecap="round" />
                <line x1={CAR.x0 - 22} y1={ay} x2={CAR.x0 - 110 + i * 10} y2={ay} stroke={v2.colors.cyan} strokeWidth={7} strokeLinecap="round" />
                <polygon points={`${CAR.x0 - 128 + i * 10},${ay} ${CAR.x0 - 104 + i * 10},${ay - 14} ${CAR.x0 - 104 + i * 10},${ay + 14}`} fill={v2.colors.cyan} stroke={v2.colors.black} strokeWidth={4} />
              </g>
            ))}
            {[{ x: GAP.x0, p: skirtR }, { x: GAP.x1, p: skirtF }].map((sk) => (
              <rect key={sk.x} x={sk.x - 7} y={CAR.floor - (CAR.floor - GAP.y0) * sk.p} width={14} height={(CAR.floor - GAP.y0) * sk.p}
                fill={sealFlash > 0.5 ? v2.colors.ink : v2.colors.magenta} stroke={v2.colors.black} strokeWidth={3} />
            ))}
            <line x1={206} y1={(GAP.y0 + GAP.y1) / 2} x2={206 + (FANS[0] - 34 - 206) * fansLbl} y2={(GAP.y0 + GAP.y1) / 2} stroke={v2.colors.black} strokeWidth={12} strokeLinecap="round" opacity={fansLbl} />
            <line x1={206} y1={(GAP.y0 + GAP.y1) / 2} x2={206 + (FANS[0] - 34 - 206) * fansLbl} y2={(GAP.y0 + GAP.y1) / 2} stroke={v2.colors.cyan} strokeWidth={5} strokeLinecap="round" opacity={fansLbl} />
            <polyline points={`${GAP.x1 + 24},${1062} ${GAP.x1 + 24},${1062 - (1062 - (GAP.y0 + GAP.y1) / 2) * skirtsLbl} ${GAP.x1 + 8},${1062 - (1062 - (GAP.y0 + GAP.y1) / 2) * skirtsLbl}`}
              fill="none" stroke={v2.colors.magenta} strokeWidth={5} opacity={skirtsLbl} />
            <Arrow x={500} y1={1292} y2={CAR.roof + 4} p={push} color={v2.colors.cyan} w={22} />
            <Arrow x={352} y1={CAR.belly + 6} y2={CAR.belly + 126} p={weight} color={v2.colors.warn} w={18} />
          </svg>
          <LabelText text="FANS" x={30} y={(GAP.y0 + GAP.y1) / 2 - 34} color={v2.colors.cyan} show={fansLbl} />
          <LabelText text="SKIRTS" x={930} y={1066} color={v2.colors.magenta} show={skirtsLbl} align="right" />
          <LabelText text="WEIGHT" x={322} y={1074} color={v2.colors.warn} show={weight} align="right" />
          <div style={{ position: "absolute", left: 556, top: 1150, padding: "8px 20px 10px", backgroundColor: v2.colors.acid,
            border: `5px solid ${v2.colors.black}`, ...HEADC, color: v2.colors.black, scale: badge,
            rotate: `${interpolate(badge, [0, 1], [-16, -3])}deg`, transformOrigin: "0% 50%" }}>
            <div style={{ fontSize: 64 }}>UP TO 2×</div>
            <div style={{ fontSize: 48, marginTop: 6 }}>ITS WEIGHT</div>
          </div>
        </AbsoluteFill>
      ) : (
        <AbsoluteFill>
          <div style={{ position: "absolute", right: 150, top: 800, display: "flex", alignItems: "baseline", gap: 14, ...HEADC }}>
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
              <div style={{ position: "absolute", left: 62, top: 0, ...HEADC, fontSize: 68, color: row.color, ...keyline(0.45, 9) }}>{row.label}</div>
              <div style={{ position: "absolute", left: track.x0, top: 4, width: track.x1 - track.x0, height: track.h, borderRadius: track.h / 2,
                backgroundColor: "rgba(255,255,255,0.10)", border: `4px solid ${v2.colors.black}` }} />
              <div style={{ position: "absolute", left: track.x0, top: 4, width: Math.max(row.w, 0), height: track.h, borderRadius: track.h / 2,
                backgroundColor: row.color, border: row.w > 6 ? `4px solid ${v2.colors.black}` : "none", transformOrigin: "0% 50%",
                scale: row.label === "FANS" ? `${pulse} ${pulse}` : "1 1" }} />
            </div>
          ))}
        </AbsoluteFill>
      )}
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------------------------- the second fact (24.5-30.2 s)
// Racing officials banned the same trick after 1970: the Chaparral 2J (two rear fans, sealed skirts). Drawn, generic.
const Chaparral: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < F.card || frame >= F.rewind) return null;
  const year = spring({ frame: frame - F.card, fps, config: { damping: 14, stiffness: 200 } });
  const car = spring({ frame: frame - F.card - 4, fps, config: { damping: 15, stiffness: 180 } });
  const name = interpolate(frame, [F.card + 8, F.card + 18], [0, 1], { ...CLAMP, easing: EASE_OUT });
  const stamp = spring({ frame: frame - F.banned, fps, config: { damping: 9, stiffness: 260 } });
  const suck = interpolate(frame, [F.sucks, F.sucks + 14], [0, 1], { ...CLAMP, easing: EASE_OUT });
  const fanAngle = frame * interpolate(frame, [F.card, F.sucks, F.sucks + 10], [10, 10, 30], CLAMP);
  const push = interpolate(frame, [F.card, F.rewind], [1, 1.05], CLAMP);
  const ground = 990;
  return (
    <AbsoluteFill style={{ background: BG }}>
      <AbsoluteFill style={{ scale: push, transformOrigin: "50% 45%" }}>
        <div style={{ position: "absolute", left: 64, top: 180, ...HEADC, fontSize: 280, color: v2.colors.acid, lineHeight: 0.86,
          scale: interpolate(year, [0, 1], [0.7, 1]), opacity: interpolate(year, [0, 0.25], [0, 1], CLAMP), transformOrigin: "0% 50%",
          ...keyline(1.9, 10) }}>1970</div>
        <svg width={1080} height={1920} style={{ position: "absolute", inset: 0, translate: `${(1 - car) * 300}px 0`,
          opacity: interpolate(car, [0, 0.3], [0, 1], CLAMP) }}>
          <line x1={40} y1={ground + 2} x2={1040} y2={ground + 2} stroke="#5E6670" strokeWidth={6} />
          {/* outside air pushing the car down once the fans pull the air from under it */}
          {[300, 470, 640].map((ax) => (
            <Arrow key={ax} x={ax} y1={640} y2={772} p={suck} color={v2.colors.cyan} w={16} />
          ))}
          {/* generic 1970 Can-Am body: low wedge nose, cockpit bump, tall rear box that houses two fans */}
          <path d={`M 170 ${ground - 40} L 330 ${ground - 120} L 620 ${ground - 132} L 640 ${ground - 196} L 900 ${ground - 196} L 900 ${ground - 40} Z`}
            fill="#F2F3F5" stroke={v2.colors.black} strokeWidth={6} strokeLinejoin="round" />
          <path d={`M 420 ${ground - 126} Q 470 ${ground - 176} 540 ${ground - 130} Z`} fill="#3B4A61" stroke={v2.colors.black} strokeWidth={5} />
          {[300, 790].map((wx) => (
            <g key={wx}>
              <circle cx={wx} cy={ground - 48} r={52} fill="#3A414B" stroke={v2.colors.black} strokeWidth={5} />
              <circle cx={wx} cy={ground - 48} r={22} fill="#B9C2CC" stroke={v2.colors.black} strokeWidth={4} />
            </g>
          ))}
          {/* skirts sealing the floor to the ground */}
          <rect x={360} y={ground - 40} width={380} height={40} fill={v2.colors.magenta} stroke={v2.colors.black} strokeWidth={4} />
          <FanGlyph x={705} y={ground - 130} angle={fanAngle} r={44} />
          <FanGlyph x={830} y={ground - 130} angle={fanAngle + 40} r={44} />
          {/* air leaving out of the back of the fans */}
          {[ground - 150, ground - 110].map((ay) => (
            <g key={ay} opacity={suck}>
              <line x1={910} y1={ay} x2={1000} y2={ay} stroke={v2.colors.black} strokeWidth={14} strokeLinecap="round" />
              <line x1={910} y1={ay} x2={1000} y2={ay} stroke={v2.colors.cyan} strokeWidth={7} strokeLinecap="round" />
            </g>
          ))}
        </svg>
        <div style={{ position: "absolute", left: 64, top: 1030, ...HEADC, fontSize: 88, color: v2.colors.ink, opacity: name,
          translate: `${(1 - name) * -40}px 0`, ...keyline(0.6, 10) }}>CHAPARRAL 2J</div>
        <div style={{ position: "absolute", left: 470, top: 470, padding: "10px 24px 12px", border: `12px solid ${v2.colors.warn}`,
          color: v2.colors.warn, ...HEADC, fontSize: 130, backgroundColor: "rgba(0,0,0,0.6)", rotate: "-9deg",
          scale: interpolate(stamp, [0, 1], [1.9, 1]), opacity: interpolate(stamp, [0, 0.2], [0, 1], CLAMP) }}>BANNED</div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------------------------- jets callout (drop)
const JetCallout: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const cue = (sec: number) => Math.round(sec * fps) - SHIFT;
  const a = cue(20.92);
  const b = cue(22.32);
  if (frame < a || frame > b) return null;
  const keys = [a, cue(21.52), cue(22.02), b];
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
      <div style={{ position: "absolute", left: lx, top: ly, ...HEADC, fontSize: 70, color: v2.colors.cyan, ...keyline(0.47, 9) }}>GAS JETS</div>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------------------------- captions
// Pages of up to 3 words, at most 16 characters, never across a sentence or comma, never ending on "the" or "a".
type Word = { text: string; fromMs: number; toMs: number };
type Page = { startMs: number; durationMs: number; tokens: Word[] };
const STOP = new Set(["the", "a", "an", "to", "of", "and", "with", "from", "in", "it"]);
const PAGES: Page[] = (() => {
  const words: Word[] = [];
  for (const c of VO_S1_CAPTIONS) {
    if (!c.text.startsWith(" ") && words.length > 0) {
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
      const carry: Word[] = [];
      if (cur && cur.tokens.length > 1 && STOP.has(cur.tokens[cur.tokens.length - 1].text.trim().toLowerCase())) {
        carry.push(cur.tokens.pop() as Word);
        cur.durationMs = cur.tokens[cur.tokens.length - 1].toMs - cur.startMs;
      }
      cur = { startMs: carry.length ? carry[0].fromMs : w.fromMs, durationMs: 0, tokens: carry };
      out.push(cur);
    }
    cur.tokens.push(w);
    cur.durationMs = w.toMs - cur.startMs;
    if (/[.,!?]$/.test(w.text.trim()) && !/^\s*\d+\.$/.test(w.text)) cur = null;
  }
  return out;
})();

const captionTop = (f: number) => (f < F.drop ? 1318 : f < F.card ? 410 : f < F.rewind ? 1318 : 410);

const Captions: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < F.diag || frame >= F.hookBack) return null;
  const ms = (frame / fps) * 1000;
  const page = PAGES.find((p, i) => ms >= p.startMs && ms < (PAGES[i + 1]?.startMs ?? p.startMs + p.durationMs + 400));
  if (!page) return null;
  const pop = interpolate(ms - page.startMs, [0, 90, 160], [0.9, 1.05, 1], CLAMP);
  const startedIdx = page.tokens.reduce((acc, tk, j) => (tk.fromMs <= ms ? j : acc), -1);
  return (
    <div style={{ position: "absolute", left: 70, right: 140, top: captionTop(frame), textAlign: "center", ...HEAD,
      fontVariationSettings: "'wdth' 88", fontSize: 88, lineHeight: 1.04, textTransform: "uppercase", scale: pop }}>
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
  const during = frame >= F.drop && frame < F.card;
  if (!opening && !during) return null;
  const text = opening ? "FOOTAGE: TESLA / YOUTUBE · 20× SLOWER" : "FOOTAGE: TESLA / YOUTUBE · 15 OCT 2026";
  return (
    <div style={{ position: "absolute", left: 0, top: opening ? 1342 : 128, padding: "10px 22px 10px 60px", backgroundColor: "rgba(0,0,0,0.74)",
      fontFamily: v2.fonts.mono, fontWeight: 500, fontSize: 40, letterSpacing: "0.02em", color: v2.colors.ink }}>
      {text}
    </div>
  );
};

export const CurveV2Short1: React.FC = () => {
  const { fps } = useVideoConfig();
  const cue = (sec: number) => Math.round(sec * fps) - SHIFT;
  return (
    <AbsoluteFill style={{ backgroundColor: v2.colors.black }}>
      <Footage />
      <Diagram />
      <Chaparral />
      <Sequence from={F.vac} durationInFrames={F.diag - F.vac}><Vacuumed /></Sequence>
      <JetCallout />
      <Hook />
      <GroundCue />
      <Captions />
      <Credit />

      <Audio src={staticFile("shorts/s1_chris_v4_cut.mp3")} />
      {/* the bed starts 10 frames in, so its beat grid moves with the cut */}
      <Audio src={staticFile("audio/sample-bed.mp3")} trimBefore={SHIFT}
        volume={(f) => interpolate(f, [0, 4, SHORT1_FRAMES - 5, SHORT1_FRAMES], [0, 0.13, 0.13, 0], CLAMP)} />
      <Sequence from={F.vac}><Audio src={staticFile("sfx/thock.mp3")} volume={0.7} /></Sequence>
      <Sequence from={F.diag}><Audio src={staticFile("sfx/whoosh.mp3")} volume={0.4} /></Sequence>
      <Sequence from={cue(7.4)}><Audio src={staticFile("sfx/form.mp3")} volume={0.4} /></Sequence>
      <Sequence from={cue(8.82)}><Audio src={staticFile("sfx/thock.mp3")} volume={0.5} /></Sequence>
      <Sequence from={cue(13.4)}><Audio src={staticFile("sfx/thock.mp3")} volume={0.7} /></Sequence>
      <Sequence from={cue(16.8)} durationInFrames={40}><Audio src={staticFile("sfx/tick_run.mp3")} volume={0.32} /></Sequence>
      <Sequence from={cue(18.12)}><Audio src={staticFile("sfx/thock.mp3")} volume={0.6} /></Sequence>
      <Sequence from={F.drop}><Audio src={staticFile("sfx/whoosh.mp3")} volume={0.55} /></Sequence>
      <Sequence from={cue(20.1)} durationInFrames={108}><Audio src={staticFile("sfx/hiss.mp3")} volume={0.9} /></Sequence>
      <Sequence from={cue(23.85)}><Audio src={staticFile("sfx/settle.mp3")} volume={0.8} /></Sequence>
      <Sequence from={F.card}><Audio src={staticFile("sfx/whoosh.mp3")} volume={0.45} /></Sequence>
      <Sequence from={F.banned}><Audio src={staticFile("sfx/thock.mp3")} volume={0.8} /></Sequence>
      <Sequence from={F.sucks}><Audio src={staticFile("sfx/form.mp3")} volume={0.4} /></Sequence>
      <Sequence from={F.rewind}><Audio src={staticFile("sfx/rewind.mp3")} volume={0.6} /></Sequence>
    </AbsoluteFill>
  );
};
