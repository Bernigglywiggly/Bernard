"""A test of real photographs in the one-camera look (7 Oct 2026; the user: "in some vids i wanna try experiment using
real photos"). Five public-domain pictures from lab/longform/ponzi/src/photo (rights in its CREDITS.md). The lines are
placeholders for timing, not a script: the Ponzi script has four lines to correct first (longform/ponzi/VERIFY.md).
  ("photo", id, label, credit)   a real picture: it arrives as characters, then resolves into the photograph itself"""
TITLE = "PHOTO TEST"
TAG = "MONEY CRIMES  ·  PHOTO TEST"
FIX = {}
CHAPTERS = [
    dict(id="t", title="", beats=[
        ("In the summer of nineteen twenty, one man in Boston promised to double your money in ninety days.",
         ("photo", "ponzi_portrait_bain_1920", "CHARLES PONZI · 1920", "BAIN NEWS SERVICE · LIBRARY OF CONGRESS")),
        ("Thousands of people took him up on it. They filled School Street from wall to wall.",
         ("photo", "school_street_crowd_1920", "SCHOOL STREET, BOSTON", "LESLIE'S WEEKLY, 1920")),
        ("Each of them left with a note like this one: two hundred dollars in, three hundred dollars back.",
         ("photo", "ponzi_promissory_note_1920", "$200 IN · $300 BACK", "THE SECURITIES EXCHANGE COMPANY, 1920")),
        ("He smiled for every camera in the city.",
         ("photo", "ponzi_straw_hat_1920", "THE WIZARD OF FINANCE", "LESLIE'S WEEKLY, 1920")),
        ("By the middle of August, the same newspapers had a different headline.",
         ("photo", "boston_american_ponzi_arrested_1920", "13 AUGUST 1920", "BOSTON AMERICAN")),
    ]),
]
