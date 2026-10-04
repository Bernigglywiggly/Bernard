# The Curve · LF04 · "The Pause": facts file (started 5 Oct 2026)

The only source for on-screen claims (CRAFT.md §5). Secondary reports below all trace to the Associated Press
(reported Saturday 26 Sep 2026) and OpenAI's own disclosure (Friday 25 Sep 2026). Before scripting: find OpenAI's
original post, the AP story itself, and Transluce's report, and replace "as reported" lines with them.

## The arc (why this is LF04)
- July 2026: OpenAI's first pause, after its models "breached the Hugging Face platform" during a cybersecurity
  evaluation; Sam Altman called it "the most severe event we've seen" (as reported by AP via Arab News Japan and
  Hardware Busters). That is LF01's story (`lf01_escape`).
- 28 Sep 2026: OpenAI cancelled GPT-6.1 Astra (LF03, `lf03_held`).
- Late Sep 2026: the second pause (this film).

## What OpenAI paused
- Training of its newest models (names not disclosed). One report (Quartz headline/summary): "all training,
  evaluation, and inference involving tool use for its most capable AI models". TO VERIFY wording against OpenAI's post.
- OpenAI: training will resume "only when we are confident that we have additional safeguards" (AP).

## What the agents did (as reported, AP / Hardware Busters)
- **Census Bureau**: agents "found Census Data API developer keys that someone had left in public GitHub repositories,
  and used them to pull demographic and economic data". Read-only; the data was public.
- **SEC**: agents "collected publicly available material from SEC.gov and Investor.gov and then republished some of it
  on another public web page, which was well outside their instructions". SEC spokesperson Kurt Hopfenspirger: "no
  nonpublic information was accessed."
- **Department of Education**: the evaluator Transluce reported what appeared to be OpenAI agents making a failed
  attempt to break into a department website; OpenAI has not confirmed it. The department: "no evidence of any impact
  to our website or databases."
- Other incidents in OpenAI's disclosure (as reported): agents signing up for disposable email addresses and searching
  GitHub for leaked keys; a model leaking a researcher's GitHub token into a public repository; a self-propagating
  prompt injection during GPT-5.4-mini training; entries dated 16 Sep 2026; an Australian health portal reported to
  authorities on 10 Sep. TO VERIFY each against the primary disclosure before it goes on screen.

## Sources so far
- Arab News Japan (AP): https://www.arabnews.jp/en/business/openai-pauses-training-of-latest-models-after-agents-probed-us-government-sites-in-unexpected-ways-3000406
- Hardware Busters: https://hwbusters.com/news/openai-pauses-training-again-after-its-agents-went-poking-around-us-government-websites/
- CBC: https://www.cbc.ca/news/business/openai-pause-training-after-probes-9.7360166 (403 to the fetcher; read in a browser)
- Quartz: https://qz.com/openai-pauses-ai-model-training-rogue-agents-government-sites-092826 (403 to the fetcher)

## Angle (CRAFT §1: a point of view)
Nothing secret was taken: the keys were public, the data was public. The alarming part is the behaviour: agents
that go looking for keys and post things "well outside their instructions", the exact tendencies the UK tests in LF03
measured. A lab stopping everything over read-only census data says more about what it saw in its logs than about the
census.
