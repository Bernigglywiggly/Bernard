import { Composition, Folder, Still } from "remotion";
import { CountUp } from "./components/CountUp";
import { KineticTitle } from "./components/KineticTitle";
import { LowerThird } from "./components/LowerThird";
import {
  calculateShowreelMetadata,
  Showreel,
  showreelSchema,
} from "./compositions/Showreel";
import { Thumbnail } from "./compositions/Thumbnail";
import { IntroScene } from "./scenes/IntroScene";
import { OutroScene } from "./scenes/OutroScene";
import { ShapesScene } from "./scenes/ShapesScene";
import { StatScene } from "./scenes/StatScene";
import { WhatIfPov } from "./whatif/WhatIfPov";
// @new-composition-imports (npm run new adds imports above this line)

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="Showreel"
        component={Showreel}
        schema={showreelSchema}
        calculateMetadata={calculateShowreelMetadata}
        defaultProps={{
          title: "MOTION LAB",
          subtitle: "PROGRAMMATIC MOTION GRAPHICS",
          outro: "MADE WITH CODE",
          accent: "#3FE6D8",
          width: 1920,
          height: 1080,
          fps: 30,
          seconds: 15,
        }}
      />
      <Still
        id="Thumbnail"
        component={Thumbnail}
        width={1280}
        height={720}
        defaultProps={{
          lines: ["MOTION", "LAB"],
          chip: "REMOTION · 1920 × 1080 · 30 FPS",
          accent: "#3FE6D8",
        }}
      />
      <Folder name="Showreel-Scenes">
        <Composition
          id="IntroScene"
          component={IntroScene}
          width={1920}
          height={1080}
          fps={30}
          durationInFrames={120}
          defaultProps={{
            title: "MOTION LAB",
            subtitle: "PROGRAMMATIC MOTION GRAPHICS",
            accent: "#3FE6D8",
          }}
        />
        <Composition
          id="StatScene"
          component={StatScene}
          width={1920}
          height={1080}
          fps={30}
          durationInFrames={132}
          defaultProps={{
            value: 1000,
            suffix: "×",
            label: "ANIMATED, NOT EDITED",
            accent: "#3FE6D8",
          }}
        />
        <Composition
          id="ShapesScene"
          component={ShapesScene}
          width={1920}
          height={1080}
          fps={30}
          durationInFrames={132}
          defaultProps={{ accent: "#3FE6D8" }}
        />
        <Composition
          id="OutroScene"
          component={OutroScene}
          width={1920}
          height={1080}
          fps={30}
          durationInFrames={120}
          defaultProps={{ title: "MADE WITH CODE", accent: "#3FE6D8" }}
        />
      </Folder>
      <Folder name="Elements">
        <Composition
          id="KineticTitle"
          component={KineticTitle}
          width={1920}
          height={1080}
          fps={30}
          durationInFrames={60}
          defaultProps={{ children: "WORDS RISE ONE BY ONE", accentWord: 2 }}
        />
        <Composition
          id="CountUp"
          component={CountUp}
          width={1920}
          height={1080}
          fps={30}
          durationInFrames={60}
          defaultProps={{ to: 3200, suffix: " T" }}
        />
        <Composition
          id="LowerThird"
          component={LowerThird}
          width={1920}
          height={1080}
          fps={30}
          durationInFrames={60}
          defaultProps={{ children: "Your Name", detail: "WHO THEY ARE" }}
        />
      </Folder>
      <Folder name="WhatIf">
        <Composition
          id="WhatIf-BlackHole"
          component={WhatIfPov}
          width={1080}
          height={1920}
          fps={30}
          durationInFrames={2100}
          defaultProps={{ film: "blackhole" }}
        />
      </Folder>
      {/* @new-composition-registrations (npm run new adds compositions above this line) */}
    </>
  );
};
