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

## Tasks (all on this Mac; each skips itself when weekly usage is 92% or more; saved in the default permission mode on 28 Oct: set each to Bypass in the app so they never stop to ask)
| Task | When (UK) | Builds |
|---|---|---|
| `b-sun-short` | Sat 31 Oct 21:15, once | The Curve, publishes Sun 1 Nov 17:00 |
| `b-curve-daily` | every day 21:15, Nov-Dec | The Curve, publishes the next day 17:00 |
| `b-channels-rota` | every day 19:00, Nov-Dec | the line for today in the table below |
| `b-daily-check-0730` | every day 07:30, Nov-Dec | finishes any run from last night that stopped before its upload |

## Week 1 (revised 28 Oct 20:55 after the alignment check, `lab/research/ALIGNMENT_2026-10-28.md`: REDIRECT)
The Curve gets most slots (A slot 17:00 every day from `b-curve-daily`, B slot 12:00 on rota days). How They Profit and
Curva Explica get real tests. Money Crimes gets only its finished backlog (best Short 33 views, hard footage,
defamation risk): no new Money Crimes build until How They Profit or Curva passes the gate.
| Build (UK) | Run | Channel | Job | Publishes (UK) |
|---|---|---|---|---|
| Sat 31 Oct 21:15 | b-sun-short | The Curve | A slot (RUNBOOK_SHORT.md §8b) | Sun 1 Nov 17:00 |
| Sun 1 Nov 19:00 | rota | How They Profit | SETUP + HTP test 1 (§9a): a clip of a business doing something that looks like it loses money, then the money flow | Mon 2 Nov 17:00 |
| Mon 2 Nov 07:30 | check | Money Crimes + How They Profit | BACKLOG PREP (below) | the drip dates below |
| Mon 2 Nov 19:00 | rota | The Curve | B slot: Microduck sequel, a new question about the same robot (§8b) | Tue 3 Nov 12:00 |
| Tue 3 Nov 19:00 | rota | Curva Explica | SETUP + Spanish Microduck; also Spanish Roadster upside down if weekly usage is under 75% (§9c) | Wed 4 Nov 17:00 (+ Thu 5 Nov 17:00) |
| Wed 4 Nov 19:00 | rota | The Curve | B slot | Thu 5 Nov 12:00 |
| Thu 5 Nov 19:00 | rota | How They Profit | HTP test 2 | Fri 6 Nov 17:00 |
| Fri 6 Nov 19:00 | rota | Curva Explica | Spanish iPhone Duo crack (and Roadster if Tuesday skipped it) | Sat 7 Nov 17:00 (+ Sun 8 Nov 17:00) |
| Sat 7 Nov 19:00 | rota | The Curve | B slot, only if weekly usage is under 75% (the allowance resets at 21:00) | Sun 8 Nov 12:00 |
| Sun 8 Nov 19:00 | rota | all | GATE (below) + a fresh alignment check (Sonnet agent) + week 2 rows | - |

**BACKLOG PREP (one morning job):** recover the 5 unuploaded Ponzi Shorts (page https://claude.ai/artifact/3dQC4krr7X2cssm2o6CcJK)
and the 12 old-look How They Profit Shorts (pages https://claude.ai/artifact/PwxaSffr73rhXBtRf7qdNH parts 4-5,
https://claude.ai/artifact/PktR2P3q7bUJ9kenGWn4cX, https://claude.ai/artifact/HbiwF8JbBuYzAcKVowLLEV) with the Artifact tool
(list scope "files", then read each path) into `lab/backlog/<channel>/`. Skip any already in `channel/uploads.done.json`.
One critic skim of the whole batch (film-critic skill, one NEW Sonnet subagent, contact sheets + loudness): drop anything
broken. Upload, private with publishAt, the 5 Ponzi Shorts on Money Crimes (Tue 3, Thu 5, Sat 7, Mon 9, Wed 11 Nov, 17:00)
and the best 3 HTP Shorts on How They Profit (Wed 4, Sun 8, Tue 10 Nov, 17:00), using the titles and descriptions in
`channel/uploads.json`. The 2 old HTP films (Costco, Amazon) are long films: they need his yes, so they wait.
If the files can't be fetched, skip the job: it is worth ~700 views in total; its use is old look vs new look.

## The gate (read 72 h after each test Short; first read Sun 8 Nov)
| Result | Rule | Then |
|---|---|---|
| PASS | one test 1,000+ views, or both 500+ | How They Profit 4 a week, Curva 5 a week; Money Crimes gets 2 new tests |
| HOLD | best 300-999 and 70%+ viewed | same slots, 2 more tests |
| FAIL | both under 300 | 1 a week or park; its slots go to Curve B slots |
- The Curve: 12 Shorts in week 1, 14 in week 2 (A every day + B slots), as the weekly allowance allows.
- Cross-posting every Curve Short to TikTok, Reels and Facebook Reels needs his accounts connected (TEAM.md §5).
