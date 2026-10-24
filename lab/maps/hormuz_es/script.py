"""Spanish version of ../hormuz/script.py (CurvaExplica, written 11 Oct 2026); same beats, same pictures, same maps.
MAPS & POWER · 01 · THE STRAIT OF HORMUZ. Working title: ORMUZ ESTÁ CERRADO. EL PETRÓLEO NO.

Thesis, sources, the facts behind every figure and the map rules are those of the English film: see the docstring of
../hormuz/script.py (sources S1-S18 as opened on 9 Oct 2026), ../hormuz/FACTS.md and ../hormuz/FACTCHECK.md. Nothing
here adds or changes a fact; only the language changes. Neutral Latin-American Spanish (tú, not vos); "mil millones"
for 10^9, "billón" only for 10^12 (not used in this film). Decimal point in prices, as the LF02 Spanish film.
Names the Spanish voice mangles are respelled through the (shown, said) tuple: Fujairah -> Fuyaira (the Fundéu/EFE
spelling), Kpler -> Kepler, Qeshm -> Keshm, Great Quoin -> Gran Cuoin.
"""
TITLE = "ORMUZ ESTÁ CERRADO. EL PETRÓLEO NO."
TAG = "CURVAEXPLICA  ·  EL ESTRECHO DE ORMUZ"
LANG = "es"
LEAD = 0.4
OPEN_RESOLVED = True
LOOK = "system"                                   # as the English film: colour = meaning, one hero per chapter
TAGLINE = ""                                      # the channel's "LA IA, EXPLICADA" line would be wrong on this film
CHROME = "chart"                                  # the maps look: nav header with live coordinates, plain captions, ruled cards
ILLUS = "MAPA  ·  DIBUJADO PARA ESTE VIDEO"       # nothing here is generated: maps and cards are drawn in code
HOLD = {"verdict_07": 1.5, "flows_04": 3.0}         # critic ES v1: the world map was up 2.3 s, too short to read the destinations                        # the watch-list stays up long enough to read
NAME = "maps_hormuz01_es"
FIX = {}

# ---- views (lon0, lat0, lon1, lat1) ----
V_WORLD = (24.0, -8.0, 145.0, 46.0)
V_GULF = (47.0, 22.5, 60.0, 31.0)
V_PIPES = (36.0, 21.0, 60.0, 31.0)
V_STRAIT = (55.0, 25.6, 57.6, 27.4)
V_NARROWS = (55.85, 26.1, 57.05, 27.0)

# ---- places (FACTS.md s.9) ----
LARAK = (56.356, 26.853)
QUOIN = (56.529, 26.494)
HORMUZ_I = (56.460, 27.068)
QESHM = (55.773, 26.768)
BANDAR_ABBAS = (56.288, 27.196)
KHASAB = (56.250, 26.183)
MUSANDAM = (56.200, 25.900)
G_TUNB = (55.267, 26.250)
L_TUNB = (55.133, 26.233)
ABU_MUSA = (55.033, 25.867)
FUJAIRAH = (56.334, 25.122)
RAS_TANURA = (50.053, 26.706)
ABQAIQ = (49.666, 25.935)
YANBU = (38.062, 24.089)
HABSHAN = (53.617, 23.825)
RAS_LAFFAN = (51.539, 25.858)
KHARG = (50.310, 29.245)
QATAR_HIT = (51.20, 26.98)            # ~94 km north of Madinat ash Shamal (approximate)
FUJ_HIT = (56.55, 25.17)              # ~10 nm east of the Fujairah moorings (approximate)

# ---- routes: schematic paths, sourced endpoints ----
R_GULF_OUT = [(50.05, 26.71), (51.2, 27.0), (52.6, 26.85), (54.0, 26.45), (55.3, 26.32), (56.12, 26.37),
              (56.26, 26.47), (56.43, 26.54), (56.55, 26.53), (56.63, 26.39), (56.67, 26.12), (57.4, 25.4), (59.4, 23.9)]   # FACTCHECK: kept on the Omani side, clear of Iran's coast
R_INDIA = [(59.4, 23.9), (63.5, 23.0), (67.5, 22.6), (69.8, 22.45)]
R_CHINA = [(59.4, 23.9), (64.0, 17.5), (72.5, 9.5), (80.3, 5.6), (88.0, 5.9), (95.3, 5.9), (98.8, 3.9), (101.6, 2.4),
           (103.0, 1.45), (103.8, 1.15), (104.4, 1.3), (106.5, 3.5), (110.5, 8.5), (115.0, 14.5), (119.0, 21.5), (121.5, 26.5), (122.3, 29.8)]
R_JAPAN = [(115.0, 14.5), (120.9, 20.0), (124.5, 24.5), (130.0, 30.5), (135.0, 33.3), (139.8, 35.3)]
R_KOREA = [(124.5, 24.5), (126.5, 31.0), (128.6, 34.3), (129.4, 35.5)]
R_EUROPE = [(59.4, 23.9), (60.0, 22.6), (59.3, 20.6), (58.5, 19.0), (53.0, 14.0), (48.0, 12.3), (43.4, 12.6), (41.0, 15.5), (38.3, 20.5),
            (35.0, 26.5), (32.55, 29.95), (32.3, 31.3), (26.0, 33.5)]
