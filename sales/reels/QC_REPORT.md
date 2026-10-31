# Reels QC report

Checked 6 Oct 2026, 00:33-00:40. Independent review of the rendered video, not the code.

**Checked: 35 Reels** (16 Stone, 19 Newcastle-under-Lyme). **SEND 31 / FIX 4 / DON'T SEND 0.**

Not checked: the Tamworth Reels (tam02 onwards) and anything rendered after about 00:38. They were still being written when the review closed.

Method: four frames per Reel (0.1, 1.6, 4.3, 7.5 s) viewed on contact sheets at 540 px per frame, plus full-resolution crops of the final frame on three Reels. ffprobe, black-frame detection and silence detection were run on the first 27 Reels (all Stone, new01-new14) and ffprobe on all 35. Name, street, town and inspection month were compared by eye against `prospects_routed.json`.

## Per-Reel verdicts

| File | Verdict | Issue |
|---|---|---|
| sto01_crown_of_india | SEND | None. 40 High Street, May 2026. |
| sto02_arcadia_tea_shop | SEND | None. "Unit 4 and 5 / High Street Arcade" reads well. |
| sto03_bear_coffee_company_ltd | SEND | "Ltd" is stripped. Shows "BEAR COFFEE COMPANY", which is still the registered name rather than what is probably on the shopfront; check the sign when walking in. |
| sto07_little_seeds_bar_kitchen | SEND | None. |
| sto08_the_ovilash_restaurant | FIX | Shows "INSPECTED DEC 2024", 22 months old. Correct per the JSON, but a stale date on a promo. Re-check the live register, then hide the date. |
| sto10_stonefield_fish_bar | SEND | None. |
| sto11_proven_pizzeria | SEND | None. Jul 2025. |
| sto12_the_secret_tea_room | SEND | None. "Unit 2 / Adies Alley". |
| sto13_pasta_di_piazza | SEND | None. |
| sto16_heaven_restaurant_bar_grill | SEND | None. Three lines, sensible breaks. |
| sto17_stone_kebab_house | SEND | None. |
| sto18_valleys_fast_food | SEND | None. Next door to Cavalli, see "templated" below. |
| sto21_cavalli | SEND | None. Pen circle sits about 15 px from the ticket edge in the final frame; inside, but tight. |
| sto22_piccolo_s_pizza_kebab_land | SEND | None. Apostrophe renders correctly. |
| sto23_walton_fish_bar | SEND | None. Business name correctly dropped from the address; date matches the JSON. |
| sto25_the_roll_in_stone | SEND | None. "Unit 24A Whitebridge Estate / Whitebridge Lane". |
| new01_pizzarama | SEND | None. Pen circle tight to the ticket edge, as Cavalli. |
| new02_fresco_cafe_eatery | SEND | Mar 2025 inspection, 19 months old. |
| new03_pizza_bar | SEND | None. Jul 2025. |
| new04_mado_cafe | SEND | Mar 2025 inspection, 19 months old. |
| new06_the_midway_cafe | SEND | None. "12 The Midway" correct. |
| new10_shaws | SEND | Mar 2025 inspection. Stamp is the most worn of the set ("HYGIENE" partly faded) but still reads as a 5. |
| new11_the_foyer | SEND | None. |
| new12_nel | FIX | Shows "INSPECTED OCT 2024", two years old. Same fix as Ovilash. |
| new13_cuisine_cart | SEND | Feb 2025 inspection, 20 months old. |
| new14_cheesious_pizza_peri_peri_house | FIX | Bad line break: "CHEESIOUS / PIZZA/PERI / PERI HOUSE" splits "Peri Peri" and reads as "Pizza/Peri". Should be "CHEESIOUS PIZZA / PERI PERI HOUSE". The JSON name has no spaces round the slash, so the two-name rule in `fit_name` never fires. |
| new15_dancing_octopus | SEND | None. Aug 2026, the freshest of the set. |
| new16_mo_s_kitchen | SEND | None. Apostrophe renders correctly. |
| new17_tasty_wok | SEND | Mar 2025 inspection, 19 months old. |
| new19_castle_oatcakes | SEND | None. Business name correctly dropped from the address. |
| new22_newcastle_kebab_house | SEND | None. |
| new25_the_one | SEND | None. |
| new28_favourite_chinese_takeaway | SEND | None. |
| new30_golden_wok | SEND | Feb 2025 inspection, 20 months old. |
| new31_chilli_jacks | FIX | Shows "INSPECTED NOV 2024", 23 months old. Same fix as Ovilash. |

## What was checked and what it showed

**1. Shop name.** All 35 match the JSON, are fully visible at frame 0 and stay inside the ticket. Line breaks are sensible except Cheesious. No "Ltd" appears on screen.

**2. "Find us" frame.** Street and town are correct on all 35. No business name is repeated as the street and "Staffordshire" never appears. Nothing is cut off.
- The postcode is shown on every Reel, small, after the town ("STONE  ST15 8AU"). It is tidy, but the brief said no postcode clutter, so this is a decision for you. The generator's `split_address` docstring includes it by design.

