"""MONEY CRIMES · long-form 01: "The Man Who Sold the Eiffel Tower" (Victor Lustig, 1890-1947). Narrated by Imogen.

Facts: Wikipedia (Victor Lustig), checked against History Facts, the Mob Museum and contemporary-press summaries. Where
sources differ the script takes the cautious line: the second Eiffel attempt failed (the buyer went to the police), the
Capone story is told as "the story goes", the Ten Commandments are "said to" be his. Each chapter is a YouTube chapter.
"""
CHAPTERS = [
    dict(id="open", title="Cold open", paras=[
        "Paris, 1925. Six of the biggest scrap-metal dealers in France receive a letter on government paper. It's marked "
        "confidential. It invites them to a private meeting at the Hôtel de Crillon, one of the grandest hotels in the city.",
        "Waiting for them is a man from the Ministry of Posts and Telegraphs. Elegant. Softly spoken. A thin scar on his "
        "left cheek.",
        "He tells them a secret. The Eiffel Tower is coming down. And one of them is going to buy it.",
        "None of it is true. The tower isn't for sale. And the man is not who he says he is.",
        "His name is Victor Lustig. Before he was finished, he would sell the Eiffel Tower, con Al Capone and live to tell "
        "the tale, flood America with fake money, and climb out of a federal jail on a rope made of bedsheets.",
        "This is how he did it. And why the same trick still works today.",
    ]),
    dict(id="boy", title="A boy from Bohemia", paras=[
        "Victor Lustig was born on the fourth of January, 1890, in Hostinné, a small town in Bohemia, then part of the "
        "Austro-Hungarian Empire. His father sold tobacco and had once been the town's mayor. He was also, by most "
        "accounts, a violent man.",
        "Victor was clever, restless, and impossible to keep in school. He was thrown out of his first one for swearing, "
        "and sent away to a boarding school in Dresden. He collected languages the way other boys collected bad habits. "
        "German. French. English. Italian. Hungarian.",
        "In 1909 he went to Paris, to study at the Sorbonne. He barely lasted a semester. He'd found something far more "
        "interesting than lectures. The card tables.",
        "Gambling taught him the one skill he would use for the rest of his life: reading people. Who was bluffing. Who "
        "was desperate. And who simply wanted to believe.",
        "Around the same time, a jealous rival slashed his face. He wore that scar on his left cheek until the day he died.",
        "Then he went to sea. On the great liners crossing the Atlantic, he posed as a Broadway producer, looking for "
        "investors in a show that didn't exist. Rich passengers. Long voyages. And nobody can check your story in the "
        "middle of the ocean.",
        "When the First World War shut the liners down, he took his act to America. And there, he started selling a box.",
    ]),
    dict(id="box", title="The money box", paras=[
        "It was called the Rumanian Box: a handsome mahogany case with two narrow slots and a row of brass dials. Lustig "
        "said it could copy money.",
        "You fed in a real banknote and a blank sheet of paper. You waited six hours while the chemicals did their work. "
        "And out came two identical notes.",
        "It was a perfect demonstration, because the second note was real. Lustig had hidden it inside in advance. He'd "
        "even walk the buyer to a bank, so a teller could confirm the money was genuine.",
        "Then he'd sell them the machine, for thousands of dollars. He'd load it with a few more real notes, so it kept "
        "working just long enough for him to leave town. After that, it printed nothing but blank paper.",
        "And here's the beautiful part. His victims almost never went to the police. What would they say? That someone "
        "had cheated them out of their illegal money-printing machine?",
        "One man did come after him: a sheriff in Texas, who chased Lustig all the way to Chicago. Lustig talked him "
        "down, apologised, and handed him a thick roll of cash to make up for it. Counterfeit cash.",
        "In 1922, under the name Robert Duval, he walked out of a bank in Springfield, Missouri, with ten thousand dollars.",
        "Remember that town. We'll be coming back to it.",
    ]),
    dict(id="tower", title="The tower nobody wanted", paras=[
        "By 1925, Lustig was back in Paris. And one morning he read a short newspaper story that gave him the idea of his "
        "life.",
        "The Eiffel Tower was in trouble.",
        "It had been built for the World's Fair of 1889, and it was never meant to last. Its permit ran for just twenty "
        "years. Some of the most famous artists in France had called it a monstrosity. It survived partly because it made "
        "such a useful radio mast.",
        "Now it was rusting. It needed repainting, the bills were enormous, and the article wondered how long Paris could "
        "keep paying them.",
        "Most people read that and turned the page. Victor Lustig read it and asked a different question.",
        "If the tower came down... who would buy seven thousand tonnes of iron?",
    ]),
    dict(id="sale", title="The sale", paras=[
        "First, he needed to become a government official. He hired a forger to make him official stationery, and he "
        "gave himself a title: Deputy Director-General of the Ministry of Posts and Telegraphs.",
        "Then he wrote to six of the biggest scrap-metal dealers in Paris, and invited them to the Crillon.",
        "His pitch was simple. The city could no longer afford the tower. It would be sold for scrap, to the highest "
        "bidder. These men had been chosen because they were honest businessmen. And because the public would be "
        "outraged, nobody could know until the deal was done.",
        "That last part was the genius of it. The secrecy explained everything that should have looked wrong. Why they "
        "were meeting in a hotel and not a ministry. Why nobody could check with anyone. Why it all had to move so fast.",
        "Then he took them to see the tower, in rented limousines.",
        "But Lustig wasn't really looking at the tower. He was watching the dealers. And one of them stood out.",
        "André Poisson was successful, but in Paris business circles he felt like an outsider. He wanted to be taken "
        "seriously. And the man who bought the Eiffel Tower would never be an outsider again.",
        "Poisson wanted it. But he had doubts. Why the secrecy? Why the rush? Was this man really who he said he was?",
        "So Lustig did something brilliant. He confessed.",
        "At a second meeting, he admitted, a little awkwardly, that a government official's salary wasn't much. That a "
        "man in his position had expenses. That a deal this size might need... a little encouragement.",
        "He was asking for a bribe.",
        "And Poisson relaxed. Because now it all made sense. A crooked official, quietly looking after himself? That, "
        "Poisson understood. Nobody would make that up.",
        "He paid the bribe. Then he paid for the tower: about seventy thousand francs.",
        "And Victor Lustig caught a train to Austria, with a suitcase full of cash.",
    ]),
    dict(id="back", title="He came back", paras=[
        "Then he waited. Every day he checked the Paris newspapers, looking for the scandal.",
        "It never came.",
        "Poisson never went to the police. Admitting he'd been fooled would have destroyed the very reputation he'd been "
        "trying to buy.",
        "So Lustig did the boldest thing of all. A month later, he came back to Paris, picked six new dealers... and tried "
        "to sell the same tower again.",
        "This time, it went wrong. One of the dealers went to the police. Lustig slipped away before they could arrest "
        "him, and he put as much distance between himself and France as he possibly could.",
        "He went to America.",
    ]),
    dict(id="capone", title="The man who conned Capone", paras=[
        "In America, the story goes, he picked the most dangerous mark in the country. Al Capone.",
        "He asked Capone for fifty thousand dollars to invest in a scheme, and promised to double it in two months. "
        "Capone handed it over.",
        "And Lustig did... nothing. He put the money in a safe-deposit box, and left it there.",
        "Two months later, he went back to Capone, full of apologies. The deal had fallen through. And he handed back "
        "every single dollar.",
        "Capone was stunned. People didn't usually give him his money back. Impressed by this rare honest man, he gave "
        "Lustig five thousand dollars to tide him over.",
        "Which had been the plan all along. Stealing fifty thousand dollars from Al Capone would have got him killed. "
        "Lustig wanted Capone to give him money. And to thank him for it.",
        "Whether it really happened like that, nobody can prove. But it's the most Lustig story there is.",
    ]),
    dict(id="money", title="Lustig money", paras=[
        "By 1930, he'd found something bigger than any single con. Instead of pretending to print money... he started "
        "printing it.",
        "He teamed up with two men from Nebraska: a pharmacist called William Watts, and a chemist called Tom Shaw. They "
        "engraved the plates. Lustig built the business: a ring of couriers who carried the notes across the country, "
        "and spent them.",
        "For five years, thousands of dollars in fake notes poured into the American economy every month, in the depths "
        "of the Great Depression. The money even had a nickname. Lustig money.",
        "The Secret Service went hunting for the man behind it. But in the end, it wasn't the government that brought "
        "Victor Lustig down.",
        "It was a woman.",
    ]),
    dict(id="locker", title="The locker", paras=[
        "Lustig had a mistress, Billy May. And she found out he was seeing a younger woman.",
        "So Billy May picked up the phone. She made an anonymous call to the federal authorities, and told them where to "
        "find him.",
        "On the tenth of May, 1935, agents arrested Victor Lustig in New York. On him, they found a key. It opened a "
        "locker at the Times Square subway station. Inside were fifty-one thousand dollars in counterfeit notes... and "
        "the plates used to print them.",
        "He was locked in a third-floor cell at the Federal House of Detention in Manhattan, to wait for his trial. The "
        "building was said to be escape-proof.",
        "On the first of September, 1935, the day before that trial, Victor Lustig escaped.",
    ]),
    dict(id="escape", title="The escape", paras=[
        "He told the guards he was ill. And when no one was watching, he knotted his bedsheets into a rope, climbed out "
        "of the window, and lowered himself down the side of the building.",
        "People in the street below looked up and saw a man calmly wiping the windows on his way down. Just a window "
        "cleaner, doing his job.",
        "He was free for twenty-seven days. Then the police caught up with him in Pittsburgh.",
        "This time, there was no talking his way out. Lustig pleaded guilty. On the ninth of December, 1935, he was "
        "sentenced to fifteen years for counterfeiting, and five more for the escape.",
        "He would serve them on the most famous prison island in America.",
        "Alcatraz.",
    ]),
    dict(id="rock", title="The Rock", paras=[
        "The man who had stayed in the finest hotels in Europe now lived in a cell on a rock in San Francisco Bay.",
        "He spent the next twelve years in federal custody. In March 1947, at the federal prison hospital in "
        "Springfield, Missouri, he caught pneumonia. Two days later, he was dead. He was fifty-seven.",
        "Springfield, Missouri. The same town where, a quarter of a century earlier, a man calling himself Robert Duval "
        "had walked out of a bank with ten thousand dollars.",
        "Even his death certificate was a disguise. It didn't say Victor Lustig. It said Robert V. Miller. Occupation: "
        "apprentice salesman.",
        "The greatest salesman of his age. An apprentice.",
    ]),
    dict(id="rules", title="The con man's commandments", paras=[
        "So how did he do it? Lustig is said to have left behind a set of rules, the Ten Commandments for Con Men. And "
        "almost none of them are about lying.",
        "Be a patient listener. Never look bored. Wait for the other person to reveal their politics, then agree with "
        "them. Never boast; just let your importance be quietly obvious. Never be untidy. Never get drunk.",
        "It isn't a guide to fooling people. It's a guide to being trusted.",
        "Now look at the Eiffel Tower con again. An official title. A secret nobody else could know. A deadline. A reason "
        "not to check. And a victim who wanted something so badly that he helped fool himself.",
        "It's the same playbook behind the scams on your phone today. The text that claims to be from your bank, telling "
        "you to act now and tell no one. The investment only insiders know about. The official who needs a small fee "
        "before he can release your money.",
        "The costumes have changed. The trick hasn't.",
        "Victor Lustig sold the Eiffel Tower. It's still standing: seven thousand tonnes of iron that was never his to sell.",
        "And somewhere, right now, someone is selling it again.",
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
