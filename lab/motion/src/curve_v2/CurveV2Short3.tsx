import { Audio, Video } from "@remotion/media";
import type React from "react";
import { AbsoluteFill, Easing, Img, interpolate, Sequence, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { CLAMP, EASE_IN_OUT, EASE_OUT } from "../lib/anim";
import { keyline } from "./HybridC";
import { makePages } from "./pager";
import { v2 } from "./palette";
import { VO_S3_CAPTIONS } from "./voS3Captions";

// Roadster Short 3, v2 (for Tue 20 Oct): "How Long Can the Tesla Roadster Fly?". 1080x1920, 30 fps.
// v2 applies critic round 1 (shorts/out/critic_s3/round1.md): opens and loops on the side-on hover (Tesla's "The Kickflip"
// upload, r5vsHHPVhJg 0:32-0:35, RIFE, about 10x slower), line 3 re-voiced as "By our estimate" (whisper heard "maps"),
// tanks labelled and drawn 2:1 (400 L seat tank, 200 L rear tank), the hover estimate on screen (8-11 s at best),
// UNPROVEN stamped on the self-refill claim, captions hidden under the 2-6 HOURS block, hard cuts on the bed's beat.
// Numbers: TESLA_ROADSTER_FACTS.md P1 (two COPVs, about 250 kg), S1/S13 (200 L rear + 400 L seat), §5 (about 2 s at
// 80 kN and 8-11 s hovering: OUR ESTIMATE), S1 (one launch per fill; 2-6 h from a nitrogen rig), P1 12:30 (Musk).
// Narration lab/curve_v2/shorts/vo/s3_chris_v4_v2.mp3 (31.9 s). Last frame = frame 0.

export const SHORT3_FRAMES = 960;

// cuts sit on beats of the 124 BPM bed (one beat = 14.52 frames)
const F = { hookOut: 88, xray: 175, gauge: 319, drain: 392, quote: 465, clock: 596, rigLabel: 702, split: 755, musk: 791, stamp: 868, eng: 880, rewind: 929, hookBack: 940, hold0: 958 };

const HEAD: React.CSSProperties = { fontFamily: v2.fonts.heavy, fontWeight: 900, letterSpacing: "-0.02em", lineHeight: 0.9 };
const HEADC: React.CSSProperties = { ...HEAD, fontVariationSettings: "'wdth' 82", whiteSpace: "nowrap" };
const BG = "radial-gradient(ellipse at 50% 40%, #1B0B3A 0%, #0A0418 55%, #000000 100%)";
const fill: React.CSSProperties = { width: "100%", height: "100%", filter: "saturate(1.1) contrast(1.06) brightness(1.06)" };
const slowPush = (frame: number, a: number, b: number, to = 1.04) => interpolate(frame, [a, b], [1, to], CLAMP);
const HOVER_FRAMES = 175; // s3_hover_10x.mp4: RIFE at a true 10x, played at 1.0x (no duplicate frames)

const Footage: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill style={{ backgroundColor: v2.colors.black }}>
      <Sequence durationInFrames={F.xray} premountFor={fps}>
        <AbsoluteFill style={{ scale: slowPush(frame, 0, F.xray), transformOrigin: "40% 55%" }}>
          <Video src={staticFile("shorts/s3_hover_10x.mp4")} muted style={fill} />
        </AbsoluteFill>
      </Sequence>
      <Sequence from={F.xray} durationInFrames={F.gauge - F.xray} premountFor={fps}>
        <Video src={staticFile("shorts/s3_xray.mp4")} muted style={{ width: "100%", height: "100%" }} />
      </Sequence>
      <Sequence from={F.gauge} durationInFrames={F.rewind - F.gauge}>
        <AbsoluteFill style={{ background: BG }} />
      </Sequence>
      {/* back to the hover: the opening plays in reverse and lands on frame 0 */}
      <Sequence from={F.rewind} durationInFrames={F.hold0 - F.rewind} premountFor={fps}>
        <AbsoluteFill style={{ scale: interpolate(frame, [F.rewind, F.hold0], [1.04, 1], { ...CLAMP, easing: EASE_IN_OUT }), transformOrigin: "40% 55%" }}>
          <Video src={staticFile("shorts/s3_hover_10x_rev.mp4")} muted playbackRate={HOVER_FRAMES / (F.hold0 - F.rewind)} style={fill} />
        </AbsoluteFill>
      </Sequence>
      <Sequence from={F.hold0}>
        <Img src={staticFile("shorts/s3_frame0_v3.png")} style={fill} />
      </Sequence>
    </AbsoluteFill>
  );
};