**3. Stamp.** Reads clearly as a 5 on all 35, and the inspection month and year match `fsaDate` on every one.
- It does not resemble the official sticker: it is a round green ink stamp with ring text, not the black-and-green rectangle with the 0-5 row.
- It does use the scheme's wording ("FOOD HYGIENE RATING", "VERY GOOD"), and the footer credits the Food Standards Agency and ratings.food.gov.uk. I see low risk of confusion.
- The month is printed on the line above the stamp ("INSPECTED MAY 2026"), not inside it.

**4. Rendering faults.** None found.
- All 35 are 1080x1920, 30 fps, 8.00 s, 240 frames, H.264 with an AAC audio stream.
- No black frames and no silent stretch over 1 s on the 27 scanned.
- No overlapping text and nothing touching the frame edge.
- The paper renders cool blue-white, not warm. It reads as a fridge light more than a heat lamp; cosmetic.
- At 1.6 s the camera has moved down and the top line of a two- or three-line name is cropped. That is the camera move, and the full name returns in the pull-back.
- The FSA source line in the final frame is very small on a phone. It is fine as attribution.

**Loudness (3 Reels)**

| File | Integrated | True peak |
|---|---|---|
| sto01_crown_of_india | -15.8 LUFS | -2.9 dBFS |
| sto22_piccolo_s_pizza_kebab_land | -16.0 LUFS | -3.6 dBFS |
| new02_fresco_cafe_eatery | -15.7 LUFS | -4.2 dBFS |

Consistent and no clipping. I measured levels only; I cannot hear whether the sound is pleasant.

**5. Would an owner be embarrassed or annoyed? Would it look good on Instagram?**
- Nothing here would embarrass or annoy an owner. The facts are right, the type is clean and it looks deliberate.
- It looks templated, because it is. Every Reel is identical apart from three text fields, and the stamp, pin and pen circle land in the same places.
- That matters most where neighbours both get one: Radford Street (sto07, sto08), Lichfield Street (sto18, sto21), Merrial Street (new02, new03), Liverpool Road (new13, new14), Pool Dam (new15, new16), and five on George Street (new22, new25, new28, new30, new31). If two of them post, the template is obvious.
- There is no food, no shopfront and no colour of the shop's own. It works as a one-off "we got a 5" post. It is not a general promo, and it fits takeaways better than the sit-down restaurants (Cavalli, Pasta Di Piazza, Little Seeds).

## Overall verdict

The batch is technically clean: 31 of 35 can go as they are. Fix the Cheesious line break before that one is shown. For the three 2024 inspections, re-check the rating on the live register and hide the date line when it is older than about 18 months. Two decisions are yours: whether the postcode stays, and whether to vary the template (ticket colour, stamp position or header line) so neighbouring shops do not receive visibly identical videos. Tamworth still needs the same check.

Contact sheet: `/Users/daestigwood/Bernard/sales/reels/build/qc_sheet.jpg` (Crown Of India, Little Seeds, Cheesious, The Roll In Stone; frames at 0.1, 1.6, 4.3, 7.5 s).

## Pass 2 (Tamworth + corrected)

Checked 6 Oct 2026, 00:48-00:52. **27 Reels: SEND 16 / FIX 11 / DON'T SEND 0.**

**Headline: 11 of the 12 "corrected" Reels have not been re-rendered.** Only `sto08_the_ovilash_restaurant.mp4` carries the fix. The other 11 files on disk are still the first renders (written 00:31-00:41, before `make_reels.py` was last saved at 00:40:50) and show exactly what Pass 1 saw. The only render after the fix ran 00:42:58-00:47:32 and rewrote the 16 Stone files; no Newcastle or Tamworth file was touched and no render was running at 00:49.

| Fix | In the output? | Evidence |
|---|---|---|
| (2) Old date replaced by "THE HIGHEST RATING THERE IS" | Confirmed on 1 of 11 | Ovilash only. Reads cleanly at 1.6, 4.3 and 7.5 s, same size and position as the date line, no overflow. The other 10 still show their 2024 / early-2025 month. |
| (1) "/" names split as two names | Not confirmed on Cheesious | Cheesious still reads "CHEESIOUS / PIZZA/PERI / PERI HOUSE". The two-name layout does work where the JSON has spaces round the slash: Tamworth Spice / Kiko Sushi renders as "TAMWORTH SPICE /" then "KIKO SUSHI". |

Method: frames at 0.1, 1.6, 4.3 and 7.5 s on contact sheets at 400 px per frame (all 27 viewed), full-resolution crops of the final frame on three, ffprobe on all 27, black-frame and silence detection on the 17 Tamworth files and Ovilash. Compared by eye against `prospects_routed.json`.

### Corrected set (12)

