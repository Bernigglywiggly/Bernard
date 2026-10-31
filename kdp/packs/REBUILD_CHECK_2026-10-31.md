# Rebuild check, Sat 31 Oct 2026 (independent; files built 04:08-04:09)

**1. Render: PASS.** Winter 2, 12, 55, 80; Christmas 5, 19, 42, 81; key entries W55, C19: legible, nothing clipped, each listed word at its stored cells once, shading equals those cells. All 100 printed grids, lists, titles and key shading per book match wordlists.json.

**2. Rude scan: PROBLEM.**
- Toolchain RUDE list (110 terms, 8 directions): 0 hits outside listed words. NOOSE/STAB/GORE/WOP/WTF gone (present in the backup).
- My own list finds slurs/obscenities in filler that RUDE lacks, same class as WOP (already in the SHIPped files):
  - Winter: YID p7,11,51,84; WOG 16,61; SPIC 31,33; HEEB 70; FCK 20,99; JAP 67,80 (10,25 from listed-word letters); GYP 34 (45); HOMO 40,70; TARD 7,8,54; FML 60,74,78; LOLI 11.
  - Christmas: YID/YIDS 34,37,38,69,87,91,98; WOG 19,37,45,91,100; SPIC 49,87; HEEB 70; FCK 58; JAP 59,84; TARD 4,64,78,80; MONG 28; FML 38,42,61; LOLI 25; GYP 62,69 (listed-word letters).
- Fix: add yid yids wog spic spik heeb jap japs gyp homo tard mong fck fml loli to RUDE, rebuild (about 30 s each), rescan.

**3. Unchanged puzzles: PASS.** Changed sets exactly as stated; all other puzzles identical to backup (JSON and rendered pages). Changed ones differ only in filler (Winter 55: same words, re-placed).

**4. Covers: PASS.** 17.5202 x 11.2500 in (backup 17.5133), one page, fonts embedded, text and pixels identical to backup; kdp_gate.py PASS (exit 0) for both.

**5. Packs: PASS.** Exactly two backwards words (L, U, UL, DL) in all 100 puzzles per book. Ranges match: Winter 16-19, Christmas 15-19. Minor: across+down is 78% overall but not a majority in Winter 96 and Christmas 28, 32, 59, 66, 86, 94, 96.

**FIX FIRST** (item 2 only; the rest is SHIP)
