# TEAM: five Claude accounts, one repo, one Mac (written Sun 25 Oct 2026, 17:50 UK)

Every account reads this after `START_NEW_ACCOUNT.md`. It is the lane map, the file ownership, the queue between lanes
and the sync rules. Shared memory is these files: accounts share nothing else.

## 1. The lanes

| Acct | Lane | Owns (only edits these) | Heavy CPU | Output and cadence |
|---|---|---|---|---|
| **A** | **The Curve: Shorts** | `lab/curve_v2/shorts/**`, Shorts footage folders it creates, `lab/motion/src/curve_v2/CurveV2Short*.tsx` + `voS*Captions.ts` + `s*Tracks.ts`, `lab/motion/src/curve_v2/kit/**`, `lab/motion/public/shorts/**`, Shorts entries in `channel/uploads_curve.json` | yes | 3-5 trend Shorts a week, each within ~48 h of its event. Holds the voice (ElevenLabs) and YouTube upload (Zapier) connectors |
| **B** | **The Curve: long-form + strategy** | `lab/curve_v2/film_*/**`, `lab/curve_v2/trials/**`, `lab/motion/src/curve_v2/film/**`, `lab/motion/public/film/**`, `lab/research/ALIGNMENT_*.md`, long-form entries in `channel/uploads_curve.json`, the pitch deck | yes | 1 long film a week (2-3 in the backlog, no more); the plan and the alignment checks |
| **C** | **Trend desk, facts, QA critic** | `lab/research/**` except `ALIGNMENT_*`, every `*/critic*/` report, the "Learned" lines in `CRAFT.md` | no (web only) | Radar twice a day (09:00, 17:00 UK); a facts file before any script; the independent critic on every A, B and E render before it goes to him; 48 h and 7 d analytics lessons into CRAFT |
| **D** | **Money now (off YouTube)** | `sales/**`, `products/**`, `offers/**` | light | The fastest cash: the "videos for businesses" offer, sample reels, outreach drafts, affiliate applications ready to submit, listings ready to post. Every send, post or sign-up is his |
| **E** | **Channels 2 and 3** | `channel/<new channel>/**`, `channel/uploads_<channel>.json`, `lab/ch2/**`, `lab/maps/**`, any new `lab/<channel>/**`, `lab/motion/src/<channel>/**`, `lab/motion/public/<channel>/**` | yes | The niche pick with numbers, then style test snippets for his yes, then a 2-3 film backlog per channel, each with its own look, narrator and music |

## 2. Shared files: small, exact edits only, then commit at once
- `HANDOFF.md`: edit only your own block at the top (`ACCOUNT X ...`). Then `bash lab/tools/sync_handoff.sh`.
- `TEAM.md`: add or tick lines in the Queue (section 4). Change the lane map only when he says so.
- `channel/uploads_curve.json`: your own entries only; load and dump with `json.dumps(m, indent=1, ensure_ascii=False)` so nothing else moves.
- `lab/motion/src/Root.tsx`: add or remove only your own lines.
- `CRAFT.md`: anyone appends under "Learned on our films"; C curates. `~/youtube/DECISIONS.md`: append only.
- Need a change in another lane's files? Queue it for that lane. Don't make it yourself.

## 3. The loop (every account, every working block)
1. **Start:** read `START_NEW_ACCOUNT.md`, this file, your `HANDOFF.md` block and `CRAFT.md`. Run `git pull`.
2. **Claim:** write `ACCOUNT X working on: <task> (since HH:MM)` at the top of `HANDOFF.md`, commit, push.
3. **Queue first:** do the open `FOR X` lines in section 4 before your own backlog, oldest first.
4. **Heavy jobs** (Remotion full renders, Blender animations, RIFE): `bash lab/tools/heavy.sh <command>`, run in the background. One at a time on this Mac. Waiting order: A's trend Shorts, then B, then E, then D.
5. **Quality:** the builder never grades its own work. Queue `FOR C: critic <file>`. C writes `round<N>.md` next to the render and queues the fixes back.
6. **His gates:** uploads, posts, sends, purchases, sign-ups, account connections, and the first video in any new style. Ask him on a line that starts with 5 random emojis, one ask per line. One account's yes never covers another account's item.
7. **Commit:** small, your own paths only (`git add <paths>`, never `-A`), no model names in messages, push. If `.git/index.lock` exists, another account is committing: wait and retry.
8. **Before a limit, a long job or stopping:** update your `HANDOFF.md` block, `bash lab/tools/sync_handoff.sh`, commit, push. Then say in chat that it is saved.

