"""Spanish version of lf02_price/script.py (8 Oct 2026); same beats, same pictures.
THE CURVE · LONG-FORM 02 · THE PRICE OF THINKING (3 Oct 2026). The 22 September price war (EP13's story, at full
length): why the price of AI falls about tenfold a year, why rivals cut within hours, and why falling prices mean MORE
spending, not less. Prices in Big Macs, the house unit. The hidden mechanism: price is the only thing a buyer can read
in an afternoon, and switching costs nothing, so the labs run like the Red Queen; and cheaper thinking gets used so
much more (Jevons) that the total bill grows: it moves from your token to the build-out.

Sources (checked 3 Oct 2026): Simon Willison, 22 Sep 2026, "Claude Opus 5.5, GPT-6 Sol, GPT-6 Luna, and a new price
war" (prices, "around an hour later", GPT-5.6's 25% November rise, Grok 4.7 and MiMo v2.6 the day before, the pelican
that hit the 128,000-token limit); The Agent Report, "The Price War Moves to Cost Per Task"; IEA, Energy and AI (2025); SiliconANGLE, 22 Sep 2026; AIOS Guide, "The AI
Model Price War Arrived in a Two-Hour Window"; a16z, "Welcome to LLMflation" (Nov 2024: $60 -> $0.06 per million
tokens, 2021-2024); Epoch AI, "Algorithmic progress in language models" (2024: the compute needed for a given
performance halves about every eight months); The Economist's Big Mac index (US $6.12, January 2026); W. S. Jevons,
The Coal Question (1865); Satya Nadella on X, 27 Jan 2025; Google I/O 2024-2026 (9.7 trillion, 480 trillion, 3.2
quadrillion tokens a month); Dell'Oro Group (data-centre capex above $1 trillion in 2026); Lewis Carroll, Through the
Looking-Glass (1871); Leigh Van Valen, "A New Evolutionary Law" (1973); Nvidia's $5 trillion market value, 29 Oct 2025.
Visuals as in ../lf01_escape/script.py.
"""
TITLE = "EL PRECIO DE PENSAR"
TAG = "CURVAEXPLICA  ·  EL PRECIO DE PENSAR"
NAME = "lf02_price"
LANG = "es"
FIX = {}

