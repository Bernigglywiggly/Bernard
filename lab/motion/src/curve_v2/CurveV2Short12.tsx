import { Audio } from "@remotion/media";
import type React from "react";
import { AbsoluteFill, interpolate, Sequence, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { CLAMP, EASE_IN_OUT, EASE_OUT } from "../lib/anim";
import { Bed, C, CaptionTrack, HEADC, keyline, MONO, pop, Sfx, Stamp, Tag } from "./kit";
import { makePages } from "./pager";
import { VO_S12 } from "./voS12Captions";

// Curve Short 12 (Fri 30 Oct 2026): "Who Changes Your Phone's Clock?". 1080x1920, 30 fps. Built by account B on Thu 29
// Oct (scheduled run). Script lab/curve_v2/shorts/short12.py; facts lab/research/PHONE_CLOCK_FACTS.md, checks
// lab/curve_v2/shorts/short12_checks.md. Every picture is our own drawing: a generic phone (no logos, no real UI), a cell
// tower and a time server, the rulebook, the 2026 releases, the 2 a.m. rule, the verdict. No borrowed footage.
// Scenes are cued by spoken words (change, rulebook, first, tower, server, then, history, volunteers #2, six, for,
// first #2, two, go, our, volunteers #3, homework): a new take retimes them, and a missing cue word throws.

const PAGES = makePages(VO_S12);
const FPS = 30;
const bare = (s: string) => s.replace(/¶/g, "").trim().toLowerCase().replace(/[^a-z0-9%']/g, "");
const cue = (word: string, nth = 1, edge: "start" | "end" = "start") => {
  let seen = 0;
  for (const c of VO_S12) {
    if (bare(c.text) === word) {
      seen += 1;
      if (seen === nth) return Math.round(((edge === "start" ? c.startMs : c.endMs) / 1000) * FPS);
    }
  }
  throw new Error(`Short 12 cue: "${word}" #${nth} not found`);
};
const LAST_MS = VO_S12[VO_S12.length - 1].endMs;
const LOOP = 30; // the last second: back to frame 0's picture
export const SHORT12_FRAMES = Math.round((LAST_MS / 1000) * FPS) + 30 + LOOP;

const T = {
  change: cue("change"), rulebook: cue("rulebook"), first: cue("first"), tower: cue("tower"), server: cue("server"),
  then: cue("then"), where: cue("where"), history: cue("history"), volunteers2: cue("volunteers", 2), whenever: cue("whenever"),
  six: cue("six"), year: cue("year"), forr: cue("for"), first2: cue("first", 2), two: cue("two"), go: cue("go"),
  our: cue("our"), clock: cue("clock"), volunteers3: cue("volunteers", 3), homework: cue("homework"),
};
// the bed is 124 BPM and starts on a beat: scene cuts move onto the next kick
const BEAT = (FPS * 60) / 124;
const beatAfter = (f: number) => Math.round(Math.ceil(f / BEAT - 1e-6) * BEAT);
const S = {
  sources: beatAfter(T.first - 6), book: beatAfter(T.then - 4), releases: beatAfter(T.volunteers2 - 4),
  rule: beatAfter(T.forr - 4), verdict: beatAfter(T.our - 4), promise: T.homework - 14, loop: SHORT12_FRAMES - LOOP,
};
const DARK: React.CSSProperties = { position: "absolute", inset: 0, background: "radial-gradient(ellipse at 50% 40%, #1A1036 0%, #0A0718 55%, #020208 100%)" };
const between = (f: number, a: number, b: number) => f >= a && f < b;
const grow = (f: number, a: number, dur = 18) => interpolate(f, [a, a + dur], [0, 1], { ...CLAMP, easing: EASE_OUT });
const DIM = "#B8B2D6";
const SMALL = 68; // labels: 48 px cap height or more (CRAFT 18 Oct)
const Label: React.FC<{ children: React.ReactNode; left: number; top: number; size?: number; color?: string; opacity?: number;
  width?: number; align?: "left" | "center"; mono?: boolean }> = ({ children, left, top, size = 64, color = C.ink, opacity = 1, width, align = "left", mono }) => (
  <div style={{ position: "absolute", left, top, width, textAlign: align, ...(mono ? MONO : HEADC), whiteSpace: width ? "normal" : "nowrap", fontSize: size,
    lineHeight: 1, color, opacity, ...keyline(size / 140, 10) }}>{children}</div>
);

// ------------------------------------------------------------------------------------------------ our generic phone
// A plain slab with a pill-shaped camera cut-out: nobody's product. `roll` 0..1 rolls the time from `from` to `to`.
const Phone: React.FC<{ x: number; y: number; w: number; h: number; from: string; to?: string; roll?: number; date?: string;
  timeSize?: number; glow?: number }> = ({ x, y, w, h, from, to, roll = 0, date, timeSize = 210, glow = 0 }) => (
  <div style={{ position: "absolute", left: x, top: y, width: w, height: h, borderRadius: w * 0.14, backgroundColor: "#05030C",
    border: "8px solid #D8D4EA", boxShadow: `0 0 ${40 + 80 * glow}px rgba(120,220,255,${0.15 + 0.35 * glow})`, overflow: "hidden" }}>
    <div style={{ position: "absolute", inset: 14, borderRadius: w * 0.11, background: "linear-gradient(160deg, #2B1660 0%, #12082E 60%, #0B0620 100%)" }} />
    <div style={{ position: "absolute", left: w / 2 - 60, top: 30, width: 120, height: 34, borderRadius: 17, backgroundColor: "#05030C" }} />
    {date ? <Label left={0} top={h * 0.2} width={w - 16} align="center" size={56} color={DIM}>{date}</Label> : null}
    <div style={{ position: "absolute", left: 0, right: 0, top: h * 0.2 + 76, height: timeSize * 1.05, overflow: "hidden" }}>
      {[from, to].map((t, i) =>
        t === undefined ? null : (
          <div key={i} style={{ position: "absolute", left: 0, right: 0, top: (i - roll) * timeSize * 1.05, textAlign: "center", ...HEADC,
            fontSize: timeSize, lineHeight: 1.05, color: C.ink }}>{t}</div>
        ),
      )}
    </div>
  </div>
);
// the rulebook: a thick closed book, spine on the left
const Book: React.FC<{ x: number; y: number; s?: number; rot?: number }> = ({ x, y, s = 1, rot = 0 }) => (
  <div style={{ position: "absolute", left: x, top: y, width: 300, height: 400, scale: s, rotate: `${rot}deg`, transformOrigin: "50% 100%" }}>
    <div style={{ position: "absolute", left: 18, top: 14, width: 290, height: 396, backgroundColor: "#EDE6D3", borderRadius: 10, border: `5px solid ${C.black}` }} />
    <div style={{ position: "absolute", inset: 0, backgroundColor: "#3B2C7A", borderRadius: 12, border: `6px solid ${C.black}` }} />
    <div style={{ position: "absolute", left: 0, top: 0, bottom: 0, width: 46, backgroundColor: "#2A1F5C", borderRadius: "12px 0 0 12px", border: `6px solid ${C.black}` }} />
    <Label left={70} top={110} size={64} color={C.acid}>TIME</Label>
    <Label left={70} top={184} size={64} color={C.acid}>ZONE</Label>
    <Label left={70} top={258} size={64} color={C.acid}>RULES</Label>
  </div>
);

// ------------------------------------------------------------------------------------------------ x1: frame 0
const Kicker: React.FC<{ s?: number }> = ({ s = 1 }) => (
  <div style={{ position: "absolute", left: 60, top: 150, scale: s, transformOrigin: "0% 0%" }}>
    <Label left={0} top={0} size={96}>WHO CHANGES</Label>
    <Label left={0} top={104} size={96} color={C.acid}>THIS CLOCK?</Label>
  </div>
);
// the hook's picture as a pure function of t, so the loop can run it backwards into frame 0
const HookPicture: React.FC<{ t: number }> = ({ t }) => {
  const roll = interpolate(t, [T.change, T.change + 10], [0, 1], { ...CLAMP, easing: EASE_IN_OUT });
  const shift = interpolate(t, [T.rulebook - 6, T.rulebook + 6], [0, 1], { ...CLAMP, easing: EASE_OUT });
  const drop = interpolate(t, [T.rulebook - 2, T.rulebook + 8], [-700, 0], { ...CLAMP, easing: EASE_OUT });
  return (
    <AbsoluteFill style={{ scale: interpolate(t, [0, S.sources], [1, 1.035], CLAMP), transformOrigin: "50% 45%" }}>
      <div style={DARK} />
      <Phone x={300 - 210 * shift} y={420} w={480} h={820} date="SUN 1 NOV" from="1:59" to="1:00" roll={roll} glow={roll} />
      {t >= T.rulebook - 2 ? <div style={{ position: "absolute", left: 0, top: drop }}><Book x={600} y={600} rot={6} /></div> : null}
    </AbsoluteFill>
  );
};
const Hook: React.FC = () => {
  const frame = useCurrentFrame();
  if (frame >= S.sources) return null;
  return (
    <AbsoluteFill>
      <HookPicture t={frame} />
      <Kicker />
      <Tag at={T.change + 4} left={250} top={1120} bg={C.acid} size={60} rot={[-6, -3]} until={T.rulebook}>BACK ONE HOUR</Tag>
      <Tag at={T.rulebook + 8} left={560} top={1040} bg={C.ink} size={60} rot={[-5, -3]}>KEPT BY<br />VOLUNTEERS</Tag>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ x2: where the time comes from
const TOWER = { x: 230, y: 520 };
const SERVER = { x: 640, y: 560 };
const PH = { x: 540, y: 1000, w: 340, h: 380 };
const Pulse: React.FC<{ from: { x: number; y: number }; at: number; frame: number; color: string }> = ({ from, at, frame, color }) => {
  if (frame < at) return null;
  const to = { x: PH.x + PH.w / 2, y: PH.y + 60 };
  return (
    <>
      {[0, 1, 2].map((k) => {
        const q = ((frame - at) / 22 + k / 3) % 1;
        return <circle key={k} cx={from.x + (to.x - from.x) * q} cy={from.y + (to.y - from.y) * q} r={16} fill={color} opacity={1 - q * 0.6} />;
      })}
      <line x1={from.x} y1={from.y} x2={to.x} y2={to.y} stroke={color} strokeWidth={4} strokeDasharray="10 14" opacity={0.6} />
    </>
  );
};
const Sources: React.FC = () => {
  const frame = useCurrentFrame();
  if (!between(frame, S.sources, S.book)) return null;
  const towerIn = grow(frame, S.sources + 2, 12);
  const serverIn = grow(frame, T.server - 16, 12);
  const got = frame >= T.server + 6;
  return (
    <AbsoluteFill style={{ scale: interpolate(frame, [S.sources, S.book], [1, 1.035], CLAMP) }}>
      <div style={DARK} />
      <Label left={60} top={170} size={72} color={C.acid}>STEP 1 · THE TIME</Label>
      <svg width={1080} height={1920} style={{ position: "absolute", left: 0, top: 0 }}>
        <g opacity={towerIn}>
          {/* a lattice mast with two antennas */}
          <path d={`M ${TOWER.x - 90} 900 L ${TOWER.x} ${TOWER.y} L ${TOWER.x + 90} 900`} fill="none" stroke={C.ink} strokeWidth={10} />
          <path d={`M ${TOWER.x - 64} 790 L ${TOWER.x + 40} 680 M ${TOWER.x + 64} 790 L ${TOWER.x - 40} 680 M ${TOWER.x - 30} 620 L ${TOWER.x + 20} 580`} stroke={C.ink} strokeWidth={6} />
          <rect x={TOWER.x - 70} y={TOWER.y + 30} width={26} height={70} fill={DIM} stroke={C.black} strokeWidth={4} />
          <rect x={TOWER.x + 44} y={TOWER.y + 30} width={26} height={70} fill={DIM} stroke={C.black} strokeWidth={4} />
        </g>
        <g opacity={serverIn}>
          {[0, 1, 2].map((i) => (
            <g key={i}>
              <rect x={SERVER.x} y={SERVER.y + i * 100} width={300} height={84} rx={10} fill="#2A1F5C" stroke={C.ink} strokeWidth={6} />
              <circle cx={SERVER.x + 40} cy={SERVER.y + 42 + i * 100} r={12} fill={i === 0 && frame % 20 < 10 ? C.acid : DIM} />
              <rect x={SERVER.x + 80} y={SERVER.y + 34 + i * 100} width={180} height={14} rx={7} fill={DIM} opacity={0.6} />
            </g>
          ))}
        </g>
        <Pulse from={{ x: TOWER.x, y: TOWER.y + 60 }} at={T.tower - 2} frame={frame} color={C.cyan} />
        <Pulse from={{ x: SERVER.x + 150, y: SERVER.y + 290 }} at={T.server - 4} frame={frame} color={C.acid} />
      </svg>
      <Label left={TOWER.x - 170} top={920} size={SMALL} opacity={towerIn}>CELL TOWER</Label>
      <Label left={SERVER.x - 20} top={SERVER.y - 90} size={SMALL} opacity={serverIn}>TIME SERVER</Label>
      <Phone x={PH.x} y={PH.y} w={PH.w} h={PH.h} from="" to="05:59" roll={got ? 1 : interpolate(frame, [T.tower + 4, T.tower + 12], [0, 1], CLAMP)} timeSize={96} glow={0.4} />
      <Tag at={T.tower + 6} left={60} top={1100} bg={C.cyan} size={60} rot={[-5, -3]}>UTC</Tag>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ x3: the rulebook
const ZONES = ["ASIA/TOKYO", "EUROPE/LONDON", "AFRICA/CAIRO", "AMERICA/CHICAGO", "PACIFIC/AUCKLAND", "EUROPE/PARIS", "ASIA/KOLKATA",
  "AMERICA/DENVER", "AUSTRALIA/SYDNEY", "AMERICA/NEW_YORK", "AMERICA/PHOENIX", "EUROPE/BERLIN", "AMERICA/TORONTO", "ASIA/DUBAI"];
const NY = ZONES.indexOf("AMERICA/NEW_YORK");
const ROW = 92;
const Rulebook: React.FC = () => {
  const frame = useCurrentFrame();
  if (!between(frame, S.book, S.releases)) return null;
  const open = grow(frame, S.book, 10);
  // the list runs past and stops with AMERICA/NEW_YORK in the highlight band on "history"
  const stop = NY * ROW;
  const y = interpolate(frame, [T.where, T.history], [0, stop], { ...CLAMP, easing: EASE_OUT });
  const hit = frame >= T.history - 2;
  return (
    <AbsoluteFill style={{ scale: interpolate(frame, [S.book, S.releases], [1, 1.035], CLAMP) }}>
      <div style={DARK} />
      <Label left={60} top={170} size={72} color={C.acid}>STEP 2 · THE RULEBOOK</Label>
      <div style={{ position: "absolute", left: 60, top: 300, width: 860, height: 640, scale: interpolate(open, [0, 1], [0.92, 1]), opacity: open,
        backgroundColor: "#EDE6D3", border: `8px solid ${C.black}`, borderRadius: 14, overflow: "hidden" }}>
        <div style={{ position: "absolute", left: 0, right: 0, top: 274, height: ROW, backgroundColor: hit ? C.acid : "rgba(59,44,122,0.18)" }} />
        {ZONES.map((z, i) => (
          <div key={z} style={{ position: "absolute", left: 40, top: 280 + i * ROW - y, ...MONO, fontSize: 64, lineHeight: 1, color: "#1A1036",
            fontWeight: i === NY && hit ? 800 : 500 }}>{z}</div>
        ))}
      </div>
      <Tag at={T.history + 2} left={60} top={980} bg={C.ink} size={60} rot={[-4, -2]}>THE TIME ZONE DATABASE</Tag>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ x4: six rewrites this year
const RELEASES = ["2026A", "2026B", "2026C", "2026D", "2026E", "2026F"];
const Releases: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (!between(frame, S.releases, S.rule)) return null;
  const at = (i: number) => Math.round(T.whenever + ((T.six + 6 - T.whenever) * i) / (RELEASES.length - 1));
  return (
    <AbsoluteFill style={{ scale: interpolate(frame, [S.releases, S.rule], [1, 1.035], CLAMP) }}>
      <div style={DARK} />
      <Label left={60} top={170} size={72} color={C.acid}>REWRITTEN BY VOLUNTEERS</Label>
      {RELEASES.map((r, i) => {
        if (frame < at(i)) return null;
        const s = pop(frame, at(i), fps, 240, 12);
        return (
          <div key={r} style={{ position: "absolute", left: 60 + (i % 2) * 450, top: 320 + Math.floor(i / 2) * 190, width: 400, height: 150,
            backgroundColor: i === 5 ? C.acid : "#2A1F5C", border: `6px solid ${i === 5 ? C.black : C.ink}`, borderRadius: 14,
            scale: interpolate(s, [0, 1], [0.6, 1]), opacity: s }}>
            <Label left={34} top={38} size={80} color={i === 5 ? C.black : C.ink}>{r}</Label>
          </div>
        );
      })}
      <Stamp at={at(5) + 6} left={600} top={860} size={72} rot={-6} color={C.warn}>27 OCT</Stamp>
      <Tag at={T.six + 2} left={60} top={880} bg={C.ink} size={60} rot={[-4, -2]}>6 IN 2026 · IANA</Tag>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ x5: the US rule
const Rule: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (!between(frame, S.rule, S.verdict)) return null;
  const parts: [string, string, number][] = [
    ["FIRST SUN · NOV", C.ink, T.first2 - 2],
    ["02:00", C.cyan, T.two - 2],
    ["−1 HOUR", C.acid, T.go - 2],
  ];
  const roll = interpolate(frame, [T.go + 6, T.go + 16], [0, 1], { ...CLAMP, easing: EASE_IN_OUT });
  return (
    <AbsoluteFill style={{ scale: interpolate(frame, [S.rule, S.verdict], [1, 1.035], CLAMP) }}>
      <div style={DARK} />
      <Label left={60} top={170} size={72} color={C.acid}>THE RULE</Label>
      <Label left={60} top={256} size={SMALL} color={DIM} mono>AMERICA/NEW_YORK</Label>
      {parts.map(([txt, col, at], i) =>
        frame < at ? null : (
          <div key={txt} style={{ position: "absolute", left: 60, top: 380 + i * 150, scale: pop(frame, at, fps, 230, 12), transformOrigin: "0% 50%" }}>
            <Label left={0} top={0} size={124} color={col}>{txt}</Label>
          </div>
        ),
      )}
      <Phone x={600} y={860} w={300} h={420} from="1:59" to="1:00" roll={roll} timeSize={110} glow={roll} />
      <Tag at={T.forr + 4} left={60} top={880} bg={C.ink} size={60} rot={[-4, -2]}>MOST OF THE US</Tag>
      <Label left={60} top={990} size={56} color={DIM} opacity={grow(frame, T.forr + 10, 8)}>NOT HAWAII OR</Label>
      <Label left={60} top={1056} size={56} color={DIM} opacity={grow(frame, T.forr + 10, 8)}>MOST OF ARIZONA</Label>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ x6: the verdict
const Verdict: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (!between(frame, S.verdict, S.loop)) return null;
  const rows: [string, string, string, number][] = [
    ["WHO CHANGES IT →", "THE RULEBOOK", C.cyan, S.verdict + 2],
    ["WHO KEEPS IT →", "VOLUNTEERS", C.ink, T.clock - 2],
    ["OUR TAKE →", "IT RUNS ON HOMEWORK", C.acid, T.volunteers3 - 4],
  ];
  return (
    <AbsoluteFill style={{ scale: interpolate(frame, [S.verdict, S.loop], [1, 1.03], CLAMP) }}>
      <div style={DARK} />
      {rows.map(([a, b, col, at], i) => (
        <div key={b} style={{ position: "absolute", left: 60, top: 200 + i * 200, opacity: frame >= at ? 1 : 0, scale: pop(frame, at, fps, 230, 12), transformOrigin: "0% 50%" }}>
          <Label left={0} top={0} size={60}>{a}</Label>
          <Label left={0} top={70} size={b.length > 14 ? 84 : 100} color={col}>{b}</Label>
        </div>
      ))}
      <div style={{ opacity: grow(frame, S.verdict + 4, 10) }}>
        <Phone x={120} y={860} w={280} h={400} from="1:00" timeSize={100} glow={0.5} />
        <Book x={480} y={880} s={0.9} rot={4} />
      </div>
    </AbsoluteFill>
  );
};

// the channel's promise, as Shorts 8 and 11 end (CRAFT 24 Oct): gone before the loop so the last frame stays frame 0
const ChannelPromise: React.FC = () => {
  const frame = useCurrentFrame();
  if (!between(frame, S.promise, S.loop)) return null;
  return (
    <div style={{ position: "absolute", left: 60, top: 1340, padding: "6px 18px 10px", backgroundColor: C.acid, color: C.black,
      border: `4px solid ${C.black}`, ...HEADC, fontSize: 60, lineHeight: 0.92, opacity: interpolate(frame, [S.promise, S.promise + 6], [0, 1], CLAMP),
      translate: `0 ${interpolate(frame, [S.promise, S.promise + 8], [24, 0], { ...CLAMP, easing: EASE_OUT })}px` }}>
      THE CURVE: HOW NEW TECH<br />ACTUALLY WORKS
    </div>
  );
};

const LoopEnd: React.FC = () => {
  const frame = useCurrentFrame();
  if (frame < S.loop) return null;
  // eased, not sprung: the kicker sits at exactly scale 1 on the last frame, as on frame 0; the picture eases from the
  // phone at 1:00 back to 1:59 (t runs from just after "change" down to 0)
  const t = interpolate(frame, [S.loop, SHORT12_FRAMES - 1], [T.change + 10, 0], { ...CLAMP, easing: EASE_IN_OUT });
  const k = interpolate(frame, [S.loop + 14, S.loop + 24], [0, 1], { ...CLAMP, easing: EASE_OUT });
  return (
    <AbsoluteFill>
      <HookPicture t={t} />
      {frame >= S.loop + 14 ? <Kicker s={interpolate(k, [0, 1], [1.2, 1])} /> : null}
    </AbsoluteFill>
  );
};

export const CurveV2Short12: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: C.black }}>
    <Hook />
    <Sources />
    <Rulebook />
    <Releases />
    <Rule />
    <Verdict />
    <ChannelPromise />
    <LoopEnd />
    <CaptionTrack pages={PAGES} hide={[[0, 4], [S.promise, SHORT12_FRAMES]]} top={1400} />
    <Sequence from={0}><Audio src={staticFile("shorts/s12_vo.mp3")} /></Sequence>
    <Bed total={SHORT12_FRAMES} level={0.12} />
    <Sfx at={T.change + 2} name="thock" volume={0.4} />
    <Sfx at={S.sources} name="whoosh" volume={0.3} />
    <Sfx at={S.book} name="whoosh" volume={0.3} />
    <Sfx at={T.history - 2} name="settle" volume={0.35} />
    <Sfx at={S.releases} name="whoosh" volume={0.3} />
    <Sfx at={S.rule} name="whoosh" volume={0.3} />
    <Sfx at={T.go + 6} name="thock" volume={0.4} />
    <Sfx at={S.verdict} name="whoosh" volume={0.3} />
    <Sfx at={S.loop} name="rewind" volume={0.35} />
  </AbsoluteFill>
);
