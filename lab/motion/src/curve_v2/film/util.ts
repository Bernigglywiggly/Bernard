import { WORDS, VO_SECONDS } from "./words";

// Timing helpers for the Roadster film (1920x1080, 30 fps). Every segment's frame 0 is the start of its own narration,
// plus LEAD frames of picture before the voice comes in.
export const FPS = 30;
export const LEAD = 12; // 0.4 s of picture before each segment's first word
export const TAIL = 18; // 0.6 s after its last word
export const segFrames = (seg: string) => LEAD + Math.ceil(VO_SECONDS[seg] * FPS) + TAIL;

const bare = (s: string) => s.toLowerCase().replace(/[^a-z0-9.%]/g, "").replace(/\.$/, "");

// Frame (segment-relative, LEAD included) where the n-th occurrence of `word` starts in the segment's narration.
// Throws at render time if the word isn't there, so a script change can't silently desync a cue.
export const cue = (seg: string, word: string, nth = 1, edge: "start" | "end" = "start"): number => {
  const target = bare(word);
  let seen = 0;
  for (const [w, s, e] of WORDS[seg]) {
    if (bare(w) === target) {
      seen += 1;
      if (seen === nth) return LEAD + Math.round(((edge === "start" ? s : e) / 1000) * FPS);
    }
  }
  throw new Error(`cue: "${word}" #${nth} not found in ${seg}`);
};
