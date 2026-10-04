"""Every AI picture in the Ponzi film (4 Oct). Stills: GPT Image 2.5 at 2k, 16:9 (medium quality, 1 credit; high, 2.75,
for the hero shots and the thumbnail). Clips: Kling 3.0 Pro, 5 s, sound off, animated from a still (7.5 credits each).

Ponzi himself is a real man with real photographs (src/arch), so the AI never draws his face: in a reconstruction he
is seen from behind, in silhouette or with his face in shadow, and the archive photographs carry his likeness.

    python3 ai_assets.py stills 0     -> batch 0 of the still requests, as JSON for generate_image_batch
    python3 ai_assets.py clips        -> the clip requests (needs the stills' job ids in src/jobs.json)
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
P = ("a short, dapper man in a pale summer suit and a straw boater hat, seen from behind (his face never visible)")
STYLE = (" Cinematic period-drama film still, photorealistic, 35mm anamorphic lens, rich low-key lighting with warm amber "
         "practical lights against cool blue shadows, fine film grain, 16:9 widescreen composition. No readable text, no "
         "signs with lettering, no captions, no watermark.")

# id, prompt, quality ("m" medium, "h" high)
STILLS = [
    # cold open: Boston, July 1920
    ("o01", "Boston in July 1920, high summer: a long line of ordinary people four abreast stretching down a narrow street "
            "of old brick and granite buildings towards an office doorway, men in caps and straw hats, women in long "
            "skirts, a policeman keeping order, hazy morning sun.", "h"),
    ("o02", "Close on anxious faces waiting in a crowded line on a Boston street in 1920: a working man in a flat cap, an "
            "elderly widow in black clutching her handbag, a young clerk holding a folded paper note, sweat and worry.", "m"),
    ("o03", "A newsboy on a Boston street corner in 1920 holding up a fresh broadsheet newspaper (headline blurred, not "
            "readable), passers-by stopping to buy, trams and early motor cars behind.", "m"),
    ("o04", f"{P}, walking along a queue of people on a Boston street in 1920, handing a cup of coffee to a woman in the "
            "line; a clerk behind him carries a tray of doughnuts; people smiling at him.", "h"),
    ("o05", "Hands passing banknotes through the brass bars of a teller's window in a crowded 1920 office, piles of cash "
            "on the counter, a hand reaching in to take them.", "m"),
    ("o06", "School Street in Boston at dusk in 1920: gas lamps coming on, empty pavement, a single office window lit "
            "high in an old granite building, long shadows.", "h"),
    # 1 two dollars and fifty cents
    ("a01", "A café in Rome around 1900 at night: well-dressed young students laughing at a marble table with wine and "
            "coffee, gaslight, an opera house glowing across the piazza.", "m"),
    ("a02", "An immigrant steamship arriving in Boston harbour on a grey November morning in 1903, passengers crowding "
            "the rail with bundles and suitcases, gulls, the city skyline in mist.", "h"),
    ("a03", "A card game in a cramped steamship cabin in 1903: hands sweeping a pile of coins and banknotes across a "
            "blanket, a young man's empty hands in the foreground, an oil lamp swinging.", "m"),
    ("a04", "Close-up of a young man's open palm holding two silver dollar coins and a half-dollar, a worn sleeve, the "
            "wooden planks of a harbour dock beneath.", "m"),
    ("a05", "A steaming restaurant kitchen in Boston around 1905: a young immigrant in shirtsleeves scrubbing a mountain "
            "of plates at a stone sink, cooks shouting behind.", "m"),
    ("a06", "A closed restaurant at night around 1905: chairs upturned on the tables, and on the floorboards between "
            "them a rolled blanket, a folded waiter's jacket and a pair of worn shoes where someone sleeps, moonlight "
            "through the window.", "m"),
    ("a07", "Close-up of a hand slipping coins from an open brass cash register into a waistcoat pocket, a restaurant "
            "dining room blurred behind.", "m"),
    # 2 robbing Peter
    ("m01", "A small immigrant bank in Montreal in 1907: a wooden counter with a brass grille, customers in winter coats "
            "queueing with savings books, snow outside the window.", "m"),
    ("m02", "Close-up of a bank ledger in 1907 under a green lamp: a hand moves a stack of banknotes from one pile on "
            "the left to another on the right, columns of figures (not readable).", "m"),
    ("m03", "A crowd of angry immigrants in winter coats outside the locked, shuttered doors of a small bank on a snowy "
            "Montreal street in 1908.", "m"),
    ("m04", "A man in a heavy coat and hat boarding a night train in a cloud of steam, glancing back, a carpetbag "
            "stuffed with money, 1908.", "m"),
    ("m05", "Close-up of a hand forging a signature on a cheque with a fountain pen, a second cheque beside it as a "
            "model, ink blot, candlelight, around 1908 (no readable text).", "m"),
    ("m06", "A stone prison corridor in Quebec around 1910: iron cell doors, a guard with keys, cold light from high "
            "barred windows.", "m"),
    ("m07", "A snowy border road at night around 1911: a horse-drawn wagon with men huddled under blankets, a lantern, "
            "dark pine forest.", "m"),
    ("m08", "A prison infirmary around 1911: a heavyset older man in a prison bed looking gravely ill, a doctor with a "
            "stethoscope bending over him, a bar of soap with shavings cut from it hidden on the bedside table.", "m"),
    # 3 the coupon
    ("c01", "A small office desk in Boston in 1919 under a lamp: an opened letter with colourful Spanish postage stamps "
            "on the envelope, and beside it a small printed slip of paper like a postal coupon (no readable text).", "h"),
    ("c02", "A post office counter in 1919: a clerk in sleeve garters sliding a sheet of postage stamps across the "
            "counter in exchange for a small paper coupon.", "m"),
    ("c03", f"{P}, sitting at a desk by lamplight in a small office in 1919, covering sheets of paper with sums, "
            "a slide rule and stacks of envelopes around him.", "m"),
    ("c04", "A mountain of postage stamps heaped on a table and spilling onto the floor of a dim office, absurd and "
            "impossible, lamplight.", "m"),
    # 4 fifty percent in forty-five days
    ("p01", "A busy small office in Boston in 1920: clerks at desks taking cash from a line of customers and handing out "
            "printed paper notes, sunlight through dusty windows, a ceiling fan.", "h"),
    ("p02", "A delighted working man in a Boston barbershop in 1920 fanning out banknotes to show his friends, the "
            "barber and customers leaning in, amazed.", "m"),
    ("p03", "An office desk drawer in 1920 so stuffed with banknotes that it cannot close, more cash in a wastepaper "
            "basket beside it.", "m"),
    ("p04", "Clerks in a 1920 office counting money late into the night, cash piled on every desk and in wire baskets, "
            "green shaded lamps.", "m"),
    # 5 the king of School Street
    ("k01", "A grand white colonial mansion in Lexington, Massachusetts in 1920, manicured lawn, a long black limousine "
            "in the gravel drive, summer evening light.", "h"),
    ("k02", "A gleaming custom-built 1920 limousine with a uniformed chauffeur holding the rear door open on a Boston "
            "street.", "m"),
    ("k03", "Close-up on dark velvet: a gold-handled walking cane, a diamond necklace and a diamond ring, lamplight "
            "glinting.", "m"),
    ("k04", f"{P}, walking down a Boston street in 1920 while a crowd follows him, men raising their hats and cheering, "
            "a woman reaching to shake his hand.", "m"),
    ("k05", "The grand marble banking hall of a Boston trust company in 1920: tall columns, brass teller cages, a few "
            "well-dressed customers, light through high windows.", "m"),
    # 6 the question
    ("n01", "A newspaper press room in 1920: huge rotary presses running, printed broadsheets streaming off the rollers, "
            "pressmen in caps and aprons, ink and steam.", "h"),
    ("n02", "A newspaper editor's office at night in 1920: a young man in shirtsleeves at a cluttered desk reading "
            "proofs under a green lamp, typewriters and stacked papers, seen in profile in shadow.", "m"),
    ("n03", "A financial analyst's desk in 1920: an adding machine, a ledger of long calculations, a pencil, a cup of "
            "coffee gone cold, lamplight.", "m"),
    # 7 the run
    ("r01", "A crowd surging towards an office door on a narrow Boston street in July 1920, police holding the line, "
            "people waving paper notes, hot sun, dust.", "h"),
    ("r02", "Through an open office window in 1920: clerks handing stacks of cash to outstretched hands in the street "
            "below, coins dropping.", "m"),
    ("r03", "A man in the crowd on a Boston street in 1920 turning back towards the office with a relieved smile, "
            "holding his returned cash, about to invest again.", "m"),
    # 8 hopelessly insolvent
    ("f01", "A former newspaperman in shirtsleeves reading through account books at night in a 1920 office, face in "
            "shadow, his hand flat on a ledger, a look of alarm.", "m"),
    ("f02", "Auditors in 1920 working through stacks of ledgers with adding machines in a cramped office, papers "
            "everywhere, cigarette smoke, late at night.", "m"),
    ("f03", "Two policemen standing guard at the locked bronze doors of a Boston bank in August 1920, a small crowd "
            "staring through the glass.", "m"),
    ("f04", f"{P}, walking between two federal agents in dark suits down the steps of a Boston building in 1920, "
            "photographers' flashbulbs going off.", "m"),
    # 9 the bill
    ("b01", "An empty, abandoned bank lobby in 1920: overturned chairs, papers on the marble floor, a closed teller "
            "window, dust in the light.", "m"),
    ("b02", "An empty federal courtroom in Boston in 1920: dark wood, the judge's bench, the witness stand, tall "
            "windows.", "m"),
    # 10 he tried again
    ("g01", "The Florida land boom in 1925: a real-estate office in a tent among palm trees, crowds of buyers waving "
            "cash, a man unrolling a plot map on a table.", "m"),
    ("g02", "A survey stake with a small flag standing in the still water of a Florida swamp in 1925, mangroves, "
            "egrets, heat haze.", "m"),
    ("g03", "A merchant ship moored at a New Orleans dock at night in 1926, a deputy sheriff with a badge walking up "
            "the gangway, lamplight on the wet planks.", "m"),
    ("g04", "An ocean liner pulling away from a Boston pier in 1934, a lone figure at the rail, a woman on the pier "
            "watching, grey sky.", "m"),
    # 11 cheap at the price
    ("e01", "Rio de Janeiro harbour at dusk in the 1940s, Sugarloaf Mountain against an orange sky, an old airline "
            "flying boat on the water.", "m"),
    ("e02", "A charity hospital ward in Rio de Janeiro in 1949: rows of iron beds, an old man lying alone in the "
            "farthest bed by a tall shuttered window, slanting light.", "h"),
    ("e03", "Close-up of a few banknotes and coins on a bare hospital bedside table in 1949, a pair of round spectacles "
            "beside them.", "m"),
    ("e04", "A modern smartphone glowing in a dark room, showing a rising price chart for a cryptocurrency (no logos, no "
            "readable text), a hand hovering over it.", "m"),
    ("e05", "Boston's old School Street today at blue hour, the old granite buildings still standing, modern people "
            "walking past, faint reflection of the past.", "m"),
]

# clip id -> (still id, motion prompt)
CLIPS = {
    "k_o01": ("o01", "Slow push along the line of people towards the office door; people shuffle forward, fan themselves "
                     "with hats; the policeman paces."),
    "k_o04": ("o04", "He hands the coffee to the woman and moves on along the line, patting a man's shoulder; people smile."),
    "k_a02": ("a02", "The steamship glides slowly towards the pier; passengers wave; gulls wheel; mist drifts."),
    "k_p01": ("p01", "Clerks take cash and hand out notes; the line moves; the ceiling fan turns; dust in the sunbeams."),
    "k_n01": ("n01", "The presses roll faster, broadsheets streaming off the rollers; a pressman checks a sheet."),
    "k_r01": ("r01", "The crowd pushes forward; police link arms; people wave their paper notes; dust rises."),
}


def stills_batch(i, size=12):
    reqs = []
    for k, (sid, prompt, q) in enumerate(STILLS[i * size:(i + 1) * size]):
        p = dict(model="gpt_image_2_5", prompt=prompt + STYLE, aspect_ratio="16:9", resolution="2k",
                 quality={"m": "medium", "h": "high"}[q])
        reqs.append(dict(index=i * size + k, params=p))
    return reqs


def clips_batch():
    """Clip requests for every clip whose still has finished (src/jobs.json has its job id) and isn't made yet."""
    jobs = json.load(open(os.path.join(HERE, "src", "jobs.json")))
    reqs = []
    for k, (cid, (sid, motion)) in enumerate(CLIPS.items()):
        if sid not in jobs or cid in jobs:
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
        print(json.dumps(clips_batch(), ensure_ascii=False))
