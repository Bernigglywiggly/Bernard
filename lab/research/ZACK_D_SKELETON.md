# How Zack D. Films' Shorts are built, and a skeleton we can use (researched 16-17 Oct 2026)

Method: yt-dlp listing of the channel's latest 200 Shorts (views), auto-captions only (no video) for the 5
most-viewed recent ones, YouTube storyboard thumbnails (one frame per second) for 3 of them, the channel's RSS feed,
and public write-ups. Captions are in the session scratchpad (`.../scratchpad/zackd/`), not the repo.
Script lines are paraphrased or quoted as short fragments: these are his copyrighted scripts.
Tags: [P] measured by us from his channel · [S] secondary source · [EST] our inference.

---

## 1. The channel in numbers

| Metric | Value | Tag | Src |
|---|---|---|---|
| Subscribers | 29.2M | P | Z1 |
| Upload rhythm | About 5 Shorts a day, at fixed slots: 12:30, 14:30, 17:30, 19:30, 21:30 UTC (13-16 Oct) | P | Z2 |
| Latest 200 Shorts (about 40 days) | Median **9.6M** views · mean 10.8M · max 53M · min 679k (the newest, under a day old) | P | Z1 |
| Typical length | **28-38 s** for the top 5. A contractor's brief: hook in 1-2 s, hold for 30-60 s | P / S | Z3, Z5 |
| Production (contractor's account) | Blender, Cascadeur (physics-assisted animation), BlenderKit assets, EmberGen (smoke and fire), After Effects and Media Encoder templates, Flamenco render farm. "A very short turnaround" | S | Z5 |
| Team size | "Around 60" and $1-3k per video are claimed by AI-tool vendors only | [UNV] | Z6 |

## 2. The five Shorts we analysed

| Short | Views | Uploaded | Length | Words | Words/s | Sentences* | Story beats |
|---|---|---|---|---|---|---|---|
| Toucan Gets A Custom Artificial Beak 😌 (MSPVq-5sbCg) | 54.0M | 4 Oct 2026 | 38 s | 111 | 2.92 | 7 | 6 |
| How Cookiecutter Sharks Bite Whales 😨 (CRGWDiIgMZ4) | 52.3M | 9 Oct 2026 | 28 s | 76 | 2.71 | 4 | 4 |
| How Peter Parker's Spider Bite Was Filmed 😮 (dLQQV73fUI0) | 30.4M | 2 Oct 2026 | 31 s | 86 | 2.77 | 4 | 4 |
| He Fell 60 Feet Into A Well 😱 (N1VSv7-h5Xc) | 28.4M | 9 Oct 2026 | 38 s | 93 | 2.45 | 6 | 6 |
| Why Alcatraz Only Gave Prisoners Hot Showers 🤨 (zZVlkSIn8BY) | 27.5M | 2 Oct 2026 | 28 s | 75 | 2.68 | 4 | 4 |
| **Average** | **38.5M** | 1-2 weeks old | **32.6 s** | **88** | **2.7 (≈160 wpm)** | **5** | **5** |

*Auto-caption punctuation, so treat sentence counts as approximate. Average sentence length: **16-21 words**,
held together by commas and connectives.

## 3. Titles: what wins (latest 200 Shorts)

| Title type | Count | Median views | Example shape |
|---|---|---|---|
| "What ..." | 9 | **13.0M** | What Happens To Bugs When You Mow? |
| "Why ..." | 22 | **11.0M** | Why Alcatraz Only Gave Prisoners Hot Showers |
| Person + event | 22 | 10.5M | He Fell 60 Feet Into A Well |
| "The X Who/That ..." | 40 | 9.3M | The Bullet That Landed Under Her Pillow |
| "How ..." (a process) | 45 | 8.4M | How Cookiecutter Sharks Bite Whales |
| "How To ..." | 14 | 7.5M | How To Get Water Out Of Your Ear |
| "Can You ..." (puzzle) | 4 | 7.0M | Can You Solve This Stolen Money Puzzle? |

| Title rule | Data |
|---|---|
| An emoji at the end | **200 of 200** titles. Most used: 😮 45 · 🤔 41 · 😨 19 · 🤨 16 · 😢 11 · 😱 10 |
| Length | Median **7 words / 37 characters** (range 3-9 words) |
| Numbers | Only 10 of 200 titles contain one, and then as the shock ("60 Feet", "133 Days") |
| Labels for made-up content | "(Patent Pending)" ×3, "(fiction)", "(parable)" |
| Description box | Empty on all five |

## 4. Hooks: how the first sentence works

Common rule: **no greeting, no topic sentence, no "did you know".** The title asks the question; the first line
drops you into the middle of the event.

| Hook type | What the first line does | Seen in | Short fragment |
|---|---|---|---|
| Mid-impact cold open | Starts at the moment of injury, with "it" before we know what "it" is | Toucan | "It swung down and smashed..." |
| Mechanism in motion | Starts halfway through the process, with a vivid comparison | Cookiecutter | "...drive in like a curved blade" |
| Secret procedure | Step 1 of a hidden process nobody has seen | Spider bite | "A special pattern was drawn onto the spider" |
| Peril in one breath | Who + mishap + one number + a sensory word | Well | "...nearly 60 ft into complete darkness" |
| Counterfactual | "If X, then Y": the logic premise first, the answer saved for the end | Alcatraz | "If Alcatraz had cold showers..." |

## 5. Rhythm and curiosity gaps

| Device | How it works | Frequency |
|---|---|---|
| Open loop | The title's question is answered only in the **last 3-5 s** | 1 per Short |
| "What happens next" chain | Each sentence ends on an action whose result isn't known yet, linked by **So / But / Then / Once / After** | 3-8 connectives per Short |
| New beat | Problem → plan ("So") → snag ("But") → fix ("So"/"Once") → next step ("Then") → payoff | **every 5-8 s** |
| No recap, no asides | Never repeats a fact and never steps outside the story | — |
| Words on screen | Captions 1-3 words at a time, white with an outline, centred low | constant |
| Cut rate [P, storyboard] | The camera angle changes about every 1-2 s; a new location every ~3 s | — |

**Beat map of the Toucan Short [EST, paraphrased]:** 0-4 s the strike and the broken beak in close-up · 4-8 s the
consequence (it can't eat) · 8-15 s the plan (scan, compare with a healthy beak, model on a computer) · 15-23 s the
snag (too heavy, so a hollow design) · 23-33 s the procedure (fit, glue, pin) · 33-38 s the payoff: it eats again,
which mirrors the opening.

## 6. How the visuals escalate [P: storyboard frames · EST]

| Stage | Picture | Seen in |
|---|---|---|
| 0-3 s | **The most visceral close-up first**: the beak snapping with fragments, teeth sinking into flesh, a toddler dropping into a shaft | Toucan, Cookiecutter, Well |
| Explanation | A clean "diorama" on a bright sky background: side-by-side comparisons, a CAD model on a monitor, a measurement label in the frame (a red "60ft" depth gauge) | Toucan, Well |
| Procedure | Macro shots of hands and tools: scanner, glue, pin, digging | Toucan, Well |
| Payoff | A warm wide shot that rhymes with the opening: the animal eats; the rescuer reaches the child | Toucan, Well |
| Look | Stylised-real 3D: smooth humans, uniformed rescuers and doctors, saturated sky blues and orange flesh tones | all |

## 7. The "unhinged" element

| Ingredient | Examples (titles) | Why it works [EST] |
|---|---|---|
| Body horror and peril in macro | Cookiecutter bite; maggots falling from a ceiling; stuck in quicksand for 14 hours | You can't look away, and it's "educational", so you don't feel bad watching |
| Absurd but true | Alcatraz's hot showers; running like Naruto; how to stuff a turtle | Your first reaction is "that can't be real" |
| Deadpan fake inventions | "The Bathroom Mode (Patent Pending)" | Comedy in the same voice and look; labelled so it isn't deception |
| Viewers' own words | "Disturbing, creepy... yet educational" (fan wiki) | Mixed feelings drive comments and shares (S) |

## 8. Endings, loops, brand marks

| Element | What he does |
|---|---|
| Ending | The last line resolves the question, **the picture rhymes with frame 1**, and it stops dead: no outro, no call to action, no logo. The loop starts before you decide to swipe |
| Loop seam | The final image (fruit eaten, the "bite" moment) sits next to the opening image (fruit slipping, the spider dropping) |
| Voice | One calm narrator, steady pace, no hype words |
| Brand marks | Emoji at the end of every title · 7-word titles · empty descriptions · word-by-word captions · stylised 3D humans · sky-blue explainer sets · 5 uploads a day at fixed times |

## 9. Borrow vs don't copy

| Borrow (the mechanics) | Don't copy (his identity, or what breaks our rules) |
|---|---|
| Open on the most extreme true moment; the title asks the question and line 1 never answers it | His character designs, colour palette, caption font and placement: make our own (CRAFT §3) |
| A So / But / Then chain, with a new beat every 5-8 s | The emoji-at-the-end title habit: it is his brand mark |
| Long, smooth sentences at about 2.7 words a second. This fits CRAFT §2 (professor voice, no staccato) | Five uploads a day. CRAFT §1 caps us at about 5-7 Shorts a week per channel (the inauthentic-content risk) |
| One number per Short, shown as an object in the frame (the "60ft" gauge) | Gore for its own sake. Our "unhinged" is the scale or absurdity of the fact (2 s of thrust, refills taking hours) |
| The payoff picture mirrors the opening; hard stop, no outro | Fake inventions presented as fact. If we ever joke, label it like he does |
| A diorama set for explaining, macro shots for the procedure | Copying his topics. His topics are human-interest; ours are tech and money |
| 28-38 s length | — |

## 10. Skeleton A: a 30-60 s segment (a Short, or one block of a long film)

At 2.7 words a second, 40 s is about 105 words. Five to seven sentences.

| Time | Beat | Words | Picture | Rule |
|---|---|---|---|---|
| 0-3 s | **Impact line**: the most extreme true moment, mid-action, with a pronoun or a number | 8-12 | Frame 0 is a finished composition: the extreme moment in close-up | No greeting, no definition (14 Oct lesson: definitions at the start cost 26 points of retention) |
| 3-8 s | **Consequence**: why it matters or what went wrong | 12-15 | Wider shot that shows the stakes | One number, shown as an object |
| 8-18 s | **"So..." the attempt or mechanism**, step 1 | 25-30 | Diorama set: side by side, cutaway, measurement | Cut every 1-2 s, a new set every ~3 s |
| 18-28 s | **"But..." the snag**, the surprising constraint | 20-28 | Macro on the part that fails | The fact that makes people comment |
| 28-36 s | **"So / Then..." the fix**, the payoff mechanism | 18-24 | Procedure in macro | — |
| 36-40 s | **Payoff line** answers the title; the picture rhymes with frame 1 | 8-12 | Mirror of the opening shot | Hard cut to black or straight back to frame 0. No outro |

**Applied to the Roadster [EST]:** 0-3 s the car hanging upside down from the curl (our own 3D). · "It is held up
by fans that suck twice its own weight." · "So the air for the thrusters is packed into a bottle at around
10,000 psi..." · "But that whole bottle lasts about two seconds at full thrust..." · "So Tesla uses it once per
fill, then waits hours to refill..." · Payoff: the car landing in smoke, the same shot as the opening, and the line
"Two seconds of rocket, then the wait."

## 11. Skeleton B: a 6-10 min film made of segments that work as Shorts

| Block | Time | Content | Cut as a Short? |
|---|---|---|---|
| Cold open | 0:00-0:20 | The single most extreme moment of the whole film, then the question the film answers | Yes, as a teaser |
| Segment 1 | 0:20-1:20 | Skeleton A: the event itself (what happened) | Yes |
| Segment 2 | 1:20-2:20 | Skeleton A: trick #1 (fans: 2 g of suction) | Yes |
| Segment 3 | 2:20-3:20 | Skeleton A: trick #2 (cold gas: 80 kN, 2 s) | Yes |
| Bridge + forward tease | 3:20-3:40 | "In a minute, the number Tesla didn't put on the slide" (CRAFT §2: a tease every 60-90 s) | No |
| Segment 4 | 3:40-4:40 | Skeleton A: the catch (the refill: hours; 38-40 kWh even with a perfect compressor) | Yes |
| Segment 5 | 4:40-5:40 | Skeleton A: rivals compared (McMurtry upside down, Rimac 1.66 s) | Yes |
| Segment 6 | 5:40-6:40 | Skeleton A: legal and safety (FAA: "not an aircraft") | Yes |
| Verdict | 6:40-7:30 | **Our judgement** (CRAFT §1 authorship): what it really is, what to watch next (Tesla Q3 on 21 Oct, 2028) | Yes, as the "verdict" Short |
| End | 7:30-8:00 | Payoff that rhymes with the cold open; one end screen | No |

Rules for this shape: every segment opens with its own impact line and closes with its own payoff, so it can be
cut out without editing. Change the order and shape from film to film (CRAFT §1: vary the structure). Above 8:00,
mid-rolls are available (RADAR_2026-10-11 §5).

## 12. Using real footage (e.g. Tesla's stream): practical rules

| Question | Answer | Src |
|---|---|---|
| Who owns event livestream footage? | The company that produced it: Tesla owns its stream and the clips on its YouTube and X accounts. A spectator's phone video belongs to whoever filmed it. News-agency pictures (Reuters, AP) are licensed products | [K] Z9 |
| Is there a "safe number of seconds"? | **No.** YouTube's fair-use page gives no time limit; courts decide case by case, and even a few seconds can draw a claim that blocks monetisation | Z7 |
| What does Content ID do? | Rights holders who qualify upload reference files. A match produces a claim, and the owner chooses **block, monetise or track**, possibly by country. Content ID cannot decide fair use; you can dispute | Z8, Z7 |
| US fair use | Four factors: purpose (transformative and commentary help), nature (factual helps), amount (small, but not the "heart"), market effect. Giving credit or writing "no infringement intended" **does not** make it fair use | Z7 |
| UK fair dealing (we're in the UK) | Criticism, review and quotation are allowed for any work, **with sufficient acknowledgement**. Reporting current events covers everything **except photographs**. The test: how would "a fair-minded and honest person" have dealt with the work? Use only what is necessary, and don't substitute for the original | Z9 |
| YouTube's money rule | "Reused content" without meaningful original commentary can lose monetisation even when it is legal; that is our CRAFT §1 risk | CRAFT §1, Z10 |

**Our rules (practical, lowest risk first):**
1. Rebuild the money shots in **our own 3D** (the curl, the roll, the plume). That is the authorship and carries no claim risk.
2. Use real clips only as **evidence** ("here's the real thing"): **3-7 s each**, a handful per film, never the whole stunt.
3. Always put **our narration on top** and remove the clip's own audio and music (music is the commonest Content ID trigger).
4. **Transform it:** freeze-frames, arrows, measurements, split-screen with our 3D, slow motion with a read-out.
5. **Credit on screen and in the description:** "Footage: Tesla, YouTube, 15 Oct 2026" plus the URL. Required for UK fair dealing; not enough on its own in the US.
6. Never make a "best moments" compilation of someone else's video; that substitutes for the original.
7. Keep a clip log per film (URL, in/out times, why we needed it) in the film's FACTS file.
8. If a claim arrives, dispute it only when the clip is short, commented on and transformed; otherwise trim it and re-upload.
9. Avoid agency footage (Reuters, AP, Getty) unless it's licensed.

## Sources

- Z1 yt-dlp listing of https://www.youtube.com/@zackdfilms/shorts (latest 200, views) and video metadata, pulled 16 Oct 2026.
- Z2 Channel RSS, https://www.youtube.com/feeds/videos.xml?channel_id=UCvz84_Q0BbvZThy75mbd-Dg, read 16 Oct 2026.
- Z3 The five Shorts: https://www.youtube.com/shorts/MSPVq-5sbCg (4 Oct 2026) · https://www.youtube.com/shorts/CRGWDiIgMZ4 (9 Oct 2026) · https://www.youtube.com/shorts/dLQQV73fUI0 (2 Oct 2026) · https://www.youtube.com/shorts/N1VSv7-h5Xc (9 Oct 2026) · https://www.youtube.com/shorts/zZVlkSIn8BY (2 Oct 2026); auto-captions (en-orig) and storyboards pulled 16 Oct 2026.
- Z4 Zack D. Films fan wiki, https://zackdfilms.fandom.com/wiki/Zack_D._Films (user-edited; read Oct 2026).
- Z5 Chris Reilly (contractor) portfolio, https://supersets.chrisreillyportfolio.com/zackdfilms.php (undated; cites "close to 20 million" subscribers, so written before 2026).
- Z6 Medium post, https://medium.com/@lazargrr1/how-i-create-zack-d-films-style-3d-shorts-with-ai-its-easy-3dd9450b4f0a, and vendor pages (team size and cost claims, unverified).
- Z7 YouTube Help, "Fair use on YouTube", https://support.google.com/youtube/answer/9783148, read 16 Oct 2026.
- Z8 YouTube Help, "How Content ID works", https://support.google.com/youtube/answer/2797370, read 16 Oct 2026.
- Z9 GOV.UK, "Exceptions to copyright", https://www.gov.uk/guidance/exceptions-to-copyright, read 16 Oct 2026.
- Z10 YouTube channel monetisation policies (reused content), https://support.google.com/youtube/answer/1311392; not re-read this session (the summary is in CRAFT.md §1).
