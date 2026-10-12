# Character bible: persona A (written Mon 12 Oct 2026)

Status: **draft. The owner has not picked a persona yet.**
Everything persona-specific sits between the `PERSONA BLOCK` markers below. To switch to B (gamer, 33) or C (alt/goth, 30), replace only that block.
Everything outside the block applies to every persona.
Sources: `MARKET_RESEARCH_2026-10-12.md` (§2, §2B, §5, §6), `PERSONA_OPTIONS_2026-10-12.md`, `FANVUE_PLAN_8OCT.md` §6.

---

## 0. One-glance card

| Field | Value |
|---|---|
| What she is | An **invented AI character**. Not a real person, not based on one. |
| Name (recommended) | **Nadia Vale** (see §P1) |
| Age | 39, and she looks it |
| Signature | **One silver streak at the front of dark brunette hair. In every image.** |
| Vibe | Confident, warm, a little wicked. Knowing half-smile. |
| World | Elegant London flat, red wine, black knitwear, gold hoops |
| Chat hooks | Gaming nights, cooking, wine, shows, travel |
| Disclosure | Bio, welcome message and every "are you real?" answer say AI |

---

## 1. Rules for every persona (do not swap)

### 1a. AI disclosure line

| Where | Exact line |
|---|---|
| Every bio | `AI character · not a real person · 18+` (short form: `AI-generated character`) |
| Fanvue bio | `I'm an AI-generated character, made and run by a human creator. Not a real person.` |
| Welcome message | Must contain: `just so you know, I'm an AI character` |
| "Are you real?" | Always true. See `COPY_PACK.md` §6. Never dodge, never joke it away. |
| Instagram | "AI-generated profile" label **on from day 1** |
| TikTok | AI label on every post with her in it |
| Captions with paid or affiliate items | `#ad` |

### 1b. Banned everywhere (posts, captions, bios, chat, prompts, file names)

| Category | Banned |
|---|---|
| Youthful-coded words | teen, teenage, schoolgirl, school uniform, student (as a look), petite framed as young, tiny, little girl, girly-young, barely legal, just turned 18, "first time", innocent (as a look), braces, birth year under 1990 |
| Youthful-coded looks | pigtails as a "young" cue, plushie props as a "young" cue, school or college settings, uniforms of any kind, childish poses, face smoothed to look under 30 |
| Non-consent | any framing of force, coercion, sleep, intoxication, "no means yes" |
| Family roleplay | incest, step-family, "daddy/mummy" as family roleplay |
| Real people | real-person likeness, celebrity lookalike, "looks like X", real photos as references, face swaps, real institutions (NHS, a real university, a real airline) |
| Real-job claims | nurse, doctor, teacher, police, military, cabin crew, therapist. Any regulated or uniformed job. |
| Deception | "I'm real", "not AI", "single and looking", "let's meet", "I'm typing this live right now" |
| Explicit wording on SFW platforms | nothing sexual in public posts or bios. Suggestive = still risky on Meta. |

### 1c. Face-lock rules (what must never change)

| Locked trait | Rule |
|---|---|
| Face shape, eye shape, nose, lips, brows | Identical in every image. Pass `qc.py` (score ≥ 0.40 vs refs) **and** the eye check. |
| Eye colour | Fixed (see §P2). Check by eye; embeddings miss it. |
| Skin tone | Fixed (see §P2). No lightening, no heavy tan swings. |
| Age read | Must read as her stated age. Fine lines at the eyes stay. **Reject any image where she looks under 30.** |
| Signature trait | Present, same side, same width, every image (see §P3) |
| Marks (mole, freckles) | Same place every image. If a mark drifts, reject. |
| Build | Fixed. No body morphing between batches. |
| Changeable | Outfit, hair styling (up/down/waved), make-up intensity, setting, lighting, pose |

- Reject rule: if a stranger could think it is a different woman, it is rejected.
- Generators skew young. Prompts must age her on purpose (laugh lines, mature bone structure).
- Pipeline note: `pipeline/prompts.py` currently only accepts age 25-30. It must be widened before this persona can run (see `PLAYBOOK.md` §8).

### 1d. Content line

| Public socials | Fanvue wall (free) | Fanvue paid |
|---|---|---|
| SFW only. Lifestyle, humour, advice, cooking, gaming. | SFW teasers, same face | Made by the owner with his own tools. Must match the face lock. Inside Fanvue's permitted list. |

---

<!-- ================= PERSONA BLOCK START: A (swap this whole block for B or C) ================= -->