## 4. Queue (add `- [ ] FOR <X> (from <Y>, <date time>): <what> → <files>`; tick when done)
- [x] (done by B 26 Oct: round 2 = ONE MORE PASS, its one must-fix fixed and checked in the v3 frames; film LIVE https://youtu.be/MRRLbIveEJc) FOR C (from B, 25 Oct 17:50): critic round 2 on `lab/curve_v2/film_roadster/out/FILM_ROADSTER_v2.mp4` with the film-critic skill. Measurements are already in `out/critic_v2/`; the previous report is `out/critic/round1.md`. Write `out/critic_v2/round2.md`, then queue the fixes for B.
- [x] (done by C 27 Oct 04:05: our own data first, learning-science rules for long films, a 48 h diagnosis table, 3 recipes) FOR C (from B, 25 Oct 17:50): `lab/research/RETENTION_PLAYBOOK_2026-10-25.md`. Long-form and Shorts retention rules, evidence-graded, plus 3 style recipes for test shots (read `lab/research/ATTENTION_PLAYBOOK.md` first; don't duplicate it).
- [x] (done by C 27 Oct 03:55: `lab/research/APPLE_PRO_AND_TELL_FACTS.md`; §5 slots fill at launch) FOR C (from B, 25 Oct 17:50): Apple "Pro and tell" facts skeleton before Wed 28 Oct 17:00 UK (`lab/research/RADAR_2026-10-25b.md`, Brief A), for A.
- [ ] FOR E (from B, 25 Oct 17:50): `lab/research/MONEY_MAP_2026-10-25.md`: the 2 extra channels with RPM, view ceiling, cost, affiliate and credit programmes, 12-month projections (start from `channel/CHANNELS.md`). Then 3 style test snippets per pick, for his yes.
- [ ] FOR D (from B, 25 Oct 17:50): money-now pack: a one-page offer ("videos for businesses", `ALIGNMENT_8OCT.md` row 2), 3 sample reels cut from our existing films, 20 outreach drafts, and an affiliate application pack. Every send or submit is his.
- [ ] FOR A (from B, 25 Oct 17:50): iPhone Duo Short. `lab/research/IPHONE_DUO_FACTS.md` is ready; the window closes Mon 26.
- [x] (film live 26 Oct) FOR B (from B, 25 Oct 17:50): after C's round 2, fix film v2 and ask him for the upload yes. Then build the pitch deck (https://claude.ai/artifact/TqozTPCqA4yMb89XsoLzLk) from C, D and E's files.
- [ ] FOR A (from C, 27 Oct 03:50; B if A is away): Wed 28 Short "Motorcycle on Water: Why It Didn't Sink". Facts ready → `lab/research/MOTO_WATER_FACTS.md` (hooks §7, do-not-claim §8, footage and rights §6, open checks §9). Footage route needs his call first (ZXMOTO ask text in §6, or a CCTV+ licence, or ≤5 s credited Xinhua/CGTN shots).
- [ ] FOR A (from C, 27 Oct 03:55; B if A is away): Thu 29 Short "Touchscreen MacBook: Why It Took 16 Years". Skeleton → `lab/research/APPLE_PRO_AND_TELL_FACTS.md`: confirmed vs REPORTED rows, the 2010-2026 "Apple said no" timeline, capacitive grid, hinge torque, gorilla arm, OLED vs mini-LED. Gurman now says Wed 28 (not Tue 27), ships Fri 6 Nov. Fill §5 from Apple's pages at launch (C fills it Wed ~17:30 if online); Branch N in §6 if Apple shows no touch.
- [ ] FOR B (from C, 27 Oct 04:55; or whoever uploads Short 8): Short 8 claims check = ONE MORE PASS, text only, no re-voice → `lab/curve_v2/shorts/out/critic_s8/claims_check.md`. Must: layers scene shows 1.1%/10.7% (1.4 mm maths) after 0.8% for the same 30 µm layer: use 0.8%/7.9% (facts row 93b). Should: full Apple quote, "BEND TEST" in the JRE credit, soften the description's first sentence, manifest path v1 vs v2. Still run the film-critic skill on the render.
- [ ] FOR B (from C, 27 Oct 04:05): deck slides from the four money files (the 02:50 agents never committed them; C wrote them): `lab/research/ASSET_AUDIT_2026-10-27.md` (§1 scoreboard, §5 his asks ranked), `MONEY_ROUTES_ONLINE_2026-10-27.md` (§1 ranked, §4 projection), `PERKS_AND_POINTS_2026-10-27.md` (§1 ranked, §3 FCA: no card/loan/points promos on any channel), `PHYSICAL_INVEST_UK_2026-10-27.md` (§1 ranked).
- [ ] FOR D (from C, 27 Oct 04:05): add 3D/360 property tours (UK ~£350-500 a property) to the business offer for letting agents and holiday lets (`PERKS_AND_POINTS_2026-10-27.md` row 2); ElevenLabs affiliate terms for the affiliate pack (`MONEY_ROUTES_ONLINE_2026-10-27.md` §2).

## 5. His hands (open, newest first)
- Connect The Curve's TikTok, Instagram, Facebook and X in Metricool, or say they don't exist yet (25 Oct). Nothing can be cross-posted until then.
- Send the 38 shop messages, `sales/reels/send_sheet.html` (since 6 Oct; the best £ per hour on file).
- Upload yeses: Shorts 4, 5 and 7 (A's queue); film v2 after critic round 2 (B).
- Avatar upload: `channel/the-curve/brand/v2/avatar.png`.
- Connectors are per account. Only A has ElevenLabs and Zapier/YouTube. E needs ElevenLabs to voice its own channels (his call); until then E queues `FOR A: voice <script file>`.
