# Who changes your phone's clock? Facts for a dated Short (US clocks go back Sun 1 Nov 2026, 2 a.m.)

Checked Tue 27 Oct 2026, ~05:10 UK, by account C (web search extracts; pages not opened). Trend board row from 24 Oct
("US cut by Sat 31 Oct"). A permission-free Saturday option: all pictures are ours (diagrams, phone UI we draw).
Status: **V** = two or more independent sources agree. **U** = one source. **OUR MATHS** = labelled on screen.

## Sources
- **T1** RFC 6557 / BCP 175, "Procedures for Maintaining the Time Zone Database" (IETF, Feb 2012): https://www.rfc-editor.org/rfc/rfc6557
- **T2** IETF draft history, draft-lear-iana-timezone-database: https://datatracker.ietf.org/doc/draft-lear-iana-timezone-database/05/
- **T3** Android Open Source Project, "Time source priority": https://source.android.com/docs/core/connect/time-source · "Time zone rules": https://source.android.com/docs/core/permissions/timezone-rules
- **T4** NITZ (network identity and time zone), Wikipedia summary of the 3GPP feature: https://en.wikipedia.org/wiki/NITZ
- **T5** The Apple Wiki, TimeZoneUpdate asset (community source): https://theapplewiki.com/wiki/TimeZoneUpdate
- **T6** US end of daylight saving time, 1 Nov 2026: ABC13 https://abc13.com/story/daylight-saving-time-2026-ending-when-fall-back/19913454/ · Farmers' Almanac https://www.farmersalmanac.com/?p=440838
- **T7** Sunshine Protection Act (H.R. 139) in the House, July 2026: Galveston Daily News/Reuters https://www.galvnews.com/news_reuters/texas/when-does-daylight-saving-time-end-in-2026-could-it-become-permanent/article_2e0035c1-610c-5c18-bbf8-566a1e409b18.html

## 1. The date

| # | Fact | Source | Status |
|---|---|---|---|
| 1 | US daylight saving time ends **Sun 1 Nov 2026 at 2:00 a.m. local**: clocks go back to 1:00 a.m. (the earliest possible date under the "first Sunday in November" rule) | T6 | V |
| 2 | The UK and EU went back on Sun 25 Oct, so for one week the US-UK gap is an hour shorter than usual | radar 24 Oct; [K] | V |
| 3 | **The House passed the Sunshine Protection Act (H.R. 139) on 14 Jul 2026, 308-117**, to make daylight time permanent; it hasn't passed the Senate, so the change still happens | T7 | U (one report for the vote count: check congress.gov) |

## 2. Who actually changes the clock

| # | Fact | Source | Status |
|---|---|---|---|
| 10 | Your phone doesn't keep "local time": it gets the time from the network and works out local time from a **rulebook of every time zone's history and rules**, the tz database | T1, T3 | V |
| 11 | That database is kept by **volunteers on a mailing list**, and it's updated about **twenty times a year** (as countries change their rules) | T1 | V |
| 12 | Arthur David Olson maintained it from the start; it was hosted at the US National Institutes of Health from the early 1980s until it moved to IANA (run by ICANN) in 2011-12 | T1, T2 | V |
| 13 | Time itself comes from **NTP** (internet time servers) or **NITZ** (the mobile network, which can also send the time zone and the daylight-saving offset; every field is optional and support varies by network) | T3, T4 | V |
| 14 | Android 12 and later prefer NTP and fall back to NITZ; Android 11 and earlier did the reverse | T3 | V (Google's docs) |
| 15 | Android 10+ gets new time-zone rules as a "Time Zone Data" module downloaded separately from full system updates | T3 | V |
| 16 | Apple ships the same IANA database as a downloadable asset; a reboot may be needed if your zone changed (community source) | T5 | U |
| 17 | GPS time is not used for routine clock setting on phones | T4-area source | U |

## 3. OUR MATHS
| # | Sum | Result |
|---|---|---|
| 20 | About 20 releases a year (row 11) | **about one rule change every two to three weeks, somewhere in the world** |

## 4. The chain, for the diagram (rows in brackets)
1. A tower or a time server says what time it is in UTC (13).
2. Your phone looks up your zone in its copy of the volunteers' rulebook (10-12, 15-16).
3. The rulebook says "first Sunday in November, 2 a.m., subtract an hour" for most of the US (1).
4. If a country changes its rules with little notice, the volunteers publish a new rulebook and phones download it (11, 15).
5. Twist for the end: the House has already voted to stop the switch; the Senate hasn't, so Sunday's change still happens (3).

## 5. Hooks (≤ 3 s)
| # | Line 1 | Frame 0 |
|---|---|---|
| H1 | "On Sunday your phone will change its own clock, using a rulebook kept by volunteers." | A phone clock flipping 1:59 → 1:00 |
| H2 | "Congress already voted to stop changing the clocks, and yours still goes back on Sunday." | The House vote count beside the clock |

## 6. Do not claim
- That the Sunshine Protection Act is law, or a date it would take effect (row 3).
- That GPS sets your phone's clock (row 17).
- Apple's exact mechanism as Apple's own words (row 16 is a community source).
- The 2011 lawsuit over the database (not checked this session).
- That every state changes: Hawaii and most of Arizona don't observe daylight saving time [K]: say "most of the US".
