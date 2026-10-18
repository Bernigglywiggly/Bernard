import { Audio, Video } from "@remotion/media";
import type React from "react";
import { AbsoluteFill, Easing, Img, interpolate, Sequence, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { CLAMP, EASE_IN_OUT, EASE_OUT } from "../lib/anim";
import { keyline } from "./HybridC";
import { v2 } from "./palette";
import { VO_S3_CAPTIONS } from "./voS3Captions";

// Roadster Short 3 (for Tue 20 Oct): "How Long Can the Tesla Roadster Fly?". 1080x1920, 30 fps.
// Footage: Tesla's 4K "The Kickflip" upload (r5vsHHPVhJg 0:32-0:35, frames 44-71), RIFE 6x, pan-crop that follows the car
// as it rolls upright on its jets and lands. 3D: our Blender x-ray of the two tanks and ten nozzles (labelled).
// Numbers: TESLA_ROADSTER_FACTS.md P1 (two COPVs, about 250 kg), §5 (about 2 s at 80 kN: OUR ESTIMATE, working shown),
// S1 (one launch per fill; 2-6 h refill from a nitrogen rig), P1 12:30 (Musk: the car refills its tank). Last frame = frame 0.
// Narration lab/curve_v2/shorts/vo/s3_chris_v4.mp3 (31.9 s).

export const SHORT3_FRAMES = 960;

const F = { hookOut: 88, xray: 175, gauge: 313, drain: 406, quote: 465, clock: 595, split: 758, musk: 791, eng: 875, rewind: 930, hookBack: 940, hold0: 958 };

const HEAD: React.CSSProperties = { fontFamily: v2.fonts.heavy, fontWeight: 900, letterSpacing: "-0.02em", lineHeight: 0.9 };
const HEADC: React.CSSProperties = { ...HEAD, fontVariationSettings: "'wdth' 82", whiteSpace: "nowrap" };
const BG = "radial-gradient(ellipse at 50% 40%, #1B0B3A 0%, #0A0418 55%, #000000 100%)";
const fill: React.CSSProperties = { width: "100%", height: "100%", filter: "saturate(1.1) contrast(1.06) brightness(1.06)" };

const Footage: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const push = interpolate(frame, [0, F.xray], [1, 1.04], CLAMP);
  const pushEnd = interpolate(frame, [F.rewind, F.hold0], [1.04, 1], { ...CLAMP, easing: EASE_IN_OUT });
  return (
    <AbsoluteFill style={{ backgroundColor: v2.colors.black }}>
      <Sequence durationInFrames={F.xray} premountFor={fps}>
        <AbsoluteFill style={{ scale: push, transformOrigin: "50% 40%" }}>
          <Video src={staticFile("shorts/s3_roll_6x.mp4")} muted style={fill} />
        </AbsoluteFill>
      </Sequence>
      <Sequence from={F.xray} durationInFrames={F.gauge - F.xray} premountFor={fps}>
        <Video src={staticFile("shorts/s3_xray.mp4")} muted style={{ width: "100%", height: "100%" }} />
      </Sequence>
      <Sequence from={F.gauge} durationInFrames={F.rewind - F.gauge}>
        <AbsoluteFill style={{ background: BG }} />
      </Sequence>
      {/* back to the opening: the roll plays in reverse from where the opening cut away, ending on frame 0 */}
      <Sequence from={F.rewind} durationInFrames={F.hold0 - F.rewind} premountFor={fps}>
        <AbsoluteFill style={{ scale: pushEnd, transformOrigin: "50% 40%" }}>
          <Video src={staticFile("shorts/s3_roll_6x_rev.mp4")} muted trimBefore={204 - F.xray} playbackRate={F.xray / (F.hold0 - F.rewind)} style={fill} />
        </AbsoluteFill>
      </Sequence>
      <Sequence from={F.hold0}>
        <Img src={staticFile("shorts/s3_frame0.png")} style={fill} />
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
        fontSize: 38, color: v2.colors.ink }}>3D ILLUSTRATION · NOT TESLA FOOTAGE</div>
    </AbsoluteFill>
  );
};

