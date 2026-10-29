# Short 12 facts check (account B, Thu 29 Oct 2026 ~18:40 UK, primary pages opened)

| Row | Checked on | What the page says | Verdict |
|---|---|---|---|
| 10 | iana.org/time-zones | the tz database "contains code and data that represent the history of local time for many representative locations worldwide" | OK |
| 11 | rfc-editor.org/rfc/rfc6557 | "updated approximately twenty times per year, depending on the year"; "previously maintained by volunteers who participated in the" TZ mailing list, now run by a TZ Coordinator | OK, but 20/year is a 2012 figure. CORRECTION used in the script: iana.org shows release **2026f, 27 Oct 2026** = the sixth release this year (2026a-f). Script says "six times this year" |
| 12 | RFC 6557 | hosted at the US NIH from the early 1980s through 2011; Olson maintained it since creation | OK (not used) |
| 13-14 | source.android.com/docs/core/connect/time-source | defaults are only Telephony (NITZ) and Network (NTP); Android 12+ prefers NTP, falls back to NITZ; 11 and lower prefer NITZ | OK |
| 17 | same page | GNSS is not a default time source | OK (we still don't claim GPS either way) |
| 3 | not checked | H.R. 139 House vote | NOT USED: dropped from the script, so no claim needs it |

FOR C (facts file): row 11 should note the 2026 count (2026a-f, latest 2026f on 27 Oct, iana.org/time-zones).
