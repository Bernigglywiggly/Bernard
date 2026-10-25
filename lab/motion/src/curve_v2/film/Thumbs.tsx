import type React from "react";
import { AbsoluteFill, Img, staticFile } from "remotion";
import { C, HEADC, keyline, MONO } from "../kit";

// Thumbnails for "How the Flying Tesla Roadster Actually Works" (1280x720), three variants for Test & Compare, built to
// lab/tools/THUMBS.md: one focal subject, 2-5 keylined words, one honest device pointing at what the film shows, the
// Curve mark top-left, bottom-right left empty for the duration badge.
const Mark: React.FC = () => (
  <svg width={86} height={86} viewBox="0 0 100 100" style={{ position: "absolute", left: 28, top: 24 }}>
    <path d="M 14 80 C 44 80, 66 66, 78 24" fill="none" stroke="#000" strokeWidth={20} strokeLinecap="round" />
    <path d="M 14 80 C 44 80, 66 66, 78 24" fill="none" stroke={C.cyan} strokeWidth={13} strokeLinecap="round" />
    <circle cx={78} cy={22} r={12} fill={C.acid} stroke="#000" strokeWidth={3} />
  </svg>
);

// A: the real car hanging upside down, ring on it, "UPSIDE DOWN. HOW?"
export const ThumbA: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: C.black }}>
    <Img src={staticFile("film/thumb_hang.png")} style={{ position: "absolute", left: 380, top: 40, width: 1080, height: 608, scale: "1.3",
      transformOrigin: "35% 30%", filter: "saturate(1.1) contrast(1.12) brightness(1.15)" }} />
    <svg width={1280} height={720} style={{ position: "absolute", inset: 0 }}>
      <ellipse cx={950} cy={370} rx={135} ry={250} fill="none" stroke={C.acid} strokeWidth={14} />
    </svg>
    <div style={{ position: "absolute", left: 40, top: 150 }}>
      <div style={{ ...HEADC, fontSize: 150, color: C.ink, lineHeight: 0.9, ...keyline(1.1, 14) }}>UPSIDE</div>
      <div style={{ ...HEADC, fontSize: 150, color: C.ink, lineHeight: 0.9, ...keyline(1.1, 14) }}>DOWN.</div>
      <div style={{ ...HEADC, fontSize: 200, color: C.acid, lineHeight: 0.9, ...keyline(1.4, 16) }}>HOW?</div>
    </div>
    <Mark />
  </AbsoluteFill>
);

// B: our own 3D x-ray of the suction, "IT'S A VACUUM"
export const ThumbB: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: C.black }}>
    <Img src={staticFile("film/thumb_xray.png")} style={{ position: "absolute", left: 300, top: 0, width: 1280, height: 720, scale: "1.15", transformOrigin: "40% 40%" }} />
    <div style={{ position: "absolute", left: 0, top: 0, width: 640, height: 720, background: "linear-gradient(90deg, rgba(0,0,0,0.92) 55%, rgba(0,0,0,0) 100%)" }} />
    <div style={{ position: "absolute", left: 40, top: 160 }}>
      <div style={{ ...HEADC, fontSize: 130, color: C.ink, lineHeight: 0.9, ...keyline(1, 14) }}>IT&apos;S A</div>
      <div style={{ ...HEADC, fontSize: 190, color: C.magenta, lineHeight: 0.9, ...keyline(1.3, 16) }}>VACUUM</div>
      <div style={{ display: "inline-block", marginTop: 16, padding: "6px 16px 8px", backgroundColor: C.cyan, color: C.black, border: "4px solid #000",
        ...HEADC, fontSize: 52 }}>TESLA ROADSTER</div>
    </div>
    <Mark />
  </AbsoluteFill>
);

// C: the number, "0.81 s", on Tesla's own stopwatch
export const ThumbC: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: C.black }}>
    <Img src={staticFile("film/thumb_launch.png")} style={{ position: "absolute", left: 360, top: 120, width: 1080, height: 608, scale: "1.35",
      transformOrigin: "60% 40%", filter: "contrast(1.1) brightness(1.1)" }} />
    <div style={{ position: "absolute", left: 0, top: 0, width: 760, height: 720, background: "linear-gradient(90deg, rgba(0,0,0,0.92) 50%, rgba(0,0,0,0) 100%)" }} />
    <div style={{ position: "absolute", left: 36, top: 150 }}>
      <div style={{ ...HEADC, fontSize: 290, color: C.acid, lineHeight: 0.86, ...keyline(2, 16) }}>0.81s</div>
      <div style={{ display: "inline-block", marginTop: 18, padding: "8px 18px 10px", backgroundColor: C.ink, color: C.black, border: "4px solid #000",
        ...HEADC, fontSize: 64, rotate: "-3deg" }}>WHO TIMED IT?</div>
    </div>
    <div style={{ position: "absolute", left: 40, bottom: 40, ...MONO, fontSize: 30, color: "#C3CAD2" }}>0-60 MPH</div>
    <Mark />
  </AbsoluteFill>
);

// D (v2, for the title "Tesla Won't Promise the Flying Roadster Arrives"): the real car hanging upside down, Tesla's
// own US contract clause on a strip of paper, "OR IF?" (facts §13.1 #1). Complements the title instead of repeating it.
export const ThumbD: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: C.black }}>
    <Img src={staticFile("film/thumb_hang.png")} style={{ position: "absolute", left: 420, top: 20, width: 1080, height: 608, scale: "1.3",
      transformOrigin: "35% 30%", filter: "saturate(1.1) contrast(1.12) brightness(1.15)" }} />
    <div style={{ position: "absolute", left: 0, top: 0, width: 700, height: 720, background: "linear-gradient(90deg, rgba(0,0,0,0.9) 55%, rgba(0,0,0,0) 100%)" }} />
    <div style={{ position: "absolute", left: 40, top: 120 }}>
      <div style={{ ...HEADC, fontSize: 230, color: C.acid, lineHeight: 0.86, ...keyline(1.6, 16) }}>OR IF?</div>
    </div>
    <div style={{ position: "absolute", left: 36, top: 430, width: 700, padding: "18px 26px 22px", backgroundColor: "#FFFFFF", rotate: "-3deg",
      boxShadow: "0 16px 40px rgba(0,0,0,0.7)", border: "4px solid #000" }}>
      <div style={{ ...MONO, fontSize: 22, color: "#5E6670" }}>TESLA&apos;S US RESERVATION AGREEMENT</div>
      <div style={{ fontFamily: "Georgia, serif", fontSize: 40, lineHeight: 1.25, color: "#111318", marginTop: 6 }}>
        …will actually be delivered <span style={{ backgroundColor: C.acid, padding: "0 6px" }}>or if it will be delivered.</span>
      </div>
    </div>
    <Mark />
  </AbsoluteFill>
);
