import type React from "react";
import { AbsoluteFill } from "remotion";
import { C, HEADC, keyline, MONO } from "./kit";

// The Curve brand stills for the 23 Oct 2026 repositioning ("the story behind the clip everyone is sharing"): the
// v2 palette and Archivo type replace the ASCII/AI look. Banner 2560x1440 (YouTube's every-device safe area is the
// central 1546x423, x 507-2053, y 508-931); avatar 800x800 (read at 40 px, so one bold mark).

const BG = "radial-gradient(ellipse at 50% 50%, #2A0E5C 0%, #14052E 45%, #05010C 100%)";

// The mark: a rising curve with a dot at its tip, drawn magenta to cyan.
const Mark: React.FC<{ size: number; stroke: number }> = ({ size, stroke }) => (
  <svg width={size} height={size} viewBox="0 0 100 100">
    <defs>
      <linearGradient id="curveGrad" x1="0" y1="1" x2="1" y2="0">
        <stop offset="0%" stopColor={C.magenta} />
        <stop offset="100%" stopColor={C.cyan} />
      </linearGradient>
    </defs>
    <path d="M 14 80 C 44 80, 66 66, 78 24" fill="none" stroke="#000" strokeWidth={stroke + 6} strokeLinecap="round" />
    <path d="M 14 80 C 44 80, 66 66, 78 24" fill="none" stroke="url(#curveGrad)" strokeWidth={stroke} strokeLinecap="round" />
    <circle cx={78} cy={22} r={stroke * 0.95} fill={C.acid} stroke="#000" strokeWidth={3} />
  </svg>
);

// Small line drawings for the wide desktop/TV band outside the safe area: our own glyphs, no logos.
const CarUpsideDown: React.FC = () => (
  <svg width={360} height={140} viewBox="0 0 190 64" style={{ rotate: "180deg" }}>
    <path d="M 8 44 C 10 30, 40 24, 70 20 C 92 8, 128 8, 150 22 C 170 26, 184 32, 184 44 Z" fill={C.cyan} stroke="#000" strokeWidth={5} />
    <circle cx={50} cy={46} r={14} fill="#15181D" stroke="#000" strokeWidth={4} />
    <circle cx={146} cy={46} r={14} fill="#15181D" stroke="#000" strokeWidth={4} />
  </svg>
);
const Rocket: React.FC = () => (
  <svg width={150} height={300} viewBox="0 0 60 120">
    <path d="M 30 4 C 44 18, 46 44, 44 80 L 16 80 C 14 44, 16 18, 30 4 Z" fill={C.ink} stroke="#000" strokeWidth={4} />
    <path d="M 16 64 L 4 92 L 16 86 Z M 44 64 L 56 92 L 44 86 Z" fill={C.magenta} stroke="#000" strokeWidth={4} />
    <path d="M 20 82 C 22 100, 26 110, 30 118 C 34 110, 38 100, 40 82 Z" fill={C.acid} stroke="#000" strokeWidth={3} />
  </svg>
);
const Robot: React.FC = () => (
  <svg width={190} height={300} viewBox="0 0 76 120">
    <rect x={24} y={4} width={28} height={22} rx={6} fill={C.ink} stroke="#000" strokeWidth={4} />
    <rect x={30} y={12} width={16} height={5} rx={2} fill={C.cyan} />
    <rect x={18} y={30} width={40} height={42} rx={8} fill={C.ink} stroke="#000" strokeWidth={4} />
    <path d="M 18 36 L 4 62 M 58 36 L 72 20" stroke={C.ink} strokeWidth={9} strokeLinecap="round" />
    <path d="M 28 72 L 22 114 M 48 72 L 58 112" stroke={C.ink} strokeWidth={10} strokeLinecap="round" />
  </svg>
);
const Chart: React.FC = () => (
  <svg width={320} height={200} viewBox="0 0 160 100">
    <path d="M 6 90 L 40 70 L 66 78 L 100 40 L 124 50 L 154 10" fill="none" stroke="#000" strokeWidth={12} strokeLinejoin="round" strokeLinecap="round" />
    <path d="M 6 90 L 40 70 L 66 78 L 100 40 L 124 50 L 154 10" fill="none" stroke={C.acid} strokeWidth={7} strokeLinejoin="round" strokeLinecap="round" />
  </svg>
);

export const CurveBanner: React.FC = () => (
  <AbsoluteFill style={{ background: BG }}>
    {/* wide band (desktop/TV only), kept clear of the safe area */}
    <div style={{ position: "absolute", left: 70, top: 540, opacity: 0.92 }}><CarUpsideDown /></div>
    <div style={{ position: "absolute", left: 130, top: 720, opacity: 0.92 }}><Chart /></div>
    <div style={{ position: "absolute", left: 2110, top: 570, opacity: 0.92 }}><Rocket /></div>
    <div style={{ position: "absolute", left: 2300, top: 600, opacity: 0.92 }}><Robot /></div>
    {/* safe area: x 507-2053, y 508-931 */}
    <div style={{ position: "absolute", left: 507, top: 508, width: 1546, height: 423, display: "flex", flexDirection: "column", alignItems: "center",
      justifyContent: "center" }}>
      <div style={{ display: "flex", alignItems: "center", gap: 26 }}>
        <div style={{ flexShrink: 0, marginTop: -20 }}><Mark size={230} stroke={11} /></div>
        <div style={{ ...HEADC, fontSize: 230, color: C.ink, ...keyline(1.5, 10) }}>THE CURVE</div>
      </div>
      <div style={{ ...HEADC, fontVariationSettings: "'wdth' 88", fontSize: 56, color: C.acid, marginTop: 10, ...keyline(0.4, 9) }}>
        THE STORY BEHIND THE CLIP EVERYONE&apos;S SHARING
      </div>
      <div style={{ ...MONO, fontSize: 40, color: C.cyan, marginTop: 18 }}>TECH · CARS · SPACE · ROBOTS · MONEY</div>
    </div>
  </AbsoluteFill>
);

export const CurveAvatar: React.FC = () => (
  <AbsoluteFill style={{ background: BG, alignItems: "center", justifyContent: "center" }}>
    <Mark size={640} stroke={12} />
  </AbsoluteFill>
);
