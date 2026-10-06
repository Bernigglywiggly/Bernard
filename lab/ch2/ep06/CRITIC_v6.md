# CRITIC v6: HTP06 (Visa) · HTP06_MASTER_v6.mp4 (1920x1080, 4:18, 30 fps)

STATUS: COMPLETE. Independent critic; did not build the film and wrote none of CRITIC_v1 to v4. Read-only pass.

Method. 129 frames at 2 s steps on 22 contact sheets (6 per sheet, 800x450 tiles), all read. 0.2 s sheets of
0:08.0-0:12.8, 0:13.2-0:15.6, 0:19.6-0:24.4, 0:25.6-0:30.4, 1:31.0-1:33.4, 2:15.8-2:18.2, 2:34.0-2:38.8,
3:25.4-3:30.2, 4:06.8-4:09.2, all read. Full-resolution frames and native crops at 0:09.4, 0:10.0, 1:08.5, 1:36,
2:41.9, 2:52, 2:58.5, 4:05.5. Per-frame statistics on all 7,740 frames (lit-pixel share above the caption band, red
and cyan pixel counts, frame difference, edge contact), and the same statistics on HTP06_full_v5.mp4 for comparison.
Text heights measured on full-resolution frames as ink height of the line (ascender to descender), so they are
generous; x-height is roughly half. Audio: ebur128, astats, silencedetect, windowed RMS against lines.json. One
attempt to re-read the 10-K on sec.gov returned only the opening of the document (it confirmed the "not a financial
institution" sentence and the "$17 trillion" sentence, nothing else).

Result in one line: **v6's three changes are all correct and nothing regressed against v5; the film still carries
faults that v5 also had, and the upload sheet has errors.**

| Gate | Result |
|---|---|
| 1 Facts | PASS WITH NOTES (one check to do before upload: F1) |
| 2 Picture | PASS WITH NOTES |
| 3 Sound | PASS |
| 4 Platform | PASS WITH NOTES (POST.md must be corrected first: P1, P2) |

---

## 1. Facts gate

### 1a. Every number, quote and claim, voice and screen

| Time | Spoken (lines.json) | On screen | Source in FACTS.md / SOURCES | Verdict |
|---|---|---|---|---|
| 0:01-0:13 | card tapped in a café in Lisbon, message to a bank in Ohio, "about a second" | "A café, Lisbon 38.72N 009.14W", "A bank, Ohio 39.96N 083.00W", "message out 0.03…0.50 s", "answer back 0.50…0.69 s", "approved · about 1 s" | Illustration, labelled | OK. Label "illustration · one card payment across a border · not a real transaction" is on screen 0:00-0:13.6 and 4:08-4:18. The invented timings (0.12 s and so on) are covered by it. |
| 0:14 | "Last year, $17 trillion of payments and cash" | "$17 trillion · payments and cash volume on the network · fiscal 2025 · Form 10-K"; "each cell $100 billion moved" (170 cells) | 10-K quote, re-confirmed today | OK |
| 0:20, 4:08 | "never held any of the money"; "a company that was never holding it" | title of the film | **Not in FACTS.md.** FACTS supports "does not issue cards, extend credit… nor bear credit risk" and "IRFs are paid by acquirers to issuers". Neither says Visa never holds funds. | **See F1** |
| 0:43-0:52 | "Visa is not a financial institution" | quote + "We do not issue cards, extend credit or set rates and fees for account holders." + "Visa Form 10-K · fiscal 2025" | 10-K quote | OK. The second line is a truncation shown without an ellipsis (the sentence continues "…of Visa products nor do we earn revenue from or bear credit risk…"). Meaning not changed. |
| 0:53 | "the loss belongs to the bank" | "carries the loss when a bill goes unpaid" | 10-K "nor… bear credit risk" | OK |
| 1:00-1:05 | bank "hands a fee across to the bank that issued the card" | "interchange · paid by the shop's bank to the cardholder's bank" | 10-K "IRFs are paid by acquirers to issuers" | OK |
| 1:05-1:10 | "for most shops it is a large part of what accepting a card costs" | "the largest of the fees a shop pays on a card · Federal Reserve Bank of Richmond, Economic Brief 11-05" | Richmond Fed EB 11-05 | **Supported, see 1b** |
| 1:10-1:17 | "Visa writes the default rates… without Visa collecting it" | "collects none of it" | 10-K "We establish default IRFs"; "paid by acquirers to issuers" | OK |
| 1:18-1:31 | "It pays banks to put Visa's name on their cards, and every card they issue sends more messages" | "The fee pays banks to issue the cards. Every card sends more messages down the wire." | **None.** This is the film's reading of why interchange exists; no line in FACTS.md | FIX (F3): fair as analysis, but it is stated as fact on screen with no source |
| 1:31 | "counted on three meters" | "three meters · fiscal 2025 · Visa results, 28 Oct 2025"; three tracks, then "+ a fourth line" | 8-K | OK (v4's three-versus-four contradiction is fixed) |
| 1:36-1:45 | service "rises with the amount spent on a bank's cards… $17.5 billion" | "01 service · for being on the network at all · $17.5B" | Figure: 8-K. The description of what the charge is: not in FACTS.md | Figure OK; description NICE (F5) |
| 1:45-1:52 | "257.5 billion transactions" | "257.5 billion transactions processed" | 8-K | OK |
| 1:52 | "roughly 700 million messages every day" | "about 700 million a day" | derived, 257.5bn / 365 = 705m | OK |
| 1:56 | "$20 billion… the largest meter" | "02 data processing · a charge on every message · $20.0B" | 8-K | OK |
| 2:01-2:10 | "only runs when the card and the shop are in different countries… $14.2 billion" | "03 international · only when card and shop are in different countries · $14.2B" | Figure: 8-K. "Only when": not in FACTS.md | Figure OK; description NICE (F5) |
| 2:11 | "about four billion more", "licences and extra services" | "+ a fourth line · licences and extra services · $4.1B" | 8-K ($4.1B) | OK |
| 2:17-2:30 | "paid $15.8 billion in incentives… the price of keeping their cards on Visa and off a rival network" | "charged to banks and partners · $55.8 billion"; "$15.8B handed back as incentives · the price of keeping cards on this network" | $15.8B: 8-K. $55.8B: derived (17.5+20.0+14.2+4.1). "The price of keeping…": interpretation, not in FACTS.md | Figures OK; interpretation NICE (F5) |
| 2:30 | "$40 billion of net revenue" | "$40.0 billion · net revenue · fiscal 2025" | 8-K | OK |
| 2:34-2:42 | "about 24 cents" per hundred dollars | "$40.0 billion what Visa kept · about 24¢ of every $100 moved" | derived, 40.0 / 17,000 = 0.235% | OK ("about") |
| 2:48 | "cost $16 billion… includes a large sum set aside for lawsuits" | "$16.0B to run" | 8-K | Figure OK. Drawing is out of proportion: see picture item N2 |
| 2:56-3:04 | "After tax, the profit was $20.1 billion… about 50 cents of every dollar" | "$20.1B profit after tax · 50¢ per dollar"; "then tax" | 8-K; derived 50.25% | OK |
| 3:05-3:18 | bank needs branches, loan books, reserves; "one more message costs it almost nothing" | "A bank needs… / The network needs data centres, a rulebook / one more message costs it almost nothing" | None (analysis) | NICE: opinion, reasonable, unsourced |
| 3:19 | "$22.8 billion back to shareholders through buybacks and dividends" | "$22.8B back to shareholders · buybacks and dividends, fiscal 2025" | 8-K | OK |
| 3:30 | "Shops have been taking Visa to court over interchange for years" | "Shops have taken Visa to court over this fee for years." | **FACTS.md lists this as NOT verified** | FIX (F2) |
| 3:34 | "set aside $2.5 billion for that litigation and other legal matters" | "$2.5 billion · set aside for the interchange litigation and other legal matters · fiscal 2025" | 8-K quote | OK |
| 3:40 | "regulators and central banks in a number of countries are reviewing those fees" | quote: "Regulatory authorities and central banks in a number of jurisdictions have reviewed or are reviewing these fees, rules and practices." · "Visa Form 10-K · fiscal 2025" | 10-K quote | OK. Voice says "countries", source says "jurisdictions"; voice drops "have reviewed". Acceptable. |
| 3:48 | "Here's how I'd read it. Visa's real product is the rulebook…" | "Visa's real product is the rulebook that lets a café in Lisbon trust a bank in Ohio. The wires only deliver it." | Opinion, flagged as such in the voice | OK |
| 3:59-4:07 | "most of what a card payment costs you goes to banks, so the rate your own bank quotes you is the part worth negotiating" | "If you run a shop: interchange goes to the banks, not to Visa." + "the rate your bank quotes is the part to negotiate" | Richmond Fed EB 11-05 (first half) | **Supported, see 1b** |

Voice and screen never disagree on a number. "Last year" is spoken six times for fiscal 2025 (0:14, 1:41, 1:49,
2:22, 2:49, 3:34); every one has "fiscal 2025" on screen beside it.

### 1b. The two interchange lines against the Richmond Fed quotations

Quotations recorded in FACTS.md: merchants "are assessed fees… the largest of which is called an 'interchange' fee";
it "is set by the card network… and is ultimately paid to the bank that issued the card"; the merchant discount
"includes the interchange fee paid to the card-issuing bank, the network assessment fee paid to the card network,
and the acquiring fee paid to the acquirer."

- **Line 1, "for most shops it is a large part of what accepting a card costs": supported.** The largest of three
  components is a large part. "For most shops" is a hedge the source does not make, but it weakens the claim rather
  than strengthening it.
- **Line 2, first half, "most of what a card payment costs you goes to banks": supported, by arithmetic.** If
  interchange is larger than the network assessment, then interchange plus the acquiring fee is more than half the
  total. One soft spot: the source says "acquirer", the film says "bank"; many acquirers are processors, not banks.
- **Line 2, second half, "so the rate your own bank quotes you is the part worth negotiating": goes beyond the
  quotations.** The source says nothing about negotiating. It is advice, it follows "Here's how I'd read it", and the
  description says "not financial advice", so it reads as the author's view. Acceptable; it is not a sourced fact
  and should not be described as one.
- **Where the wording goes past the source: place and date.** The brief is about the United States in 2011. The
  film's example is a café in Lisbon, and the on-screen credit ("Federal Reserve Bank of Richmond, Economic Brief
  11-05") gives neither the year nor the country. FACTS.md records this limit; the screen does not. POST.md does
  give "May 2011". Fix in F4.

Verdict on the two lines: **the v4 BLOCKER (item 4) is closed.**

### 1c. POST.md

- **Chapter times are all about 2 s early (P1).** Each mark lands while the previous chapter's last sentence is
  still being spoken. From lines.json: Four parties starts 26.11 (sheet says 0:24); The fee 60.12 (0:58); Three
  meters 91.69 (1:30); The money it hands back 136.63 (2:15); Half 163.15 (2:41, which cuts into "…Visa kept about
  24 cents", ending 162.63); The rulebook 206.16 (3:24). Correct list: 0:00, 0:26, 1:00, 1:31, 2:16, 2:43, 3:26.
- Source list matches SOURCES and FACTS.md. No source has a link; FACTS.md has both EDGAR URLs. Add them, and the
  Richmond Fed URL (F6).
- "28 October 2025" for the 8-K is in script.py and on screen but FACTS.md records only "Oct 2025". Record the day
  in FACTS.md (NICE).
- Description text: accurate against FACTS.md. "an illustration, not a real transaction" is there. Synthetic voice
  is disclosed.

### 1d. Issues

| # | Time | Sev | What | Suggested fix |
|---|---|---|---|---|
| F1 | 0:20, 4:08, title | **FIX, check before upload** | The film's headline claim, "never held any of the money" / "never touches your money", has no entry in FACTS.md. What FACTS.md supports is narrower: Visa does not issue, lend, or bear credit risk, and does not receive interchange. From my own recollection of Visa's annual reports (not verified today, sec.gov returned only the top of the filing): the balance sheet carries "settlement receivable" and "settlement payable" lines and the notes describe Visa guaranteeing settlement between its clients, which would mean the banks' funds do pass through Visa's settlement process. If that is right, "never held" is a simplification a knowledgeable viewer can challenge under the film's own title. | Open the FY2025 10-K, search "settlement receivable" and "settlement guarantee", record what it says in FACTS.md. If funds pass through Visa: add one sentence to the description ("Visa runs the settlement between the banks; it holds no deposits and lends nothing") and prefer title 3. No re-voice needed. |
| F2 | 3:30 | FIX | "for years", spoken and on screen, is still marked NOT verified in FACTS.md. The 8-K quote proves the litigation exists, not its duration. | Record the filing year of the interchange MDL from the 10-K legal note in FACTS.md and SOURCES. |
| F3 | 1:18-1:31 | FIX | "The fee pays banks to issue the cards" is on screen as a flat statement with no source; it is the film's interpretation. | Record a supporting sentence in FACTS.md (the Richmond brief or the 10-K's description of interchange), or accept it as the author's reading and say so in the description. |
| F4 | 1:07-1:31, 3:29-4:07 | FIX (next render) | Richmond source line on screen has no year and no country. | "…Federal Reserve Bank of Richmond, 2011 (US)". |
| F5 | 1:36, 2:01, 2:22 | NICE | Plain-language descriptions of service revenue, international revenue and incentives are not recorded in FACTS.md. | Add the 10-K's definitions to FACTS.md. |
| F6 | POST.md | FIX | No links in the source list. | Add the two EDGAR URLs and the Richmond Fed URL. |
| F7 | whole film | NICE | Fiscal 2026 results are due about three weeks after today. "Last year" (six times) will then point at the wrong year. On-screen "fiscal 2025" labels and the description cover it. | Keep the description line; pin a comment when FY2026 is out. |

**Facts gate: PASS WITH NOTES.** No number is wrong. The two interchange lines are supported. One claim (F1) needs a
ten-minute check before upload because the title rests on it.

---

## 2. Picture gate

### 2a. The three v6 changes

| Change | Verdict | Evidence |
|---|---|---|
| 1080p | **TRUE** | h264, 1920x1080, yuv420p, 30 fps, 7,740 frames, 258.000 s. Lit-pixel share per frame matches v5 within 1 point on every frame, so nothing moved that was not meant to. |
| Last chapter raised; caption clear of the cyan box | **TRUE** | 4:05.5 full resolution: cyan box "the rate your bank quotes is the part to negotiate" occupies y 832-851; the caption plate's top rule is at y 876. 25 px clear, for the whole of 4:03.5-4:07. The top quote "Visa is not a financial institution." is whole at y 83 for the whole chapter. Nothing touches the top edge from 3:29 to 4:07 (edge-contact count zero). **v4's BLOCKER X1 is closed.** |
| Richmond source line under "interchange" | **TRUE, but too small** | Appears 1:07.0, stays to 1:31 and returns 3:29-4:07. Text: "the largest of the fees a shop pays on a card · Federal Reserve Bank of Richmond, Economic Brief 11-05". Ink height 12 px (x-height about 6 px) at about 54% grey at 1:08; smaller in the last chapter (about 7 px ink). Readable on a desktop at full screen, not on a phone. |

Red: present continuously 3:28.4-4:07.9 on the interchange arc and nowhere else in the film. Confirmed.

### 2b. Issues present in v6

Every item below is also in v5 (checked by statistics, and the worst one by frame).

| # | Time | Sev | What | Suggested fix |
|---|---|---|---|---|
| N1 | 0:08.8-0:12.0 | **FIX (highest)** | **Ghost element in the hook.** Four black-filled rectangles (the party boxes of the next scene, which sits on the arc at that spot) are drawn over the opening. At 0:09.6-0:10.3 they strike through the cyan tag, blacking out the lower half of "message out" (full-resolution frame at 0:10.0). At 0:10.4-0:12.0 they chop the apex of the arc into dashes. Three seconds, inside the first twelve. | Give the four-parties boxes zero opacity (fill and outline) until 0:28. |
| N2 | 2:49-2:57 | FIX | In the lit cell the dark block labelled "$16.0B to run" is drawn as exactly half of net revenue (cyan x 564-872, teal x 873-1182 at 2:52). $16.0B is 40% of $40.0B. The split only becomes true at 2:58 when "then tax" is added. For 8 s the drawing says $20B. | Draw the cost block at 40% at 2:49, widen to 50% when "then tax" lands. |
| N3 | 2:35.2-2:36.8 | FIX | Picture area is empty: 28 consecutive frames (2:35.3-2:36.2, 0.93 s) with no lit pixel above the caption, under 0.8% lit for 1.6 s. A fade to black in a film whose idea is one unbroken camera. CRITIC_v4 found no such frame in v4; it arrived in v5. | Keep the revenue bar on screen until the arc enters (2:36.2), or start the arc 1 s earlier. |
| N4 | 0:29.1-0:37.6, 0:40-0:43 | FIX | Four-parties scene opens near-empty: under 1.2% lit for 8.5 s, under 2% for 19 s (0:28.5-0:47.7). Boxes 3 and 4 are a few grey levels above black. Near-still 0:31.7-0:35.3 and 0:37.3-0:43.2. Open since v1 (item 14). | Draw unlit boxes with a 35% grey outline; add the scene label at readable size. |
| N5 | 0:27.8-0:28.4, 2:37.0-2:38.2, 3:27.0-3:27.8, 4:08-4:15 | FIX | Caption plate over picture. In the three transits the plate is a hard black box knocking a hole in the grey grid (worst 2:37.0-2:38.2). At the close it covers the map's axis labels 060W-020W and the bottom of both continents for 7 s. | Hide the caption plate's black fill during transits; at the close, raise the map 60 px or shorten the caption to two lines. |
| N6 | 0:28.6-0:29.6, 3:28.2-3:29.0, 4:07.6-4:08.0 | FIX | Next scene arrives as a thumbnail (about 300 px wide at 0:29.2, 180 px at 3:28.4) riding the arc in a near-black frame, then inflates. v4's X6, unchanged. | Start the push-in earlier so the target is a third of frame width when first visible. |
| N7 | 0:20.0-0:22.0 | FIX | "$17 trillion" slides out through the left edge: "$" clipped at 0:20.0, "17 trillion" 0:20.4, "trillion" 0:20.8, "illion" 0:21.0, "on" 0:21.4. Its sub-line is cut the same way. v4's V2, unchanged. | Fade the headline out in place before the push. |
| N8 | 0:08.8-0:10.8 | NICE | "A café, Lisbon" and its coordinates slide under the caption plate and out of the bottom-right corner ("A caf", "38.72N" alone at 0:10.4). v1 item 24, unchanged. | Fade the label before it reaches the plate. |
| N9 | 0:14.4-0:15.0 | NICE | Near-empty transit frame: map sliver on the top edge, "$17 trillion" at about 15% grey. v2's N6, unchanged. | Bring the headline in at full strength 0.3 s earlier. |
| N10 | 2:17.7-2:22.0 | NICE | 4.3 s under 1.2% lit: title, an empty outlined bar and a grey stub. v3's V7, unchanged. | Start the $15.8B fill at 2:18. |
| N11 | 3:26.4-3:27.0 | NICE | During the pull-back, the old "$40.0 billion / what Visa kept / about 24¢ of every $100 moved" note reappears beside the shrinking cell and collides with the caption ("$100 moved" pokes out to the right of the plate at 3:27.0). | Keep that note hidden after 2:44. |
| N12 | 3:06-3:24 | NICE | Five-line caption plate cuts the cell's glow with a hard edge. The cell itself is now clear of the plate. | Split the caption in two. |
| N13 | 3:30-4:07 | NICE | Lower-left quadrant (about x 0-1000, y 540-860) is empty for the whole last chapter; the diagram occupies the top-left third. Near-still 3:45.5-3:48.2 and 4:04.1-4:06.4. | Scale the diagram up 25% or centre it vertically. |
| N14 | 1:04.0, 3:18.0, 0:26.0, 2:16.6 | NICE | Two captions superimposed for 2-4 frames at cross-fades. v1 item 25, unchanged. | Fade out fully before fading in. |
| N15 | 4:16-4:18 | NICE | Picture ends on a hard stop at full brightness while the sound fades. No end card (POST.md lists it as still to make). | Add a 0.5 s fade, or the end card. |
| N16 | arcs, lit cell | NICE | Glow on the arcs and the cell halo (CRAFT §3 bans glows on UI). v1 item 28, unchanged. | Reduce or remove. |

Checked and not found: no clipped element at the top edge in the last chapter; no flash; no frozen stretch of 1 s
or more (frozen share 3.9%, near-still 41.6%); no stray red; no element cut by the left edge in the last chapter
(the wire stub now ends at x 78).

### 2c. Text under about 14 px tall at 1080p (ink height, ascender to descender)

| Text | When | Height | Tone |
|---|---|---|---|
| "Visa Form 10-K · fiscal 2025" under the top quote | 3:29-4:07 | 7 px | 42% grey |
| Node numbers 01-04 | 0:30-1:31, 3:29-4:07 | 8 px | 53% grey |
| "collects none of it" | 3:29-4:07 | 8 px | white |
| "We do not issue cards, extend credit or set rates and fees for account holders." | 3:29-4:07 | 9 px | 54% grey |
| Richmond source line; "paid by the shop's bank to the cardholder's bank" | 3:29-4:07 | about 7-8 px | about 45% grey |
| Same two lines in the first appearance | 1:07-1:31 | 12-13 px | 54% grey |
| Node sub-labels ("collects card payments") | 3:29-4:07 | 13 px | 60% grey |
| "set aside for the interchange litigation and other legal matters · fiscal 2025" | 3:36-4:07 | about 11 px | about 45% grey |
| "one card payment · four parties" | 0:30-1:31 | about 10 px | about 45% grey |
| "handed back as incentives / the price of keeping cards on this network" | 2:22-2:34 | about 10 px | about 45% grey |
| "charged to banks and partners · $55.8 billion" | 2:18-2:34 | about 10 px | about 45% grey |
| Map axis labels (100W…000E), coordinates in the wide map | 0:12-0:14, 4:08-4:18 | about 9 px | about 45% grey |
| "three meters · fiscal 2025 · Visa results, 28 Oct 2025" | 1:33-2:16 | 14 px | 55% grey |
| "The wires only deliver it." | 3:56-4:07 | 15 px | 55% grey |

For reference, readable: meter labels 16 px, cyan tag text 17 px, node titles 18 px, shop advice 25 px, verdict
32-39 px, captions 33 px. Every source credit in the film is in the under-14 group. On a phone none of them can be
read; the description carries them, which is why F6 matters.

### 2d. CRITIC_v4's open items

| v4 item | Status in v6 |
|---|---|
| X1 top-edge clipping in the last chapter (BLOCKER) | **FIXED** |
| Item 4 spoken interchange claims (BLOCKER) | **FIXED** (sourced) |
| X2 three meters versus four tracks | **FIXED** (three tracks, then "+ a fourth line") |
| X4 caption plate on the cell corner | **FIXED** for the cell; glow still cut (N12) |
| X8 wire stub to the left edge | **FIXED** |
| V1 / claim (b) meters hole | **MOSTLY FIXED**: under 2% lit 1:32.6-1:37.8 (5.2 s), first fill starts 1:36 |
| X3 café node cut by the left edge 0:46-0:54, 1:11-1:19 | **FIXED** (all four boxes whole in every 2 s frame) |
| Item 2 / X6 thumbnail arrivals, chopped glyphs in transits | STILL PRESENT (N6) |
| Item 9 / V2 "$17 trillion" cut by the left edge | STILL PRESENT (N7) |
| Item 14 / N1 four-parties near-empty | STILL PRESENT (N4) |
| Item 15 small mono notes | STILL PRESENT (2c) |
| Item 18 slow push 2:45-2:57 | STILL PRESENT, and the block is mis-proportioned (N2) |
| X5 overview never held | STILL PRESENT |
| Item 20 hook | STILL PRESENT (see platform) |
| Item 21 "Last year" six times | STILL PRESENT (F7) |
| Items 24, N11 opening label cut | STILL PRESENT (N8) |
| Item 25 superimposed captions | STILL PRESENT (N14) |
| Item 26 quote detail truncated | STILL PRESENT |
| Item 27 "for years" unsourced | STILL PRESENT (F2) |
| Item 28 glows | STILL PRESENT (N16) |
| N6, V7, X9, X10, X11 | STILL PRESENT (N9, N10) |
| New since v4, not in any earlier report | N1 ghost boxes in the hook; N2 cost block out of proportion; N3 black second at 2:35 |

**Picture gate: PASS WITH NOTES.** No fault here would mislead a viewer except N2. N1 is the one I would fix before
anything else: it is a visible error on screen-text inside the first twelve seconds.

---

## 3. Sound gate (measured)

| Measure | v6 | Target |
|---|---|---|
| Integrated loudness | -14.0 LUFS | -14 |
| True peak | -1.9 dBFS | at or below -1 |
| Loudness range | 1.4 LU | flat, fine for narration |
| First 30 s / last 30 s | -13.9 / -14.2 LUFS | even |
| Max sample / clipped samples / flat factor | 0.777 / 0 / 0 | none |
| RMS left / right | -17.19 / -17.18 dB | balanced |
| Mix level while the voice speaks (38 lines) | -16.9 dB mean, range -17.5 to -16.0 | even |
| Music in the gaps between lines (36 gaps of 0.24-0.66 s) | -27.3 dB mean, range -36.8 to -23.8 | about 10 dB under the voice |
| One loud gap | 3:34.2-3:34.4 at -15.0 dB (peak 0.64) | the hit on "$2.5 billion"; intended, not clipped |
| Head | first 0.2 s -61.6 dB, bed fades in to -33 dB by 0:00.6, voice at 0:01.2 | no dead air |
| Tail | last word ends 4:15.0; -35.3 dB at 4:15, -38.8 at 4:16, -45.6 at 4:17, -54.9 at 4:17.5, -75.7 in the last 50 ms; digital silence only from 4:17.7 | faded, monotonic |
| Left/right correlation | 0.9996 | effectively mono |

The audio stream is not bit-identical to v5 (different MD5; v5 and v4 match each other), so it was encoded again
for the master; every measurement is unchanged from CRITIC_v4's table. The bed between lines is audible but only in
quarter-second windows, so the music never gets a moment of its own. Mono is acceptable for narration; a little
width on the bed would cost nothing (NICE).

**Sound gate: PASS.**

---

## 4. Platform gate (CRAFT §1 and §6)

- **Point of view: present.** "Here's how I'd read it" at 3:48, a verdict the filings do not hand over (the product
  is the rulebook), and advice to shop owners at 3:59. The 1:18 reading of what interchange is for is also the
  author's. This is enough to show an author.
- **Structure: distinct.** One tap on a map, one drawing, one camera; seven chapters whose names are specific to
  this film, not the fixed price/machine/proof/money/you/what-if/close set, and a different shape from EP05's
  follow-one-$100. Two forward teases (1:27 "In a minute…", 2:53 "which we will come back to"). Sources are named in
  the description and credited on screen. Synthetic narration is declared.
- **First 8 seconds: a scene, not a hook (P3).** 0:01-0:07 is "A card touches a reader in a café in Lisbon, and
  about a second later the reader says approved." True and well drawn, but it is the least surprising sentence in
  the film. The first number arrives at 0:14 and the surprising claim at 0:20-0:26. CRAFT §2 asks for the most
  surprising true thing inside 8 s. Frame 0 is a finished composition with a label, which is right. The ghost boxes
  (N1) fall in this stretch.
- **Titles (P2).**

| Option | Words | Characters | CRAFT §6 (6 words or fewer, about 30-50 characters) |
|---|---|---|---|
| The Company That Never Touches Your Money | **7** | 41 | **Fails the word rule** the sheet itself states. Also rests on F1. |
| Visa Never Holds Your Money | 5 | 27 | Words pass; 3 characters short. Rests on F1. |
| How Visa Keeps Half | 4 | 19 | Words pass; well short of 30; weakest tension, but every word is sourced. |

  A title inside the rules that does not depend on F1: "Visa Keeps Half of What It Earns" (7 words, no) or
  "Why Half of Visa's Revenue Is Profit" (7, no); "Visa Turns Half Its Revenue Into Profit" (7, no). Six-word
  options: "How Visa Turns Half Into Profit" (6 words, 31 characters); "Visa Sets a Fee It Never Collects"
  is 7. Recommended: **"How Visa Turns Half Into Profit"**, or title 2 if F1 checks out.
- Thumbnail text: "24¢ PER $100" (3 words) and "HALF IS PROFIT" (3 words) both pass and neither repeats a title,
  except that "HALF IS PROFIT" would repeat the recommended title; pair that title with "24¢ PER $100".
- Still missing per POST.md: thumbnail image and end card. An upload without a custom thumbnail falls back to a
  frame; frame 0 is acceptable for that.

| # | Where | Sev | What | Suggested fix |
|---|---|---|---|---|
| P1 | POST.md chapters | FIX (before upload) | All six chapter marks about 2 s early; 2:41 cuts the "24 cents" line. | 0:00, 0:26, 1:00, 1:31, 2:16, 2:43, 3:26. |
| P2 | POST.md titles | FIX (before upload) | Title 1 is 7 words; titles 2 and 3 are under 30 characters. | See above. |
| P3 | 0:00-0:08 | FIX (next film; needs a re-voice here) | Hook is scene-setting. | Open on the 0:20 line or on "$17 trillion". |
| P4 | POST.md | NICE | Thumbnail and end card not made. | Make the thumbnail before upload. |

**Platform gate: PASS WITH NOTES.** The film itself meets §1. The upload sheet does not yet meet §6.

---

## All issues, by severity

| # | Time | Sev | What | Fix |
|---|---|---|---|---|
| — | — | BLOCKER | None found in the file. Both v4 BLOCKERs are closed. | — |
| F1 | 0:20, 4:08, title | FIX, check before upload | "Never held any of the money" is not in FACTS.md and may be contradicted by the 10-K's settlement notes (unverified recollection). | Read the settlement notes; record; add a description sentence if needed. |
| P1 | POST.md | FIX before upload | Chapter times 2 s early. | Corrected list above. |
| P2 | POST.md | FIX before upload | Title 1 breaks the 6-word rule. | Pick a compliant title. |
| F6 | POST.md | FIX before upload | No source links. | Add three URLs. |
| N1 | 0:08.8-0:12.0 | FIX | Ghost boxes over the tag and the arc in the hook. | Zero opacity until 0:28. |
| N2 | 2:49-2:57 | FIX | "$16.0B to run" drawn as 50%. | Draw at 40%. |
| N3 | 2:35.2-2:36.8 | FIX | Black picture for about a second. | Overlap the outgoing bar and the incoming arc. |
| F2 | 3:30 | FIX | "for years" unverified. | Source the MDL's start year. |
| F3 | 1:18-1:31 | FIX | "The fee pays banks to issue the cards" unsourced on screen. | Source it or own it as a reading. |
| F4 | 1:07, 3:29 | FIX | Source line lacks "2011 (US)". | Add. |
| N4-N7 | see 2b | FIX | Near-empty four-parties opening; caption plate over grid and map; thumbnail arrivals; "$17 trillion" cut by the left edge. | See 2b. |
| P3 | 0:00-0:08 | FIX | Hook is a scene. | Next film. |
| N8-N16, F5, F7, P4 | see above | NICE | — | — |

**UPLOAD, after three edits to POST.md and one ten-minute check; no re-render is required.** Reasons: every number
matches the filings; the two interchange lines that stopped v4 are now sourced and worded within the source; v6's
three changes are all verified and nothing regressed against the v5 the owner approved; sound is on target; the film
shows an author and a non-template structure. Before pressing upload: correct the chapter times (P1), choose a
title that passes the 6-word rule (P2), add the source links (F6), and read the 10-K's settlement notes so the title
claim is either confirmed or qualified in the description (F1). If a v7 is rendered for any reason, fix N1, N2 and
N3 first, in that order; all three are also in v5.
