# ROTA: which channel gets each day's Short (B, Wed 28 Oct 2026 21:00 UK)

The owner on 28 Oct, 20:30 UK: "Continue, have all other channels going too and wherever u think best opportunity is
to gain views and climb to monetisation best do that, let's get goin". Before that, the same day: "Yes: the daily
scheduled runs can upload each Short (scheduled for 17:00) without asking me first."

The scheduled runs read this file. Change a line here to change what a run builds; the tasks stay as they are.

## Why the Curve gets the most slots (YouTube APIs, 28 Oct 20:35 UK)
| Channel | Lifetime views | Subs | Best video |
|---|---|---|---|
| The Curve | 42,984 | 36 | Microduck 17,753 in 2 days (83% viewed); Roadster upside down 15,466; all 8 "clip, explained" Shorts passed 800 |
| How They Profit | 183 | 0 | McDonald's Short 87 |
| Money Crimes | 116 | 0 | 33 |
| Curva Explica | 3 | 0 | 3 |
One Claude Pro account makes everything: one full Short is about 4-5% of the weekly allowance (resets Sat 21:00 UK),
so about 18 Shorts a week fit with a safety margin.

## Tasks (all on this Mac, Bypass mode; each skips itself when weekly usage is 92% or more)
| Task | When (UK) | Builds |
|---|---|---|
| `b-sun-short` | Sat 31 Oct 21:15, once | The Curve, publishes Sun 1 Nov 17:00 |
| `b-curve-daily` | every day 21:15, Nov-Dec | The Curve, publishes the next day 17:00 |
| `b-channels-rota` | every day 19:00, Nov-Dec | the line for today in the table below |
| `b-daily-check-0730` | every day 07:30, Nov-Dec | finishes any run from last night that stopped before its upload |

## The other channels: two test Shorts each in week 1, then the gate
| Build day (19:00 UK) | Channel | Job | Publishes |
|---|---|---|---|
| Sun 1 Nov | How They Profit | SETUP + HTP Short 1 (RUNBOOK_SHORT.md §9a) | Mon 2 Nov 17:00 |
| Mon 2 Nov | Money Crimes | SETUP + MC Short 1 (§9b) | Tue 3 Nov 17:00 |
| Tue 3 Nov | Curva Explica | Spanish version of Curve Short 7 Microduck (§9c) | Wed 4 Nov 17:00 |
| Wed 4 Nov | How They Profit | HTP Short 2 | Thu 5 Nov 17:00 |
| Thu 5 Nov | Money Crimes | MC Short 2 | Fri 6 Nov 17:00 |
| Fri 6 Nov | Curva Explica | Spanish version of Curve Short 1 Roadster upside down | Sat 7 Nov 17:00 |
| Sat 7 Nov | The Curve | a second Curve Short only if weekly usage is under 70%, publishing Sun 8 Nov 12:00; else nothing | Sun 8 Nov 12:00 |
| Sun 8 Nov on | (set by the gate below) | | |

## The gate (Sat 7 Nov run, or the Monday 09:00 weekly review, writes the next week's lines here)
- Views 72 h after publishing, from the YouTube Analytics API (GROWTH.md).
- A channel with a test Short over 1,000 views: 3 Shorts a week. 300-1,000: 2 a week. Both under 300: 1 a week, and
  its other slots become a second daily Curve Short (12:00 UK).
- The Curve: a second daily slot as soon as the weekly allowance allows it (more Curve Shorts = more shots at a
  100k+ hit, which is what moves subscribers).
