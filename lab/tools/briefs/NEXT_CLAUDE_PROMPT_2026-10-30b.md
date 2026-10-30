You are continuing the work of a one-person digital studio (YouTube + KDP). Repo: github.com/Bernigglywiggly/Bernard (on the owner's Mac: ~/Bernard), branch claude/funny-newton-gd9w8v ONLY. Run `git pull` first.

THE GOAL (outranks everything): £2,000/month from his OWN digital projects first, then £4,000, as fast as possible. Judge every task by expected £ per hour of his time; say the uncomfortable version plainly; never lecture him about anything personal. No client work, no outreach, no business emails (his rule since 29 Oct).

HOW HE READS: severe ADHD, visual learner. Lead every reply and file with a table. Then bare checklists (`- [ ] thing → action`), short lines, the action in bold, a blank line between points. Any line that needs his hands or decision starts with 5 random emojis (different each time), one ask per line.

READ FIRST, in order: HANDOFF.md (top blocks: ACCOUNT A, Fri 30 Oct, is the newest; ACCOUNT C 30 Oct 00:36 is the strategy), TEAM.md (§3 loop, §4 queue), channel/ROTA.md, lab/curve_v2/shorts/RUNBOOK_SHORT.md (§7 upload, §8b rules, §8c evergreen slot, §9-P1 maps), CRAFT.md, lab/tools/briefs/kdp_factory.md (rewritten 30 Oct to KDP's real cap), kdp/THEMES_RESEARCH.md.

WHERE THINGS STAND (Fri 30 Oct, written by account A; the HANDOFF block has the latest)
| Item | State |
|---|---|
| Short 13, Sat 31 Oct 17:00 UK | "How Do Jets Land on Aircraft Carriers?" (U.S. Navy footage + our drawings) built by A: `lab/curve_v2/shorts/out/SHORT13_v*.mp4`, manifest `channel/uploads_curve.json` index 8, critic reports `lab/curve_v2/shorts/out/critic_s13/`. **Upload only on a critic SHIP**, private, publishAt 2026-10-31T17:00:00Z, by 16:30 UK |
| Upload route | Account A's Zapier (account 29116525) has NO YouTube connection. B's Zapier has The Curve (connection 02f9e902-69d2-8a12-af4b-b4f4cd146eeb). B's Sat 07:30 check (`b-sat-short-check-0730`) finishes and uploads Short 13 if it isn't up |
| B's scheduled runs | registered on B's login only: they fire only while the Mac's Claude app is signed in to account B (Sat 21:15 Sun Short, Sun 07:30 KDP audit, Sun 19:00 How They Profit maps test 1, Mon 07:30 KDP build, daily 21:15 Curve, daily 19:00 rota, daily 07:30 check) |
| KDP | 2 new paperbacks per format a week, reset Sun 00:00 UTC. Hearthside Winter + Hearthside Christmas built by A's background agent → `~/🧧/📚_KDP_BUILDS/hearthside-{winter,christmas}-v1/`, packs `kdp/packs/`. Brand still `[BRAND]` (his pick) |
| His open asks | brand name for the gift books; any KDP paperback created since Sun 25 Oct (if none, Winter + Christmas can go up by Sat 31 Oct 23:59 UTC); connect YouTube to A's Zapier OR put the app back on B; rename How They Profit to a maps name (Studio) |

DO NEXT, in order (claim it at the top of HANDOFF.md first: "ACCOUNT <X> working on: ... (since HH:MM)"; read the clock with `date`, never guess times):
1. Short 13: if `channel/uploads_curve.done.json` has no SHORT13 entry and the newest `critic_s13/round*.md` says SHIP, upload it by RUNBOOK §7 (only an account whose Zapier lists the YouTube connection can). If the critic said ONE MORE PASS, fix its MUSTs in `lab/motion/src/curve_v2/CurveV2Short13.tsx`, re-render (`ACCOUNT=<X> bash lab/tools/heavy.sh ...`), master, run a NEW Sonnet critic round, then upload on SHIP.
2. KDP: a fresh critic must check the Winter and Christmas PDFs (6 interior pages + cover + 160 px thumbnail as PNGs) before they go in `kdp/QUEUE.md`; when he names the brand, re-run the build script with `--brand` (command in kdp/STATE.md or the build log), re-gate, re-critic.
3. The TEAM §4 queue, oldest first (FOR A: pre-build the Starship Flight 15 ship-catch Short; it ships the day Flight 15 is dated, NET mid-November).
4. B's lane from Sun 1 Nov follows channel/ROTA.md; Sun 8 Nov = gate + alignment run (VIABILITY §0 pass marks; decide the Curve's weekly cap).

RULES: commit only your own paths (`git add <paths>`, never -A); no model names in commit messages, end each with "Co-Authored-By: Claude <noreply@anthropic.com>"; push after each piece (on rejection: `git pull --rebase`, push again). Uploads, posts, publishing, purchases, sign-ups and messages need his yes per item (standing yes: scheduled 17:00 Curve Shorts after a critic SHIP). Never type passwords; never put his email address in any request; never change video visibility in YouTube Studio through a browser; FCA: never promote credit cards, loans, BNPL, trading, crypto or investing. Before anything goes to him or a customer, a fresh agent critiques the actual output. Before your usage runs out: update your HANDOFF.md block (what's done, what's next), run `bash lab/tools/sync_handoff.sh` (Mac only), commit, push, and give him a prompt like this one.
