import type React from "react";
import {
  Interactive,
  type InteractivitySchema,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { theme } from "../theme";

type TypeOnProps = {
  readonly children: string;
  readonly charsPerSecond?: number;
  readonly caret?: boolean;
  readonly style?: React.CSSProperties;
};

// Typewriter text with a block caret that blinks once the line is typed.
const TypeOnInner: React.FC<TypeOnProps> = ({
  children,
  charsPerSecond = 32,
  caret = true,
  style,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const shown = Math.floor((Math.max(0, frame) * charsPerSecond) / fps);
  const typing = shown < children.length;
  const blinkOn = Math.floor(frame / (fps * 0.5)) % 2 === 0;

  return (
    <div
      style={{
        fontFamily: theme.fonts.mono,
        fontSize: 44,
        letterSpacing: "0.08em",
        color: theme.colors.gold,
        whiteSpace: "pre",
        ...style,
      }}
    >
      {children.slice(0, shown)}
      <span
        style={{
          display: "inline-block",
          width: "0.55em",
          height: "0.95em",
          marginLeft: "0.12em",
          verticalAlign: "-0.1em",
          backgroundColor: theme.colors.accent,
          opacity: caret && (typing || blinkOn) ? 1 : 0,
        }}
      />
    </div>
  );
};

const typeOnSchema = {
  children: { type: "text-content", default: "", description: "Text" },
  charsPerSecond: {
    type: "number",
    hiddenFromList: false,
    default: 32,
    min: 1,
    max: 200,
    step: 1,
    description: "Characters per second",
  },
  caret: { type: "boolean", default: true, description: "Show caret" },
  ...Interactive.textSchema,
} as const satisfies InteractivitySchema;

export const TypeOn = Interactive.withSchema({
  Component: TypeOnInner,
  componentName: "<TypeOn>",
  schema: typeOnSchema,
  wrapInSequence: true,
});
