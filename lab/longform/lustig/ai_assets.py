"""Every AI picture in the film, as prompts (2 Oct). Stills: GPT Image 2.5 at 2k, 16:9 (medium quality, 1 credit; high,
2.75, for the hero close-ups and the thumbnail), with the two character references from short 01 so Lustig and Poisson
are the same men in both. Clips: Kling 3.0 Pro, 5 s, sound off, animated from a still (7.5 credits each).

    python3 ai_assets.py stills 0     -> batch 0 of the still requests, as JSON for generate_image_batch
    python3 ai_assets.py clips 0      -> batch 0 of the clip requests (needs the stills' job ids in src/jobs.json)
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REF_L, REF_P = "39f996cb-4e18-4b8b-9c1a-8271e3d52559", "69f86d74-2bb4-488c-8b6c-f906e3a512a9"
L = ("Victor Lustig, the man in the reference photo: slicked-back dark hair, a thin moustache, sharp cheekbones, a thin "
     "pale scar on his left cheek, an immaculate dark pinstripe three-piece suit")
LY = "the man in the reference photo as a 19-year-old student: slicked-back dark hair, clean-shaven, a sharp suit"
P = ("André Poisson, the man in the reference photo: heavyset, balding, round wire glasses, a bushy grey moustache, a "
     "brown tweed three-piece suit")
STYLE = (" Cinematic period-drama film still, photorealistic, 35mm anamorphic lens, rich low-key lighting with warm amber "
         "practical lights against cool blue shadows, fine film grain, 16:9 widescreen composition. No captions, no "
         "watermark.")

# id, prompt, refs, quality ("m" medium, "h" high)
STILLS = [
    # cold open
    ("o01", "Paris at dawn in 1925 seen from high above the rooftops: zinc roofs, chimney pots, morning mist over the "
            "Seine, the Eiffel Tower rising in the distance, a few 1920s motor cars and a horse cart in the street below.", [], "h"),
    ("o02", "Close-up of gloved hands breaking the red wax seal of a heavy cream envelope at a mahogany desk under a brass "
            "lamp; a folded letter on official government letterhead is partly visible.", [], "m"),
    ("o03", f"{L}, standing by the tall windows of a grand Paris hotel suite in 1925, gilded mouldings, heavy drapes, "
            "Paris roofs beyond; he turns from the window toward the camera, composed and elegant.", [REF_L], "h"),
    ("o04", f"Extreme close-up of {L}: his face in half shadow, one eye catching the light, the thin scar on his left "
            "cheek clearly visible.", [REF_L], "h"),
    ("o05", "Six prosperous 1920s Paris businessmen of different ages, scrap-metal dealers in dark suits, seated around a "
            "polished table in an ornate hotel salon under a crystal chandelier, cigar smoke, listening intently.", [], "m"),
    ("o06", "The Eiffel Tower at dusk in 1925 seen from the Trocadéro gardens, gas lamps glowing, a stormy violet sky, a "
            "few figures in long coats and hats.", [], "m"),
    ("o07", f"{L}, his reflection in a tarnished gilded mirror in a dim hotel corridor, half his face hidden in shadow, "
            "enigmatic.", [REF_L], "m"),
    ("o08", f"{L} seen from behind, walking away down a wet cobbled Paris street at night, overcoat and fedora, gaslight "
            "reflections, the Eiffel Tower faint in the mist at the end of the street.", [REF_L], "m"),
    # chapter 1
    ("b01", "A small Bohemian town square in winter in the 1890s: snow, a baroque church tower, a horse-drawn sleigh, "
            "warm lit windows, people in heavy coats.", [], "m"),
    ("b02", "1890s house interior at dusk: an empty dark wooden staircase and a hallway lit by one oil lamp; the long "
            "shadow of a tall man in a hat stretches across the wallpaper. Quiet, sombre mood.", [], "m"),
    ("b03", "A restless boy of about ten in an 1890s village schoolroom: chalk slates, wooden benches, a stern teacher "
            "blurred in the background; the boy stares out of the window, bored.", [], "m"),
    ("b04", "The grand baroque facade of a German boarding school in Dresden around 1905, boys in dark uniforms crossing "
            "a cobbled courtyard, grey winter light.", [], "m"),
    ("b05", f"{LY}, reading by candlelight at a dormitory desk piled with books in German, French, English, Italian and "
            "Hungarian, absorbed.", [REF_L], "m"),
    ("b06", "A smoky Paris gambling club in 1909: a green baize card table under oil lamps, stacks of chips, players in "
            "evening dress, a dealer's hands mid-deal.", [], "m"),
    ("b07", f"{LY}, at a green baize card table in a smoky 1909 Paris gambling club, studying the other players over his "
            "cards with a faint, knowing smile.", [REF_L], "h"),
    ("b08", "Across a card table in a smoky 1909 gambling club: an older gambler in evening dress, sweating, eyes "
            "darting, holding his cards close to his chest.", [], "m"),
    ("b09", "A narrow Paris alley at night in 1909, two men's silhouettes struggling beneath a single gas lamp, the glint "
            "of a blade, rain. No blood, nothing graphic.", [], "m"),
    ("b10", f"The first-class saloon of an Edwardian ocean liner: chandeliers, palms, wealthy passengers in evening wear "
            f"gathered around {LY}, who gestures expansively with a theatre programme, charming them.", [REF_L], "m"),
    ("b11", "An Edwardian four-funnelled ocean liner crossing the Atlantic at night, rows of lit portholes, smoke "
            "streaming from the funnels, a dark heaving sea, moonlight.", [], "m"),
    ("b12", "A mysterious object the size of a small trunk hidden under a dark velvet cloth on a table in a dim 1920s "
            "hotel room, lit by a single lamp.", [], "m"),
    # chapter 2
    ("x01", "The 'Rumanian Box': a handsome polished mahogany box the size of a small steamer trunk, with two narrow "
            "brass-lined slots on top, a row of brass dials and little levers on the front, sitting on a velvet-covered "
            "table in a dim 1920s hotel room, dramatic side light.", [], "h"),
    ("x02", f"{L}, resting one hand proudly on a polished mahogany box with brass dials and slots, smiling at someone "
            "off camera in a dim 1920s hotel room.", [REF_L], "m"),
    ("x03", "A 1920s bank teller in sleeve garters and a green eyeshade examining a banknote under a green-shaded lamp "
            "behind a brass teller's cage.", [], "m"),
    ("x04", f"A nervous 1920s businessman counting a thick stack of banknotes onto a table in front of {L}; a polished "
            "mahogany box with brass dials sits between them.", [REF_L], "m"),
    ("x05", "A polished mahogany box with brass dials, its lid open, only blank white paper inside and spilling onto the "
            "table; a man's hands frozen above it in disbelief.", [], "m"),
    ("x06", "A man in a rumpled 1920s suit sitting alone on the edge of a cheap hotel bed at night, head in his hand, "
            "staring at a mahogany box on the dresser. Despair.", [], "m"),
    ("x07", "A 1920s Texas sheriff (Stetson hat, star badge, walrus moustache) sitting by a train window, jaw set, the "
            "plains rushing past outside.", [], "m"),
    ("x08", f"A 1920s Chicago hotel lobby with potted palms: {L} hands a thick roll of banknotes to a Texas sheriff in a "
            "Stetson; both men are smiling.", [REF_L], "m"),
    ("x09", "A 1920s Midwestern bank: a stone building with columns on a small-town main street, Model T cars, a man in "
            "a bowler hat walking out of the doors with a briefcase.", [], "m"),
    # chapter 3
    ("t01", f"{L}, sitting at a Paris cafe terrace one morning in 1925, reading a newspaper, a coffee cup on the marble "
            "table, a waiter passing.", [REF_L], "m"),
    ("t02", "Close-up of a 1925 French newspaper page with an engraving of the Eiffel Tower and a bold headline: "
            "\"LA TOUR EIFFEL : QUI PAIERA LES RÉPARATIONS ?\", columns of small print, a coffee ring.", [], "m"),
    ("t03", "Extreme close-up of the Eiffel Tower's iron girders and rivets, flaking brown paint and orange rust, an "
            "overcast sky behind.", [], "m"),
    ("t04", "1920s painters in caps suspended high on the Eiffel Tower's iron girders with buckets and long brushes, "
            "Paris spread out far below.", [], "m"),
    ("t05", f"{L}, standing on a Paris street with a folded newspaper, looking up at the Eiffel Tower in the distance, "
            "a slow calculating look.", [REF_L], "m"),
    ("t06", "Looking straight up through the centre of the Eiffel Tower's iron lattice from directly beneath, dramatic "
            "perspective, overcast sky.", [], "m"),
    # chapter 4
    ("s01", "A forger's back room in 1925 Paris: magnifying glass, inks, engraving tools, rubber stamps and sheets of "
            "blank official letterhead under a single lamp.", [], "m"),
    ("s02", "A silver tray on a hotel desk holding six sealed cream envelopes addressed in elegant handwriting, red wax "
            "seals, a fountain pen.", [], "m"),
    ("s03", f"{L}, standing at the head of a long table in an ornate Paris hotel salon, addressing six seated "
            "businessmen; papers and a blueprint of the Eiffel Tower on the table, chandelier light.", [REF_L], "h"),
    ("s04", "Blueprints of the Eiffel Tower and pages of financial estimates spread on a polished table, a fountain pen, "
            "a cigar smoking in a crystal ashtray.", [], "m"),
    ("s05", "Close faces of 1920s businessmen in lamplight around a table, leaning in, intrigued and greedy, cigar smoke.", [], "m"),
    ("s06", "Two black 1920s limousines driving along the Seine embankment toward the Eiffel Tower on a grey morning.", [], "m"),
    ("s07", f"A group of businessmen in overcoats at the base of the Eiffel Tower looking up at it in awe; {L} stands "
            "slightly behind them, watching them, not the tower.", [REF_L], "m"),
    ("s08", f"Portrait of {P} in his office, ambitious and anxious, a ledger on the desk, Paris rooftops in the window.", [REF_P], "h"),
    ("s09", f"A glittering Paris society reception in 1925: {P} stands alone at the edge of the room holding a glass, "
            "while elegant businessmen laugh together, ignoring him.", [REF_P], "m"),
    ("s10", f"{P}, alone at night in his office by a green lamp, holding an official letter, frowning with doubt.", [REF_P], "m"),
    ("s11", f"A dim hotel bar: {L} leans across a small table toward {P}, speaking in a low confiding voice; two glasses "
            "of cognac between them.", [REF_L, REF_P], "h"),
    ("s12", "Close-up of a fat envelope of 1920s French franc banknotes slid across a marble table under a man's palm.", [], "m"),
    ("s13", f"{P}, smiling with relief, shaking hands with {L} across a hotel table.", [REF_L, REF_P], "m"),
    ("s14", "A night express pulling out of a Paris station in 1925 in great clouds of steam, glowing carriage windows, "
            "porters, the station clock.", [], "m"),
    # chapter 5
    ("r01", f"{L}, in a Vienna coffee house, leafing through a stack of French newspapers, amused, a coffee and a slice "
            "of cake on the marble table.", [REF_L], "m"),
    ("r02", f"{P}, at his desk in the dark, head in his hands, a crumpled official letter in front of him. Shame.", [REF_P], "m"),
    ("r03", "A Paris scrap-metal dealer in a bowler hat climbing the steps of a 1920s Paris police station holding a "
            "sheaf of papers, two gendarmes at the door.", [], "m"),
    ("r04", f"{L}, slipping out of a hotel service door into a rainy alley at night, coat collar turned up, glancing "
            "back.", [REF_L], "m"),
    ("r05", "A transatlantic liner arriving in New York harbour in the 1920s, the Manhattan skyline in the morning haze, "
            "tugboats.", [], "m"),
    # chapter 6
    ("c01", f"A 1920s Chicago gangster's office: men in fedoras by the wall, a big desk with stacks of banknotes, the "
            f"boss seen only from behind in silhouette with cigar smoke; {L} sits opposite him, perfectly calm.", [REF_L], "m"),
    ("c02", "In a bank vault, a manicured hand slides a long steel safe-deposit box into its slot in a wall of brass "
            "boxes.", [], "m"),
    ("c03", f"{L}, placing bundles of banknotes back on a gangster's desk with an apologetic expression; the boss in "
            "silhouette in the foreground.", [REF_L], "m"),
    ("c04", "The silhouette of a 1920s gangster boss with a cigar, backlit through venetian blinds, a stack of returned "
            "banknotes on the desk in front of him.", [], "m"),
    ("c05", f"{L}, walking out onto a busy 1920s Chicago street, putting on his fedora and smiling to himself.", [REF_L], "m"),
    # chapter 7
    ("m01", "A hidden 1930s counterfeiting workshop: a hand-cranked printing press, sheets of green banknotes hanging to "
            "dry on lines, a bare bulb, ink everywhere.", [], "m"),
    ("m02", "Close-up of a printing press rolling out a sheet of crisp green banknotes, ink rollers gleaming.", [], "m"),
    ("m03", "Close-up of an engraver's hands cutting a copper banknote printing plate under a magnifying loupe.", [], "m"),
    ("m04", "A 1930s Secret Service office: agents in shirtsleeves around a map of the United States pinned with string "
            "and photographs, cigarette smoke.", [], "m"),
    # chapter 8
    ("l01", f"A 1930s New York nightclub: a glamorous woman with a dark bob in a satin gown watches across the room, "
            f"jealous, as {L} dances with a younger woman.", [REF_L], "m"),
    ("l02", "A glamorous 1930s woman with a dark bob picking up a candlestick telephone in a dark apartment, "
            "determined.", [], "m"),
    ("l03", "Close-up of a small brass locker key lying in a federal agent's open palm, the shadow of a fedora.", [], "m"),
    ("l04", "A 1930s New York subway station under Times Square: a row of coin-operated lockers against tiled walls, "
            "commuters blurred in motion.", [], "m"),
    ("l05", "A steel locker door standing open, revealing tightly stacked counterfeit banknotes and two engraved metal "
            "printing plates.", [], "m"),
    ("l06", "A grim 1930s federal detention building in Manhattan at dusk, rows of barred windows, one third-floor window "
            "lit.", [], "m"),
    ("l07", "An empty 1930s jail cell, the iron bunk stripped of its sheets, light through the window bars.", [], "m"),
    # chapter 9
    ("e01", f"{L}, in a 1930s jail cell, clutching his stomach and grimacing, a guard peering in through the bars.", [REF_L], "m"),
    ("e02", f"A rope of knotted white bedsheets hanging from a high window of a stone building in 1935; {L} climbing "
            "down it.", [REF_L], "m"),
    ("e03", f"Street view looking up at {L} halfway down a building's facade on a knotted bedsheet rope, calmly wiping a "
            "window with a rag; passers-by in 1930s clothes glance up.", [REF_L], "m"),
    ("e04", f"A 1935 American courtroom, dark wood panelling: {L} stands before the judge between lawyers, a "
            "stenographer typing.", [REF_L], "m"),
    # chapter 10
    ("k01", f"A 1930s Alcatraz cell house: a long tier of cells; {L}, older and greyer in prison uniform, sits on his "
            "bunk in one cell.", [REF_L], "m"),
    ("k02", "A 1940s prison hospital ward: an empty iron bed beside a barred window, pale morning light.", [], "m"),
    # chapter 11
    ("n01", "An old leather notebook lying open on a desk, a list handwritten in fountain-pen ink (illegible), the pen "
            "beside it, lamplight.", [], "m"),
    ("n02", f"{L}, smiling warmly and listening attentively across a restaurant table, utterly charming.", [REF_L], "h"),
    ("n04", "Present day: a scammer's hands on a laptop keyboard in a dark room lit by several screens, hoodie, nothing "
            "readable on the screens.", [], "m"),
    ("n05", "The Eiffel Tower today at golden hour, seen across the Seine, tourists on the bridge, warm light.", [], "m"),
    ("n06", "Present day: a man in a sharp modern suit seen from behind at a hotel window at night, looking out at the "
            "illuminated Eiffel Tower.", [], "m"),
    # the thumbnail
    ("th1", f"{L}, smirking at the camera and holding up a large antique brass key, the Eiffel Tower behind him at dusk, "
            "dramatic rim light, a poster-like composition with empty space on the right.", [REF_L], "h"),
    # added: the Depression, when Commons wouldn't serve the NARA breadline photograph to this machine
    ("m05", "New York, 1932, the Great Depression: a long breadline of men in worn overcoats and flat caps waiting along a "
            "brick wall in winter, steam from a soup kitchen door, grey sky. Black-and-white documentary photograph look", [], "m"),
]

# clip id -> (still id, motion prompt)
CLIPS = {
    "k_o01": ("o01", "Slow aerial drift forward over the Paris rooftops toward the Eiffel Tower, mist moving, smoke from chimneys."),
    "k_o03": ("o03", "He turns slowly from the window toward the camera and straightens his cuff; the curtains stir."),
    "k_o08": ("o08", "He walks slowly away down the wet street, gaslight flickering, mist drifting."),
    "k_b06": ("b06", "The dealer deals cards across the green baize; smoke curls in the lamplight; players shift."),
    "k_b11": ("b11", "The liner steams forward through the dark sea, smoke streaming, moonlight on the waves."),
    "k_x02": ("x02", "He pats the box gently and smiles; the lamp flickers softly."),
    "k_t01": ("t01", "He lowers the newspaper slowly and looks off into the distance, thinking."),
    "k_t05": ("t05", "Slow push in on his face as he looks up at the tower, a faint smile forming."),
    "k_s03": ("s03", "He speaks to the seated men, gesturing at the blueprint; they lean in; cigar smoke drifts."),
    "k_s06": ("s06", "The two limousines drive along the embankment toward the tower; the camera tracks alongside."),
    "k_s11": ("s11", "He leans closer and speaks quietly; the heavyset man listens, then slowly nods."),
    "k_s14": ("s14", "The train pulls out of the station in billowing steam, carriages sliding past."),
    "k_r04": ("r04", "He steps out into the rain, glances back over his shoulder, and hurries away down the alley."),
    "k_c02": ("c02", "The hand slides the steel box fully into its slot and the small door swings shut."),
    "k_c05": ("c05", "He puts on his fedora and walks into the crowd, smiling to himself."),
    "k_m02": ("m02", "The press rolls, feeding out a fresh sheet of banknotes; rollers turn."),
    "k_l02": ("l02", "She lifts the receiver and begins to dial, jaw set."),
    "k_l05": ("l05", "The locker door swings open slowly, revealing the stacks of notes and the plates."),
    "k_e02": ("e02", "He lowers himself hand over hand down the knotted bedsheet rope; the sheets sway."),
    "k_n05": ("n05", "Slow push toward the Eiffel Tower in golden light, people crossing the bridge."),
}


def stills_batch(i, size=12):
    reqs = []
    for k, (sid, prompt, refs, q) in enumerate(STILLS[i * size:(i + 1) * size]):
        p = dict(model="gpt_image_2_5", prompt=prompt + STYLE, aspect_ratio="16:9", resolution="2k",
                 quality={"m": "medium", "h": "high"}[q])
        if refs:
            p["medias"] = [dict(value=r, role="image_references") for r in refs]
        reqs.append(dict(index=i * size + k, params=p))
    return reqs


def clips_batch(i=None, ids=None, size=12):
    """Clip requests, by batch number or for the clip ids given; only clips whose still has finished (src/ai/<id>.png)."""
    jobs = json.load(open(os.path.join(HERE, "src", "jobs.json")))
    items = list(CLIPS.items())
    reqs = []
    for k, (cid, (sid, motion)) in enumerate(items):
        if (ids is not None and cid not in ids) or (ids is None and not i * size <= k < (i + 1) * size):
            continue
        if not os.path.exists(os.path.join(HERE, "src", "ai", sid + ".png")) or cid in jobs:
            continue
        reqs.append(dict(index=100 + k, params=dict(
            model="kling3_0", prompt=motion + " Subtle, realistic motion, cinematic, no cuts.", duration=5, mode="pro",
            sound="off", aspect_ratio="16:9", declined_preset_id="24bae836-2c4a-48e0-89b6-49fcc0b21612",
            medias=[dict(value=jobs[sid], role="start_image")])))
    return reqs


if __name__ == "__main__":
    if sys.argv[1] == "stills":
        print(json.dumps(stills_batch(int(sys.argv[2])), ensure_ascii=False))
    else:
        print(json.dumps(clips_batch(ids=set(CLIPS))[:12]))
