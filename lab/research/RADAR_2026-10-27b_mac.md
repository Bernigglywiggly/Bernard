# Radar addendum: view counts, Tue 27 Oct 2026, 17:50 UK (Mac; adds to `RADAR_2026-10-27b.md`)

**Read `RADAR_2026-10-27b.md` (cloud C, 17:45) first: it has the news (Apple's M6 MacBook Pro and iMac announced today, touch model
still Wed 28) and the permission-free top 3.** This file adds only what the cloud can't read: live view counts and outlier ratios.
The Mac's scheduled 17:00 run failed on a usage limit at 17:00:11; this is a shorter manual run. Data: `lab/tools/radar_outliers.py`
over 12 candidate queries (window = week, sorted by views, top 6 per query, 5,000+ views), read 17:45-17:50 UK; ratio = views ÷
that channel's median (≥3 outlier, ≥10 breakout). TSV in the session scratchpad, not the repo.

## 1. What the numbers say about this week's plan

| Day | Planned video | Demand this week (best video on the angle) | Verdict |
|---|---|---|---|
| Tue 27 | Short 8 iPhone Duo crack | JerryRigEverything "iPhone Duo Durability: Destroyed" **12.70M** (11.77M on 26 Oct: about +0.9M a day); MKBHD review 12.57M; Mrwhosetheboss 10.18M | **Still hot. Ship Short 8 as soon as the critic passes it** |
| Wed 28 | Motorcycle on water | Nothing with 5,000+ views this week on "motorcycle on water record"; the ride's biggest uploads are news re-posts (Kompas 234k, row 80b of the facts) | **Weakest of the week**, and it needs his footage call. Alignment check (13:04) also says drop it |
| Thu 29 | Touchscreen MacBook (Apple event Wed 28, 10:00 PT = 17:00 UK; press releases and films, not a keynote) | Pre-event videos ~400-450k at about 1× their channels' medians | Normal demand that will spike after Apple's films land. Keep; fill §5 Wed 17:20 |
| Sat 31 | Crosswind 737, or SpaceX money, or phone clock | **Crosswind:** Airport Action's "Emirates Airbus A380 vs STORM AUSTEN" 632k = **105×** its median (breakout). **SpaceX money:** "Elon Musk: The UNTHINKABLE's About to Happen to SpaceX!" 1.48M = 18×. **Clocks:** "What Life Was Like When Britain Skipped the Clocks Going Back (1968)" 85.8k = **242×** | All three have demand. Crosswind is the biggest breakout but needs Airport Action's yes; SpaceX money needs nobody's (script `short10.py` ready) |
| ~7-21 Nov | Starship Flight 15 ship catch (pre-build) | VideoFromSpace "Elon Musk: SpaceX Will Attempt to Catch BOTH Starship & Booster" 563k = 20× | Pre-build holds. Still no date (Musk 10 Oct: "four to six weeks"; NET 8 Nov per one tracker, optimistic) |

**Swap to consider (his call):** Wed's slot goes to the SpaceX money Short (script ready, SEC-checked, permission-free,
1.48M outlier on the angle) and Sat takes crosswind if Airport Action says yes, else the phone-clock Short for the US change
on Sun 1 Nov (the 242× clocks breakout is UK-side history, but it shows the clocks angle travels).

## 2. Also checked
- Anthropic's draft IPO filing: "Anthropic Just Filed Its IPO. The Numbers Are a Horror Show" 443k (1.5×); Bloomberg's
  report 67.8k (9.2×). Moderate; numbers-led; no clip. No change.
- SEMA 2026 (3-6 Nov): big build channels at ~400k (below their medians). Wait for the one build that breaks out.
- Tesla robotaxi: under 90k, no outlier. Drop.
- A general "viral today" news search found nothing new in our five verticals.

## Sources
- JerryRigEverything https://youtu.be/5laDGy4INB0 · MKBHD https://youtu.be/ESABTN4VtrA · Mrwhosetheboss https://youtu.be/Xrxy_W78SKk
- Airport Action https://youtu.be/WO6UHkyWtmo · David Carbutt https://youtu.be/PZI1zEvKhYA · Lost Britain https://youtu.be/YY5qL2eOlqw
- VideoFromSpace https://youtu.be/di6_DcLjeWE · House of El https://youtu.be/R4dUq9yG2L8 · Bloomberg https://youtu.be/5nuuobUmoCE
- Apple event timing (10:00 PT, Los Angeles; format reported as press releases plus films): Macworld https://macworld.com/article/3264015/apple-teases-pro-and-tell-event-on-october-28.html · MobileSyrup https://mobilesyrup.com/2026/10/19/apple-pro-and-tell-event-october-28
- Starship Flight 15 timing: Space Launch Schedule https://www.spacelaunchschedule.com/news/starship-flight-15-launch-date-how-to-watch/ · NewSpace Economy https://newspaceeconomy.ca/2026/10/11/starship-flight-15-will-attempt-to-recover-its-upper-stage-spacecraft-in-november-launch/
