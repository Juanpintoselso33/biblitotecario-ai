# CIGOB — Complemento a los comentarios del Votómetro
**Fecha:** 12 de abril de 2026  
**Documento base:** 260403 COMENTARIOS VOTOMETRO + 260407 VOTOMETRO ESQUEMA  
**Versión analizada:** `remixed-71df43cf.html` (versión original Redlines, Mar 10 2026)  
**Propósito:** Completar con análisis político y criterios concretos los puntos que quedaron abiertos

---

## 1. VALORACIÓN — Hitos políticos para el gráfico de aprobación

El documento señala que sería bueno vincular la curva de aprobación con hechos relevantes y que "no entiendo por qué están vinculadas las consultoras". Dos aclaraciones:

**Sobre las consultoras vinculadas:** la sección que genera confusión es "Imagen de Dirigentes", donde cada barra muestra la fuente como "Prom. Giacobbe/Opina/Atlas feb.26". Lo que el usuario ve es una mezcla de tres consultoras distintas sin explicación de por qué. La propuesta de sacarlas del label es correcta: mostrar solo "feb. 2026" sin nombrar las consultoras en la visualización.

**Hitos políticos propuestos para anotar en el gráfico de aprobación:**

| Fecha aprox. | Hito | Efecto esperado |
|---|---|---|
| Ago 2024 | Veto presidencial a ley de reforma jubilatoria | Caída: primer punto de inflexión negativo |
| Feb 2025 | Escándalo $LIBRA (criptoestafa vinculada al gobierno) | Caída marcada: mínimo del ICG Di Tella (1.94 pts) |
| Abr 2025 | Acuerdo FMI USD 20.000 M + salida del cepo | Recuperación: mejora de expectativas |
| Oct 2025 | Elecciones legislativas — LLA 40.66% | Alza: pico de aprobación del período |
| Feb 2026 | Inicio caso Adorni (viajes, patrimonio, jubiladas prestamistas) | Caída: segundo punto de inflexión |
| Mar 2026 | Piso histórico de aprobación (~37-38%) | Mínimo: ICC 42.03 pts, peor desde oct-2025 |

**Nota:** el gráfico de saldo neto debería arrancar desde oct-2024 (cuando comienzan los datos de encuestas directas), no desde dic-2023. El tramo anterior son estimaciones reconstruidas.

---

## 2. INTENCIÓN DE VOTO — Consultoras en la tabla

El documento dice "las encuestas o las pondría al final o no las pondría". En el Votómetro original, la sección "Encuestas Agregadas" muestra una tabla con 96 filas, una por encuesta, con columnas: Consultora / Fecha / LLA% / PJ% / Peso (barra visual). Eso es lo que el comentario propone mover o sacar.

**Posición CIGOB:** la tabla de encuestas es la fuente de auditoría del modelo. No publicarla en la pantalla principal está bien, pero debería ser accesible de alguna forma (acordeón, pestaña, link "ver fuentes") para mantener la transparencia del producto.

---

## 3. INTENCIÓN DE VOTO — Esquema de colores

El esquema genera confusión ("¿quiénes son el violeta y el azul?"). La asignación en el original:

| Color | Código | Espacio |
|---|---|---|
| Violeta | #7B3FE4 | LLA (La Libertad Avanza) |
| Azul | #1E88E5 | PJ / Unión por la Patria |
| Amarillo | #FFD600 | PRO — propuesto para remover del gráfico de evolución |
| Naranja | #FF9800 | Provincias Unidas |
| Rojo | #E53935 | UCR / FIT |
| Gris | #78909C | Otros |

**Propuesta:** en el gráfico de evolución temporal mostrar solo LLA (violeta) y PJ (azul). Agregar una línea punteada gris "Resto" que agrupe PRO+UCR+PU para mostrar la polarización sin proliferación de colores.

---

## 4. PRO — Por qué "Bullrich no iría hoy"

El comentario dice "PRO: Bullrich no iría hoy, es violeta solo por hoy" sin desarrollarlo. Contexto político actual:

- Macri activó el armado del PRO en busca de candidato propio (reunión nacional 19-mar-2026). Consigna: "tener candidato presidencial y reelecciones en los distritos propios".
- Bullrich sigue como Ministra de Seguridad de Milei. Lidera el ranking de imagen positiva (40%, Haime mar-2026), por encima del propio Milei (39%).
- Hay negociaciones en curso: oferta de vicepresidencia de parte del oficialismo a Bullrich, a cambio de ceder CABA al candidato de Karina Milei.
- El PRO está en reconstrucción: decenas de dirigentes migraron a LLA; la interna Bullrich-Larreta de 2023 destruyó la línea sucesoria.

**Tres escenarios posibles para el PRO en 2027:**
1. Bullrich va con LLA (candidata vice o presidencial del espacio libertario)
2. PRO tiene candidato propio (Macri, Vidal u otro)
3. PRO no presenta candidato presidencial y acompaña a alguien del centro

