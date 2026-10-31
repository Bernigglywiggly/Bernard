"""MONEY CRIMES · 02 · THE ORIGINAL PONZI SCHEME (Charles Ponzi, 1882-1949). The corrected, re-cut script (8 Oct 2026),
converted to beats from lab/longform/ponzi/script.py, with every "Must change" item of lab/longform/ponzi/VERIFY.md
(an independent fact check, 7 Oct 2026: premise holds) applied on the way. Content, order and voice are the source's;
no new facts were added.

Corrections applied from VERIFY.md (its section 3, by number):
   1  Cold open: the four-abreast line was people queuing to invest; the crowd now "fills School Street" wanting its
      money back, and the Post's question is shown as plain words, not as a quotation or headline.
   2  Ponzi "rose to manager" at Zarossi's bank (was "assistant manager").
   3  After the run, many "left their money where it was" (was "invested again").
   4  Supreme Court order of events: the state charges came first, the Court ruled while he was a federal prisoner,
      three trials, seven to nine years in 1925.
   5  "Sentenced to five years" (was "in federal prison"; he served it in the Plymouth county jail).
   6  "Coffee and hot dogs" (was "coffee and doughnuts"), in the cold open and in the run.
   7  The coupon arithmetic is no longer attributed to Barron; his name is kept for the supported line that follows.
   8  "By May, the money was coming in by the hundred thousand" (the $420,000 figure is gone).
   9  Investors got back "about thirty cents on the dollar" (was "less than"); on screen "ABOUT 30¢".
  10  The forged cheque is "a little over four hundred dollars"; on screen "$400+".
  11  Morse fooled the doctors, "it was later said, by swallowing soap" (was "eating soap shavings").
  12  Brazil: "an Italian airline. The war closed it down" (was the state airline, shut when Brazil joined the war).
  13  "Around nineteen oh seven" he moved to Montreal; on screen "c. 1907".
  14  "Barely five foot two".
  15  "A mansion in Lexington, a chauffeured limousine, and gold-headed canes" ("twelve-room", "custom-built" and
      the diamonds are gone).
  16  "He had first landed in America thirty-one years earlier" (was "lived in America for thirty years").
  17  Florida: "Some of it was under water" (the hedge is dropped; it is on the record).
  18  Archive credit "DON'T BE PONZIED": that advertisement is not used in this cut, so nothing to correct.
  19  Sources now include American Heritage (Francis Russell, 1973), Ponzi v. Fessenden, 258 U.S. 254 (1922) and the
      National Archives' Prologue article on his inmate file, beside the Smithsonian Sidedoor transcript, Boston.com
      (2015), BU Bridge (Zuckoff interview) and Time (2017). The old docstring's "Smithsonian: about $15M from about
      40,000" could not be checked and is not relied on.

Cut or hedged as unverifiable (Wikipedia-only or snippet-only in VERIFY.md); none of these numbers is on screen:
  - Birth: the day (3 March) and Lugo are cut; "born in eighteen eighty-two, in northern Italy".
  - University in Rome and the "four-year holiday": hedged "by the usual account".
  - Dishwasher, waiter, sleeping on the floor, fired: hedged "by most accounts".
  - Zarossi fleeing to Mexico: hedged "to Mexico it's said".
  - The four hundred percent margin: hedged "by one account".
  - "The city's biggest newspaper": now "one of the city's biggest newspapers".
  - The Post headline of 24 July (wording seen in a snippet only): paraphrased, not shown as a quotation.
  - Barron as "the most respected financial journalist in America" (opinion): cut to "the financial journalist".
  - 160 million coupons needed and 27,000 in circulation: hedged "by one widely repeated estimate", off screen.
  - Two million dollars paid out in three days: hedged "by one widely repeated figure", off screen.
  - Controlling interest in the Hanover Trust: hedged "by most accounts".
  - McMasters "looked at the books": loosened to "looked through the paperwork".
  - Hanover Trust seized "the same day" as the Post's 11 August story: now "around the same time".
  - Florida's two hundred percent in sixty days: hedged "by one account", off screen.
  - The shaved head: hedged "the story goes"; New Orleans as the ship's "last American port" is cut.
  - Death: the day (18 January) is cut; "in January nineteen forty-nine".
  - Madoff's sixty-five billion dollars: hedged "by the widely reported figure", off screen.
Quotation cards are used only for wording VERIFY.md confirmed word for word: Ponzi's "$2.50 in cash" line, his two
"cheap at that price" sentences, and the Post's 2 August headline.

Photographs: 18 real, public-domain pictures, all used. Their sources and rights are recorded in
lab/longform/ponzi/src/photo/CREDITS.md. AI illustrations (ids from lab/longform/ponzi/assets_ai.json) are atmosphere
or reconstruction only, never labelled as photographs, and never show Ponzi's face.

Each chapter is a list of beats: (spoken text, visual). Visuals:
  ("photo", id, label, credit)               a real photograph from CREDITS.md; label and credit typed
  ("img", id[, label])                       an AI still, a slow move; label typed top left
  ("num", big, small)                        a big number; the caption typed in gold
  ("words", text)                            a short line, large
  ("quote", text, who)                       a quotation typed crisp, its source below
  ("list", [items][, title])                 lines typed one after another
  ("split", (big, small), (big, small))      two numbers side by side
  ("tl", [(date, what), ...])                a dated line, the marks typed in turn
"""
TITLE = "THE ORIGINAL PONZI SCHEME"
TAG = "MONEY CRIMES  ·  THE ORIGINAL PONZI SCHEME"
FIX = {}

