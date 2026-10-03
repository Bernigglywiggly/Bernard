"""THE CURVE · LONG-FORM 02 · THE PRICE OF THINKING (3 Oct 2026). The 22 September price war (EP13's story, at full
length): why the price of AI falls about tenfold a year, why rivals cut within hours, and why falling prices mean MORE
spending, not less. Prices in Big Macs, the house unit. The hidden mechanism: price is the only thing a buyer can read
in an afternoon, and switching costs nothing, so the labs run like the Red Queen; and cheaper thinking gets used so
much more (Jevons) that the total bill grows: it moves from your token to the build-out.

Sources (checked 3 Oct 2026): Simon Willison, 22 Sep 2026, "Claude Opus 5.5, GPT-6 Sol, GPT-6 Luna, and a new price
war" (prices, "around an hour later", GPT-5.6's 25% November rise, Grok 4.7 and MiMo v2.6 the day before, the pelican
that hit the 128,000-token limit); The Agent Report, "The Price War Moves to Cost Per Task"; IEA, Energy and AI (2025); SiliconANGLE, 22 Sep 2026; AIOS Guide, "The AI
Model Price War Arrived in a Two-Hour Window"; a16z, "Welcome to LLMflation" (Nov 2024: $60 -> $0.06 per million
tokens, 2021-2024); Epoch AI, "Algorithmic progress in language models" (2024: the compute needed for a given
performance halves about every eight months); The Economist's Big Mac index (US $6.12, January 2026); W. S. Jevons,
The Coal Question (1865); Satya Nadella on X, 27 Jan 2025; Google I/O 2024-2026 (9.7 trillion, 480 trillion, 3.2
quadrillion tokens a month); Dell'Oro Group (data-centre capex above $1 trillion in 2026); Lewis Carroll, Through the
Looking-Glass (1871); Leigh Van Valen, "A New Evolutionary Law" (1973); Nvidia's $5 trillion market value, 29 Oct 2025.
Visuals as in ../lf01_escape/script.py.
"""
TITLE = "THE PRICE OF THINKING"
TAG = "THE CURVE  ·  THE PRICE OF THINKING"
NAME = "lf02_price"
FIX = {"Opus 5 .5": "Opus 5.5", "GPT -6": "GPT-6", "GPT -5.6": "GPT-5.6"}

