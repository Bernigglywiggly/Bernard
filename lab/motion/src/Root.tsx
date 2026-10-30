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
import { HybridC } from "./curve_v2/HybridC";
import { HybridCReal } from "./curve_v2/HybridCReal";
import { HybridCRealVertical } from "./curve_v2/HybridCRealVertical";
import { HybridCReal2 } from "./curve_v2/HybridCReal2";
import { CurveV2Short1, SHORT1_FRAMES } from "./curve_v2/CurveV2Short1";
import { CurveV2Short2, SHORT2_FRAMES } from "./curve_v2/CurveV2Short2";
import { CurveV2Short3, SHORT3_FRAMES } from "./curve_v2/CurveV2Short3";
import { CurveAvatar, CurveBanner } from "./curve_v2/Brand";
import { CurveV2Short4, SHORT4_FRAMES } from "./curve_v2/CurveV2Short4";
import { CurveV2Short5, SHORT5_FRAMES } from "./curve_v2/CurveV2Short5";
import { CurveV2Short7, SHORT7_FRAMES } from "./curve_v2/CurveV2Short7";
import { CurveV2Short8, SHORT8_FRAMES } from "./curve_v2/CurveV2Short8";
import { CurveV2Short10, SHORT10_FRAMES } from "./curve_v2/CurveV2Short10";
import { CurveV2Short11, SHORT11_FRAMES } from "./curve_v2/CurveV2Short11";
import { CurveV2Short12, SHORT12_FRAMES } from "./curve_v2/CurveV2Short12";
import { CurveV2Short13, SHORT13_FRAMES } from "./curve_v2/CurveV2Short13";
import { FILM_FRAMES, FILM_ORDER, FilmRoadster } from "./curve_v2/film/FilmRoadster";
import { segFrames } from "./curve_v2/film/util";
import { ThumbA, ThumbB, ThumbC, ThumbD } from "./curve_v2/film/Thumbs";
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
      <Folder name="Curve-v2-trials">
        <Composition id="CurveV2-HybridC" component={HybridC} width={1920} height={1080} fps={30} durationInFrames={270} defaultProps={{}} />
        <Composition id="CurveV2-HybridC-Real" component={HybridCReal} width={1920} height={1080} fps={30} durationInFrames={381} defaultProps={{}} />
        <Composition id="CurveV2-HybridC-Real2" component={HybridCReal2} width={1920} height={1080} fps={30} durationInFrames={498} defaultProps={{}} />
        <Composition id="CurveV2-HybridC-Real-Vertical" component={HybridCRealVertical} width={1080} height={1920} fps={30} durationInFrames={381} defaultProps={{}} />
        <Composition id="CurveV2-Short1" component={CurveV2Short1} width={1080} height={1920} fps={30} durationInFrames={SHORT1_FRAMES} defaultProps={{}} />
        <Composition id="CurveV2-Short2" component={CurveV2Short2} width={1080} height={1920} fps={30} durationInFrames={SHORT2_FRAMES} defaultProps={{}} />
        <Composition id="CurveV2-Short3" component={CurveV2Short3} width={1080} height={1920} fps={30} durationInFrames={SHORT3_FRAMES} defaultProps={{}} />
        <Composition id="CurveV2-Short4" component={CurveV2Short4} width={1080} height={1920} fps={30} durationInFrames={SHORT4_FRAMES} defaultProps={{}} />
        <Composition id="CurveV2-Short5" component={CurveV2Short5} width={1080} height={1920} fps={30} durationInFrames={SHORT5_FRAMES} defaultProps={{}} />
        <Composition id="CurveV2-Short7" component={CurveV2Short7} width={1080} height={1920} fps={30} durationInFrames={SHORT7_FRAMES} defaultProps={{}} />
        <Composition id="CurveV2-Short8" component={CurveV2Short8} width={1080} height={1920} fps={30} durationInFrames={SHORT8_FRAMES} defaultProps={{}} />
        <Composition id="CurveV2-Short10" component={CurveV2Short10} width={1080} height={1920} fps={30} durationInFrames={SHORT10_FRAMES} defaultProps={{}} />
        <Composition id="CurveV2-Short11" component={CurveV2Short11} width={1080} height={1920} fps={30} durationInFrames={SHORT11_FRAMES} defaultProps={{}} />
        <Composition id="CurveV2-Short12" component={CurveV2Short12} width={1080} height={1920} fps={30} durationInFrames={SHORT12_FRAMES} defaultProps={{}} />
        <Composition id="CurveV2-Short13" component={CurveV2Short13} width={1080} height={1920} fps={30} durationInFrames={SHORT13_FRAMES} defaultProps={{}} />
        <Composition id="Film-Roadster" component={FilmRoadster} width={1920} height={1080} fps={30} durationInFrames={FILM_FRAMES} defaultProps={{}} />
        {FILM_ORDER.map(([seg, Comp]) => (
          <Composition key={seg} id={`Film-${seg}`} component={Comp} width={1920} height={1080} fps={30} durationInFrames={segFrames(seg)} defaultProps={{}} />
        ))}
        <Still id="Thumb-Roadster-A" component={ThumbA} width={1280} height={720} defaultProps={{}} />
        <Still id="Thumb-Roadster-B" component={ThumbB} width={1280} height={720} defaultProps={{}} />
        <Still id="Thumb-Roadster-C" component={ThumbC} width={1280} height={720} defaultProps={{}} />
        <Still id="Thumb-Roadster-D" component={ThumbD} width={1280} height={720} defaultProps={{}} />
        <Still id="Curve-Banner" component={CurveBanner} width={2560} height={1440} defaultProps={{}} />
        <Still id="Curve-Avatar" component={CurveAvatar} width={800} height={800} defaultProps={{}} />
      </Folder>
      {/* @new-composition-registrations (npm run new adds compositions above this line) */}
    </>
  );
};
