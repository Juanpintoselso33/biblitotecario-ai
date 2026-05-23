# Pestaña Macroeconomía — análisis matusiano del Cinturón Económico

> Análisis del Cinturón Económico del dashboard `https://cigob.k1t.eu/index.html` desde la planificación estratégica situacional (PES). Marco de referencia: `_brief_matus.md` (Matus 1997, *Los Tres Cinturones del Gobierno*; Matus tardío, Teoría del Juego Social).

Score declarado por el dashboard: **+57 → cinturón holgado**. La tesis de este archivo es que ese número es engañoso: la pestaña mide bien la dimensión financiera de corto plazo del cinturón económico, pero subindexa la dimensión real (actividad, empleo, deuda, expectativas), y por eso queda expuesta al barbarismo tecnocrático que el propio Matus diagnostica como la patología más frecuente del análisis macro.

---

## A. Indicadores presentes

| Indicador | Valor (mar–may 2026) | Fuente probable | Naturaleza | Fidelidad matusiana |
|---|---|---|---|---|
| Resultado fiscal primario | +297 B$ mes (positivo) | MECON / Tesoro — Informe Mensual Ingresos y Gastos | Flujo fiscal | Alta. Núcleo del equilibrio macro de Matus. |
| Brecha cambiaria oficial vs paralelo | 5,6% (baja) | BCRA + cotización informal | Precio / señal de expectativas | Media. Mide más expectativa que economía real. |
| ITCRM (tipo de cambio real multilateral) | 94,5 (apreciado) | BCRA — Serie ITCRM base 2010=100 | Precio relativo (stock comercial) | Alta. Captura competitividad estructural. |
| Saldo comercial | USD +788 M (superávit mes) | INDEC — Intercambio Comercial Argentino (ICA) | Flujo externo | Alta. Equilibrio externo, vértice clásico de Matus. |
| EMBI+ Argentina | 539 pb | JP Morgan / Rava / Ámbito | Precio financiero | Media. Mide percepción de acreedores externos. |
| IPC | 3,4% mes / 32,6% i.a. | INDEC — IPC Nacional | Precio | Alta. Variable nominal central. |
| Reservas BCRA | USD 41,1 mM | BCRA — Reservas Internacionales brutas | Stock externo | Alta. Stock disponible para shocks. |

Observación 1: la mezcla **stocks / flujos / precios** está sesgada hacia precios y stocks financieros. De los 7 indicadores, **3 son precios** (brecha, ITCRM, IPC), **2 son stocks financieros** (reservas, EMBI), **2 son flujos** (fiscal y comercial). No hay ningún indicador de **stock de deuda**, ningún indicador de **cantidad real producida**, ningún indicador de **mercado de trabajo**.

Observación 2: el score +57 surge de "más positivos que negativos". Pero "positivo" se asigna a un superávit fiscal de un mes y a una brecha cambiaria contenida, ignorando que ambos pueden ser síntoma de una contracción brutal de demanda más que de equilibrio sostenible. Matus diría: el indicador no captura la **velocidad ni la dirección de la trayectoria** (brief, sección 6).

---

## B. Indicadores faltantes

Priorizados por relevancia matusiana y costo de incorporación.

| # | Indicador propuesto | Por qué importa para Matus | Fuente | Frecuencia | Costo |
|---|---|---|---|---|---|
| 1 | **EMAE (Estimador Mensual de Actividad Económica)** | Variable de actividad real. Sin ella el dashboard no puede distinguir "ajuste exitoso" de "recesión inducida". Núcleo del juego económico de Matus. | INDEC — EMAE | Mensual | Bajo |
| 2 | **Tasa de desempleo + subocupación** | Mercado de trabajo es el puente entre cinturón económico y cinturón de vida cotidiana. Matus lo trata como variable de gobernabilidad de primer orden. | INDEC — EPH | Trimestral | Bajo |
| 3 | **Deuda pública bruta / PBI (y deuda en moneda extranjera / reservas)** | Stock de obligaciones. Sin esto, el resultado fiscal mensual se lee fuera de contexto. Matus distingue equilibrio coyuntural de solvencia estructural. | Secretaría de Finanzas — Boletín Trimestral | Trimestral | Bajo |
| 4 | **Expectativas de inflación REM (12 meses adelante)** | Variable forward-looking. Permite leer si la baja del IPC es transitoria o desinflación creíble. Matus: el actor que solo mira el pasado está ciego al futuro. | BCRA — REM | Mensual | Bajo |
| 5 | **Recaudación tributaria real (deflactada por IPC, var. i.a.)** | Indicador adelantado de actividad y consumo. Más oportuno que EMAE. Cruza fiscal con real. | AFIP — Informe Mensual | Mensual | Bajo |
| 6 | **Crédito al sector privado en términos reales** | Mide si el sistema financiero está funcionando como motor o como freno. Variable de transmisión del juego económico. | BCRA — Informe Monetario Mensual | Mensual | Bajo |
| 7 | **Utilización de la capacidad instalada industrial** | Complementa EMAE con foco productivo. Detecta cuello de botella o subutilización. | INDEC — UCI | Mensual | Bajo |
| 8 | **Pobreza por ingresos (SIPA + canasta básica)** | Aunque va parcialmente en Vida Cotidiana, una proxy mensual (variación de canasta básica vs salario medio) corresponde al cinturón económico. | INDEC — IPCBA | Mensual / semestral | Medio |

Las **prioridades 1, 2, 3 y 4** son las que cambian sustantivamente el diagnóstico: sin ellas, la pestaña hoy podría dar +57 (holgado) en una economía que estuviera cayendo 4% i.a., con desempleo subiendo y deuda creciendo en términos reales. Eso es justamente el escenario que Matus llama "trampa tecnocrática": el tablero verde mientras la calle entra en crisis.