| File | Verdict | Issue |
|---|---|---|
| sto08_the_ovilash_restaurant | SEND | Fixed. Shows "THE HIGHEST RATING THERE IS", no date. It sits directly under "TOP RATING · VERY GOOD", so the top rating is said twice in two lines; cosmetic. |
| new02_fresco_cafe_eatery | FIX | Not re-rendered. Still "INSPECTED MAR 2025" (19 months). |
| new04_mado_cafe | FIX | Not re-rendered. Still "INSPECTED MAR 2025" (19 months). |
| new10_shaws | FIX | Not re-rendered. Still "INSPECTED MAR 2025" (19 months). |
| new12_nel | FIX | Not re-rendered. Still "INSPECTED OCT 2024" (24 months). |
| new13_cuisine_cart | FIX | Not re-rendered. Still "INSPECTED FEB 2025" (20 months). |
| new14_cheesious_pizza_peri_peri_house | FIX | Not re-rendered. Still "CHEESIOUS / PIZZA/PERI / PERI HOUSE". Date (Sep 2025) is fine. |
| new17_tasty_wok | FIX | Not re-rendered. Still "INSPECTED MAR 2025" (19 months). |
| new30_golden_wok | FIX | Not re-rendered. Still "INSPECTED FEB 2025" (20 months). |
| new31_chilli_jacks | FIX | Not re-rendered. Still "INSPECTED NOV 2024" (23 months). |
| tam15_pizza_boss | FIX | Not re-rendered. Still "INSPECTED MAR 2025" (19 months). Name and "36 Aldergate" are correct. |
| tam23_eat_well | FIX | Not re-rendered. Still "INSPECTED MAY 2024", 29 months old, the oldest date in the whole batch. Name and "156 Kettlebrook Road / Kettlebrook · Tamworth" are correct. |

Apart from the date line or line break, all 11 are otherwise clean (name, address, stamp, render), so a re-render is the only work needed.

### Tamworth (the other 15)

| File | Verdict | Issue |
|---|---|---|
| tam02_brew | SEND | None. "Unit 7 Town Hall Place / Market Street". Feb 2026. |
| tam04_phat_bites | SEND | None. "64 Church Street" (JSON capitals normalised). |
| tam06_china_aroma | SEND | None. Nov 2025. |
| tam07_tamworth_spice_kiko_sushi | SEND | Two-name split works. Name type is much smaller than on every other ticket, so it looks slightly underweight. May 2025 is 17 months old and crosses the 18-month line in December; send soon or re-render then. |
| tam09_jeffrey_s_fine_sandwiches | SEND | None. Apostrophe renders correctly. |
| tam13_swallow_cantonese_take_away | SEND | None. Business name correctly dropped from the address ("39A Aldergate"). Next door to Papudom 4U. |
| tam14_papudom_4u | SEND | None. |
| tam16_steves_fish_bar | SEND | None. "Steves" has no apostrophe, as in the JSON. |
| tam17_rayu_pan_asian | SEND | None. Oct 2025. |
| tam18_shake_take_tamworth | SEND | None. "&" kept, sensible breaks. |
| tam19_mr_chips | SEND | None. Full stop kept in "MR." |
| tam22_between_the_buns | SEND | None. Jul 2026. |
| tam24_the_tamworth_tandoor | SEND | None. Spelt "Tandoor" as in the JSON; check the shop sign in case it is "Tandoori". |
| tam26_2_gates_grill | SEND | None. "Unit 2 St Catherine's Court / 104 Tamworth Road / Two Gates · Tamworth" all fits. |
| tam99_fu_house_chinese_takeaway | SEND | None. Three lines. Jul 2026. |

### What was checked and what it showed (27 files)

- **Name.** All 27 match the JSON and are fully visible at frame 0 and in the final frame. No clipping at the ticket edge. Only fault: the Cheesious line break.
- **"Find us".** Street and town correct on all 27. No business name used as the street (Swallow handled correctly), "Staffordshire" never shown, nothing cut off. District names (Kettlebrook, Two Gates) appear before the town, which is right for those shops. Postcode still shown on every Reel.
- **Stamp.** Reads as a 5 on all 27. Wear varies; Eat Well and Ovilash are the most worn and still read clearly.
- **Rendering.** All 27 are 1080x1920, 30 fps, 8.00 s, 240 frames, H.264 + AAC. No black frames and no silence over 1 s on the 18 scanned. No overlapping text, nothing touching the frame edge. The pen circle round "5/5" sits tight to the ticket edge on Tamworth Spice, as on Cavalli; inside, not clipped.
- **Neighbours getting the same template.** Church Street (tam04, tam06, tam07), Aldergate (tam13, tam14, tam15), Lower Gungate (tam16, tam17).

### Verdict

Tamworth is clean: 15 can go now. The corrected set is not done: re-run the render for the 9 Newcastle IDs, Pizza Boss, Eat Well and Cheesious, then re-check those 11 files. Cheesious needs the slash rule to fire on a name with no spaces round the "/" ("PIZZA/PERI"); if it still breaks the same way after a re-render, the code fix did not cover that case. Until then, hold all 11; the four that most need holding are Eat Well (May 2024), NEL (Oct 2024), Chilli Jacks (Nov 2024) and Cheesious.

Contact sheets: `/private/tmp/qc2/sheet_01.jpg` to `sheet_14.jpg` (01-05 corrected set, 06-14 Tamworth); full-resolution crops in `/private/tmp/qc2/full.jpg`.
