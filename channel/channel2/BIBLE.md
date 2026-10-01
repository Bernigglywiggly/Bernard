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
| 2 | The Landlord in the Golden Arches | McDonald's earns much of its money as a landlord to franchisees | McDonald's sells burgers; it collects rent |
| 3 | The $60 Membership | Costco's profit is mostly membership fees, so the goods can be sold near cost | The shop barely profits from the shopping |
| 4 | The Ink Trap | Printers sold at a loss, ink sold at a huge markup (razor and blades) | Printer ink, by the litre, against champagne |
| 5 | €20 Flights | Ryanair's ancillary revenue: seats, bags, priority, the app | The ticket is the advert |
| 6 | The Gym Paradox | Memberships that bet on members not coming | The best customer never turns up |
| 7 | The 30% Toll | App store commissions on every in-app purchase | Every subscription on your phone pays a toll |
| 8 | The House Edge | How casinos and betting apps win over thousands of bets | Every bet is fair-looking; the sum never is |
| 9 | The Meal Deal | UK supermarkets' loss leaders and the basket around them | The cheapest item pays for the rest |
| 10 | Pay Per Stream | How Spotify's money reaches artists (or doesn't) | A million streams, and what the artist gets |

Every film from 2 on needs its facts checked and sourced the way the pilot's are.

## Before launch
1. Check the name and handles are free (YouTube, TikTok, Instagram).
2. Voice the pilot with Elder A (needs the ElevenLabs key: `EL_VOICE=elder`), build its scenes on the engine in the
   ledger look, then two more films before launch.
3. Channel art in the ledger look (`engine/brand.py` as the model).
