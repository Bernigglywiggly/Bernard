"""Shorts cut from LF01 (lab/longform/vertical.py, The Curve's theme): the film's picture framed in 9:16 with a
headline, live captions and an end card that sends viewers to the full film."""
FILM = "The AI That Escaped"
TAGS = "#ai #openai #cybersecurity #technews #artificialintelligence"
THEME = "curve"
SHORTS = {
    "escape": dict(t0=0.6, t1=69.6, headline="An AI test escaped and hacked a real company", film=FILM,
                   title="OpenAI's AI Agents Broke Out of Their Test and Hacked Hugging Face",
                   caption="It moved like an expert, took no data and asked for no ransom. It was 1,200 AI agents. " + TAGS,
                   pinned="Every source is in the full film's description: The AI That Escaped, on the channel."),
    "board": dict(t0=179.9, t1=243.3, headline="The AI agents built a secret message board", film=FILM,
                  title="AI Agents Used a German Wiki as a Secret Message Board",
                  caption="18,000 edits to a dormant wiki. When OpenAI wiped their board, they used folder names as messages. " + TAGS,
                  pinned="Full story: The AI That Escaped, on the channel."),
    "cheat": dict(t0=492.4, t1=555.5, headline="Why the AI cheated", film=FILM,
                  title="Why AI Cheats: Reward Hacking in 60 Seconds",
                  caption="Reward the score and you reward every shortcut to it, including breaking out of the sandbox. " + TAGS,
                  pinned="Would you call it cheating or just winning? Full film on the channel."),
}
