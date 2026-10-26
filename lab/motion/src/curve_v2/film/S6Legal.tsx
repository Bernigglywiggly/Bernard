import type React from "react";
import { AbsoluteFill, Easing, interpolate, random, useCurrentFrame, useVideoConfig } from "remotion";
import { CLAMP, EASE_IN_OUT, EASE_OUT } from "../../lib/anim";
import { BG_NIGHT, C, ClipScene, Credit, HEAD, HEADC, keyline, MONO, pop, slowPush, Stamp, Tag } from "../kit";
import { EvidenceStamp, Sfx } from "./fx";
import { BODY, GREY, Jet, Roadster, ROADSTER_NOZZLE, TYRE, WS } from "./S5FanCar";
import { cue } from "./util";

// Roadster film, segment S6 ("Is it legal?", 38.6 s). A "who's in charge?" map the camera moves through: the sky, where
// the aviation regulator stamps the car NOT AN AIRCRAFT and it drops out of the sky onto a public road; the road, where
// the road-safety regulator says it's up to Tesla; then a pan onto Tesla's own page (Rocket: "Not approved for public
// road use"). Hard cuts to a jet throwing gravel (physics, seeded), Musk's hedge as full-frame type (no likeness), and
// the payoff over Tesla's aerial of the test site, which is exactly "somewhere nobody calls a road".
// Facts: TESLA_ROADSTER_FACTS.md §13.3 (FAA to Politico: "does not meet the FAA's definition of an aircraft"; DOT: the
// maker must meet the federal safety standards; NHTSA "won't hesitate to act to protect the driving public"; tesla.com
// labels "Road ready" / "Race ready" / "Air ready", "So yes, it can fly.", "Note: Not approved for public road use."),
// §4 (Thrust road-legal, thrusters not for roads, gravel becomes a projectile; Tesla to Top Gear), §6 11:50 (Musk; the
// file has two word orders, so only the shared fragment "legal in all jurisdictions" is quoted), §0 (SpaceX site,
// McGregor, Texas). Footage: Tesla / YouTube.

const S = "S6";
const Q = {
  american: cue(S, "American"), flying: cue(S, "flying"), it: cue(S, "it"), isnt: cue(S, "isn't"), aircraft: cue(S, "aircraft"),
  leaves: cue(S, "leaves"), road: cue(S, "road"), regulator2: cue(S, "regulator", 2), up: cue(S, "up"), federal: cue(S, "federal"),
  keep: cue(S, "keep"), but: cue(S, "But"), website: cue(S, "website"), rocket: cue(S, "rocket"), flies: cue(S, "flies"),
  approved: cue(S, "approved"), all: cue(S, "all"), top: cue(S, "Top"), thrust: cue(S, "thrust"), legal: cue(S, "legal"),
  thrusters: cue(S, "thrusters"), meant: cue(S, "meant"), jet: cue(S, "jet"), strong: cue(S, "strong"), loose: cue(S, "loose"),
  projectiles: cue(S, "projectiles"), musk: cue(S, "Musk"), sure: cue(S, "sure"), legal2: cue(S, "legal", 2), so: cue(S, "So"),
  fly: cue(S, "fly"), somewhere: cue(S, "somewhere"), calls: cue(S, "calls"),
};
const GRAVEL = Q.jet - 2; // hard cut to the gravel close-up
const QUOTE = Q.musk - 2; // hard cut to Musk's line
const AERIAL = Q.so - 2; // hard cut to the aerial

