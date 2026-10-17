"""Shorts cut from the long-form (../vertical.py): the stretch of film, a headline, the card that sends to the full film,
and the copy for TikTok, YouTube Shorts and Reels (link the full film as the Short's related video on YouTube). `music`
names the film's jazz cues inside each stretch (music.py), for the CC BY credit in its description."""
FILM = "The Man Who Sold the Eiffel Tower"
TAGS = "#truecrime #history #conartist #scam"
SHORTS = {
    "capone": dict(t0=496.6, t1=561.6, headline="He conned Al Capone. And lived.", film=FILM, music=["On the Cool Side"],
                   title="He Conned Al Capone by Giving the Money Back",
                   caption="He borrowed $50,000 from Al Capone... and gave every dollar back. That was the con. " + TAGS,
                   pinned="Would you have tried this on Capone? Full story: The Man Who Sold the Eiffel Tower, on the channel."),
    "escape": dict(t0=669.7, t1=734.4, headline="He escaped jail dressed as a window cleaner", film=FILM,
                   music=["Walking Along", "Faster Does It"],
                   title="He Escaped Jail by Pretending to Clean the Windows",
                   caption="A bedsheet rope, a rag, and a man calmly 'cleaning windows' down the side of a federal jail. " + TAGS,
                   pinned="27 days of freedom. Full story: The Man Who Sold the Eiffel Tower, on the channel."),
    "box": dict(t0=162.3, t1=237.0, headline="The box that 'printed' money", film=FILM, music=["Spy Glass"],
                title="The Money-Printing Machine That Fooled Everyone",
                caption="Feed in a $100 bill, wait six hours, get two. The con man's 'money machine', explained. " + TAGS,
                pinned="Would you have bought one? Full story: The Man Who Sold the Eiffel Tower, on the channel."),
    "bribe": dict(t0=376.4, t1=437.6, headline="He asked for a bribe. That's what sold it.", film=FILM,
                  music=["Dances and Dames"],
                  title="The Confession That Sold the Eiffel Tower",
                  caption="The buyer had doubts. So the con man confessed to being corrupt, and the doubts vanished. " + TAGS,
                  pinned="Would a bribe have convinced you? Full story: The Man Who Sold the Eiffel Tower, on the channel."),
    "certificate": dict(t0=745.4, t1=792.7, headline="Even his death certificate was a disguise", film=FILM,
                        music=["Night on the Docks - Trumpet"],
                        title="The Greatest Con Man's Death Certificate Was Still a Lie",
                        caption="It didn't say Victor Lustig. Occupation: apprentice salesman... and counterfeiter. " + TAGS,
                        pinned="The man who sold the Eiffel Tower, an apprentice. Full story on the channel."),
    "rules": dict(t0=797.8, t1=842.7, headline="The con man's ten commandments", film=FILM, music=["Acid Trumpet"],
                  title="The Ten Commandments for Con Men (and Why They Still Work)",
                  caption="Be a patient listener. Never look bored. Never boast. It isn't a guide to fooling people. "
                          "It's a guide to being trusted. " + TAGS,
                  pinned="Which rule have you seen a scammer use on you? Full story on the channel."),
}
