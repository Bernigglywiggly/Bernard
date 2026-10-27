# Motorcycle on water: facts for the Short "Motorcycle on Water: Why It Didn't Sink" (Wed 28 Oct)

Checked Tue 27 Oct 2026, 03:35-03:50 UK (GMT), by account C. Radar pick: `RADAR_2026-10-26.md` §1 #3 and §4(a) #2.
Row numbers are what the script's `facts=` fields point at. Anything not in this file does not go on screen or in the voice.

**How this was checked (read this first):** this cloud session's network blocks direct page reads (publishers, YouTube, RSS),
so every row comes from search-engine extracts of the pages listed, not from the page itself. The one exception is S2, read
from source code. Status: **V** = two or more independent outlets agree in those extracts (Xinhua copies count once).
**U** = one outlet, or only the team making the claim. **OUR MATHS** = our arithmetic on sourced inputs: label it on screen.
**Quotes:** the wording is as the extracts give it. Open the page and copy the words before any quote goes on screen.

## Sources

The record
- **R1** Xinhua (English), 25 Oct 2026, "China's Zhang Xue sets new Guinness World Record with motorcycle on water".
  https://english.news.cn/20261025/c82eb3ff563f45c9afcb374d35790f23/c.html (copied by The Star, China.org.cn, Beijing Review, The Peninsula)
- **R2** China Daily, 25 Oct 2026. http://global.chinadaily.com.cn/a/202610/25/WS6ade05dfe4b06d4aa0564ac2.html and
  https://www.chinadaily.com.cn/a/202610/25/WS6addd674e4b06d4aa0564a8b_2.html
- **R3** CGTN, 25 Oct 2026, with a 0:31 video report. https://news.cgtn.com/news/2026-10-25/China-s-Zhang-Xue-sets-Guinness-World-Record-for-longest-ride-on-water-1Rx61irCDZu/p.html
- **R4** Yahoo News, "From four fails to Guinness World Record: ZXMOTO founder rides 25.3 miles on open water".
  https://www.yahoo.com/news/world/articles/four-fails-guinness-world-record-071956657.html
- **R5** UPI, 26 Oct 2026. https://www.upi.com/Odd_News/2026/10/26/guinness-world-records-motorcycle-water/9111793033790/
- **R6** Interesting Engineering. https://interestingengineering.com/transportation/motorcycle-skims-across-water-record
- **R7** IT之家 (ITHome), 25 Oct 2026. https://www.ithome.com/1/017/564.htm · Guangming Daily, 25 Oct: https://m.gmw.cn/2026-10/25/content_1304579090.htm
- **R8** Sina, ZXMOTO's head of R&D Deng Liansong (邓连松) on the two bikes, the boards, the paddle wheel and the sprocket:
  https://www.sina.cn/weibo/detail/5357535607391102.html and https://www.sina.cn/weibo/detail/5357927582140804.html
- **R9** Sina, the 2009 attempt on CCTV: https://www.sina.cn/weibo/detail/5358202460047839.html and https://www.sina.cn/gc/article/niwkmrm3728128.html
- **R10** Sina, the record's rules as reported: https://k.sina.com.cn/article_7879995911_1d5af320706802wkh2.html and
  https://k.sina.com.cn/article_7879995911_1d5af320706802wiyc.html
- **R11** Sina, Zhang on a possible road-and-water model: https://k.sina.com.cn/article_7879995911_1d5af320706802wmra.html
- **R12** Baidu Baike, the record's entry: https://baike.baidu.com/item/%E6%94%B9%E8%A3%85%E6%91%A9%E6%89%98%E8%BD%A6%E5%9C%A8%E5%BC%80%E9%98%94%E6%B0%B4%E5%9F%9F%E8%A1%8C%E9%A9%B6%E6%9C%80%E8%BF%9C%E8%B7%9D%E7%A6%BB/69484150
- **Z1** Wikipedia, Zhang Xue (entrepreneur). https://en.wikipedia.org/wiki/Zhang_Xue_(entrepreneur) · **Z2** Wikipedia, ZXMOTO: https://en.wikipedia.org/wiki/ZXMOTO ·
  Visordown, "New brand started by Kove founder makes European debut": https://www.visordown.com/features/zxmoto-makes-its-european-debut ·
  Sixth Tone: https://www.sixthtone.com/news/1018369

Earlier rides on water
- **M1** MythBusters, "Motorcycle Water Ski" (season 12, aired June 2013). https://mythresults.com/motorcycle-water-ski ·
  https://www.pogdesign.co.uk/cat/MythBusters/Season-12/Episode-6