const openingShown = (frame: number, i: number) =>
  frame >= F.hookBack
    ? interpolate(frame, [F.hookBack + i * 3, F.hookBack + 10 + i * 3], [0, 1], { ...CLAMP, easing: EASE_OUT })
    : 1 - interpolate(frame, [F.hookOut - 8 + i * 2, F.hookOut + i * 2], [0, 1], { ...CLAMP, easing: Easing.in(Easing.cubic) });

const Hook: React.FC = () => {
  const frame = useCurrentFrame();
  if (frame > F.hookOut + 4 && frame < F.hookBack) return null;
  const lines = [
    { a: "FLIGHT: ", b: "SECONDS", bc: v2.colors.acid },
    { a: "REFILL: ", b: "HOURS", bc: v2.colors.magenta },
  ];
  return (
    <div style={{ position: "absolute", left: 60, top: 132, ...HEADC }}>
      {lines.map((ln, i) => {
        const shown = openingShown(frame, i);
        return (
          <div key={ln.b} style={{ fontSize: 112, color: v2.colors.ink, opacity: interpolate(shown, [0, 0.35], [0, 1], CLAMP),
            translate: `${(1 - shown) * -90}px 0`, marginBottom: 6, ...keyline(0.75, 10) }}>
            {ln.a}<span style={{ color: ln.bc }}>{ln.b}</span>
          </div>
        );
      })}
    </div>
  );
};

const Tag: React.FC<{ text: string; left: number; top: number; show: number; bg?: string; size?: number }> = ({ text, left, top, show, bg = v2.colors.acid, size = 60 }) => (
  <div style={{ position: "absolute", left, top, padding: "8px 18px 10px", backgroundColor: bg, color: v2.colors.black, border: `4px solid ${v2.colors.black}`,
    ...HEADC, fontSize: size, scale: show, rotate: `${interpolate(show, [0, 1], [-14, -3])}deg`, transformOrigin: "0% 50%" }}>{text}</div>
);

const Xray: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < F.xray || frame >= F.gauge) return null;
  const kg = spring({ frame: frame - 244, fps, config: { damping: 10, stiffness: 230 } });
  return (
    <AbsoluteFill>
      <Tag text="≈250 KG OF GAS" left={64} top={1120} show={kg} />
      <div style={{ position: "absolute", left: 0, top: 128, padding: "8px 20px 8px 60px", backgroundColor: "rgba(0,0,0,0.7)", fontFamily: v2.fonts.mono,
        fontSize: 40, color: v2.colors.ink }}>3D ILLUSTRATION · NOT TESLA FOOTAGE</div>
    </AbsoluteFill>
  );
};

