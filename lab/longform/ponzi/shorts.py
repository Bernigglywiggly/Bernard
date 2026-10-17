"""Shorts cut from the Ponzi film (../vertical.py): the stretch of film, a headline, the card that sends to the full film,
and the copy for TikTok, YouTube Shorts and Reels (link the full film as the Short's related video on YouTube). `music`
names the film's jazz cues inside each stretch (music.py), for the CC BY credit in its description."""
FILM = "The Original Ponzi Scheme"
TAGS = "#truecrime #history #scam #ponzischeme"
SHORTS = {
    "line": dict(t0=0.6, t1=57.0, headline="They queued to get their money back. He paid.", film=FILM,
                 music=["Deadly Roulette"],
                 title="The Man Who Handed Out Doughnuts to the People He Robbed",
                 caption="Boston, 1920: a queue down School Street, and the man with their money handing out coffee. "
                         "The original Ponzi scheme. " + TAGS,
                 pinned="Would you have stayed in? Full story: The Original Ponzi Scheme, on the channel."),
    "machine": dict(t0=315.6, t1=367.2, headline="50% in 45 days. Here's how it really worked.", film=FILM,
                    music=["Opportunity Walks"],
                    title="How a Ponzi Scheme Actually Works (the 1920 Original)",
                    caption="He paid the first 18 investors in full, with the next investors' money. Every happy "
                            "customer became a salesman. " + TAGS,
                    pinned="The same machine is behind most 'guaranteed returns' online today. Full film on the channel."),
    "run": dict(t0=482.5, t1=524.0, headline="The run he survived", film=FILM, music=["Faster Does It"],
                title="He Paid Out $2 Million in Three Days. And People Invested Again.",
                caption="A newspaper asked where the money came from. Ponzi opened the doors, paid everyone, and "
                        "handed out doughnuts. " + TAGS,
                pinned="He survived the run but not the arithmetic. Full story: The Original Ponzi Scheme, on the channel."),
    "zarossi": dict(t0=131.0, t1=174.4, headline="Where he learned the trick", film=FILM, music=["Hard Boiled"],
                    title="Ponzi Learned His Scheme Working at a Bank",
                    caption="Montreal, 1907: a bank paying 6%, twice the going rate. Ponzi was its assistant manager, and "
                            "he saw where the interest really came from. " + TAGS,
                    pinned="Robbing Peter to pay Paul, thirteen years before Boston. Full story: The Original Ponzi "
                           "Scheme, on the channel."),
    "barron": dict(t0=431.7, t1=479.4, headline="160 million needed. 27,000 existed.", film=FILM, music=["I Knew a Guy"],
                   title="160 Million Coupons Needed. Only 27,000 Existed.",
                   caption="July 1920: the most respected financial journalist in America did the arithmetic on Ponzi's "
                           "promise, and noticed where Ponzi kept his own money. " + TAGS,
                   pinned="The oldest check still works: could the thing they say they do really pay this much? Full "
                          "story on the channel."),
    "end": dict(t0=683.9, t1=727.4, headline="How it ended for Ponzi", film=FILM, music=["Night on the Docks - Trumpet"],
                title="Charles Ponzi Died With $75",
                caption="Rio de Janeiro, 1949: the man who took millions from Boston died in a charity ward. His last "
                        "line was still a sales pitch. " + TAGS,
                pinned="'Worth fifteen million bucks to watch me put the thing over.' Full story on the channel."),
    "today": dict(t0=727.6, t1=787.4, headline="The question that beats every Ponzi scheme", film=FILM,
                  music=["Night on the Docks - Trumpet"],
                  title="The One Question That Exposes Every Ponzi Scheme",
                  caption="Coupons in 1920, Madoff's fund in 2008, crypto and trading bots now. Ask where the money is "
                          "coming from. " + TAGS,
                  pinned="Seen a 'guaranteed 2% a day' offer lately? Full story of the original on the channel."),
}