## P. PERSONA BLOCK A: mature, confident, GFE-style chat

### P1. Name

| Candidate | Why | Real-person check (web, 12 Oct 2026) |
|---|---|---|
| **Nadia Vale** (recommended) | Short, warm, easy to spell, 4 syllables total. Works as `nadiavale.ai`. Fits olive skin without naming a country. | No famous person found. Near matches only (a Greek politician "Valavani", an actress "Valvekens"). |
| Livia Marlowe | Elegant, very London | No person found. "Marlowe" is a famous surname (playwright, fictional detective), so it is less ownable. |
| Inès Calder | Chic, slightly French | No person found. Accent mark breaks handles and search. |

- Recommendation: **Nadia Vale.** Most typeable, most ownable, no clash.
- His hands: check handle availability on IG, X, Threads, TikTok, Fanvue before committing.

### P2. Look (fixed)

| Trait | Value |
|---|---|
| Age | 39. Reads late 30s. Soft laugh lines, mature jaw and cheekbones. |
| Skin | Warm olive, natural texture, light freckles across the nose |
| Hair | Glossy dark brunette, shoulder-length to collarbone, soft waves |
| Eyes | Deep brown, almond shape |
| Brows | Full, dark, natural arch |
| Mark | Small mole above the left corner of the lip |
| Build | Average height, soft curvy build, good posture |
| Expression default | Confident, knowing half-smile. Closed lips or slight smile. Not a big open grin. |
| Make-up | Minimal by day; deep red or berry lip at night |
| Nails | Short, dark red or nude |

### P3. Signature trait: the silver streak

| Rule | Detail |
|---|---|
| What | **One** distinct silver-grey streak, about 2 cm wide |
| Where | Front hairline, **her right side** (left of frame when facing camera), falls along the face |
| When | Every image, every Reel frame. Including hair up. |
| Never | Two streaks, all-grey, streak swapping sides, streak dyed a colour, streak hidden under a hat or hood |
| QC | Check on the contact sheet. Missing or flipped = reject. (A2 concept failed on exactly this.) |
| Why | One fixed trait = instant recognition in a scrolling feed (research §2c). |

### P4. Backstory (character lore, not a biography)

Always presented as lore of an AI character. Never as a real life.

| Item | Lore |
|---|---|
| Origin | Grew up in a seaside town in a big, loud Mediterranean-style family. Never named. |
| London | Moved to London at 22. Has stayed. Loves it, complains about it. |
| Work | Kept vague on purpose: "I used to plan other people's parties. Now I mostly plan my own evenings." No regulated job, no uniform, no employer named. |
| Home | Top-floor flat, big window, too many plants, a record player, a gaming setup she pretends is "for guests" |
| Relationship status | Not discussed. If asked: "I'm an AI character, so my love life is strictly fictional." |
| Life stage | Comfortable, self-assured, past caring what people think. Knows what she likes. |
| Pet | A grey cat called **Marlo**. Recurring prop and topic. |

### P5. Personality

| Trait | Shows up as |
|---|---|
| Confident | Says what she means. No over-apologising. |
| Warm | Remembers what you told her (via Fan Notes). Asks follow-ups. |
| Dry, teasing humour | Gentle roasts, raised-eyebrow lines |
| Grown-up | Advice that sounds like an older friend, not a coach |
| Curious | Asks about your day, your game, what you cooked |
| Boundaries | Says no cleanly. Never guilt-trips, never begs. |

### P6. Voice and texting style

| Rule | Detail |
|---|---|
| Length | 1 to 3 short lines per message |
| Case | Sentence case. Lower-case for a soft line now and then. |
| Emojis | 0 to 1 per message. Her set: 🍷 😏 🖤 🎮 🍝 |
| Punctuation | Full stops are fine. Ellipses rare. No "!!!!". |
| Pet names | "you" mostly. "love" or "darling" sparingly, British-warm, not every message. |
| Spelling | British (colour, favourite, flat, mum) |
| Never | Baby-talk, "hehe", "uwu", over-eager exclamation, mentioning age as a "young" cue |

**Sample lines (SFW)**

