"""Curve Short 12 (Fri 30 Oct 2026, publishes 17:00 UK): "Who Changes Your Phone's Clock?"

Account B, Thu 29 Oct 2026 ~18:45 UK (scheduled run b-fri-clock-short-2). US clocks go back Sun 1 Nov, 2 a.m. local.
Facts: lab/research/PHONE_CLOCK_FACTS.md (rows), checks lab/curve_v2/shorts/short12_checks.md (2026f = sixth release
this year, iana.org/time-zones). All pictures ours: a generic phone we draw (no logos, no real UI), a tower and a time
server, the rulebook, the 2 a.m. rule line, the verdict. The House vote (row 3) is NOT used.

Frame 0: our phone's lock screen at 1:59 with "SUN 1 NOV" and the kicker "WHO CHANGES / THIS CLOCK?"; it flips to 1:00
on "change". Loop: the verdict eases back to the phone at 1:59.
"""
TITLE = "Who Changes Your Phone's Clock?"
LINES = [
    dict(id="x1", facts="1 (US: Sun 1 Nov 2026, 2:00 a.m. back to 1:00); 10-11 (tz database, volunteers)",
         text="On Sunday, phones across America will change their own clocks, using a rulebook kept by volunteers.",
         cap="On Sunday, / phones across America / will change / their own clocks, / using a rulebook / kept by volunteers.",
         shot="frame 0 = our phone at 1:59, SUN 1 NOV, kicker 'WHO CHANGES / THIS CLOCK?'; on 'change' 1:59 rolls back to 1:00; "
              "on 'rulebook' a thick book drops beside the phone, tag 'KEPT BY VOLUNTEERS'"),
    dict(id="x2", facts="13, 14 (time from NTP internet time servers or NITZ from the mobile network; Android 12+ prefers NTP)",
         text="First, your phone gets the time from a cell tower or an internet time server.",
         cap="First, your phone / gets the time / from a cell tower / or an internet / time server.",
         shot="our drawing: a cell tower and a time server, each sending a pulse to the phone; labels CELL TOWER and "
              "TIME SERVER; the pulse carries 'UTC 06:59'"),
    dict(id="x3", facts="10 (the tz database: the history of local time for locations worldwide)",
         text="Then it looks up where you are in a rulebook of every time zone's history.",
         cap="Then it looks up / where you are / in a rulebook / of every time zone's / history.",
         shot="the rulebook opens: pages of zone names (AMERICA/NEW_YORK, EUROPE/LONDON, ASIA/TOKYO...) flick past, "
              "a finger-line stops on AMERICA/NEW_YORK; tag 'THE TIME ZONE DATABASE'"),
    dict(id="x4", facts="11 (kept by volunteers on a mailing list, a new release when countries change rules); checks: 2026f on 27 Oct = sixth release of 2026",
         text="Volunteers rewrite that rulebook whenever a country moves its clocks, six times already this year.",
         cap="Volunteers rewrite / that rulebook / whenever a country / moves its clocks, / six times already / this year.",
         shot="six release cards stack up 2026A to 2026F, the last stamped '27 OCT'; tag 'IANA · TZ RELEASES 2026'"),
    dict(id="x5", facts="1 (first Sunday in November, 2 a.m. local, back one hour; most of the US: Hawaii and most of Arizona don't change)",
         text="For most of the US, one line says first Sunday in November, two a.m., go back an hour.",
         cap="For most of the US, / one line says / first Sunday in November, / two a.m., / go back an hour.",
         shot="the rule line typed large: FIRST SUN · NOV · 02:00 · -1 HOUR; a US map with Hawaii and Arizona greyed, "
              "tag 'MOST OF THE US'"),
    dict(id="x6", facts="verdict (our point of view)",
         text="Our take? It's the clock you trust most, and it only works because volunteers do the homework.",
         cap="Our take? / It's the clock / you trust most, / and it only works / because volunteers / do the homework.",
         shot="verdict: the phone back at 1:59 beside the book; OUR TAKE row; ease back to frame 0 (loop)"),
]