// Our sum, shown: about 80 kN from the rear nozzles, gas leaving at roughly 600 m/s, so about 130 kg a second; about
// 250 kg lasts about 2 s at full thrust. Hovering needs far less push: 8-11 s at best (§5). The drain takes 2 real seconds.
const Gauge: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < F.gauge || frame >= F.quote) return null;
  const rate = interpolate(frame, [F.gauge + 4, F.gauge + 14], [0, 1], { ...CLAMP, easing: EASE_OUT });
  const t = interpolate(frame, [F.drain, F.drain + 2 * fps], [0, 2], CLAMP);
  const left = 1 - t / 2;
  const tag = spring({ frame: frame - (F.gauge + 8), fps, config: { damping: 11, stiffness: 220 } });
  const hover = spring({ frame: frame - (F.gauge + 40), fps, config: { damping: 12, stiffness: 210 } });
  const empty = spring({ frame: frame - (F.drain + 2 * fps), fps, config: { damping: 9, stiffness: 250 } });
  const tanks = [
    { label: "SEAT TANK · 400 L", y: 700, w: 800 },
    { label: "REAR TANK · 200 L", y: 880, w: 400 },
  ];
  return (
    <AbsoluteFill style={{ scale: slowPush(frame, F.gauge, F.quote), transformOrigin: "50% 45%" }}>
      <div style={{ position: "absolute", left: 64, top: 230, ...HEADC, fontSize: 60, color: v2.colors.cyan, ...keyline(0.4, 9) }}>REAR NOZZLES, FULL THRUST</div>
      <div style={{ position: "absolute", left: 64, top: 306, ...HEADC, fontSize: 104, color: v2.colors.ink, opacity: rate, ...keyline(0.7, 10) }}>≈130 KG A SECOND</div>
      <div style={{ position: "absolute", left: 64, top: 418, ...HEADC, fontSize: 44, color: "#C3CAD2", opacity: rate, ...keyline(0.3, 7) }}>80 kN ÷ ≈600 m/s GAS SPEED</div>
      <Tag text="OUR ESTIMATE" left={64} top={478} show={tag} bg={v2.colors.cyan} size={50} />
      {tanks.map((tk) => (
        <div key={tk.label}>
          <div style={{ position: "absolute", left: 110, top: tk.y - 62, ...HEADC, fontSize: 44, color: v2.colors.ink, ...keyline(0.3, 7) }}>{tk.label}</div>
          <div style={{ position: "absolute", left: 110, top: tk.y, width: tk.w, height: 104, borderRadius: 52,
            border: `6px solid ${v2.colors.black}`, backgroundColor: "rgba(255,255,255,0.08)", overflow: "hidden", boxShadow: "inset 0 0 0 4px rgba(230,255,46,0.35)" }}>
            <div style={{ width: `${left * 100}%`, height: "100%", backgroundColor: v2.colors.acid, borderRadius: 52 }} />
          </div>
        </div>
      ))}
      <div style={{ position: "absolute", left: 110, top: 1010, ...HEADC, fontSize: 130, color: left <= 0 ? v2.colors.warn : v2.colors.ink,
        fontVariantNumeric: "tabular-nums", scale: left <= 0 ? interpolate(empty, [0, 1], [1.3, 1]) : 1, transformOrigin: "0% 50%", ...keyline(0.87, 10) }}>
        {t.toFixed(1)} s
      </div>
      <div style={{ position: "absolute", left: 420, top: 1050, ...HEADC, fontSize: 66, color: v2.colors.warn, opacity: interpolate(empty, [0, 0.3], [0, 1], CLAMP),
        ...keyline(0.44, 9) }}>EMPTY</div>
      <div style={{ position: "absolute", left: 64, top: 1180, ...HEADC, fontSize: 56, color: v2.colors.acid, opacity: interpolate(hover, [0, 0.3], [0, 1], CLAMP),
        translate: `${(1 - hover) * -40}px 0`, ...keyline(0.37, 8) }}>HOVERING: ≈8–11 s AT BEST</div>
    </AbsoluteFill>
  );
};

const Quote: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < F.quote || frame >= F.clock) return null;
  const big = spring({ frame: frame - (F.quote + 4), fps, config: { damping: 12, stiffness: 210 } });
  return (
    <AbsoluteFill style={{ scale: slowPush(frame, F.quote, F.clock), transformOrigin: "30% 40%" }}>
      <div style={{ position: "absolute", left: 64, top: 300, ...HEADC, fontSize: 60, color: "#C3CAD2", lineHeight: 1.05, ...keyline(0.4, 8) }}>
        TESLA TO TOP GEAR,<br />ABOUT THE THRUST VERSION
      </div>
      <div style={{ position: "absolute", left: 64, top: 520, ...HEADC, fontSize: 168, color: v2.colors.ink, lineHeight: 0.92,
        opacity: interpolate(big, [0, 0.25], [0, 1], CLAMP), translate: `${(1 - big) * -80}px 0`, ...keyline(1.1, 10) }}>
        A SINGLE<br />LAUNCH<br /><span style={{ color: v2.colors.acid }}>PER FILL</span>
      </div>
    </AbsoluteFill>
  );
};