CHAPTERS = [
    dict(id="open", title="", beats=[
        ("El veintidós de septiembre, un laboratorio de inteligencia artificial lanzó un nuevo modelo insignia, una quinta parte más barato que el anterior.",
         ("num", "−20%", "22 SEP 2026 · $5 → $4 POR MILLÓN DE TOKENS DE ENTRADA")),
        ("Unos noventa minutos después, su mayor rival respondió. Dos modelos nuevos, cada uno a la mitad del precio del anterior.",
         ("num", "−50%", "90 MINUTOS DESPUÉS · DOS MODELOS NUEVOS")),
        ("Dos empresas. Una tarde. Las dos bajaron sus precios.", ("words", "DOS EMPRESAS. UNA TARDE.")),
        ("Esto ya pasa todo el tiempo. El precio de la inteligencia artificial está cayendo más rápido de lo que jamás cayó el de los chips de computadora.",
         ("img", "p01")),
        ("Lo cual debería significar que la industria gasta menos. En cambio, va camino de gastar más de un billón de dólares este año, en edificios llenos de chips.",
         ("num", "$1 BILLÓN+", "GASTO EN CENTROS DE DATOS, 2026 · DELL'ORO · 1 BILLÓN = UN MILLÓN DE MILLONES")),
        ("Entonces, ¿quién está pagando en realidad para que pensar sea más barato? ¿Y qué pasará cuando sea casi gratis?", ("img", "p02")),
    ]),
    dict(id="afternoon", title="UNA TARDE", beats=[
        (("Ni siquiera fue el único lanzamiento de esa semana. El día anterior, xAI había presentado Grok 4.7, y el fabricante de teléfonos Xiaomi, dos modelos propios.", "Ni siquiera fue el único lanzamiento de esa semana. El día anterior, equis A I había presentado Grok 4.7, y el fabricante de teléfonos Xiaomi, dos modelos propios."),
         ("img", "p21")),
        ("El primer movimiento fue de Anthropic. Su nuevo modelo Opus, Claude Opus 5.5, costaba cuatro dólares por leer un millón de tokens de texto, en lugar de cinco, y veinte dólares por escribir un millón, en lugar de veinticinco.",
         ("split", ("$4", "LEER UN MILLÓN DE TOKENS · ANTES $5"), ("$20", "ESCRIBIR UN MILLÓN · ANTES $25"))),
        ("Leer texto que ya había visto se volvió un sesenta por ciento más barato.", ("num", "−60%", "LECTURAS EN CACHÉ · $0.50 → $0.20")),
        ("Después, OpenAI lanzó GPT-6 Sol, a dos dólares y diez dólares: la mitad del precio del modelo al que reemplazaba.",
         ("split", ("$2", "SOL · LEER"), ("$10", "SOL · ESCRIBIR"))),
        ("Y un hermano menor, GPT-6 Luna, a diez centavos por leer un millón de tokens.", ("num", "$0.10", "GPT-6 LUNA · POR MILLÓN DE TOKENS LEÍDOS")),
        ("El programador Simon Willison dijo que Luna es uno de los modelos más baratos que OpenAI ha lanzado jamás.",
         ("quote", "uno de los modelos más baratos que OpenAI ha lanzado jamás", "SIMON WILLISON · 22 SEP 2026")),
        ("Y había un detalle más discreto. El anterior GPT 5.6 tiene un precio promocional que OpenAI solo garantiza hasta finales de noviembre. Simon Willison espera un aumento del veinticinco por ciento.",
         ("num", "+25%?", "PROMO DE GPT-5.6 GARANTIZADA SOLO HASTA EL 21 NOV")),
        ("Modelos nuevos más baratos, y modelos viejos a punto de encarecerse. A todos los empujan en la misma dirección: hacia adelante.", ("words", "A TODOS LOS EMPUJAN HACIA ADELANTE.")),
    ]),
    dict(id="thousand", title="MIL VECES", beats=[
        ("Para ver lo extraño que es esto, retrocedamos cinco años.", ("img", "p03")),
        ("En 2021, la única inteligencia artificial capaz de alcanzar cierta puntuación en una prueba estándar de conocimientos costaba unos sesenta dólares por millón de tokens. A finales de 2024, el modelo más barato con la misma puntuación costaba seis centavos.",
         ("num", "1000×", "$60 → $0.06 POR MILLÓN DE TOKENS · 2021 → 2024 · a16z")),
        (("Mil veces más barato, en tres años. La firma de inversión a16z lo llamó LLMflation: unas diez veces más barato, cada año.", "Mil veces más barato, en tres años. La firma de inversión a dieciséis zeta lo llamó LLMflation: unas diez veces más barato, cada año."),
         ("words", "UNAS 10× MÁS BARATO, CADA AÑO")),
        ("En comparación, la Ley de Moore, la famosa duplicación de los transistores de un chip cada dos años, tarda unos veinte años en llegar a mil veces.",
         ("split", ("~20 AÑOS", "LEY DE MOORE · 1000×"), ("3 AÑOS", "IA · 1000×"))),
        ("Tres cosas hacen el trabajo a la vez. Cada nueva generación de chips hace más por cada vatio.", ("img", "p04")),
        ("Los propios modelos se vuelven más inteligentes por cada cálculo. Investigadores de Epoch AI estiman que el cómputo necesario para el mismo rendimiento se reduce a la mitad aproximadamente cada ocho meses.",
         ("num", "÷2", "CÓMPUTO PARA EL MISMO RESULTADO · CADA ~8 MESES · EPOCH AI")),
        ("Y los modelos grandes les enseñan a los pequeños: un modelo barato puede aprender a responder casi tan bien como uno caro, a partir de las respuestas del propio modelo caro.",
         ("img", "p05")),
        ("Y los laboratorios dejaron de cobrar el precio completo por el texto que un modelo ya leyó. Envía dos veces el mismo documento largo, y la segunda lectura cuesta una fracción.",
         ("num", "$0.20", "POR MILLÓN DE TOKENS EN CACHÉ · OPUS 5.5 Y SOL")),
    ]),
    dict(id="bigmac", title="EN BIG MACS", beats=[
        ("Los precios por millón de tokens no le dicen nada a la mayoría de la gente. Así que aquí va en la unidad que este canal usa siempre.", ("img", "p06")),
        ("Un Big Mac en Estados Unidos cuesta seis dólares con veintidós centavos.", ("num", "$6.22", "UN BIG MAC · EE. UU. · THE ECONOMIST, JUL 2026")),
        ("Un millón de tokens son unas setecientas cincuenta mil palabras. Más o menos ocho novelas.",
         ("num", "≈ 8 NOVELAS", "1 MILLÓN DE TOKENS ≈ 750 000 PALABRAS")),
        ("En 2021, hacer que una máquina leyera ocho novelas costaba unos diez Big Macs.", ("num", "≈ 10 BIG MACS", "$60 · LEER 8 NOVELAS · 2021")),
        ("Con GPT-6 Luna, cuesta más o menos la sesentava parte de uno.", ("num", "1/60", "DE UN BIG MAC · LEER 8 NOVELAS · 2026")),
        ("O dicho al revés. Por el precio de un Big Mac, una máquina ya puede leer unas quinientas novelas.",
         ("num", "≈ 500", "NOVELAS LEÍDAS · POR UN BIG MAC")),
        ("Escribir cuesta más que leer. Hacer que Opus 5.5 escriba un millón de tokens cuesta veinte dólares: un poco más de tres Big Macs.",
         ("num", "≈ 3 BIG MACS", "$20 · OPUS 5.5 ESCRIBE UN MILLÓN DE TOKENS")),
        ("Toda tu lista de lecturas. Cada reseña que ha recibido un restaurante. Años de tus correos.", ("img", "p07")),
    ]),
    dict(id="why", title="POR QUÉ BAJAN", beats=[
        ("Entonces, ¿por qué los laboratorios siguen bajando los precios, y tan rápido?", ("img", "p08")),
        ("Cuando un producto mejora cada pocos meses, los clientes en realidad comparan dos cosas. Qué tan bueno es, y cuánto cuesta.",
         ("list", ["¿CALIDAD?", "¿PRECIO?"])),
        ("Nadie puede saber qué tan bueno es en una tarde. Probar bien un modelo lleva semanas. El precio lo ve cualquiera en segundos.",
         ("split", ("SEMANAS", "PARA VER LA CALIDAD"), ("SEGUNDOS", "PARA VER EL PRECIO"))),
        ("Así que el precio es la señal. Y cambiar de proveedor no cuesta casi nada.", ("words", "EL PRECIO ES LA SEÑAL.")),
        ("La mayoría de estos modelos se invocan de la misma manera, por internet, a través de conexiones casi idénticas. Un desarrollador puede pasar de un laboratorio a otro cambiando una línea de código.",
         ("img", "p09")),
        ("Así que, cuando un laboratorio baja el precio, los clientes pueden abandonar al otro antes de que termine la tarde. El otro laboratorio tiene horas para responder, no semanas.",
         ("words", "HORAS, NO SEMANAS.")),
    ]),
    dict(id="queen", title="LA REINA ROJA", beats=[
        ("Los biólogos tienen un nombre para este tipo de carrera.", ("img", "a01", "LA REINA ROJA · JOHN TENNIEL, 1871")),
        ("En el libro «A través del espejo», la Reina Roja le dice a Alicia: hace falta correr todo lo que puedas para quedarte en el mismo lugar.",
         ("quote", "hace falta correr todo lo que puedas para quedarte en el mismo lugar.", "LA REINA ROJA · LEWIS CARROLL, 1871")),
        (("En 1973, el biólogo Leigh Van Valen la tomó prestada para explicar por qué las especies nunca parecen sacar ventaja. Sus rivales también siguen evolucionando.", "En 1973, el biólogo Li Van Valen la tomó prestada para explicar por qué las especies nunca parecen sacar ventaja. Sus rivales también siguen evolucionando."),
         ("img", "p10", "LEIGH VAN VALEN · \"A NEW EVOLUTIONARY LAW\" · 1973")),
        ("Los laboratorios corren tan rápido como pueden, y siguen exactamente en el mismo lugar unos frente a otros.", ("img", "p11")),
        ("Y con cada paso que dan, a ti te sale más barato.", ("words", "CADA PASO: MÁS BARATO PARA TI.")),
    ]),
    dict(id="paradox", title="LA PARADOJA", beats=[
        ("Si pensar es cada vez más barato, uno esperaría que el mundo gastara menos en ello. En 1865, un economista inglés explicó por qué pasa lo contrario.",
         ("img", "a02", "WILLIAM STANLEY JEVONS")),
        ("William Stanley Jevons notó que, a medida que las máquinas de vapor quemaban carbón con más eficiencia, Gran Bretaña quemaba más carbón, no menos.",
         ("img", "a03", "THE COAL QUESTION · 1865")),
        ("Haz que algo sea más barato de usar, y la gente le encuentra tantos usos nuevos que el total sube. Se llama la paradoja de Jevons.",
         ("words", "LA PARADOJA DE JEVONS")),
        ("Cuando un laboratorio chino lanzó un modelo barato y capaz en enero de 2025, el director ejecutivo de Microsoft, Satya Nadella, publicó: «La paradoja de Jevons ataca de nuevo».",
         ("quote", "¡La paradoja de Jevons ataca de nuevo!", "SATYA NADELLA · MICROSOFT · ENERO DE 2025")),
        ("Tenía razón. En la primavera de 2024, Google procesaba casi diez billones de tokens al mes.", ("num", "9.7 BILLONES", "TOKENS AL MES · GOOGLE · 2024")),
        ("En 2025, cuatrocientos ochenta billones.", ("num", "480 BILLONES", "TOKENS AL MES · GOOGLE · 2025")),
        ("En mayo de este año: tres mil doscientos billones. Más de trescientas veces más, en dos años.",
         ("num", "3200 BILLONES", "TOKENS AL MES · GOOGLE · MAYO 2026 · 3.2 MIL BILLONES")),
    ]),
    dict(id="catch", title="EL PERO", beats=[
        ("Hay un pero en todo esto. El precio de un token está bajando. La cantidad de tokens en cada respuesta está subiendo.",
         ("split", ("MENOS", "PRECIO POR TOKEN"), ("MÁS", "TOKENS POR RESPUESTA"))),
        ("Los modelos más nuevos piensan antes de responder, y escriben largas cadenas de razonamiento que nunca ves. Pagas por cada palabra.",
         ("img", "p22")),
        ("Cuando Simon Willison le pidió a Opus 5.5 el dibujo de un pelícano, con el nivel de pensamiento más alto, el modelo pensó hasta llegar a su límite de ciento veintiocho mil tokens, y nunca respondió.",
         ("num", "128 000", "TOKENS DE RAZONAMIENTO · SIN RESPUESTA · OPUS 5.5 EN \"MAX\"")),
        ("A veinte dólares el millón, ese silencio cuesta unos dos dólares con cincuenta y seis centavos. Cuatro décimas de un Big Mac, a cambio de nada.",
         ("num", "$2.56", "≈ 0.4 BIG MACS · SIN RESPUESTA")),
        ("Y los agentes, inteligencia artificial que trabaja por su cuenta durante horas, pueden consumir millones de tokens en una sola tarea.", ("img", "p23")),
        ("Así que la guerra de precios se está moviendo en silencio, del precio de un token al precio de una tarea terminada.",
         ("words", "DEL TOKEN A LA TAREA")),
    ]),
    dict(id="pays", title="QUIÉN PAGA", beats=[
        ("Cada uno de esos tokens corre en un chip, dentro de un edificio, conectado a una línea eléctrica.", ("img", "p12")),
        ("Este año, el mundo va camino de gastar más de un billón de dólares en centros de datos, según la firma de investigación Dell'Oro.",
         ("num", "$1 BILLÓN+", "INVERSIÓN EN CENTROS DE DATOS · 2026")),
        ("En Big Macs, son más de ciento sesenta mil millones. Veinte por cada persona viva.",
         ("num", "≈ 20", "BIG MACS POR PERSONA EN EL MUNDO · $1 BILLÓN ÷ $6.22 ÷ 8300 MILLONES")),
        ("Y la energía para hacerlos funcionar. La Agencia Internacional de la Energía estima que los centros de datos usaron alrededor del uno y medio por ciento de la electricidad del mundo en 2024, y espera que esa cifra aumente a más del doble para 2030.",
         ("split", ("1.5%", "DE LA ELECTRICIDAD MUNDIAL · 2024"), ("×2+", "PARA 2030 · AIE"))),
        ("Así que la cuenta no desapareció. Se movió: del precio de tu token, a todo lo que se está construyendo detrás.", ("img", "p13")),
        ("Los inversionistas están pagando ahora, apostando a que el uso seguirá creciendo más rápido de lo que caen los precios.", ("img", "p14")),
        ("Y a las empresas que venden las palas les va muy bien. En octubre de 2025, el fabricante de chips Nvidia se convirtió en la primera empresa de la historia en valer cinco billones de dólares.",
         ("num", "$5 BILLONES", "NVIDIA · LA PRIMERA EMPRESA EN LOGRARLO · 29 OCT 2025")),
    ]),
    dict(id="wins", title="QUIÉN GANA", beats=[
        ("En una guerra de precios, el primer ganador es el cliente.", ("img", "p15")),
        ("Cada herramienta construida sobre estos modelos se vuelve más barata de operar, y también los experimentos por los que nadie habría pagado hace un año.",
         ("list", ["UN TUTOR PARA CADA ESTUDIANTE", "UN TRADUCTOR EN CADA TELÉFONO", "UNA SEGUNDA OPINIÓN PARA CADA CONTRATO"])),
        ("Y las empresas que construyen encima. Una aplicación que se cambia a los nuevos modelos puede recortar su mayor costo operativo en una quinta parte, o a la mitad, en una tarde.",
         ("img", "p24")),
        ("Los laboratorios están en una posición más difícil. Cada rebaja los hace más populares, y les deja menos ganancia por cada palabra.", ("img", "p16")),
        ("Su apuesta es que ser el mejor, o el más barato, en el momento justo será suficiente. La apuesta de la Reina Roja es que nadie mantiene la delantera por mucho tiempo.",
         ("words", "NADIE LIDERA POR MUCHO TIEMPO.")),
    ]),
    dict(id="imagine", title="IMAGINA", beats=[
        ("Entonces, imagina que la carrera nunca se detiene. No es un pronóstico. Es una hipótesis.", ("words", "UNA HIPÓTESIS. NO UN PRONÓSTICO.")),
        ("Imagina que el mejor tutor del mundo cuesta menos que un mensaje de texto.", ("img", "p17")),
        ("Después, el mejor programador. El mejor traductor. La mejor segunda opinión, a las tres de la mañana.", ("img", "p18")),
        ("Cuando pensar es casi gratis, ¿qué se vuelve caro?", ("words", "¿QUÉ SE VUELVE CARO?")),
        ("Quizá las cosas que una máquina no te puede enviar. Tu tiempo. Tu atención. Alguien que esté ahí.",
         ("list", ["TU TIEMPO", "TU ATENCIÓN", "ALGUIEN QUE ESTÉ AHÍ"])),
    ]),
    dict(id="close", title="SIGUEN CORRIENDO", beats=[
        ("La versión de esta noche es más sencilla. Busca esa tarea que vienes postergando porque implica horas de lectura, y delégala por unos centavos.",
         ("img", "p19")),
        ("El veintidós de septiembre, un laboratorio le puso a su nuevo modelo un precio una quinta parte más bajo. Noventa minutos después, el otro redujo el suyo a la mitad.",
         ("split", ("−20%", "UNO"), ("−50%", "EL OTRO"))),
        ("Los dos siguen corriendo.", ("img", "p20")),
        ("Y hasta ahora, cada paso que dan hace que pensar te salga más barato.", ("words", "SIGUEN CORRIENDO.")),
    ]),
]
