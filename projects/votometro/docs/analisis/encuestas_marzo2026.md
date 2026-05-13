# Encuestas Presidenciales Argentina — Marzo 2026
## Búsqueda para actualización del Votómetro Argentina 2027

**Rango buscado:** 2 al 14 de marzo de 2026
**Fecha de búsqueda:** 14 de marzo de 2026
**Búsquedas realizadas:** Trends, CB Global Data, Synopsis, Poliarquía, Giacobbe, Management & Fit, Analogías, Pulso Research, Atlas Intel/Bloomberg, Opina Argentina

---

## RESULTADO GENERAL

Se encontraron encuestas verificables con números de intención de voto presidencial publicadas en el período buscado (2–14 de marzo de 2026), aunque la mayoría corresponde a trabajo de campo de **febrero de 2026** con publicación en los primeros días de marzo. Se identificaron además algunas encuestas de imagen/gestión de marzo sin datos de intención de voto por espacios.

**Consultoras buscadas sin datos de intención de voto para el período:**
- Synopsis: sin encuesta de intención de voto presidencial encontrada para este período
- Poliarquía: encuesta de diciembre 2025 sobre reelección (41% apoyaría), nada nuevo de marzo 2026
- CB Global Data: encuesta de febrero (10–15/feb) ya circulando en medios en los primeros días de marzo — potencialmente ya en el Votómetro si se cargó con fecha 1/3
- Trends Consultora: encuesta de enero 2026 (5–16/ene) — anterior al corte del Votómetro

---

## TABLA DE ENCUESTAS ENCONTRADAS

| # | Consultora | Campo | Publicación | LLA% | PJ% | PRO% | PU% | FIT% | OTROS% | NsNc/Ind% | n= | Tipo | Calidad |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Analogías | 20–23 feb 2026 | ~1 mar 2026 | 31.7 | 27.9 | — | — | 4.6 | 12.3 | 23.6 | 2691 | espacio | A |
| 2 | Giacobbe | 23–27 feb 2026 | 11 mar 2026 | — | — | — | — | — | — | — | 2500 | candidato* | A |
| 3 | Management & Fit | 9–24 feb 2026 | 4 mar 2026 | — | — | — | — | — | — | — | 2200 | imagen** | A |
| 4 | Pulso Research | 3–9 mar 2026 | 12 mar 2026 | — | — | — | — | — | — | — | n/d | gestión*** | — |
| 5 | Atlas Intel + Bloomberg | 19–24 feb 2026 | ~1–3 mar 2026 | — | — | — | — | — | — | — | 4761 | gestión**** | A |

\* Giacobbe (11/3/2026): mide imagen de dirigentes y preferencia de candidatos por menciones espontáneas (qualitativi), NO da % de intención de voto por espacio. Patricia Bullrich superó en imagen positiva a Milei. No hay número de intención de voto comparable al formato `encuestasRaw`.

\** Management & Fit (4/3/2026): mide imagen de 15 dirigentes. Milei: 39.8% positiva / 46.4% negativa. No reporta intención de voto por espacio en los datos disponibles públicamente.

\*** Pulso Research "Brújula Social" marzo 2026 (campo 3–9 mar, pub. ~12 mar): mide aprobación de gestión (cayó a 37.2%, piso histórico) y percepción de responsabilidad económica. No se encontraron números de intención de voto por espacio en las fuentes disponibles.

\**** Atlas Intel + Bloomberg "Latam Pulse" febrero 2026 (campo 19–24 feb): mide imagen de gestión, optimismo económico. No reporta intención de voto por espacio político en los datos accesibles.

---

## ÚNICA ENCUESTA CON DATOS COMPLETOS DE INTENCIÓN DE VOTO (espacio)

### Analogías — Febrero 2026

