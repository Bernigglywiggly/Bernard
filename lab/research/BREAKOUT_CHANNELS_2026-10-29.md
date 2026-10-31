# Breakout channels started on or after 1 May 2026: who is already pulling heavy views, and what they do

**29 Oct 2026 | YouTube Data API v3 via Zapier, read-only | 10 `search.list` queries (q = how it works, explained, robot, engineering, science facts, AI, money, business, history with `videoDuration=short`; documentary with `medium`), `order=viewCount`, `publishedAfter=2026-10-01`, `regionCode=US`, `relevanceLanguage=en`, 50 results each | 5 `channels.list` calls (250 channel ids) | 1 `videos.list` call (50 video ids) | kept = channel created on or after 2026-05-01 AND (1,000,000+ total views OR 10,000+ subscribers) | age and views/day measured to 29 Oct 2026.**

Niche, format and engine fit are my reading of channel names, video titles and video lengths. I did not watch the videos or listen to them, so 'Language' is the language of the titles. 'Inferred' marks a guess. Missing fields are written n/a.

| Headline numbers | Value |
|---|---|
| API calls used | 16 of 16 (10 search, 5 channels, 1 videos; the 16th went on video stats instead of a sixth channel batch) |
| Unique channel ids the 10 searches surfaced | about 410 (hand count, plus or minus 5) |
| Channel ids looked up | 250 (about 42 big established brands and about 120 low-fit small channels were skipped; see Limits) |
| Created on or after 1 May 2026 | 44 of the 250 |
| Kept (also 1M+ views or 10k+ subs) | 39 |
| Created 1 Jan-30 Apr 2026 and cleared a threshold | 21 (context only, section 5) |
| Kept channels whose format our engine could make ('yes' or 'partly') | 22 of 39; 21 of them sit in the five concepts in section 3 (Reconstructed, 16 min, is the exception). The other 17 are 'no' (section 4). |

## 1. Kept channels, ranked by views per day of age

Views/day = lifetime channel views / days since the channel was created. Under 7 days of age is noisy (Doodles Fact is 5 days old). Subs per 1k views = subscribers / views x 1,000 (for reference, The Curve is about 0.84: 36 subs on 42,984 views, 28 Oct, from HANDOFF.md).

