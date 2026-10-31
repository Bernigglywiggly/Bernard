# Starship Flight 15: facts for the pre-built Short "How SpaceX Will Catch a Falling Starship"

Checked Tue 27 Oct 2026, ~05:00 UK, by account C (web search extracts; pages not opened). For A's pre-build (TEAM queue).
**Re-check the date, the mission page and the catch plan the day it flies:** this file is written before the launch.
Status: **V** = two or more independent outlets agree. **U** = one outlet. **OUR MATHS** = labelled on screen.

## 0. Re-check Sat 31 Oct 2026, 08:50 UK (account A, for the Short 14 pre-build)
- **Date: still none from SpaceX.** spacex.com/launches lists no Flight 15 page (fetched 08:50 UK). Trackers and Wikipedia
  ("SpaceX Starship integrated flight tests", read 08:52 UK) give **NET 8 Nov 2026**, Pad 2 (OLP-2), Booster 22 + Ship 42,
  booster catch + first ship catch attempt. No FAA licence update found. The Short says only "expected in November" (row 13 stays U).
- **Booster catches = three, re-checked (row 3 → V):** Flight 5 (13 Oct 2024), Flight 7 (16 Jan 2025), Flight 8 (6 Mar 2025);
  Flight 6 aborted to the sea; Flights 9-14 no catch (Wikipedia flight table; Space.com on Flight 8; S1). A June 2026 "double catch"
  page found in search is an unsourced aggregator: ignored.
- **No ship caught yet (row 4): V** (Wikipedia table, S1, S3).
- **Footage:** SpaceX's own "Starship's Fifth Flight Test" (youtube.com/watch?v=hI9HQfCAw64), 128-150 s = the first tower catch.
  Copy + SOURCES.txt in `lab/curve_v2/footage/spacex_flight5/`. Credit "SPACEX VIDEO · SLOWED"; each shot under 5 s of source.
- **Launch-day swap:** Short 14's date phrase lives in `DATE_PHRASE` at the top of `lab/curve_v2/shorts/short14.py` and the
  on-screen stamp in `DATE_STAMP` in `CurveV2Short14.tsx`.

## Sources
- **S1** Space.com, Flight 14 live updates and wrap-up (28 Sep 2026): https://www.space.com/space-exploration/launches-spacecraft/spacex-starship-megarocket-flight-14-orbital-launch-success
- **S2** Wikipedia, Starship flight 14: https://en.wikipedia.org/wiki/Starship_flight_14
- **S3** Gizmodo, "SpaceX Is Finally Going for the Starship Double Catch": https://gizmodo.com/spacex-is-finally-going-for-the-starship-double-catch-2000828826 · Technology.org (23 Oct): https://www.technology.org/2026/10/23/spacex-starship-flight-15-ship-booster-tower-catch-november/
- **S4** KeepTrack Starship launch tracker: https://keeptrack.space/deep-dive/starship-launch-tracker · Space Launch Schedule: https://www.spacelaunchschedule.com/launch/starship-flight-15/
- **S5** SpaceDaily on SpaceX's V3 description (124.4 m, ~5,533 t): https://spacedaily.com/?p=1085988 · BGR, why catch instead of legs: https://www.bgr.com/2279871/why-spacex-plans-to-catch-starship-instead-of-landing-legs/
- **S6** First booster catch, 13 Oct 2024 (Flight 5): https://www.inverse.com/heres-how-spacexs-chopsticks-caught-a-rocket · https://space.com/spacex-starship-chopsticks-animation

## 1. Where things stand

| # | Fact | Source | Status |
|---|---|---|---|
| 1 | Flight 14 (28 Sep 2026, Booster 21 + Ship 41): Starship's **first flight to orbit**; deployed working Starlink V3 satellites; the booster made a controlled splashdown in the Gulf of Mexico (not caught); the ship splashed down intact in the northern Pacific after about 3 h 8 min, cut short from a planned ~9 h 50 min | S1, S2, S4 | V |
| 2 | One engine shut down early on Flight 14; sources disagree on which stage | S1, S2 | U (which stage) |
| 3 | Boosters have been caught by the tower ("chopsticks") on **three** test flights; the first on 13 Oct 2024 (Flight 5), first try | S1, S6 | V |
| 4 | **No ship has ever been caught** | S1, S3 | V |

## 2. The Flight 15 plan

| # | Fact | Source | Status |
|---|---|---|---|
| 10 | Catch **both** stages with the tower: the booster and, for the first time, the ship. Announced by Musk on SpaceX's earnings call, 20 Oct | S3 | V |
| 11 | Musk's odds, as quoted: "Success is not guaranteed on these first flights, but I'd say it's more likely than not that this succeeds next flight" (earlier he said "at least 50 or 60 percent") | S3, S4 | V (quote via extracts: copy from the call recording) |
| 12 | Hardware: Booster 22 + Ship 42, the fourth V3 pair, from Pad 2; Ship 42 already did multi-day catch-related tests between the Pad 2 arms (NASASpaceflight) | S4, S3 | V |
| 13 | Target: no earlier than ~8 Nov (reported); Musk on 10 Oct: "four to six weeks". No SpaceX mission page yet; no FAA licence change published as of 11 Oct | S4, radar 27 Oct | U (date) |
| 14 | The licence must cover a return to the launch site and tower catches for both stages; the ship's return path crosses land (northern Mexico), a hurdle | S3 | U |

## 3. How a ship catch works (for the Blender shot)

| # | Fact | Source | Status |
|---|---|---|---|
| 20 | SpaceX's simulation: the ship falls belly-first, steering with its flaps; near the tower it fires its engines briefly, swings upright and drops between the arms, which close around it and meet hardware on its sides | S3 | V (as shown on the call) |
| 21 | The full V3 stack stands **124.4 m** and weighs about **5,533 t** at launch (SpaceX's V3 description, as reported) | S5 | U |
| 22 | Why catch at all: no landing legs means less mass and cost, and the booster can go straight back on the launch mount; Musk's goal is a reflight "in under an hour" | S5 | V (Musk's words via two outlets) |
| 23 | Belly-flop speeds and the timing of the landing burn: **not published**. Don't give numbers | our check | V (absence) |

## 4. Footage and rights
- SpaceX's own launch, catch and simulation footage (its X and YouTube): credited, ≤5 s per shot, under our commentary.
- NASASpaceflight and other streamers own their streams: ask first (radar 25 Oct Brief B).
- Our Blender: tower arms, ship flip and catch, labelled "SIMULATION, DRAWN FOR THIS VIDEO".

## 5. Hooks (line 1 ≤ 3 s)
| # | Line 1 | Frame 0 |
|---|---|---|
| H1 | "SpaceX is about to catch the top half of its rocket, which nobody has ever done." | Our Blender arms closing on the ship |
| H2 | "This tower has caught a falling rocket three times; next it tries the one coming back from orbit." | A real booster catch (SpaceX), then the ship |

## 6. Do not claim
- A launch date before SpaceX posts one (row 13).
- That a ship catch has happened, until it has; after the flight, re-write this file from SpaceX's own account.
- Speeds, forces or timings for the flip and catch (row 23).
- Which stage lost an engine on Flight 14 (row 2).
- A catch count above three without a fresh check (row 3).
