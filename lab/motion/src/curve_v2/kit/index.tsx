import { Audio, Video } from "@remotion/media";
import type React from "react";
import { AbsoluteFill, interpolate, Sequence, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { CLAMP, EASE_OUT } from "../../lib/anim";
import { keyline } from "../HybridC";
import type { CapPage } from "../pager";
import { v2 } from "../palette";

// The Curve "clip, explained" kit (23 Oct 2026): the parts every Short repeats, lifted from Roadster Shorts 1-3 so a
// new Short is a timeline (F), one bespoke diagram and these pieces. Vertical 1080x1920 by default; every piece takes
// its position as props, so a 16:9 film can place it too.

export const C = v2.colors;
export { keyline };
export const HEAD: React.CSSProperties = { fontFamily: v2.fonts.heavy, fontWeight: 900, letterSpacing: "-0.02em", lineHeight: 0.9 };
export const HEADC: React.CSSProperties = { ...HEAD, fontVariationSettings: "'wdth' 82", whiteSpace: "nowrap" };
export const MONO: React.CSSProperties = { fontFamily: v2.fonts.mono, fontWeight: 500, letterSpacing: "0.02em" };
export const BG_NIGHT = "radial-gradient(ellipse at 50% 38%, #1B0B3A 0%, #0A0418 55%, #000000 100%)";
export const FILL: React.CSSProperties = { width: "100%", height: "100%", objectFit: "cover", filter: "saturate(1.1) contrast(1.06) brightness(1.05)" };

export const slowPush = (frame: number, a: number, b: number, to = 1.04) => interpolate(frame, [a, b], [1, to], CLAMP);
export const inRanges = (frame: number, ranges: [number, number][]) => ranges.some(([a, b]) => frame >= a && frame < b);
export const pop = (frame: number, at: number, fps: number, stiffness = 210, damping = 12) =>
  spring({ frame: frame - at, fps, config: { damping, stiffness } });

// A borrowed clip on screen for [from, from + dur), with a slow push so it never sits still.
export const ClipScene: React.FC<{ src: string; from: number; dur: number; rate?: number; trimBefore?: number;
  push?: [number, number]; origin?: string; style?: React.CSSProperties }> = ({ src, from, dur, rate = 1, trimBefore, push = [1, 1.04], origin = "50% 48%", style }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <Sequence from={from} durationInFrames={dur} premountFor={fps}>
      <AbsoluteFill style={{ scale: interpolate(frame, [from, from + dur], push, CLAMP), transformOrigin: origin }}>
        <Video src={staticFile(src)} muted playbackRate={rate} trimBefore={trimBefore} style={{ ...FILL, ...style }} />
      </AbsoluteFill>
    </Sequence>
  );
};

const QUIET = new Set(["a", "an", "the", "and", "or", "but", "so", "to", "of", "in", "on", "at", "by", "for", "with", "from", "it", "its", "is", "are",
  "was", "were", "be", "that", "this", "as", "than", "then", "yet", "also", "you're", "it's", "there"]);

