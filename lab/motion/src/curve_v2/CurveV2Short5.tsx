import { Audio } from "@remotion/media";
import type React from "react";
import { AbsoluteFill, Easing, Img, interpolate, Sequence, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { CLAMP } from "../lib/anim";
import { Bed, BG_NIGHT, C, CaptionTrack, ClipScene, Credit, FILL, HBars, HEAD, HEADC, Headline, keyline, MONO, pop, Sfx, slowPush, Tag } from "./kit";
import { makePages } from "./pager";
import { VO_S5_CAPTIONS } from "./voS5Captions";

// Curve Short 5 (Sun 25 Oct 2026): "Tesla Showed a Flying Car. Then Its Profit Fell 43%". 1080x1920, 30 fps.
// Every number from Tesla's Q3 2026 Update (8-K exhibit 99.1, 21 Oct 2026): lab/research/TESLA_Q3_2026_FACTS.md rows
// 3, 6, 7, 11 and Tesla's "Profitability" sentence, quoted word for word. Footage: Tesla, YouTube, 16 Oct 2026 (the
// Roadster clips made for Shorts 1-2). Cuts on the 124 BPM bed's beats. Narration s5_chris_v4_tight.mp3 (31.6 s).
// The last frame is frame 0.

export const SHORT5_FRAMES = 970;

const F = { drop: 125, gross: 189, rnd: 348, quote: 479, credits: 653, verdict: 784, rewind: 948, hold0: 960 };
const PAGES = makePages(VO_S5_CAPTIONS);
const SOURCE = "SOURCE: TESLA Q3 2026 UPDATE";

const Footage: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill style={{ backgroundColor: C.black }}>
      <ClipScene src="shorts/s1_hook_20x.mp4" from={0} dur={F.drop} push={[1, 1.04]} origin="40% 40%" />
      <ClipScene src="shorts/s1_drop.mp4" from={F.drop} dur={F.gross - F.drop} push={[1.04, 1.08]} origin="40% 40%" />
      <Sequence from={F.gross} durationInFrames={F.verdict - F.gross}><AbsoluteFill style={{ background: BG_NIGHT }} /></Sequence>
      <Sequence from={F.verdict} durationInFrames={F.rewind - F.verdict} premountFor={fps}>
        <AbsoluteFill style={{ scale: slowPush(frame, F.verdict, F.rewind, 1.05) }}>
          <ClipScene src="shorts/s2_launch_8x_v2.mp4" from={0} dur={F.rewind - F.verdict} push={[1, 1]} style={{ filter: "brightness(0.5) saturate(1.05)" }} />
        </AbsoluteFill>
      </Sequence>
      <ClipScene src="shorts/s1_hook_20x_rev.mp4" from={F.rewind} dur={F.hold0 - F.rewind} rate={125 / 12} push={[1, 1]} />
      <Sequence from={F.hold0}><Img src={staticFile("shorts/s5_frame0.png")} style={FILL} /></Sequence>
    </AbsoluteFill>
  );
};

// Frame 0 and the end: the claim beside the car that made the headlines.
const Hook: React.FC = () => {
  const frame = useCurrentFrame();
  if (!(frame < F.gross || frame >= F.hold0)) return null;
  const punch = frame < F.gross ? interpolate(frame, [0, F.gross], [1, 1.03], CLAMP) : 1;
  return (
    <div style={{ position: "absolute", left: 60, top: 120, scale: punch, transformOrigin: "0% 0%" }}>
      <div style={{ ...HEADC, fontSize: 104, color: C.ink, ...keyline(0.7, 11) }}>TESLA&apos;S PROFIT</div>
      <div style={{ ...HEADC, fontSize: 300, color: C.warn, lineHeight: 0.84, ...keyline(2, 11) }}>−43%</div>
      <div style={{ display: "inline-block", marginTop: 14, padding: "6px 18px 9px", backgroundColor: C.ink, color: C.black, ...HEADC,
        fontSize: 56, border: `4px solid ${C.black}` }}>6 DAYS AFTER THIS ↓</div>
    </div>
  );
};

const Gross: React.FC = () => {
  const frame = useCurrentFrame();
  if (frame < F.gross || frame >= F.rnd) return null;
  return (
    <AbsoluteFill style={{ scale: slowPush(frame, F.gross, F.rnd, 1.04), transformOrigin: "30% 40%" }}>
      <Headline at={F.gross + 2} top={200} lines={[{ text: "GROSS PROFIT", size: 150, color: C.acid }]} />
      <Headline at={F.gross + 8} top={360} lines={[{ text: "WHAT'S LEFT AFTER MAKING", size: 60 }, { text: "WHAT IT SELLS", size: 60 }]} stroke={8} />
      <HBars at={F.gross + 20} top={560} max={6} width={680} rows={[
        { label: "Q3 2025", value: 5.054, show: (v) => `$${v.toFixed(2)}B`, color: "#8FA3B8" },
        { label: "Q3 2026", value: 5.494, show: (v) => `$${v.toFixed(2)}B`, color: C.acid },
      ]} />
      <Tag at={F.gross + 122} left={64} top={1010} bg={C.acid} size={110}>+9%</Tag>
    </AbsoluteFill>
  );
};

