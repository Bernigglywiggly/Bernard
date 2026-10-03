"""Shorts cut from LF02 (lab/longform/vertical.py, The Curve's theme): the film's picture framed in 9:16 with a
headline, live captions and an end card that sends viewers to the full film."""
FILM = "The Price of Thinking"
TAGS = "#ai #chatgpt #claude #technews #artificialintelligence"
THEME = "curve"
SHORTS = {
    "war": dict(t0=0.6, t1=42.6, headline="Two AI labs cut prices in one afternoon", film=FILM,
                title="Two AI Labs Cut Their Prices Within an Hour of Each Other",
                caption="One cut by a fifth. The other answered by half. So why is AI spending over a trillion dollars? " + TAGS,
                pinned="Every source is in the full film's description: The Price of Thinking, on the channel."),
    "bigmac": dict(t0=195.2, t1=252.0, headline="What AI really costs, in Big Macs", film=FILM,
                   title="What AI Really Costs Now, in Big Macs",
                   caption="In 2021, a machine reading eight novels cost ten Big Macs. Now one Big Mac buys about five hundred. " + TAGS,
                   pinned="Full film on the channel: The Price of Thinking."),
    "jevons": dict(t0=339.3, t1=399.8, headline="Cheaper AI means a bigger bill", film=FILM,
                   title="The 1865 Paradox That Explains AI Spending",
                   caption="Jevons saw it with coal. Google's token count went up more than 300 times in two years. " + TAGS,
                   pinned="Is cheaper AI saving money or just making us use more of it? Full film on the channel."),
}
