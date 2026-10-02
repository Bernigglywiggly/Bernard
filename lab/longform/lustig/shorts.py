"""Shorts cut from the long-form (../vertical.py): the stretch of film, a headline, the card that sends to the full film,
and the copy for TikTok, YouTube Shorts and Reels (link the full film as the Short's related video on YouTube)."""
FILM = "The Man Who Sold the Eiffel Tower"
TAGS = "#truecrime #history #conartist #scam"
SHORTS = {
    "capone": dict(t0=496.6, t1=561.6, headline="He conned Al Capone. And lived.", film=FILM,
                   title="He Conned Al Capone by Giving the Money Back",
                   caption="He borrowed $50,000 from Al Capone... and gave every dollar back. That was the con. " + TAGS,
                   pinned="Would you have tried this on Capone? Full story: The Man Who Sold the Eiffel Tower, on the channel."),
    "escape": dict(t0=669.7, t1=734.4, headline="He escaped jail dressed as a window cleaner", film=FILM,
                   title="He Escaped Jail by Pretending to Clean the Windows",
                   caption="A bedsheet rope, a rag, and a man calmly 'cleaning windows' down the side of a federal jail. " + TAGS,
                   pinned="27 days of freedom. Full story: The Man Who Sold the Eiffel Tower, on the channel."),
    "box": dict(t0=162.3, t1=237.0, headline="The box that 'printed' money", film=FILM,
                title="The Money-Printing Machine That Fooled Everyone",
                caption="Feed in a $100 bill, wait six hours, get two. The con man's 'money machine', explained. " + TAGS,
                pinned="Would you have bought one? Full story: The Man Who Sold the Eiffel Tower, on the channel."),
}