// ------------------------------------------------------------------------------------------------ the map's camera
type Cam = { x: number; y: number; z: number };
type Key = Cam & { f: number; e?: (t: number) => number };
const ROAD_Y = 1300; // the road zone sits this far below the sky zone
const PAGE_X = 2400; // Tesla's page sits this far right of the road zone
const SINE = Easing.inOut(Easing.sin);
const KEYS: Key[] = [
  { f: 0, x: 960, y: 540, z: 1 },
  { f: Q.leaves + 2, x: 960, y: 540, z: 1.035, e: SINE },
  { f: Q.leaves + 56, x: 960, y: 540 + ROAD_Y, z: 1 },
  { f: Q.but, x: 960, y: 540 + ROAD_Y, z: 1.035, e: SINE },
  { f: Q.but + 32, x: 960 + PAGE_X, y: 540 + ROAD_Y, z: 1 },
  { f: Q.rocket - 4, x: 960 + PAGE_X, y: 540 + ROAD_Y, z: 1.02, e: SINE },
  { f: Q.rocket + 20, x: 1520 + PAGE_X, y: 552 + ROAD_Y, z: 1.12 },
  { f: Q.approved - 6, x: 1522 + PAGE_X, y: 554 + ROAD_Y, z: 1.125, e: SINE },
  { f: Q.approved + 16, x: 1500 + PAGE_X, y: 610 + ROAD_Y, z: 1.16 },
  { f: Q.top - 2, x: 1502 + PAGE_X, y: 612 + ROAD_Y, z: 1.165, e: SINE },
  { f: Q.top + 24, x: 960 + PAGE_X, y: 1520 + ROAD_Y, z: 1.0 },
  { f: GRAVEL, x: 960 + PAGE_X, y: 1520 + ROAD_Y, z: 1.04, e: SINE },
];
const camAt = (f: number): Cam => {
  if (f <= KEYS[0].f) return KEYS[0];
  for (let i = 1; i < KEYS.length; i++) {
    const a = KEYS[i - 1];
    const b = KEYS[i];
    if (f <= b.f) {
      const t = (b.e ?? EASE_IN_OUT)((f - a.f) / (b.f - a.f));
      return { x: a.x + (b.x - a.x) * t, y: a.y + (b.y - a.y) * t, z: a.z + (b.z - a.z) * t };
    }
  }
  return KEYS[KEYS.length - 1];
};
const world = (cam: Cam): React.CSSProperties => ({
  position: "absolute", left: 0, top: 0, width: 10, height: 10, transformOrigin: "0px 0px",
  translate: `${960 - cam.x * cam.z}px ${540 - cam.y * cam.z}px`, scale: String(cam.z),
});

const Svg: React.FC<{ x?: number; y?: number; children: React.ReactNode }> = ({ x = 0, y = 0, children }) => (
  <svg width={1920} height={1080} viewBox="0 0 1920 1080" style={{ position: "absolute", left: x, top: y, overflow: "visible" }}>{children}</svg>
);

const Rise: React.FC<{ at: number; left: number; top: number; size: number; color: string; children: React.ReactNode; frame: number; fps: number; font?: React.CSSProperties; stroke?: number }> = ({
  at, left, top, size, color, children, frame, fps, font, stroke = 9,
}) => {
  if (frame < at) return null;
  const s = pop(frame, at, fps, 210, 15);
  return (
    <div style={{ position: "absolute", left, top, ...(font ?? { ...HEADC, ...WS }), fontSize: size, color, opacity: interpolate(s, [0, 0.3], [0, 1], CLAMP),
      translate: `0 ${(1 - s) * 34}px`, ...(font ? {} : keyline(size / 150, stroke)) }}>{children}</div>
  );
};

// ------------------------------------------------------------------------------------------------ sky + road
// The car: hovers on its corner jets, the jets cut, it falls out of the sky zone and lands on the public road.
const FALL0 = Q.leaves - 4;
const LAND = Q.leaves + 52;
const CAR_X = 1370;
const SKY_CAR_Y = 690;
const ROAD_CAR_Y = ROAD_Y + 900;
const carState = (frame: number) => {
  if (frame < FALL0) return { y: SKY_CAR_Y + 8 * Math.sin(frame / 9), rot: 1.5 * Math.sin(frame / 13), jets: 1, squash: 1 };
  if (frame < LAND) {
    const t = frame - FALL0;
    const g = (2 * (ROAD_CAR_Y - SKY_CAR_Y)) / (LAND - FALL0) ** 2;
    return { y: SKY_CAR_Y + 0.5 * g * t * t, rot: interpolate(t, [0, 20, LAND - FALL0], [0, -7, -3], CLAMP), jets: interpolate(t, [0, 5], [1, 0], CLAMP), squash: 1 };
  }
  const k = frame - LAND;
  return { y: ROAD_CAR_Y, rot: 0, jets: 0, squash: 1 - 0.07 * Math.exp(-k / 4) * Math.cos(k * 0.9) };
};