// Word-by-word captions from makePages(); the word being spoken is acid. Long pages shrink to one line instead of
// wrapping (Short 3 lesson). Hidden in `hide` ranges, where the scene's own text would collide.
export const CaptionTrack: React.FC<{ pages: CapPage[]; top?: number; left?: number; right?: number; hide?: [number, number][];
  until?: number; maxSize?: number; width?: number }> = ({ pages, top = 1318, left = 70, right = 150, hide = [], until = Infinity, maxSize = 88, width = 800 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame >= until || inRanges(frame, hide)) return null;
  const ms = (frame / fps) * 1000;
  const page = pages.find((p, i) => ms >= p.startMs && ms < (pages[i + 1]?.startMs ?? p.startMs + p.durationMs + 600));
  if (!page) return null;
  const chars = page.tokens.map((t) => t.text).join("").trim().length;
  const size = Math.min(maxSize, Math.floor(width / (Math.max(chars, 1) * 0.6)));
  const s = interpolate(ms - page.startMs, [0, 90, 160], [0.9, 1.05, 1], CLAMP);
  const cur = page.tokens.reduce((acc, tk, j) => (tk.fromMs <= ms ? j : acc), -1);
  const plain = (t: string) => QUIET.has(t.trim().toLowerCase().replace(/[^a-z']/g, ""));
  return (
    <div style={{ position: "absolute", left, right, top, textAlign: "center", ...HEAD, fontVariationSettings: "'wdth' 88",
      fontSize: size, lineHeight: 1.04, textTransform: "uppercase", whiteSpace: "nowrap", scale: s }}>
      {page.tokens.map((t, i) => (
        <span key={`${t.fromMs}-${i}`} style={{ color: i === cur && !plain(t.text) ? C.acid : C.ink, ...keyline(0.6, 11) }}>{t.text}</span>
      ))}
    </div>
  );
};

// "FOOTAGE: OWNER / YOUTUBE, DATE · 10× SLOWER", shown whenever borrowed footage is on screen.
export const Credit: React.FC<{ text: string; show: [number, number][]; top?: number }> = ({ text, show, top = 1460 }) => {
  const frame = useCurrentFrame();
  if (!inRanges(frame, show)) return null;
  return (
    <div style={{ position: "absolute", left: 0, top, padding: "10px 22px 10px 60px", backgroundColor: "rgba(0,0,0,0.74)", ...MONO,
      fontSize: 44, color: C.ink }}>{text}</div>
  );
};

// A flat label that slaps in with a small rotation ("OUR MATH", "TESLA'S OWN TIMING").
export const Tag: React.FC<{ children: React.ReactNode; at: number; left: number; top: number; bg?: string; color?: string; size?: number;
  rot?: [number, number]; until?: number; style?: React.CSSProperties }> = ({ children, at, left, top, bg = C.ink, color = C.black, size = 54,
  rot = [-12, -2], until = Infinity, style }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < at || frame >= until) return null;
  const s = pop(frame, at, fps, 230, 10);
  return (
    <div style={{ position: "absolute", left, top, padding: "8px 18px 10px", backgroundColor: bg, color, border: `4px solid ${C.black}`,
      ...HEADC, fontSize: size, lineHeight: 1, scale: s, rotate: `${interpolate(s, [0, 1], rot)}deg`, transformOrigin: "0% 50%", ...style }}>
      {children}
    </div>
  );
};

// A rubber stamp verdict ("UNPROVEN", "BANNED"): lands big and settles.
export const Stamp: React.FC<{ children: React.ReactNode; at: number; left: number; top: number; color?: string; size?: number; rot?: number;
  until?: number }> = ({ children, at, left, top, color = C.warn, size = 96, rot = -7, until = Infinity }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < at || frame >= until) return null;
  const s = pop(frame, at, fps, 260, 9);
  return (
    <div style={{ position: "absolute", left, top, padding: "10px 26px 14px", border: `10px solid ${color}`, color, ...HEADC, fontSize: size,
      textAlign: "center", lineHeight: 0.95, backgroundColor: "rgba(0,0,0,0.55)", scale: interpolate(s, [0, 1], [1.8, 1]),
      opacity: interpolate(s, [0, 0.2], [0, 1], CLAMP), rotate: `${rot}deg` }}>{children}</div>
  );
};

// Stacked headline lines that rise in one after another.
export type Line = { text: React.ReactNode; color?: string; size: number; wdth?: number };
export const Headline: React.FC<{ lines: Line[]; at: number; left?: number; top: number; stagger?: number; until?: number; align?: "left" | "center";
  stroke?: number }> = ({ lines, at, left = 64, top, stagger = 5, until = Infinity, align = "left", stroke = 10 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < at || frame >= until) return null;
  return (
    <div style={{ position: "absolute", left: align === "center" ? 0 : left, right: align === "center" ? 0 : undefined, top, textAlign: align }}>
      {lines.map((ln, i) => {
        const s = pop(frame, at + i * stagger, fps, 200, 14);
        return (
          <div key={i} style={{ ...HEADC, fontVariationSettings: `'wdth' ${ln.wdth ?? 82}`, fontSize: ln.size, color: ln.color ?? C.ink,
            opacity: interpolate(s, [0, 0.3], [0, 1], CLAMP), translate: `0 ${(1 - s) * 40}px`, ...keyline(ln.size / 150, stroke) }}>{ln.text}</div>
        );
      })}
    </div>
  );
};

// Horizontal bars that grow from zero on a shared scale; the value counts up with its bar.
export type Bar = { label: string; value: number; show: (v: number) => string; color: string; note?: string };
export const HBars: React.FC<{ rows: Bar[]; at: number; max: number; top: number; left?: number; width?: number; rowH?: number; stagger?: number;
  grow?: number; until?: number; labelSize?: number; valueSize?: number }> = ({ rows, at, max, top, left = 64, width = 760, rowH = 210, stagger = 8,
  grow = 22, until = Infinity, labelSize = 56, valueSize = 96 }) => {
  const frame = useCurrentFrame();
  if (frame < at || frame >= until) return null;
  return (
    <div style={{ position: "absolute", left, top }}>
      {rows.map((r, i) => {
        const k = interpolate(frame, [at + i * stagger, at + i * stagger + grow], [0, 1], { ...CLAMP, easing: EASE_OUT });
        const v = r.value * k;
        return (
          <div key={r.label} style={{ position: "absolute", left: 0, top: i * rowH, width: width + 600 }}>
            <div style={{ ...HEADC, fontSize: labelSize, color: C.ink, ...keyline(labelSize / 140, 9) }}>{r.label}</div>
            <div style={{ display: "flex", alignItems: "center", gap: 22, marginTop: 10 }}>
              <div style={{ width: Math.max(8, (width * v) / max), height: 74, flexShrink: 0, backgroundColor: r.color, border: `5px solid ${C.black}` }} />
              <div style={{ ...HEADC, fontSize: valueSize, color: r.color, fontVariantNumeric: "tabular-nums", ...keyline(valueSize / 140, 10) }}>{r.show(v)}</div>
            </div>
            {r.note ? <div style={{ ...HEADC, fontSize: 40, color: "#C3CAD2", marginTop: 6, opacity: k, ...keyline(0.28, 7) }}>{r.note}</div> : null}
          </div>
        );
      })}
    </div>
  );
};

// The music bed holds one level to the last frame, so the loop back to frame 0 has no dip.
export const Bed: React.FC<{ total: number; level?: number; src?: string }> = ({ total, level = 0.13, src = "audio/sample-bed.mp3" }) => (
  <Audio src={staticFile(src)} volume={(f) => interpolate(f, [0, 2, total - 2, total], [level * 0.5, level, level, level * 0.5], CLAMP)} />
);

export const Sfx: React.FC<{ at: number; name: "whoosh" | "thock" | "form" | "hiss" | "rewind" | "riser" | "settle" | "tick_run"; volume?: number;
  dur?: number }> = ({ at, name, volume = 0.45, dur }) => (
  <Sequence from={at} durationInFrames={dur}><Audio src={staticFile(`sfx/${name}.mp3`)} volume={volume} /></Sequence>
);
