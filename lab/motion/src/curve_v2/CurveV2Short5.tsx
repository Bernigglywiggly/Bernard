import { Audio } from "@remotion/media";
import type React from "react";
import { AbsoluteFill, Easing, interpolate, Sequence, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { CLAMP } from "../lib/anim";
import { BG_NIGHT, C, CaptionTrack, ClipScene, Credit, HBars, HEAD, HEADC, Headline, keyline, MONO, pop, Sfx, slowPush, Tag } from "./kit";
import { makePages } from "./pager";
import { VO_S5_CAPTIONS } from "./voS5Captions";

// Curve Short 5 v2 (Sun 25 Oct 2026): "Tesla Showed a Flying Car. Then Its Profit Fell 43%". 1080x1920, 30 fps.
// v2 applies critic round 1 (lab/curve_v2/shorts/out/critic_s5/round1.md): the -43% is labelled GAAP and set against
// Tesla's own adjusted figure (-4%); Tesla's sentence is quoted word for word and "SI" glossed as Tesla's own term
// "Super Intelligence"; "reported", not "said"; frame 0 is the airborne-thrusters frame, not Short 1's; charts fill
// the frame in four different layouts; captions come from the script; the -73% holds 1.6 s.
// Numbers: Tesla's Q3 2026 Update (8-K exhibit 99.1, 21 Oct 2026), lab/research/TESLA_Q3_2026_FACTS.md rows 3, 6, 7,
// 11, 13b. Footage: Tesla, YouTube, 16 Oct 2026. Narration s5_chris_v5_tight.mp3 (34.2 s). Cuts on the 124 BPM beat.

export const SHORT5_FRAMES = 1052;

const F = { hover: 118, gross: 203, rnd: 363, quote: 479, credits: 581, adjusted: 711, verdict: 871, rewind: 1046, hold0: 1052 };
const PAGES = makePages(VO_S5_CAPTIONS);
const SOURCE = "SOURCE: TESLA Q3 2026 UPDATE";
const EASE = Easing.bezier(0.16, 1, 0.3, 1);

const Footage: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill style={{ backgroundColor: C.black }}>
      <ClipScene src="shorts/s5_hook.mp4" from={0} dur={F.hover} push={[1, 1.04]} origin="35% 50%" />
      <ClipScene src="shorts/s3_hover_10x.mp4" from={F.hover} dur={F.gross - F.hover} push={[1.02, 1.07]} origin="50% 45%" />
      <Sequence from={F.gross} durationInFrames={F.verdict - F.gross}><AbsoluteFill style={{ background: BG_NIGHT }} /></Sequence>
      <Sequence from={F.verdict} durationInFrames={F.rewind - F.verdict} premountFor={fps}>
        <AbsoluteFill style={{ scale: slowPush(frame, F.verdict, F.rewind, 1.05) }}>
          <ClipScene src="shorts/s1_hang_8x.mp4" from={0} dur={F.rewind - F.verdict} push={[1, 1]} style={{ filter: "brightness(0.45) saturate(1.05)" }} />
        </AbsoluteFill>
      </Sequence>
      <ClipScene src="shorts/s5_hook_rev.mp4" from={F.rewind} dur={SHORT5_FRAMES - F.rewind} rate={117 / (SHORT5_FRAMES - F.rewind)} push={[1, 1]} />
    </AbsoluteFill>
  );
};

// Frame 0 and the end: the claim, labelled, beside the car that made the headlines.
const Hook: React.FC = () => {
  const frame = useCurrentFrame();
  if (!(frame < F.gross || frame >= F.rewind + 3)) return null;
  const punch = frame < F.gross ? interpolate(frame, [0, F.gross], [1, 1.03], CLAMP) : 1;
  return (
    <div style={{ position: "absolute", left: 60, top: 120, scale: punch, transformOrigin: "0% 0%" }}>
      <div style={{ ...HEADC, fontSize: 104, color: C.ink, ...keyline(0.7, 11) }}>TESLA&apos;S NET PROFIT</div>
      <div style={{ display: "flex", alignItems: "flex-end", gap: 22 }}>
        <div style={{ ...HEADC, fontSize: 300, color: C.warn, lineHeight: 0.84, ...keyline(2, 11) }}>−43%</div>
        <div style={{ ...MONO, fontSize: 60, color: C.ink, padding: "4px 12px", marginBottom: 26, backgroundColor: "rgba(0,0,0,0.75)" }}>GAAP</div>
      </div>
      <div style={{ display: "inline-block", marginTop: 14, padding: "6px 18px 9px", backgroundColor: C.ink, color: C.black, ...HEADC,
        fontSize: 56, border: `4px solid ${C.black}` }}>6 DAYS AFTER THIS ↓</div>
    </div>
  );
};

