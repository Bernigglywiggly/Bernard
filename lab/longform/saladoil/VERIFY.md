# Money Crimes 03 · The Salad Oil Swindle: verification of script v0 (6 Oct 2026)

Checker pass over `script.py` (v0, 5 Oct). The script was not edited. 44 claims checked: 34 confirmed, 4 wrong,
4 disputed (keep, but soften), 2 unverifiable from here.

**How far this goes.** Court opinions and TIME (1965, 1966) were read online. The New York Times pieces are paywalled:
only the headline and first sentence of the 18 Aug 1965 report were seen, and the 6 June 1972 item only by its title.
Norman C. Miller's book was not read directly: page references come from Wikipedia's citations and figures from
Novel Investor's chapter notes on the book. Court quotes below came through a page summariser, so re-read the opinion
before putting any quote on screen. Buffett's partnership letters were not checked; his figures rest on Foerster (2024,
via Fortune) and on secondary summaries of Lowenstein and Schroeder.

## 1. Lines that must change

| Script line | Problem | Corrected wording |
|---|---|---|
| L64 "Allied filed for bankruptcy on the 18th of November, 1963." | Allied filed on **19 November 1963** (Second Circuit, 1975; Miller). 18 Nov is the day Haupt found itself in trouble, and Wikipedia's "salad oil scandal" page gives 18 while its De Angelis page gives 19. | "Allied filed for bankruptcy on the 19th of November, 1963." |
| L65 "Four days later, President Kennedy was shot in Dallas..." | Follows from the date above: 19 to 22 Nov is three days. | "Three days later, President Kennedy was shot in Dallas, and the country's attention went somewhere else entirely." |
| L68 "...the New York Stock Exchange stepped in with about 36 million dollars." | The Exchange pledged **up to $12 million** and actually advanced **about $9.5 million**. Haupt's bank creditors deferred roughly $24 million of their own claims (two dollars for each Exchange dollar). $36 million is the two added together, or Haupt's bank debt (Miller: $37.1 million to ten banks); it was never Exchange money. | "To protect Haupt's ordinary customers, the New York Stock Exchange stepped in with up to 12 million dollars of its members' money, and Haupt's banks agreed to wait for theirs." |
| L34 "...a subsidiary of American Express, called American Express Field Warehousing." | The company that issued Allied's receipts and went into Chapter XI was **American Express Warehousing, Ltd.** American Express Field Warehousing Corporation was the older sister subsidiary; its business was sold to Lawrence Warehouse on 16 May 1963, with the Bayonne salad-oil account kept out of the sale. | "The warehouse company was a subsidiary of American Express, called American Express Warehousing. A receipt with that name on it was treated almost like cash." |
| L72 "American Express Field Warehousing faced about 210 million dollars of claims." | Same name fix. | "American Express Warehousing faced about 210 million dollars of claims." |

`FACTS.md` carries the same three errors (18 Nov, NYSE $36M, "Field Warehousing") and should be corrected with the script.

## 2. Lines to soften, because sources disagree

| Script line | Why | Suggested wording |
|---|---|---|
| L50-51 "Allied claimed about 900,000 tons of oil as collateral." | Counts differ: New York magazine 1.8 billion lb claimed (900,000 short tons); Miller 1.854 billion lb *missing*, worth $175M; Second Circuit (1977) "1.6 billion pounds... disappeared"; American Express Warehousing's own receipts peaked at 937 million lb. The script's "By the usual account... about" already hedges. | Keep, or "By the usual account, the receipts described something like 900,000 tons of oil." |
| L52 "The tanks held something closer to 55,000 tons." | 110 million lb (55,000 short tons) is New York magazine's figure. Miller: 124 million lb found in the December 1963 inventory, about half of it soap stock, and 100 to 137 million lb in other passages. | "The tanks held perhaps 60,000 tons, and not all of that was oil." |
| L53-54 "...claimed stocks were larger than the government's own figures for all the salad oil in the United States." | The figures were the Census Bureau's (not the USDA's, as FACTS.md has it), and summaries of Miller split between "equalled" and "exceeded". Wikipedia cites Miller p. 104 for "exceeded". | "...Allied's claimed stocks were as large as the government's own count of all the soybean and cottonseed oil in the United States." |
| L60 "betting heavily on the price of soybean oil" | He was long both cottonseed oil (New York Produce Exchange, where by November he held about 90% of the contracts) and soybean oil (Chicago Board of Trade). | "betting heavily on the price of soybean and cottonseed oil" |
| L77 "in 1965 he was sentenced to 20 years in prison" | Correct for the final sentence (Newark, 17 Aug 1965). But TIME (4 June 1965) and Miller's book, which went to press first, report a ten-year sentence on 28 May 1965; that was a provisional commitment. Expect commenters to cite "10 years". | Keep as written. Optionally: "and in August 1965 he was sentenced to 20 years in prison." |
| L84 "He put a large part of his partnership's money into American Express shares" | About $3M, 17% of the partnership, by June 1964 (Foerster); about $13M, roughly 40% of the partnership and 5% of American Express, by 1966 (Lowenstein and Schroeder, as summarised). "A large part" covers both. | Keep. Do not put "40%" or "17%" on screen without a year next to it. |