| # | Channel | Created | Age (d) | Subs | Total views | Videos | Views/day | Views/video | Subs per 1k views | Niche | Format | Language | Our engine? |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | The Why Side | 2026-09-26 | 33 | 33,300 | 65,571,436 | 35 | 1,987,013 | 1,873,470 | 0.51 | engineering and science curiosities | faceless curiosity explainer, 39-73 s, 'Why...' titles; visuals not inspected | English | yes: the 'why does this odd thing exist' formula with our own drawings; check any real person's story first |
| 2 | Cini Mini Tamil | 2026-07-16 | 105 | 177,000 | 176,666,550 | 107 | 1,682,539 | 1,651,089 | 1.00 | film recaps | film-clip commentary with Tamil voice-over | Tamil | no: copyrighted film clips |
| 3 | Doodles Fact | 2026-10-24 | 5 | 11,400 | 5,435,063 | 6 | 1,087,013 | 905,844 | 2.10 | engineering, build process | cross-section build animation, 1 min 39 s (inferred from title) | English | partly: the same title sits on 'digs' a day later, so it is being cloned; change subject and look |
| 4 | Zidan Construction | 2026-10-13 | 16 | 11,300 | 16,187,251 | 43 | 1,011,703 | 376,448 | 0.70 | construction robots | raw-looking 18 s clip with a promise title | English | partly: topic fits The Curve; the clip itself is probably not ours to copy, so use maker footage (5 s or less a shot, credited) plus a diagram |
| 5 | ShortsBreak Plus OTT | 2026-06-17 | 134 | 127,000 | 130,513,105 | 275 | 973,978 | 474,593 | 0.97 | comedy skit series | AI-generated episodes (title says 'AI Robot') | Hindi | no: AI-generated serial skits |
| 6 | Under Six Minutes Studio | 2026-05-31 | 151 | 20,700 | 143,190,148 | 58 | 948,279 | 2,468,796 | 0.14 | engineering, product design | animated explainer, 35 s hero (inferred from name and length) | English | yes: 'how engineers solved X' in 35 s with our own animation, no clip needed |
| 7 | Bot Wars Usa | 2026-09-07 | 52 | 16,500 | 40,383,683 | 17 | 776,609 | 2,375,511 | 0.41 | robot combat spectacle | 15 s clips that look AI-made (title and length; not verified) | English | no: AI spectacle with no explanation |
| 8 | 지구또보기 | 2026-05-14 | 168 | 25,800 | 128,441,003 | 527 | 764,530 | 243,721 | 0.20 | industrial processes | 8 s process loops at 3.1 uploads a day; probably reuploaded footage | English titles | no: reuploaded loops |
| 9 | Hyperbolic AI | 2026-09-20 | 39 | 6,410 | 23,827,126 | 45 | 610,952 | 529,492 | 0.27 | AI and meme clips | 7 s transition clip | English | no: AI visual with no explanation |
| 10 | Behind The Process | 2026-06-28 | 123 | 113,000 | 59,013,431 | 195 | 479,784 | 302,633 | 1.91 | science and archaeology facts | faceless fact Shorts | Hindi | partly: the fact format is ours, the language is not |
| 11 | Income Edge | 2026-06-19 | 132 | 6,190 | 55,177,911 | 126 | 418,014 | 437,920 | 0.11 | personal finance | clip commentary (hashtag #daveramsey, so a real person's clips; inferred) | English | no: a real person's clips; only 0.11 subs per 1,000 views |
| 12 | One Map, One Battle | 2026-10-07 | 22 | 9,370 | 9,138,062 | 46 | 415,366 | 198,654 | 1.03 | military history | animated-map explainer, about 1 min 20 s (inferred from name) | English | yes: maps are our own drawings; new niche for us |
| 13 | Mekii Stories | 2026-08-12 | 78 | 146,000 | 31,306,442 | 105 | 401,365 | 298,157 | 4.66 | family drama | AI-generated story serial (#ai in title) | Hindi/Urdu | no: AI serial |
| 14 | PS Rank | 2026-07-11 | 110 | 26,300 | 39,575,730 | 98 | 359,779 | 403,834 | 0.66 | robot-fail rankings | ranking compilation, probably third-party clips (inferred) | English | no: third-party clips |
| 15 | Untold Theory | 2026-08-20 | 70 | 42,500 | 21,950,170 | 57 | 313,574 | 385,091 | 1.94 | 'evolution of' product and tech history | 43-51 s timeline Shorts | English | yes: our own drawing per era |
| 16 | How Things Were Built | 2026-10-15 | 14 | 9,890 | 4,068,365 | 91 | 290,598 | 44,707 | 2.43 | construction, build process | cross-section build explainer; 91 videos in 14 days | English | partly: format fine, but 6.5 uploads a day is mass-production |
| 17 | Fact Capture | 2026-08-05 | 85 | 345,000 | 22,226,346 | 73 | 261,486 | 304,470 | 15.52 | animal and world facts | faceless fact Shorts, 32 s hero | English | partly: format is ours but needs our own pictures; best subscriber conversion in the table |
| 18 | Facts Compass | 2026-07-16 | 105 | 34,500 | 26,754,004 | 42 | 254,800 | 637,000 | 1.29 | India infrastructure and engineering facts | explainer, 2 min 35 s hero | English | partly: build stories with our own diagrams |
| 19 | Cleanwith__Marina | 2026-07-29 | 92 | 3,790 | 23,388,308 | 84 | 254,221 | 278,432 | 0.16 | home-cleaning humour | person-on-camera skit, 9 s hero (inferred from hashtags) | English | no: person on camera, skit |
| 20 | Couple Core | 2026-05-29 | 153 | 33,400 | 36,264,896 | 171 | 237,025 | 212,075 | 0.92 | family-drama skits | scripted or AI skit; same 'dad spent the tuition money' premise on 3 channels | English | no: mass-produced skit template |
| 21 | Reconstructed | 2026-10-03 | 26 | 21,200 | 5,226,508 | 28 | 201,020 | 186,661 | 4.06 | aviation incident reconstruction | long-form animated reconstruction, 16 min | English | partly: own animation fits, but 16 min and real named people |
| 22 | Bodycam C4 | 2026-09-09 | 50 | 15,000 | 9,463,132 | 14 | 189,263 | 675,938 | 1.59 | true crime | police bodycam compilation, 19 min (inferred) | English | no: third-party footage of real people |
| 23 | redmark. | 2026-10-10 | 19 | 2,270 | 2,336,189 | 22 | 122,957 | 106,190 | 0.97 | tech and cars, news-led | topical explainer, 1 min 19 s | English | partly: news-jack; the sampled hero has only 33k views |
| 24 | Ali Wildlife Hunt | 2026-09-17 | 42 | 3,970 | 4,871,807 | 3 | 115,995 | 1,623,936 | 0.81 | wildlife | footage-led long-form, 11 min, 3 videos | English | no: long-form footage |
| 25 | How Things Work | 2026-09-17 | 42 | 5,060 | 4,165,675 | 24 | 99,183 | 173,570 | 1.21 | engineering mechanisms | 30 s mechanism explainer | English | yes: 30 s, one mechanism, own diagram |
| 26 | Jayansh Insight | 2026-06-23 | 128 | 11,300 | 11,709,262 | 19 | 91,479 | 616,277 | 0.97 | Indian history | documentary-style long-form, 16 min | English | no: long-form, third-party images |
| 27 | CA Yash Aggarwal | 2026-10-10 | 19 | 6,030 | 1,570,059 | 13 | 82,635 | 120,774 | 3.84 | tax and finance | talking head | English/Hinglish | no: real person on camera |
| 28 | Varz Thought | 2026-06-27 | 124 | 4,100 | 9,711,868 | 46 | 78,322 | 211,128 | 0.42 | science and engineering curiosities | 35 s curiosity Shorts | English | partly: the hit needs macro footage of tiny parts that we do not have, so draw it instead |
| 29 | Built Mysteries | 2026-06-22 | 129 | 24,700 | 10,030,717 | 96 | 77,757 | 104,487 | 2.46 | built-environment history | explainer, about 1 min 17 s hero | English | partly: needs historical pictures; use our own drawings and maps |
| 30 | Sasta Animator | 2026-09-24 | 35 | 1,520 | 2,712,546 | 36 | 77,501 | 75,348 | 0.56 | engineering mechanisms | animated explainer, 51 s hero | English titles | yes: animated mechanism explainer |
| 31 | Curadels | 2026-09-18 | 41 | 1,110 | 2,991,429 | 25 | 72,962 | 119,657 | 0.37 | tech and cars, news-led | topical explainer, 35 s hero | English | partly: news-jack; the sampled hero has only 115k views |
| 32 | The History Talks | 2026-05-25 | 157 | 16,300 | 11,262,059 | 185 | 71,733 | 60,876 | 1.45 | Indian history, exam coaching | classroom clips of a named teacher (inferred) | Hindi | no: a real person's clips |
| 33 | Boult Explained | 2026-06-26 | 125 | 20,100 | 7,069,911 | 18 | 56,559 | 392,773 | 2.84 | film lore | film-clip commentary | English | no: copyrighted film clips |
| 34 | Rural Travel TV | 2026-09-27 | 32 | 8,840 | 1,694,995 | 5 | 52,969 | 338,999 | 5.22 | village-life travel | footage-led documentary, 16 min, 5 videos | Urdu/Hindi | no: long-form footage |
| 35 | Knowledge Universe | 2026-06-08 | 143 | 51,600 | 5,781,626 | 165 | 40,431 | 35,040 | 8.92 | body and food science | 3D science animation, 1 min 48 s hero | Hindi | partly: close to our animated diagrams; language is not ours |
| 36 | History Maps Lore | 2026-09-01 | 58 | 3,850 | 2,329,002 | 3 | 40,155 | 776,334 | 1.65 | military history | map explainer, 1 min 25 s hero, 3 videos | English | yes: maps are our own drawings |
| 37 | GeoGlobeFiles | 2026-06-04 | 147 | 3,410 | 3,487,179 | 138 | 23,722 | 25,269 | 0.98 | geography facts | map facts Shorts, 1 min 8 s hero | English | yes: maps are our own drawings |
| 38 | Gyan ka Pitara | 2026-07-01 | 120 | 16,500 | 2,698,730 | 161 | 22,489 | 16,762 | 6.11 | body and food science | 3D science animation, 1 min 34 s hero | Hindi | partly: language is not ours |
| 39 | MythProcess | 2026-07-27 | 94 | 1,440 | 1,782,315 | 10 | 18,961 | 178,232 | 0.81 | science myths | 45 s science Shorts | Hindi | partly: language is not ours |

Country (from the API, where set) for context: The Why Side US; Cini Mini Tamil IN; 지구또보기 KR; Behind The Process IN; Income Edge US; Mekii Stories PK; PS Rank IN; Untold Theory IN; How Things Were Built NL; Fact Capture IN; Facts Compass IN; Reconstructed US; Bodycam C4 US; redmark. MA; Ali Wildlife Hunt US; How Things Work IN; Jayansh Insight IN; CA Yash Aggarwal IN; Varz Thought US; Sasta Animator IN; Curadels TR; Boult Explained IN; Rural Travel TV PK; Knowledge Universe IN; Gyan ka Pitara IN; MythProcess IN. Not set: Doodles Fact, Zidan Construction, ShortsBreak Plus OTT, Under Six Minutes Studio, Bot Wars Usa, Hyperbolic AI, One Map, One Battle, Cleanwith__Marina, Couple Core, Built Mysteries, The History Talks, History Maps Lore, GeoGlobeFiles.

Channel ids (for checking on the public pages): The Why Side = UCjFTPUCLQucNHkHSTuGxraw; Cini Mini Tamil = UCwcP64M0pMxJTGquwL8El7g; Doodles Fact = UCMtaW-zKVdo0p6n6HDXyQrA; Zidan Construction = UCiYu-Z1h-dfGDwnla98OLRA; ShortsBreak Plus OTT = UCwbCPNrYIDp5L2nXclpkViQ; Under Six Minutes Studio = UCK0qJ9LKfKLqeGE34wi3w3Q; Bot Wars Usa = UC0-dfOw4t5wgyp2TZcJEB-w; 지구또보기 = UCJeT-X5BBHR44wAwrlLNXgg; Hyperbolic AI = UCrS0xtNJz7sKoNoMyWeu3vQ; Behind The Process = UCqzWfyoY0RW5HcPhvuKxr_Q; Income Edge = UCHGdZu_76D-DnGufNmkECdA; One Map, One Battle = UC2IqgiZ84MYrPHPntArYdnQ; Mekii Stories = UCurJAQNt2BqQY-AMphsAUig; PS Rank = UCL_CH9qqRhil-ZQi5PWLcrA; Untold Theory = UCy1FYb3aMUEIkLIurSkNk6A; How Things Were Built = UC6Z9TREvOqKn-22qR8dzooQ; Fact Capture = UC5XOAtJKxxUaT6105JwOkTw; Facts Compass = UC94r11nVa7YlLwqH4P2rQPw; Cleanwith__Marina = UCy4C1waHcMxtri8aHc61ETw; Couple Core = UCanZCEZTzoI1K-bPk2MpL2w; Reconstructed = UCdZhRs4wM7SgVXoP9WSW2yA; Bodycam C4 = UCtoxoIsudLFxMl8HGMHF6wA; redmark. = UC5h1WrC25S7-RCc5yF3YZfQ; Ali Wildlife Hunt = UChY6sPOC2XIvN_thMyB-1Yw; How Things Work = UCKkvTzcxADWP9flCTnOAkAA; Jayansh Insight = UCqXVm5DgKJ56G69e-YwEx2g; CA Yash Aggarwal = UCeyrzInjVuwgW89BCiPLUhQ; Varz Thought = UCuLjPEb5aJQBW8rclUnvlOA; Built Mysteries = UCHAcyBpgz0N5H-Zr9Bfvu6Q; Sasta Animator = UCzOBFJweRnM49kLTNo3L0tw; Curadels = UC3YS9-PBaaXP4J-_cgdgpSw; The History Talks = UC-qyrcT_VvT5YbD6FIPV6tA; Boult Explained = UCHErVodGAQP3cBXFrzPr1Zw; Rural Travel TV = UCRCY_kJZdZUAI4S9IGRAFRQ; Knowledge Universe = UCuyh2tVDYXdX-m-ZC-0nuNQ; History Maps Lore = UCFREyVa1PdzGJLugAZmnfcg; GeoGlobeFiles = UCtIqcPhGbg_qCIbNAn4lA8w; Gyan ka Pitara = UCt2Xa4Ds9TyakHFSVTW0MeQ; MythProcess = UCX0q5V5r8aCN_OzFO81ywfg.

## 2. The video that surfaced each channel (views measured on 29 Oct)

'Surfaced video' = the video that put the channel into the search results (its views were read with `videos.list`). Open any of them at youtube.com/watch?v=<video id>. Titles are as returned by the search, HTML entities decoded, emoji removed, a pipe replaced by a slash, non-English titles glossed in square brackets. 'Share' = this video's views / the channel's total views (over 100% is just the two counters being read at slightly different moments). A high share means a one-hit channel so far.

| Channel | Surfaced in query | Title | Video id | Length | Views | Likes | Share of channel views |
|---|---|---|---|---|---|---|---|
| The Why Side | history | He Put His Head in a Particle Accelerator | fM-_0tJG8Eo | 1:13 | 11,480,070 | 419,519 | 18% |
| The Why Side | engineering | The Truck You Don't Want Behind You | vxnnsMcoCMs | 0:39 | 9,862,589 | 148,605 | 15% |
| The Why Side | engineering | Why This Yellow Box Eats Guardrails | coqlbmfsiO0 | 1:12 | 2,322,336 | 55,792 | 4% |
| Cini Mini Tamil | explained | [Tamil title] Movie Explained in Tamil / Tamil voice over | 7KvEUkJGQ_I | 0:53 | 6,121,216 | 96,720 | 3% |
| Doodles Fact | engineering | How A Hole in your yard can become a nuclear bunker | TLF9znXtSFc | 1:39 | 5,432,083 | 209,999 | 100% |
| Zidan Construction | robot | The Future of Construction: This Robot Plasters Walls Instantly! | Y-wyehrJOiI | 0:18 | 12,690,747 | 73,606 | 78% |
| ShortsBreak Plus OTT | robot, AI | Episode 5 - Sheela Tez Hai / Kaamwali Bai vs AI Robot | CRF4DghebtI | 2:34 | 13,126,069 | 384,230 | 10% |
| Under Six Minutes Studio | engineering | How Engineers Solved the Erasable Pen Problem | jcH6bhMJf2c | 0:35 | 11,173,617 | 115,160 | 8% |
| Bot Wars Usa | robot | Bullets vs Liquid Nitrogen: One Robot Frozen Solid | qUhzgt0dt8o | 0:15 | 5,530,231 | 44,681 | 14% |
| 지구또보기 | engineering | How Heavy Steel Beams Are Shaped | cUE85T4gDLE | 0:08 | 2,933,252 | 3,802 | 2% |
| Hyperbolic AI | AI | The F1 transition that people are calling AI. | yDguQmBiwEw | 0:07 | 16,418,985 | 201,080 | 69% |
| Behind The Process | science facts | [Hindi] 5,700-year-old chewing gum found! | 3HsvJ9oV6Ew | 1:20 | 888,339 | 27,955 | 2% |
| Income Edge | money | His Money, Her Money... Or OURS (#finance #daveramsey #marriage) | jnaqwJis6jg | 0:45 | 3,631,559 | 97,397 | 7% |
| One Map, One Battle | history | How the US Army stopped North Korea | --OgT4BBKnU | 1:19 | 3,388,460 | 55,162 | 37% |
| Mekii Stories | AI | [Hinglish] Jethani Ka Anmol Tohfa / Shazia Ki Zindagi Badal Gayi (#ai) | CVfYRDxYLzo | 2:59 | 2,636,537 | 100,914 | 8% |
| PS Rank | robot | Ranking Funniest Robot Fail | Jf8ysLteLIk | 0:51 | 6,197,279 | 44,785 | 16% |
| Untold Theory | science facts | The Crazy Evolution of cycles | s8MzUmVv-8w | 0:43 | 2,991,232 | n/a (hidden) | 14% |
| Untold Theory | science facts | Evolution of Bulletproof Vests | RLbPLKtvkmY | 0:51 | 1,544,714 | n/a (hidden) | 7% |
| How Things Were Built | how it works | How a Hole in the Ground Becomes a Well | B7QXEVriygE | 1:04 | 197,400 | 2,165 | 5% |
| Fact Capture | explained | 190+ Years Old?! This Turtle Is STILL Alive! | dGr1Di2Gl9Q | 0:32 | 1,119,170 | 37,595 | 5% |
| Facts Compass | engineering | How India Built the World's Tallest Statue / Statue of Unity | nMNLwtTjs34 | 2:35 | 2,158,883 | 48,821 | 8% |
| Cleanwith__Marina | robot | Did this happen to you too? (#vaccum #roombavsmatic #squarerobots) | ippXKNbo5ZY | 0:09 | 14,760,308 | 266,127 | 63% |
| Couple Core | money | He Couldn't Believe What His Dad Did With His Tuition Money #shorts | NdD-rDB1xkE | 0:54 | 3,471,857 | 108,792 | 10% |
| Reconstructed | documentary | What Really Happened Inside the flydubai Cockpit | s7WaBHkgjL0 | 16:26 | 3,276,717 | 43,470 | 63% |
| Bodycam C4 | documentary | Brinks Truck Driver Robs Coworker & Steals $700,000 | aQ43bCkjZoM | 19:06 | 1,522,560 | 8,967 | 16% |
| redmark. | how it works | How Does The Flying Tesla Work? | bUlAqmCDv44 | 1:19 | 33,017 | n/a (hidden) | 1% |
| Ali Wildlife Hunt | documentary | Great Horned Owl Life Cycle: Egg to First Flight / Wildlife Documentary | 0ilC6ccFmgw | 11:07 | 4,953,797 | 5,971 | >=100% |
| How Things Work | how it works | How Drilling Finds Water Underground | QiTdwT9mjpg | 0:30 | 4,184,188 | 51,376 | >=100% |
| Jayansh Insight | documentary | The Famine Britain Ignored - 1876, India's Darkest Chapter / Full Documentary | EH8rYPDqUfM | 16:33 | 4,189,189 | 5,340 | 36% |
| CA Yash Aggarwal | business | How Sourav Joshi & Other Creators and Businessmen Save Taxes | McyC2Ds9uNY | 1:14 | 1,556,765 | 46,811 | 99% |
| Varz Thought | engineering | Can you see the world's smallest drone motor? | BGIVANaYVoY | 0:35 | 3,805,936 | 80,294 | 39% |
| Built Mysteries | engineering, history | San Francisco Built Its Most Famous Park on Sand Dunes. | oK50sybHnIo | 1:17 | 2,187,638 | 99,146 | 22% |
| Sasta Animator | how it works | How submarine works under water | ouDc4Nm4ZoM | 0:51 | 734,265 | n/a (hidden) | 27% |
| Curadels | how it works | How The Flying Tesla Works? | s-ajj6ELDyQ | 0:35 | 114,898 | 1,901 | 4% |
| The History Talks | history | [Hindi] about the world's most beautiful woman / Rajveer Sir / Rajasthan History / Springboard Jaipur | aVa_oE9glSc | 2:30 | 3,122,946 | 57,596 | 28% |
| Boult Explained | explained | How Doctor Strange Made a Dangerous Mistake with Time Magic (#marvel #explained) | y2LaBDr-CT4 | 2:33 | 2,893,897 | n/a (hidden) | 41% |
| Rural Travel TV | documentary | Egypt Village Life / Full Documentary & History in Urdu and Hindi | 59S5LE28cLo | 16:06 | 1,218,633 | n/a (hidden) | 72% |
| Knowledge Universe | science facts | [Hindi] 3D biological truth of a childhood fruit: what does Jungle Jalebi do inside the stomach? | xAfWWdBDBkE | 1:48 | 4,345,946 | 236,537 | 75% |
| History Maps Lore | history | The Tiny Island That Stopped an Empire - Malta 1565 | W1blLBpUeZ8 | 1:25 | 2,273,906 | 40,679 | 98% |
| GeoGlobeFiles | history | Why There Are TWO "Indias" in the World (#facts #maps) | JJlo0lAjQA0 | 1:08 | 1,789,554 | 24,319 | 51% |
| Gyan ka Pitara | science facts | [Hindi] The scary truth of custard-apple seeds (3D Science Animation) | EL3glgV7wN0 | 1:34 | 1,961,593 | 62,254 | 73% |
| MythProcess | science facts | The Bullet-Proof Glass (AK-47 fails too) #shorts #science | wdNGAuw1fc4 | 0:45 | 1,798,519 | 40,553 | >=100% |

## 3. The five most replicable proven concepts for our engine, ranked by evidence

Our engine: a real clip (only the maker's own publicity footage, 5 s or less a shot, credited) or our own drawings, plus our own animated diagrams, an AI narrator voice, ~30 s Shorts, 1-2 a day, no copying, no mass-produced templates. Ranked by the combined views/day of the kept channels that share the concept, which rewards both more channels and faster channels (the channel count is shown next to it). 'Combined' is the sum of the channels' lifetime views/day. 'Median' is per channel. Channels are counted once; concept 2 holds three channels whose formats are 'no' because the topic, not the format, is the signal.

| Rank | Concept | Kept channels | Their combined views/day | Median channel views/day | Median uploads/day | Median subs per 1k views | Engine | Closest channel of ours |
|---|---|---|---|---|---|---|---|---|
| 1 | Mechanism and 'why does this exist' Shorts, 30-70 s | 7 (230,679,291 views together) | 3,386,217 | 99,183 | 0.61 | 0.51 | yes | The Curve |
| 2 | Robots and machines doing a job, 8-18 s clips with a one-line promise (a topic signal more than a format) | 4 (119,534,972 views together) | 2,402,313 | 568,194 | 0.90 | 0.54 | partly | The Curve |
| 3 | 'How it is built' cross-sections, 45-100 s | 4 (46,288,149 views together) | 1,710,168 | 272,699 | 0.97 | 2.26 | yes, with our own look and subjects | The Curve (cars, space, tech builds); Curva Explica as a Spanish re-render |
| 4 | Fast facts, 'evolution of' lists and 'what happens inside' science animations, 30-110 s, one picture per beat | 6 (113,452,618 views together) | 1,136,725 | 150,959 | 1.01 | 4.03 | partly | Curva Explica or a Curve B slot |
| 5 | Map-led history and geography Shorts, 60-90 s | 3 (14,954,243 views together) | 479,244 | 40,155 | 0.94 | 1.03 | yes | none today; nearest are Money Crimes (heist routes) or How They Profit (supply chains) |

**1. Mechanism and 'why does this exist' Shorts.** Channels: The Why Side, Under Six Minutes Studio, How Things Work, Sasta Animator, Varz Thought, Curadels, redmark..

| Item | Detail |
|---|---|
| Best measured Shorts | 35 s 'How Engineers Solved the Erasable Pen Problem' 11.2M views; 39 s 'The Truck You Don't Want Behind You' 9.9M; 1 min 13 s 'He Put His Head in a Particle Accelerator' 11.5M; 30 s 'How Drilling Finds Water Underground' 4.2M; 35 s 'smallest drone motor' 3.8M |
| What we would make | 'How engineers solved [one real design problem]' in 30-40 s: one object, our own animated cross-section, one number on screen, one payoff line. No third-party clip needed. |
| Why it fits | It is The Curve's own lane and the only lane where we already have views (Microduck 18,084). Four of the five measured hero Shorts are 30-39 s, our length. |
| Watch-out | Topical piggy-backing is low-yield: five channels made 'how the flying Tesla works' in October (Curadels, redmark., ExplainTheLeap, Inside Decoded, Self made engineer); the two I measured got 114,898 and 33,017 views. |

**2. Robots and machines doing a job.** Channels: Zidan Construction, Bot Wars Usa, PS Rank, Cleanwith__Marina. Outside the date filter: Knownasdex (created 27 Apr 2026, 266.1M views, 273k subs).

| Item | Detail |
|---|---|
| Best measured Shorts | 18 s 'The Future of Construction: This Robot Plasters Walls Instantly!' 12.7M views; 9 s robot-vacuum meme 14.8M; 15 s 'Bullets vs Liquid Nitrogen: One Robot Frozen Solid' 5.5M; 51 s 'Ranking Funniest Robot Fail' 6.2M |
| What we would make | 'This robot does [one job]; here is how it works' in ~30 s: the maker's own publicity footage (5 s or less a shot, credited) plus our diagram of the mechanism and one real number. |
| Honest read | Robots draw views, which backs The Curve's topic. The four winners are four different formats (raw clip, AI spectacle, home skit, ranking compilation), all 9-51 s with little or no explanation, and none is a format we can copy. Treat this as a topic signal, not a template. |

**3. 'How it is built' cross-sections.** Kept: How Things Were Built, Doodles Fact, Built Mysteries, Facts Compass. Outside the date filter: You Made It, two channels with the same name (created 27 Feb and 21 Mar 2026), 63.0M views from 11 videos; all three sampled heroes are exactly 1 min 11 s and have 8.5M-16.8M views each.

| Item | Detail |
|---|---|
| Best measured Shorts | 1 min 39 s 'How A Hole in your yard can become a nuclear bunker' 5.4M views and 210k likes in 5 days; outside the filter 'How a Ditch in a Field Becomes a Trench' 16.8M |
| What we would make | 'How a [rocket catch tower, gigacasting machine, battery pack] is built' in 45-60 s: our own cross-section animation, the build in 5-6 steps, a cost or time figure at the end. Different subjects and a different look from the clones. |
| Watch-out | It is being cloned: the same title sits on Doodles Fact (24 Oct) and digs (25 Oct), and six channels (counting the two You Made It channels) used 'How a Hole/Ditch... Becomes a...' titles in the second half of October. How Things Were Built uploaded 91 videos in 14 days (6.5 a day). Copying the wording or the cadence would trip the inauthentic-content rules. Evidence for the cross-section style itself is thinnest: only How Things Were Built and Doodles Fact (plus the two You Made It channels outside the filter) use the 'hole becomes' wording; Built Mysteries and Facts Compass are build stories whose visuals I did not inspect. |

**4. Fast facts, 'evolution of' and science animations.** Channels: Fact Capture, Untold Theory, Behind The Process, Knowledge Universe, Gyan ka Pitara, MythProcess. Outside the date filter: Heavenly Palace (Spanish titles, engineering and science facts), created 5 Apr 2026, 49.4M views, 58.7k subs.

| Item | Detail |
|---|---|
| Best measured Shorts | 1 min 48 s Hindi 3D science animation 4.3M views and 236,537 likes; 43 s 'The Crazy Evolution of cycles' 3.0M; 32 s turtle fact 1.1M |
| What we would make | 'Evolution of [phones, cars, rockets]' or 'seven facts about [one machine]' in 40-50 s, one of our drawings per beat. This is my adaptation of the proven format and it is untested. |
| Why it matters | Best subscriber conversion in the whole table: Fact Capture 15.52 subs per 1,000 views (345,000 subs in 85 days), Knowledge Universe 8.92, Gyan ka Pitara 6.11, against 0.14-1.21 for the concept-1 channels. Subscribers are what unlock monetisation. |
| Watch-out | The Hindi channels cannot be copied (language) and I could not see whether the others use stock footage or generated pictures. |

**5. Map-led history and geography.** Channels: One Map, One Battle, History Maps Lore, GeoGlobeFiles. Outside the date filter: MapLore (created 9 Apr 2026, 132.4M views, 95k subs, 62 videos).

| Item | Detail |
|---|---|
| Best measured Shorts | 1 min 19 s 'How the US Army stopped North Korea' 3.4M views; 1 min 25 s 'The Tiny Island That Stopped an Empire - Malta 1565' 2.3M (3 videos in total) |
| What we would make | 'One map, one story': an animated map of a heist route, a trade route or a supply chain with the money flow, 60-90 s. The proven niche is military history; moving it to money maps is my adaptation and untested. |
| Watch-out | A new niche for us, so it means re-pointing a 0-subscriber channel or starting a new one. History needs the same sourced-facts discipline as our films. |

### Do these concepts beat the niches of our dead channels? Plain answer

On this sample, yes. Concepts 1, 3, 4 and 5 each have kept channels in a format we can make; the three dead niches have none. The sample is English, US-ranked and short on money and Spanish content, so absence here is a blind spot, not proof the niche cannot work.

| Dead channel (our numbers, 28 Oct) | Its niche | What this scan found |
|---|---|---|
| How They Profit (183 views, 0 subs) | business models | No animated business-model explainer created since 1 May cleared the filter. The 'business' query returned mostly Indian business-story Shorts from older channels (Therichtalkk, created 29 Jan 2025, 135.9M views, 258k subs; Basic Paradox, 2020, 120.4M; Harsh Explain, 2022, 69.5M) plus one new tax talking head (CA Yash Aggarwal); the 'money' query returned skits and clip commentary. The nearest new-in-2026 evidence is a near-miss: Money talks by Financially Free (created 18 Jan 2026, 122.3M views, 164k subs, Indian, story-led). So business-story Shorts have an audience, but nothing started since May cleared the filter in our format. Concepts 1, 3, 4 and 5 beat it on evidence. |
| Money Crimes (116 views, 0 subs) | scams and heists | Only Bodycam C4 (9.5M views, 14 videos, 19-min police-bodycam footage) and Reconstructed (5.2M views, 16-min animated aviation incident) are new since May, and neither is our format. True crime has big audiences on older channels (EWU Crime Storytime, created 2021, 581.7M views; Wronged, 2023, 500.1M), so the genre is not dead, but no 30 s heist or scam explainer showed up. Concepts 1, 3, 4 and 5 beat it on evidence. |
| Curva Explica (3 views, 0 subs) | Spanish tech | No Spanish-language channel created since 1 May cleared the filter. One near-miss: Heavenly Palace (Spanish titles, engineering and science facts, created 5 Apr 2026, 49.4M views, 58.7k subs). The queries were English, so Spanish was barely sampled. The only Spanish evidence sits closest to concept 4 (engineering and science facts); nothing here tests concepts 1 or 3 in Spanish. |

## 4. Not for us

| Format | Channels (lifetime views) | Why not |
|---|---|---|
| AI story and skit serials | ShortsBreak Plus OTT (130,513,105), Mekii Stories (31,306,442), Couple Core (36,264,896), Hyperbolic AI (23,827,126) | Mass-produced AI or scripted skits; no diagrams, no sourced facts; the inauthentic-content rules target exactly this. Couple Core, Shadow Gainz (created 2024) and Rivenor (created 2015) all have the same 'dad spent the tuition money' premise, judging by their titles. |
| Film and TV recaps on film clips | Cini Mini Tamil (176,666,550), Boult Explained (7,069,911) | Copyrighted clips; we only use a maker's own publicity footage. |
| Reuploaded process loops | 지구또보기 (128,441,003) | 8 s loops at 3.1 uploads a day, probably other people's footage; 0.20 subs per 1,000 views. |
| Clip commentary or lectures built on a real person | Income Edge (55,177,911), The History Talks (11,262,059) | A real person's clips or likeness; Income Edge converts only 0.11 subs per 1,000 views (inferred from the #daveramsey tag). |
| Talking head | CA Yash Aggarwal (1,570,059) | A real person on camera. |
| Third-party clip rankings | PS Rank (39,575,730) | Other people's robot-fail clips ranked; copyright and no authorship. |
| AI robot spectacle | Bot Wars Usa (40,383,683) | Generated-looking 15 s clips with no explanation (inferred); 17 videos, 2.4M views each on average, so the demand is real but the format is AI spectacle. |
| Person-on-camera humour | Cleanwith__Marina (23,388,308) | A person on camera, a skit about a robot vacuum; not our format. |
| Long-form footage (11-19 min) | Bodycam C4 (9,463,132), Rural Travel TV (1,694,995), Ali Wildlife Hunt (4,871,807), Jayansh Insight (11,709,262) | Not Shorts; third-party footage, archival images or real people (bodycam). |

| Other flags | Detail |
|---|---|
| Kids content | None of the 39 kept channels is a kids channel. |
| Mass production | Lifetime uploads per day: How Things Were Built 6.50, 지구또보기 3.14, Zidan Construction 2.69, One Map, One Battle 2.09, ShortsBreak Plus OTT 2.05. Even where the topic is fine, copying that cadence would look mass-produced; our 1-2 a day sits at the low end. |
| Real people | Income Edge (Dave Ramsey tag, inferred), The History Talks (a named teacher, inferred), Bodycam C4 (arrested people), CA Yash Aggarwal (talking head). |
| Reconstructed (not in the table above) | Long-form animated incident reconstruction, 16 min, 28 videos, 5.2M views, 4.06 subs per 1,000 views. Its own-animation style fits our drawings, but it is long-form and about named real people, so I marked it 'partly' and left it out of the five concepts. |
| Combined weight | The 'no' channels are 17 of the 39 kept channels and 733,185,979 of the 1,159,974,039 lifetime views; the views are real but they sit in formats we cannot or should not copy. |

## 5. Created 1 Jan-30 Apr 2026 (fails the date filter only, context only)

These cleared a threshold but were created before 1 May, so they are not in the ranking or the concept counts. They show the same concepts working earlier in 2026.

| Channel | Created | Age (d) | Subs | Total views | Videos | Views/day | Relevance |
|---|---|---|---|---|---|---|---|
| Knownasdex | 2026-04-27 | 185 | 273,000 | 266,143,009 | 61 | 1,438,611 | concept 2 (robot rankings); created 4 days before the cutoff |
| Kam Ki Bat Studio | 2026-04-05 | 207 | 254,000 | 189,554,494 | 48 | 915,722 | 'how a product is made' (Indian currency note); n/a on format |
| Xfacto | 2026-02-07 | 264 | 178,000 | 212,239,071 | 260 | 803,936 | facts, Tamil |
| MapLore | 2026-04-09 | 203 | 95,000 | 132,402,390 | 62 | 652,229 | concept 5 (map history) |
| Money talks by Financially Free | 2026-01-18 | 284 | 164,000 | 122,279,274 | 180 | 430,561 | business stories, Indian; nearest to How They Profit |
| Fact Mine 3D | 2026-04-16 | 196 | 46,000 | 74,502,495 | 134 | 380,115 | concept 1 and 3 (3D explainers); sampled hero only 514,114 views |
| 3D_Spectra_YT | 2026-02-23 | 248 | 62,200 | 69,527,660 | 156 | 280,353 | concept 1 (3D engineering explainer, 2 min 6 s hero 5.2M) |
| Explaining Medicals | 2026-03-26 | 217 | 27,900 | 60,221,031 | 198 | 277,516 | medical explainers, Indian |
| Heavenly Palace | 2026-04-05 | 207 | 58,700 | 49,376,586 | 236 | 238,534 | concept 4 and Curva Explica (Spanish engineering facts) |
| You Made It (id ...Rg-9w) | 2026-03-21 | 222 | 70,900 | 46,326,100 | 7 | 208,676 | concept 3; hero 1 min 11 s 14.7M views |
| Fresh Point | 2026-02-09 | 262 | 94,700 | 50,684,065 | 399 | 193,451 | n/a |
| Atharv Explains Why | 2026-04-19 | 193 | 171,000 | 37,054,045 | 69 | 191,990 | n/a |
| Deals Editx | 2026-04-04 | 208 | 5,710 | 23,654,165 | 7 | 113,722 | business clips, 7 videos |
| History Snap92 | 2026-03-31 | 212 | 3,890 | 20,808,439 | 206 | 98,153 | history facts |
| ARCHIV \| HUMAN HISTORY | 2026-01-12 | 290 | 5,450 | 20,860,561 | 225 | 71,933 | history facts |
| You Made It (id ...CCehA) | 2026-02-27 | 244 | 17,600 | 16,664,933 | 4 | 68,299 | concept 3; same name as the other You Made It |
| Wait, Really!? | 2026-01-17 | 285 | 18,700 | 14,882,379 | 17 | 52,219 | concept 3 (Indonesian building-engineering Short, 1 min 14 s, 5.0M) |
| FactGyanix | 2026-01-09 | 293 | 4,070 | 11,292,494 | 108 | 38,541 | facts, Hindi |
| Schematik | 2026-04-03 | 209 | 17,600 | 6,125,451 | 175 | 29,308 | concept 1 (electronics explainers); sampled hero 230,370 views |
| NOBITA 2.0 | 2026-01-15 | 287 | 5,960 | 4,602,402 | 111 | 16,036 | n/a |
| The Curious Mind | 2026-01-01 | 301 | 11,900 | 2,598,060 | 89 | 8,631 | n/a |

Measured hero Shorts of some of these (not in the ranking):

| Channel | Title | Video id | Length | Views | Likes |
|---|---|---|---|---|---|
| You Made It (...Rg-9w) | How a Jungle Hole Becomes the Cu Chi Tunnels | 7J2V-np5Bks | 1:11 | 14,725,505 | 421,528 |
| You Made It (...Rg-9w) | How a Hole in Your Yard Becomes a Basement | 69L18XqgIqc | 1:11 | 8,536,169 | 260,633 |
| You Made It (...CCehA) | How a Ditch in a Field Becomes a Trench | 6SDuStkFbrE | 1:11 | 16,823,573 | 388,626 |
| Knownasdex | Ranking Funniest Robot Moments | UMntAhPsMJI | 0:42 | 9,135,563 | 62,034 |
| 3D_Spectra_YT | How Engineers Invented a Transmission With No Fixed Gears | WH3qkdl5zNE | 2:06 | 5,202,472 | 126,065 |
| Wait, Really!? | [Indonesian] What keeps buildings standing for hundreds of years (#engineering) | rO77CndxeRc | 1:14 | 4,987,610 | 75,758 |
| Fact Mine 3D | How Does a Diesel Hammer Drive Steel Piles? | TFXWm-54rj8 | 2:27 | 514,114 | n/a |
| Schematik | What is a DHT Sensor and How does it work? | laNADtV7XSQ | 1:09 | 230,370 | 6,235 |

Created on or after 1 May 2026 but under both thresholds (not kept): Engine sim (2026-10-03, 713,690 views, 1,120 subs, 24 videos); ExplainTheLeap (2026-10-08, 12,169 views, 18 subs, 23 videos); Brain And Mind (2026-09-28, 977,207 views, 5,600 subs, 96 videos); Maze Docs (2026-07-20, 967,081 views, 3,390 subs, 9 videos); Travel Nama 2.0 (2026-08-16, 690,276 views, 777 subs, 5 videos).

## 6. Limits of this method

| Limit | What it means |
|---|---|
| Search ranking | `search.list` with `order=viewCount` returns at most 50 results per query, with no deeper pages in this budget, and its ordering is approximate. A channel only shows up if one of its videos published on or after 1 Oct 2026 made the top 50 for one of the 10 queries. Channels that broke out in May-Aug and have since slowed are largely invisible. |
| Region and language | `regionCode=US` and `relevanceLanguage=en` bias the ranking but do not filter the audience. Many hits are Indian, Pakistani or Indonesian. The sample is not a US-only picture, and Spanish is barely sampled. |
| Queries | Ten topics only. Cars, space, tech news, satisfying, quiz, kids, sports and Spanish queries were not run, so The Curve's cars and space lanes and Curva Explica's market are under-sampled. The 'money' query returned mostly skits and clip commentary; the 'business' query mostly Indian business-story Shorts from older channels. |
| 'Short' filter | `videoDuration=short` means under 4 minutes, not 60 seconds. Several hero videos are 1 min 30 s to 3 min. The 'documentary' query used `medium` (4-20 min), so those five channels are long-form, not Shorts. |
| Coverage of the lookup | About 410 channel ids surfaced; 250 were looked up (5 calls x 50). About 42 big established brands (news, studios, corporates) and about 120 small channels judged low-fit (regional-language skits, trailers, local-business vlogs, gaming) were skipped. The last, lowest-priority batch still produced 5 kept channels out of 50, so the skipped tail probably holds a few more breakouts, mostly in formats we would not copy. |
| Lifetime averages | Views/day is lifetime views over age, not recent velocity; I had no analytics access to other people's channels. A channel with one viral video looks better than it is: Doodles Fact, Ali Wildlife Hunt, How Things Work, CA Yash Aggarwal, History Maps Lore, MythProcess get 95% or more of their views from the surfaced video. |
| Counters | Subscriber counts are rounded by YouTube to three significant figures. Channel and video counters were read minutes apart, so a video can exceed its channel total by a small amount. Views can be inflated or botted; I cannot tell. |
| Age | The API's channel `publishedAt` is the channel creation date, not the first upload or the first hit. |
| Classification | By name, titles, lengths and country only. Nothing was watched or listened to, so 'AI-generated', 'reuploaded' and 'animated' are inferences. The next step is to open the top few channels in each concept and check the visuals and the audio before any build. |
| Budget choice | The 16th call went on `videos.list` (views and length of 50 surfaced videos) instead of a sixth channel batch, because hero views and lengths say more about the five concepts than 50 more low-priority channels. |

Raw numbers were read on 29 Oct 2026 and will have moved. Re-read any channel on its public page before using it as evidence.