// Our sum, shown: about 80 kN from the rear nozzles, gas leaving at roughly 600 m/s, so about 130 kg a second; about
// 250 kg of gas lasts about 2 seconds. The drain on screen takes exactly 2 real seconds.
const Gauge: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < F.gauge || frame >= F.quote) return null;
  const enter = interpolate(frame, [F.gauge, F.gauge + 10], [0, 1], { ...CLAMP, easing: EASE_OUT });
  const rate = interpolate(frame, [F.gauge + 8, F.gauge + 18], [0, 1], { ...CLAMP, easing: EASE_OUT });
  const t = interpolate(frame, [F.drain, F.drain + 2 * fps], [0, 2], CLAMP);
  const left = 1 - t / 2;
  const tag = spring({ frame: frame - (F.gauge + 4), fps, config: { damping: 11, stiffness: 220 } });
  const empty = spring({ frame: frame - (F.drain + 2 * fps), fps, config: { damping: 9, stiffness: 250 } });
  const leave = interpolate(frame, [F.quote - 6, F.quote], [0, 1], CLAMP);
  const tanks = [{ y: 760, w: 600 }, { y: 920, w: 860 }];
  return (
    <AbsoluteFill style={{ opacity: enter * (1 - leave), scale: interpolate(frame, [F.gauge, F.quote], [1, 1.04], CLAMP), transformOrigin: "50% 45%" }}>
      <div style={{ position: "absolute", left: 64, top: 240, ...HEADC, fontSize: 64, color: v2.colors.cyan, ...keyline(0.43, 9) }}>AT FULL POWER</div>
      <div style={{ position: "absolute", left: 64, top: 320, ...HEADC, fontSize: 104, color: v2.colors.ink, opacity: rate, ...keyline(0.7, 10) }}>≈130 KG A SECOND</div>
      <div style={{ position: "absolute", left: 64, top: 432, ...HEADC, fontSize: 44, color: "#C3CAD2", opacity: rate, ...keyline(0.3, 7) }}>80 kN ÷ ≈600 m/s GAS SPEED</div>
      <Tag text="OUR ESTIMATE" left={64} top={500} show={tag} bg={v2.colors.cyan} size={52} />
      {tanks.map((tk) => (
        <div key={tk.y} style={{ position: "absolute", left: 110, top: tk.y, width: tk.w, height: 120, borderRadius: 60,
          border: `6px solid ${v2.colors.black}`, backgroundColor: "rgba(255,255,255,0.08)", overflow: "hidden", boxShadow: "inset 0 0 0 4px rgba(230,255,46,0.35)" }}>
          <div style={{ width: `${left * 100}%`, height: "100%", backgroundColor: v2.colors.acid, borderRadius: 60 }} />
        </div>
      ))}
      <div style={{ position: "absolute", left: 110, top: 1080, ...HEADC, fontSize: 150, color: left <= 0 ? v2.colors.warn : v2.colors.ink,
        fontVariantNumeric: "tabular-nums", scale: left <= 0 ? interpolate(empty, [0, 1], [1.3, 1]) : 1, transformOrigin: "0% 50%", ...keyline(1, 10) }}>
        {t.toFixed(1)} s
      </div>
      <div style={{ position: "absolute", left: 470, top: 1130, ...HEADC, fontSize: 70, color: v2.colors.warn, opacity: interpolate(empty, [0, 0.3], [0, 1], CLAMP),
        ...keyline(0.47, 9) }}>EMPTY</div>
    </AbsoluteFill>
  );
};