- **M2** Robbie Maddison, "Pipe Dream", Tahiti (2015). Rolling Stone: https://www.rollingstone.com/culture/culture-sports/robbie-maddison-on-cheating-death-to-make-his-pipe-dream-a-reality-54328 ·
  IOL: https://www.iol.co.za/motoring/bikes/surfing-tahiti-on-a-motorcycle-1894707
- **M3** Robbie Maddison across the Bosphorus (2021). https://www.rideapart.com/news/530055/robbie-maddison-istanbul-world-record/ ·
  https://www.ulladullatimes.com.au/story/7407970/robbie-revs-his-way-to-another-world-record-ride-in-istanbul
- **M4** Luca Colombo across Lake Como (2017). https://www.visordown.com/features/general/italian-nutter-sets-world-lake-riding-record ·
  https://www.snopes.com/fact-check/daredevil-ride-motorcycle-lake-como/

Physics
- **S1** NASA Glenn Research Center, Beginner's Guide to Aeronautics, "The Lift Equation". https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/lift-equation/
- **S2** Savitsky, D. (1964), "Hydrodynamic Design of Planing Hulls", *Marine Technology* 1(1), 71-94: the standard planing-lift
  equations, **read in code** in OpenPlaning 0.4.9 (https://pypi.org/project/openplaning), `openplaning.py` lines 503-510:
  `F_z = C_Lbeta * 0.5 * rho * U**2 * b**2`, with `C_L0 = tau**1.1 * (0.012 * lambda_W**0.5 + 0.0055 * lambda_W**2.5 / Fn_B**2)`
  (U = speed, b = width of the planing surface, tau = its angle to the water in degrees, lambda_W = wetted length / width).
- **S3** Clanet, Hersen & Bocquet (2004), "Secrets of successful stone-skipping", *Nature* 427, 29. https://www.nature.com/articles/427029a
- **S4** Barefoot water skiing speed rule. https://en.wikipedia.org/wiki/Barefoot_skiing · Zenon Bilas (7-time US champion), barefoot.org, 2015:
  https://barefoot.org/2015/04/14/what-a-feet-follow-this-bevy-of-tips-to-get-yourself-barefooting-this-summer-by-zenon-bilas/

## 1. The record

| # | Fact | Words in the source | Source | Status |
|---|---|---|---|---|
| 1 | Zhang Xue, founder of ZXMOTO, rode a modified motorcycle 40.74 km across open water | "40.74 kilometres across open water" | R1, R2, R3, R5 | V |
| 2 | Date: Sunday 25 Oct 2026 | | R1, R2, R3 | V |
| 3 | Place: a river in his home county, Mayang Miao Autonomous County, Huaihua, Hunan, China. Chinese reports name it the Jinjiang (锦江); UPI calls it the Chen River. OpenStreetMap files the Chen River (辰水) under the Jinjiang, so both names likely mean the same water. **On screen: "MAYANG, HUNAN, CHINA"** | | R1, R5, R7, R12 | V (place); river name U |
| 4 | The Guinness title, in the Chinese reports: 改装摩托车在开阔水域行驶最远距离 ("farthest distance on open water by a modified motorcycle", our translation). English wording varies by outlet | | R7, R12 | V (Chinese wording) |
| 5 | Previous record: 31.8 km. **No source names who set it** | "The previous record was 31.8 kilometers." | R1, R4, R5, R7 | V (number); holder unknown |
| 6 | Checked on site by Guinness: GPS tracking, timing data and video; adjudicator Xiong Wen confirmed it on the spot | | R1, R4, R6 | V |
| 7 | Time: set off at 11 a.m., finished shortly after 11:30 a.m. (local, UTC+8): about 32 minutes | "about 32 minutes" | R4, R12, R8 | V |
| 8 | Course: back-and-forth runs along the river, eight sections and seven turns | "eight sections and seven turns" | R4/R6 (one report) | U |
| 9 | Rules as reported: one rider, continuous riding on open water; stopping or going under ends the attempt | | R10 | U (news reading of the rules; Guinness page not found) |
| 10 | Rescue boats and medical teams on standby throughout | | R4/R6 | U |
| 11 | He said he held back on speed to finish safely | "purposely held back on speed" | R4 | U (one outlet) |
| 12 | Afterwards he gave the certificate and the bike to his home county | | R8/R9 family (Sina) | U |

## 2. The bike: what was changed

| # | Fact | Words in the source | Source | Status |
|---|---|---|---|---|
| 20 | Base: a ZXMOTO MX450 (450 cc motocross bike) with its standard frame and powertrain | "retained a standard motorcycle frame and powertrain" | R4, R6 | V |
| 21 | Added: a ski system underneath, a bigger fuel tank, waterproofing of key parts incl. intake and exhaust | "amphibious skis, an enlarged fuel tank and additional waterproofing" | R1, R4, R6 | V |
| 22 | **Thrust:** a paddle-style rear wheel with enlarged paddles pushes water backward | "pushing water backward" | R4, R8 | V |
| 23 | **Steering:** the front ski works as a rudder | "the front ski acted as a rudder" | R4 | U |
| 24 | Steel boards welded at the front and rear wheels give lift and balance (Deng: 钢制桨板提供浮力与平衡) | | R8 | U (team, one report) |
| 25 | Two record bikes were built: one with wide boards, one with narrow boards | | R8 | U (team) |
| 26 | The boards got narrower over the versions: less lift, but quicker to turn (Deng) | | R8 (English outlets say "to improve both lift and steering": R4) | U |
| 27 | A 50-plus-tooth rear sprocket: more pulling force, less top speed | | R8 | U (team) |
| 28 | Six versions; about five months of work on lift, sealing and power | "five months" | R4, R8 | U |
| 29 | The team claims the narrow-board bike reaches about 90 km/h | | R8 | U (team claim, untested) |
| 30 | The MX450 is not on retail sale yet (prototype plus record modifications) | | R8 family | U |
| 31 | Zhang: maybe a road-and-water version one day, **no production plan or date** | | R11 | U |
| 32 | The bike's weight, the boards' size and the rider's weight: **not published anywhere we found** | | our check | V (absence) |

## 3. The man and the 2009 attempt

| # | Fact | Words in the source | Source | Status |
|---|---|---|---|---|
| 40 | Zhang Xue, born 1987 (39 at the record) | | Z1; Sina headline "39 岁张雪" | V |
| 41 | Co-founded Kove Moto in 2017, left in March 2024, founded ZXMOTO in Chongqing in April 2024 | | Z1, Visordown | V |
| 42 | ZXMOTO's 820RR won races in the 2026 **World Supersport** championship (Valentin Debise, a double at Portimão). Not World Superbike: one Xinhua copy says WSBK, which is wrong | | Z1, Z2, Sixth Tone | V |
| 43 | **2009:** aged 22, on CCTV's programme 人与社会 ("People and Society"), in Wuyi county, Zhejiang; target 26 m; four tries, every one ended in the water; best 20 m | (China Daily, paraphrased in the extract: all four attempts ended in the water, best 20 m) | R2 (four falls, 20 m); R9 (CCTV, Wuyi, 26 m target) | V (four falls, 20 m); rest U |
| 44 | 2009 kit: a 500-yuan motorbike and home-made sheet-iron boards, launched off a ramp built in the river | | R9 | U |
| 45 | What he told the camera in 2009 (Chinese reports): 就算我这次没成功，我也还会继续做，总有一次我会成功 ("even if I don't make it this time, I'll keep going; one day I'll make it") | | R9 | U |
| 46 | Quoted by Xinhua around the record: "I have strong faith that I can make it happen" and "Even if I fail, I will pursue it without hesitation" | as quoted | R1 (and copies) | U until read on the page |
| 47 | Some reposts place an earlier try in 2006 or 2007, one claims 100 m in 2009: these conflict with China Daily's 20 m. **Use 2009 and 20 m only** | | Sina reposts | U (conflicting) |

## 4. Earlier motorcycles on water (it's been done before, never this far)

| # | Fact | Source | Status |
|---|---|---|---|
| 50 | MythBusters, 2013: "confirmed". A rig held a wheel against the water off a speedboat and got it skimming at 60 mph (97 km/h). Supercross rider Eric McCrummen crossed 50 ft, then 100 ft, of water. A bike left to coast sank after about 300 ft (91 m): it was riding on momentum | M1 | U (fan episode guides; episode not watched) |
| 51 | Robbie Maddison, 2015, Tahiti (Teahupo'o and Papara): a KTM 250 SX with custom skis (skegs underneath as rudders) and a paddle rear tyre, launched from a barge to reach skimming speed. He said a wave travels at only about 15 mph, a speed that would normally sink the bike | M2 | V |
| 52 | Maddison's prototypes: six bikes, each sunk and rebuilt about 10 times; 5-7 hours to clear the sea water each time | M2 (Rolling Stone) | U |
| 53 | Luca Colombo, 2017: a modified Suzuki 450 across Lake Como, about 5.6 km in about five minutes (~75 km/h), skis around both wheels and rubber blades on the rear tyre | M4 | V (two outlets) |
| 54 | Maddison, 2021: across the Bosphorus, Europe to Asia, about 70 km/h, about 90 s each way | M3 | U |

## 5. Physics for the diagram

### Sourced inputs

| # | Fact | Words in the source | Source | Status |
|---|---|---|---|---|
| 60 | Lift = lift coefficient x density x half the speed squared x area | "Cl times the density rho times half of the velocity V squared times the wing area A" | S1 | V |
| 61 | NASA names "density times the square of the velocity divided by two" the dynamic pressure | | S1 | V |
| 62 | The planing equations boats are designed with use the same speed-squared term: lift = C_L x ½ x density x speed² x (board width)² | `F_z = C_Lbeta * 0.5 * rho * U**2 * b**2` | S2 (code) | V |
| 63 | C_L grows with the board's angle to the water (tau^1.1) and with how much of the board is wet (lambda) | `C_L0 = tau**1.1 * (0.012*lambda_W**0.5 + ...)` | S2 (code) | V |
| 64 | Skipping stones: about 20° between stone and water gives the most bounces | (abstract, paraphrased in the extract) | S3 | V |
| 65 | Barefoot skiers need roughly (weight in lb ÷ 10) + 20 mph, usually 30-45 mph; on shoe skis about 18 mph is enough, because the bigger surface gives more lift | | S4 (Wikipedia + Bilas) | V (rule of thumb) |
| 66 | Thrust: the paddle wheel throws water backward, so the water pushes the bike forward (Newton's third law) | | R4, R8 | V |

### OUR MATHS (show as estimates)

| # | Sum | Result |
|---|---|---|
| 70 | Average speed: 40.74 km in about 32 min = 40.74 / (32/60) | **about 76 km/h (47 mph)**, average. R4 gives the same |
| 71 | Against the old record: 40.74 / 31.8 | **28% further** (8.94 km) |
| 72 | Against 2009: 40,740 m / 20 m | **about 2,000 times further** |
| 73 | Speed squared (rows 60, 62), same board, same angle, same wet area: half the speed = (1/2)² | **a quarter of the lift** |
| 74 | Maddison's 15 mph (24 km/h) wave against Zhang's 76 km/h average: (24/76)² | **about a tenth of the lift.** That's why a wave speed sinks the bike (row 51) |
| 75 | To carry the same weight at half the speed, the board needs 4x the area (2x the width, row 62) | why wide boards are easier and narrow ones need more speed (rows 26, 65) |

**What happens as it slows (the chain, rows in brackets):** lift falls with the square of speed (60, 62). The board sinks deeper
and tilts up, which buys a little lift back (63), until the wet area turns into drag faster than it adds lift. A motorcycle has
almost no buoyancy of its own, so below that point it goes under: MythBusters' coasting bike (50), Maddison's wave speed (51),
Zhang's four falls in 2009 (43). The exact sinking speed of this bike is **not published**: never give one on screen.

### The chain, for the Blender diagram

1. Side view: the boards meet the water at a shallow angle, like a skipping stone (64). Pressure arrows under the board, sized
   with speed squared (60, 62, 73).
2. The paddle wheel throws a jet of water back; a thrust arrow points forward (22, 66).
3. Slow the bike: the arrows shrink to a quarter at half speed (73), the board digs in (63), the bike settles and goes under.
4. Board width: wide = more lift at low speed, narrow = needs more speed but turns quicker (26, 65, 75).

## 6. Footage and rights (decide before cutting)

| # | Clip | Owner | Use |
|---|---|---|---|
| 80 | Xinhua / New China TV video of the ride (YouTube Shorts https://www.youtube.com/shorts/c6Vh_VP-Ys4, owner not confirmed) | Xinhua | ≤5 s per shot, credited on screen, as commentary. Claim risk: state media do claim |
| 80b | **Checked 27 Oct ~13:30 (C, Mac, yt-dlp metadata only, nothing downloaded):** the Short in row 80 is **CGTN Europe's** ("China's Zhang Xue sets Guinness World Record by riding motorcycle on water", 44 s, uploaded 25 Oct, 24.7k views), not Xinhua's. Biggest YouTube uploads of the ride are news re-posts, not owners (Kompas.com 234k, Workpoint 122k, never use: row 84). No English explainer of why it stays up was found in the top 12 results for "motorcycle on water record 40 km": the angle is open | CGTN Europe | Same rule as 80: ≤5 s per shot, credited "CGTN EUROPE" |
| 81 | CGTN's 0:31 video report (R3) | CGTN | Same as 80 |
| 82 | CCTV+ agency clip (radar 26 Oct: cctvplus.com/news/20261026/8505344.shtml) | CCTV+ | Licensable: the clean route if he wants to pay. Ask the price first |
| 83 | ZXMOTO / 张雪机车's own film (Weibo, Douyin) | ZXMOTO | Best: ask for permission (draft below). Global site global.zxmoto.com (Z2); no press email found |
| 84 | Jamuna TV (531k), DBC, NEWS24, CTi re-uploads (radar 26 Oct) | not the owners | **Never use** |
| 85 | Guinness World Records' own clips | GWR | **Never** (claim risk, radar 26 Oct) |
| 86 | 2009 CCTV 人与社会 footage of the falls | CCTV | Only if found on CCTV's own upload, ≤3 s, credited. Otherwise our Blender rebuild, labelled RECONSTRUCTION |

Borrowed footage under half the runtime (CRAFT, 18 Oct). Our own shots carry the explanation: Blender side view of board + paddle
wheel + arrows, a scale bar 20 m vs 40.74 km, a map pin on Mayang, Hunan.

**Ask text for him to send to ZXMOTO (he sends; we never do):**
> Hello ZXMOTO team, congratulations on Mr Zhang's 40.74 km Guinness World Record. I run The Curve, a YouTube channel that explains
> the physics behind viral clips. May we use 10-15 seconds of your official footage of the ride in a 30-second explainer, credited
> on screen and in the description to ZXMOTO? We'll link your channel. Thank you.

## 7. Hooks (answer in line 1, under 3 s spoken; frame 0 = the bike skimming in its own spray plume, mid-river)

| # | Line 1 | Words | Frame 0 text |
|---|---|---|---|
| H1 | "This motorcycle just rode forty kilometres on water." | 8 | WHY DOESN'T IT SINK? |
| H2 | "You're watching a motorcycle on water that sinks if it slows down." | 12 (long: trim) | 40 KM. ON WATER. |
| H3 | "In 2009 this man sank after twenty metres." (then the 40 km ride) | 8 | 20 M → 40 KM |

H1 says the search phrase "motorcycle on water" only if line 2 does ("A motorcycle on water stays up only while it's fast"):
CRAFT §9.1 wants it said out loud. H3 is the strongest story but opens on a person, not the impossible frame (CRAFT 24 Oct lesson): use it as the
middle beat. Verdict (our point of view): "It's a skipping stone with an engine, and like a stone, it sinks the moment it slows."
Loop: end on the bike slowing and settling into the water, cut to frame 0 (the bike at full speed).

## 8. Do not claim

- That it **floats.** The boards plane on lift from speed; their buoyancy, if any, is unpublished. Say "stays up", "skims".
- Who held the **31.8 km** record (unknown to us), or that this is the **first** motorcycle on water (rows 50-54).
- A **top speed** as fact: 90 km/h is the team's claim (row 29); 76 km/h is our average (row 70), labelled.
- A **sinking speed** in km/h (not published). "Slow down and it sinks" is fine (rows 50, 51, 73, 74).
- **Lake.** It was a river. Don't say the 2009 attempt was on the same river (Wuyi, Zhejiang, row 43).
- **Stock or showroom MX450.** It's a prototype, heavily modified (rows 20, 21, 30). No "you can buy one" (row 31).
- "Non-stop at full throttle": he says he held back (row 11).
- The bike's or rider's weight, or the "104 kg" in one Sina headline (unexplained).
- World Superbike wins. ZXMOTO's wins are World Supersport (row 42).
- Any quote on screen before it is copied from the page itself (method note at the top).

## 9. Open for the builder (watch the footage before scripting)

- How the run starts (R6: "builds up speed on land before skimming"): find the shot of the bike entering the water.
- How it ends: does it ride out onto land, or settle into the water? The loop and the verdict depend on it.
- The clearest shot of the paddle wheel's spray (thrust arrow) and of a turn (one of the seven, row 8).
- Which bike was used for the record run, wide or narrow boards (row 25)? If the footage shows it, name it; if not, don't.