**Criterio editorial:** correcto no asignarle candidato al PRO en primera vuelta. Mostrar "PRO" como espacio con porcentaje propio sin nombre. Nota al pie: "espacio en definición de candidatura".

---

## 5. BALLOTAGE — Valores actuales y clasificación de fuerzas

En el Votómetro original los valores de segunda vuelta están hardcodeados a partir de **Trends enero 2026**: **Milei 49%, Kicillof 35%**. Ese es el valor que ve el usuario.

**Clasificación de fuerzas para la segunda vuelta** (según el esquema propuesto en el PPTX de "dividir en más cercanos a LLA y más cercanos a PJ"):

| Espacio | Transferencia a LLA | Transferencia a PJ |
|---|---|---|
| PRO | ~85% | ~5% |
| UCR / Provincias Unidas | ~75% | ~15% |
| FIT-Unidad | ~15% | ~60% |

**Texto sugerido para el módulo condicional:**
> "Si las elecciones derivaran en segunda vuelta, los datos disponibles proyectan: Milei ~49%, Kicillof ~35%, blancos/nulos ~9%. La alta transferencia de votos PRO (~85%) y UCR/PU (~75%) hacia LLA reproduce el patrón del ballotage de 2023."

---

## 6. KICILLOF — Contexto de candidatura

El PPTX propone el label "Milei vs Kisi" en el ballotage. Ese naming tiene respaldo político concreto:

- Kicillof asumió la presidencia del PJ bonaerense en acuerdo con Máximo Kirchner (marzo 2026). El acuerdo incluye un guiño explícito a su candidatura presidencial 2027.
- Milei lo subió al ring discursivo a fines de marzo (caso YPF), acelerando su construcción federal.
- Su movimiento "Derecho al Futuro" se expande a provincias fuera del conurbano.

**Conclusión:** el label "Kicillof" en ballotage está justificado. Texto propuesto: *"Axel Kicillof (PJ — candidatura en construcción)"*.

---

## 7. ALERTA — Datos de ballotage potencialmente desactualizados

**Este es el hallazgo más importante de esta revisión.**

El Votómetro usa Trends enero 2026 como única encuesta de ballotage: Milei 49%, Kicillof 35%. Sin embargo, una encuesta de **Delfos de marzo 2026** muestra el resultado opuesto: **Kicillof 46%, Milei 37.5%** — 13 puntos de diferencia en sentido contrario en el mismo mes.

**Posible explicación:** Trends ene-2026 es pre-Adorni. La encuesta Delfos es post-Adorni y captura el deterioro de imagen del gobierno en la proyección de segunda vuelta.

**Lo que esto significa para el Votómetro:**
- El 49%/35% de ballotage puede estar desactualizado.
- Antes de publicar el módulo condicional de ballotage, Redlines debería conseguir encuestas de segunda vuelta más recientes (post-caso Adorni, post-mar-2026).
- Redlines debería incorporar al menos 2-3 encuestas de ballotage adicionales y recalcular el promedio antes de publicarlo como dato central.

---

## 8. ICG DI TELLA — Qué expresa el gráfico y posición sobre su uso

El comentario en el PPTX (slide 7-8) dice "¿es la aprobación a Milei o a la gestión?" y "me gustaría conversar para entender qué expresa".

**Qué es el ICG:** el Índice de Confianza en el Gobierno (UTDT, Escuela de Gobierno) mide mensualmente qué tan confiada está la sociedad en el gobierno. Es distinto del ICC (Confianza del Consumidor): el ICG es específicamente político, el ICC es económico.

**Qué muestra el gráfico en el Votómetro original:** una correlación entre la serie histórica del ICG (dic-2023 a mar-2026) y la intención de voto LLA. El gráfico tiene eje Y dual y muestra las dos series superpuestas para ilustrar que se mueven en la misma dirección.

**Problema de ese gráfico:** 27 de los 28 puntos de la serie ICG son estimaciones visuales reconstruidas por el equipo, no datos publicados por la UTDT. Solo el punto de feb-2026 (2.38) tiene respaldo estadístico confirmado. El gráfico no lo señala visualmente de forma prominente.

**Estado actual (mar-2026):** ICG = 2.30 pts (-3.5% respecto a febrero). Cayó dos meses consecutivos. Nivel un 0.9% por debajo del ICG de marzo de 2018 (gobierno Macri).

**Posición CIGOB:** el gráfico ICG vs LLA no pertenece a la pantalla principal. Es un análisis estructural interesante para CIGOB internamente, pero requiere demasiada explicación para ser útil al lector general. Si se mantiene, debería estar en la sección metodológica, no como sección independiente del dashboard.

---

## 9. APROBACIÓN — "¿Es a Milei o a la gestión de gobierno?"