const Quote: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < F.quote || frame >= F.clock) return null;
  const a = spring({ frame: frame - F.quote, fps, config: { damping: 14, stiffness: 190 } });
  const big = spring({ frame: frame - 545, fps, config: { damping: 11, stiffness: 220 } });
  const leave = interpolate(frame, [F.clock - 6, F.clock], [0, 1], CLAMP);
  return (
    <AbsoluteFill style={{ opacity: 1 - leave, scale: interpolate(frame, [F.quote, F.clock], [1, 1.04], CLAMP), transformOrigin: "30% 40%" }}>
      <div style={{ position: "absolute", left: 64, top: 300, ...HEADC, fontSize: 60, color: "#C3CAD2", lineHeight: 1.05, opacity: a, ...keyline(0.4, 8) }}>
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
  const label = spring({ frame: frame - 702, fps, config: { damping: 11, stiffness: 220 } });
  const leave = interpolate(frame, [F.split - 6, F.split], [0, 1], CLAMP);
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
    <AbsoluteFill style={{ opacity: 1 - leave, scale: interpolate(frame, [F.clock, F.split], [1, 1.05], CLAMP), transformOrigin: "50% 45%" }}>
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
  const a = spring({ frame: frame - F.musk, fps, config: { damping: 14, stiffness: 200 } });
  const b = spring({ frame: frame - F.eng, fps, config: { damping: 14, stiffness: 200 } });
  const vs = spring({ frame: frame - (F.eng - 6), fps, config: { damping: 10, stiffness: 240 } });
  const leave = interpolate(frame, [F.rewind - 6, F.rewind], [0, 1], CLAMP);
  return (
    <AbsoluteFill style={{ opacity: 1 - leave, scale: interpolate(frame, [F.split, F.rewind], [1, 1.06], CLAMP), transformOrigin: "20% 40%" }}>
      <div style={{ position: "absolute", left: 64, top: 290, ...HEADC, opacity: interpolate(a, [0, 0.25], [0, 1], CLAMP), translate: `${(1 - a) * -80}px 0` }}>
        <div style={{ fontSize: 60, color: "#C3CAD2", ...keyline(0.4, 8) }}>MUSK, ON STAGE</div>
        <div style={{ fontSize: 112, color: v2.colors.ink, lineHeight: 0.95, marginTop: 10, ...keyline(0.75, 10) }}>THE CAR<br />REFILLS ITSELF</div>
      </div>
      <div style={{ position: "absolute", left: 64, top: 690, ...HEADC, fontSize: 96, color: v2.colors.warn, scale: vs, transformOrigin: "0% 50%", ...keyline(0.64, 9) }}>VS</div>
      <div style={{ position: "absolute", left: 64, top: 830, ...HEADC, opacity: interpolate(b, [0, 0.25], [0, 1], CLAMP), translate: `${(1 - b) * 80}px 0` }}>
        <div style={{ fontSize: 60, color: "#C3CAD2", ...keyline(0.4, 8) }}>HIS ENGINEER, TO TOP GEAR</div>
        <div style={{ fontSize: 112, color: v2.colors.magenta, lineHeight: 0.95, marginTop: 10, ...keyline(0.75, 10) }}>2–6 HOURS<br />ON A RIG</div>
      </div>
    </AbsoluteFill>
  );
};

type Word = { text: string; fromMs: number; toMs: number };
type Page = { startMs: number; durationMs: number; tokens: Word[] };
const STOP = new Set(["the", "a", "an", "to", "of", "and", "with", "from", "in", "it", "for"]);
const PAGES: Page[] = (() => {
  const words: Word[] = [];
  for (const c of VO_S3_CAPTIONS) {
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
    if (/[.,!?]$/.test(w.text.trim())) cur = null;
  }
  return out;
})();