const RnD: React.FC = () => {
  const frame = useCurrentFrame();
  if (frame < F.rnd || frame >= F.quote) return null;
  const cols = [
    { label: "Q3 2025", v: 1.63, color: "#8FA3B8", x: 150, at: F.rnd + 14 },
    { label: "Q3 2026", v: 2.761, color: C.magenta, x: 600, at: F.rnd + 26 },
  ];
  const base = 1180, maxH = 600, maxV = 3;
  return (
    <AbsoluteFill style={{ scale: slowPush(frame, F.rnd, F.quote, 1.04), transformOrigin: "50% 70%" }}>
      <Headline at={F.rnd + 2} top={180} lines={[{ text: "RESEARCH SPENDING", size: 98, color: C.magenta }]} />
      {cols.map((c) => {
        const k = interpolate(frame, [c.at, c.at + 24], [0, 1], { ...CLAMP, easing: Easing.bezier(0.16, 1, 0.3, 1) });
        const h = (maxH * c.v * k) / maxV;
        return (
          <div key={c.label}>
            <div style={{ position: "absolute", left: c.x, top: base - h, width: 330, height: h, backgroundColor: c.color, border: `6px solid ${C.black}` }} />
            <div style={{ position: "absolute", left: c.x, width: 330, top: base - h - 120, textAlign: "center", ...HEADC, fontSize: 96, color: c.color,
              opacity: k, ...keyline(0.7, 10), fontVariantNumeric: "tabular-nums" }}>${(c.v * k).toFixed(2)}B</div>
            <div style={{ position: "absolute", left: c.x, width: 330, top: base + 18, textAlign: "center", ...HEADC, fontSize: 56, color: C.ink,
              ...keyline(0.4, 8) }}>{c.label}</div>
          </div>
        );
      })}
      <Tag at={F.rnd + 90} left={630} top={330} bg={C.magenta} color={C.ink} size={110}>+69%</Tag>
    </AbsoluteFill>
  );
};

// Tesla's sentence, word for word, filling the frame (no card); the two causes light up as the narration names them.
const Quote: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < F.quote || frame >= F.credits) return null;
  const inQ = pop(frame, F.quote + 6, fps, 180, 15);
  const hi = (at: number) => interpolate(frame, [at, at + 8], [0, 1], CLAMP);
  const h1 = hi(F.quote + 38);   // "research projects" ~17.3 s
  const h2 = hi(F.quote + 80);   // "stock pay, including Elon Musk's 2025 award" ~18.5-21.9 s
  const mark = (t: number): React.CSSProperties => ({
    color: t > 0.5 ? C.black : C.ink,
    backgroundImage: `linear-gradient(${C.acid}, ${C.acid})`, backgroundRepeat: "no-repeat", backgroundSize: `${t * 100}% 100%`,
    padding: "0 6px", boxDecorationBreak: "clone", WebkitBoxDecorationBreak: "clone",
  });
  return (
    <AbsoluteFill style={{ scale: slowPush(frame, F.quote, F.credits, 1.03), transformOrigin: "20% 30%" }}>
      <Tag at={F.quote + 2} left={64} top={200} bg={C.ink} size={56}>TESLA&apos;S OWN EXPLANATION</Tag>
      <div style={{ position: "absolute", left: 64, right: 90, top: 340, ...HEAD, fontVariationSettings: "'wdth' 88", fontWeight: 800,
        fontSize: 78, lineHeight: 1.16, color: C.ink, opacity: interpolate(inQ, [0, 0.3], [0, 1], CLAMP), translate: `0 ${(1 - inQ) * 40}px` }}>
        <span style={{ color: C.acid, fontSize: 120, lineHeight: 0.5 }}>“</span>…an increase in operating expenses driven by{" "}
        <span style={mark(h1)}>SI and other R&amp;D projects</span>,{" "}
        <span style={mark(h2)}>SBC (including 2025 CEO Performance Award)</span> and SG&amp;A
      </div>
      <div style={{ position: "absolute", left: 64, top: 1130, ...MONO, fontSize: 38, color: C.cyan,
        opacity: interpolate(frame, [F.quote + 84, F.quote + 96], [0, 1], CLAMP) }}>SBC = STOCK-BASED PAY · R&amp;D = RESEARCH</div>
    </AbsoluteFill>
  );
};