CHAPTERS = [
    dict(id="open", title="", beats=[
        ("On the twenty-second of September, one AI lab cut the price of its best model by a fifth.",
         ("num", "−20%", "22 SEP 2026 · $5 → $4 PER MILLION INPUT TOKENS")),
        ("Within about an hour, its biggest rival answered. Two new models, each at half the price of the one before.",
         ("num", "−50%", "ABOUT AN HOUR LATER · TWO NEW MODELS")),
        ("Two companies. One afternoon. Both went cheaper.", ("words", "TWO COMPANIES. ONE AFTERNOON.")),
        ("This happens all the time now. The price of artificial intelligence is falling faster than the price of almost anything people have ever made.",
         ("img", "p01")),
        ("Which should mean the industry is spending less. Instead, it's spending more than a trillion dollars this year, on buildings full of chips.",
         ("num", "$1 TRILLION+", "DATA-CENTRE SPENDING, 2026 · DELL'ORO")),
        ("So who is actually paying for cheaper thinking? And what happens when it gets close to free?", ("img", "p02")),
    ]),
    dict(id="afternoon", title="ONE AFTERNOON", beats=[
        ("It wasn't even the only launch that week. The day before, xAI had released Grok 4.7, and the phone maker Xiaomi two new models of its own.",
         ("img", "p21")),
        ("The first move came from Anthropic. Its new top model, Claude Opus 5.5, cost four dollars to read a million tokens of text, down from five, and twenty dollars to write a million, down from twenty-five.",
         ("split", ("$4", "TO READ A MILLION TOKENS · WAS $5"), ("$20", "TO WRITE A MILLION · WAS $25"))),
        ("Reading text it had already seen got sixty percent cheaper.", ("num", "−60%", "CACHED READS · $0.50 → $0.20")),
        ("Then OpenAI launched GPT-6 Sol, at two dollars and ten dollars: half the price of the model it replaced.",
         ("split", ("$2", "SOL · TO READ"), ("$10", "SOL · TO WRITE"))),
        ("And a smaller sibling, GPT-6 Luna, at ten cents to read a million tokens.", ("num", "$0.10", "GPT-6 LUNA · PER MILLION TOKENS READ")),
        ("The programmer Simon Willison called Luna one of the cheapest models OpenAI has ever released.",
         ("quote", "one of the cheapest models OpenAI have ever released", "SIMON WILLISON · 22 SEP 2026")),
        ("And there was a quieter detail. OpenAI also scheduled a price rise for its older models: twenty-five percent, in November.",
         ("num", "+25%", "THE OLDER GPT-5.6 · FROM NOVEMBER")),
        ("Cheaper new models, dearer old ones. Everyone gets pushed the same way: forward.", ("words", "EVERYONE GETS PUSHED FORWARD.")),
    ]),
    dict(id="thousand", title="A THOUSAND TIMES", beats=[
        ("To see how strange this is, go back five years.", ("img", "p03")),
        ("In 2021, the cheapest AI that could reach a set score on a standard knowledge test cost about sixty dollars per million tokens. By late 2024, a model with the same score cost six cents.",
         ("num", "1,000×", "$60 → $0.06 PER MILLION TOKENS · 2021 → 2024 · a16z")),
        ("A thousand times cheaper, in three years. The investment firm a16z called it LLMflation: about ten times cheaper, every year.",
         ("words", "ABOUT 10× CHEAPER, EVERY YEAR")),
        ("For comparison, computer chips, the most famous price collapse in history, took around twenty years to get a thousand times better.",
         ("split", ("~20 YRS", "COMPUTER CHIPS · 1,000×"), ("3 YRS", "AI · 1,000×"))),
        ("Three things are doing the work at once. Each new generation of chips does more per watt.", ("img", "p04")),
        ("The models themselves get smarter per calculation. Researchers at Epoch AI estimate that the computing needed for the same performance halves about every eight months.",
         ("num", "÷2", "COMPUTE NEEDED FOR THE SAME RESULT · EVERY ~8 MONTHS · EPOCH AI")),
        ("And big models teach small ones: a cheap model can learn to answer almost as well as an expensive one, from the expensive one's own answers.",
         ("img", "p05")),
        ("And labs have stopped charging full price for text a model has already read. Send the same long document twice, and the second read is a fraction of the cost.",
         ("num", "$0.20", "PER MILLION CACHED TOKENS · OPUS 5.5 AND SOL")),
    ]),
    dict(id="bigmac", title="IN BIG MACS", beats=[
        ("Prices per million tokens mean nothing to most people. So here it is in the unit this channel always uses.", ("img", "p06")),
        ("A Big Mac in the United States costs six dollars and twelve cents.", ("num", "$6.12", "A BIG MAC · USA · THE ECONOMIST, JAN 2026")),
        ("A million tokens is about seven hundred and fifty thousand words. Roughly eight novels.",
         ("num", "≈ 8 NOVELS", "1 MILLION TOKENS ≈ 750,000 WORDS")),
        ("In 2021, having a machine read eight novels cost about ten Big Macs.", ("num", "≈ 10 BIG MACS", "$60 · TO READ 8 NOVELS · 2021")),
        ("With GPT-6 Luna, it costs about a sixtieth of one.", ("num", "1/60", "OF A BIG MAC · TO READ 8 NOVELS · 2026")),
        ("Or put it the other way. For the price of one Big Mac, a machine can now read around five hundred novels.",
         ("num", "≈ 500", "NOVELS READ · FOR ONE BIG MAC")),
        ("Writing costs more than reading. Having the top model write eight novels' worth of text costs twenty dollars: a bit more than three Big Macs.",
         ("num", "≈ 3 BIG MACS", "$20 · OPUS 5.5 WRITING 750,000 WORDS")),
        ("Your whole reading list. Every review a restaurant has ever had. Years of your emails.", ("img", "p07")),
    ]),
    dict(id="why", title="WHY THEY CUT", beats=[
        ("So why do the labs keep cutting, and so fast?", ("img", "p08")),
        ("When a product gets better every few months, customers are really comparing two things. How good, and how much.",
         ("list", ["HOW GOOD?", "HOW MUCH?"])),
        ("Nobody can tell how good in an afternoon. Testing a model properly takes weeks. Everyone can see the price in seconds.",
         ("split", ("WEEKS", "TO TELL HOW GOOD"), ("SECONDS", "TO SEE THE PRICE"))),
        ("So price is the signal. And switching costs almost nothing.", ("words", "PRICE IS THE SIGNAL.")),
        ("Most of these models are called the same way, over the internet, through nearly identical connections. A developer can move from one lab to another by changing a line of code.",
         ("img", "p09")),
        ("So when one lab cuts, customers can leave the other one by teatime. The other lab has hours to answer, not weeks.",
         ("words", "HOURS, NOT WEEKS.")),
    ]),
    dict(id="queen", title="THE RED QUEEN", beats=[
        ("Biologists have a name for this kind of race.", ("img", "a01", "THE RED QUEEN · JOHN TENNIEL, 1871")),
        ("In Through the Looking-Glass, the Red Queen tells Alice: it takes all the running you can do, to keep in the same place.",
         ("quote", "it takes all the running you can do, to keep in the same place.", "THE RED QUEEN · LEWIS CARROLL, 1871")),
        ("In 1973, the biologist Leigh Van Valen borrowed her to explain why species never seem to get ahead. Their rivals keep evolving too.",
         ("img", "p10", "LEIGH VAN VALEN · \"A NEW EVOLUTIONARY LAW\" · 1973")),
        ("The labs are running as fast as they can, and staying exactly where they are against each other.", ("img", "p11")),
        ("And every step they take, you get it cheaper.", ("words", "EVERY STEP: CHEAPER FOR YOU.")),
    ]),
    dict(id="paradox", title="THE PARADOX", beats=[
        ("If thinking keeps getting cheaper, you'd expect the world to spend less on it. In 1865, an English economist explained why the opposite happens.",
         ("img", "a02", "WILLIAM STANLEY JEVONS")),
        ("William Stanley Jevons noticed that as steam engines burned coal more efficiently, Britain burned more coal, not less.",
         ("img", "a03", "THE COAL QUESTION · 1865")),
        ("Make something cheaper to use, and people find so many new uses that the total goes up. It's called the Jevons paradox.",
         ("words", "THE JEVONS PARADOX")),
        ("When a Chinese lab released a cheap, capable model in January 2025, Microsoft's chief executive, Satya Nadella, posted: Jevons paradox strikes again.",
         ("quote", "Jevons paradox strikes again!", "SATYA NADELLA · MICROSOFT · JANUARY 2025")),
        ("He was right. In 2024, Google said it processed nearly ten trillion tokens a month.", ("num", "9.7 T", "TOKENS A MONTH · GOOGLE · 2024")),
        ("In 2025, four hundred and eighty trillion.", ("num", "480 T", "TOKENS A MONTH · GOOGLE · 2025")),
        ("In May this year: three point two quadrillion. More than three hundred times as much, in two years.",
         ("num", "3,200 T", "TOKENS A MONTH · GOOGLE · MAY 2026")),
    ]),
    dict(id="catch", title="THE CATCH", beats=[
        ("There's a catch in all of this. The price of a token is falling. The number of tokens in each answer is rising.",
         ("split", ("LESS", "PRICE PER TOKEN"), ("MORE", "TOKENS PER ANSWER"))),
        ("The newest models think before they answer, writing out long chains of reasoning you never see. You pay for every word of it.",
         ("img", "p22")),
        ("When Simon Willison asked Opus 5.5 for a drawing of a pelican at its highest thinking setting, it thought until it hit its limit of a hundred and twenty-eight thousand tokens, and never answered.",
         ("num", "128,000", "TOKENS OF THINKING · NO ANSWER · OPUS 5.5 ON \"MAX\"")),
        ("At twenty dollars a million, that silence cost about two dollars and fifty-six cents. Almost half a Big Mac, for nothing.",
         ("num", "$2.56", "≈ 0.4 BIG MACS · FOR NO ANSWER")),
        ("And agents, AI that works on its own for hours, can burn through millions of tokens on a single job.", ("img", "p23")),
        ("So the price war is quietly moving, from the price of a token to the price of a job done.",
         ("words", "FROM PER TOKEN, TO PER JOB")),
    ]),
    dict(id="pays", title="WHO PAYS", beats=[
        ("Every one of those tokens runs on a chip, in a building, on a power line.", ("img", "p12")),
        ("This year, the world is on course to spend more than a trillion dollars on data centres, according to the research firm Dell'Oro.",
         ("num", "$1 TRILLION+", "DATA-CENTRE CAPITAL SPENDING · 2026")),
        ("In Big Macs, that's more than a hundred and sixty billion of them. Twenty for every person alive.",
         ("num", "≈ 20", "BIG MACS PER PERSON ON EARTH · $1 TRILLION ÷ $6.12 ÷ 8.2 BILLION")),
        ("And the power to run them. The International Energy Agency estimates data centres used about one and a half percent of the world's electricity in 2024, and expects that to more than double by 2030.",
         ("split", ("1.5%", "OF WORLD ELECTRICITY · 2024"), ("×2+", "BY 2030 · IEA"))),
        ("So the bill hasn't gone away. It has moved: from the price of your token, to the build-out behind it.", ("img", "p13")),
        ("Investors are paying now, on the bet that usage keeps growing faster than prices fall.", ("img", "p14")),
        ("And the companies selling the shovels are doing very well. In October 2025, the chipmaker Nvidia became the first company in history worth five trillion dollars.",
         ("num", "$5 TRILLION", "NVIDIA · FIRST COMPANY TO REACH IT · 29 OCT 2025")),
    ]),
    dict(id="wins", title="WHO WINS", beats=[
        ("In a price war, the first winner is the customer.", ("img", "p15")),
        ("Every tool built on these models gets cheaper to run, and so do the experiments nobody would have paid for a year ago.",
         ("list", ["A TUTOR FOR EVERY STUDENT", "A TRANSLATOR IN EVERY PHONE", "A SECOND OPINION ON EVERY CONTRACT"])),
        ("And the companies building on top. Every app with AI inside just had its biggest running cost cut in half, overnight, without lifting a finger.",
         ("img", "p24")),
        ("The labs are in a harder spot. Each cut makes them more popular, and earns them less on every word.", ("img", "p16")),
        ("Their bet is that being the best, or the cheapest, at the right moment will be enough. The Red Queen's bet is that nobody stays ahead for long.",
         ("words", "NOBODY STAYS AHEAD FOR LONG.")),
    ]),
    dict(id="imagine", title="IMAGINE", beats=[
        ("So imagine the running never stops. Not a forecast. A what-if.", ("words", "A WHAT-IF. NOT A FORECAST.")),
        ("Imagine the best tutor on Earth costs less than a text message.", ("img", "p17")),
        ("Then the best coder. The best translator. The best second opinion, at three in the morning.", ("img", "p18")),
        ("When thinking is almost free, what gets expensive?", ("words", "WHAT GETS EXPENSIVE?")),
        ("Maybe the things a machine can't send you. Your time. Your attention. Someone who turns up.",
         ("list", ["YOUR TIME", "YOUR ATTENTION", "SOMEONE WHO TURNS UP"])),
    ]),
    dict(id="close", title="STILL RUNNING", beats=[
        ("Tonight's version is simpler. Find the one job you've been putting off because it means hours of reading, and hand it over for pennies.",
         ("img", "p19")),
        ("On the twenty-second of September, one lab cut its price by a fifth. Within about an hour, the other cut it in half.",
         ("split", ("−20%", "ONE LAB"), ("−50%", "THE OTHER"))),
        ("Both of them are still running.", ("img", "p20")),
        ("And so far, every step they take makes thinking cheaper for you.", ("words", "STILL RUNNING.")),
    ]),
]