const Captions: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < F.hookOut + 2 || frame >= F.hookBack) return null;
  const ms = (frame / fps) * 1000;
  const page = PAGES.find((p, i) => ms >= p.startMs && ms < (PAGES[i + 1]?.startMs ?? p.startMs + p.durationMs + 400));
  if (!page) return null;
  const pop = interpolate(ms - page.startMs, [0, 90, 160], [0.9, 1.05, 1], CLAMP);
  const startedIdx = page.tokens.reduce((acc, tk, j) => (tk.fromMs <= ms ? j : acc), -1);
  const top = frame < F.xray || frame >= F.rewind ? 400 : 1318;
  return (
    <div style={{ position: "absolute", left: 70, right: 140, top, textAlign: "center", ...HEAD, fontVariationSettings: "'wdth' 88",
      fontSize: 88, lineHeight: 1.04, textTransform: "uppercase", scale: pop }}>
      {page.tokens.map((t, i) => (
        <span key={t.fromMs} style={{ color: i === startedIdx ? v2.colors.acid : v2.colors.ink, ...keyline(0.6, 11) }}>{t.text}</span>
      ))}
    </div>
  );
};

const Credit: React.FC = () => {
  const frame = useCurrentFrame();
  if (!(frame < F.xray || frame >= F.hookBack)) return null;
  return (
    <div style={{ position: "absolute", left: 0, top: 1342, padding: "10px 22px 10px 60px", backgroundColor: "rgba(0,0,0,0.74)",
      fontFamily: v2.fonts.mono, fontWeight: 500, fontSize: 40, letterSpacing: "0.02em", color: v2.colors.ink }}>
      FOOTAGE: TESLA / YOUTUBE · 6× SLOWER
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

      <Audio src={staticFile("shorts/s3_chris_v4.mp3")} />
      <Audio src={staticFile("audio/sample-bed.mp3")} volume={(f) => interpolate(f, [0, 4, SHORT3_FRAMES - 5, SHORT3_FRAMES], [0, 0.13, 0.13, 0], CLAMP)} />
      <Sequence from={30} durationInFrames={108}><Audio src={staticFile("sfx/hiss.mp3")} volume={0.7} /></Sequence>
      <Sequence from={F.xray}><Audio src={staticFile("sfx/whoosh.mp3")} volume={0.45} /></Sequence>
      <Sequence from={212}><Audio src={staticFile("sfx/form.mp3")} volume={0.4} /></Sequence>
      <Sequence from={244}><Audio src={staticFile("sfx/thock.mp3")} volume={0.6} /></Sequence>
      <Sequence from={F.gauge}><Audio src={staticFile("sfx/whoosh.mp3")} volume={0.4} /></Sequence>
      <Sequence from={F.drain} durationInFrames={60}><Audio src={staticFile("sfx/hiss.mp3")} volume={0.8} /></Sequence>
      <Sequence from={F.drain + 60}><Audio src={staticFile("sfx/thock.mp3")} volume={0.7} /></Sequence>
      <Sequence from={F.quote}><Audio src={staticFile("sfx/whoosh.mp3")} volume={0.4} /></Sequence>
      <Sequence from={545}><Audio src={staticFile("sfx/thock.mp3")} volume={0.65} /></Sequence>
      <Sequence from={F.clock}><Audio src={staticFile("sfx/whoosh.mp3")} volume={0.4} /></Sequence>
      <Sequence from={F.clock + 10} durationInFrames={110}><Audio src={staticFile("sfx/tick_run.mp3")} volume={0.25} /></Sequence>
      <Sequence from={702}><Audio src={staticFile("sfx/thock.mp3")} volume={0.6} /></Sequence>
      <Sequence from={F.split}><Audio src={staticFile("sfx/whoosh.mp3")} volume={0.4} /></Sequence>
      <Sequence from={F.eng - 6}><Audio src={staticFile("sfx/thock.mp3")} volume={0.65} /></Sequence>
      <Sequence from={F.rewind}><Audio src={staticFile("sfx/rewind.mp3")} volume={0.55} /></Sequence>
    </AbsoluteFill>
  );
};