const STARS = Array.from({ length: 46 }).map((_, i) => ({ x: random(`sx${i}`) * 1920, y: 40 + random(`sy${i}`) * 1000, r: 1.5 + random(`sr${i}`) * 2.2, ph: random(`sp${i}`) * 6 }));
const Stars: React.FC<{ frame: number }> = ({ frame }) => (
  <g>
    {STARS.map((st, i) => <circle key={i} cx={st.x} cy={st.y} r={st.r} fill={C.ink} opacity={0.18 + 0.22 * (0.5 + 0.5 * Math.sin(frame / 14 + st.ph))} />)}
  </g>
);

const Puffs: React.FC<{ frame: number; at: number; x: number; y: number }> = ({ frame, at, x, y }) => {
  const k = frame - at;
  if (k < 0 || k > 40) return null;
  const p = interpolate(k, [0, 40], [0, 1], { ...CLAMP, easing: EASE_OUT });
  return (
    <g opacity={1 - p}>
      {[-1, 1].map((d) => [0, 1, 2].map((i) => (
        <ellipse key={`${d}${i}`} cx={x + d * (400 + i * 70 + p * 160)} cy={y - 10 - i * 4 - p * 16} rx={(40 - i * 8) * (0.7 + p)} ry={(16 - i * 3) * (0.7 + p)} fill={GREY} opacity={0.7} />
      )))}
    </g>
  );
};

const SkyRoad: React.FC<{ frame: number; fps: number }> = ({ frame, fps }) => {
  const car = carState(frame);
  const quoteIn = pop(frame, Q.it + 4, fps, 200, 15);
  const dash = (frame >= LAND ? 0 : 0) % 1;
  const lanes: React.ReactNode[] = [];
  for (let x = -600; x < 2600; x += 220) lanes.push(<rect key={x} x={x + dash} y={ROAD_Y + 944} width={120} height={14} fill={BODY} opacity={0.75} />);
  return (
    <>
      <Svg>
        <Stars frame={frame} />
        {/* the road zone: asphalt seen from slightly above, with a kerb at the far edge */}
        <rect x={-800} y={ROAD_Y + 820} width={3400} height={460} fill="#120A24" />
        <rect x={-800} y={ROAD_Y + 820} width={3400} height={12} fill={GREY} opacity={0.5} />
        {lanes}
        <rect x={-800} y={ROAD_Y + 1040} width={3400} height={10} fill={GREY} opacity={0.35} />
        <ellipse cx={CAR_X} cy={ROAD_CAR_Y + 4} rx={430} ry={26} fill="#000" opacity={0.45} />
        <Puffs frame={frame} at={LAND} x={CAR_X} y={ROAD_CAR_Y} />
        <g transform={`translate(${CAR_X} ${car.y}) rotate(${car.rot}) scale(0.8 ${0.8 * car.squash})`}>
          <Jet x={452} y={-38} len={250} w={52} frame={frame} seed={1} op={car.jets} />
          <Jet x={-462} y={-38} len={250} w={52} frame={frame} seed={2} op={car.jets} />
          <Roadster />
        </g>
      </Svg>
      {/* SKY: the question, the aviation regulator, its answer */}
      <div style={{ position: "absolute", left: 150, top: 120, ...HEADC, fontSize: 112, color: C.ink, ...keyline(0.75, 10) }}>IS IT AN AIRCRAFT?</div>
      <Rise at={Q.american - 4} left={150} top={262} size={250} color={C.cyan} frame={frame} fps={fps} stroke={10}>FAA</Rise>
      <Rise at={Q.american + 6} left={156} top={490} size={54} color={C.ink} frame={frame} fps={fps}>THE AMERICAN<br />AVIATION REGULATOR</Rise>
      {frame >= Q.it + 4 ? (
        <div style={{ position: "absolute", left: 156, top: 640, width: 760, opacity: interpolate(quoteIn, [0, 0.3], [0, 1], CLAMP), translate: `0 ${(1 - quoteIn) * 30}px` }}>
          <div style={{ ...HEAD, fontWeight: 800, fontVariationSettings: "'wdth' 88", fontSize: 54, lineHeight: 1.12, color: C.ink, ...keyline(0.36, 8) }}>
            “DOES NOT MEET THE FAA&apos;S DEFINITION OF AN AIRCRAFT.”
          </div>
          <div style={{ ...MONO, fontSize: 44, color: GREY, marginTop: 16, whiteSpace: "nowrap" }}>FAA TO POLITICO, 16 OCT 2026</div>
        </div>
      ) : null}
      <Stamp at={Q.isnt} left={940} top={300} size={86} rot={-6} until={FALL0 + 8}>NOT AN AIRCRAFT</Stamp>
      {/* ROAD: the road-safety regulator */}
      <div style={{ position: "absolute", left: 0, top: ROAD_Y, width: 1920, height: 1080 }}>
        <Rise at={Q.road - 10} left={150} top={150} size={240} color={C.ink} frame={frame} fps={fps} stroke={10}>NHTSA</Rise>
        <Rise at={Q.road - 2} left={156} top={372} size={54} color={C.cyan} frame={frame} fps={fps}>THE ROAD-SAFETY REGULATOR</Rise>
        <Rise at={Q.up} left={1010} top={146} size={120} color={C.acid} frame={frame} fps={fps} stroke={10}>UP TO TESLA</Rise>
        <Rise at={Q.federal - 4} left={1016} top={282} size={52} color={C.ink} frame={frame} fps={fps}>TO MEET FEDERAL<br />SAFETY STANDARDS</Rise>
        <Rise at={Q.keep - 8} left={1016} top={418} size={48} color={C.ink} frame={frame} fps={fps}
          font={{ ...HEAD, fontWeight: 800, fontVariationSettings: "'wdth' 88", lineHeight: 1.12, ...keyline(0.32, 8) }}>
          “WON&apos;T HESITATE TO ACT TO<br />PROTECT THE DRIVING PUBLIC”
        </Rise>
        <Rise at={Q.keep} left={1018} top={542} size={44} color={GREY} frame={frame} fps={fps} font={MONO}>NHTSA, VIA POLITICO</Rise>
      </div>
    </>
  );
};

