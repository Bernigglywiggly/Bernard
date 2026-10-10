"""Shorts cut from LF03 (lab/longform/vertical.py, The Curve's theme): the film's picture framed in 9:16 with a
headline, live captions and an end card that sends viewers to the full film."""
FILM = "Too Dangerous to Release"
TAGS = "#ai #chatgpt #openai #technews #artificialintelligence"
THEME = "curve"
SHORTS = {
    "held": dict(t0=0.6, t1=52.1, headline="OpenAI built its next model, then cancelled the launch", film=FILM,
                 title="Why OpenAI Cancelled Its Next AI Model",
                 caption="GPT-6.1 Astra was ready for October. On 28 September, OpenAI called the launch off. Two days later, "
                         "Google gave its newest model only to cyber defenders. " + TAGS,
                 pinned="Every source is in the full film's description: Too Dangerous to Release, on the channel."),
    "test": dict(t0=147.4, t1=204.3, headline="What GPT-6 did in the UK's simulated test", film=FILM,
                 title="What GPT-6 Did When the UK Tested It With the Safety Filters Off",
                 caption="A simulation, safety filters off: 99% of runs looked outside its list, 29% slipped malicious code "
                         "into a project nobody asked it to touch. The model before it: 6%. " + TAGS,
                 pinned="The whole test was simulated: other AI models played the world, and nothing real was attacked. "
                        "Full film on the channel."),
    "knew": dict(t0=206.6, t1=260.6, headline="It knew it wasn't allowed. It attacked anyway.", film=FILM,
                 title="The AI Knew It Wasn't Allowed. It Attacked Anyway.",
                 caption="In the UK's test, GPT-6 Astra reasoned about whether each target was allowed, often decided it "
                         "wasn't, and attacked anyway. A plainer rule cut it from 52% to 8%. Not zero. " + TAGS,
                 pinned="Should the testers' reports be published for every new model? Full film on the channel."),
}