P_EASTWEST = [ABQAIQ, (47.5, 25.3), (45.0, 24.7), (42.0, 24.4), (39.8, 24.2), YANBU]
P_HABSHAN = [HABSHAN, (54.6, 24.1), (55.5, 24.6), (56.0, 25.0), FUJAIRAH]
R_NORTH = [(55.90, 26.55), (56.20, 26.75), (56.30, 26.90), (56.45, 26.96), (56.75, 26.86), (57.02, 26.62)]     # Iran-approved route (CSIS: closer to Iranian waters)
R_SOUTH = [(55.95, 26.30), (56.25, 26.42), (56.48, 26.42), (56.62, 26.25), (56.62, 25.95)]     # the southern corridor, Omani side
R_SHUTTLE = [(55.60, 26.28), (55.95, 26.30), (56.25, 26.42), (56.48, 26.42), (56.62, 26.25), (56.62, 25.80), (56.50, 25.40)]
LINE_GAP = [LARAK, QUOIN]

# ---- zones: the two lanes, 2 nmi each with a 2 nmi buffer, drawn schematically (FACTS F02) ----
# FACTCHECK 9 Oct: redrawn so both lanes sit on the Omani side of the Larak-Quoin median (the old drawing put the
# inbound lane, and the eastern ends of both, nearer Iran's coast than Oman's, against the narration). Still schematic.
Z_INBOUND = [(56.088, 26.408), (56.23, 26.514), (56.416, 26.591), (56.581, 26.573), (56.688, 26.405), (56.728, 26.122),
             (56.765, 26.126), (56.724, 26.414), (56.604, 26.599), (56.409, 26.624), (56.21, 26.542), (56.064, 26.433)]
Z_OUTBOUND = [(56.112, 26.382), (56.25, 26.486), (56.424, 26.559), (56.559, 26.547), (56.652, 26.395), (56.692, 26.118),
              (56.655, 26.114), (56.616, 26.386), (56.536, 26.521), (56.431, 26.526), (56.27, 26.458), (56.136, 26.357)]
Z_SOUTH = [(55.95, 26.36), (56.30, 26.47), (56.55, 26.45), (56.68, 26.25), (56.68, 25.90), (56.56, 25.90),
           (56.56, 26.22), (56.45, 26.37), (56.25, 26.37), (55.95, 26.26)]

# ---- attack pins, 1-8 Oct (approximate, from UKMTO / Windward descriptions) ----
# 10 Oct: #2 nudged 0.025E (about 2.5 km, inside the descriptions' uncertainty) so its ring sits in water clear of Musandam.
OCT_HITS = [(56.46, 26.40), (56.505, 26.26), (56.52, 26.42), (56.57, 26.12), (56.47, 25.97), (56.60, 26.30)]

CAP_EIA = "FUENTE: EIA DE EE. UU. · TODAY IN ENERGY · 16 JUN 2025"
CAP_LANES = "CARRILES ESQUEMÁTICOS · ANCHOS: EIA DE EE. UU."
CAP_ROUTES = "RUTAS MARÍTIMAS Y OLEODUCTOS ESQUEMÁTICOS"