const Clock: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < F.clock || frame >= F.split) return null;
  const enter = spring({ frame: frame - F.clock, fps, config: { damping: 15, stiffness: 180 } });
  const sweep = interpolate(frame, [F.clock + 10, 727], [0, 1], { ...CLAMP, easing: EASE_IN_OUT });
  const hours = 6 * sweep;
  const label = spring({ frame: frame - F.rigLabel, fps, config: { damping: 11, stiffness: 220 } });
  const cx = 540;
  const cy = 760;
  const r = 300;
  const pt = (h: number, rr: number) => [cx + Math.sin((h / 12) * Math.PI * 2) * rr, cy - Math.cos((h / 12) * Math.PI * 2) * rr];
  const arc = (h0: number, h1: number) => {
    if (h1 <= h0) return "";
    const [x0, y0] = pt(h0, r - 24);
    const [x1, y1] = pt(h1, r - 24);
    return `M ${cx} ${cy} L ${x0} ${y0} A ${r - 24} ${r - 24} 0 ${h1 - h0 > 6 ? 1 : 0} 1 ${x1} ${y1} Z`;
  };
  const [hx, hy] = pt(hours, r - 60);
  return (
    <AbsoluteFill style={{ scale: slowPush(frame, F.clock, F.split, 1.05), transformOrigin: "50% 45%" }}>
      <svg width={1080} height={1920} style={{ position: "absolute", inset: 0, scale: interpolate(enter, [0, 1], [0.75, 1]), transformOrigin: `${cx}px ${cy}px`,
        opacity: interpolate(enter, [0, 0.3], [0, 1], CLAMP) }}>
        <circle cx={cx} cy={cy} r={r} fill="#0B0F17" stroke={v2.colors.ink} strokeWidth={10} />
        <path d={arc(0, Math.min(hours, 2))} fill={v2.colors.cyan} opacity={0.25} />
        <path d={arc(2, Math.max(2, hours))} fill={v2.colors.magenta} opacity={0.55} />
        {Array.from({ length: 12 }).map((_, i) => {
          const [x0, y0] = pt(i, r - 14);
          const [x1, y1] = pt(i, r - 50);
          return <line key={i} x1={x0} y1={y0} x2={x1} y2={y1} stroke={v2.colors.ink} strokeWidth={i % 3 === 0 ? 10 : 5} />;
        })}
        <line x1={cx} y1={cy} x2={hx} y2={hy} stroke={v2.colors.acid} strokeWidth={16} strokeLinecap="round" />
        <circle cx={cx} cy={cy} r={22} fill={v2.colors.acid} stroke="#000" strokeWidth={5} />
      </svg>
      <div style={{ position: "absolute", left: 0, right: 0, top: 1100, textAlign: "center", ...HEADC, opacity: interpolate(label, [0, 0.25], [0, 1], CLAMP),
        translate: `0 ${(1 - label) * 40}px` }}>
        <div style={{ fontSize: 150, color: v2.colors.magenta, ...keyline(1, 10) }}>2–6 HOURS</div>
        <div style={{ fontSize: 56, color: v2.colors.ink, marginTop: 10, ...keyline(0.37, 8) }}>TO REFILL FROM A NITROGEN RIG</div>
      </div>
    </AbsoluteFill>
  );
};