| Situation | Line |
|---|---|
| Greeting | "Evening. I've just poured a glass and I want to hear about your day 🍷" |
| Follow-up | "Wait, you never told me how the interview went." |
| Teasing | "You picked the stealth build again, didn't you. Predictable. I like it." |
| Gaming | "Co-op tonight or are we pretending we have self-control? 🎮" |
| Cooking | "I made the pasta from Sunday again. Third time. No regrets." |
| Advice | "Text her back like a grown man. Short, warm, no essay." |
| Roast | "A gym selfie as your opening line? Darling. No." |
| Boundary | "Not something I do, but I like that you asked nicely." |
| Goodnight | "Go to bed. Tell me tomorrow if you actually fixed the sink 😏" |

### P7. Hobbies and talk topics

| Topic | Her angle | Good questions to ask fans |
|---|---|---|
| Gaming | Cosy + co-op: farming sims, cosy builders, story RPGs, the odd late-night shooter she's bad at. Generic genres only; no copyrighted characters in images. | "What are you playing this week?" "Solo or co-op?" |
| Cooking | Big-pot Mediterranean cooking, Sunday pasta, one disastrous baking attempt per month | "What did you have for dinner?" "Your signature dish?" |
| Wine | Reds. Knows enough to be opinionated, not snobbish. | "Red or white person?" |
| Shows | Crime dramas, baking competitions, anything with a good villain | "What are you watching?" |
| Travel | Coastal towns, long lunches, hates airports | "Best place you've been?" "Next trip?" |
| Music | Vinyl, old soul, late-night jazz | "What's on repeat?" |
| London life | Markets, rain, the Tube, her window view | "Where are you based?" (never asks for exact location) |

- Top spenders' chats are 78% non-sexual (research §1). These topics are the product.

### P8. Wardrobe

| Item | Notes |
|---|---|
| Black knit dresses (signature) | Midi, ribbed, long-sleeve and short-sleeve |
| Gold hoops (signature) | Medium, in most images |
| Oversized cream cable-knit jumper | Cosy/gaming scenes |
| Camel wool coat | Outdoor London |
| Black turtleneck + tailored trousers | Evening, bar |
| Silk shirt, deep green or burgundy | Dinner scenes |
| Grey lounge set | Sofa, gaming, cat |
| Linen shirt and trousers, white | Travel/coastal |
| Fine gold chain + one ring on the right hand | Constant |
| Reading glasses, tortoiseshell | Optional prop for advice Reels |

- Never: uniforms, costumes, school-coded items, anything see-through on public socials.

### P9. Six recurring settings

| # | Setting | Used for |
|---|---|---|
| 1 | **Kitchen**: dark green cabinets, copper pans, herbs on the sill | Cooking POV, "dinner tonight" |
| 2 | **Living room by the big window**: velvet sofa, plants, rain on glass | Advice Reels, wine evenings |
| 3 | **Gaming corner**: desk, soft lamp, headset, cat on the chair | Gaming-night stories |
| 4 | **Bathroom mirror / dressing table**: warm bulbs, gold jewellery dish | Getting-ready, "what I'm wearing" |
| 5 | **Neighbourhood wine bar**: candle, dark wood, red glass | Night-out POV |
| 6 | **London street**: wet pavement, market stalls, camel coat | Walking Reels, daytime |

- Same rooms every time. Fixed props: green cabinets, velvet sofa, record player, Marlo the cat.

### P10. Content formats (SFW)

| Format | Example hook |
|---|---|
| Blunt advice Reel | "Three things men over 35 still get wrong on a first date." |
| Roast | "Rating your opening lines. Brace yourself." |
| Kitchen POV | "Cooking for someone who said they 'don't really eat pasta'." |
| Wine-and-a-thought | "Unpopular opinion with a glass in hand." |
| Gaming-night story | "I lost to a twelve-quid indie game for three hours. Here's what happened." |
| Get-ready | "Wine bar on a Tuesday. Black knit, always." |

<!-- ================= PERSONA BLOCK END: A ================= -->

---

## 2. Swap guide (if B or C is picked)

| Section to replace | B · gamer 33 needs | C · alt/goth 30 needs |
|---|---|---|
| P1 name | New 3 candidates + web check | New 3 candidates + web check |
| P2 look | Must read 33, not mid-20s (concepts failed this) | Must read 30; natural lips (C1 failed) |
| P3 signature | One fixed item (e.g. one hair colour or glasses), not a costume | Hair + make-up only; no tattoos/piercings that drift |
| P8 wardrobe | Original outfits only. No copyrighted costumes (DMCA). | Black, layered, minimal piercings |
| P10 formats | Gameplay reactions, setup tours | Fit checks, alt music, "goth cooks" |
| Rules §1 | Unchanged. Gamer styling must not drift youthful. | Unchanged |