CHAPTERS = [
    dict(id="open", hero="yellow", title="", beats=[
        ("El ocho de octubre, solo ocho barcos cruzaron el estrecho de Ormuz. Y sin embargo, según una empresa de rastreo, las exportaciones de crudo de Oriente Medio han vuelto más o menos al nivel de antes de la guerra.",
         ("map", {"view": V_NARROWS,
                  "labels": [(56.44, 26.67, "ESTRECHO DE ORMUZ", "26.6N 56.4E · 8 OCT 2026"), (56.62, 26.95, "8 BARCOS", "5 ENTRAN · 3 SALEN · WINDWARD", "data")],
                  "routes": [R_GULF_OUT[4:11]], "pins": [], "zones": [Z_INBOUND, Z_OUTBOUND],
                  "caption": "TRÁNSITOS: WINDWARD, DATOS AL 8 OCT 2026 · " + CAP_LANES})),
        ("Antes de que empezaran los combates en febrero, unos ciento veinticinco grandes barcos pasaban cada día por este paso.",
         ("split", ("~125", "GRANDES BARCOS AL DÍA · ANTES DEL 28 FEB"), ("8", "8 DE OCTUBRE DE 2026 · WINDWARD"))),
        ("Las dos cosas son ciertas a la vez, y la brecha entre ambas es la verdadera historia del estrecho.",
         ("words", "CERRADO A LOS BARCOS · ABIERTO AL PETRÓLEO")),
        ("Este video trata de cómo un canal que se puede cruzar en lancha rápida en menos de una hora llegó a tener en sus manos el precio del petróleo, y de por qué su verdadero poder no es el que casi todo el mundo imagina.",
         ("map", {"view": V_WORLD,
                  "labels": [(56.4, 26.6, "ORMUZ", "26.6N 56.4E")],
                  "routes": [], "pins": [(56.4, 26.6)], "zones": [],
                  "caption": "EIA DE EE. UU. · 2024 · RUTA ESQUEMÁTICA"})),
        ("Antes de terminar verás el estrecho de cerca, el truco que sacó el petróleo de todos modos y las tres cosas que yo vigilaría de aquí en adelante.",
         ("map", {"view": V_GULF,
                  "labels": [(53.6, 29.3, "IRÁN", "", {"ink": "magenta"}), (48.9, 24.6, "ARABIA SAUDITA", "", {"ink": "grey"}), (54.3, 23.6, "EAU", "", {"ink": "grey"}),
                             (57.6, 23.0, "OMÁN", "", {"ink": "green"}), (51.2, 25.3, "QATAR", "", {"ink": "grey"}), (47.9, 29.4, "KUWAIT", "", {"ink": "grey"})],
                  "routes": [], "pins": [(56.4, 26.6)], "zones": [], "caption": ""})),
    ]),
    dict(id="gap", hero="cyan", title="EL PASO", beats=[
        ("El golfo Pérsico es un mar casi cerrado, y su única salida al océano abierto es este recodo entre Irán y la punta de Omán.",
         ("map", {"view": V_STRAIT,
                  "labels": [(BANDAR_ABBAS[0], BANDAR_ABBAS[1], "BANDAR ABBAS", "IRÁN · 27.2N 56.3E", {"ink": "magenta"}),
                             (MUSANDAM[0], MUSANDAM[1], "MUSANDAM", "OMÁN · 25.9N 56.2E", {"ink": "green"}),
                             (KHASAB[0], KHASAB[1], "KHASAB", "26.2N 56.3E", {"ink": "green"})],
                  "routes": [], "pins": [], "zones": [], "caption": "COORDENADAS: ARTÍCULOS DE WIKIPEDIA"})),
        (("En su punto más estrecho, entre la isla iraní de Larak y la isla omaní de Gran Quoin, el agua mide unas veintiuna millas náuticas de ancho.", "En su punto más estrecho, entre la isla iraní de Larak y la isla omaní de Gran Cuoin, el agua mide unas veintiuna millas náuticas de ancho."),
         ("map", {"view": V_NARROWS,
                  "labels": [(LARAK[0], LARAK[1], "LARAK", "IRÁN · 26.9N 56.4E", {"ink": "magenta"}),
                             (QUOIN[0], QUOIN[1], "GRAN QUOIN", "OMÁN · 26.5N 56.5E", {"ink": "green"}),
                             (56.48, 26.67, "21 MN", "MILLAS NÁUTICAS · UNOS 39 KM", "data")],
                  "routes": [LINE_GAP], "kinds": ["line"], "pins": [LARAK, QUOIN], "pin_inks": ["magenta", "green"], "zones": [],
                  "caption": "ANCHO MÍNIMO: EIA DE EE. UU. (2012) · WIKIPEDIA"})),
        ("En kilómetros son unos treinta y nueve, y los carriles marcados son aún más estrechos.",
         ("num", "39 KM", "ANCHO MÍNIMO · UNAS 21 MILLAS NÁUTICAS · DE LARAK A GRAN QUOIN")),
        ("Los grandes buques siguen dos carriles marcados, el de entrada al norte y el de salida al sur. Cada carril mide unas dos millas de ancho, con una franja de separación del mismo ancho entre ambos.",
         ("map", {"view": V_NARROWS,
                  "labels": [(56.12, 26.68, "ENTRADA", "≈2 MILLAS"), (56.45, 26.36, "SALIDA", "≈2 MILLAS")],
                  "routes": [], "pins": [], "zones": [Z_INBOUND, Z_OUTBOUND], "caption": CAP_LANES})),
        (("Esos carriles están en aguas de Omán, pero las islas que los dominan, Qeshm, Ormuz y Larak, pertenecen a Irán.", "Esos carriles están en aguas de Omán, pero las islas que los dominan, Keshm, Ormuz y Larak, pertenecen a Irán."),
         ("map", {"view": V_STRAIT,
                  "labels": [(LARAK[0], LARAK[1], "LARAK", "IRÁN · 26.9N 56.4E", {"ink": "magenta"}),     # critic ES v1: LARAK placed first so its plate sits below its own pin, not beside ORMUZ's
                             (QESHM[0], QESHM[1], "QESHM", "IRÁN · 26.8N 55.8E", {"ink": "magenta"}),
                             (HORMUZ_I[0], HORMUZ_I[1], "ORMUZ", "IRÁN · 27.1N 56.5E", {"ink": "magenta"})],
                  "routes": [], "pins": [QESHM, HORMUZ_I, LARAK], "pin_inks": "magenta", "zones": [Z_INBOUND, Z_OUTBOUND], "caption": CAP_LANES})),
        ("Más al oeste, Irán también controla las dos islas Tunb y Abu Musa, que tomó en 1971 y que los Emiratos todavía reclaman.",
         ("map", {"view": V_STRAIT,
                  "labels": [(G_TUNB[0], G_TUNB[1], "TUNB MAYOR", "26.3N 55.3E", {"ink": "magenta"}), (L_TUNB[0], L_TUNB[1] - 0.12, "TUNB MENOR", "26.2N 55.1E", {"ink": "magenta"}),
                             (ABU_MUSA[0], ABU_MUSA[1], "ABU MUSA", "EN MANOS DE IRÁN · RECLAMADA POR EAU", {"ink": "magenta"})],
                  "routes": [], "pins": [G_TUNB, L_TUNB, ABU_MUSA], "pin_inks": "magenta", "zones": [], "caption": "TOMADAS POR IRÁN EN 1971"})),
        ("Así que los carriles pasan por las aguas de un país y junto a las islas de otro, y pronto verás por qué eso importó menos de lo que nadie esperaba.",
         ("split", ("OMÁN", "LOS CARRILES"), ("IRÁN", "LAS ISLAS"))),
    ]),
    dict(id="flows", hero="yellow", title="LO QUE FLUYE", beats=[
        ("Antes de la guerra, unos veinte millones de barriles de petróleo cruzaban el estrecho cada día, según la Administración de Información Energética de Estados Unidos.",
         ("num", "20M", "BARRILES DE PETRÓLEO AL DÍA POR ORMUZ · 2024 · EIA DE EE. UU.")),
        ("Eso equivale a más o menos una quinta parte de todo el petróleo que consume el mundo.",
         ("num", "~20%", "DEL CONSUMO MUNDIAL DE PETRÓLEO · 2024 · EIA DE EE. UU.")),
        ("También era más de una cuarta parte de todo el petróleo que se comercia por mar, y cerca de una quinta parte del comercio mundial de gas natural licuado, en su mayoría de Qatar.",
         ("split", ("> 1/4", "DEL COMERCIO MARÍTIMO DE PETRÓLEO"), ("~1/5", "DEL COMERCIO MUNDIAL DE GNL · SOBRE TODO QATAR"))),
        ("Arabia Saudita es el país que más envía por él, seguida de Irak, los Emiratos, Irán, Kuwait y Qatar.",
         ("map", {"view": V_GULF,
                  "labels": [(RAS_TANURA[0], RAS_TANURA[1], "RAS TANURA", "ARABIA SAUDITA · 38% DEL CRUDO DE ORMUZ", "data"),
                             (KHARG[0], KHARG[1], "KHARG", "IRÁN · 29.2N 50.3E", {"ink": "magenta"}),
                             (RAS_LAFFAN[0], RAS_LAFFAN[1], "RAS LAFFAN", "QATAR · GNL · 25.9N 51.5E")],
                  "routes": [R_GULF_OUT], "pins": [RAS_TANURA, KHARG, RAS_LAFFAN], "zones": [], "caption": CAP_EIA})),
        ("Ahora síguelo hacia el resto del mundo.",
         ("map", {"view": V_WORLD,
                  "labels": [(69.8, 22.45, "INDIA", "1.9M B/D", "data"), (122.3, 29.8, "CHINA", "4.8M B/D", "data"),
                             (129.4, 35.5, "COREA DEL SUR", "1.7M B/D", "data"), (139.8, 35.3, "JAPÓN", "1.5M B/D", "data"),
                             (30.0, 33.0, "EUROPA", "0.7M B/D", "data")],
                  "routes": [R_INDIA, R_CHINA, R_JAPAN, R_KOREA, R_EUROPE], "pins": [], "zones": [],
                  "caption": "CRUDO DE ORMUZ POR DESTINO, 2024 · EIA / VORTEXA · " + CAP_ROUTES})),
        ("En 2024, cerca del ochenta y cuatro por ciento del crudo que cruzó el estrecho fue a Asia.",
         ("num", "84%", "DEL CRUDO Y CONDENSADO DE ORMUZ FUE A ASIA · 2024 · EIA DE EE. UU.")),
        ("Solo China se llevó cerca de un tercio, con India, Corea del Sur y Japón muy por detrás.",
         ("map", {"view": (55.0, -2.0, 145.0, 42.0),
                  "labels": [(122.3, 29.8, "CHINA", "CERCA DE UN TERCIO · 4.8M B/D", "data"), (69.8, 22.45, "INDIA", "1.9M B/D", "data"),
                             (129.4, 35.5, "COREA DEL SUR", "1.7M B/D", "data"), (139.8, 35.3, "JAPÓN", "1.5M B/D", "data")],
                  "routes": [R_CHINA, R_INDIA, R_JAPAN, R_KOREA], "pins": [], "zones": [],
                  "caption": "EIA DE EE. UU. / VORTEXA · 2024 · " + CAP_ROUTES})),
        ("Europa se llevó alrededor del cinco por ciento, y Estados Unidos, apenas un tres por ciento.",
         ("split", ("~5%", "EUROPA"), ("~3%", "EE. UU. · PARTE DEL CRUDO DE ORMUZ · 2024 · EIA"))),
        ("Así que el estrecho le importa sobre todo a Asia, pero, como verás, su precio se paga en todas partes.",
         ("words", "EL PETRÓLEO ES DE ASIA · EL PRECIO ES DE TODOS")),
    ]),
    dict(id="closing", hero="orange", title="EL CIERRE", beats=[
        ("El veintiocho de febrero, Estados Unidos e Israel empezaron a atacar a Irán, y en pocas horas la Guardia Revolucionaria iraní advertía por radio a los barcos que no pasaría ninguno.",
         ("map", {"view": V_STRAIT,
                  "labels": [(BANDAR_ABBAS[0], BANDAR_ABBAS[1], "28 FEB 2026", "AVISOS POR RADIO A LOS BARCOS", "event")],
                  "routes": [], "pins": [BANDAR_ABBAS], "pin_kinds": "event", "zones": [Z_INBOUND, Z_OUTBOUND], "caption": "FUENTE: REUTERS · AVISO UKMTO 003-26"})),
        ("El dos de marzo, según el Centro de Estudios Estratégicos e Internacionales, el estrecho ya estaba prácticamente cerrado.",
         ("num", "2 MAR", "ESTRECHO PRÁCTICAMENTE CERRADO · CSIS, 22 ABR 2026")),
        ("Diez días después, la Agencia Internacional de Energía dio su veredicto sobre lo que estaba pasando.",
         ("quote", "La guerra en Oriente Medio está provocando la mayor interrupción del suministro en la historia del mercado mundial del petróleo.",
          "AIE · OIL MARKET REPORT · 12 MAR 2026 · TRADUCCIÓN PROPIA")),
        ("Sus miembros acordaron poner en el mercado cuatrocientos millones de barriles de reservas de emergencia.",
         ("num", "400M", "BARRILES DE RESERVAS DE EMERGENCIA LIBERADOS · ACORDADO EL 11 MAR · AIE")),
        ("Los productores del Golfo, sin tener adónde enviar su crudo, recortaron su producción en al menos diez millones de barriles diarios.",
         ("num", "−10M", "COMO MÍNIMO · B/D DE PRODUCCIÓN DEL GOLFO RECORTADOS · MARZO 2026 · AIE")),
        ("Un cargamento físico de crudo Brent costaba unos setenta y un dólares por barril antes de la guerra. A principios de abril casi se había duplicado, hasta su nivel más alto desde julio de 2008.",
         ("split", ("$71.32", "BRENT AL CONTADO · 27 FEB"), ("$138.21", "7 ABR · MÁXIMO DESDE JULIO DE 2008 · EIA"))),
        ("Luego vinieron meses de avances y retrocesos.",
         ("tl", [("28 FEB", "EMPIEZAN LOS ATAQUES"), ("2 MAR", "PRÁCTICAMENTE CERRADO"), ("13 ABR", "BLOQUEO DE EE. UU. A IRÁN"),
                 ("17 ABR", "ABIERTO UN DÍA"), ("17 JUN", "ACUERDO · BREVE REAPERTURA"), ("6 JUL", "MISILES CONTRA BARCOS"),
                 ("6 OCT", "9 ATAQUES A PETROLEROS")])),
        ("En abril, Irán declaró abierto el estrecho, y su Guardia Revolucionaria lo volvió a cerrar al día siguiente.",
         ("map", {"view": V_NARROWS,
                  "labels": [(56.62, 26.95, "17 ABR · ABIERTO", "18 ABR · CERRADO", "event"), (56.30, 26.40, "AL MENOS 13", "PETROLEROS LOGRARON PASAR · CSIS", "data")],
                  "routes": [R_GULF_OUT[4:11]], "pins": [], "zones": [Z_INBOUND, Z_OUTBOUND], "caption": "FUENTE: CSIS · STARBOARD MARITIME INTELLIGENCE"})),
        ("En junio, un acuerdo entre Washington y Teherán trajo una reapertura breve y parcial. Empezó a desmoronarse a principios de julio, cuando unos misiles alcanzaron a un buque gasero qatarí y a un petrolero saudí.",
         ("map", {"view": V_STRAIT,
                  "labels": [(56.60, 25.95, "6–7 JUL", "GASERO QATARÍ ATACADO · LIMAH, OMÁN", "event")],
                  "routes": [], "pins": [(56.60, 25.95)], "pin_kinds": "event", "zones": [], "caption": "FUENTE: AL JAZEERA / REUTERS · UKMTO · POSICIÓN APROXIMADA"})),
        ("Así que durante la mayor parte de este año el estrecho ha estado cerrado en la práctica, y lo curioso, como veremos ahora, es cómo.",
         ("words", "¿CÓMO SE CIERRA UN ESTRECHO?")),
    ]),
    dict(id="how", hero="magenta", title="CÓMO SE CIERRA UN ESTRECHO", beats=[
        ("Nadie levantó un muro sobre el agua. El cierre se hizo con avisos por radio, drones, misiles y algún que otro apresamiento, dirigidos contra un número reducido de barcos.",
         ("map", {"view": V_NARROWS,
                  "labels": [(56.62, 26.95, "EL CIERRE", "AVISOS · DRONES · MISILES · APRESAMIENTOS", "event")],
                  "routes": [], "pins": OCT_HITS[:3], "pin_kinds": "event", "zones": [Z_INBOUND, Z_OUTBOUND], "caption": "UKMTO · WINDWARD · POSICIONES APROXIMADAS"})),
        ("Con eso bastó, porque antes de que un petrolero zarpe, alguien tiene que estar dispuesto a asegurarlo.",
         ("words", "¿ALGUIEN ASEGURARÁ EL BARCO?")),
        ("En los primeros días de marzo, el seguro de riesgo de guerra pasó de costar una quinta parte del uno por ciento del valor del barco a costar hasta el uno por ciento.",
         ("split", ("~0.2%", "DEL VALOR DEL BARCO · FINALES DE FEBRERO"), ("1%", "INICIOS DE MARZO · SECTOR, VÍA AL JAZEERA"))),
        ("En un superpetrolero nuevo, ese uno por ciento supera el millón de dólares por un solo viaje.",
         ("num", "$1.3M", "POR VIAJE · 1% DE UN SUPERPETROLERO NUEVO DE ~$130M · PRECIO: WINDWARD")),
        ("En marzo, el secretario general de la Organización Marítima Internacional dijo que unos veinte mil marinos estaban atrapados dentro del Golfo, sin poder salir con seguridad.",
         ("map", {"view": V_GULF,
                  "labels": [(51.8, 27.2, "≈20 000 MARINOS", "ATRAPADOS EN EL GOLFO · OMI, MARZO 2026", "data")],
                  "routes": [], "pins": [], "zones": [], "caption": "FUENTE: SECRETARIO GENERAL DE LA OMI, 18 MAR 2026"})),
        ("Entonces Irán ofreció sus propias condiciones. Los barcos aprobados tomarían una ruta más cercana a su costa, compartirían los datos de su travesía y, en algunos casos, pagarían una tarifa.",
         ("map", {"view": V_NARROWS,
                  "labels": [(56.45, 26.98, "RUTA APROBADA POR IRÁN", "MÁS CERCA DE LA COSTA IRANÍ", {"ink": "magenta"}), (56.70, 26.10, "CORREDOR SUR", "LADO OMANÍ", {"ink": "green"})],
                  "routes": [R_NORTH, R_SOUTH], "pins": [LARAK], "pin_inks": "magenta", "zones": [], "caption": "CSIS, ABRIL 2026 · RUTAS ESQUEMÁTICAS"})),
        ("Más de la mitad de los barcos que pasaron en marzo y abril los operaban empresas de solo cuatro países, con China a la cabeza.",
         ("num", "187", "BARCOS · 4 MAR–22 ABR · MÁS DE LA MITAD DE 4 PAÍSES · CHINA PRIMERO · CSIS")),
        ("Así que el cierre funcionó como un sistema de permisos, y los productores del Golfo se pusieron a buscar cómo rodearlo.",
         ("words", "UN SISTEMA DE PERMISOS")),
    ]),
    dict(id="around", hero="green", title="EL RODEO", beats=[
        ("Arabia Saudita ya tenía una forma de rodearlo. Su oleoducto Este-Oeste lleva crudo a través del desierto desde Abqaiq, cerca del Golfo, hasta el puerto de Yanbu, en el mar Rojo.",
         ("map", {"view": V_PIPES,
                  "labels": [(43.5, 24.9, "OLEODUCTO ESTE–OESTE", "5M B/D NOMINAL · 7M AMPLIADO · EIA", "flow")],
                  "routes": [P_EASTWEST], "pins": [ABQAIQ, YANBU], "zones": [], "caption": "CAPACIDAD: EIA DE EE. UU. · " + CAP_ROUTES})),
        ("Su capacidad normal es de cinco millones de barriles diarios. A finales de marzo, según la prensa, funcionaba a pleno rendimiento, con su capacidad ampliada de siete millones.",
         ("num", "7M", "BARRILES DIARIOS · OLEODUCTO ESTE–OESTE A PLENA CAPACIDAD · 28 MAR · BLOOMBERG")),
        (("Los Emiratos tienen un oleoducto más pequeño, desde sus campos de Habshan hasta Fujairah, que está fuera del estrecho, en el golfo de Omán.", "Los Emiratos tienen un oleoducto más pequeño, desde sus campos de Habshan hasta Fuyaira, que está fuera del estrecho, en el golfo de Omán."),
         ("map", {"view": V_GULF,
                  "labels": [(HABSHAN[0], HABSHAN[1], "HABSHAN", "EAU · 23.8N 53.6E"), (FUJAIRAH[0], FUJAIRAH[1], "FUJAIRAH", "FUERA DEL ESTRECHO · 1.5–1.8M B/D", "flow")],
                  "routes": [P_HABSHAN], "pins": [HABSHAN, FUJAIRAH], "zones": [], "caption": "CAPACIDAD: EIA DE EE. UU. · " + CAP_ROUTES})),
        ("Antes de la guerra, la agencia de energía estadounidense calculaba que solo había unos dos millones y medio de barriles diarios de capacidad libre en oleoductos para esquivar el estrecho.",
         ("num", "2.6M", "B/D DE CAPACIDAD LIBRE DE DESVÍO · ARABIA SAUDITA + EAU · EIA, JUN 2025")),
        ("Frente a veinte millones de barriles diarios, aquello parecía una causa perdida.",
         ("split", ("20M", "B/D POR EL ESTRECHO"), ("2.6M", "B/D DE OLEODUCTO LIBRE"))),
        ("El segundo truco son los barcos lanzadera. Son petroleros pequeños, muchas veces con el transpondedor apagado, que cruzan el estrecho con crudo y lo bombean a petroleros gigantes que esperan fuera.",
         ("map", {"view": V_STRAIT,
                  "labels": [(55.60, 26.20, "CARGAN LAS LANZADERAS", "DENTRO DEL GOLFO", "flow"), (56.50, 25.40, "DE BUQUE A BUQUE", "A SUPERPETROLEROS FUERA", "flow")],
                  "routes": [R_SHUTTLE], "pins": [(56.50, 25.40)], "zones": [], "caption": "AL JAZEERA · WINDWARD · RUTA ESQUEMÁTICA"})),
        ("El siete de octubre, la empresa de rastreo Windward contó unos once millones de barriles de crudo que salieron por el estrecho, la mayoría mediante transbordos de buque a buque.",
         ("num", "11.1M", "BARRILES SALIERON POR ORMUZ EL 7 OCT · 9.1M DE BUQUE A BUQUE · WINDWARD")),
        (("Si se suman los oleoductos, los analistas de Kpler calculan que cerca del cuarenta por ciento de las exportaciones de petróleo de la región ya no pasan por el estrecho.", "Si se suman los oleoductos, los analistas de Kepler calculan que cerca del cuarenta por ciento de las exportaciones de petróleo de la región ya no pasan por el estrecho."),
         ("num", "~40%", "DE LAS EXPORTACIONES DE LA REGIÓN EVITAN ORMUZ · KPLER VÍA AL JAZEERA · 6 OCT")),
        (("A finales de septiembre, las cifras provisionales de Kpler situaban las exportaciones de crudo de Oriente Medio en unos dieciocho millones de barriles diarios, más o menos como antes de la guerra.", "A finales de septiembre, las cifras provisionales de Kepler situaban las exportaciones de crudo de Oriente Medio en unos dieciocho millones de barriles diarios, más o menos como antes de la guerra."),
         ("split", ("~18.0M", "B/D · PROMEDIO DEL AÑO ANTES DE LA GUERRA"), ("18.3M", "PROMEDIO DE 7 DÍAS · 30 SEP · KPLER, PROVISIONAL"))),
        ("Yo lo tomaría con cautela, porque los datos de la Agencia Internacional de Energía para agosto, un mes antes y con combustibles además de crudo, todavía situaban las exportaciones del Golfo en apenas la mitad de su nivel de antes de la guerra.",
         ("split", ("~½", "EXPORTACIONES DE PETRÓLEO DEL GOLFO · AGOSTO · AIE"), ("≈ PREGUERRA", "CRUDO DE ORIENTE MEDIO · FIN DE SEPTIEMBRE · KPLER"))),
        ("En cualquier caso, el petróleo vuelve a moverse, y precisamente por eso los ataques han cambiado, lo que nos lleva a este mes.",
         ("map", {"view": V_STRAIT,
                  "labels": [(57.15, 25.85, "OCTUBRE", "", "event")],
                  "routes": [R_SOUTH], "pins": [], "zones": [Z_SOUTH], "zone_inks": "orange", "caption": "CORREDOR Y RUTA ESQUEMÁTICOS"})),
    ]),
    dict(id="october", hero="orange", title="OCTUBRE", beats=[
        ("En los seis primeros días de octubre, la oficina de comercio marítimo de la Marina Real británica, conocida como UKMTO, registró nueve ataques contra petroleros en el estrecho.",
         ("num", "9", "ATAQUES CONTRA PETROLEROS EN EL ESTRECHO · 1–6 OCT 2026 · UKMTO VÍA AFP")),
        ("Eso ya era la mitad del total de septiembre, sumando el estrecho y todo el Golfo.",
         ("split", ("9", "EN EL ESTRECHO · 1–6 DE OCTUBRE"), ("~18", "ESTRECHO Y GOLFO · TODO SEPTIEMBRE · UKMTO"))),
        ("Fíjate en dónde fueron atacados los barcos.",
         ("map", {"view": V_NARROWS,
                  "labels": [(56.80, 26.20, "1–6 OCT", "PETROLEROS ATACADOS", "event")],
                  "routes": [], "pins": OCT_HITS, "pin_kinds": "event", "zones": [Z_SOUTH], "zone_inks": "orange", "caption": "UKMTO · WINDWARD · POSICIONES APROXIMADAS"})),
        ("Según Windward, todos los barcos atacados que pudo confirmar navegaban sin emitir su posición por el corredor sur, del lado omaní, la ruta de la que dependen las lanzaderas.",
         ("map", {"view": V_NARROWS,
                  "labels": [(56.72, 26.05, "CORREDOR SUR", "TODOS LOS BLANCOS CONFIRMADOS · SIN AIS", "event")],
                  "routes": [R_SHUTTLE[1:6]], "pins": OCT_HITS, "pin_kinds": "event", "zones": [Z_SOUTH], "zone_inks": "orange", "caption": "WINDWARD, 9 OCT 2026 · CORREDOR ESQUEMÁTICO"})),
        (("Luego, el día siete, un petrolero fue atacado mucho más al oeste, frente a la costa norte de Qatar, y el ocho había otro en llamas frente a Fujairah, según los primeros informes.", "Luego, el día siete, un petrolero fue atacado mucho más al oeste, frente a la costa norte de Qatar, y el ocho había otro en llamas frente a Fuyaira, según los primeros informes."),
         ("map", {"view": V_GULF,
                  "labels": [(QATAR_HIT[0], QATAR_HIT[1], "7 OCT", "PETROLERO ATACADO · 94 KM AL N DE QATAR", "event"), (FUJ_HIT[0], FUJ_HIT[1], "8 OCT", "PETROLERO EN LLAMAS · FRENTE A FUJAIRAH", "event")],
                  "routes": [], "pins": [QATAR_HIT, FUJ_HIT], "pin_kinds": "event", "zones": [], "caption": "UKMTO VÍA AFP · WINDWARD · POSICIONES APROXIMADAS"})),
        (("Fujairah es donde el oleoducto de desvío de los Emiratos llega al mar.", "Fuyaira es donde el oleoducto de desvío de los Emiratos llega al mar."),
         ("map", {"view": V_STRAIT,
                  "labels": [(FUJAIRAH[0], FUJAIRAH[1], "FUJAIRAH", "FINAL DEL OLEODUCTO DE DESVÍO"), (FUJ_HIT[0] + 0.25, FUJ_HIT[1] + 0.12, "8 OCT", "ATAQUE A ~10 MN", "event")],
                  "routes": [P_HABSHAN[2:]], "pins": [FUJAIRAH, FUJ_HIT], "pin_kinds": ["place", "event"], "zones": [], "caption": "WINDWARD · " + CAP_ROUTES})),
        ("Si lo estoy leyendo bien, los ataques están siguiendo al petróleo, fuera del estrecho y hacia las rutas que se construyeron para evitarlo.",
         ("words", "LOS ATAQUES SIGUEN AL PETRÓLEO")),
        ("Y mover el petróleo dando un rodeo tiene un costo que nos alcanza a todos.",
         ("map", {"view": V_WORLD,
                  "labels": [(56.4, 26.6, "ORMUZ", "")],
                  "routes": [R_CHINA, R_EUROPE], "pins": [(56.4, 26.6)], "zones": [], "caption": CAP_ROUTES})),
    ]),
    dict(id="price", hero="yellow", title="EL PRECIO DEL DESVÍO", beats=[
        ("Cada lanzadera, cada desvío y cada póliza de seguro necesita barcos, y en el mundo no hay superpetroleros de sobra.",
         ("words", "NO HAY SUPERPETROLEROS DE SOBRA")),
        ("Según Windward, el flete supone ahora entre una cuarta parte y casi un tercio del costo del crudo del Golfo puesto en destino, cuando en tiempos normales es de entre el uno y el tres por ciento.",
         ("split", ("1–3%", "PESO DEL FLETE EN EL COSTO EN DESTINO · NORMAL"), ("25–30%", "AHORA · WINDWARD, 9 OCT 2026"))),
        ("Un superpetrolero de segunda mano se habría vendido por un precio récord, muy por encima de lo que cuesta uno nuevo.",
         ("split", ("~$200M", "SUPERPETROLERO USADO · UN RÉCORD"), ("~$130M", "UNO NUEVO · WINDWARD"))),
        ("Y el petróleo tiene ahora dos precios. El seis de octubre, los futuros del Brent, el precio de papel de los titulares, cotizaban justo por debajo de los cien dólares.",
         ("num", "$99.57", "FUTUROS DEL BRENT · 6 OCT 2026 · OILPRICE.COM VÍA AL JAZEERA")),
        ("El precio de un cargamento real, según la agencia de energía estadounidense, era de ciento veinticinco.",
         ("split", ("$99.57", "PAPEL · FUTUROS DEL BRENT"), ("$125.44", "FÍSICO · BRENT AL CONTADO · EIA · 6 OCT"))),
        ("Esa diferencia mide lo escasos que son ahora los barriles reales, y yo la veo como parte del peaje del estrecho.",
         ("words", "LA DIFERENCIA ES ESCASEZ")),
        ("Mientras tanto, el mundo ha estado viviendo de sus ahorros. Según la Agencia Internacional de Energía, las reservas mundiales de petróleo han caído en más de quinientos millones de barriles desde que empezó la guerra.",
         ("num", "−507M", "BARRILES SACADOS DE LAS RESERVAS MUNDIALES · FEB A FIN DE AGO · AIE, SEP 2026")),
        ("La agencia prevé ahora que la demanda mundial de petróleo caiga este año, por el efecto de los precios altos.",
         ("num", "−2.5M", "B/D · DEMANDA MUNDIAL DE PETRÓLEO EN 2026 · PRONÓSTICO · AIE, SEPTIEMBRE 2026")),
        ("En Estados Unidos, un galón de gasolina regular costaba tres dólares con doce centavos hace un año. El cinco de octubre costaba cuatro dólares con treinta y cinco.",
         ("split", ("$3.12", "EL GALÓN · 6 OCT 2025"), ("$4.35", "5 OCT 2026 · EIA"))),
    ]),
    dict(id="verdict", hero="cyan", title="EL VEREDICTO", beats=[
        ("Entonces, ¿cuál es en realidad el poder del estrecho?",
         ("map", {"view": V_NARROWS, "labels": [], "routes": [], "pins": [], "zones": [Z_INBOUND, Z_OUTBOUND], "caption": CAP_LANES})),
        ("Mi respuesta es que Ormuz funciona menos como una llave de paso y más como un peaje.",
         ("split", ("LLAVE DE PASO", "LO QUE TODOS TEMÍAN"), ("UN PEAJE", "LO QUE RESULTÓ SER"))),
        ("Cerrarlo recortó el flujo con fuerza durante meses, pero nunca detuvo el petróleo. Una vez establecidos los desvíos, sobre todo encareció el transporte de cada barril, y el mundo recurrió a sus reservas para cubrir la diferencia.",
         ("words", "COBRA PEAJE A CADA BARRIL")),
        ("También muestra cómo es un cierre, porque este año vivimos algo muy parecido a uno.",
         ("list", ["EL PRECIO CASI SE DUPLICÓ · $71 → $138", "PRODUCCIÓN DEL GOLFO −10M+ B/D", "RESERVAS MUNDIALES −507M BARRILES",
                   "LA DEMANDA MUNDIAL CAE", "EL PETRÓLEO SIGUIÓ MOVIÉNDOSE"], "CÓMO FUE UN CIERRE")),
        ("El mundo no se quedó sin petróleo, pero hoy el colchón es menor que en marzo.",
         ("num", "−507M", "BARRILES SACADOS HASTA FIN DE AGOSTO · EL COLCHÓN ES MENOR · AIE")),
        (("Si tuviera que vigilar tres cosas, la primera serían nuevos ataques cerca de Fujairah y contra el oleoducto Este-Oeste, las rutas que mantuvieron el petróleo en movimiento.", "Si tuviera que vigilar tres cosas, la primera serían nuevos ataques cerca de Fuyaira y contra el oleoducto Este-Oeste, las rutas que mantuvieron el petróleo en movimiento."),
         ("map", {"view": V_PIPES,
                  "labels": [(YANBU[0], YANBU[1], "YANBU", "VIGILAR"), (FUJAIRAH[0], FUJAIRAH[1], "FUJAIRAH", "VIGILAR")],
                  "routes": [P_EASTWEST, P_HABSHAN], "pins": [YANBU, FUJAIRAH, FUJ_HIT], "pin_kinds": ["place", "place", "event"], "zones": [], "caption": CAP_ROUTES})),
        ("La segunda es el costo de fletar un superpetrolero, porque ahí es donde se cobra el peaje.",
         ("words", "EL COSTO DE UN SUPERPETROLERO")),
        ("La tercera es la diferencia entre el precio de papel y el precio físico, que te dice lo escasos que son los barriles reales.",
         ("list", ["1 · FUJAIRAH Y EL OLEODUCTO ESTE–OESTE", "2 · EL COSTO DE FLETAR UN SUPERPETROLERO", "3 · BRENT DE PAPEL VS. FÍSICO"],
          "QUÉ VIGILAR")),
        ("Nada de esto es un pronóstico ni un consejo financiero, y todas las fuentes y fechas están en la descripción.",
         ("words", "FUENTES EN LA DESCRIPCIÓN")),
        ("El ocho de octubre, ocho barcos cruzaron el estrecho, y aun así el petróleo encontró la forma de salir, a cambio de un precio.",
         ("map", {"view": V_NARROWS,
                  "labels": [(56.44, 26.67, "ESTRECHO DE ORMUZ", "26.6N 56.4E · 8 OCT 2026"), (56.62, 26.95, "8 BARCOS", "EL PETRÓLEO DIO UN RODEO", "data")],
                  "routes": [R_GULF_OUT[4:11], R_SHUTTLE], "pins": [], "zones": [Z_INBOUND, Z_OUTBOUND],
                  "caption": "TRÁNSITOS: WINDWARD · " + CAP_LANES})),
    ]),
]
