// Word-level captions for a narration file (whisper.cpp medium.en, DTW token timestamps).
// Usage: node scripts/transcribe.mjs <16kHz-mono.wav> <out.json>
import path from "node:path";
import fs from "node:fs";
import { transcribe, toCaptions } from "@remotion/install-whisper-cpp";

const [, , wav, out] = process.argv;
const whisperPath = path.join(process.cwd(), "whisper.cpp");
const result = await transcribe({
  inputPath: wav,
  whisperPath,
  whisperCppVersion: "1.7.6",
  model: "medium.en",
  tokenLevelTimestamps: true,
});
const { captions } = toCaptions({ whisperCppOutput: result });
fs.writeFileSync(out, JSON.stringify(captions, null, 1));
console.log(`${captions.length} tokens -> ${out}`);