---

## C. Indicadores redundantes o débiles

| Indicador | Diagnóstico | Recomendación |
|---|---|---|
| **Brecha cambiaria 5,6%** | Con cepo flexibilizado o levantado, la brecha pierde poder informativo. Mide más arbitraje técnico que tensión cambiaria estructural. | Refundirla con ITCRM o reemplazarla por **prima de riesgo cambiario en futuros** (ROFEX vs spot). |
| **EMBI+ 539 pb** | Indicador útil, pero correlacionado con expectativas que también capta el REM. Solapa señal con brecha cambiaria. | Mantener, pero acompañar con **paridad de bonos en USD (Globales)**, que es más sensible y diaria. |
| **Saldo comercial mensual** | Volátil mes a mes (estacionalidad sojera, energía). Un mes positivo no informa. | Reemplazar por **saldo comercial acumulado 12 meses móviles**, que captura tendencia. |
| **Resultado fiscal primario mensual** | Mismo problema de volatilidad. Hay aguinaldos, pagos extraordinarios, armado contable. | Mostrar **acumulado del año vs meta** y **resultado financiero** (incluye intereses), no solo primario. El primario sin intereses oculta el peso de la deuda. |

Síntesis: cuatro de los siete indicadores actuales están subóptimamente especificados. No hace falta sacarlos; hace falta presentarlos en su **forma matusianamente útil**: tendencia, dirección, contraste con meta. El score binario positivo/negativo agrava el problema.

---

## D. Lectura matusiana del cinturón

### Estado del cinturón económico

Si tomamos los siete indicadores tal como están: superávit fiscal, brecha contenida, IPC desacelerando, reservas creciendo, comercio positivo. El dashboard los lee como **holgado +57**. Una lectura matusiana — incluso con la información incompleta de la pestaña — daría algo distinto:

- ITCRM en 94,5 indica **apreciación cambiaria** acumulada. Eso erosiona competitividad y, vía cuenta corriente, anticipa tensión externa futura.
- EMBI+ en 539 pb es **alto** en términos absolutos: el mercado todavía exige prima de riesgo significativa pese a los buenos números fiscales.
- IPC mensual 3,4% anualizado es ~50%; el i.a. 32,6% sigue siendo de los más altos del mundo.
- Sin EMAE ni desempleo, no se puede saber si el ajuste fiscal está montado sobre crecimiento o sobre recesión.

Diagnóstico provisional: el cinturón **no está holgado**, está en una **estabilización financiera frágil** con apreciación cambiaria, riesgo país elevado e inflación todavía alta. La regla matusiana de los tres cinturones (brief, sección 2) lo confirma: la pestaña Vida Cotidiana muestra −20 (tensionado), salario real cayendo y actividad PyME −1,8% i.a. Eso es **exactamente lo que falta en esta pestaña** y lo que cambiaría el color del semáforo.

### Barbarismo dominante: el tecnocrático

El brief (sección 5) define el **barbarismo tecnocrático** como "gobernar mirando solo indicadores económicos, sin lectura política ni de vida cotidiana — el cinturón político se rompe sin aviso". La pestaña Macroeconomía, vista en aislamiento, **es el caldo de cultivo perfecto** de ese barbarismo:

- Selecciona variables financieras de corto plazo (precio del dólar, EMBI, brecha) por encima de variables de actividad real.
- Aplica un score positivo/negativo que premia el síntoma de éxito financiero (superávit, baja brecha) sin pesarlo contra costo social.
- No incluye un solo indicador de empleo, salarios reales, deuda o pobreza dentro del propio cinturón.
- No mide expectativas (REM), por lo que la lectura es retrospectiva.

Un usuario que mire **solo esta pestaña** concluye que el gobierno tiene la macro resuelta. Cualquier responsable político con esa información tomaría decisiones equivocadas, porque la economía real no aparece. Matus llamaría a esto "gobernar con un tablero cuyos sensores apuntan al cielo y no a la ruta".

### Mezcla stocks/flujos/precios

Como se mostró en A: 3 precios + 2 stocks financieros + 2 flujos = **0 cantidades reales, 0 mercado de trabajo, 0 stock de deuda**. La mezcla está desbalanceada a favor de la dimensión nominal y financiera. Matus exigiría al menos uno de cada categoría real: cantidad producida (EMAE/UCI), empleo (EPH), pasivo estructural (deuda/PBI).

### Recomendación de rediseño

Una intervención mínima de alto retorno:

1. **Sumar 4 indicadores de costo bajo y frecuencia mensual**: EMAE (INDEC), recaudación real (AFIP), expectativas de inflación REM (BCRA), deuda bruta / PBI (Secretaría de Finanzas, trimestral). Esto cierra la dimensión real y la dimensión forward-looking sin inflar la pestaña.
2. **Reformular dos indicadores existentes**: saldo comercial → 12 meses móviles; resultado fiscal → acumulado del año + financiero (con intereses).
3. **Sustituir el score binario por un score de tres dimensiones**: nivel, dirección (mejora/empeora), velocidad. Un cinturón que mejora en nivel pero empeora en velocidad debe encender alerta amarilla, no quedar en verde.
4. **Mostrar siempre, en el encabezado de la pestaña, el cruce con Vida Cotidiana**: salario real y empleo. Eso es el cortafuegos contra el barbarismo tecnocrático: imposible mirar la macro sin ver simultáneamente cómo aterriza en la calle.

Con esos cambios, la lectura del cinturón económico pasaría de "holgado +57" — diagnóstico falso — a algo más matusiano: estabilización financiera real, recesión real, deuda monitoreada, expectativas en proceso de anclaje. Esa es la información que un gobernante necesita para no caer en la trampa de los tres cinturones apretados al mismo tiempo (brief, sección 2).