const Split: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < F.split || frame >= F.rewind) return null;
  const a = spring({ frame: frame - (F.split + 8), fps, config: { damping: 14, stiffness: 200 } });
  const stamp = spring({ frame: frame - F.stamp, fps, config: { damping: 9, stiffness: 260 } });
  const b = spring({ frame: frame - F.eng, fps, config: { damping: 14, stiffness: 200 } });
  const vs = spring({ frame: frame - (F.eng - 4), fps, config: { damping: 10, stiffness: 240 } });
  const pre = spring({ frame: frame - F.split, fps, config: { damping: 14, stiffness: 200 } });
  return (
    <AbsoluteFill style={{ scale: slowPush(frame, F.split, F.rewind, 1.06), transformOrigin: "20% 40%" }}>
      {/* the frame is never empty while "Yet on stage" plays: the stage label lands first */}
      <div style={{ position: "absolute", left: 64, top: 290, ...HEADC, opacity: interpolate(pre, [0, 0.25], [0, 1], CLAMP), translate: `${(1 - pre) * -60}px 0` }}>
        <div style={{ fontSize: 60, color: "#C3CAD2", ...keyline(0.4, 8) }}>MUSK, ON STAGE</div>
      </div>
      <div style={{ position: "absolute", left: 64, top: 360, ...HEADC, opacity: interpolate(a, [0, 0.25], [0, 1], CLAMP), translate: `${(1 - a) * -80}px 0` }}>
        <div style={{ fontSize: 112, color: v2.colors.ink, lineHeight: 0.95, ...keyline(0.75, 10) }}>THE CAR<br />REFILLS ITSELF</div>
      </div>
      <div style={{ position: "absolute", left: 330, top: 600, padding: "8px 22px 10px", border: `10px solid ${v2.colors.warn}`, color: v2.colors.warn, ...HEADC,
        fontSize: 88, backgroundColor: "rgba(0,0,0,0.6)", rotate: "-8deg", scale: interpolate(stamp, [0, 1], [1.8, 1]), opacity: interpolate(stamp, [0, 0.2], [0, 1], CLAMP) }}>
        UNPROVEN
      </div>
      <div style={{ position: "absolute", left: 64, top: 690, ...HEADC, fontSize: 96, color: v2.colors.warn, scale: vs, transformOrigin: "0% 50%", ...keyline(0.64, 9) }}>VS</div>
      <div style={{ position: "absolute", left: 64, top: 830, ...HEADC, opacity: interpolate(b, [0, 0.25], [0, 1], CLAMP), translate: `${(1 - b) * 80}px 0` }}>
        <div style={{ fontSize: 60, color: "#C3CAD2", ...keyline(0.4, 8) }}>HIS ENGINEER, TO TOP GEAR</div>
        <div style={{ fontSize: 112, color: v2.colors.magenta, lineHeight: 0.95, marginTop: 10, ...keyline(0.75, 10) }}>2–6 HOURS<br />ON A RIG</div>
      </div>
    </AbsoluteFill>
  );
};

const PAGES = makePages(VO_S3_CAPTIONS);

const Captions: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < F.hookOut + 2 || frame >= F.rewind) return null;
  if (frame >= F.rigLabel && frame < F.split) return null; // the 2-6 HOURS block owns the lower frame
  const ms = (frame / fps) * 1000;
  const page = PAGES.find((p, i) => ms >= p.startMs && ms < (PAGES[i + 1]?.startMs ?? p.startMs + p.durationMs + 600));
  if (!page) return null;
  const pop = interpolate(ms - page.startMs, [0, 90, 160], [0.9, 1.05, 1], CLAMP);
  const startedIdx = page.tokens.reduce((acc, tk, j) => (tk.fromMs <= ms ? j : acc), -1);
  const top = frame < F.xray ? 470 : 1318;
  // a long page (a kept-together name like TOP GEAR) shrinks to one line instead of wrapping
  const chars = page.tokens.map((t) => t.text).join("").trim().length;
  const size = Math.min(88, Math.floor(860 / (chars * 0.56)));
  return (
    <div style={{ position: "absolute", left: 70, right: 140, top, textAlign: "center", ...HEAD, fontVariationSettings: "'wdth' 88",
      fontSize: size, lineHeight: 1.04, textTransform: "uppercase", scale: pop, whiteSpace: "nowrap" }}>
      {page.tokens.map((t, i) => (
        <span key={t.fromMs} style={{ color: i === startedIdx ? v2.colors.acid : v2.colors.ink, ...keyline(0.6, 11) }}>{t.text}</span>
      ))}
    </div>
  );
};

