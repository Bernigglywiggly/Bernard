import type { Caption } from "@remotion/captions";

// Caption pages for the Curve Shorts (v2, 23 Oct 2026, after critics on Shorts 4-5 found pages like "TELLS" alone,
// "PROFIT HAD" and "FROM TESLA'S"): split the narration into phrases first (at , . ; : ! ? and before a conjunction),
// then cut each phrase into as few pages as fit (4 words, 20 characters), balanced (5 words = 3 + 2, never 4 + 1),
// and move a boundary so a page never ends on a function word, an adjective or a possessive, and a number keeps its
// unit and a proper name stays whole.
export type CapWord = { text: string; fromMs: number; toMs: number };
export type CapPage = { startMs: number; durationMs: number; tokens: CapWord[] };

const WEAK = new Set(["the", "a", "an", "to", "of", "and", "with", "from", "in", "it", "for", "on", "at", "its", "is", "up", "that", "his",
  "her", "but", "so", "then", "has", "had", "have", "was", "were", "are", "been", "be", "about", "can", "would", "will", "what", "by", "as",
  "their", "our", "your", "my", "this", "these", "those", "into", "than", "each", "every", "more", "most", "very", "other", "own", "new",
  "real", "small", "big", "public", "virtual", "quarterly", "gross", "flying", "not", "no", "all"]);
const BREAK_BEFORE = new Set(["and", "but", "then", "before", "after", "when", "while", "because", "so", "yet"]);
const NUMBER = /^(\d[\d.,]*|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|twenty|thirty|forty|fifty|hundred)$/;
const UNIT = /^(seconds?|hours?|minutes?|miles?|mph|kg|g|tonnes?|percent|times|days?|years?)[.,;:!?]?$/;
const bare = (w: CapWord) => w.text.trim().toLowerCase().replace(/[^a-z0-9.'%]/g, "");
const ends = (w: CapWord) => /[.,;:!?]$/.test(w.text.trim()) && !/^\d+\.$/.test(w.text.trim());
const isWeak = (w: CapWord) => WEAK.has(bare(w).replace(/[.']$/, "")) || /'s$/.test(bare(w));
const isCap = (w: CapWord) => /^[A-Z]/.test(w.text.trim());
const chars = (ws: CapWord[]) => ws.map((t) => t.text.trim()).join(" ").length;

export const makePages = (captions: Caption[]): CapPage[] => {
  const words: CapWord[] = [];
  for (const c0 of captions) {
    const forced = c0.text.includes("¶");
    const c = forced ? { ...c0, text: c0.text.replace("¶", "") } : c0;
    if (forced) words.push({ text: "¶", fromMs: c.startMs, toMs: c.startMs });
    if (!c.text.startsWith(" ") && words.length > 0 && words[words.length - 1].text !== "¶") {
      const w = words[words.length - 1];
      w.text += c.text;
      w.toMs = c.endMs;
    } else {
      words.push({ text: c.text, fromMs: c.startMs, toMs: c.endMs });
    }
  }
  // 1. phrases
  const phrases: CapWord[][] = [];
  let cur: CapWord[] = [];
  const hasForced = words.some((w) => w.text === "¶");
  for (const w of words) {
    if (w.text === "¶") {
      if (cur.length) phrases.push(cur);
      cur = [];
      continue;
    }
    if (!hasForced && cur.length >= 2 && BREAK_BEFORE.has(bare(w))) {
      phrases.push(cur);
      cur = [];
    }
    cur.push(w);
    if (!hasForced && ends(w)) {
      phrases.push(cur);
      cur = [];
    }
  }
  if (cur.length) phrases.push(cur);
  // 2. balanced pages per phrase, with boundary fixes
  const out: CapPage[] = [];
  for (const ph of phrases) {
    const n = ph.length;
    // manual pages (the script's " / " breaks) stay whole unless they're over 5 words or 26 characters
    const k = hasForced
      ? (n > 5 || chars(ph) > 26 ? Math.max(2, Math.ceil(chars(ph) / 24)) : 1)
      : Math.max(1, Math.ceil(n / 4), Math.ceil(chars(ph) / 20));
    const sizes = Array.from({ length: k }, (_, i) => Math.floor(n / k) + (i < n % k ? 1 : 0));
    const cuts: number[] = []; // index where each page after the first starts
    let acc = 0;
    for (let i = 0; i < k - 1; i++) {
      acc += sizes[i];
      cuts.push(acc);
    }
    for (let c = 0; c < cuts.length; c++) {
      const lo = c === 0 ? 0 : cuts[c - 1];
      const hi = c + 1 < cuts.length ? cuts[c + 1] : n;
      const bad = (i: number) => isWeak(ph[i - 1]) || (NUMBER.test(bare(ph[i - 1])) && UNIT.test(bare(ph[i]))) ||
        (isCap(ph[i - 1]) && isCap(ph[i]) && !ends(ph[i - 1]) && i - 1 > lo);
      // the nearest clean cut on either side that keeps both pages at 1-4 words; else leave it
      let best = cuts[c];
      for (let d = 0; d <= 3; d++) {
        const tries = d === 0 ? [cuts[c]] : [cuts[c] - d, cuts[c] + d];
        const ok = tries.find((at) => at > lo && at < hi && at - lo <= 4 && hi - at <= 4 && !bad(at));
        if (ok !== undefined) {
          best = ok;
          break;
        }
      }
      cuts[c] = best;
    }
    const bounds = [0, ...cuts, n];
    for (let i = 0; i < bounds.length - 1; i++) {
      const tokens = ph.slice(bounds[i], bounds[i + 1]);
      if (!tokens.length) continue;
      out.push({ startMs: tokens[0].fromMs, durationMs: tokens[tokens.length - 1].toMs - tokens[0].fromMs, tokens });
    }
  }
  return out;
};
