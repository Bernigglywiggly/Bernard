# CRITIC · ORMUZ_ES_v1.mp4 · "Ormuz está cerrado. El petróleo no." · 12 Oct 2026

## VERDICT: FIX THEN UPLOAD

The voice is clean: **nothing needs re-voicing.** All the fixes are in the picture, so it is one picture re-render with the mix unchanged.

- [ ] **Picture fixes** → rows 1-6 (re-render the picture only; keep the mix)
- [ ] **On-screen strings** → list below
- [ ] 🎧🗺️🔍🧭🪝 **Listen to 6 moments: 1:05, 5:55, 6:12, 7:52, 10:51, 11:12** → Gran Cuoin, Yanbu, Habshan, UKMTO, stress in "Fuyaira", onset click

Method: 77 takes through faster_whisper medium (es), suspect clips re-run on small and base; a full-size grab at the end of every beat, plus frame 0, chapter cards and outro; ebur128, silencedetect, head/tail level of every take; cards checked against FACTCHECK (all match).

## Severity table

| # | Sev | Where | Problem | Exact fix |
|---|---|---|---|---|
| 1 | HIGH | `gap_03` 1:15-1:28 | Labels crossed: **SALIDA reads north, ENTRADA south**, the opposite of the voice. The leaders are right, but nobody follows leaders | Move the anchors apart: ENTRADA `(56.12, 26.68)`, SALIDA `(56.45, 26.36)`; check the grab |
| 2 | HIGH | `flows_04` 2:32-2:34 | The line lasts 2.3 s; only the India route draws before the 84% card. **Korea, Japan and Europe (0.7M) are never seen** | `HOLD = {"verdict_07": 1.5, "flows_04": 3.0}` |
| 3 | MED | All relief maps, frame 0 included | English word in the caption | string below (engine, not script.py) |
| 4 | MED | `gap_04` 1:28-1:36 | Labels crossed: LARAK sits at Hormuz Island's pin, ORMUZ at Larak's | Offset the labels as for Tunb Menor: LARAK `(LARAK[0]-0.05, LARAK[1]-0.10)`, ORMUZ `(HORMUZ_I[0]+0.08, HORMUZ_I[1]+0.04)` |
| 5 | MED | `flows_02` 2:14, `flows_07` 2:47, `how_02` 4:48 | Captions run 4-17 px past the card | Strings below |
| 6 | LOW-MED | `price_02` 9:08 | English jargon `VLCC` | String below |
| 7 | LOW | `around_02` 6:08-6:17 | The FUJAIRAH label sits inside the Gulf while the voice says "fuera del estrecho" | Label at `(57.3, 24.9)` |
| 8 | LOW | `around_10` 7:40-7:42 | The drift clips the latitude ticks at the left edge | Stop the drift earlier or pad the margin |
| 9 | LOW | 0:00, 11:12 · card headers 0:26, 2:34, 8:40, 8:46 | The route crosses "ESTRECHO DE ORMUZ" · the headers show coordinates like `83.76°N 120.09°W` | Label `(56.38, 26.72)` · hold the last map's coordinates |

## LINES TO RE-VOICE

**None.** No line is clearly wrong as heard. All 77 transcripts match the said text, give or take spelling of the same sounds. Two false alarms:
- `closing_05`: medium dropped "2008"; the tail re-run hears it (3 models).
- `verdict_05`: "Oeste-Oeste" is the elision in "oleoducto Este". The clip reads "Este-Oeste" (medium) or "este o este" (small, base), which is how the phrase sounds.

## Pronunciation of the names

| Name | Heard as (prob.) | Verdict |
|---|---|---|
| Fujairah → Fuyaira | "Fuyaira" ×3 (0.68-0.71), "Fuyaíra" at 10:51 | OK; possible stress shift at 10:51 |
| Yanbu | "Yambú" (0.76) | Natural n→m. Probably final stress (Arabic: YAN-bu). Minor |
| UKMTO | "UKMTO" (0.98) | **Cannot verify** Spanish vs English letter names |
| Gran Quoin → Gran Cuoin | "Gran Coín" (0.38) | Matches the English "coin"; low confidence |
| Abqaiq, Habshan | "Abqaiq" (0.82), "Hapshan" (0.72) | Probably fine; the h vs jota in Habshan cannot be verified |

Clean: Ormuz ("Hormuz", the same sound), Qeshm→"Keshm" (0.52), Kpler→"Kepler" (0.97), Larak (0.83), Tunb→"Tumb", Windward (0.99), Brent (0.89). **Musandam is on screen only** (the `gap_00` label) and is never said.

## On-screen strings to change

| Beat | Now | Change to |
|---|---|---|
| all relief maps | `RELIEF: NOAA ETOPO 2022` | `RELIEVE: NOAA ETOPO 2022` |
| `price_02` | `VLCC DE SEGUNDA MANO · UN RÉCORD` | `SUPERPETROLERO USADO · UN RÉCORD` |
| `flows_02` right | `DEL COMERCIO MUNDIAL DE GNL · SOBRE TODO QATAR · EIA` | `DEL COMERCIO MUNDIAL DE GNL · SOBRE TODO QATAR` |
| `flows_07` right | `ESTADOS UNIDOS · PARTE DEL CRUDO DE ORMUZ · 2024 · EIA` | `EE. UU. · PARTE DEL CRUDO DE ORMUZ · 2024 · EIA` |
| `how_02` right | `INICIOS DE MARZO · FUENTES DEL SECTOR VÍA AL JAZEERA` | `INICIOS DE MARZO · SECTOR, VÍA AL JAZEERA` |
| optional, 7 places | `FUJAIRAH` / "Fujairah" in captions | `FUYAIRA` / "Fuyaira" (the script's Fundéu spelling; matches the voice) |

Everything else is correct Spanish; `OIL MARKET REPORT` and `OILPRICE.COM` are titles, so they stay.

## Sound

**-14.0 LUFS integrated, true peak -3.1 dBFS, LRA 1.8 LU.** No silences of 1.2 s or more (the short-term dips are the chapter cards and the outro). No line cut off: the last sound ends at least 0.12 s before its slot does. `verdict_08` (11:12) has sound in its first 20 ms; "Nada" is heard whole, so it only needs one listen for a click.

## Spanish as heard

Near-native neutral Latin-American Spanish. Mexico and Colombia hear it as native; Spain hears it as Latin American ("costo", "video", "gasolina regular"). No false friends, no number errors.

Optional taste re-voices (only if a batch opens anyway):
- `october_06` "Si lo estoy leyendo bien" (a calque) → `Si no lo interpreto mal, los ataques están siguiendo al petróleo…`
- `price_03` "el precio de papel de los titulares" → `el precio de papel que sale en los titulares`
- `verdict_02` "recortó el flujo con fuerza" → `redujo mucho el flujo durante meses`
- `around_03` "unos dos millones y medio" → `unos dos coma seis millones` (matches the card)
- `how_04` "marinos" → `marineros`
