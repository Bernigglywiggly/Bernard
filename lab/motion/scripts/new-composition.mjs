// Scaffolds a new composition and registers it in src/Root.tsx.
//
//   npm run new -- MyScene                       1920x1080, 30 fps, 5 s
//   npm run new -- MyShort --vertical --seconds 20
//   npm run new -- MyClip --width 3840 --height 2160 --fps 60
import { existsSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const args = process.argv.slice(2);
const name = args.find((a) => !a.startsWith("--"));
const flag = (key, fallback) => {
  const i = args.indexOf(`--${key}`);
  return i >= 0 && args[i + 1] ? Number(args[i + 1]) : fallback;
};

if (!name || !/^[A-Z][A-Za-z0-9]*$/.test(name)) {
  console.error("Usage: npm run new -- <PascalCaseName> [--vertical] [--width W --height H] [--fps N] [--seconds S]");
  process.exit(1);
}

const vertical = args.includes("--vertical");
const width = flag("width", vertical ? 1080 : 1920);
const height = flag("height", vertical ? 1920 : 1080);
const fps = flag("fps", 30);
const seconds = flag("seconds", 5);
const file = join(root, "src", "compositions", `${name}.tsx`);
const rootFile = join(root, "src", "Root.tsx");

if (existsSync(file)) {
  console.error(`${file} already exists.`);
  process.exit(1);
}

const title = name.replace(/([a-z0-9])([A-Z])/g, "$1 $2").toUpperCase();
const source = readFileSync(join(root, "scripts", "composition-template.tsx.tpl"), "utf8")
  .replaceAll("__NAME__", name)
  .replaceAll("__TITLE__", title)
  .replaceAll("__WIDTH__", String(width))
  .replaceAll("__HEIGHT__", String(height))
  .replaceAll("__FPS__", String(fps))
  .replaceAll("__FRAMES__", String(Math.round(seconds * fps)));
writeFileSync(file, source);

const importMarker = "// @new-composition-imports";
const registerMarker = "{/* @new-composition-registrations";
let rootSource = readFileSync(rootFile, "utf8");
if (!rootSource.includes(importMarker) || !rootSource.includes(registerMarker)) {
  console.error(`Created ${file}, but the markers are missing from src/Root.tsx: register <${name}Composition /> by hand.`);
  process.exit(1);
}
rootSource = rootSource
  .replace(importMarker, `import { ${name}Composition } from "./compositions/${name}";\n${importMarker}`)
  .replace(registerMarker, `<${name}Composition />\n      ${registerMarker}`);
writeFileSync(rootFile, rootSource);

console.log(`Created src/compositions/${name}.tsx (${width}x${height}, ${fps} fps, ${seconds} s) and registered it in src/Root.tsx.`);
console.log(`Preview: npm run dev, then open http://localhost:3000/${name}`);
console.log(`Render:  npx remotion render ${name} out/${name}.mp4`);
