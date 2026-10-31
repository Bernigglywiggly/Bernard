import { blackhole } from "./blackhole";
import type { WhatIfFilm } from "./types";

// Every "What if" film, by id. Add a film: a data file next to blackhole.ts, then one line here and one
// <Composition> in Root.tsx.
export const FILMS: Record<string, WhatIfFilm> = { blackhole };