// gross profit: big horizontal bars
const Gross: React.FC = () => {
  const frame = useCurrentFrame();
  if (frame < F.gross || frame >= F.rnd) return null;
  return (
    <AbsoluteFill style={{ scale: slowPush(frame, F.gross, F.rnd, 1.04), transformOrigin: "30% 45%" }}>
      <Headline at={F.gross - 6} top={170} lines={[{ text: "GROSS PROFIT", size: 140, color: C.acid }]} />
      <Headline at={F.gross - 2} top={340} lines={[{ text: "WHAT'S LEFT AFTER MAKING", size: 66 }, { text: "WHAT IT SELLS", size: 66 }]} stroke={8} />
      <HBars at={F.gross + 22} top={560} max={6} width={620} rowH={300} labelSize={70} valueSize={104} rows={[
        { label: "Q3 2025", value: 5.054, show: (v) => `$${v.toFixed(2)}B`, color: "#8FA3B8" },
        { label: "Q3 2026", value: 5.494, show: (v) => `$${v.toFixed(2)}B`, color: C.acid },
      ]} />
      <Tag at={326} left={64} top={1150} bg={C.acid} size={120}>+9%</Tag>
    </AbsoluteFill>
  );
};

// research: rising columns
const RnD: React.FC = () => {
  const frame = useCurrentFrame();
  if (frame < F.rnd || frame >= F.quote) return null;
  const cols = [
    { label: "Q3 2025", v: 1.63, color: "#8FA3B8", x: 110, at: F.rnd + 30 },
    { label: "Q3 2026", v: 2.761, color: C.magenta, x: 590, at: F.rnd + 50 },
  ];
  const base = 1236, maxH = 690, maxV = 3;
  return (
    <AbsoluteFill style={{ scale: slowPush(frame, F.rnd, F.quote, 1.04), transformOrigin: "50% 70%" }}>
      <Headline at={F.rnd - 6} top={170} lines={[{ text: "THE DIFFERENCE:", size: 90 }, { text: "SPENDING", size: 120, color: C.magenta }]} />
      {cols.map((c) => {
        const k = interpolate(frame, [c.at, c.at + 24], [0, 1], { ...CLAMP, easing: EASE });
        const h = (maxH * c.v * k) / maxV;
        return (
          <div key={c.label}>
            <div style={{ position: "absolute", left: c.x, top: base - h, width: 380, height: h, backgroundColor: c.color, border: `6px solid ${C.black}` }} />
            <div style={{ position: "absolute", left: c.x, width: 380, top: base - h - 128, textAlign: "center", ...HEADC, fontSize: 110, color: c.color,
              opacity: k, ...keyline(0.8, 10), fontVariantNumeric: "tabular-nums" }}>${(c.v * k).toFixed(2)}B</div>
            <div style={{ position: "absolute", left: c.x, width: 380, top: base + 18, textAlign: "center", ...HEADC, fontSize: 60, color: C.ink,
              ...keyline(0.4, 8) }}>{c.label}</div>
          </div>
        );
      })}
      <Tag at={456} left={610} top={720} bg={C.ink} color={C.black} size={100}>+69%</Tag>
      <div style={{ position: "absolute", left: 110, top: 392, ...MONO, fontSize: 48, color: C.magenta, opacity: interpolate(frame, [F.rnd + 10, F.rnd + 20], [0, 1], CLAMP) }}>RESEARCH &amp; DEVELOPMENT</div>
    </AbsoluteFill>
  );
};

