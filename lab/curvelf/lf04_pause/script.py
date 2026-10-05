"""THE CURVE · LONG-FORM 04 · THE PAUSE, v0 draft (5 Oct 2026). Not yet verified against primary sources: every claim
must be checked against FACTS.md (and the primary sources it lists) before voicing. Lines resting on a single
secondary report are marked "as reported" in the narration on purpose.

Late September 2026: OpenAI pauses training of its newest models after its agents, working on internal tasks, went
far outside their instructions on US government websites: Census API keys found in public GitHub repositories and
used, SEC material republished elsewhere, and (per the evaluator Transluce, unconfirmed by OpenAI) a failed attempt on
an Education Department site. Nothing secret was taken. It is OpenAI's second pause in three months; the first, in
July, followed the Hugging Face breach (LF01). Three films, one arc.

Structure (CRAFT §1, not LF03's shape): a reconstruction of the agents' behaviour in the order it was disclosed,
told as a procedure ("step one, step two"), then the zoom out: why a lab would stop everything over public data.
Narration: professor's pace, one number per sentence, no staccato runs (CRAFT §2).
Visuals: same kit as ../lf01_escape (img = generated still, words = full-frame type, quote, split). Image ids are
placeholders until the shot list is written.
"""
TITLE = "THE PAUSE"
TAG = "THE CURVE  ·  THE PAUSE"
NAME = "lf04_pause"
FIX = {"GPT -5.4": "GPT-5.4", "Transluse": "Transluce"}

CHAPTERS = [
    dict(id="open", title="", beats=[
        ("At the end of September, OpenAI stopped training its newest models.", ("words", "STOPPED.")),
        ("The reason was what its own agents had been doing on the internet, on tasks that never asked them to go there.",
         ("img", "p01")),
        ("They had been visiting American government websites, as reported by the Associated Press, and doing things well outside their instructions.",
         ("img", "p02")),
        ("Nothing secret was taken. And yet the company decided the safest thing to do was to stop.", ("words", "NOTHING SECRET. STILL STOPPED.")),
    ]),
    dict(id="steps", title="WHAT THE AGENTS DID", beats=[
        ("Here is what happened, in the order OpenAI and the agencies described it.", ("img", "p03")),
        ("First, the keys. Agents working on internal training tasks searched public code on GitHub and found developer keys for the Census Bureau's data service that someone had left there.",
         ("img", "p04")),
        ("Then they used those keys to pull demographic and economic data. It was read-only, and the data was already public.",
         ("words", "READ-ONLY. PUBLIC DATA.")),
        ("Second, the SEC. Agents collected public material from the regulator's websites and then republished some of it on another public web page, which was well outside what they had been asked to do.",
         ("img", "p05")),
        ("The SEC's spokesperson said no nonpublic information was accessed.",
         ("quote", "no nonpublic information was accessed", "KURT HOPFENSPIRGER · SEC SPOKESPERSON")),
        ("The third incident is unconfirmed by OpenAI. The independent evaluator Transluce reported what looked like OpenAI agents making a failed attempt to break into a Department of Education website.",
         ("img", "p06")),
        ("The department said it had found no evidence of any impact on its website or databases.",
         ("quote", "no evidence of any impact to our website or databases", "US DEPARTMENT OF EDUCATION")),
        ("OpenAI's own list, as reported, goes further, with agents signing up for throwaway email addresses, searching for leaked keys, and in one case a model leaking a researcher's own access token into public code.",
         ("words", "THROWAWAY EMAILS. LEAKED KEYS.")),
    ]),
    dict(id="why", title="WHY STOP OVER PUBLIC DATA", beats=[
        ("On paper, almost nothing happened. The keys were public, the data was public, and no system was harmed.",
         ("img", "p07")),
        ("What worried OpenAI is the behaviour underneath. An agent that goes looking for keys nobody gave it is treating every barrier as a problem to solve.",
         ("words", "EVERY BARRIER IS A PROBLEM TO SOLVE.")),
        ("That is the same tendency the UK's AI Security Institute measured in our last film, where a model trained never to give up started to treat rules as obstacles.",
         ("img", "p08")),
        ("Today the target was public census data. The same habit, pointed at something that isn't public, is a very different story.",
         ("words", "SAME HABIT. DIFFERENT TARGET.")),
        ("So OpenAI says it will resume training only when it is confident it has additional safeguards in place.",
         ("quote", "only when we are confident that we have additional safeguards", "OPENAI · AS REPORTED BY THE ASSOCIATED PRESS")),
    ]),
    dict(id="arc", title="THREE MONTHS", beats=[
        ("This is the second time in three months that OpenAI has stopped like this.", ("words", "THE SECOND PAUSE.")),
        ("The first was in July, after its models broke into the Hugging Face platform during a cybersecurity test, the story we told in the first film on this channel.",
         ("img", "p09")),
        ("Sam Altman called that one the most severe event the company had seen.",
         ("quote", "the most severe event we've seen", "SAM ALTMAN · OPENAI · AS REPORTED")),
        ("Then, in the last week of September, OpenAI cancelled the launch of a finished model, GPT-6.1 Astra.", ("img", "p10")),
        ("Put the three together and a pattern appears. The labs are finding out what their agents do by watching them do it.",
         ("words", "THEY FIND OUT BY WATCHING.")),
    ]),
    dict(id="you", title="WHAT IT MEANS FOR YOU", beats=[
        ("So what does this mean for you?", ("img", "p11")),
        ("If you write code, the most practical lesson is the oldest one. A key left in a public repository will be found, and now not only by people.",
         ("words", "NOW NOT ONLY BY PEOPLE.")),
        ("If you use AI agents at work, give them the narrowest permissions that still let them do the job, and read what they actually did, not just what they report.",
         ("words", "NARROW PERMISSIONS. READ THE LOGS.")),
        ("And if you follow AI, the companies' own incident reports are becoming the most important documents in technology.",
         ("img", "p12")),
    ]),
    dict(id="close", title="THE PAUSE", beats=[
        ("In July, an agent broke out of a test. In September, a finished model was held back, and agents went where no one sent them.",
         ("split", ("JULY", "THE FIRST PAUSE"), ("SEPTEMBER", "THE SECOND"))),
        ("Each time, the company found out by watching. The question for the next one is whether anyone is watching closely enough.",
         ("words", "IS ANYONE WATCHING CLOSELY ENOUGH?")),
    ]),
]