CHAPTERS = [
    dict(id="open", title="", beats=[
        ("Boston, July nineteen twenty. A crowd fills School Street, outside a small office. Working people, mostly. Some of them have put in their life savings.",
         ("photo", "school_street_crowd_1920", "SCHOOL STREET, BOSTON · 1920", "UNDERWOOD & UNDERWOOD · MID-WEEK PICTORIAL, 1920")),
        ("Two days ago they were queuing four abreast to hand their money over. Today they want it back.",
         ("img", "o01", "RECONSTRUCTION")),
        ("That morning, one of the city's biggest newspapers has started asking the question nobody wanted to ask: where is the money coming from?",
         ("words", "WHERE IS THE MONEY COMING FROM?")),
        ("And walking through the crowd, in an immaculate suit, is the man who has their money.",
         ("photo", "ponzi_straw_hat_1920", "CHARLES PONZI · 1920", "KEYSTONE VIEW CO. · THE LITERARY DIGEST, 1920")),
        ("He's handing out coffee and hot dogs. He's telling them they have nothing to worry about. And he pays them. Every one of them.",
         ("img", "o05")),
        ("His name was Charles Ponzi. He didn't invent the trick. But he ran it so spectacularly that it has carried his name ever since.",
         ("photo", "ponzi_portrait_bain_1920", "CHARLES PONZI · c. 1920", "BAIN NEWS SERVICE · LIBRARY OF CONGRESS")),
        ("This is how it worked, how it fell apart, and why it's still running today.",
         ("list", ["HOW IT WORKED", "HOW IT FELL APART", "WHY IT'S STILL RUNNING"])),
    ]),
    dict(id="arrive", title="TWO DOLLARS AND FIFTY CENTS", beats=[
        ("Carlo Ponzi was born in eighteen eighty-two, in northern Italy. His family had known better days, and they wanted him to restore them.",
         ("words", "BORN 1882 · NORTHERN ITALY")),
        ("By the usual account, he went to university in Rome, where his richer friends treated it as a four-year holiday. He followed them to the bars, the cafés and the opera.",
         ("img", "a01")),
        ("In November nineteen oh three, he arrived in Boston on a steamship. He had gambled away almost everything on the crossing.",
         ("img", "a02", "BOSTON HARBOUR, NOVEMBER 1903 · RECONSTRUCTION")),
        ("He stepped onto the dock with two dollars and fifty cents to his name.",
         ("num", "$2.50", "IN CASH, ON THE DOCK · BOSTON, NOVEMBER 1903")),
        ("He later said he landed with two dollars fifty in cash, and a million dollars in hopes. And the hopes never left him.",
         ("quote", "I landed in this country with $2.50 in cash and $1 million in hopes, and those hopes never left me.",
          "CHARLES PONZI · AS HE LATER TOLD A REPORTER")),
        ("By most accounts, he washed dishes. He waited tables, and slept on the restaurant floor.",
         ("img", "a05")),
        ("He was promoted, and then fired, for short-changing the customers and stealing from the till.",
         ("img", "a07")),
        ("For a man who wanted to be rich, America was turning out to be very hard work.",
         ("words", "VERY HARD WORK")),
    ]),
    dict(id="montreal", title="ROBBING PETER", beats=[
        ("Around nineteen oh seven, he moved to Montreal, and found a job at a small bank run by Luigi Zarossi, which served the city's Italian immigrants.",
         ("img", "m01", "MONTREAL · c. 1907 · RECONSTRUCTION")),
        ("Zarossi's bank paid six percent interest. Twice what other banks paid.",
         ("num", "6%", "ZAROSSI'S INTEREST · TWICE WHAT OTHER BANKS PAID")),
        ("Ponzi rose to manager, and discovered how it was done. The interest wasn't coming from profits. The bank was in trouble.",
         ("img", "m02")),
        ("Old customers were being paid with new customers' deposits. Robbing Peter to pay Paul.",
         ("words", "ROBBING PETER TO PAY PAUL")),
        ("Ponzi watched it closely. And he watched what happened when it stopped working.",
         ("img", "m03")),
        ("The bank collapsed, and Zarossi fled, to Mexico it's said, with much of the money that was left.",
         ("img", "m04")),
        ("Broke again, Ponzi forged a cheque for a little over four hundred dollars. He was caught almost at once, and sent to a Quebec penitentiary.",
         ("num", "$400+", "A FORGED CHEQUE · MONTREAL")),
        ("Out of prison, he crossed back into the United States, and was caught again, this time smuggling Italian immigrants over the border. Two more years, in the federal prison in Atlanta.",
         ("img", "m07")),
        ("There, by most accounts, he met Charles Morse, a Wall Street millionaire serving time for fraud.",
         ("list", ["CHARLES W. MORSE", "WALL STREET MILLIONAIRE", "FELLOW PRISONER, ATLANTA"], "BY MOST ACCOUNTS")),
        ("Morse fooled the prison doctors, it was later said, by swallowing soap, to make himself look gravely ill. He was soon released.",
         ("img", "m08", "RECONSTRUCTION")),
        ("Ponzi was paying attention. Appearances, he was learning, are worth more than facts.",
         ("words", "APPEARANCES BEAT FACTS")),
    ]),
    dict(id="coupon", title="THE COUPON", beats=[
        ("By nineteen nineteen, he was back in Boston, married to a young woman called Rose Gnecco, and still poor.",
         ("photo", "boston_washington_st_1920", "WASHINGTON STREET, BOSTON · 1920", "LEON ABDALIAN · BOSTON PUBLIC LIBRARY")),
        ("Then, one day, a letter arrived from a company in Spain. Inside was a small slip of paper.",
         ("img", "c01")),
        ("It was an international reply coupon. You could buy one at a post office in one country, and post it abroad.",
         ("photo", "reply_coupon_rome_type", "INTERNATIONAL REPLY COUPON · 1907 DESIGN", "UNIVERSAL POSTAL UNION · BELGIAN ISSUE")),
        ("The person who received it could swap it for stamps, so they could write back for free.",
         ("img", "c02")),
        ("The exchange rates had been fixed by international agreement, before the First World War. After the war, money across Europe collapsed in value. The coupons didn't.",
         ("words", "THE COUPONS HELD THEIR VALUE")),
        ("So a coupon bought cheaply in Spain, or Italy, could be swapped in America for stamps worth more than it cost.",
         ("list", ["BUY CHEAP IN EUROPE", "SWAP FOR STAMPS IN AMERICA", "KEEP THE DIFFERENCE"])),
        ("On paper, it was a profit. And on paper, it was perfectly legal.",
         ("words", "LEGAL. ON PAPER.")),
        ("Ponzi did the sums and saw a fortune. He told people, by one account, that the margin could be four hundred percent.",
         ("img", "c03")),
        ("There was one problem. You can't spend stamps. To turn a profit into cash, you'd have to buy coupons by the hundred thousand, and ship them across the ocean.",
         ("words", "YOU CAN'T SPEND STAMPS")),
        ("Then you'd have to swap them for stamps, and sell a mountain of stamps. Nobody could do that. Ponzi never really tried.",
         ("img", "c04")),
    ]),
    dict(id="promise", title="FIFTY PERCENT IN FORTY-FIVE DAYS", beats=[
        ("At the start of nineteen twenty, he set up the Securities Exchange Company, in a small office on School Street, and made a promise.",
         ("photo", "boston_kings_chapel_school_st_1920", "KING'S CHAPEL, AT THE TOP OF SCHOOL STREET · JULY 1920", "LEON ABDALIAN · BOSTON PUBLIC LIBRARY")),
        ("Give him your money, and in forty-five days he would pay you back with fifty percent on top. Wait ninety days, and he would double it.",
         ("split", ("50%", "ON TOP, IN 45 DAYS"), ("100%", "ON TOP, IN 90 DAYS"))),
        ("In the first month, eighteen people took the chance. Between them, they put in eighteen hundred dollars.",
         ("split", ("18", "INVESTORS IN THE FIRST MONTH"), ("$1,800", "PUT IN BETWEEN THEM"))),
        ("And then Ponzi did something that made everything else possible. He paid them. On time, and in full.",
         ("words", "PAID. ON TIME. IN FULL.")),
        ("The money didn't come from coupons. It came from the next investors. But the first investors didn't know that. All they knew was that it worked.",
         ("img", "p01")),
        ("So they told their friends. And their friends told theirs. That was the whole machine.",
         ("img", "p02")),
        ("Every happy customer became a salesman, and every salesman brought in the money to pay the last one.",
         ("list", ["A HAPPY CUSTOMER", "BECOMES A SALESMAN", "BRINGS IN NEW MONEY", "WHICH PAYS THE LAST ONE"], "THE MACHINE")),
        ("By May, the money was coming in by the hundred thousand. By June, two and a half million.",
         ("num", "$2.5M", "TAKEN IN BY JUNE 1920 · AMERICAN HERITAGE")),
        ("By July, by some accounts, as much as a quarter of a million dollars was arriving every day.",
         ("num", "$250,000", "A DAY, BY SOME ACCOUNTS · JULY 1920 · BOSTON.COM")),
    ]),
    dict(id="king", title="THE KING OF SCHOOL STREET", beats=[
        ("Ponzi was barely five foot two, and suddenly he was the most famous man in Boston.",
         ("photo", "ponzi_straw_hat_1920", "CHARLES PONZI · 1920", "KEYSTONE VIEW CO. · THE LITERARY DIGEST, 1920")),
        ("He bought a mansion in Lexington, a chauffeured limousine, and gold-headed canes.",
         ("photo", "ponzi_house_lexington_1920", "THE PONZI HOUSE, LEXINGTON · 1920", "INTERNATIONAL · LESLIE'S WEEKLY, 1920")),
        ("Crowds followed him down the street, and called him a genius.",
         ("img", "k04", "RECONSTRUCTION")),
        ("He wanted more than money. He wanted to be a banker. By most accounts, he poured millions of his investors' dollars into the Hanover Trust Company, until he controlled the bank itself.",
         ("img", "k05")),
        ("And most of his investors never asked for their profits. Why would they?",
         ("words", "WHY WOULD THEY?")),
        ("It was easier to leave the money where it was, and watch it grow. On paper.",
         ("photo", "ponzi_promissory_note_1920", "A SECURITIES EXCHANGE COMPANY NOTE · JUNE 1920", "UNDERWOOD & UNDERWOOD · MID-WEEK PICTORIAL, 1920")),
    ]),
    dict(id="post", title="THE QUESTION", beats=[
        ("On the twenty-fourth of July, nineteen twenty, the Boston Post put him on its front page. He was doubling people's money, the story said, within three months. Thousands more came running.",
         ("img", "n01")),
        ("But at the Post, the young acting publisher, Richard Grozier, had doubts. Two days later, his paper started asking questions.",
         ("tl", [("24 JULY", "THE POST'S FRONT PAGE"), ("TWO DAYS LATER", "THE POST'S QUESTIONS")])),
        ("Then the numbers came out. By one widely repeated estimate, about one hundred and sixty million postal reply coupons would have had to be in circulation to cover what Ponzi had taken in.",
         ("img", "n03")),
        ("There were, on the same estimate, only about twenty-seven thousand.",
         ("words", "THE SUMS DIDN'T ADD UP")),
        ("And the financial journalist Clarence Barron noticed one more thing.",
         ("words", "ONE MORE THING")),
        ("Ponzi, the man who promised everyone fifty percent, wasn't putting his own money into his own scheme.",
         ("words", "NOT HIS OWN MONEY")),
    ]),
    dict(id="run", title="THE RUN", beats=[
        ("The morning the questions appeared, the crowd came to School Street. Not to invest. To get out.",
         ("photo", "school_street_run_1920", "THE RUN ON PONZI'S OFFICE, SCHOOL STREET · 1920", "UNDERWOOD & UNDERWOOD · THE LITERARY DIGEST, 1920")),
        ("And this is where Ponzi was at his most brilliant. He didn't hide. He opened the doors, and paid.",
         ("words", "HE OPENED THE DOORS, AND PAID.")),
        ("Over three days, by one widely repeated figure, around two million dollars went back out of the window.",
         ("img", "r02")),
        ("He walked the line, handing out coffee and hot dogs, smiling, joking, telling them there was nothing to worry about.",
         ("words", "COFFEE AND HOT DOGS")),
        ("It worked. People who saw the money being paid out so easily decided it must be safe. Many of them turned round, and left their money where it was.",
         ("list", ["THEY SAW HIM PAY", "THEY DECIDED IT WAS SAFE", "THEY LEFT THE MONEY IN"])),
        ("Ponzi had survived the run. But he couldn't survive arithmetic.",
         ("words", "HE COULDN'T SURVIVE ARITHMETIC")),
    ]),
    dict(id="fall", title="HOPELESSLY INSOLVENT", beats=[
        ("The end came from inside. Ponzi had hired a publicity agent, a former newspaperman called William McMasters.",
         ("img", "f01", "RECONSTRUCTION")),
        ("McMasters looked through the paperwork, and went to the Post.",
         ("words", "HE WENT TO THE POST")),
        ("On the second of August, the Post printed his verdict on its front page. Ponzi was hopelessly insolvent. Millions of dollars in debt.",
         ("quote", "Declares Ponzi Is Now Hopelessly Insolvent", "THE BOSTON POST · FRONT-PAGE HEADLINE, 2 AUGUST 1920")),
        ("Auditors moved in. The hole kept getting deeper. Then, on the eleventh of August, the Post found his past.",
         ("img", "f02")),
        ("Montreal. Zarossi's bank. The forged cheque. The prison photograph of the man Boston had called a genius.",
         ("list", ["MONTREAL", "ZAROSSI'S BANK", "THE FORGED CHEQUE", "THE PRISON PHOTOGRAPH"], "THE POST, 11 AUGUST 1920")),
        ("Around the same time, the state's banking commissioner seized the Hanover Trust.",
         ("img", "f03", "RECONSTRUCTION")),
        ("Within days, Charles Ponzi gave himself up to federal agents.",
         ("photo", "boston_american_ponzi_arrested_1920", "\"PONZI ARRESTED\" · 12 AUGUST 1920", "BOSTON AMERICAN, 12 AUGUST 1920")),
        ("The paper that asked the question won the Pulitzer Prize, the following year.",
         ("photo", "editor_publisher_post_pulitzer_1921", "THE POST WINS THE PULITZER · JUNE 1921", "EDITOR & PUBLISHER, 4 JUNE 1921")),
    ]),
    dict(id="bill", title="THE BILL", beats=[
        ("When it was over, the bill was enormous. Tens of thousands of people had handed him somewhere between ten and fifteen million dollars, in nineteen-twenty money.",
         ("num", "$10–15M", "FROM TENS OF THOUSANDS OF PEOPLE · 1920 DOLLARS")),
        ("The Hanover Trust failed, and five other banks went down with it.",
         ("photo", "hanover_trust_closed_1920", "THE HANOVER TRUST, CLOSED · AUGUST 1920", "UNDERWOOD · LESLIE'S WEEKLY, 1920")),
        ("Years later, his investors got back about thirty cents on the dollar.",
         ("num", "ABOUT 30¢", "ON THE DOLLAR, YEARS LATER · ACCOUNTS DIFFER")),
        ("Ponzi pleaded guilty to a single count of mail fraud, and was sentenced to five years.",
         ("photo", "ponzi_under_arrest_1920", "PONZI IN CUSTODY · AUGUST 1920", "INTERNATIONAL · LESLIE'S WEEKLY, 1920")),
        ("But Massachusetts had charges of its own, and didn't want to wait. Could a state put a federal prisoner on trial?",
         ("photo", "j_weston_allen_attorney_general", "J. WESTON ALLEN, STATE ATTORNEY GENERAL · c. 1920", "BAIN NEWS SERVICE · LIBRARY OF CONGRESS")),
        ("The question went all the way to the Supreme Court. Massachusetts won.",
         ("words", "MASSACHUSETTS WON")),
        ("It took three trials, but in nineteen twenty-five he was given seven to nine years more.",
         ("num", "7–9 YEARS", "MORE · MASSACHUSETTS, 1925")),
    ]),
    dict(id="again", title="HE TRIED AGAIN", beats=[
        ("But Charles Ponzi wasn't finished. Out on bail in nineteen twenty-five, he went to Florida, in the middle of a land boom, and started selling plots of land. Some of it was under water.",
         ("img", "g02", "FLORIDA · 1925 · RECONSTRUCTION")),
        ("His promise this time, by one account: two hundred percent, in sixty days.",
         ("img", "g01")),
        ("He was convicted of fraud in Florida, jumped bail, and signed on as a crewman on a ship bound for Italy. The story goes that he shaved his head.",
         ("list", ["CONVICTED IN FLORIDA", "JUMPED BAIL", "SIGNED ON AS CREW"])),
        ("A deputy sheriff caught up with the ship at New Orleans, and arrested him there.",
         ("img", "g03", "NEW ORLEANS · RECONSTRUCTION")),
        ("He served his years in Massachusetts. And in nineteen thirty-four, the United States deported him to Italy.",
         ("img", "g04", "1934 · RECONSTRUCTION")),
        ("He had first landed in America thirty-one years earlier, and never become a citizen.",
         ("num", "31 YEARS", "SINCE HE FIRST LANDED · NEVER A CITIZEN")),
        ("Rose stayed behind in Boston. A few years later, she divorced him.",
         ("photo", "rose_ponzi_and_mother_1920", "ROSE PONZI, WITH HIS MOTHER · 1920", "UNDERWOOD · LESLIE'S WEEKLY, 1920")),
    ]),
    dict(id="end", title="CHEAP AT THE PRICE", beats=[
        ("His last job was in Brazil, working for an Italian airline. The war closed it down, and he was left with nothing.",
         ("img", "e01")),
        ("Charles Ponzi died in January nineteen forty-nine, in a charity ward in Rio de Janeiro. He was half blind, and partly paralysed.",
         ("img", "e02", "RIO DE JANEIRO · JANUARY 1949 · RECONSTRUCTION")),
        ("He left seventy-five dollars, barely enough for his funeral.",
         ("num", "$75", "ALL HE LEFT · BARELY ENOUGH FOR HIS FUNERAL")),
        ("Near the end, he still had a line ready. Even if they never got anything for it, he said, it was cheap at that price.",
         ("photo", "ponzi_straw_hat_1920", "\"CHEAP AT THAT PRICE\"", "KEYSTONE VIEW CO. · THE LITERARY DIGEST, 1920")),
        ("It was easily worth fifteen million bucks to watch me put the thing over.",
         ("quote", "It was easily worth fifteen million bucks to watch me put the thing over.", "CHARLES PONZI · LATE-LIFE INTERVIEW")),
        ("Look at what he actually built. A return too good to refuse. A story too complicated to check.",
         ("photo", "school_street_crowd_1920", "TOO GOOD TO REFUSE", "UNDERWOOD & UNDERWOOD · MID-WEEK PICTORIAL, 1920")),
        ("The first investors paid, so they become the salesmen. And money that only keeps coming while new money keeps arriving.",
         ("list", ["A RETURN TOO GOOD TO REFUSE", "A STORY TOO COMPLICATED TO CHECK", "FIRST INVESTORS PAID", "NEW MONEY PAYS THE OLD"], "WHAT HE BUILT")),
        ("Eighty-eight years after Boston, a respected New York investor called Bernie Madoff confessed that his fund was the same trick, on a far bigger scale.",
         ("photo", "ponzi_portrait_bain_1920", "88 YEARS LATER · THE SAME TRICK", "BAIN NEWS SERVICE · LIBRARY OF CONGRESS")),
        ("On paper, by the widely reported figure, his investors' accounts held about sixty-five billion dollars. Most of it had never existed.",
         ("words", "MOST OF IT NEVER EXISTED")),
        ("The coupons have become crypto coins, trading bots and foreign exchange. The promise is still the same.",
         ("img", "e04")),
        ("So when someone offers you a return that sounds too good to be true, ask the question the Boston Post asked, more than a hundred years ago.",
         ("img", "e05")),
        ("Not, how much will I make. But, where is the money coming from?",
         ("words", "WHERE IS THE MONEY COMING FROM?")),
    ]),
]
