// One-time setup of whisper.cpp (Metal) + an English model for word-level caption timing.
// Usage: node scripts/whisper-setup.mjs        (installs into ./whisper.cpp, which is git-ignored)
import path from "node:path";
import { downloadWhisperModel, installWhisperCpp } from "@remotion/install-whisper-cpp";

const to = path.join(process.cwd(), "whisper.cpp");
await installWhisperCpp({ to, version: "1.7.6" });
await downloadWhisperModel({ model: "medium.en", folder: to });
console.log("whisper.cpp ready in", to);