// ------------------------------------------------------------------------------------------------ Tesla's own page
const COLS = [
  { x: 150, name: "PERFORMANCE", label: "Road ready" },
  { x: 720, name: "THRUST", label: "Race ready" },
  { x: 1290, name: "ROCKET", label: "Air ready" },
];
const PAGE_INK = "#111318";
const Marker: React.FC<{ p: number; children: React.ReactNode; color?: string }> = ({ p, children, color = C.acid }) => (
  <span style={{ backgroundImage: `linear-gradient(${color}, ${color})`, backgroundRepeat: "no-repeat", backgroundSize: `${p * 100}% 100%`,
    boxDecorationBreak: "clone", WebkitBoxDecorationBreak: "clone", padding: "0 6px" }}>{children}</span>
);
const Page: React.FC<{ frame: number; fps: number }> = ({ frame, fps }) => {
  const focus = (i: number) => {
    if (frame < Q.rocket - 2) return 1;
    if (frame < Q.top) return i === 2 ? 1 : 0.16;
    return i === 1 ? 1 : i === 2 ? 0.5 : 0.24;
  };
  const fly = interpolate(frame, [Q.flies - 8, Q.flies + 6], [0, 1], { ...CLAMP, easing: EASE_OUT });
  const hi = interpolate(frame, [Q.approved, Q.all + 4], [0, 1], { ...CLAMP, easing: Easing.inOut(Easing.quad) });
  const header = interpolate(frame, [Q.rocket - 6, Q.rocket + 2], [1, 0], CLAMP);
  return (
    <div style={{ position: "absolute", left: PAGE_X, top: ROAD_Y, width: 1920, height: 1080 }}>
      <div style={{ position: "absolute", left: -160, top: -140, width: 3200, height: 1400, backgroundColor: "#EEF0F3", rotate: "-0.8deg",
        boxShadow: "0 30px 80px rgba(0,0,0,0.6)" }} />
      <div style={{ opacity: header }}>
        <div style={{ position: "absolute", left: 150, top: 116, padding: "8px 18px 10px", backgroundColor: PAGE_INK, color: C.ink, ...HEADC, ...WS, fontSize: 60 }}>
          TESLA&apos;S OWN WEBSITE
        </div>
        <div style={{ position: "absolute", left: 156, top: 222, ...MONO, fontSize: 44, color: "#5E6670" }}>TESLA.COM/ROADSTER</div>
      </div>
      {[690, 1260].map((x) => <div key={x} style={{ position: "absolute", left: x, top: 330, width: 3, height: 470, backgroundColor: "#DDE1E6" }} />)}
      {COLS.map((c, i) => (
        <div key={c.name} style={{ position: "absolute", left: c.x, top: 330, width: 540, opacity: focus(i) }}>
          <div style={{ ...HEADC, fontSize: 66, color: PAGE_INK }}>{c.name}</div>
          <div style={{ ...HEAD, fontWeight: 800, fontVariationSettings: "'wdth' 92", fontSize: 76, color: "#2A2F36", marginTop: 26, letterSpacing: "-0.01em" }}>{c.label}</div>
          {i === 2 ? (
            <div style={{ ...HEAD, fontVariationSettings: "'wdth' 92", letterSpacing: "-0.005em", lineHeight: 1.18, color: PAGE_INK }}>
              <div style={{ fontWeight: 700, fontSize: 60, marginTop: 40 }}><Marker p={fly} color={C.cyan}>So yes, it can fly.</Marker></div>
              <div style={{ fontWeight: 800, fontSize: 66, marginTop: 40 }}>Note: <Marker p={hi}>Not approved for public road use.</Marker></div>
            </div>
          ) : null}
        </div>
      ))}
    </div>
  );
};

