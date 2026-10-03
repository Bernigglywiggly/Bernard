import { Audio } from "@remotion/media";
import { linearTiming, springTiming, TransitionSeries } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { slide } from "@remotion/transitions/slide";
import { wipe } from "@remotion/transitions/wipe";
import { zColor } from "@remotion/zod-types";
import {
  AbsoluteFill,
  type CalculateMetadataFunction,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { z } from "zod";
import { CLAMP, EASE_IN_OUT, sec } from "../lib/anim";
import { AudioLevelProvider } from "../lib/audio";
import { IntroScene } from "../scenes/IntroScene";
import { OutroScene } from "../scenes/OutroScene";
import { ShapesScene } from "../scenes/ShapesScene";
import { StatScene } from "../scenes/StatScene";

// Size, frame rate and length are props, so they can be changed in the Studio's props panel or with --props,
// e.g. --props=props/vertical.json for a 1080x1920 Short. Scenes stretch to fit the length.
export const showreelSchema = z.object({
  title: z.string(),
  subtitle: z.string(),
  outro: z.string(),
  accent: zColor(),
  width: z.number().int().min(240).max(7680).multipleOf(2),
  height: z.number().int().min(240).max(7680).multipleOf(2),
  fps: z.number().int().min(1).max(120),
  seconds: z.number().min(6).max(50),
});

export type ShowreelProps = z.infer<typeof showreelSchema>;

export const calculateShowreelMetadata: CalculateMetadataFunction<ShowreelProps> = ({ props }) => ({
  width: props.width,
  height: props.height,
  fps: props.fps,
  durationInFrames: Math.round(props.seconds * props.fps),
  defaultOutName: `showreel-${props.width}x${props.height}-${props.fps}fps`,
});

const MUSIC = staticFile("audio/sample-bed.mp3");
const SCENE_SECONDS = [4, 4.4, 4.4, 4]; // intro, stats, shapes, outro: 15 s with three 0.6 s transitions
const TRANSITION_SECONDS = 0.6;

// Frames for each scene and transition, so the whole thing lasts exactly `total` frames.
export const showreelTimeline = (fps: number, total: number) => {
  const overlap = sec(TRANSITION_SECONDS, fps);
  const sceneFrames = total + overlap * (SCENE_SECONDS.length - 1);
  const weight = SCENE_SECONDS.reduce((a, b) => a + b, 0);
  const scenes = SCENE_SECONDS.map((s) => Math.round((s / weight) * sceneFrames));
  scenes[scenes.length - 1] += sceneFrames - scenes.reduce((a, b) => a + b, 0);
  const starts = scenes.map((_, i) =>
    scenes.slice(0, i).reduce((a, b) => a + b, 0) - i * overlap,
  );
  return { overlap, scenes, starts, cuts: starts.slice(1) };
};

export const Showreel: React.FC<ShowreelProps> = ({ title, subtitle, outro, accent }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const t = showreelTimeline(fps, durationInFrames);

  return (
    <AbsoluteFill style={{ backgroundColor: "black" }}>
      <AudioLevelProvider src={MUSIC}>
        <TransitionSeries>
          <TransitionSeries.Sequence name="Intro" durationInFrames={t.scenes[0]} premountFor={fps}>
            <IntroScene title={title} subtitle={subtitle} accent={accent} />
          </TransitionSeries.Sequence>
          <TransitionSeries.Transition
            presentation={fade()}
            timing={linearTiming({ durationInFrames: t.overlap, easing: EASE_IN_OUT })}
          />
          <TransitionSeries.Sequence name="Stats" durationInFrames={t.scenes[1]} premountFor={fps}>
            <StatScene value={1000} suffix="×" label="ANIMATED, NOT EDITED" accent={accent} />
          </TransitionSeries.Sequence>
          <TransitionSeries.Transition
            presentation={slide({ direction: "from-right" })}
            timing={springTiming({ config: { damping: 200 }, durationInFrames: t.overlap })}
          />
          <TransitionSeries.Sequence name="Shapes" durationInFrames={t.scenes[2]} premountFor={fps}>
            <ShapesScene accent={accent} />
          </TransitionSeries.Sequence>
          <TransitionSeries.Transition
            presentation={wipe({ direction: "from-left" })}
            timing={linearTiming({ durationInFrames: t.overlap, easing: EASE_IN_OUT })}
          />
          <TransitionSeries.Sequence name="Outro" durationInFrames={t.scenes[3]} premountFor={fps}>
            <OutroScene title={outro} accent={accent} />
          </TransitionSeries.Sequence>
        </TransitionSeries>
      </AudioLevelProvider>
      <AbsoluteFill
        style={{
          backgroundColor: "black",
          pointerEvents: "none",
          opacity: interpolate(frame, [durationInFrames - 0.6 * fps, durationInFrames - 1], [0, 1], CLAMP),
        }}
      />
      <Audio
        name="Music"
        src={MUSIC}
        volume={(f) =>
          interpolate(f, [0, 0.4 * fps, durationInFrames - 1.2 * fps, durationInFrames - 1], [0, 0.7, 0.7, 0], CLAMP)
        }
      />
      <Audio name="Title hit" from={sec(0.3, fps)} src={staticFile("sfx/form.mp3")} volume={0.5} premountFor={fps} />
      {t.cuts.map((cut, i) => (
        <Audio key={i} name={`Whoosh ${i + 1}`} from={cut} src={staticFile("sfx/whoosh.mp3")} volume={0.45} premountFor={fps} />
      ))}
      <Audio name="Number lands" from={t.starts[1] + sec(1.2, fps)} src={staticFile("sfx/thock.mp3")} volume={0.6} premountFor={fps} />
    </AbsoluteFill>
  );
};
