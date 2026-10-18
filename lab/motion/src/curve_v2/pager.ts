import type { Caption } from "@remotion/captions";

// Caption pages for the Curve Shorts: up to 4 words and 16 characters, never across a sentence or comma, never
// ending on a function word ("IT TO", "WITH UP" slipped through on Short 1), and a new page before a conjunction.
export type CapWord = { text: string; fromMs: number; toMs: number };
export type CapPage = { startMs: number; durationMs: number; tokens: CapWord[] };

const FUNCTION = new Set(["the", "a", "an", "to", "of", "and", "with", "from", "in", "it", "for", "on", "at", "its", "is", "up", "that", "his", "but", "so", "then", "has", "about", "can", "would", "will", "be", "what"]);
const BREAK_BEFORE = new Set(["and", "but", "then", "before", "after", "when", "while", "because", "so", "yet"]);

const NUMBER = /^(\d[\d.,]*|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|twenty|thirty|fifty|hundred)$/;
const UNIT = /^(seconds?|hours?|minutes?|miles?|mph|kg|g|tonnes?|percent)[.,!?]?$/;
const bare = (w: CapWord) => w.text.trim().toLowerCase().replace(/[^a-z0-9.']/g, "");

export const makePages = (captions: Caption[]): CapPage[] => {
  const words: CapWord[] = [];
  for (const c of captions) {
    if (!c.text.startsWith(" ") && words.length > 0) {
      const w = words[words.length - 1];
      w.text += c.text;
      w.toMs = c.endMs;
    } else {
      words.push({ text: c.text, fromMs: c.startMs, toMs: c.endMs });
    }
  }
  const out: CapPage[] = [];
  let cur: CapPage | null = null;
  const close = (p: CapPage | null) => {
    if (p && p.tokens.length > 0) p.durationMs = p.tokens[p.tokens.length - 1].toMs - p.startMs;
  };
  for (const w of words) {
    const len = cur ? cur.tokens.map((t) => t.text).join("").trim().length : 0;
    // keep a proper name together ("TOP GEAR", "TESLA ROADSTER"): two capitalised words in a row stay on one page
    const prev = cur && cur.tokens.length ? cur.tokens[cur.tokens.length - 1].text.trim() : "";
    const proper = /^[A-Z]/.test(prev) && /^[A-Z]/.test(w.text.trim()) && !/[.,!?]$/.test(prev);
    const full = cur !== null && (cur.tokens.length >= 4 || len + w.text.length > (proper ? 21 : 16));
    const conj = cur !== null && cur.tokens.length >= 2 && BREAK_BEFORE.has(bare(w));
    if (!cur || full || conj) {
      const carry: CapWord[] = [];
      while (cur && cur.tokens.length > 1 && FUNCTION.has(bare(cur.tokens[cur.tokens.length - 1]))) {
        carry.unshift(cur.tokens.pop() as CapWord);
      }
      // a number stays with its unit ("TWO SECONDS", "SIX HOURS")
      if (cur && cur.tokens.length > 1 && NUMBER.test(bare(cur.tokens[cur.tokens.length - 1])) && UNIT.test(bare(w))) {
        carry.unshift(cur.tokens.pop() as CapWord);
      }
      // a page left holding one function word ("AND", "BUT") joins the next page instead
      if (cur && carry.length > 0 && cur.tokens.length === 1 && FUNCTION.has(bare(cur.tokens[0]))) {
        carry.unshift(cur.tokens.pop() as CapWord);
        out.pop();
        cur = null;
      }
      close(cur);
      cur = { startMs: carry.length ? carry[0].fromMs : w.fromMs, durationMs: 0, tokens: carry };
      out.push(cur);
    }
    cur.tokens.push(w);
    close(cur);
    if (/[.,!?]$/.test(w.text.trim()) && !/^\s*\d+\.$/.test(w.text)) cur = null;
  }
  return out;
};