// ------------------------------------------------------------------------------------------------ the gravel shot
const G_GROUND = 770;
const NOZ = { x: 1890 + ROADSTER_NOZZLE.x * 1.6, y: G_GROUND + ROADSTER_NOZZLE.y * 1.6 };
const JET_ON = GRAVEL + 4;
const FRONT_V = 11; // px per frame: how fast the jet's reach sweeps along the ground
type Stone = { x: number; r: number; pts: string; shade: string; vx: number; vy: number; spin: number; near: boolean };
const STONES: Stone[] = Array.from({ length: 90 }).map((_, i) => {
  const r = 7 + random(`r${i}`) * 13;
  const pts = Array.from({ length: 7 }).map((__, k) => {
    const a = (k / 7) * Math.PI * 2;
    const rr = r * (0.7 + 0.45 * random(`p${i}-${k}`));
    return `${(Math.cos(a) * rr).toFixed(1)},${(Math.sin(a) * rr * 0.8).toFixed(1)}`;
  }).join(" ");
  const shades = ["#8F99A3", "#B9C2CC", "#6E7782", "#A7A0B8"];
  return {
    x: 260 + random(`x${i}`) * 860, r, pts, shade: shades[i % 4],
    vx: -(13 + 24 * random(`vx${i}`)), vy: -(8 + 15 * random(`vy${i}`)), spin: (random(`s${i}`) - 0.5) * 34, near: i % 9 === 0,
  };
});
const stoneAt = (s: Stone, frame: number) => {
  const t0 = s.near ? Q.projectiles - 16 + (Math.round(s.x) % 5) * 3 : JET_ON + 6 + Math.max(0, (NOZ.x - 120 - s.x) / FRONT_V);
  const t = frame - t0;
  const rest = { x: s.x, y: G_GROUND - s.r * 0.45, rot: 0, scale: 1, flying: false };
  if (t <= 0) return rest;
  const g = 0.95;
  let x = s.x + s.vx * t;
  let y = G_GROUND - s.r * 0.45 + s.vy * t + 0.5 * g * t * t;
  const tHit = (-2 * s.vy) / g; // back on the ground
  if (t > tHit) {
    const t2 = t - tHit;
    x = s.x + s.vx * tHit + s.vx * 0.6 * t2;
    y = Math.min(G_GROUND - s.r * 0.45, G_GROUND - s.r * 0.45 + s.vy * 0.35 * t2 + 0.5 * g * t2 * t2);
  }
  const scale = s.near ? 1 + t * 0.09 : 1;
  if (s.near) y += t * 3;
  return { x, y, rot: s.spin * t, scale, flying: true };
};

