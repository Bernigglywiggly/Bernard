"""MONEY CRIMES · long-form 02: "The Original Ponzi Scheme" (Charles Ponzi, 1882-1949). Narrated by Imogen, as film 01.

Facts (checked 3 Oct 2026): Wikipedia (Charles Ponzi; Richard Grozier; William McMasters), Smithsonian Magazine ("In
Ponzi We Trust"), Boston.com ("95 years ago, the original Ponzi scheme fell apart", 2015), and on Madoff, Wikipedia
(Bernie Madoff). Where sources differ the script takes the cautious line: the takings are "ten to fifteen million
dollars" from "tens of thousands" of people (Boston.com: about $10M from about 20,000; Smithsonian: about $15M from about
40,000), the peak "as much as a quarter of a million dollars a day" (Boston.com), the swamp "the story goes". Ponzi's
own lines are said to be his ("he later said"). Each chapter is a YouTube chapter.
"""
CHAPTERS = [
    dict(id="open", title="Cold open", paras=[
        "Boston, July 1920. A line of people, four abreast, stretches from City Hall to School Street. Working people, "
        "mostly. Some of them have put in their life savings.",
        "They're not here to invest. They're here to get their money back. That morning, the city's biggest newspaper "
        "has asked a question nobody wanted to ask: where is the money coming from?",
        "And walking up and down the line, in an immaculate suit, is the man who has their money. He's "
        "handing out coffee and doughnuts. He's telling them they have nothing to worry about.",
        "And he pays them. Every one of them.",
        "His name was Charles Ponzi. He didn't invent the trick. But he ran it so spectacularly that it has carried his "
        "name ever since. This is how it worked, how it fell apart, and why it's still running today.",
    ]),
    dict(id="arrive", title="Two dollars and fifty cents", paras=[
        "Carlo Ponzi was born on the third of March, 1882, in Lugo, a small town in northern Italy. His family had "
        "known better days, and they wanted him to restore them. He went to university in Rome, where his richer friends "
        "treated it as a four-year holiday. He followed them to the bars, the cafés and the opera.",
        "In November 1903, he arrived in Boston on a steamship. He had gambled away almost everything on the crossing. "
        "He stepped onto the dock with two dollars and fifty cents.",
        "He later said he landed with two dollars fifty in cash, and a million dollars in hopes. And the hopes never "
        "left him.",
        "He washed dishes. He waited tables, and slept on the restaurant floor. He was promoted, and then fired, for "
        "short-changing the customers and stealing from the till.",
        "For a man who wanted to be rich, America was turning out to be very hard work.",
    ]),
    dict(id="montreal", title="Robbing Peter", paras=[
        "In 1907, he moved to Montreal, and found a job at a small bank run by Luigi Zarossi, which served the city's "
        "Italian immigrants. Zarossi's bank paid six percent interest. Twice what other banks paid.",
        "Ponzi rose to assistant manager, and discovered how it was done. The interest wasn't coming from profits. The "
        "bank was in trouble. Old customers were being paid with new customers' deposits.",
        "Robbing Peter to pay Paul. Ponzi watched it closely. And he watched what happened when it stopped working. The "
        "bank collapsed, and Zarossi fled to Mexico with much of the money that was left.",
        "Broke again, Ponzi forged a cheque for four hundred and twenty-three dollars and fifty-eight cents. He was "
        "caught almost at once, and sent to a Quebec penitentiary.",
        "Out of prison, he crossed back into the United States, and was caught again, this time smuggling Italian "
        "immigrants over the border. Two more years, in the federal prison in Atlanta.",
        "There, he met Charles Morse, a Wall Street millionaire serving time for fraud. Morse fooled the prison doctors "
        "by eating soap shavings, to make himself look gravely ill. He was soon released.",
        "Ponzi was paying attention. Appearances, he was learning, are worth more than facts.",
    ]),
    dict(id="coupon", title="The coupon", paras=[
        "By 1919, he was back in Boston, married to a young woman called Rose Gnecco, and still poor. Then, one day, "
        "a letter arrived from a company in Spain. Inside was a small slip of paper.",
        "It was an international reply coupon. You could buy one at a post office in one country, and post it abroad. "
        "The person who received it could swap it for stamps, so they could write back for free.",
        "The exchange rates had been fixed by international agreement, before the First World War. After the war, "
        "money across Europe collapsed in value. The coupons didn't.",
        "So a coupon bought cheaply in Spain, or Italy, could be swapped in America for stamps worth more than it cost. "
        "On paper, it was a profit. And on paper, it was perfectly legal.",
        "Ponzi did the sums and saw a fortune. He told people the margin could be four hundred percent.",
        "There was one problem. You can't spend stamps. To turn a profit into cash, you'd have to buy coupons by the "
        "hundred thousand, ship them across the ocean, swap them for stamps, and then sell a mountain of stamps. Nobody "
        "could do that. Ponzi never really tried.",
    ]),
    dict(id="promise", title="Fifty percent in forty-five days", paras=[
        "At the start of 1920, he set up the Securities Exchange Company, and made a promise. Give him your money, and "
        "in forty-five days he would pay you back with fifty percent on top. Wait ninety days, and he would double it.",
        "In the first month, eighteen people took the chance. Between them, they put in eighteen hundred dollars.",
        "And then Ponzi did something that made everything else possible. He paid them. On time, and in full.",
        "The money didn't come from coupons. It came from the next investors. But the first investors didn't know that. "
        "All they knew was that it worked. So they told their friends. And their friends told theirs.",
        "That was the whole machine. Every happy customer became a salesman, and every salesman brought in the money "
        "to pay the last one.",
        "By May, he had taken in four hundred and twenty thousand dollars. By June, two and a half million. By July, "
        "by some accounts, as much as a quarter of a million dollars was arriving every day.",
    ]),
    dict(id="king", title="The king of School Street", paras=[
        "Ponzi was five foot two, and suddenly he was the most famous man in Boston.",
        "He bought a twelve-room mansion in Lexington, a custom-built limousine, and gold-handled canes. He bought "
        "Rose diamonds. Crowds followed him in the street, and called him a genius.",
        "He wanted more than money. He wanted to be a banker. He poured millions of his investors' dollars into the "
        "Hanover Trust Company, until he had bought a controlling interest in the bank itself.",
        "And most of his investors never asked for their profits. Why would they? It was easier to leave the money "
        "where it was, and watch it grow. On paper.",
    ]),
    dict(id="post", title="The question", paras=[
        "On the twenty-fourth of July, 1920, the Boston Post put him on its front page. Doubles the money within three "
        "months, said the headline. Thousands more came running.",
        "But at the Post, the young acting publisher, Richard Grozier, had doubts. Two days later, his paper started "
        "asking questions.",
        "Then Clarence Barron, the most respected financial journalist in America, did the arithmetic. To cover what "
        "Ponzi had taken in, about one hundred and sixty million postal reply coupons would have had to be in "
        "circulation. There were only about twenty-seven thousand.",
        "And Barron noticed one more thing. Ponzi, the man who promised everyone fifty percent, wasn't putting his own "
        "money into his own scheme.",
    ]),
    dict(id="run", title="The run", paras=[
        "The morning the questions appeared, the crowd came to School Street. Not to invest. To get out.",
        "And this is where Ponzi was at his most brilliant. He didn't hide. He opened the doors, and paid. Over three "
        "days, around two million dollars went back out of the window.",
        "He walked the line, handing out coffee and doughnuts, smiling, joking, telling them there was nothing to worry "
        "about.",
        "It worked. People who saw the money being paid out so easily decided it must be safe. Some of them turned "
        "round, and invested again.",
        "Ponzi had survived the run. But he couldn't survive arithmetic.",
    ]),
    dict(id="fall", title="Hopelessly insolvent", paras=[
        "The end came from inside. Ponzi had hired a publicity agent, a former newspaperman called William McMasters. "
        "McMasters looked at the books, and went to the Post.",
        "On the second of August, the Post printed his verdict on its front page. Ponzi was hopelessly insolvent. "
        "Millions of dollars in debt.",
        "Auditors moved in. The hole kept getting deeper.",
        "Then, on the eleventh of August, the Post found his past. Montreal. Zarossi's bank. The forged cheque. The prison "
        "photograph of the man Boston had called a genius.",
        "The same day, the state's banking commissioner seized the Hanover Trust. Within days, Ponzi gave himself up to "
        "federal agents.",
        "The paper that asked the question won the Pulitzer Prize.",
    ]),
    dict(id="bill", title="The bill", paras=[
        "When it was over, the bill was enormous. Tens of thousands of people had handed him somewhere between ten and "
        "fifteen million dollars, in nineteen-twenty money. The Hanover Trust failed, and five other banks went down "
        "with it.",
        "Years later, his investors got back less than thirty cents on the dollar.",
        "Ponzi pleaded guilty to a single count of mail fraud, and was sentenced to five years in federal prison. When "
        "he came out, the state of Massachusetts was waiting, with charges of its own. The case went all the way to the "
        "Supreme Court. Massachusetts won. Seven to nine years more.",
    ]),
    dict(id="again", title="He tried again", paras=[
        "But Charles Ponzi wasn't finished. Out on bail in 1925, he went to Florida, in the middle of a land boom, and "
        "started selling plots of land. Some of it, the story goes, was under water.",
        "His promise this time: two hundred percent, in sixty days.",
        "He was convicted of fraud in Florida, jumped bail, shaved his head, and signed on as a crewman on a ship bound "
        "for Italy. A deputy sheriff followed the ship to its last American port, New Orleans, and arrested him there.",
        "He served his years in Massachusetts. And in 1934, the United States deported him to Italy. He had lived in "
        "America for thirty years, and never become a citizen. Rose stayed behind. A few years later, she divorced him.",
    ]),
    dict(id="end", title="Cheap at the price", paras=[
        "His last job was in Brazil, working for Italy's state airline. When Brazil joined the war against Italy, the "
        "airline was shut down, and he was left with nothing.",
        "Charles Ponzi died on the eighteenth of January, 1949, in a charity ward in Rio de Janeiro. He was half blind, "
        "and partly paralysed. He left seventy-five dollars, barely enough for his funeral.",
        "Near the end, he still had a line ready. Even if they never got anything for it, he said, it was cheap at that "
        "price. It was easily worth fifteen million bucks to watch me put the thing over.",
        "Look at what he actually built. A return too good to refuse. A story too complicated to check. The first "
        "investors paid, so they become the salesmen. And money that only keeps coming while new money keeps arriving.",
        "Eighty-eight years after Boston, a respected New York investor called Bernie Madoff confessed that his fund was "
        "the same trick, on a far bigger scale. On paper, his investors' accounts held about sixty-five billion dollars. "
        "Most of it had never existed.",
        "The coupons have become crypto coins, trading bots and foreign exchange. The promise is still the same.",
        "So when someone offers you a return that sounds too good to be true, ask the question the Boston Post asked, "
        "more than a hundred years ago. Not how much will I make. Where is the money coming from?",
    ]),
]


def parts(limit=1350):
    """TTS takes: each chapter's paragraphs packed into reads of at most `limit` characters. [(chapter id, part, text)]"""
    out = []
    for ch in CHAPTERS:
        cur, k = [], 0
        for p in ch["paras"]:
            if cur and len(" ".join(cur + [p])) > limit:
                out.append((ch["id"], k, "\n\n".join(cur)))
                cur, k = [], k + 1
            cur.append(p)
        out.append((ch["id"], k, "\n\n".join(cur)))
    return out


if __name__ == "__main__":
    n = sum(len(" ".join(c["paras"]).split()) for c in CHAPTERS)
    print(n, "words,", round(n / 146, 1), "min at Imogen's 146 wpm")
    for cid, k, t in parts():
        print(f"{cid}.{k}", len(t), "chars")
