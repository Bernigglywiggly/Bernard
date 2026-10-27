import { Audio } from "@remotion/media";
import type React from "react";
import { AbsoluteFill, interpolate, Sequence, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { CLAMP, EASE_IN_OUT } from "../lib/anim";
import { Bed, C, CaptionTrack, ClipScene, Credit, HEADC, keyline, MONO, pop, Sfx, Stamp, Tag } from "./kit";
import { makePages } from "./pager";
import { VO_S8 } from "./voS8Captions";

// Curve Short 8 (for Tue 27 Oct 2026): "iPhone Duo Crack: Why It Happens at the Fold". 1080x1920, 30 fps.
// Script lab/curve_v2/shorts/short8.py; facts lab/research/IPHONE_DUO_FACTS.md (rows in the comments). Frame 0 is the
// green line on JerryRigEverything's inner screen (the clip everyone is sharing); then our own bend diagram (one strip,
// a live stretch readout tied to the real numbers: 30 µm glass at a ~1.9 mm fold, OUR MATHS row 94), thick vs thin glass
// (row 91), Apple's own layer shot, glued vs sliding layers (book pages, row 93, illustrative), Apple's statement (row
// 34), and the fold glowing hottest before the hard cut back into the crack, so the Short loops. We never say what broke
// JRE's phone or that his line runs along the fold (rows 56-57). Every scene is cued by a spoken word (cue() below), so
// regenerating voS8Captions.ts from the real narration retimes the whole Short.

const PAGES = makePages(VO_S8);
// the narration: false until shorts/s8_vo.mp3 exists (voS8Captions.ts holds placeholder timings until then)
const HAS_VO = true;
const FPS = 30;
const bare = (s: string) => s.replace(/¶/g, "").trim().toLowerCase().replace(/[^a-z0-9%']/g, "");
const cue = (word: string, nth = 1, edge: "start" | "end" = "start") => {
  let seen = 0;
  for (const c of VO_S8) {
    if (bare(c.text) === word) {
      seen += 1;
      if (seen === nth) return Math.round(((edge === "start" ? c.startMs : c.endMs) / 1000) * FPS);
    }
  }
  throw new Error(`Short 8 cue: "${word}" #${nth} not found`);
};
const LAST_MS = VO_S8[VO_S8.length - 1].endMs;
const LOOP = 30; // the last second: back into the crack, landing on frame 0's picture
export const SHORT8_FRAMES = Math.round((LAST_MS / 1000) * FPS) + 16 + LOOP;

const T = {
  stretches: cue("stretches"), cracks: cue("cracks"), bend: cue("bend"), thicker: cue("thicker"), tighter: cue("tighter"),
  ordinary: cue("ordinary"), shatter: cue("shatter"), thirty: cue("30"), thats: cue("that's"), toughened: cue("toughened"),
  book: cue("book"), apple: cue("apple"), small: cue("small"), replacing: cue("replacing"), verdict: cue("so", 3),
  hardest: cue("hardest"), reported: cue("reported"),
};
const S = {
  hookEnd: T.stretches - 3, bendEnd: T.ordinary - 2, glassEnd: T.thats - 2, layersShot: T.thats - 2, stack: T.book - 22,
  apple: T.apple - 2, verdict: T.verdict - 2, loop: SHORT8_FRAMES - LOOP,
};
const DARK: React.CSSProperties = { position: "absolute", inset: 0, background: "radial-gradient(ellipse at 50% 42%, #10224A 0%, #070D1F 55%, #02040A 100%)" };
const SHADE_TOP: React.CSSProperties = { position: "absolute", left: 0, right: 0, top: 0, height: 900,
  background: "linear-gradient(180deg, rgba(1,4,14,0.88) 0%, rgba(1,4,14,0.55) 60%, rgba(1,4,14,0) 100%)" };
const between = (f: number, a: number, b: number) => f >= a && f < b;
const ease = (f: number, a: number, b: number) => interpolate(f, [a, b], [0, 1], { ...CLAMP, easing: EASE_IN_OUT });

// ------------------------------------------------------------------------------------------------ geometry
// A strip of length L whose middle A bends into an arc of angle th (0 = flat, PI = a U opening upwards); (cx, cy) is the
// bottom of the bend. Returns the centre line as an SVG path, offset `off` px towards the outside of the bend.
const strip = (cx: number, cy: number, L: number, A: number, th: number, off = 0, arm?: number) => {
  const a = arm ?? (L - A) / 2;
  if (th < 0.02) return `M ${cx - L / 2} ${cy + off} L ${cx + L / 2} ${cy + off}`;
  const R = A / th + off; // the outer side of the bend sits below the centre line
  const ox = cx, oy = cy - A / th; // centre of the arc
  const P = (p: number) => [ox + R * Math.sin(p), oy + R * Math.cos(p)];
  const [x1, y1] = P(-th / 2);
  const [x2, y2] = P(th / 2);
  const tx = Math.cos(th / 2), ty = -Math.sin(th / 2);
  return `M ${x1 - tx * a} ${y1 + ty * a} L ${x1} ${y1} A ${R} ${R} 0 0 0 ${x2} ${y2} L ${x2 + tx * a} ${y2 + ty * a}`;
};

// ------------------------------------------------------------------------------------------------ 1. the crack (frame 0 and the loop)
const Hook: React.FC = () => {
  const frame = useCurrentFrame();
  if (!(frame < S.hookEnd || frame >= S.loop)) return null;
  return (
    <AbsoluteFill>
      <div style={{ ...SHADE_TOP, height: 760 }} />
      <div style={{ position: "absolute", left: 64, top: 250, ...HEADC, fontSize: 136, color: C.ink, lineHeight: 0.92, ...keyline(0.9, 11) }}>WHY DO IPHONE</div>
      <div style={{ position: "absolute", left: 64, top: 376, ...HEADC, fontSize: 136, color: C.acid, lineHeight: 0.92, ...keyline(0.9, 11) }}>DUOS CRACK?</div>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ 2. one strip, bending
const Bend: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (!between(frame, S.hookEnd, S.bendEnd)) return null;
  const fold = ease(frame, S.hookEnd + 4, T.cracks + 6); // 0 -> 1 = flat -> folded
  // d2: thicker, then tighter, each makes the outside stretch more
  const thick = 1 + 0.9 * ease(frame, T.thicker - 4, T.thicker + 12);
  const tight = 1 + 0.55 * ease(frame, T.tighter - 4, T.tighter + 12);
  const th = Math.PI * fold;
  const L = 900, A = 520 / tight, t = 34 * thick;
  const stretch = 0.79 * fold; // % at the real numbers (30 µm, ~1.9 mm fold); the thicker/tighter beats show the rule instead
  const hot = Math.min(1, stretch / 1.0);
  const formula = pop(frame, T.bend + 2, fps, 220, 13);
  const limitIn = ease(frame, T.cracks - 6, T.cracks + 6);
  return (
    <AbsoluteFill>
      <div style={DARK} />
      <svg width={1080} height={1920} style={{ position: "absolute", inset: 0 }}>
        <defs>
          <marker id="s8arr" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
            <path d="M0 0 L10 5 L0 10 Z" fill={C.warn} />
          </marker>
        </defs>
        {/* the strip and its hot outer face */}
        <path d={strip(540, 1230, L, A, th)} fill="none" stroke="#1B3A66" strokeWidth={t + 12} strokeLinecap="round" />
        <path d={strip(540, 1230, L, A, th)} fill="none" stroke={C.cyan} strokeWidth={t} strokeLinecap="round" opacity={0.85} />
        <path d={strip(540, 1230, L, A, th, t / 2)} fill="none" stroke={`rgb(255,${Math.round(220 - 150 * hot)},${Math.round(60 - 40 * hot)})`}
          strokeWidth={10} strokeLinecap="round" opacity={0.3 + 0.7 * fold} />
        {/* stretch arrows on the outside of the bend */}
        {fold > 0.35 ? [-0.32, 0, 0.32].map((p) => {
          const R = A / th + t / 2 + 46;
          const cx = 540 + R * Math.sin(p * th), cy = 1230 - A / th + R * Math.cos(p * th);
          const dx = Math.cos(p * th) * 44, dy = -Math.sin(p * th) * 44;
          return <line key={p} x1={cx - dx} y1={cy - dy} x2={cx + dx} y2={cy + dy} stroke={C.warn} strokeWidth={9} markerStart="url(#s8arr)"
            markerEnd="url(#s8arr)" opacity={ease(frame, S.hookEnd + 30, S.hookEnd + 40)} />;
        }) : null}
      </svg>
      {/* the readout against glass's limit (d1), then the rule takes the top of the frame (d2) */}
      <div style={{ position: "absolute", left: 64, top: 230, opacity: 1 - ease(frame, T.bend - 4, T.bend + 6) }}>
        <div style={{ ...HEADC, fontSize: 70, color: C.ink, ...keyline(0.5, 9) }}>THE OUTSIDE STRETCHES</div>
        <div style={{ ...HEADC, fontSize: 250, color: hot > 0.75 ? C.warn : C.acid, lineHeight: 0.9, fontVariantNumeric: "tabular-nums", ...keyline(1.6, 12) }}>
          {stretch.toFixed(1)}%
        </div>
        <div style={{ position: "relative", width: 900, height: 44, marginTop: 18, border: "5px solid #000", backgroundColor: "rgba(255,255,255,0.12)" }}>
          <div style={{ width: `${Math.min(100, (stretch / 1.6) * 100)}%`, height: "100%", backgroundColor: hot > 0.75 ? C.warn : C.acid }} />
          <div style={{ position: "absolute", left: `${(1 / 1.6) * 100}%`, top: -18, bottom: -18, width: 8, backgroundColor: C.ink, opacity: limitIn }} />
        </div>
        <div style={{ ...HEADC, fontSize: 52, color: C.ink, marginTop: 14, marginLeft: `${(1 / 1.6) * 900 - 160}px`, opacity: limitIn, ...keyline(0.4, 8) }}>GLASS CRACKS ≈1%</div>
      </div>
      <Tag at={S.hookEnd + 10} until={T.bend - 2} left={64} top={790} bg={C.acid} size={46} rot={[-6, -2]}>OUR MATHS · 30 µm GLASS, ~1.9 mm FOLD</Tag>
      {frame >= T.bend ? (
        <div style={{ position: "absolute", left: 0, right: 0, top: 250, textAlign: "center", opacity: interpolate(formula, [0, 0.3], [0, 1], CLAMP),
          translate: `0 ${(1 - formula) * 30}px` }}>
          <div style={{ ...HEADC, fontSize: 120, color: C.ink, ...keyline(0.8, 11) }}>STRETCH = t ÷ 2r</div>
          <div style={{ ...MONO, fontSize: 40, color: "#C9D3E0", marginTop: 10 }}>t = THICKNESS · r = BEND RADIUS</div>
        </div>
      ) : null}
      <Tag at={T.thicker - 2} left={64} top={500} bg={C.warn} color={C.ink} size={48} rot={[-6, -2]}>2× THICKER → 2× THE STRETCH</Tag>
      <Tag at={T.tighter - 2} left={64} top={590} bg={C.warn} color={C.ink} size={48} rot={[5, 1]}>2× TIGHTER → 2× THE STRETCH</Tag>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ 3. thick glass vs thin glass
const Glass: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (!between(frame, S.bendEnd, S.glassEnd)) return null;
  const fold = ease(frame, S.bendEnd + 2, T.shatter - 2);
  const th = Math.PI * 0.82 * fold;
  const crack = pop(frame, T.shatter - 2, fps, 260, 9);
  const thin = pop(frame, T.thirty - 4, fps, 220, 12);
  const shards = frame >= T.shatter - 2;
  const col = (cx: number, t: number, color: string, broken: boolean) => (
    <g>
      <path d={strip(cx, 1180, 440, 300, th)} fill="none" stroke={color} strokeWidth={t} strokeLinecap="round" opacity={broken ? 1 - 0.5 * crack : 1} />
      {broken && shards ? [-0.3, -0.1, 0.12, 0.31].map((p, i) => {
        const R = 300 / Math.max(th, 0.05);
        const x = cx + R * Math.sin(p * th), y = 1180 - R + R * Math.cos(p * th);
        return <path key={i} d={`M ${x} ${y - t} l ${-14 + i * 9} ${t * 0.7} l 16 ${t * 0.5} l -10 ${t * 0.8}`} fill="none" stroke={C.warn}
          strokeWidth={7} opacity={crack} />;
      }) : null}
    </g>
  );
  return (
    <AbsoluteFill>
      <div style={DARK} />
      <svg width={1080} height={1920} style={{ position: "absolute", inset: 0 }}>
        {col(300, 64, "#9FB4C8", true)}
        {col(800, 10, C.cyan, false)}
      </svg>
      <div style={{ position: "absolute", left: 64, top: 230, width: 470 }}>
        <div style={{ ...HEADC, fontSize: 64, color: C.ink, whiteSpace: "normal", lineHeight: 1, ...keyline(0.45, 8) }}>ORDINARY PHONE GLASS</div>
        <div style={{ ...MONO, fontSize: 44, color: "#C9D3E0", marginTop: 8 }}>0.5 mm</div>
        <div style={{ ...HEADC, fontSize: 150, color: C.warn, marginTop: 10, opacity: interpolate(crack, [0, 0.3], [0, 1], CLAMP), ...keyline(1, 11) }}>13%+</div>
        <div style={{ ...HEADC, fontSize: 64, color: C.warn, opacity: interpolate(crack, [0, 0.3], [0, 1], CLAMP), ...keyline(0.45, 8) }}>SHATTERS</div>
      </div>
      <div style={{ position: "absolute", left: 600, top: 230, width: 420 }}>
        <div style={{ ...HEADC, fontSize: 64, color: C.ink, whiteSpace: "normal", lineHeight: 1, ...keyline(0.45, 8) }}>FOLDABLE GLASS</div>
        <div style={{ ...MONO, fontSize: 44, color: "#C9D3E0", marginTop: 8 }}>30 µm</div>
        <div style={{ ...HEADC, fontSize: 150, color: C.cyan, marginTop: 10, opacity: interpolate(thin, [0, 0.3], [0, 1], CLAMP), ...keyline(1, 11) }}>0.8%</div>
        <div style={{ ...HEADC, fontSize: 64, color: C.cyan, opacity: interpolate(thin, [0, 0.3], [0, 1], CLAMP), ...keyline(0.45, 8) }}>BENDS</div>
      </div>
      <Tag at={S.bendEnd + 8} left={64} top={760} bg={C.acid} size={46} rot={[-6, -2]}>OUR MATHS · SAME ~1.9 mm FOLD</Tag>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ 4. the layers, glued vs sliding (book pages)
const N = 10; // the tag says 10 layers, so draw 10 (thinner strips, closer, same overall size as the old 7)
const LAYER = ["#E9EEF5", "#8FD7FF", "#3DFFF2", "#FF2BD6", "#8FD7FF", "#F2C14E", "#3DFFF2", "#FF2BD6", "#8FD7FF", "#B7BEC8"]; // polymer, glass, OLED, glue, glass, glue, OLED, glue, glass, titanium
const Stack: React.FC<{ fold: number; slide: number; hot: number }> = ({ fold, slide, hot }) => {
  const th = Math.PI * fold;
  const L = 860, A0 = 300, gap = 15;
  return (
    <svg width={1080} height={1920} style={{ position: "absolute", inset: 0 }}>
      {Array.from({ length: N }).map((_, i) => {
        // glued: every layer keeps the inner layer's arms, so the outer ones must stretch; sliding: each keeps its own length
        const off = i * gap;
        const arcI = (A0 / Math.max(th, 0.02) + off) * th;
        const armGlued = (L - A0) / 2;
        const armSlide = (L - arcI) / 2;
        const arm = armGlued + (armSlide - armGlued) * slide;
        const heat = (1 - slide) * (i / (N - 1)) * hot;
        return (
          <path key={i} d={strip(540, 1300, L, A0, th, off, arm)} fill="none" strokeLinecap="round" strokeWidth={10}
            stroke={heat > 0.05 ? `rgb(255,${Math.round(200 - 140 * heat)},${Math.round(80 - 60 * heat)})` : LAYER[i]} />
        );
      })}
    </svg>
  );
};
const Layers: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (!between(frame, S.stack, S.apple)) return null;
  const fold = ease(frame, S.stack, S.stack + 20);
  const slide = ease(frame, T.book - 4, T.book + 14);
  const glued = frame < T.book - 4;
  const lab = pop(frame, glued ? S.stack + 6 : T.book - 4, fps, 230, 12);
  return (
    <AbsoluteFill>
      <div style={DARK} />
      <Stack fold={fold * 0.92} slide={slide} hot={fold} />
      <div style={{ position: "absolute", left: 64, top: 230, opacity: interpolate(lab, [0, 0.3], [0, 1], CLAMP) }}>
        <div style={{ ...HEADC, fontSize: 92, color: glued ? C.warn : C.cyan, lineHeight: 0.95, ...keyline(0.7, 10) }}>{glued ? "GLUED SOLID" : "SLIDING LIKE"}</div>
        <div style={{ ...HEADC, fontSize: 92, color: glued ? C.warn : C.cyan, lineHeight: 0.95, ...keyline(0.7, 10) }}>{glued ? "OUTER LAYER 7.9%" : "BOOK PAGES: 0.8%"}</div>
      </div>
      <Tag at={S.stack + 10} left={64} top={500} bg={C.ink} size={44} rot={[-5, -2]}>ILLUSTRATIVE · 10 LAYERS OF 30 µm<br />AT A ~1.9 mm FOLD</Tag>
      <Tag at={T.book + 6} left={64} top={650}bg={C.acid} size={44} rot={[4, 1]}>APPLE: LAYERS &quot;GLIDE&quot; PAST EACH OTHER</Tag>
    </AbsoluteFill>
  );
};

const LayersShotTag: React.FC = () => {
  const frame = useCurrentFrame();
  if (!between(frame, S.layersShot, S.stack)) return null;
  return (
    <>
      <div style={{ ...SHADE_TOP, height: 700 }} />
      <Tag at={S.layersShot + 2} left={64} top={230} bg={C.ink} size={58} rot={[-5, -2]}>APPLE: &quot;MORE THAN 10<br />ULTRATHIN LAYERS&quot;</Tag>
    </>
  );
};

// ------------------------------------------------------------------------------------------------ 5. Apple's words
const AppleSays: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (!between(frame, S.apple, S.verdict)) return null;
  const q = pop(frame, T.small - 6, fps, 210, 14);
  return (
    <AbsoluteFill>
      <div style={{ ...SHADE_TOP, height: 1100 }} />
      <Tag at={S.apple + 2} left={64} top={200} bg={C.ink} size={48} rot={[-5, -2]}>APPLE, TO MACRUMORS · 26 OCT</Tag>
      <div style={{ position: "absolute", left: 64, top: 300, width: 950, opacity: interpolate(q, [0, 0.3], [0, 1], CLAMP), translate: `0 ${(1 - q) * 30}px` }}>
        <div style={{ ...HEADC, whiteSpace: "normal", fontSize: 72, color: C.ink, lineHeight: 1.02, ...keyline(0.6, 10) }}>
          “AN ISSUE IMPACTING<br />THE INNER DISPLAY ON<br />A SMALL NUMBER OF<br />IPHONE DUO UNITS”
        </div>
      </div>
      <Stamp at={T.replacing - 2} left={70} top={690} size={74} color={C.acid}>APPLECARE<br />REPLACEMENT</Stamp>
      <Tag at={T.replacing + 10} left={64} top={930} bg={C.warn} color={C.ink} size={44} rot={[5, 1]}>NO CAUSE GIVEN</Tag>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ 6. the verdict: the fold works hardest
const Verdict: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (!between(frame, S.verdict, S.loop)) return null;
  const glow = 0.6 + 0.4 * Math.sin((frame - S.verdict) / 4);
  const h = pop(frame, T.hardest - 6, fps, 220, 12);
  return (
    <AbsoluteFill>
      <div style={DARK} />
      <Stack fold={0.92} slide={1} hot={1} />
      <svg width={1080} height={1920} style={{ position: "absolute", inset: 0 }}>
        <ellipse cx={540} cy={1340} rx={260} ry={120} fill={C.warn} opacity={0.18 * glow} />
      </svg>
      <div style={{ position: "absolute", left: 64, top: 230, opacity: interpolate(h, [0, 0.3], [0, 1], CLAMP), translate: `0 ${(1 - h) * 30}px` }}>
        <div style={{ ...HEADC, fontSize: 120, color: C.ink, lineHeight: 0.92, ...keyline(0.85, 11) }}>THE FOLD</div>
        <div style={{ ...HEADC, fontSize: 120, color: C.warn, lineHeight: 0.92, ...keyline(0.85, 11) }}>WORKS HARDEST</div>
      </div>
      <Tag at={T.reported - 2} left={64} top={520} bg={C.ink} size={44} rot={[-5, -2]}>REPORTED CRACKS: ALONG THE HINGE</Tag>
    </AbsoluteFill>
  );
};

// dark band behind the captions while Apple's bright footage is on screen (white captions vanish on it otherwise)
const CapScrim: React.FC = () => {
  const frame = useCurrentFrame();
  const w = ([[S.layersShot, S.stack], [S.apple, S.verdict]] as [number, number][]).find(([a, b]) => between(frame, a, b));
  if (!w) return null;
  const o = Math.min(interpolate(frame, [w[0], w[0] + 6], [0, 1], CLAMP), interpolate(frame, [w[1] - 6, w[1]], [1, 0], CLAMP));
  return (
    <div style={{ position: "absolute", left: 0, right: 0, top: 1180, height: 560, opacity: o,
      background: "linear-gradient(180deg, rgba(6,9,14,0) 0%, rgba(6,9,14,0.74) 32%, rgba(6,9,14,0.74) 76%, rgba(6,9,14,0) 100%)" }} />
  );
};

export const CurveV2Short8: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: C.black }}>
    {/* pictures: the crack at frame 0; Apple's own layer and unfold shots; the crack again for the loop */}
    <ClipScene src="shorts/s8_hook.mp4" from={0} dur={S.hookEnd} push={[1, 1.04]} origin="50% 55%" />
    <ClipScene src="shorts/s8_layers.mp4" from={S.layersShot} dur={S.stack - S.layersShot} push={[1.02, 1.07]} />
    <ClipScene src="shorts/s8_unfold.mp4" from={S.apple} dur={S.verdict - S.apple} push={[1, 1.05]} />
    <ClipScene src="shorts/s8_loop.mp4" from={S.loop} dur={LOOP} push={[1.04, 1]} origin="50% 55%" />
    <Bend />
    <Glass />
    <LayersShotTag />
    <Layers />
    <AppleSays />
    <Verdict />
    <Hook />
    <CapScrim />
    <CaptionTrack pages={PAGES} hide={[[0, S.hookEnd], [S.loop, SHORT8_FRAMES]]} top={1360} />
    <Credit text="JERRYRIGEVERYTHING · BEND TEST" show={[[0, S.hookEnd], [S.loop, SHORT8_FRAMES]]} />
    <Credit text="APPLE · YOUTUBE" show={[[S.layersShot, S.stack], [S.apple, S.verdict]]} />
    {HAS_VO ? <Sequence from={0}><Audio src={staticFile("shorts/s8_vo.mp3")} /></Sequence> : null}
    <Bed total={SHORT8_FRAMES} level={0.12} />
    <Sfx at={S.hookEnd} name="whoosh" volume={0.3} />
    <Sfx at={T.cracks - 2} name="thock" volume={0.45} />
    <Sfx at={S.bendEnd} name="whoosh" volume={0.3} />
    <Sfx at={T.shatter - 2} name="thock" volume={0.55} />
    <Sfx at={S.layersShot} name="whoosh" volume={0.3} />
    <Sfx at={T.book - 4} name="settle" volume={0.35} />
    <Sfx at={S.apple} name="whoosh" volume={0.3} />
    <Sfx at={T.replacing - 2} name="thock" volume={0.45} />
    <Sfx at={S.verdict} name="whoosh" volume={0.3} />
    <Sfx at={S.loop} name="whoosh" volume={0.25} />
  </AbsoluteFill>
);
