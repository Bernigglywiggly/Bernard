# VERIFY: lf02_price "The Price of Thinking"

**PREMISE HOLDS** - the 22 Sep 2026 price moves, the ~10x-a-year fall (a16z), Jevons, the Red Queen and the $1 trillion+ build-out (Dell'Oro) are all supported by sources I opened, but 1 line is wrong and 13 need rewording before upload.

Checked 7 Oct 2026 against the open web. Script file was not edited.
Status rule used: CONFIRMED = I opened a page that states it. PARTLY = true only with a caveat, or supported only by a search-result snippet / derived arithmetic. Beat numbers count from 1 inside each chapter.

Counts: CONFIRMED 26 · PARTLY 13 · WRONG 1 · UNVERIFIABLE 3 (43 claims)

## 1. Claim table

| # | Claim (short) | Where | Status | Source | What the source actually says |
|---|---|---|---|---|---|
| 1 | Opus 5.5 priced 20% below predecessor, $5 -> $4 input, 22 Sep 2026 | open/1, afternoon/2, close/2 | CONFIRMED | https://platform.claude.com/docs/en/about-claude/pricing ; https://simonwillison.net/2026/Sep/22/opus-and-sol-and-luna/ | Anthropic table: Opus 5.5 $4 / $20, Opus 5 $5 / $25. Willison: "Opus 5.5 is a 20% reduction" |
| 2 | Opus 5.5 is Anthropic's "best model" / "new top model" | open/1, afternoon/2 | PARTLY | https://platform.claude.com/docs/en/about-claude/pricing ; https://the-agent-report.com/2026/09/gpt-6-sol-luna-opus-5-5-price-war/ | Anthropic's own price list has Claude Fable 5.1 above it at $10 / $50. Agent Report says Opus 5.5 is "pitched as Fable 5.1-class". It is the top Opus, not shown to be the top model. Also it is a new model priced lower, not a cut to an existing model's price. |
| 3 | OpenAI answered "within about an hour" | open/2, close/2 | PARTLY | https://simonwillison.net/2026/Sep/22/opus-and-sol-and-luna/ ; https://cellcog.ai/blog/gpt-6-sol-release-date/ ; https://the-agent-report.com/2026/09/gpt-6-sol-luna-opus-5-5-price-war/ ; https://siliconangle.com/2026/09/22/anthropic-releases-claude-opus-5-5-and-openai-counters-with-two-cheaper-gpt-6-models/ | Willison: "around an hour later". Timestamps (cellcog, citing the two labs' posts): 16:31 UTC and 18:00 UTC = 89 minutes. Agent Report: "Ninety minutes later". SiliconANGLE: "minutes later". Sources disagree; the timestamps say an hour and a half. |
| 4 | Two new OpenAI models, each half the price of its predecessor | open/2, afternoon/4 | CONFIRMED | https://developers.openai.com/api/docs/pricing | GPT-6 Sol $2 / $10 vs GPT-5.6 Sol $4 / $20; GPT-6 Luna $0.10 / $0.50 vs GPT-5.6 Luna $0.20 / $1.20 (Luna output is 58% lower, input is half) |
| 5 | AI price "falling faster than almost anything people have ever made" | open/4 | UNVERIFIABLE | https://a16z.com/llmflation-llm-inference-cost/ | a16z only compares with Moore's Law and Edholm's Law and calls the LLM decline faster. No source for "almost anything ever made". |
| 6 | Data-centre capex above $1 trillion in 2026, Dell'Oro | open/5, pays/2 | CONFIRMED | https://www.delloro.com/news/ai-infrastructure-buildouts-and-memory-cost-inflation-drove-data-center-capex-higher-in-1q-2026/ | 10 Jun 2026: "outlook was raised to more than $1 trillion for 2026". (Feb 2026 release said only "approach $1 Trillion".) It is a forecast, and Dell'Oro says part of the growth is memory price inflation. |
| 7 | xAI released Grok 4.7 the day before | afternoon/1 | CONFIRMED | https://simonwillison.net/2026/Sep/22/opus-and-sol-and-luna/ ; https://cellcog.ai/blog/grok-4-7-release-date/ | Willison: "Yesterday was Grok 4.7 and MiMo v2.6 Flash/Pro". cellcog: xAI, 21 Sep 2026, 16:17 UTC. |
| 8 | Xiaomi released two models the day before | afternoon/1 | CONFIRMED | https://simonwillison.net/2026/Sep/22/opus-and-sol-and-luna/ | Same sentence: MiMo v2.6 Flash and Pro. (Search snippets say about four hours after Grok 4.7; one timeline lists 22 Sep, probably China time. Not opened.) |
| 9 | Opus 5.5 $4 read / $20 write, was $5 / $25 | afternoon/2 | CONFIRMED | https://platform.claude.com/docs/en/about-claude/pricing | Table rows for Opus 5.5 and Opus 5, as above. |
| 10 | Cached reads 60% cheaper, $0.50 -> $0.20 | afternoon/3 | CONFIRMED | https://platform.claude.com/docs/en/about-claude/pricing | Cache hits: Opus 5 $0.50 / MTok, Opus 5.5 $0.20 / MTok. Willison: "The price for cache reads fell 60%." |
| 11 | GPT-6 Sol $2 / $10, half the model it replaced | afternoon/4 | CONFIRMED | https://developers.openai.com/api/docs/pricing | See row 4. Note GPT-5.6 Sol's $4 / $20 is itself labelled promotional. |
| 12 | GPT-6 Luna, $0.10 per million tokens read | afternoon/5 | CONFIRMED | https://developers.openai.com/api/docs/pricing | GPT-6 Luna input $0.10, cached $0.01, output $0.50. |
| 13 | Willison quote on Luna | afternoon/6 | CONFIRMED | https://simonwillison.net/2026/Sep/22/opus-and-sol-and-luna/ | "GPT-6 Luna is one of the cheapest models OpenAI have ever released" |
| 14 | OpenAI "also scheduled" a 25% rise for "its older models" in November | afternoon/7 | PARTLY | https://simonwillison.net/2026/Sep/22/opus-and-sol-and-luna/ ; https://developers.openai.com/api/docs/pricing ; https://neomanex.com/news/gpt-5-6-sol-promotional-pricing-november-2026 | Willison: "GPT-5.6 has a scheduled 25% price increase for November". OpenAI's page only says GPT-5.6 Sol's promotional pricing runs "at least through November 21, 2026" and publishes no later rate. The note predates 22 Sep (article dated 7 Sep), so it was not part of that day's news, and it is one model line, not "older models". |
| 15 | 2021: $60 per million tokens; late 2024: $0.06 for the same test score | thousand/2 | CONFIRMED | https://a16z.com/llmflation-llm-inference-cost/ | GPT-3, Nov 2021, MMLU 42, $60; Llama 3.2 3B, same score, $0.06. Nuance: GPT-3 was "the only model" at that score, not "the cheapest". |
| 16 | 1,000x in three years; a16z "LLMflation"; ~10x a year | thousand/3 | CONFIRMED | https://a16z.com/llmflation-llm-inference-cost/ | "the cost is decreasing by 10x every year" (Guido Appenzeller, 12 Nov 2024) |
| 17 | Computer chips took ~20 years for 1,000x; "most famous price collapse in history" | thousand/4 | PARTLY | https://www.intel.com/content/www/us/en/newsroom/resources/moores-law.html ; https://a16z.com/llmflation-llm-inference-cost/ | Intel: transistors "double every two years". 2^10 = 1,024, so 20 years is derived arithmetic about transistor count, not price. a16z gives no chip timescale. "Most famous price collapse in history" has no source. |
| 18 | Chips do more per watt; big models teach small ones | thousand/5, thousand/7 | PARTLY | https://a16z.com/llmflation-llm-inference-cost/ | a16z lists "Better cost/performance of the GPUs" and smaller models as causes. It does not say "per watt". No source opened for distillation. |
| 19 | Epoch AI: compute for the same performance halves about every 8 months | thousand/6 | CONFIRMED | https://epoch.ai/blog/algorithmic-progress-in-language-models | "halved roughly every 8 months, with a 95% confidence interval of 5 to 14" (12 Mar 2024; language-model pre-training; data to 2023) |
| 20 | $0.20 per million cached tokens on Opus 5.5 and Sol | thousand/8 | CONFIRMED | https://platform.claude.com/docs/en/about-claude/pricing ; https://developers.openai.com/api/docs/pricing | Opus 5.5 cache hits $0.20; GPT-6 Sol cached input $0.20. |
| 21 | A US Big Mac costs $6.12 (Economist, Jan 2026) | bigmac/2 | PARTLY | https://raw.githubusercontent.com/TheEconomist/big-mac-data/master/source-data/big-mac-source-data-v2.csv | The Economist's own data: USA 6.12 on 2026-01-01, and 6.22 on 2026-07-01. The on-screen "JAN 2026" label is right; the spoken present-tense "costs" is one edition out of date. |
| 22 | 1 million tokens ~ 750,000 words ~ 8 novels | bigmac/3 | PARTLY | https://platform.claude.com/docs/en/about-claude/pricing | "1 token is approximately 4 characters or 0.75 words in English". Same page: Claude 4.7 and later use a tokenizer producing "approximately 30% more tokens". "8 novels" assumes ~94,000 words a novel; no source. |
| 23 | 2021: reading 8 novels ~ 10 Big Macs | bigmac/4 | CONFIRMED | arithmetic on rows 15 and 21 | $60 / $6.12 = 9.8 |
| 24 | Luna: about 1/60 of a Big Mac | bigmac/5 | CONFIRMED | arithmetic on rows 12 and 21 | $0.10 / $6.12 = 1/61 |
| 25 | One Big Mac ~ 500 novels read | bigmac/6 | CONFIRMED | arithmetic | $6.12 / $0.10 = 61.2M tokens x 8 novels per million = 490 |
| 26 | Opus 5.5 writes 750,000 words for $20 ~ 3 Big Macs | bigmac/7 | PARTLY | https://platform.claude.com/docs/en/about-claude/pricing | $20 / $6.12 = 3.3 is right. But on the newer Claude tokenizer a million tokens is about 30% less text: roughly 580,000 words, not 750,000. |
| 27 | Proper testing takes weeks; switching labs is one line of code | why/3, why/5 | UNVERIFIABLE | none opened | General industry claims. Not checked against a named source. |
| 28 | Red Queen image: John Tenniel, 1871 | queen/1 | PARTLY | https://collections.vam.ac.uk/item/O1505312/through-the-looking-glass-and-book-sir-john-tenniel/ (search snippet only) ; https://www.gutenberg.org/ebooks/12 | Snippet: published 6 Dec 1871, title page dated 1872, fifty illustrations by Tenniel. Gutenberg gives 1871. I did not open the V&A page itself. |
| 29 | Carroll quote | queen/2 | CONFIRMED | https://www.gutenberg.org/files/12/12-h/12-h.htm | "it takes all the running you can do, to keep in the same place." (Red Queen to Alice, ch. II) |
| 30 | Leigh Van Valen, "A New Evolutionary Law", 1973, borrowed the Red Queen | queen/3 | PARTLY | https://link.springer.com/article/10.1007/s13752-021-00391-w (login redirect, not opened) | Search snippets only: Evolutionary Theory 1:1-30, 1973; constant extinction probability explained by co-evolving rivals. Consistent with the script, but no page opened. |
| 31 | Jevons, English economist, The Coal Question, 1865: more efficient engines, more coal | paradox/1-3 | CONFIRMED | https://www.econlib.org/library/YPDBooks/Jevons/jvnCQ.html?chapter_num=9 ; https://www.econlib.org/library/Enc/bios/Jevons.html | "It is wholly a confusion of ideas to suppose that the economical use" (ch. VII, "Of the Economy of Fuel"). Born Liverpool; published 1865. |
| 32 | Nadella post, January 2025, after a cheap Chinese model | paradox/4 | CONFIRMED | https://fortune.com/2025/01/27/microsoft-ceo-satya-nadella-deepseek-optimism-jevons-paradox/ | "Jevons paradox strikes again!" 27 Jan 2025, after DeepSeek's R1. Original X post not opened (see section 5). |
| 33 | "In 2024, Google said it processed nearly ten trillion tokens a month" | paradox/5 | PARTLY | https://blog.google/technology/ai/io-2025-keynote/ | Figure is right; timing of the statement is not. Pichai said it in May 2025: "This time last year, we were processing 9.7 trillion tokens a month". |
| 34 | 2025: 480 trillion a month | paradox/6 | CONFIRMED | https://blog.google/technology/ai/io-2025-keynote/ | "Now, we're processing over 480 trillion" (20 May 2025) |
| 35 | May 2026: 3.2 quadrillion; 300x+ in two years | paradox/7 | CONFIRMED | https://www.shacknews.com/article/149205/google-3-2-quadrillion-monthly-ai-tokens | Pichai, I/O keynote 19 May 2026: over 3.2 quadrillion tokens a month. 3,200 / 9.7 = 330x. Secondary source; Google's own post is on X and was not opened. |
| 36 | Willison's pelican: Opus 5.5 on "max" hit 128,000 tokens, no answer | catch/3 | CONFIRMED | https://simonwillison.net/2026/Sep/22/opus-and-sol-and-luna/ | "Claude Opus 5.5 at 'max' thinking level failed to return a response!" It is the 128,000 maximum output limit. |
| 37 | That silence cost about $2.56, ~0.4 Big Macs | catch/4 | PARTLY | arithmetic on rows 9, 21, 36 | 128,000 x $20 / 1M = $2.56; / $6.12 = 0.42. Derived by the script. I did not find Willison stating a cost, and "almost half" stretches 0.42. |
| 38 | Price war moving from per token to per job | catch/6 | CONFIRMED | https://the-agent-report.com/2026/09/gpt-6-sol-luna-opus-5-5-price-war/ | "Per-task cost, not per-token price, is what decides which model an agent runs." One outlet's analysis, not a measured fact. |
| 39 | $1 trillion = 160 billion+ Big Macs = 20 per person; 8.2 billion people | pays/3 | PARTLY | https://worldpopulationclock.net/world-population-2026/ (search snippet, UN WPP 2024) | $1T / $6.12 = 163 billion, correct. UN figure for mid-2026 is about 8.30 billion, not 8.2. Result is 19.7, still "about twenty". |
| 40 | IEA: data centres ~1.5% of world electricity in 2024, more than double by 2030 | pays/4 | CONFIRMED | https://www.iea.org/reports/energy-and-ai/executive-summary | "around 1.5% of the world's electricity consumption in 2024, or 415 terawatt-hours". "set to more than double to around 945 TWh by 2030" (the doubling is consumption in TWh) |
| 41 | Nvidia first company worth $5 trillion, 29 Oct 2025 | pays/7 | CONFIRMED | https://techcrunch.com/2025/10/29/nvidia-becomes-first-public-company-worth-5-trillion/ | "first public company to pass the $5 trillion market cap milestone" |
| 42 | "Every app with AI inside just had its biggest running cost cut in half, overnight, without lifting a finger" | wins/3 | WRONG | https://developers.openai.com/api/docs/pricing ; https://platform.claude.com/docs/en/about-claude/pricing | Only OpenAI's two new models are half their predecessors. Opus 5.5 is 20% lower. Existing models kept their prices (GPT-5.6 Sol still $4 / $20, Opus 5 still $5 / $25), so an app saves nothing until it switches model. |
| 43 | Agents "can burn through millions of tokens on a single job" | catch/5 | UNVERIFIABLE | none opened | Plausible; no source in the docstring and none checked. |

## 2. Must change before upload

1. **wins/3 (WRONG).**
   - Spoken now: "Every app with AI inside just had its biggest running cost cut in half, overnight, without lifting a finger."
   - Spoken, supported: "And the companies building on top. An app that switches to the new models can cut its biggest running cost by a fifth, or by half, in an afternoon."
   - On screen: image only, no text change needed.

2. **open/2 and close/2 (timing).**
   - Spoken now: "Within about an hour, its biggest rival answered." / "Within about an hour, the other cut it in half."
   - Spoken, supported: "About ninety minutes later, its biggest rival answered." / "Ninety minutes later, the other cut it in half."
   - On screen now: "ABOUT AN HOUR LATER · TWO NEW MODELS" -> "90 MINUTES LATER · TWO NEW MODELS".
   - If you would rather keep Willison's wording, attribute it on screen: "'AROUND AN HOUR LATER' · SIMON WILLISON". Do not present it as a measured time.

3. **open/1, afternoon/2, close/2 ("best model", "cut the price").**
   - Spoken now: "one AI lab cut the price of its best model by a fifth." / "Its new top model, Claude Opus 5.5..."
   - Spoken, supported: "one AI lab launched a new flagship model a fifth cheaper than the last one." / "Its new Opus model, Claude Opus 5.5..."
   - On screen: "−20% · 22 SEP 2026 · $5 → $4 PER MILLION INPUT TOKENS" is fine as it stands.
   - close/2 spoken, supported: "one lab priced its new model a fifth lower. Ninety minutes later, the other halved its own."

4. **afternoon/7 (the 25% rise).**
   - Spoken now: "OpenAI also scheduled a price rise for its older models: twenty-five percent, in November."
   - Spoken, supported: "And there was a quieter detail. The older GPT-5.6 is on promotional pricing that OpenAI only guarantees until late November. Simon Willison expects a twenty-five percent rise."
   - On screen now: "+25% · THE OLDER GPT-5.6 · FROM NOVEMBER" -> "+25%? · GPT-5.6 PROMO PRICE GUARANTEED ONLY TO 21 NOV".
   - afternoon/8 "Cheaper new models, dearer old ones" then needs softening: "Cheaper new models, and old ones about to get dearer."

5. **bigmac/7 (Opus word count).**
   - Spoken now: "Having the top model write eight novels' worth of text costs twenty dollars: a bit more than three Big Macs."
   - Spoken, supported: "Having Opus 5.5 write a million tokens, around six novels' worth, costs twenty dollars: a bit more than three Big Macs."
   - On screen now: "$20 · OPUS 5.5 WRITING 750,000 WORDS" -> "$20 · OPUS 5.5 WRITING A MILLION TOKENS".

6. **bigmac/2 (stale Big Mac price).** Two options, pick one:
   - Keep $6.12 and make the date spoken: "In January, a Big Mac in the United States cost six dollars and twelve cents." On-screen text unchanged.
   - Or update to the July 2026 index, $6.22. Every Big Mac figure still rounds the same (9.6 -> "about ten"; 1/62 -> "about a sixtieth"; 492 novels -> "around five hundred"; 3.2 -> "a bit more than three"; 0.41; 161 billion; 19.4 per person), but on-screen "$6.12" and "÷ $6.12" must become "$6.22" and the label "THE ECONOMIST, JUL 2026".

7. **pays/3 (population).**
   - On screen now: "$1 TRILLION ÷ $6.12 ÷ 8.2 BILLION" -> "$1 TRILLION ÷ $6.12 ÷ 8.3 BILLION". Spoken line can stay ("Twenty for every person alive").

8. **paradox/5 (who said what when).**
   - Spoken now: "In 2024, Google said it processed nearly ten trillion tokens a month."
   - Spoken, supported: "In the spring of 2024, Google was processing nearly ten trillion tokens a month."
   - On screen: unchanged.

9. **thousand/4 (chips comparison).**
   - Spoken now: "For comparison, computer chips, the most famous price collapse in history, took around twenty years to get a thousand times better."
   - Spoken, supported: "For comparison, Moore's Law, the famous doubling of transistors on a chip every two years, takes around twenty years to reach a thousand times."
   - On screen now: "~20 YRS · COMPUTER CHIPS · 1,000×" -> "~20 YRS · MOORE'S LAW · 1,000×".

10. **thousand/2 (small wording).**
    - Spoken now: "the cheapest AI that could reach a set score"
    - Spoken, supported: "the only AI that could reach a set score on a standard knowledge test cost about sixty dollars per million tokens. By late 2024, the cheapest model with the same score cost six cents."

11. **open/4 (unsupported superlative).**
    - Spoken now: "falling faster than the price of almost anything people have ever made."
    - Spoken, supported: "falling faster than computer chips ever did." (a16z supports this comparison.)

12. **catch/4 (soften).**
    - Spoken now: "Almost half a Big Mac, for nothing."
    - Spoken, supported: "At twenty dollars a million, that silence works out at about two dollars and fifty-six cents. Four-tenths of a Big Mac, for nothing."
    - On screen: unchanged.

13. **open/5 and pays/2 (forecast, not a total).** Spoken lines are acceptable ("on course to spend"). In open/5 change "it's spending more than a trillion dollars this year" to "it's on course to spend more than a trillion dollars this year".

## 3. Quotes of named people

| Person | Script wording | Exact sourced wording | Where | Match |
|---|---|---|---|---|
| Simon Willison | "one of the cheapest models OpenAI have ever released" | "At $0.10/$0.50 GPT-6 Luna is one of the cheapest models OpenAI have ever released" | simonwillison.net, 22 Sep 2026 | Yes, exact fragment. Date right. |
| Simon Willison (paraphrase) | "around an hour later" (docstring; open/2 on-screen "ABOUT AN HOUR LATER") | "around an hour later OpenAI released GPT-6 Sol and GPT-6 Luna" | same post | Wording matches Willison, but timestamps show 89 minutes. |
| The Red Queen / Lewis Carroll | "it takes all the running you can do, to keep in the same place." | "Now, here, you see, it takes all the running you can do, to keep in the same place." | Through the Looking-Glass, ch. II (Project Gutenberg #12) | Yes. Script drops the opening four words; comma placement is right. In the original "here" and "you" are italic. |
| Satya Nadella | "Jevons paradox strikes again!" | "Jevons paradox strikes again! As AI gets more efficient and accessible, we will see its use skyrocket, turning it into a commodity we just can't get enough of." | Posted 27 Jan 2025. Fortune describes a LinkedIn post; search results show the same text on X (x.com/satyanadella/status/1883753899255046301). | Yes, exact first sentence. Spoken line drops the exclamation mark, which is fine. On-screen "JANUARY 2025" right. |
| Sundar Pichai / Google (figures, not quoted) | 9.7 trillion, 480 trillion, 3.2 quadrillion | "This time last year, we were processing 9.7 trillion tokens a month across our products and APIs. Now, we're processing over 480 trillion" | blog.google, I/O 2025 keynote | Figures match. See item 8 above for the "In 2024, Google said" wording. |
| W. S. Jevons (paraphrased, not quoted) | "as steam engines burned coal more efficiently, Britain burned more coal, not less" | "It is wholly a confusion of ideas to suppose that the economical use of fuel is equivalent to a diminished consumption." | The Coal Question (1865), ch. VII | Fair paraphrase. |

## 4. Could not check, and why

- **x.com posts** (Nadella's original post; Google's 3.2 quadrillion post; Anthropic and OpenAI launch-time posts): not opened. Wording and times taken from Fortune, Shacknews and cellcog, which cite them.
- **The Economist's Big Mac index page**: the fetch tool cannot reach economist.com. Used The Economist's own public data file on GitHub instead, which is primary.
- **Springer** (Solé, "Revisiting Leigh Van Valen's 'A New Evolutionary Law'"): redirected to a login page; not pursued. Van Valen's 1973 paper itself was not opened. Row 30 rests on search snippets.
- **V&A / Met pages for Tenniel and the 1871/1872 dating**: seen in search results only, not opened. Britannica returned 403.
- **GeekWire, CNBC, OpenAI help centre**: 403. NPR: timed out. Equivalent sources were used.
- **AIOS Guide, "The AI Model Price War Arrived in a Two-Hour Window"** (listed in the docstring): not opened. Its title is itself consistent with a gap longer than an hour.
- **Anthropic's and OpenAI's launch announcements**: not opened directly; prices were confirmed on both companies' live pricing pages instead.
- **Whether Fable 5.1 outperforms Opus 5.5**: not checked. Row 2 rests on Anthropic's price list and the Agent Report's wording only.
- **Whether the 128,000 reasoning tokens were actually billed to Willison at $2.56**: not stated in what I extracted from his post. The figure is the script's arithmetic.
- **General mechanism claims with no named source**: testing takes weeks; switching is one line of code; distillation; agents using millions of tokens per job; "about eight novels" per 750,000 words.
- **The imagery** (p01-p24, a01-a03): not reviewed. Only the caption text in the script was checked.
- All web pages were read through a summarising fetch tool, so quotes above are as that tool returned them. Re-read the two or three you put on screen before upload.

---

## Applied to script.py on 7 Oct 2026
All 13 items of the must-change list were applied as worded (the Big Mac updated to $6.22, July 2026). See the could-not-check list above for what is still open.