- **Consultora:** Analogías (trabaja para el kirchnerismo)
- **Campo:** 20 al 23 de febrero de 2026
- **Publicación en medios:** Circa 1 de marzo 2026 (circuló ampliamente en la primera semana de marzo)
- **Muestra:** 2.691 casos nacionales, 16–74 años
- **Margen de error:** ±2%
- **Tipo:** espacio (mide espacios políticos, no candidatos nominales)
- **Calidad:** A (n>1000, muestra grande)
- **Sesgo declarado:** consultora cercana al kirchnerismo

**Datos:**

| Espacio | % |
|---|---|
| LLA (Milei) | 31.7% |
| Peronismo (PJ/K) | 27.9% |
| Otras fuerzas | 12.3% |
| Izquierda (FIT) | 4.6% |
| No sabe / Indecisos | 23.6% |

**Observación crítica:** Los datos de Analogías ya podrían estar cargados en el Votómetro con fecha 1/3/2026 (fecha del corte declarado). Verificar si ya existe entrada de Analogías febrero 2026 antes de agregar.

**Nota sobre PRO:** Analogías no reporta al PRO como espacio separado — lo incluye en "Otras fuerzas" (12.3%) junto a radicales, provincias unidas y otros. No es posible desagregar.

---

## ENCUESTA ADICIONAL DETECTADA: El Observador (Instagram, 12 mar 2026)

La cuenta `@elobservadorar` publicó el 12 de marzo de 2026:
> "Encuesta: Javier Milei ganaría en primera vuelta ante sus rivales de 2023"

473 likes, 130 comentarios. **No se pudo acceder al contenido completo** — el post es de Instagram y la fuente no está disponible en texto abierto. Sin datos numéricos verificables.

---

## CÓDIGO JAVASCRIPT PARA `encuestasRaw`

Solo hay UNA encuesta con datos suficientes para agregar al array. Verificar primero que no esté ya cargada:

```js
// ANALOGÍAS — campo: 20-23 feb 2026 — publicada ~1 mar 2026
// ADVERTENCIA: verificar que no exista ya en encuestasRaw con fecha 2026-03-01 o 2026-02-23
// Nota: PRO no reportado separado — incluido en OTROS
// Nota: PU (Provincias Unidas/Peronismo no K) no reportado separado — incluido en OTROS
// OTROS 12.3 incluye PRO + PU + UCR + resto
// NsNc 23.6 excluido del cálculo de voto válido — se mantiene como campo no estándar

{ fecha:'2026-03-01', consultora:'Analogías', LLA:31.7, PJ:27.9, PRO:0.0, PU:0.0, FIT:4.6, OTROS:12.3, muestra:2691, tipo:'espacio', calidad:'A', url:'https://www.lavoz.com.ar/politica/encuestas-milei-cristina-kirchnerismo_0_TUCmDrAMf5.html' },
```

> **ALERTA:** Este registro suma solo 76.5% (31.7+27.9+4.6+12.3). El 23.6% restante corresponde a indecisos (NsNc). Según la metodología del Votómetro, verificar si el array `encuestasRaw` trabaja con porcentajes incluyendo indecisos o solo sobre voto válido. Si trabaja sobre voto válido, habría que reproporcionar:
> - LLA: 41.4%, PJ: 36.5%, FIT: 6.0%, OTROS: 16.1% (sobre los que definen voto)

---

## RESUMEN DE BÚSQUEDAS POR CONSULTORA

| Consultora | ¿Encontrada? | Período de campo | ¿Datos de intención de voto? | Observación |
|---|---|---|---|---|
| Trends | Sí | 5–16 ene 2026 | Sí (LLA 43%, PJ 32%) | Anterior al corte; ya en Votómetro |
| CB Global Data | Sí | 10–15 feb 2026 | Sí (candidatos: Milei 35.7%, Kicillof 22.5%, Villarruel 5.2%) | Probablemente ya cargada en Votómetro |
| Synopsis | No encontrada | — | — | Sin publicaciones identificadas para feb–mar 2026 |
| Poliarquía | Parcial | Dic 2025 | No (solo imagen líderes / reelección) | Sin nueva encuesta en el período |
| Giacobbe | Sí | 23–27 feb 2026 | No (cualitativo / imagen) | Publicada 11/3/2026; no da % por espacio |
| Management & Fit | Sí | 9–24 feb 2026 | No (solo imagen 15 dirigentes) | Publicada 4/3/2026; no da % de intención de voto |
| Analogías | Sí | 20–23 feb 2026 | SÍ (ver tabla arriba) | Publicada ~1/3/2026; única con datos completos |
| Pulso Research | Sí | 3–9 mar 2026 | No (solo aprobación/gestión) | Publicada ~12/3/2026; no da % por espacio |
| Atlas Intel + Bloomberg | Sí | 19–24 feb 2026 | No (imagen de gestión) | Publicada ~1–3/3/2026; no da % por espacio |
| Opina Argentina | Sí | ~ene 2026 | Sí (LLA 44%, PJ 35%) | Período de campo anterior al corte |