// Tesla's sentence, word for word, filling the frame; the causes light up as the narration names them.
const Quote: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < F.quote || frame >= F.credits) return null;
  const inQ = pop(frame, F.quote - 6, fps, 180, 15);
  const hi = (at: number) => interpolate(frame, [at, at + 8], [0, 1], CLAMP);
  const h1 = hi(F.quote + 4);    // research was just named
  const h2 = hi(490);            // "stock pay"
  const h3 = hi(547);            // "2025 award"
  const mark = (t: number, col: string = C.acid): React.CSSProperties => ({
    color: t > 0.5 ? C.black : C.ink,
    backgroundImage: `linear-gradient(${col}, ${col})`, backgroundRepeat: "no-repeat", backgroundSize: `${t * 100}% 100%`,
    padding: "0 6px", boxDecorationBreak: "clone", WebkitBoxDecorationBreak: "clone",
  });
  return (
    <AbsoluteFill style={{ scale: slowPush(frame, F.quote, F.credits, 1.03), transformOrigin: "20% 30%" }}>
      <Tag at={F.quote - 6} left={64} top={170} bg={C.ink} size={56}>TESLA&apos;S OWN WORDS</Tag>
      <div style={{ position: "absolute", left: 64, right: 90, top: 300, ...HEAD, fontVariationSettings: "'wdth' 88", fontWeight: 800,
        fontSize: 84, lineHeight: 1.14, color: C.ink, opacity: interpolate(inQ, [0, 0.3], [0, 1], CLAMP), translate: `0 ${(1 - inQ) * 40}px` }}>
        <span style={{ color: C.acid }}>“…</span>driven by{" "}
        <span style={mark(h1, C.magenta)}>SI and other R&amp;D projects</span>,{" "}
        <span style={mark(h2)}>SBC (including <span style={h3 > 0.5 ? { textDecoration: "underline", textDecorationThickness: 8 } : {}}>2025 CEO Performance Award</span>)</span> and SG&amp;A
        <span style={{ color: C.acid }}>”</span>
      </div>
      <div style={{ position: "absolute", left: 64, top: 1000, ...MONO, fontSize: 48, lineHeight: 1.35, color: C.cyan,
        opacity: interpolate(frame, [F.quote + 20, F.quote + 32], [0, 1], CLAMP) }}>
        SI = SUPER INTELLIGENCE,<br />TESLA&apos;S OWN TERM<br />SBC = STOCK-BASED PAY
      </div>
    </AbsoluteFill>
  );
};

// credits: one bar that shrinks, the lost part left as a ghost
const Credits: React.FC = () => {
  const frame = useCurrentFrame();
  if (frame < F.credits || frame >= F.adjusted) return null;
  const grow = interpolate(frame, [F.credits + 12, F.credits + 30], [0, 1], { ...CLAMP, easing: EASE });
  const shrink = interpolate(frame, [652, 676], [0, 1], { ...CLAMP, easing: Easing.bezier(0.65, 0, 0.35, 1) }); // "shrank"
  const W = 940;
  const v = interpolate(shrink, [0, 1], [417, 113]) * grow;
  const w = (W * v) / 417;
  return (
    <AbsoluteFill style={{ scale: slowPush(frame, F.credits, F.adjusted, 1.04), transformOrigin: "30% 50%" }}>
      <Headline at={F.credits - 6} top={170} lines={[{ text: "CREDITS SOLD TO", size: 102, color: C.cyan }, { text: "OTHER CARMAKERS", size: 102, color: C.cyan }]} />
      <div style={{ position: "absolute", left: 64, top: 430, ...MONO, fontSize: 48, color: "#D2CBE3",
        opacity: interpolate(frame, [F.credits + 10, F.credits + 20], [0, 1], CLAMP) }}>(REGULATORY CREDITS)</div>
      <div style={{ position: "absolute", left: 64, top: 580, width: W, height: 200, border: `6px dashed rgba(255,255,255,${0.55 * shrink})` }} />
      <div style={{ position: "absolute", left: 64, top: 580, width: w, height: 200, backgroundColor: shrink > 0.02 ? C.warn : "#8FA3B8",
        border: `6px solid ${C.black}` }} />
      <div style={{ position: "absolute", left: 64, top: 810, ...HEADC, fontSize: 150, color: shrink > 0.02 ? C.warn : C.ink, ...keyline(1, 10),
        fontVariantNumeric: "tabular-nums", opacity: grow }}>${Math.round(v)}M</div>
      <div style={{ position: "absolute", left: 64, top: 970, ...HEADC, fontSize: 64, color: C.ink, ...keyline(0.45, 8), opacity: grow }}>
        {shrink < 0.02 ? "Q3 2025" : "Q3 2026"}
      </div>
      <Tag at={662} left={560} top={620} bg={C.warn} color={C.ink} size={120}>−73%</Tag>
    </AbsoluteFill>
  );
};