Pregunta del PPTX (slide 7). Respuesta: en el Votómetro original la sección no distingue explícitamente entre imagen personal y aprobación de gestión. La sección "Imagen de Dirigentes" muestra a Milei con 45% positiva, que es imagen personal (promedio Opina/Giacobbe/Atlas feb-2026).

Las dos métricas dan números distintos en las mismas encuestas de marzo 2026:

| Métrica | Resultado mar-2026 | Quién la mide |
|---|---|---|
| Imagen personal positiva | ~42-43% | CB Global Data |
| Aprobación de gestión | ~37-38% | UdeSA / Haime / AtlasIntel |

**Propuesta para Redlines:** si se mantiene alguna métrica de aprobación en el header o en una sección, especificar claramente si es imagen personal o aprobación de gestión. La diferencia de 5pp es significativa y puede generar confusión si se citan estas cifras en medios.

---

## 10. ESCENARIOS — Qué existe y qué sacar

El comentario dice "no pondría escenarios". Los escenarios actuales son dos grillas:

**Primera Vuelta (3 escenarios):**
1. "LLA gana sin ballotage" — probabilidad calculada por Monte Carlo
2. "Se va a ballotage" — probabilidad complementaria  
3. "Otro candidato 2do" — fijo en ≈0%

**Ballotage (2 escenarios):**
4. "Milei gana el ballotage" — con probabilidad condicional
5. "Kicillof gana el ballotage" — con probabilidad condicional

**Posición CIGOB:** sacar las dos grillas. Los escenarios de ballotage quedan absorbidos en el módulo condicional. Los de primera vuelta son redundantes si el porcentaje de intención de voto ya incluye un intervalo de confianza. Una sola frase del tipo "en X de cada 10 simulaciones hay segunda vuelta" es suficiente y más clara.

---

## 11. ÚLTIMA ENCUESTA — Por qué confunde

El comentario dice: *"la última encuesta... aparte es de enero 26 cuando se utilizan encuestas de marzo del 26"*. Ahora el problema es claro:

La sección "Última Encuesta por Candidato" muestra **QSocial enero 2026** con Milei en **45%** y Kicillof en 25%. Es la encuesta tipo "candidato" más reciente en la base, pero:
- Tiene sesgo pro-gobierno documentado de ~5pp según track record
- El propio Votómetro advierte en esa sección que "el modelo corrige este dato"
- Hay encuestas más recientes de tipo "espacio" (Giacobbe mar-2026, Trends feb-2026) que muestran 41-43%

El usuario ve "última encuesta: Milei 45%" cuando el modelo en realidad calcula ~41%. La etiqueta "última" genera una expectativa que el modelo luego contradice.

**Propuesta:** eliminar la sección "Última Encuesta destacada" completamente. Si se mantiene, renombrarla como "Encuesta tipo candidato más reciente" y agregar la advertencia de sesgo de forma prominente, no en letra chica.

---

## 12. COMPARATIVA 2023/2025/2027 — Por qué no se entienden los números

El comentario dice "no la entiendo, no la pondría" y también "no me dan tampoco esos números". El gráfico compara tres series:
- 2023: elección presidencial (Milei 29.99%, PJ 27.27%, PRO 16.93%)
- 2025: elecciones legislativas (LLA 40.66%, PJ 31.70%, PRO: 0% — no compitió como espacio nacional unificado)
- 2027: proyección presidencial (~41%)

El PRO aparece con 16.93% en 2023 y 0% en 2025 — lo que parece una desaparición del espacio cuando en realidad es un problema de cómo se codificaron los datos de las legislativas. Eso explica "no me dan esos números": la caída a 0% del PRO en 2025 es un artefacto de la base de datos, no un resultado real.

**Posición CIGOB:** sacar el gráfico de la UI pública. La comparativa mezcla tipos de elección incomparables (presidencial vs. legislativa) y el artefacto del PRO=0% en 2025 genera confusión factual.

---

## 13. MAPA FEDERAL — Respuesta a la pregunta del documento

Sí, es una sola encuesta: **CB Global Data, febrero 2026, 24.690 casos**. Es imagen presidencial georreferenciada, no intención de voto provincial.

**Criterio de activación propuesto:** mostrar el mapa recién cuando haya al menos dos encuestas distintas de intención de voto distrital, con cobertura de al menos 15 de 24 distritos.

---

## 14. GOBERNADORES — Criterio de activación

Activar la sección cuando se cumplan las dos condiciones:
1. Al menos 3 encuestas de imagen / intención de voto por provincia
2. Cobertura de al menos 8 de las 10 provincias más grandes por padrón (Buenos Aires, CABA, Córdoba, Santa Fe, Mendoza, Tucumán, Entre Ríos, Salta, Chaco, Misiones)

---

*Documento producido por CIGOB para complementar los comentarios al Votómetro antes de la presentación a Redlines.*  
*Versión analizada: `remixed-71df43cf.html` (original Redlines, Mar 10 2026 — antes de modificaciones CIGOB)*