// Credit off the jets (under the hook, in the black sky), on every frame of Tesla footage.
const Credit: React.FC = () => {
  const frame = useCurrentFrame();
  const onFootage = frame < F.xray || frame >= F.rewind;
  if (!onFootage) return null;
  const slowed = frame < F.xray || frame >= F.hookBack; // the opening and the frame-0 still are slowed footage
  return (
    <div style={{ position: "absolute", left: 0, top: 372, padding: "8px 22px 8px 60px",
      backgroundColor: "rgba(0,0,0,0.74)", fontFamily: v2.fonts.mono, fontWeight: 500, fontSize: 38, letterSpacing: "0.02em", color: v2.colors.ink }}>
      FOOTAGE: TESLA / YOUTUBE, 15 OCT 2026{slowed ? " · 10× SLOWER" : ""}
    </div>
  );
};

export const CurveV2Short3: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: v2.colors.black }}>
      <Footage />
      <Xray />
      <Gauge />
      <Quote />
      <Clock />
      <Split />
      <Hook />
      <Captions />
      <Credit />

      <Audio src={staticFile("shorts/s3_chris_v4_v2.mp3")} />
      <Audio src={staticFile("audio/sample-bed.mp3")} volume={(f) => interpolate(f, [0, 2, SHORT3_FRAMES - 2, SHORT3_FRAMES], [0.06, 0.13, 0.13, 0.06], CLAMP)} />
      <Sequence from={0} durationInFrames={108}><Audio src={staticFile("sfx/hiss.mp3")} volume={0.7} /></Sequence>
      <Sequence from={F.xray}><Audio src={staticFile("sfx/whoosh.mp3")} volume={0.45} /></Sequence>
      <Sequence from={212}><Audio src={staticFile("sfx/form.mp3")} volume={0.4} /></Sequence>
      <Sequence from={244}><Audio src={staticFile("sfx/thock.mp3")} volume={0.6} /></Sequence>
      <Sequence from={F.gauge}><Audio src={staticFile("sfx/whoosh.mp3")} volume={0.4} /></Sequence>
      <Sequence from={F.drain} durationInFrames={60}><Audio src={staticFile("sfx/hiss.mp3")} volume={0.8} /></Sequence>
      <Sequence from={F.drain + 60}><Audio src={staticFile("sfx/thock.mp3")} volume={0.7} /></Sequence>
      <Sequence from={F.quote}><Audio src={staticFile("sfx/whoosh.mp3")} volume={0.4} /></Sequence>
      <Sequence from={F.quote + 4}><Audio src={staticFile("sfx/thock.mp3")} volume={0.6} /></Sequence>
      <Sequence from={F.clock}><Audio src={staticFile("sfx/whoosh.mp3")} volume={0.4} /></Sequence>
      <Sequence from={F.clock + 10} durationInFrames={110}><Audio src={staticFile("sfx/tick_run.mp3")} volume={0.25} /></Sequence>
      <Sequence from={F.rigLabel}><Audio src={staticFile("sfx/thock.mp3")} volume={0.6} /></Sequence>
      <Sequence from={F.split}><Audio src={staticFile("sfx/whoosh.mp3")} volume={0.4} /></Sequence>
      <Sequence from={F.stamp}><Audio src={staticFile("sfx/thock.mp3")} volume={0.8} /></Sequence>
      <Sequence from={F.eng - 4}><Audio src={staticFile("sfx/thock.mp3")} volume={0.55} /></Sequence>
      <Sequence from={F.rewind}><Audio src={staticFile("sfx/rewind.mp3")} volume={0.55} /></Sequence>
    </AbsoluteFill>
  );
};
