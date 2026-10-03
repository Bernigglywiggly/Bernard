import { useWindowedAudioData, visualizeAudio } from "@remotion/media-utils";
import { createContext, useContext } from "react";
import { useCurrentFrame, useVideoConfig } from "remotion";

const LevelContext = createContext<number | null>(null);

// Reads the bass level of `src` at the composition's own frame and shares it with everything inside. Put it at the
// top of a video (outside any <Sequence>) so the level matches the music, wherever a scene sits on the timeline.
export const AudioLevelProvider: React.FC<{
  readonly src: string;
  readonly gain?: number;
  readonly children: React.ReactNode;
}> = ({ src, gain = 3, children }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const { audioData, dataOffsetInSeconds } = useWindowedAudioData({
    src,
    frame,
    fps,
    windowInSeconds: 10,
  });

  let level = 0;
  if (audioData) {
    const bins = visualizeAudio({
      fps,
      frame,
      audioData,
      numberOfSamples: 32,
      optimizeFor: "speed",
      dataOffsetInSeconds,
    });
    level = Math.min(1, ((bins[0] + bins[1] + bins[2]) / 3) * gain);
  }

  return <LevelContext.Provider value={level}>{children}</LevelContext.Provider>;
};

// 0..1 bass level. Without a provider (a scene previewed on its own) it falls back to a pulse on a `bpm` grid.
export const useBass = (bpm = 124): number => {
  const level = useContext(LevelContext);
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (level !== null) {
    return level;
  }
  const beat = (frame / fps) * (bpm / 60);
  return Math.exp(-5 * (beat % 1));
};

// Frame of beat `n` on a `bpm` grid that starts at `offsetSeconds`. Use it to land cuts and hits on the music.
export const beatFrame = (n: number, bpm: number, fps: number, offsetSeconds = 0) =>
  Math.round((offsetSeconds + (n * 60) / bpm) * fps);