Also worth knowing, though no line is wrong: L22-23 "more than 150 million dollars" is safe (NYT 1965 "$150 million",
Miller $175M, Wikipedia $180M, New York courts "more than $200,000,000"). The opening inspector scene (L16-19) is a
reconstruction and should carry the "reconstruction" label under CRAFT §5.

## 3. Claim table

Verdicts: CONFIRMED / WRONG / DISPUTED / UNVERIFIABLE. Sources are keyed to the list in section 4.

| # | Line | Claim as written | Verdict | Correct figure / note | Source |
|---|---|---|---|---|---|
| 1 | L16 | Tanks at Bayonne, New Jersey | CONFIRMED | Bayonne tank farm | [S2], [S3] |
| 2 | L16 | "early 1960s" | CONFIRMED | Field warehousing of Allied ran to Nov 1963 | [S1], [S7] |
| 3 | L16-19 | Inspector climbs the tank, lowers a sampling tube, signs the form | UNVERIFIABLE | Illustrative scene; consistent with accounts of top-sampling. Label as reconstruction | [S7], [S9] |
| 4 | L20-21 | Banks lent against the receipts, brokers traded on them, a trusted name stood behind them | CONFIRMED | | [S1], [S5], [S7] |
| 5 | L22 | Most of what was in the tanks was water | CONFIRMED | Court: "a small ocean of salt water"; Miller: forty feet of water under two feet of oil in many tanks | [S1], [S7] |
| 6 | L22-23 | "more than 150 million dollars had been lent against oil that did not exist" | CONFIRMED | $150M (NYT 1965), $175M (Miller), $180M (Wikipedia), over $200M losses (courts) | [S6], [S7], [S9], [S4] |
| 7 | L25 | Warren Buffett, a young investor in Omaha | CONFIRMED | Aged 33 in Nov 1963 | [S10] |
| 8 | L28 | Anthony De Angelis, known as Tino | CONFIRMED | 1915-2009 | [S1], [S8], [S11] |
| 9 | L28-29 | Company: Allied Crude Vegetable Oil Refining | CONFIRMED | Full name "Allied Crude Vegetable Oil Refining Corporation", founded 1955 | [S1], [S4], [S7] |
| 10 | L29 | Bought, stored and sold edible oils on a very large scale | CONFIRMED | Miller: sales over $200M a year; three quarters of US edible-oil exports | [S7] |
| 11 | L32-33 | An independent warehouse company counted the oil and issued receipts used as collateral | CONFIRMED | Field warehousing | [S1], [S9] |
| 12 | L34 | Subsidiary "called American Express Field Warehousing" | WRONG | American Express Warehousing, Ltd. (see section 1) | [S1], [S2], [S12] |
| 13 | L34-35 | A receipt with that name was treated almost like cash | CONFIRMED | Framing; 51 lenders accepted them | [S7], [S9] |
| 14 | L39-40 | A little oil over a lot of water; samples drawn from the top | CONFIRMED | | [S1], [S7], [S9] |
| 15 | L41-42 | Hidden compartments in some tanks ("according to later accounts") | CONFIRMED | Wikipedia citing TIME, 3 Jan 1964; the script's hedge is right. TIME piece not opened | [S9] |
| 16 | L43-44 | Tanks connected by pipes; same oil pumped ahead of inspectors and counted twice | CONFIRMED | Wikipedia citing Miller p. 92 | [S9] |
| 17 | L45 | Later the receipts themselves were forged | CONFIRMED | Miller: $39.4M of forged receipts, 14 Oct to 18 Nov 1963; first indictment 23 Dec 1963 on 18 counts | [S7] |
| 18 | L46-47 | The custodians were Allied's own people | CONFIRMED | American Express Warehousing hired Allied employees to run the tanks it subleased from Allied | [S9], [S13] |
| 19 | L50-51 | About 900,000 tons claimed as collateral | DISPUTED | 1.6 to 1.85 billion lb depending on the count (see section 2); short tons | [S9], [S7], [S4] |
| 20 | L52 | "closer to 55,000 tons" actually there | DISPUTED | 100 to 137 million lb (50,000 to 68,500 short tons), partly soap stock | [S7], [S9] |
| 21 | L53-54 | Claimed stocks larger than the government's figures for all US salad oil | DISPUTED | Census Bureau figures; "equalled" or "exceeded" depending on the summary | [S9], [S14] |
| 22 | L57 | 51 banks and firms had lent against the receipts | CONFIRMED | Miller p. 180 (via Wikipedia); Novel Investor: "51 companies and banks" | [S7], [S9] |
| 23 | L60 | By 1963 De Angelis was betting heavily on soybean oil futures | DISPUTED | Soybean and cottonseed oil; about 90% of the Produce Exchange's cottonseed contracts by Nov 1963 | [S4], [S7], [S15] |
| 24 | L60-61 | Bought through Wall Street brokers | CONFIRMED | Ira Haupt & Co. (broker on 80% of his Produce Exchange contracts) and J. R. Williston & Beane | [S4], [S8] |
| 25 | L61 | Believed prices would keep rising | CONFIRMED | Corner attempt on expected export demand | [S7], [S9] |
| 26 | L62 | Then the price fell | CONFIRMED | Collapse began 14-15 Nov 1963; the Produce Exchange closed on 19 Nov | [S4], [S15] |
| 27 | L62-63 | Allied could not meet its brokers' cash calls; it gave way in days | CONFIRMED | Haupt paid about $12M of margin for Allied in five days | [S4] |
| 28 | L64 | Bankruptcy filed 18 November 1963 | WRONG | 19 November 1963 | [S1], [S7], [S11], [S13] |
| 29 | L65 | Kennedy shot "four days later" | WRONG | Three days later (22 Nov) | follows from 28 |
| 30 | L66 | Ira Haupt & Co., a Wall Street brokerage, collapsed | CONFIRMED | In trouble 18 Nov, suspended by the Exchange 20 Nov 1963, "hopelessly insolvent"; 20,000 customers | [S5] |
| 31 | L66-67 | Haupt had financed De Angelis's trading | CONFIRMED | Loans to Allied against oil, hedged by futures; Miller: $37.1M owed to ten banks | [S15], [S7] |
| 32 | L67 | The receipts Haupt held were worthless | CONFIRMED | By secondary accounts and Miller's notes; the 1969 Haupt opinion that details the receipts could not be opened | [S7], [S9] |
| 33 | L68 | NYSE stepped in with about $36 million | WRONG | Up to $12M pledged, about $9.5M advanced; banks deferred about $24M | [S5], [S16], [S17], [S7] |
| 34 | L71 | Investigators opened the tanks and found water | CONFIRMED | Seawater | [S1], [S7] |
| 35 | L72 | About $210 million of claims on the subsidiary | CONFIRMED | Miller p. 217 (via Wikipedia). TIME 1965 gives $219M across 160 claims in the Allied bankruptcy, a different total | [S9], [S7], [S8] |
| 36 | L73 | About $130,000 of assets | UNVERIFIABLE | Only source is Wikipedia citing Miller p. 217; check the page before it goes on screen | [S9] |
| 37 | L74-75 | American Express's business depended on trust in its name | CONFIRMED | Framing; consistent with Howard Clark's 27 Nov 1963 "morally bound" statement | [S12] |
| 38 | L75 | Settled for about $60 million | CONFIRMED | Court: American Express "agreed to contribute sixty million dollars"; plan confirmed 1967. After tax about $31.6M (secondary) | [S1], [S12] |
| 39 | L76 | Share price fell by more than a third | CONFIRMED | $61.81 on 20 Nov 1963 to $35.31 on 2 June 1964, a 43% fall. "Half" overstates it | [S10] |
| 40 | L77 | De Angelis pleaded guilty | CONFIRMED | Four federal counts, plea of 8 Jan 1965 | [S1], [S7], [S8] |
| 41 | L77 | Sentenced in 1965 to 20 years | CONFIRMED | Newark, 17 Aug 1965. A provisional ten-year sentence was reported on 28 May 1965 | [S6], [S1], [S8] |
| 42 | L77 | Released in 1972 | CONFIRMED | Paroled from Lewisburg; NYT, 6 June 1972 (title only seen) | [S18], [S13] |
| 43 | L82-83 | Buffett's reasoning: balance sheet hurt, customers stayed | CONFIRMED | He checked restaurants, banks and card users in Omaha; told Clark it would pass like a storm | [S10] |
| 44 | L84-85 | A large part of the partnership's money; one of his best early investments | CONFIRMED | 17% by June 1964; about 40% and $13M by 1966; sold by 1968 for a profit of about $20M (secondary) | [S10], [S19] |