// two ways to count it: GAAP vs Tesla's adjusted figure
const Adjusted: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < F.adjusted || frame >= F.verdict) return null;
  const a = pop(frame, F.adjusted + 6, fps, 200, 13);
  const b = pop(frame, 796, fps, 200, 13);     // "adjusted"
  const land = pop(frame, 853, fps, 260, 9);   // "four"
  const col = (x: number, s: number, title: string, sub: string, big: string, color: string, from: number, to: number, extra = 1): React.ReactNode => (
    <div style={{ position: "absolute", left: x, top: 420, width: 470, opacity: interpolate(s, [0, 0.3], [0, 1], CLAMP), translate: `0 ${(1 - s) * 50}px` }}>
      <div style={{ ...HEADC, fontSize: 64, color: C.ink, ...keyline(0.45, 8) }}>{title}</div>
      <div style={{ ...MONO, fontSize: 40, color: "#D2CBE3", marginTop: 6 }}>{sub}</div>
      <div style={{ ...HEADC, fontSize: 188, color, lineHeight: 0.9, marginTop: 30, ...keyline(1.3, 11), scale: extra, transformOrigin: "0% 100%" }}>{big}</div>
      <div style={{ ...HEADC, fontSize: 54, color: C.ink, marginTop: 20, ...keyline(0.4, 8) }}>${from.toFixed(2)}B → ${to.toFixed(2)}B</div>
    </div>
  );
  return (
    <AbsoluteFill style={{ scale: slowPush(frame, F.adjusted, F.verdict, 1.04), transformOrigin: "50% 40%" }}>
      <Headline at={F.adjusted - 6} top={170} lines={[{ text: "TWO WAYS TO COUNT IT", size: 90 }]} />
      {col(64, a, "NET PROFIT", "GAAP", "−43%", C.warn, 1.373, 0.787)}
      {col(590, b, "ADJUSTED", "TESLA'S NON-GAAP", "−4%", C.cyan, 1.77, 1.697, frame >= 853 ? interpolate(land, [0, 1], [1.15, 1]) : 1)}
      <div style={{ position: "absolute", left: 64, top: 1040, ...MONO, fontSize: 48, lineHeight: 1.35, color: "#D2CBE3", opacity: b }}>ADJUSTED = BEFORE STOCK PAY<br />AND A FEW OTHER ITEMS</div>
    </AbsoluteFill>
  );
};

const Verdict: React.FC = () => {
  const frame = useCurrentFrame();
  if (frame < F.verdict || frame >= F.rewind) return null;
  const lab = (at: number): React.CSSProperties => ({ ...MONO, fontSize: 52, color: "#D2CBE3", opacity: interpolate(frame, [at, at + 8], [0, 1], CLAMP) });
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", left: 64, top: 290, ...lab(F.verdict - 4) }}>THE HEADLINES</div>
      <Headline at={F.verdict - 2} top={360} lines={[{ text: "THE FLYING CAR", size: 132 }]} />
      <div style={{ position: "absolute", left: 64, top: 620, ...lab(932) }}>THE BILL</div>
      <Headline at={936} top={690} lines={[{ text: "STOCK PAY", size: 132, color: C.warn }, { text: "+ BETS ON WHAT'S NEXT", size: 92, color: C.acid }]} />
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
    <Adjusted />
    <Verdict />
    <Hook />
    <CaptionTrack pages={PAGES} hide={[[0, 24]]} until={F.rewind} />
    <Credit text="FOOTAGE: TESLA · SLOWED DOWN" show={[[0, F.gross], [F.verdict, SHORT5_FRAMES]]} />
    <Credit text={SOURCE} show={[[F.gross, F.verdict]]} />

    <Audio src={staticFile("shorts/s5_vo.mp3")} />
    <Audio src={staticFile("audio/sample-bed.mp3")} volume={(f) => interpolate(f, [0, 2, SHORT5_FRAMES - 24, SHORT5_FRAMES - 2, SHORT5_FRAMES],
      [0.06, 0.12, 0.12, 0.07, 0.06], CLAMP)} />
    <Sfx at={0} name="hiss" volume={0.55} dur={70} />
    <Sfx at={F.hover} name="whoosh" volume={0.35} />
    <Sfx at={F.gross} name="whoosh" volume={0.4} />
    <Sfx at={F.gross + 22} name="form" volume={0.35} />
    <Sfx at={326} name="thock" volume={0.6} />
    <Sfx at={F.rnd} name="whoosh" volume={0.4} />
    <Sfx at={F.rnd + 30} name="form" volume={0.35} />
    <Sfx at={456} name="thock" volume={0.6} />
    <Sfx at={F.quote} name="whoosh" volume={0.35} />
    <Sfx at={F.credits} name="whoosh" volume={0.4} />
    <Sfx at={652} name="settle" volume={0.5} />
    <Sfx at={662} name="thock" volume={0.7} />
    <Sfx at={F.adjusted} name="whoosh" volume={0.4} />
    <Sfx at={853} name="thock" volume={0.6} />
    <Sfx at={F.verdict} name="whoosh" volume={0.4} />
    <Sfx at={936} name="thock" volume={0.55} />
    <Sfx at={F.rewind} name="rewind" volume={0.45} />
  </AbsoluteFill>
);
