import { Audio, Video } from "@remotion/media";
import { evolvePath } from "@remotion/paths";
import type React from "react";
import { AbsoluteFill, Img, interpolate, Sequence, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { CLAMP, EASE_IN_OUT, EASE_OUT } from "../lib/anim";
import { Bed, BG_NIGHT, C, CaptionTrack, ClipScene, Credit, FILL, HEADC, Headline, keyline, MONO, pop, Sfx, slowPush, Stamp, Tag } from "./kit";
import { makePages } from "./pager";
import { VO_S4_CAPTIONS } from "./voS4Captions";

// Curve Short 4 (Sat 24 Oct 2026): "How Does a Robot Learn Kung Fu? Unitree's H2-X". 1080x1920, 30 fps.
// First Short on the kit and the first off the Roadster. Facts: lab/research/UNITREE_H2X_FACTS.md (rows in brackets).
// Footage: Unitree Robotics, YouTube, 21 Oct 2026 (Y3zb4o47yqA), 1080p50, RIFE slow motion; Unitree's own on-screen
// labels are shown as real-pixel crops [4-6]. The simulator shots are our Blender illustration
// (lab/curve_v2/shorts/blender/s4_sim.py): 4,096 robots = unitree_rl_gym's default num_envs [12]. Cuts on the 124 BPM
// bed's beats (beat k = k x 14.516 frames). Narration lab/curve_v2/shorts/vo/s4_chris_v4_tight.mp3 (33.2 s).
// The last frame is frame 0 (hook clip reversed into its first frame, hook text and credit as at frame 0).

export const SHORT4_FRAMES = 1014;

const F = { kick: 87, glimpse: 160, mocap: 232, practise: 334, reveal: 479, balance: 610, print: 726, knife: 842, verdict: 900,
  rewind: 990, hold0: 1004 };
const PAGES = makePages(VO_S4_CAPTIONS);
const DARKEN: React.CSSProperties = { position: "absolute", left: 0, right: 0, top: 0, height: 760,
  background: "linear-gradient(180deg, rgba(5,1,12,0.82) 0%, rgba(5,1,12,0.5) 60%, rgba(5,1,12,0) 100%)" };

// ------------------------------------------------------------------------------------------------ backgrounds
const Footage: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill style={{ backgroundColor: C.black }}>
      <ClipScene src="shorts/s4_hook.mp4" from={0} dur={F.kick} push={[1, 1.06]} origin="50% 30%" />
      <ClipScene src="shorts/s4_kick.mp4" from={F.kick} dur={F.glimpse - F.kick} push={[1.02, 1.08]} origin="50% 45%" />
      <ClipScene src="shorts/s4_sim_c.mp4" from={F.glimpse} dur={F.mocap - F.glimpse} push={[1, 1.02]} />
      <Sequence from={F.mocap} durationInFrames={F.practise - F.mocap}><AbsoluteFill style={{ background: BG_NIGHT }} /></Sequence>
      <ClipScene src="shorts/s4_sim_e.mp4" from={F.practise} dur={F.reveal - F.practise} push={[1, 1.03]} />
      <ClipScene src="shorts/s4_sim_f.mp4" from={F.reveal} dur={F.balance - F.reveal} rate={136 / 131} push={[1, 1]} />
      <ClipScene src="shorts/s4_balance.mp4" from={F.balance} dur={F.print - F.balance} push={[1, 1.05]} origin="50% 55%" />
      {/* small print: the same shot, blurred, under Unitree's own label */}
      <Sequence from={F.print} durationInFrames={F.knife - F.print} premountFor={fps}>
        <AbsoluteFill style={{ scale: slowPush(frame, F.print, F.knife, 1.06) }}>
          <Video src={staticFile("shorts/s4_balance.mp4")} muted trimBefore={70} playbackRate={0.4}
            style={{ ...FILL, filter: "blur(10px) brightness(0.42) saturate(0.9)" }} />
        </AbsoluteFill>
      </Sequence>
      <ClipScene src="shorts/s4_knife.mp4" from={F.knife} dur={F.verdict - F.knife} push={[1, 1.05]} origin="60% 45%" />
      <Sequence from={F.verdict} durationInFrames={F.rewind - F.verdict} premountFor={fps}>
        <AbsoluteFill style={{ scale: slowPush(frame, F.verdict, F.rewind, 1.05) }}>
          <Video src={staticFile("shorts/s4_kick.mp4")} muted playbackRate={0.6} style={{ ...FILL, filter: "brightness(0.38) saturate(0.85)" }} />
        </AbsoluteFill>
      </Sequence>
      {/* back to the opening picture: the flip rewinds into frame 0 */}
      <ClipScene src="shorts/s4_hook_rev.mp4" from={F.rewind} dur={F.hold0 - F.rewind} rate={6.5} push={[1, 1]} />
      <Sequence from={F.hold0}><Img src={staticFile("shorts/s4_frame0.png")} style={FILL} /></Sequence>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ hook (frame 0 and the end)
const Hook: React.FC = () => {
  const frame = useCurrentFrame();
  const show = frame < F.kick || frame >= F.hold0;
  if (!show) return null;
  const receipt = frame < F.kick ? interpolate(frame, [34, 46], [0, 1], { ...CLAMP, easing: EASE_OUT }) : 0;
  const punch = frame < F.kick ? interpolate(frame, [0, F.kick], [1, 1.03], CLAMP) : 1;
  return (
    <>
      <div style={{ position: "absolute", left: 60, top: 760, scale: punch, transformOrigin: "0% 50%" }}>
        <div style={{ ...HEADC, fontSize: 112, color: C.ink, ...keyline(0.75, 11) }}>THIS ROBOT&apos;S FLIP</div>
        <div style={{ ...HEADC, fontSize: 158, color: C.acid, lineHeight: 0.86, ...keyline(1.05, 11) }}>ISN&apos;T SPED UP</div>
        <div style={{ display: "inline-block", marginTop: 16, padding: "6px 16px 9px", backgroundColor: C.ink, color: C.black, ...HEADC,
          fontSize: 48, border: `4px solid ${C.black}` }}>SAYS UNITREE</div>
      </div>
      {receipt > 0 ? (
        <div style={{ position: "absolute", left: 60, top: 1150, opacity: receipt, translate: `${(1 - receipt) * -80}px 0`,
          border: `5px solid ${C.acid}`, backgroundColor: C.black }}>
          <Img src={staticFile("shorts/s4_label_speed.png")} style={{ width: 960, display: "block" }} />
        </div>
      ) : null}
    </>
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
const HX = 40, RX = 560, BY = 520; // left edges of the person and the robot, shared top

const Mocap: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < F.mocap || frame >= F.practise) return null;
  const s = pop(frame, F.mocap + 2, fps, 190, 14);
  const robotIn = pop(frame, F.mocap + 14, fps, 190, 14);
  const at = (k: number) => F.mocap + 30 + k * 4.2; // the joints link one by one through "joint by joint"
  const P = (x: number, k: string): P2 => [x + POSE[k][0], BY + POSE[k][1]];
  return (
    <AbsoluteFill style={{ scale: slowPush(frame, F.mocap, F.practise, 1.04), transformOrigin: "50% 50%" }}>
      <Tag at={F.mocap + 2} left={64} top={190} bg={C.acid} size={50}>STEP 1</Tag>
      <Headline at={F.mocap + 6} top={270} lines={[{ text: "COPY A PERSON", size: 132, color: C.ink }]} />
      <svg width={1080} height={1920} style={{ position: "absolute", inset: 0 }}>
        {/* the person in a motion-capture suit: dark limbs, magenta markers */}
        <g opacity={interpolate(s, [0, 0.4], [0, 1], CLAMP)}>
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
        {/* the robot: the same pose */}
        <g opacity={interpolate(robotIn, [0, 0.4], [0, 1], CLAMP)} transform={`translate(0 ${(1 - robotIn) * 40})`}>
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
        {/* marker -> joint links, drawn on in sequence */}
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
      <div style={{ position: "absolute", left: HX + 40, top: 1262, ...HEADC, fontSize: 46, color: C.magenta, ...keyline(0.3, 7) }}>PERSON</div>
      <div style={{ position: "absolute", left: RX + 120, top: 1262, ...HEADC, fontSize: 46, color: C.cyan, ...keyline(0.3, 7) }}>ROBOT</div>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ step 2 and the 4,096
const SimLabels: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const inGlimpse = frame >= F.glimpse && frame < F.mocap;
  const inPractise = frame >= F.practise && frame < F.reveal;
  const inReveal = frame >= F.reveal && frame < F.balance;
  if (!inGlimpse && !inPractise && !inReveal) return null;
  // the share of robots on the floor in our illustration falls as they practise (GN: 55% at Blender frame 100 -> 5% at 250)
  const bf = 101 + (frame - F.practise);
  const floorShare = interpolate(bf, [100, 250], [0.55, 0.05], CLAMP);
  const count = Math.round(interpolate(frame, [F.reveal + 40, F.reveal + 96], [1, 4096], { ...CLAMP, easing: EASE_OUT }));
  const landed = pop(frame, F.reveal + 96, fps, 260, 9);
  return (
    <AbsoluteFill>
      <div style={DARKEN} />
      <div style={{ position: "absolute", left: 64, top: 100, ...MONO, fontSize: 32, color: "#B9B2CC" }}>OUR 3D ILLUSTRATION OF A TRAINING SIMULATOR</div>
      {inGlimpse ? <Tag at={F.glimpse + 8} left={64} top={190} bg={C.cyan} size={64}>VIRTUAL COPIES</Tag> : null}
      {inPractise ? (
        <>
          <Tag at={F.practise + 2} left={64} top={170} bg={C.acid} size={50}>STEP 2</Tag>
          <Headline at={F.practise + 6} top={250} lines={[{ text: "PRACTISE IN A", size: 112 }, { text: "SIMULATOR", size: 112, color: C.cyan }]} />
          <div style={{ position: "absolute", left: 64, top: 520, ...HEADC, fontSize: 52, color: C.ink, ...keyline(0.35, 8),
            opacity: interpolate(frame, [F.practise + 40, F.practise + 52], [0, 1], CLAMP) }}>
            ON THE FLOOR
            <div style={{ marginTop: 10, width: 560, height: 30, border: `4px solid ${C.black}`, backgroundColor: "rgba(255,255,255,0.18)" }}>
              <div style={{ width: `${floorShare * 100 / 0.55}%`, height: "100%", backgroundColor: C.warn }} />
            </div>
          </div>
        </>
      ) : null}
      {inReveal ? (
        <div style={{ position: "absolute", left: 64, top: 170 }}>
          <div style={{ ...HEADC, fontSize: 250, color: C.acid, lineHeight: 0.86, fontVariantNumeric: "tabular-nums", ...keyline(1.7, 11),
            scale: frame >= F.reveal + 96 ? interpolate(landed, [0, 1], [1.12, 1]) : 1, transformOrigin: "0% 100%",
            opacity: interpolate(frame, [F.reveal + 30, F.reveal + 42], [0, 1], CLAMP) }}>{count.toLocaleString("en-GB")}</div>
          <div style={{ ...HEADC, fontSize: 72, color: C.ink, marginTop: 10, ...keyline(0.5, 9),
            opacity: interpolate(frame, [F.reveal + 50, F.reveal + 62], [0, 1], CLAMP) }}>ROBOTS PRACTISING AT ONCE</div>
        </div>
      ) : null}
      {inReveal ? <Tag at={F.reveal + 100} left={64} top={560} bg={C.cyan} size={46}>UNITREE&apos;S OWN PUBLIC TRAINING CODE</Tag> : null}
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ the real robot: 50 a second
const Balance: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < F.balance || frame >= F.print) return null;
  const sec = (frame - (F.balance + 24)) / fps; // ticks run once the number lands
  const lit = sec < 0 ? 0 : Math.floor((sec % 1) * 50) + 1;
  return (
    <AbsoluteFill>
      <div style={DARKEN} />
      <Headline at={F.balance + 4} top={150} lines={[{ text: "CORRECTS ITS BALANCE", size: 84 }]} />
      <Headline at={F.balance + 12} top={240} lines={[{ text: "≈50× A SECOND", size: 138, color: C.acid }]} stroke={11} />
      <svg width={1080} height={120} style={{ position: "absolute", left: 0, top: 430 }}>
        {Array.from({ length: 50 }).map((_, i) => (
          <rect key={i} x={64 + i * 19} y={20} width={13} height={i % 10 === 0 ? 70 : 50} fill={i < lit ? C.acid : "rgba(255,255,255,0.22)"}
            stroke="#000" strokeWidth={2} />
        ))}
      </svg>
      <Tag at={F.balance + 30} left={64} top={560} bg={C.cyan} size={44}>IN UNITREE&apos;S PUBLIC CODE: EVERY 0.02 s</Tag>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ the small print
// A push into the real frame of Unitree's film (24.2 s) until its own label fills the screen: source px [1160..1920] x
// [30..140] -> screen x [40..1040], y from 640. The highlight box and underline sit in source coordinates, so they ride
// the push.
const SmallPrint: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < F.print || frame >= F.knife) return null;
  const inS = pop(frame, F.print + 2, fps, 200, 15);
  const z = interpolate(frame, [F.print + 10, F.print + 44], [0, 1], { ...CLAMP, easing: EASE_IN_OUT });
  const k = interpolate(z, [0, 1], [1080 / 1920, 1000 / 760]);
  const left = interpolate(z, [0, 1], [0, 40 - 1160 * (1000 / 760)]);
  const top = interpolate(z, [0, 1], [640, 640 - 30 * (1000 / 760)]);
  const box8 = interpolate(frame, [F.print + 50, F.print + 58], [0, 1], { ...CLAMP, easing: EASE_OUT });   // "eight-hour" ~25.8 s
  const under = interpolate(frame, [F.print + 88, F.print + 104], [0, 1], { ...CLAMP, easing: EASE_OUT }); // "standing" ~27.2 s
  return (
    <AbsoluteFill>
      <Tag at={F.print + 2} left={64} top={250} bg={C.ink} size={54}>THE VIDEO&apos;S OWN SMALL PRINT</Tag>
      <div style={{ position: "absolute", left: 0, top: 0, width: 1920, height: 1080, transformOrigin: "0 0",
        translate: `${left}px ${top + (1 - inS) * 60}px`, scale: k, opacity: interpolate(inS, [0, 0.3], [0, 1], CLAMP) }}>
        <Img src={staticFile("shorts/s4_src_24.png")} style={{ width: 1920, height: 1080, display: "block" }} />
        <div style={{ position: "absolute", left: 1752, top: 86, width: 142, height: 50, border: `${7 / k}px solid ${C.acid}`, opacity: box8 }} />
        <div style={{ position: "absolute", left: 1224, top: 130, height: 9, width: 178 * under, backgroundColor: C.acid }} />
      </div>
      <div style={{ position: "absolute", left: 64, top: 860, ...HEADC, fontSize: 84, color: C.acid, opacity: under, ...keyline(0.6, 10),
        translate: `0 ${(1 - under) * 30}px` }}>STANDING, NOT FIGHTING</div>
    </AbsoluteFill>
  );
};

const KnifeLabel: React.FC = () => {
  const frame = useCurrentFrame();
  if (frame < F.knife || frame >= F.verdict) return null;
  const k = interpolate(frame, [F.knife + 18, F.knife + 28], [0, 1], { ...CLAMP, easing: EASE_OUT });
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", left: 40, top: 300, opacity: k, translate: `${(1 - k) * -60}px 0`, border: `5px solid ${C.warn}`,
        backgroundColor: C.black }}>
        <Img src={staticFile("shorts/s4_label_demo.png")} style={{ width: 760, display: "block" }} />
      </div>
      <Stamp at={F.knife + 30} left={60} top={470} size={96}>A DEMONSTRATION</Stamp>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ verdict
const Verdict: React.FC = () => {
  const frame = useCurrentFrame();
  if (frame < F.verdict || frame >= F.rewind) return null;
  return (
    <AbsoluteFill>
      <Headline at={F.verdict + 4} top={420} lines={[{ text: "KUNG FU", size: 150 }]} />
      <Tag at={F.verdict + 20} left={64} top={590} bg={C.acid} size={92} rot={[-10, -3]}>LEARNED</Tag>
      <Headline at={F.verdict + 40} top={820} lines={[{ text: "BODYGUARD", size: 150 }]} />
      <Stamp at={F.verdict + 52} left={64} top={990} size={104}>STILL A DEMO</Stamp>
    </AbsoluteFill>
  );
};

export const CurveV2Short4: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: C.black }}>
      <Footage />
      <Mocap />
      <SimLabels />
      <Balance />
      <SmallPrint />
      <KnifeLabel />
      <Verdict />
      <Hook />
      <CaptionTrack pages={PAGES} hide={[[0, 46], [F.print, F.print + 1]]} until={F.rewind} />
      <Credit text="FOOTAGE: UNITREE / YOUTUBE · 7× SLOWER" show={[[0, F.kick], [F.hold0, SHORT4_FRAMES]]} />
      <Credit text="FOOTAGE: UNITREE / YOUTUBE · 2× SLOWER" show={[[F.kick, F.glimpse], [F.balance, F.print]]} />
      <Credit text="FOOTAGE: UNITREE / YOUTUBE" show={[[F.knife, F.verdict]]} />

      <Audio src={staticFile("shorts/s4_vo.mp3")} />
      <Bed total={SHORT4_FRAMES} level={0.12} />
      <Sfx at={F.kick} name="whoosh" volume={0.4} />
      <Sfx at={F.glimpse} name="whoosh" volume={0.4} />
      <Sfx at={F.mocap} name="whoosh" volume={0.35} />
      <Sfx at={F.mocap + 30} name="form" volume={0.35} />
      <Sfx at={F.practise} name="whoosh" volume={0.4} />
      <Sfx at={F.reveal} name="riser" volume={0.3} />
      <Sfx at={F.reveal + 40} name="tick_run" volume={0.25} dur={56} />
      <Sfx at={F.reveal + 96} name="thock" volume={0.7} />
      <Sfx at={F.balance} name="whoosh" volume={0.4} />
      <Sfx at={F.balance + 24} name="tick_run" volume={0.18} dur={80} />
      <Sfx at={F.print} name="whoosh" volume={0.35} />
      <Sfx at={F.knife} name="whoosh" volume={0.4} />
      <Sfx at={F.knife + 30} name="thock" volume={0.75} />
      <Sfx at={F.verdict} name="whoosh" volume={0.4} />
      <Sfx at={F.verdict + 20} name="thock" volume={0.55} />
      <Sfx at={F.verdict + 52} name="thock" volume={0.75} />
      <Sfx at={F.rewind} name="rewind" volume={0.45} />
    </AbsoluteFill>
  );
};