const GravelShot: React.FC<{ frame: number; fps: number }> = ({ frame, fps }) => {
  if (frame < GRAVEL || frame >= QUOTE) return null;
  const reach = Math.min(1, Math.max(0, (frame - JET_ON) / 14));
  const crack = interpolate(frame, [Q.projectiles - 2, Q.projectiles + 4], [0, 1], { ...CLAMP, easing: EASE_OUT });
  const bed: React.ReactNode[] = [];
  for (let i = 0; i < 150; i++) {
    const x = random(`bx${i}`) * 1920;
    const y = G_GROUND + 14 + random(`by${i}`) * 300;
    bed.push(<ellipse key={i} cx={x} cy={y} rx={4 + random(`bs${i}`) * 9} ry={3 + random(`bt${i}`) * 5} fill={i % 3 ? "#2A2240" : "#3A3152"} />);
  }
  return (
    <AbsoluteFill style={{ background: BG_NIGHT, scale: String(slowPush(frame, GRAVEL, QUOTE, 1.05)), transformOrigin: "60% 70%" }}>
      <svg width={1920} height={1080} style={{ position: "absolute", inset: 0 }}>
        <rect x={0} y={G_GROUND} width={1920} height={400} fill="#171127" />
        {bed}
        <line x1={0} y1={G_GROUND} x2={1920} y2={G_GROUND} stroke={GREY} strokeOpacity={0.4} strokeWidth={3} />
        {/* the car behind: its windscreen takes a stone */}
        <g>
          <path d={`M -40 ${G_GROUND - 40} L -40 ${G_GROUND - 250} L 120 ${G_GROUND - 250} L 236 ${G_GROUND - 150} L 330 ${G_GROUND - 132} L 342 ${G_GROUND - 40} Z`} fill={BODY} stroke={C.black} strokeWidth={6} strokeLinejoin="round" />
          <path d={`M 20 ${G_GROUND - 236} L 112 ${G_GROUND - 236} L 214 ${G_GROUND - 152} L 20 ${G_GROUND - 152} Z`} fill="#3B4A61" stroke={C.black} strokeWidth={5} strokeLinejoin="round" />
          <circle cx={226} cy={G_GROUND - 40} r={58} fill={TYRE} stroke={C.black} strokeWidth={6} />
          <circle cx={226} cy={G_GROUND - 40} r={30} fill="#B9C2CC" stroke={C.black} strokeWidth={4} />
          <g opacity={crack} transform={`translate(120 ${G_GROUND - 194})`}>
            {[0, 40, 96, 150, 205, 262, 318].map((a, i) => (
              <polyline key={a} points={`0,0 ${Math.cos((a * Math.PI) / 180) * 40 * crack + (i % 2 ? 6 : -6)},${Math.sin((a * Math.PI) / 180) * 30 * crack} ${Math.cos((a * Math.PI) / 180) * 92 * crack},${Math.sin((a * Math.PI) / 180) * 50 * crack}`}
                fill="none" stroke={C.ink} strokeWidth={5} strokeLinejoin="round" />
            ))}
            <circle r={22 * crack} fill="none" stroke={C.ink} strokeWidth={4} />
            <circle r={7} fill={C.ink} />
          </g>
        </g>
        {Array.from({ length: 16 }).map((_, i) => {
          const dx = NOZ.x - 160 - i * 60;
          const born = JET_ON + 6 + (NOZ.x - 160 - dx) / FRONT_V;
          const k = frame - born;
          if (k < 0) return null;
          const p = Math.min(1, k / 50);
          return <circle key={`d${i}`} cx={dx - k * (3 + (i % 3))} cy={G_GROUND - 20 - k * (1.2 + (i % 4) * 0.4)} r={18 + k * 1.6} fill={GREY} opacity={0.34 * (1 - p)} />;
        })}
        {STONES.map((s, i) => {
          const st = stoneAt(s, frame);
          if (st.x < -80 || st.y > 1200) return null;
          return (
            <g key={i} transform={`translate(${st.x} ${st.y}) rotate(${st.rot}) scale(${st.scale})`}>
              {st.flying ? <line x1={0} y1={0} x2={-s.vx * 1.4} y2={-s.vy * 0.9} stroke={s.shade} strokeOpacity={0.35} strokeWidth={s.r * 0.8} strokeLinecap="round" /> : null}
              <polygon points={s.pts} fill={s.shade} stroke={C.black} strokeWidth={2.5} />
            </g>
          );
        })}
        <Jet x={NOZ.x} y={NOZ.y} len={900 * reach} w={70} deg={82} frame={frame} seed={3} op={reach > 0 ? 1 : 0} />
        <g transform={`translate(1890 ${G_GROUND}) scale(1.6)`}><Roadster /></g>
      </svg>
      <Tag at={JET_ON + 2} left={NOZ.x - 560} top={NOZ.y - 168} bg={C.cyan} size={54} style={WS}>COLD-GAS JET</Tag>
      <Rise at={Q.loose - 4} left={150} top={150} size={124} color={C.ink} frame={frame} fps={fps} stroke={10}>LOOSE GRAVEL</Rise>
      <Rise at={Q.projectiles - 4} left={150} top={290} size={150} color={C.warn} frame={frame} fps={fps} stroke={10}>→ PROJECTILES</Rise>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ Musk's line
const QuoteShot: React.FC<{ frame: number; fps: number }> = ({ frame, fps }) => {
  if (frame < QUOTE || frame >= AERIAL) return null;
  const mark = pop(frame, QUOTE, fps, 160, 16);
  const hl = interpolate(frame, [Q.legal2 - 2, Q.legal2 + 14], [0, 1], { ...CLAMP, easing: Easing.inOut(Easing.quad) });
  return (
    <AbsoluteFill style={{ background: BG_NIGHT }}>
      <AbsoluteFill style={{ scale: String(slowPush(frame, QUOTE, AERIAL, 1.045)), transformOrigin: "20% 40%" }}>
        <div style={{ position: "absolute", right: 120, top: -40, ...HEADC, fontSize: 640, lineHeight: 1, color: C.magenta, opacity: interpolate(mark, [0, 0.3], [0, 1], CLAMP),
          translate: `0 ${(1 - mark) * -60}px`, ...keyline(3, 10) }}>”</div>
        <Tag at={QUOTE + 2} left={150} top={170} bg={C.ink} size={60} style={WS}>ELON MUSK, ON STAGE</Tag>
        <Rise at={Q.musk + 6} left={150} top={300} size={120} color={C.ink} frame={frame} fps={fps} stroke={10}>HE ISN&apos;T SURE IT&apos;S</Rise>
        {frame >= Q.sure + 2 ? (
          <div style={{ position: "absolute", left: 150, top: 450, opacity: interpolate(pop(frame, Q.sure + 2, fps, 210, 15), [0, 0.3], [0, 1], CLAMP) }}>
            {["“LEGAL IN ALL", "JURISDICTIONS”"].map((ln, i) => {
              const k = Math.min(1, Math.max(0, hl * 2 - i));
              return (
                <div key={ln} style={{ position: "relative", ...HEADC, ...WS, fontSize: 150, lineHeight: 0.98, marginTop: i === 1 ? -3 : 0 }}>
                  <div style={{ padding: "0 12px", color: C.acid, ...keyline(1, 10) }}>{ln}</div>
                  <div style={{ position: "absolute", left: 0, top: 0, padding: "0 12px", color: C.black, backgroundColor: C.acid, clipPath: `inset(0 ${(1 - k) * 100}% 0 0)` }}>{ln}</div>
                </div>
              );
            })}
          </div>
        ) : null}
        <Rise at={Q.sure + 10} left={156} top={790} size={44} color={GREY} frame={frame} fps={fps} font={MONO}>TESLA&apos;S ROADSTER EVENT, 15 OCT 2026</Rise>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ the payoff
const AerialShot: React.FC<{ frame: number; fps: number }> = ({ frame, fps }) => {
  if (frame < AERIAL) return null;
  return (
    <AbsoluteFill>
      <ClipScene src="film/ramp_aerial_wide.mp4" from={AERIAL} dur={170} push={[1, 1.06]} origin="58% 42%" />
      <AbsoluteFill style={{ background: "linear-gradient(90deg, rgba(10,4,24,0.78) 0%, rgba(10,4,24,0.5) 36%, rgba(10,4,24,0) 62%)" }} />
      <Rise at={Q.fly - 8} left={150} top={130} size={86} color={C.cyan} frame={frame} fps={fps}>IT CAN FLY,</Rise>
      <Rise at={Q.somewhere} left={150} top={232} size={112} color={C.ink} frame={frame} fps={fps} stroke={10}>SOMEWHERE NOBODY</Rise>
      <Rise at={Q.calls - 4} left={150} top={352} size={146} color={C.acid} frame={frame} fps={fps} stroke={10}>CALLS A ROAD</Rise>
      <Rise at={AERIAL + 10} left={154} top={760} size={60} color={C.ink} frame={frame} fps={fps}>SPACEX TEST SITE</Rise>
      <Rise at={AERIAL + 16} left={156} top={832} size={44} color={GREY} frame={frame} fps={fps} font={MONO}>McGREGOR, TEXAS</Rise>
      <Credit text="FOOTAGE: TESLA / YOUTUBE" show={[[AERIAL, 99999]]} top={930} />
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ the segment
// Under Tesla's page (the camera has dropped below it): Top Gear's claim, outside Tesla's words (critic round 1: the
// v1 badge sat inside the page and read as Tesla's own). Facts: S1 (Top Gear, on the Thrust version), §13.3 (Tesla's
// page says Thrust is "Race ready", never "street legal").
const TopGear: React.FC<{ frame: number; fps: number }> = ({ frame, fps }) => {
  if (frame < Q.top + 14 || frame >= GRAVEL) return null;
  const legal = pop(frame, Q.legal - 4, fps, 230, 12);
  return (
    <AbsoluteFill>
      <EvidenceStamp kind="tesla" at={Q.top + 14} left={150} top={400} text="TOP GEAR WAS TOLD" note="ON THE THRUST VERSION" />
      {frame >= Q.legal - 4 ? (
        <div style={{ position: "absolute", left: 150, top: 560, ...HEADC, ...WS, fontSize: 170, color: C.cyan, opacity: interpolate(legal, [0, 0.3], [0, 1], CLAMP),
          translate: `0 ${(1 - legal) * 30}px`, ...keyline(1.1, 11) }}>ROAD LEGAL</div>
      ) : null}
      <Tag at={Q.meant - 10} left={156} top={780} bg={C.warn} color={C.ink} size={66} rot={[8, -2]} style={WS}>BUT ITS THRUSTERS: NOT FOR PUBLIC ROADS</Tag>
    </AbsoluteFill>
  );
};

export const S6Legal: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const cam = camAt(frame);
  const prev = camAt(Math.max(0, frame - 1));
  const vx = Math.abs(cam.x - prev.x) * cam.z;
  const vy = Math.abs(cam.y - prev.y) * cam.z;
  const bx = Math.min(40, Math.max(0, vx - 6) * 0.3);
  const by = Math.min(30, Math.max(0, vy - 8) * 0.22);
  return (
    <AbsoluteFill style={{ background: BG_NIGHT, overflow: "hidden" }}>
      <svg width={0} height={0} style={{ position: "absolute" }}>
        <defs><filter id="s6-mb" x="-5%" y="-5%" width="110%" height="110%"><feGaussianBlur stdDeviation={`${bx.toFixed(1)} ${by.toFixed(1)}`} /></filter></defs>
      </svg>
      {frame < GRAVEL ? (
        <AbsoluteFill style={bx + by > 0.5 ? { filter: "url(#s6-mb)" } : undefined}>
          <div style={world(cam)}>
            <SkyRoad frame={frame} fps={fps} />
            <Page frame={frame} fps={fps} />
          </div>
        </AbsoluteFill>
      ) : null}
      <TopGear frame={frame} fps={fps} />
      <GravelShot frame={frame} fps={fps} />
      <QuoteShot frame={frame} fps={fps} />
      <AerialShot frame={frame} fps={fps} />

      <Sfx at={0} name="hiss" volume={0.18} dur={FALL0} />
      <Sfx at={Q.american - 4} name="form" volume={0.35} />
      <Sfx at={Q.isnt} name="thock" volume={0.7} />
      <Sfx at={FALL0 + 4} name="whoosh" volume={0.45} />
      <Sfx at={LAND} name="thock" volume={0.75} />
      <Sfx at={LAND + 2} name="settle" volume={0.4} />
      <Sfx at={Q.up} name="form" volume={0.35} />
      <Sfx at={Q.but} name="whoosh" volume={0.45} />
      <Sfx at={Q.approved} name="tick_run" volume={0.25} dur={30} />
      <Sfx at={Q.legal - 4} name="thock" volume={0.4} />
      <Sfx at={Q.meant - 10} name="thock" volume={0.55} />
      <Sfx at={JET_ON} name="hiss" volume={0.6} dur={QUOTE - JET_ON} />
      <Sfx at={Q.projectiles - 2} name="thock" volume={0.6} />
      <Sfx at={QUOTE} name="whoosh" volume={0.4} />
      <Sfx at={Q.sure + 2} name="form" volume={0.35} />
      <Sfx at={AERIAL} name="whoosh" volume={0.4} />
      <Sfx at={Q.calls - 4} name="thock" volume={0.55} />
    </AbsoluteFill>
  );
};