## 4. Sources

- [S1] *In the Matter of American Express Warehousing, Ltd.*, 525 F.2d 1012 (2d Cir. 1975): https://www.casemine.com/judgement/us/5914959aadd7b049345d1acd
- [S2] *American Express Warehousing, Ltd. v. Transamerica Insurance Co.*, 380 F.2d 277 (2d Cir. 1967): https://openjurist.org/380/f2d/277 (blocked to this checker; seen as a search snippet at https://www.casemine.com/search/us/salad+oil+scandal)
- [S3] *Procter & Gamble v. Lawrence American Field Warehousing Corp.* (N.Y. 1965) and *Zeeman v. United States* (S.D.N.Y. 1967), search snippets: https://www.casemine.com/search/us/salad+oil+scandal
- [S4] *Seligson v. New York Produce Exchange*, 550 F.2d 762 (2d Cir. 1977): https://law.resource.org/pub/us/case/reporter/F2/550/550.F2d.762.75-5024.76-5002.235.236.html
- [S5] *In re Ira Haupt & Co.*, 234 F. Supp. 167 (S.D.N.Y. 1964): https://www.casemine.com/judgement/us/59149b3eadd7b04934631fbd (also https://law.justia.com/cases/federal/district-courts/FSupp/234/167/1671334/)
- [S6] Richard Phalon, "DeAngelis Receives a 20-Year Sentence", New York Times, 18 Aug 1965, p. 1: https://nyti.ms/4tPe55h (headline and first sentence only)
- [S7] Norman C. Miller, *The Great Salad Oil Swindle* (1965), through chapter notes: https://novelinvestor.com/notes/the-great-salad-oil-swindle-by-norman-c-miller/
- [S8] "Crime: The Man Who Fooled Everybody", TIME, 4 June 1965: https://time.com/archive/6833300/crime-the-man-who-fooled-everybody/
- [S9] Wikipedia, "Salad oil scandal" (cites Miller pp. 92, 104, 174, 180, 217, 223, 245-246; TIME 3 Jan 1964; New York magazine 1 Apr 2012): https://en.wikipedia.org/wiki/Salad_oil_scandal
- [S10] Fortune, 22 Sep 2024, extract from Stephen Foerster, *Trailblazers, Heroes, and Crooks* (2024): https://fortune.com/2024/09/22/warren-buffett-investing-strategy-american-express-stock-scandal/
- [S11] Wikipedia, "Tino De Angelis": https://en.wikipedia.org/wiki/Tino_De_Angelis
- [S12] Wikipedia, "Lawrence Warehouse Company" (cites Wall Street Journal, 25 May 1964, p. 4): https://en.wikipedia.org/wiki/Lawrence_Warehouse_Company ; Clark statement and after-tax cost as summarised at https://inelasticmodels.substack.com/p/american-express-and-the-salad-oil
- [S13] The Tontine Coffee-House, "Salad Oil and American Express": https://tontinecoffeehouse.com/2021/11/15/salad-oil-and-american-express/
- [S14] MarketsWiki, "Great Salad Oil Scandal" (Census Bureau comparison): https://www.marketswiki.com/wiki/Great_Salad_Oil_Scandal
- [S15] *Seligson v. New York Produce Exchange*, 394 F. Supp. 125 (S.D.N.Y. 1975), search snippets: https://www.casemine.com/search/us/Seligson+v.+New+York+Produce+Exchange+Allied+Haupt+soybean+cottonseed+oil+futures
- [S16] *In re Ira Haupt & Co.* (2d Cir., Docket 29310): Exchange "agreed to contribute up to $12,000,000": https://www.casemine.com/judgement/us/5914c89dadd7b049347ebcab ; *Newin Corp. v. Hartford Accident & Indemnity Co.* (1984), $9.5 million advanced: https://www.casemine.com/judgement/us/59148f34add7b04934561596
- [S17] "Wall Street: A Man for Everyman's Capitalism", TIME, 1966 (Funston and the $9.5 million): https://time.com/archive/6889527/wall-street-a-man-for-everymans-capitalism/
- [S18] "Notes on People: De Angelis Freed", New York Times, 6 June 1972: https://www.nytimes.com/1972/06/06/archives/de-angelis-freed.html (title only)
- [S19] Secondary summaries of Lowenstein and Schroeder on the size of the stake: https://www.gurufocus.com/news/244542/standing-in-the-shoes-of-the-oracle-from-omaha-american-express ; https://www.granitefirm.com/blog/us/2023/07/12/american-express/

## 5. Still open before voicing

- Read Miller pp. 104, 174 and 217 directly for the Census comparison, the Haupt rescue terms and the $130,000 of assets.
- Read the full New York Times reports of 20 Nov 1963, 18 Aug 1965 and 6 June 1972.
- Buffett's partnership letters do not appear to have been checked by anyone in the chain; keep "as he and his
  biographers later told it" and avoid "from his letters" on screen until they are.
