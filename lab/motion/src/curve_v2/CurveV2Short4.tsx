import { Audio, Video } from "@remotion/media";
import { evolvePath } from "@remotion/paths";
import type React from "react";
import { AbsoluteFill, Img, interpolate, Sequence, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { CLAMP, EASE_IN_OUT, EASE_OUT } from "../lib/anim";
import { BG_NIGHT, C, CaptionTrack, ClipScene, Credit, FILL, HEADC, Headline, keyline, MONO, pop, Sfx, slowPush, Stamp, Tag } from "./kit";
import { makePages } from "./pager";
import { HERO_TRACK } from "./s4HeroTrack";
import { VO_S4_CAPTIONS } from "./voS4Captions";

// Curve Short 4 v2 (Sat 24 Oct 2026): "How Unitree's Kung Fu Robot Learned to Fight". 1080x1920, 30 fps.
// v2 applies critic round 1 (lab/curve_v2/shorts/out/critic_s4/round1.md): line 1 states Unitree's claim and teases the
// small print; the flip plays at real speed, then the 7x replay; the knife scene is shown full width so the attacker
// and the woman are in frame; the 4,096 reveal shows copies walking (that config is a walking trainer); the
// 50-a-second line plays over our own 3D robot with its centre of mass tracked from Blender, not over Unitree's robot;
// a music dip and hit mark the twist; a 3D-to-real match-cut carries the verdict; text >= 44 px and clear of the
// Shorts buttons. Facts: lab/research/UNITREE_H2X_FACTS.md. Footage: Unitree Robotics, YouTube, 21 Oct 2026
// (Y3zb4o47yqA). Narration s4_chris_v5_tight.mp3 (34.2 s). Cuts on the 124 BPM beat. Last frame = frame 0.

export const SHORT4_FRAMES = 1044;

const F = { replay: 18, tease: 117, mocap: 218, practise: 348, reveal: 508, balance: 639, print: 769, knife: 857, verdict: 929,
  real: 947, rewind: 1022, hold0: 1034 };
const PAGES = makePages(VO_S4_CAPTIONS);
const DARKEN: React.CSSProperties = { position: "absolute", left: 0, right: 0, top: 0, height: 820,
  background: "linear-gradient(180deg, rgba(5,1,12,0.85) 0%, rgba(5,1,12,0.55) 60%, rgba(5,1,12,0) 100%)" };
const DISCLOSE: React.CSSProperties = { position: "absolute", left: 64, top: 150, ...MONO, fontSize: 40, color: "#C9C2DA" };

// ------------------------------------------------------------------------------------------------ backgrounds
const BlurBg: React.FC<{ src: string; trim?: number }> = ({ src, trim = 0 }) => (
  <AbsoluteFill>
    <Video src={staticFile(src)} muted trimBefore={trim} style={{ ...FILL, filter: "blur(18px) brightness(0.35)", scale: "1.2" }} />
  </AbsoluteFill>
);

const Footage: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill style={{ backgroundColor: C.black }}>
      <ClipScene src="shorts/s4_real.mp4" from={0} dur={F.replay} push={[1, 1.01]} origin="50% 30%" />
      <ClipScene src="shorts/s4_hook.mp4" from={F.replay} dur={F.tease - F.replay} rate={92 / 99} push={[1, 1.06]} origin="50% 30%" />
      {/* the bodyguard tease: Unitree's knife scene at full width, so the attacker and the woman are both in frame */}
      <Sequence from={F.tease} durationInFrames={F.mocap - F.tease} premountFor={fps}>
        <BlurBg src="shorts/s4_knife_wide.mp4" />
        <div style={{ position: "absolute", left: -270, top: 520, width: 1350, height: 760, scale: slowPush(frame, F.tease, F.mocap, 1.04), transformOrigin: "80% 50%" }}>
          <Video src={staticFile("shorts/s4_knife_wide.mp4")} muted style={{ width: 1350, height: 760, display: "block" }} />
        </div>
      </Sequence>
      <Sequence from={F.mocap} durationInFrames={F.practise - F.mocap}><AbsoluteFill style={{ background: BG_NIGHT }} /></Sequence>
      <ClipScene src="shorts/s4_sim_e.mp4" from={F.practise} dur={F.reveal - F.practise} rate={145 / 160} push={[1, 1.03]} />
      <ClipScene src="shorts/s4_sim_f.mp4" from={F.reveal} dur={F.balance - F.reveal} rate={136 / 131} push={[1, 1]} />
      {/* no push on the hero shot: the overlay is tracked to its pixels */}
      <ClipScene src="shorts/s4_sim_hero.mp4" from={F.balance} dur={F.print - F.balance} push={[1, 1]} />
      <Sequence from={F.print} durationInFrames={F.knife - F.print} premountFor={fps}>
        <BlurBg src="shorts/s4_balance.mp4" trim={70} />
      </Sequence>
      <Sequence from={F.knife} durationInFrames={F.verdict - F.knife} premountFor={fps}>
        <BlurBg src="shorts/s4_knife_wide.mp4" trim={60} />
        <div style={{ position: "absolute", left: -270, top: 600, width: 1350, height: 760, scale: slowPush(frame, F.knife, F.verdict, 1.05), transformOrigin: "80% 50%" }}>
          <Video src={staticFile("shorts/s4_knife_wide.mp4")} muted trimBefore={60} style={{ width: 1350, height: 760, display: "block" }} />
        </div>
      </Sequence>
      {/* verdict: our 3D copy mid-kick match-cuts into the real robot's kick */}
      <ClipScene src="shorts/s4_sim_hero.mp4" from={F.verdict} dur={F.real - F.verdict} trimBefore={60} push={[1.04, 1.1]} origin="50% 50%" />
      <ClipScene src="shorts/s4_kick.mp4" from={F.real} dur={F.rewind - F.real} push={[1.02, 1.07]} style={{ filter: "brightness(0.5) saturate(0.95)" }} />
      <ClipScene src="shorts/s4_real_rev.mp4" from={F.rewind} dur={SHORT4_FRAMES - F.rewind} rate={18 / (SHORT4_FRAMES - F.rewind)} push={[1, 1]} />
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ hook (frame 0 and the end)
const Hook: React.FC = () => {
  const frame = useCurrentFrame();
  if (!(frame < F.tease || frame >= F.hold0)) return null;
  const receipt = frame < F.tease ? interpolate(frame, [30, 42], [0, 1], { ...CLAMP, easing: EASE_OUT }) : 0;
  const punch = frame < F.tease ? interpolate(frame, [0, F.tease], [1, 1.03], CLAMP) : 1;
  return (
    <>
      <div style={{ position: "absolute", left: 60, top: 770, scale: punch, transformOrigin: "0% 50%" }}>
        <div style={{ ...HEADC, fontSize: 110, color: C.ink, ...keyline(0.75, 11) }}>UNITREE SAYS</div>
        <div style={{ ...HEADC, fontSize: 168, color: C.acid, lineHeight: 0.86, ...keyline(1.1, 11) }}>IT&apos;S REAL.</div>
        <div style={{ display: "inline-block", marginTop: 16, padding: "6px 16px 9px", backgroundColor: C.ink, color: C.black, ...HEADC,
          fontSize: 52, border: `4px solid ${C.black}`, opacity: frame >= 20 && frame < F.tease ? 1 : 0 }}>NOW READ THE SMALL PRINT ↓</div>
      </div>
      {receipt > 0 ? (
        <div style={{ position: "absolute", left: 60, top: 1170, width: 880, opacity: receipt, translate: `${(1 - receipt) * -80}px 0`,
          border: `5px solid ${C.acid}`, backgroundColor: C.black }}>
          <Img src={staticFile("shorts/s4_label_speed.png")} style={{ width: 870, display: "block" }} />
        </div>
      ) : null}
    </>
  );
};

const Tease: React.FC = () => {
  const frame = useCurrentFrame();
  if (frame < F.tease || frame >= F.mocap) return null;
  return (
    <AbsoluteFill>
      <Headline at={F.tease + 4} top={250} lines={[{ text: "BUT THE", size: 120 }, { text: "BODYGUARD?", size: 160, color: C.acid }]} />
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ step 1: copy a person
type P2 = [number, number];
const POSE: Record<string, P2> = {
  head: [210, 70], neck: [205, 140], shL: [150, 165], shR: [262, 160], elL: [92, 230], haL: [70, 150], elR: [318, 236], haR: [356, 312],
  hip: [205, 380], hipL: [178, 384], hipR: [234, 376], knL: [168, 548], ftL: [160, 712], knR: [338, 318], ftR: [470, 236],
};
const BONES: [string, string][] = [["neck", "hip"], ["shL", "shR"], ["shL", "elL"], ["elL", "haL"], ["shR", "elR"], ["elR", "haR"],
  ["hipL", "hipR"], ["hipL", "knL"], ["knL", "ftL"], ["hipR", "knR"], ["knR", "ftR"], ["neck", "head"]];
const MARKERS = ["head", "shL", "elL", "haL", "shR", "elR", "haR", "hipL", "knL", "ftL", "hipR", "knR", "ftR"];
const HX = 40, RX = 560, BY = 500;

const Mocap: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < F.mocap || frame >= F.practise) return null;
  const s = pop(frame, F.mocap + 2, fps, 190, 14);
  const robotIn = pop(frame, F.mocap + 14, fps, 190, 14);
  const at = (k: number) => F.mocap + 68 + k * 4.2; // the links draw one by one through "joint by joint" (~10.1-11.4 s)
  const P = (x: number, k: string): P2 => [x + POSE[k][0], BY + POSE[k][1]];
  return (
    <AbsoluteFill style={{ scale: slowPush(frame, F.mocap, F.practise, 1.05), transformOrigin: "50% 50%" }}>
      <Tag at={F.mocap + 2} left={64} top={170} bg={C.acid} size={52}>STEP 1</Tag>
      <Headline at={F.mocap + 6} top={250} lines={[{ text: "COPY A PERSON", size: 132, color: C.ink }]} />
      <svg width={1080} height={1920} style={{ position: "absolute", inset: 0 }}>
        <g opacity={interpolate(s, [0, 0.4], [0, 1], CLAMP)} transform={`rotate(${Math.sin(frame / 9) * 2} ${HX + 205} ${BY + 380})`}>
          {BONES.map(([a, b]) => {
            const [x1, y1] = P(HX, a); const [x2, y2] = P(HX, b);
            return <line key={a + b} x1={x1} y1={y1} x2={x2} y2={y2} stroke="#4A5068" strokeWidth={38} strokeLinecap="round" />;
          })}
          <circle cx={P(HX, "head")[0]} cy={P(HX, "head")[1]} r={44} fill="#4A5068" />
          {MARKERS.map((k, i) => {
            const on = frame >= at(i);
            return <circle key={k} cx={P(HX, k)[0]} cy={P(HX, k)[1]} r={on ? 14 : 11} fill={C.magenta} stroke={C.ink} strokeWidth={on ? 5 : 3} />;
          })}
        </g>
        <g opacity={interpolate(robotIn, [0, 0.4], [0, 1], CLAMP)} transform={`translate(0 ${(1 - robotIn) * 40}) rotate(${Math.sin(frame / 9 + 0.6) * 2} ${RX + 205} ${BY + 380})`}>
          {BONES.map(([a, b]) => {
            const [x1, y1] = P(RX, a); const [x2, y2] = P(RX, b);
            return <line key={a + b} x1={x1} y1={y1} x2={x2} y2={y2} stroke={C.ink} strokeWidth={30} strokeLinecap="round" />;
          })}
          <rect x={P(RX, "head")[0] - 40} y={P(RX, "head")[1] - 46} width={80} height={92} rx={26} fill={C.ink} stroke="#000" strokeWidth={5} />
          <rect x={P(RX, "head")[0] - 28} y={P(RX, "head")[1] - 10} width={56} height={18} rx={8} fill={C.cyan} />
          {MARKERS.filter((k) => k !== "head").map((k) => {
            const i = MARKERS.indexOf(k);
            const on = frame >= at(i) + 4;
            return <circle key={k} cx={P(RX, k)[0]} cy={P(RX, k)[1]} r={15} fill="#11141B" stroke={on ? C.cyan : "#59606E"} strokeWidth={on ? 6 : 4} />;
          })}
        </g>
        {MARKERS.map((k, i) => {
          const [x1, y1] = P(HX, k); const [x2, y2] = P(RX, k);
          const midY = Math.min(y1, y2) - 90 - (i % 3) * 30;
          const d = `M ${x1} ${y1} Q ${(x1 + x2) / 2} ${midY} ${x2} ${y2}`;
          const t = interpolate(frame, [at(i), at(i) + 10], [0, 1], { ...CLAMP, easing: EASE_OUT });
          if (t <= 0) return null;
          const ev = evolvePath(t, d);
          return <path key={k} d={d} fill="none" stroke={C.cyan} strokeWidth={5} strokeLinecap="round" strokeDasharray={ev.strokeDasharray}
            strokeDashoffset={ev.strokeDashoffset} opacity={0.9} />;
        })}
      </svg>
      <div style={{ position: "absolute", left: HX + 40, top: 1240, ...HEADC, fontSize: 52, color: C.magenta, ...keyline(0.35, 7) }}>PERSON</div>
      <div style={{ position: "absolute", left: RX + 120, top: 1240, ...HEADC, fontSize: 52, color: C.cyan, ...keyline(0.35, 7) }}>ROBOT</div>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ step 2 and the 4,096
const SimLabels: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const inPractise = frame >= F.practise && frame < F.reveal;
  const inReveal = frame >= F.reveal && frame < F.balance;
  if (!inPractise && !inReveal) return null;
  const bf = 101 + (frame - F.practise) * (145 / 160);
  const floorShare = interpolate(bf, [100, 250], [0.55, 0.05], CLAMP);
  const count = Math.round(interpolate(frame, [F.reveal + 32, F.reveal + 92], [1, 4096], { ...CLAMP, easing: EASE_OUT }));
  const landed = pop(frame, F.reveal + 92, fps, 260, 9);
  return (
    <AbsoluteFill>
      <div style={DARKEN} />
      <div style={DISCLOSE}>OUR 3D ILLUSTRATION OF A SIMULATOR</div>
      {inPractise ? (
        <>
          <Tag at={F.practise + 2} left={64} top={230} bg={C.acid} size={52}>STEP 2</Tag>
          <Headline at={F.practise + 6} top={310} lines={[{ text: "PRACTISE IN A", size: 112 }, { text: "SIMULATOR", size: 112, color: C.cyan }]} />
          <div style={{ position: "absolute", left: 64, top: 580, ...HEADC, fontSize: 56, color: C.ink, ...keyline(0.38, 8),
            opacity: interpolate(frame, [F.practise + 40, F.practise + 52], [0, 1], CLAMP) }}>
            ON THE FLOOR
            <div style={{ marginTop: 10, width: 560, height: 32, border: `4px solid ${C.black}`, backgroundColor: "rgba(255,255,255,0.18)" }}>
              <div style={{ width: `${(floorShare * 100) / 0.55}%`, height: "100%", backgroundColor: C.warn }} />
            </div>
          </div>
        </>
      ) : null}
      {inReveal ? (
        <div style={{ position: "absolute", left: 64, top: 220 }}>
          <div style={{ ...HEADC, fontSize: 240, color: C.acid, lineHeight: 0.86, fontVariantNumeric: "tabular-nums", ...keyline(1.6, 11),
            scale: frame >= F.reveal + 92 ? interpolate(landed, [0, 1], [1.12, 1]) : 1, transformOrigin: "0% 100%",
            opacity: interpolate(frame, [F.reveal + 22, F.reveal + 34], [0, 1], CLAMP) }}>{count.toLocaleString("en-GB")}</div>
          <div style={{ ...HEADC, fontSize: 76, color: C.ink, marginTop: 46, ...keyline(0.52, 9),
            opacity: interpolate(frame, [F.reveal + 44, F.reveal + 56], [0, 1], CLAMP) }}>VIRTUAL ROBOTS AT ONCE</div>
        </div>
      ) : null}
      {inReveal ? <Tag at={F.reveal + 96} left={64} top={600} bg={C.cyan} size={46}>DEFAULT IN UNITREE&apos;S PUBLIC CODE</Tag> : null}
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ 50 a second, on our 3D robot
const Balance: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < F.balance || frame >= F.print) return null;
  const i = Math.min(HERO_TRACK.length - 1, Math.max(0, frame - F.balance));
  const [[cx, cy], [fx, fy]] = HERO_TRACK[i];
  const show = interpolate(frame, [F.balance + 10, F.balance + 22], [0, 1], CLAMP);
  const sec = (frame - (F.balance + 70)) / fps; // ticks run once "50" is said (~23.9 s)
  const lit = sec < 0 ? 0 : Math.floor((sec % 1) * 50) + 1;
  const pulse = (frame - F.balance) % 6 < 2 ? 1 : 0; // a correction blip every few frames
  return (
    <AbsoluteFill>
      <div style={DARKEN} />
      <div style={DISCLOSE}>OUR 3D ILLUSTRATION</div>
      <Headline at={F.balance + 4} top={230} lines={[{ text: "THE CONTROLLER ADJUSTS IT", size: 64 }]} />
      <Headline at={F.balance + 66} top={320} lines={[{ text: "50× A SECOND", size: 150, color: C.acid }]} stroke={11} />
      <svg width={1080} height={120} style={{ position: "absolute", left: 0, top: 480 }}>
        {Array.from({ length: 50 }).map((_, k) => (
          <rect key={k} x={64 + k * 19} y={20} width={13} height={k % 10 === 0 ? 70 : 50} fill={k < lit ? C.acid : "rgba(255,255,255,0.22)"}
            stroke="#000" strokeWidth={2} />
        ))}
      </svg>
      <Tag at={F.balance + 80} left={64} top={610} bg={C.cyan} size={44}>IN UNITREE&apos;S PUBLIC CODE: EVERY 0.02 s</Tag>
      {/* centre of mass over the stance foot, tracked from the Blender camera */}
      <svg width={1080} height={1920} style={{ position: "absolute", inset: 0, opacity: show }}>
        <line x1={cx} y1={cy} x2={fx} y2={fy} stroke={C.ink} strokeWidth={4} strokeDasharray="14 10" />
        <ellipse cx={fx} cy={fy + 6} rx={70} ry={16} fill="none" stroke={C.cyan} strokeWidth={5} />
        <circle cx={cx} cy={cy} r={26 + pulse * 6} fill="none" stroke={C.acid} strokeWidth={6} />
        <circle cx={cx} cy={cy} r={8} fill={C.acid} />
        <line x1={cx - 44} y1={cy} x2={cx + 44} y2={cy} stroke={C.acid} strokeWidth={3} />
        <line x1={cx} y1={cy - 44} x2={cx} y2={cy + 44} stroke={C.acid} strokeWidth={3} />
      </svg>
      <div style={{ position: "absolute", left: cx + 46, top: cy - 70, ...HEADC, fontSize: 46, color: C.acid, opacity: show, ...keyline(0.32, 7) }}>BALANCE POINT</div>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ the small print
const SmallPrint: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < F.print || frame >= F.knife) return null;
  const inS = pop(frame, F.print + 2, fps, 200, 15);
  const z = interpolate(frame, [F.print + 8, F.print + 34], [0, 1], { ...CLAMP, easing: EASE_IN_OUT });
  const k = interpolate(z, [0, 1], [1080 / 1920, 1000 / 760]);
  const left = interpolate(z, [0, 1], [0, 40 - 1160 * (1000 / 760)]);
  const top = interpolate(z, [0, 1], [640, 640 - 30 * (1000 / 760)]);
  const drift = interpolate(frame, [F.print + 34, F.knife], [1, 1.05], CLAMP);
  const box8 = interpolate(frame, [805, 813], [0, 1], { ...CLAMP, easing: EASE_OUT });  // "eight-hour" 26.8 s
  const under = interpolate(frame, [838, 852], [0, 1], { ...CLAMP, easing: EASE_OUT }); // "standing" 28.0 s
  return (
    <AbsoluteFill>
      <Tag at={F.print + 2} left={64} top={250} bg={C.ink} size={56}>THE VIDEO&apos;S OWN SMALL PRINT</Tag>
      <div style={{ position: "absolute", left: 0, top: 0, width: 1920, height: 1080, transformOrigin: "0 0",
        translate: `${left}px ${top + (1 - inS) * 60}px`, scale: k * drift, opacity: interpolate(inS, [0, 0.3], [0, 1], CLAMP) }}>
        <Img src={staticFile("shorts/s4_src_24.png")} style={{ width: 1920, height: 1080, display: "block" }} />
        <div style={{ position: "absolute", left: 1752, top: 86, width: 142, height: 50, border: `${7 / k}px solid ${C.acid}`, opacity: box8 }} />
        <div style={{ position: "absolute", left: 1224, top: 130, height: 9, width: 178 * under, backgroundColor: C.acid }} />
      </div>
      <div style={{ position: "absolute", left: 64, top: 860, ...HEADC, fontSize: 70, color: C.acid, opacity: under, ...keyline(0.5, 10),
        translate: `0 ${(1 - under) * 30}px` }}>STANDING, NOT FIGHTING</div>
    </AbsoluteFill>
  );
};

const KnifeLabel: React.FC = () => {
  const frame = useCurrentFrame();
  if (frame < F.knife || frame >= F.verdict) return null;
  const k = interpolate(frame, [F.knife + 10, F.knife + 20], [0, 1], { ...CLAMP, easing: EASE_OUT });
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", left: 40, top: 300, opacity: k, translate: `${(1 - k) * -60}px 0`, border: `5px solid ${C.warn}`,
        backgroundColor: C.black }}>
        <Img src={staticFile("shorts/s4_label_demo.png")} style={{ width: 760, display: "block" }} />
      </div>
      <Stamp at={902} left={60} top={460} size={96}>A DEMONSTRATION</Stamp>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ verdict
const Verdict: React.FC = () => {
  const frame = useCurrentFrame();
  if (frame < F.verdict || frame >= F.rewind) return null;
  return (
    <AbsoluteFill>
      <Headline at={F.verdict + 6} top={400} lines={[{ text: "THE KICKS", size: 150 }]} />
      <Tag at={948} left={64} top={570} bg={C.acid} size={96} rot={[-10, -3]}>REAL</Tag>
      <Headline at={968} top={800} lines={[{ text: "THE BODYGUARD", size: 116 }]} />
      <Stamp at={980} left={64} top={960} size={104}>STILL A DEMO</Stamp>
    </AbsoluteFill>
  );
};

export const CurveV2Short4: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: C.black }}>
    <Footage />
    <Tease />
    <Mocap />
    <SimLabels />
    <Balance />
    <SmallPrint />
    <KnifeLabel />
    <Verdict />
    <Hook />
    <CaptionTrack pages={PAGES} hide={[[0, 21]]} until={F.rewind} />
    <Credit text="FOOTAGE: UNITREE · REAL SPEED" show={[[0, F.replay], [F.hold0, SHORT4_FRAMES]]} />
    <Credit text="FOOTAGE: UNITREE · 7× SLOWER" show={[[F.replay, F.tease]]} />
    <Credit text="FOOTAGE: UNITREE" show={[[F.tease, F.mocap], [F.knife, F.verdict]]} />
    <Credit text="FOOTAGE: UNITREE · SLOWED" show={[[F.real, F.rewind]]} />

    <Audio src={staticFile("shorts/s4_vo.mp3")} />
    {/* the bed holds one level, dips before the twist ("But the small print") and lands back on the hit */}
    <Audio src={staticFile("audio/sample-bed.mp3")} volume={(f) => interpolate(f, [0, 2, F.print - 18, F.print - 8, F.print + 2, F.print + 6,
      SHORT4_FRAMES - 2, SHORT4_FRAMES], [0.06, 0.12, 0.12, 0.0, 0.0, 0.12, 0.12, 0.06], CLAMP)} />
    <Sfx at={F.replay} name="whoosh" volume={0.35} />
    <Sfx at={F.tease} name="whoosh" volume={0.4} />
    <Sfx at={F.mocap} name="whoosh" volume={0.35} />
    <Sfx at={F.mocap + 68} name="form" volume={0.35} />
    <Sfx at={F.practise} name="whoosh" volume={0.4} />
    <Sfx at={F.reveal} name="riser" volume={0.3} />
    <Sfx at={F.reveal + 32} name="tick_run" volume={0.25} dur={60} />
    <Sfx at={F.reveal + 92} name="thock" volume={0.7} />
    <Sfx at={F.balance} name="whoosh" volume={0.35} />
    <Sfx at={F.balance + 70} name="tick_run" volume={0.18} dur={56} />
    <Sfx at={F.print - 30} name="riser" volume={0.35} />
    <Sfx at={F.print} name="thock" volume={1} />
    <Sfx at={F.print} name="settle" volume={0.6} />
    <Sfx at={F.knife} name="whoosh" volume={0.4} />
    <Sfx at={902} name="thock" volume={0.75} />
    <Sfx at={F.verdict} name="whoosh" volume={0.4} />
    <Sfx at={948} name="thock" volume={0.55} />
    <Sfx at={980} name="thock" volume={0.75} />
    <Sfx at={F.rewind} name="rewind" volume={0.45} />
  </AbsoluteFill>
);