const Credits: React.FC = () => {
  const frame = useCurrentFrame();
  if (frame < F.credits || frame >= F.verdict) return null;
  const grow = interpolate(frame, [F.credits + 12, F.credits + 30], [0, 1], { ...CLAMP, easing: Easing.bezier(0.16, 1, 0.3, 1) });
  const shrink = interpolate(frame, [F.credits + 74, F.credits + 100], [0, 1], { ...CLAMP, easing: Easing.bezier(0.65, 0, 0.35, 1) }); // "shrunk"
  const W = 900;
  const v = interpolate(shrink, [0, 1], [417, 113]) * grow;
  const w = (W * v) / 417;
  return (
    <AbsoluteFill style={{ scale: slowPush(frame, F.credits, F.verdict, 1.04), transformOrigin: "30% 50%" }}>
      <Headline at={F.credits + 2} top={200} lines={[{ text: "CREDITS SOLD TO", size: 104, color: C.cyan }, { text: "OTHER CARMAKERS", size: 104, color: C.cyan }]} />
      <div style={{ position: "absolute", left: 64, top: 440, ...MONO, fontSize: 38, color: "#C3CAD2",
        opacity: interpolate(frame, [F.credits + 10, F.credits + 20], [0, 1], CLAMP) }}>(REGULATORY CREDITS, A QUARTER&apos;S REVENUE)</div>
      <div style={{ position: "absolute", left: 64, top: 600, width: W, height: 150, border: `6px dashed rgba(255,255,255,${0.55 * shrink})` }} />
      <div style={{ position: "absolute", left: 64, top: 600, width: w, height: 150, backgroundColor: shrink > 0.02 ? C.warn : "#8FA3B8",
        border: `6px solid ${C.black}` }} />
      <div style={{ position: "absolute", left: 64, top: 780, ...HEADC, fontSize: 112, color: shrink > 0.02 ? C.warn : C.ink, ...keyline(0.8, 10),
        fontVariantNumeric: "tabular-nums", opacity: grow }}>${Math.round(v)}M</div>
      <div style={{ position: "absolute", left: 64, top: 910, ...HEADC, fontSize: 56, color: C.ink, ...keyline(0.4, 8), opacity: grow }}>
        {shrink < 0.5 ? "Q3 2025" : "Q3 2026"}
      </div>
      <Tag at={F.credits + 100} left={560} top={630} bg={C.warn} color={C.ink} size={110}>−73%</Tag>
    </AbsoluteFill>
  );
};

const Verdict: React.FC = () => {
  const frame = useCurrentFrame();
  if (frame < F.verdict || frame >= F.rewind) return null;
  const lab = (at: number): React.CSSProperties => ({ ...MONO, fontSize: 42, color: "#C3CAD2", opacity: interpolate(frame, [at, at + 8], [0, 1], CLAMP) });
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", left: 64, top: 300, ...lab(F.verdict + 4) }}>THE HEADLINES</div>
      <Headline at={F.verdict + 6} top={360} lines={[{ text: "THE FLYING CAR", size: 128 }]} />
      <div style={{ position: "absolute", left: 64, top: 620, ...lab(F.verdict + 64) }}>THE BILL</div>
      <Headline at={F.verdict + 66} top={680} lines={[{ text: "BETS ON", size: 128, color: C.acid }, { text: "WHAT'S NEXT", size: 128, color: C.acid }]} />
    </AbsoluteFill>
  );
};

export const CurveV2Short5: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: C.black }}>
    <Footage />
    <Gross />
    <RnD />
    <Quote />
    <Credits />
    <Verdict />
    <Hook />
    <CaptionTrack pages={PAGES} hide={[[0, 46]]} until={F.rewind} />
    <Credit text="FOOTAGE: TESLA / YOUTUBE · SLOWED DOWN" show={[[0, F.gross], [F.verdict, F.rewind], [F.hold0, SHORT5_FRAMES]]} />
    <Credit text={SOURCE} show={[[F.gross, F.verdict]]} />

    <Audio src={staticFile("shorts/s5_vo.mp3")} />
    <Bed total={SHORT5_FRAMES} level={0.12} />
    <Sfx at={F.drop} name="hiss" volume={0.6} dur={64} />
    <Sfx at={F.gross} name="whoosh" volume={0.4} />
    <Sfx at={F.gross + 20} name="form" volume={0.35} />
    <Sfx at={F.gross + 122} name="thock" volume={0.6} />
    <Sfx at={F.rnd} name="whoosh" volume={0.4} />
    <Sfx at={F.rnd + 14} name="form" volume={0.35} />
    <Sfx at={F.rnd + 90} name="thock" volume={0.6} />
    <Sfx at={F.quote} name="whoosh" volume={0.35} />
    <Sfx at={F.credits} name="whoosh" volume={0.4} />
    <Sfx at={F.credits + 14} name="form" volume={0.35} />
    <Sfx at={F.credits + 74} name="settle" volume={0.5} />
    <Sfx at={F.credits + 100} name="thock" volume={0.7} />
    <Sfx at={F.verdict} name="whoosh" volume={0.4} />
    <Sfx at={F.verdict + 66} name="thock" volume={0.55} />
    <Sfx at={F.rewind} name="rewind" volume={0.45} />
  </AbsoluteFill>
);
