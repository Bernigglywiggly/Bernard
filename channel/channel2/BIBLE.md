# Channel 2: The Margin (working name)

**What it is:** one company's real business model per film, the part the price tag hides. Built for the two rules in
`channel/CHANNELS.md`: long-form for watch hours, and a format that is clearly not The Curve re-skinned.

Other names to check for availability: The Fine Print, Where the Money Is, Paid For, Unit Economics.

## Why this niche
- **Money:** business and finance sit near the top of YouTube's RPM ranges, and search for "how X makes money" never
  stops (evergreen, unlike AI news).
- **The user's rule:** people care about what it means for them. Every film ends on what the mechanism means for the
  viewer's wallet, and how to use it to their advantage.
- **The factory fits:** sourced figures on screen, a number made physical, one hidden mechanism, a labelled what-if, a
  mirrored close. The same discipline, a different world.

## What keeps it distinct from The Curve
| | The Curve | The Margin |
|---|---|---|
| Subject | AI's hidden mechanisms | One company's money machine |
| Length | 2-3 min films | **8-10 min** films (mid-roll ads, watch hours), plus shorts |
| Look | ASCII characters, turquoise on graphite | **Ledger and ink**: navy-black ground, brass and paper-white line work, receipts, flows of coins through a diagram; no ASCII |
| Narrator | George (ElevenLabs premade) | **Curve Elder A** (ElevenLabs designed voice `zCRDVM74mhi1dWed3bbU`, deep and warm, made 29 Sep; never George) |
| Music | Arena, Mainframe | A new bed: slow, warm, tape-like (start from `beds.tape_loop`), never Arena |
| Unit | Big Macs | **Per person, per card, per seat**: the amount split down to one viewer's share |
| Structure | Six floors | **THE PRICE → THE MACHINE → THE PROOF → THE MONEY → YOU → WHAT IF → THE CLOSE** |

## The look, v1 (style frames, 1 Oct 2026)
`lab/ch2/look.py` draws the style frames in `channel/channel2/look/` (`sheet.jpg` shows all six): navy-black ground
ruled like a ledger with a brass double margin; IBM Plex Serif for titles and figures, IBM Plex Mono for labels
and the source line under every figure (fonts in `lab/ch2/fonts`, SIL Open Font License). Recurring objects: the
**receipt** (a figure set in a till receipt, the key line circled in brass ink), the **split bar** (one $10 or one
£10 cut into who gets what), **accounts boxes** joined by arrows with **coins** for cash and **paper tickets** for
miles or points. Floors are numbered in roman italics (I · THE PRICE ... VII · THE CLOSE). Next: animate these as
engine scenes once a film is voiced.

## Production (1 Oct 2026): the films are storyboarded and render on the shared engine
- `engine.film.main(..., look_mod=ch2.ledger, cap_mod=ch2.ledger.CAPTIONS)` swaps The Curve's ASCII look and captions
  for the ledger page and serif captions (The Curve is unchanged when these are left out).
- `lab/ch2/kit.py` is the storyboard kit: a film is a list of `Beat`s, each landing on a line or a word (number cards
  with their source line, statements, receipts, split bars, accounts and arrows with coins or tickets, stamps, floor
  cards, quotes, icons). `lab/ch2/ep01-03/scenes.py` are the three storyboards; `film.py` beside each runs them.
- Checked on an estimated Elder-pace timeline (`python3 tools/est_timeline.py ch2/ep01 2.1`, then
  `EP_BUILD=build_est python3 film.py still 30 90 ...`): 8:18, 8:36 and 8:23. Once voiced, the same commands render
  the films: `EL_VOICE=elder python3 film.py voice`, `parts 4 0 4`, `join 4`, `sound`, `master`.
- Music: `chrome_marl` (72 BPM, calm) for now, never Arena; a ledger bed of its own is a later job.
- Shorts: five parts a film (`CLIPS` in each `film.py`), dressed by `ledger.style_shorts()` (THE MARGIN, brass, serif);
  `python3 film.py shorts` after the master, as for The Curve.

## The rules (same discipline as The Curve)
- No jokes. Straight in with the strangest true number. Calm, curious, precise.
- Every figure dated and sourced on screen and in the description. Say "about"; round to two figures.
- One labelled what-if per film ("Not a forecast. A what-if.").
- Every film answers: what does this mean for you, and what should you do differently?
- Disclose the AI narrator (YouTube Studio: Altered or synthetic content: Yes).

## The first ten films
| # | Film | The hidden mechanism | The hook |
|---|---|---|---|
| 1 | **Banks With Wings** (pilot, scripted: `lab/ch2/ep01/script.py`) | Airlines sell miles to banks; the loyalty scheme is worth more than the airline | American Express paid Delta $8.2B in 2025, more than Delta's whole pre-tax profit |
| 2 | **The Landlord in the Golden Arches** (scripted: `lab/ch2/ep02/script.py`) | McDonald's earns much of its money as a landlord to franchisees | $10.4B of rent in 2025, more than its whole net income ($8.6B) |
| 3 | **The $65 Membership** (scripted: `lab/ch2/ep03/script.py`) | Costco's profit is mostly membership fees, so the goods can be sold near cost | The $1.50 hot dog; fees are half of Costco's operating profit |
| 4 | The Ink Trap | Printers sold at a loss, ink sold at a huge markup (razor and blades) | Printer ink, by the litre, against champagne |
| 5 | €20 Flights | Ryanair's ancillary revenue: seats, bags, priority, the app | The ticket is the advert |
| 6 | The Gym Paradox | Memberships that bet on members not coming | The best customer never turns up |
| 7 | The 30% Toll | App store commissions on every in-app purchase | Every subscription on your phone pays a toll |
| 8 | The House Edge | How casinos and betting apps win over thousands of bets | Every bet is fair-looking; the sum never is |
| 9 | The Meal Deal | UK supermarkets' loss leaders and the basket around them | The cheapest item pays for the rest |
| 10 | Pay Per Stream | How Spotify's money reaches artists (or doesn't) | A million streams, and what the artist gets |

Films 1-3 are scripted and sourced (1 Oct 2026, figures from the latest filings: Delta FY2025, McDonald's FY2025,
Costco FY2026). Each runs ~930-960 words: about 8 minutes at Elder A's measured pace (~117 words a minute with the
engine's pauses; EP08 in Elder A ran 2:31 for 295 words). Mid-roll ads need 8:00, so if a voiced film lands under
8:00, add a line in THE MONEY or YOU rather than slowing the voice. Films 4-10 still need their facts checked and
sourced the same way.

## Before launch
1. Check the name and handles are free (YouTube, TikTok, Instagram).
2. Voice films 1-3 with Elder A (needs the ElevenLabs key: `EL_VOICE=elder`; the cloud container has no key), build
   their scenes on the engine in the ledger look, and launch with all three.
3. Channel art in the ledger look (`engine/brand.py` as the model).