---

## NOTAS SOBRE CONFIABILIDAD DE FUENTES

1. **Analogías (lavoz.com.ar, eldestapeweb.com, cholilaonline.ar):** Datos consistentes entre múltiples fuentes. Confiable. Sesgo declarado: trabaja para el kirchnerismo — sus datos tienden a mostrar LLA más bajo y PJ más alto que otras consultoras. Históricamente subestima a LLA vs. resultados reales.

2. **Giacobbe (iProfesional, perfil.com):** Fuentes sólidas. El dato reportado es cualitativo — no apto para `encuestasRaw`. La encuesta midió imagen y menciones espontáneas de candidatos preferidos. Sin número de intención de voto comparable.

3. **Management & Fit (viapais.com.ar, elobservador.com.uy):** Fuentes sólidas. La publicación del 4/3/2026 es de imagen de dirigentes. En encuestas anteriores sí midió intención de voto, pero la de febrero 2026 no lo hizo de forma pública.

4. **Pulso Research (eldestapeweb.com, perfil.com "Brújula Social"):** El informe de marzo (campo 3–9/3) mide aprobación de gestión, no intención de voto por espacio. Dato de aprobación: 37.2% (piso histórico), desaprobación: 54.8%.

5. **Atlas Intel + Bloomberg (diagonales.com, perfil.com):** Datos de gestión e imagen. No publica intención de voto por espacio en el formato requerido para el Votómetro.

6. **El Observador (Instagram @elobservadorar, 12/3/2026):** Post detectado con título "Milei ganaría en primera vuelta". Sin acceso al contenido numérico completo. No se puede cargar sin verificar los datos originales.

---

## CONTEXTO GENERAL DEL PERÍODO (2–14 de marzo de 2026)

El período está dominado por encuestas de **imagen y gestión** con desgaste del gobierno, pero escasas encuestas de intención de voto por espacio político. El patrón general de todos los sondeos:

- **LLA:** ~31–44% según consultora y metodología (rango amplio por diferente tratamiento de indecisos)
- **PJ/K:** ~27–35%
- **Tendencia:** desgaste de imagen de Milei, pero oposición sin candidato consolidado
- **Indecisos/NsNc:** entre 6% y 23% según encuesta — variable crítica

---

## CONCLUSIÓN PARA EL VOTÓMETRO

**Encuestas nuevas aptas para cargar en `encuestasRaw`:** 1 (Analogías, con cautelas)

**Recomendación:**
1. Verificar si Analogías feb 2026 ya está cargada (campo 20–23/feb, publicada ~1/3)
2. Resolver el tratamiento de indecisos antes de cargar (23.6% de NsNc es inusualmente alto)
3. Pendiente: conseguir datos completos del post de El Observador del 12/3 — podría ser una encuesta nueva
4. Synopsis y Poliarquía no publicaron intención de voto presidencial en el período buscado
5. CB Global Data de febrero (35.7% Milei candidato, 22.5% Kicillof) puede ya estar en el Votómetro

**Estado del Votómetro post-búsqueda:** No hay encuestas nuevas significativas entre el 2 y 14 de marzo que modifiquen materialmente el mapa electoral. El escenario sigue igual al de fines de febrero.
