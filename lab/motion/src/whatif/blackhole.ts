import type { WhatIfFilm } from "./types";

// A black hole of 10 solar masses (public/whatif/blackhole/SCIENCE.md has the working).
const GM = 1.3275e21; // m^3/s^2
const MOON = 4.9048e12 / Math.pow(3.844e8, 3); // the Moon's tidal coefficient on Earth, s^-2
const MILE = 1609.344;
const START = 4.8e6; // miles
const BREAK = 745000; // miles: the stretching across Earth equals its surface gravity
const T_BREAK = 44; // seconds into the film

const miles = (t: number) => START * Math.pow(BREAK / START, t / T_BREAK);
const tides = (d: number) => GM / Math.pow(d * MILE, 3) / MOON;

const sig = (x: number, digits = 2) => {
  const p = Math.pow(10, Math.floor(Math.log10(x)) - digits + 1);
  return (Math.round(x / p) * p).toLocaleString("en-US");
};

export const blackhole: WhatIfFilm = {
  title: "What if Earth fell into a black hole?",
  clips: [1, 2, 3, 4, 5, 6, 7].map((i) => `whatif/blackhole/c${i}.mp4`),
  clipSeconds: 10,
  sound: "whatif/blackhole/sound.wav",
  captions: [
    { from: 5.5, to: 9.6, text: "Ten times the Sun's mass. Only 37 miles wide." },
    { from: 12.5, to: 17.0, text: "It bends the starlight behind it." },
    { from: 21.5, to: 26.0, text: "Even the air is pulled towards it." },
    { from: 31.0, to: 35.5, text: "The ground begins to crack." },
    { from: 40.5, to: 46.0, text: "750,000 miles out, its pull beats Earth's gravity." },
    { from: 50.5, to: 55.0, text: "We never reach the edge." },
    { from: 61.0, to: 66.5, text: "We become part of its ring." },
  ],
  readout: (t) => {
    const d = miles(t);
    const fade = Math.min(1, Math.max(0, (t - 0.5) / 1.0)) * Math.min(1, Math.max(0, (60 - t) / 1.5));
    if (t < T_BREAK + 1) {
      return {
        label: "DISTANCE",
        value: `${sig(d, 3)} mi`,
        sub: `TIDES ${sig(tides(d))}× THE MOON'S`,
        opacity: fade,
      };
    }
    return { label: "EARTH", value: "Breaking up", sub: `${sig(d, 2)} MI FROM THE BLACK HOLE`, opacity: fade };
  },
};
