#!/usr/bin/env python3
"""Lint a film script for the narration rules in CRAFT.md §2 before it is voiced.

Usage: python3 script_lint.py lab/ch2/ep05/script.py [more scripts...]

Reads LINES (How They Profit) or CHAPTERS (The Curve) and flags:
  NOT-X     a sentence starting "Not ..." (the "Not X. Y." device)
  COLON     a colon reveal inside narration ("...: the answer")
  STACCATO  three or more sentences of 5 words or fewer in a row
  NUMBERS   a sentence with three or more numbers in it
  HERE'S    stock openers: "Here's the thing", "Let that sink in", "But here's"
Exit code 1 if anything is flagged, so it can gate a voicing step.
"""
import re
import runpy
import sys

STOCK = ("here's the thing", "let that sink in", "but here's", "make no mistake", "the truth is")
NUM = re.compile(r"\$?\d[\d,.]*%?|\b(?:one|two|three|four|five|six|seven|eight|nine|ten|hundred|thousand|million|billion|trillion)\b",
                 re.I)


def narration(path):
    """The script modules are plain data (dicts built with dict(...)), so run them and read LINES or CHAPTERS."""
    mod = runpy.run_path(path)
    out = []
    for d in mod.get("LINES", []):
        out.append((d.get("id", "?"), d.get("text", "")))
    for ch in mod.get("CHAPTERS", []):
        out += [(ch.get("id", "?"), beat[0]) for beat in ch.get("beats", [])]
    return out


def lint(path):
    issues, run = [], []
    for lid, text in narration(path):
        for s in re.split(r"(?<=[.!?])\s+", text.strip()):
            if not s:
                continue
            low = s.lower()
            if re.match(r"not\b", low):
                issues.append((lid, "NOT-X", s))
            if re.search(r"\w: [a-z]", s) and not re.search(r"\d:\d", s):
                issues.append((lid, "COLON", s))
            if len(NUM.findall(s)) >= 3:
                issues.append((lid, "NUMBERS", s))
            if any(k in low for k in STOCK):
                issues.append((lid, "HERE'S", s))
            run = run + [s] if len(s.split()) <= 5 else []
            if len(run) == 3:
                issues.append((lid, "STACCATO", " | ".join(run)))
    return issues


if __name__ == "__main__":
    bad = 0
    for p in sys.argv[1:]:
        found = lint(p)
        print(f"{p}: {len(found)} flagged")
        for lid, kind, s in found:
            print(f"  [{kind}] {lid}: {s}")
        bad += len(found)
    sys.exit(1 if bad else 0)
