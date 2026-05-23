# Proyecto País: Indicadores en trabajo — Estado de extracción

**Fecha:** 23 de mayo de 2026
**Versión:** actualización del documento base "Proyecto País: Indicadores en trabajo" (260520).

Este documento mantiene la misma estructura del documento base y actualiza, para cada indicador propuesto, su estado actual de extracción: si ya está implementado, qué fuente se usa, cuándo se ejecutó por última vez, y en qué casos no se pudo automatizar y por qué.

**Convenciones:**
- ✅ AUTO — extracción automática operativa
- 📋 MANUAL — carga manual periódica desde `data/*/manuales.json`
- ❌ BLOQUEADO — fuente no accesible / sin proxy viable (detalle al pie)
- 🔬 PROPUESTO — no implementado, factible con fuentes identificadas

---

## 1. Cinturón de la Vida Cotidiana

Este cinturón cuenta con un alto grado de avance, con la mayoría de sus métricas ya integradas en el orquestador automático (`scripts/vida_cotidiana/main.py`, 8 fuentes activas), utilizando proxies metodológicos en los casos donde la fuente original no era viable. **Cobertura: 14/14 conceptos del 260520 cubiertos + 1 manual estructural.**

### Indicadores Seleccionados / Activos

| Indicador | Fuente / Proxy Utilizado | Frecuencia | Estado | Último dato |
|---|---|---|---|---|
| Brecha Salario Real vs. CBT | datos.gob.ar (RIPTE + CBT) | Mensual | ✅ AUTO | 3.82 canastas (mar-2026) |
| IPC-Alimentos | datos.gob.ar (serie 146.3) | Mensual | ✅ AUTO | +3.35% m/m (mar-2026) |
| Endeudamiento Familiar | BCRA API v4.0 (tarjeta + personales + hipotecarios + consumo) | Diaria | ✅ AUTO | $129.334M (may-2026) |
| Peso de Tarifas | IPC-Vivienda + IPC-Regulados (proxy INDEC) | Mensual | ✅ AUTO | +3.71% / +5.08% (mar-2026) |
| Consumo de Carne Vacuna | CICCRA (Scraping PDF) | Mensual | ✅ AUTO | abr-2026 |
| Informalidad Laboral | datos.gob.ar (asalariados sin descuento) | Anual | ✅ AUTO | 36.75% (ene-2026) |
| Mortalidad de PyMEs | IPI Manufacturero + EMAE (proxy INDEC) | Mensual | ✅ AUTO | feb-2026 |
| Despacho de Cemento e Hierro | ISAC + Acero crudo (proxy INDEC) | Mensual | ✅ AUTO | 143.5 / 731.6 (feb-2026) |
| Pluriempleo | Subocupación demandante EPH (proxy) | Trimestral | ✅ AUTO | 7.8% (oct-2025) |
| Espera en Salud Pública | DEIS / API CKAN (proxy débil — solo lista datasets) | Variable | ⚠ AUTO parcial | 3 datasets |
| Inseguridad Urbana | SNIC + CABA datos abiertos | Anual | ✅ AUTO | 2.501.057 hechos (2024) |
| ICC Confianza del Consumidor | UTDT (scraping XLS) | Mensual | ✅ AUTO | 40.5 (may-2026) |
| Sentimiento Digital | Google Trends (pytrends — 4 términos) | Tiempo real | ✅ AUTO | inflación 1.8, precios 9.2 |
| Apatía Electoral | Votómetro CIGOB (vive en cinturón POLÍTICO como `votometro_ventaja_lla`) | Continua | ✅ AUTO | +13.3pp LLA−PJ (mar-2026) |

**Bonus extraído pero no en el 260520:** Patentamiento de motos (CAFAM) como proxy adicional de consumo discrecional — 51.124 unidades may-2026.

### Indicadores Propuestos / Revisión Manual

| Indicador | Estado / Observación |
|---|---|
| Deserción Escolar | 📋 MANUAL — no automatizable por rezago anual del Ministerio de Educación. Carga manual anual recomendada. |
| Ingreso Disponible Real (Empiria) | 🔬 PROPUESTO PRIORITARIO — IS_registrado / IPC_vivienda. Cálculo verificado: ene-2026 vs ene-2025 = **−8.0% i.a.** (salario perdió contra gastos fijos pese a desinflación general). Implementable como `collectors/ingreso_disponible.py`. |

### Nota técnica

El script puente `scripts/vida_cotidiana.py` (que integra con el orquestador global del informe) solo expone 3 indicadores legacy (`ipc_total + desocupacion + icc_utdt`). El dashboard agregado debería migrarse a leer del output `scripts/vida_cotidiana/data/vida_cotidiana_*.json` para tener la cobertura completa de los 14 indicadores.

---

## 2. Cinturón de la Macroeconomía

Posee un núcleo de indicadores financieros y de precios ya codificados — **11/11 del 260520 implementados como AUTO**. La batería de indicadores propuestos desde la visión estratégica situacional sigue en diseño.

**Score actual (23-may-2026):** 2.1 — estable. 11/11 frescos en última ejecución.

### Indicadores Seleccionados / Activos (Scripting)

> El 260520 anotó "son 19 bajamos ¿??" — la lista codificada quedó en **11**, los 8 restantes se reservaron como propuestos (ver tabla siguiente).

| Indicador | Qué Mide | Fuente | Estado | Último valor |
|---|---|---|---|---|
| IPC Total | Inflación mensual nacional | INDEC (serie 148.3) | ✅ AUTO | 3.38% m/m |
| Reservas BCRA | Reservas internacionales brutas | BCRA API v4.0 var 1 | ✅ AUTO | 46.585 M USD |
| Tasa BADLAR | Costo del dinero para depósitos mayoristas | BCRA API v4.0 var 7 | ✅ AUTO | 22.0% anual |
| EMAE (Var. Interanual) | Actividad económica general adelantada | INDEC (serie 143.3) | ✅ AUTO | +1.88% i.a. |
| Saldo Comercial (12 meses) | Balance exportaciones vs importaciones acumulado | INDEC (serie 164.3) | ✅ AUTO | +17.125 M USD |
| Recaudación Tributaria | Variación mensual de la recaudación total | INDEC/AFIP (serie 172.3) | ✅ AUTO | −0.99% var m |
| TCRM | Tipo de cambio real multilateral | INDEC (serie 116.3) | ✅ AUTO | 79.77 (base 2010=100) |
| Expectativas Inflación (REM) | Proyección del mercado a 12 meses | BCRA API v4.0 var 29 | ✅ AUTO | 24.2% anual |
| Préstamos Privados | Variación del crédito bancario al sector privado | BCRA API v4.0 var 26 | ✅ AUTO | +2.13% var m |
| Base Monetaria | Variación de billetes y reservas bancarias | BCRA API v4.0 var 15 | ✅ AUTO | +0.7% var m |
| Tipo de Cambio Mayorista | Variación del precio oficial de referencia | BCRA API v4.0 var 5 | ✅ AUTO | −0.27% var m |

### Indicadores Propuestos / En Diseño (Perspectiva Matusiana)

| Indicador | Justificación Estratégica | Estado | Fuente plausible |
|---|---|---|---|
| Resultado Fiscal Financiero | Incluye intereses de deuda; supera la visión sólo primaria. | 🔬 PROPUESTO | Hacienda — informe mensual ejecución presupuestaria |
| Riesgo País (EMBI+) | Mide el costo de oportunidad y percepción externa. | 🔬 PROPUESTO | JPMorgan EMBI+ vía scraping AmbitoFinanciero o API datos.gob.ar |
| Deuda Pública Bruta / PBI | Indicador de solvencia estructural a largo plazo. | 🔬 PROPUESTO | Hacienda — anual |
| Tasa de Desempleo / Subocupación | Puente directo con la gobernabilidad y la vida cotidiana. | ✅ YA EXTRAÍDO | INDEC EPH (ya está en cinturón Vida Cotidiana — falta exponerlo en Macro) |
| Utilización Capacidad Instalada | Complementa al EMAE detectando cuellos de botella industriales. | 🔬 PROPUESTO | INDEC mensual (serie UCI) |
| Pobreza por Ingresos (Proxy) | Variación de canasta básica versus salario medio. | ✅ YA EXTRAÍDO | CBT, CBA y RIPTE ya extraídos en Vida Cotidiana — calcular ratio |
| Brecha Cambiaria | Termómetro de desconfianza (sujeto a revisión por flexibilización de cepo). | ✅ YA EXTRAÍDO | dolarapi.com — ya usado en `cepo_mulc` (Gestión) como brecha CCL/oficial |
| Formación Bruta de Capital Fijo | Inversión real como soporte físico del crecimiento. | 🔬 PROPUESTO | INDEC — Cuentas Nacionales trimestrales |

**Observación:** 3 de los 8 propuestos ya están parcialmente extraídos por otros cinturones (Desempleo, Pobreza Proxy, Brecha Cambiaria) — basta con exponerlos en Macro.

---

## 3. Cinturón de la Política

El 260520 señaló que las métricas estaban "íntegramente en fase de propuesta". **Esto cambió: 7 de 10 indicadores propuestos están AUTO + 2 manual + 1 sin implementar.** Score actual: **4.7 en tensión**.

### Indicadores Propuestos — estado real

| Indicador propuesto en 260520 | Implementación técnica | Descripción / Objetivo | Estado | Valor (may-2026) |
|---|---|---|---|---|
| Tasa de Eficacia Parlamentaria (TEP) | `eficacia_legislativa` | Relación entre proyectos enviados al Congreso y leyes aprobadas. | ✅ AUTO (datos.hcdn.gob.ar CKAN) | 4.8% (1/21 proyectos PE en 12m) |
| Ratio DNU | `ratio_dnu` | Proporción de decretos de urgencia sobre leyes sancionadas. | ✅ AUTO (InfoLeg sesión POST) | 3.14 (22 DNU / 7 leyes período 144) |
| Índice de Armonía Federal (IAF) | `iaf_transferencias` | Cruce de transferencias automáticas/discrecionales con apoyo de gobernadores. | ✅ AUTO (RON Hacienda CSV) | +1.8% real i.a. |
| Tasa de Judicialización de la Gestión | — | Medidas cautelares activas contra reformas gubernamentales clave. | ❌ NO IMPLEMENTADO | sin fuente estructurada CSJN |
| Control de Agenda (Iniciativa) | — | Vida media de crisis o escándalos de gobierno medida vía Google Trends. | 🔬 PROPUESTO | factible con `pytrends` (ya usado en Vida Cotidiana) |
| Índice de Tensión Social (ITS) | `movilizacion_cepa` | Frecuencia de paros, movilizaciones y cortes. | ✅ AUTO (scraping centrocepa.com.ar) | 46.0 (cache — 404 hoy) |
| Tasa de Compromiso RIGI/RIMI | — | Nivel de adhesiones provinciales y sindicales a los regímenes. | 🔬 PROPUESTO | requiere parseo de declaraciones provinciales — manual |
| Impacto del Clima Internacional | — | Efecto de procesos electorales en la región (EE.UU., Brasil, Colombia). | 🔬 PROPUESTO | construible con calendario electoral + spread soberano regional |
| Tensión Estructural Discursiva | — | Medición del conflicto conversacional entre bloques políticos. | 🔬 PROPUESTO | requiere NLP sobre Twitter/X de diputados — fuera de scope inmediato |
| Independencia del Banco Central | — | Autonomía institucional como factor de sostenibilidad política. | ❌ NO IMPLEMENTABLE | métrica cualitativa sin proxy objetivo |

### Indicadores adicionales implementados (no estaban en el 260520)

| Indicador | Descripción | Estado | Valor |
|---|---|---|---|
| `votometro_ventaja_lla` | Brecha ponderada LLA−PJ en intención de voto | ✅ AUTO (parse Votómetro CIGOB) | +13.3pp |
| `veto_quorum` | % sesiones frustradas por falta de quórum | ✅ AUTO (CKAN HCDN `REUNION_TIPO~Fracasada`) | 0.0% (período 144) |
| `comisiones_caidas` | % proyectos con dictamen OD que no llegan al recinto | ✅ AUTO (CKAN HCDN) | 99.6% (alto estructural) |
| `cohesion_bloque` | % diputados LLA alineados con la posición oficial | 📋 MANUAL | 78% placeholder |
| `gobernadores_alineamiento` | % gobernadores alineados con política nacional | 📋 MANUAL | 55% placeholder |

### Por qué los 2 manuales no se pudieron automatizar

- **`cohesion_bloque`**: las votaciones nominales en CKAN HCDN están **congeladas en período 137 (2019)**. La composición actual del bloque LLA (95 diputados) está disponible pero **sin `PERSONA_ID` que mapee a los votos históricos**. Requeriría headless browser sobre `hcdn.gob.ar/votaciones` o acuerdo con HCDN para fuente alternativa.
- **`gobernadores_alineamiento`**: sin fuente estructurada pública. Podría construirse con NLP sobre declaraciones (La Nación Data, Infobae) pero requiere un proyecto separado.

---

## 4. Cinturón de Gestión

Definido recientemente como un tablero para medir el cumplimiento estricto de las reformas del Estado y compromisos de la APN. **Cobertura: 12/12 indicadores del 260520. Score actual: 5.9 en tensión. Auto frescos: 6/6.**

### Indicadores Propuestos — estado real

| Eje / Desafío Enunciado | Indicador de Avance Sugerido (260520) | Implementación | Estado | Avance (may-2026) |
|---|---|---|---|---|
| Desmantelamiento del Cepo | Volumen diario de compra/venta de divisas en MULC. | `cepo_mulc` — brecha **CCL**/oficial (dolarapi.com) | ✅ AUTO | 78.4% (brecha 4.32%) |
| Privatizaciones | Transferencia efectiva de acciones y pliegos publicados. | `privatizaciones` — manuales.json | ❌ BLOQUEADO | 15% (manual) |
| Concesiones de Infraestructura | Km concesionados (corredores viales) y servicios públicos transferidos. | `concesiones_infraestructura` — manuales.json | 📋 MANUAL | 35% |
| Reducción del Estado | Cierre de fondos fiduciarios y variación neta de la dotación de empleo público. | `reduccion_estado` — datos.gob.ar (puestos trabajo público) | ✅ AUTO | 2.7% (var −0.8%) |
| Reestructuración de Organismos | Entidades disueltas, fusionadas o centralizadas. | `reestructuracion_organismos` — InfoLeg `texto="disolucion"` desde dic-2023 | ✅ AUTO | 40% (18 normas) |
| Inversiones (RIGI / Super RIGI) | Proyectos presentados, aprobados y montos proyectados. | `rigi_inversiones` — InfoLeg `tipo=3 texto="VPU"` desde jul-2024 | ✅ AUTO ⭐ | 28% (28 resoluciones VPU) |
| Desregulación Normativa (índice de libertad económica) | Artículos y normas eliminadas o modificadas. | `desregulacion_normativa` — InfoLeg `texto="deroga"` desde dic-2023 | ✅ AUTO | 55% (55 normas) |
| Apertura Comercial | Eliminación de aranceles y trabas no arancelarias. | `apertura_comercial` — datos.gob.ar (importaciones totales, proxy) | ✅ AUTO | 100% (+42.4% i.a.) |
| Asistencia Directa | Porcentaje de beneficiarios sociales sin intermediación de organizaciones. | `asistencia_directa` — manuales.json | 📋 MANUAL | 35% |
| Modernización Laboral (FAL) | Empresas adheridas y evolución de aportes al Fondo de Asistencia. | `fal_modernizacion_laboral` — manuales.json | 📋 MANUAL | 10% (FAL operativo H2-2026) |
| Libertad de Opción en Salud | Traspasos efectivos entre obras sociales y prepagas. | `libertad_opcion_salud` — manuales.json | ❌ BLOQUEADO | 40% (manual) |
| Protocolo Antipiquetes | Evolución de cortes sin interrupción total del tránsito. | `protocolo_antipiquetes` — manuales.json | 📋 MANUAL | 55% |

### Hito reciente: desbloqueo del RIGI (may-2026)

El indicador `rigi_inversiones` estaba bloqueado. La investigación produjo el siguiente recorrido:

| Vía intentada | Resultado |
|---|---|
| Portal oficial `argentina.gob.ar/economia/industria/rigi` | 404 (URL cambió, sin alternativa publicada) |
| CKAN datos.gob.ar packages RIGI | 0 packages |
| InfoLeg `texto="RIGI"` (cualquier tipo) | 93 normas mezcladas — OR-search no aísla aprobaciones |
| InfoLeg `texto="adhesion RIGI"` | 164 normas — OR-search infla resultado |
| Wikipedia "Régimen de Incentivo..." | Página existe pero última edición oct-2025 (desactualizada) |
| BO API JSON | Endpoints retornan HTML, no JSON parseable |
| ComprAR pliegos | ASP.NET con `__VIEWSTATE` — scraping frágil |
| **InfoLeg `tipoNorma=3` (Resolución) + `texto="VPU"` desde jul-2024** | **28 normas** ⭐ |

**Solución implementada:** "VPU" (Vehículo de Proyecto Único, terminología técnica de la Ley 27.742) es vocabulario **exclusivo** del RIGI — aparece solo en resoluciones de aprobación e implementación. Calibración: 28 resoluciones VPU = avance 28.0%, casi idéntico al dato manual de El Cronista may-2026 (28.7% calculado sobre USD 27.210M aprobados / USD 94.965M totales).

### Por qué los 2 BLOQUEADOS no se pudieron automatizar

| Indicador | Fuentes intentadas | Razón del bloqueo |
|---|---|---|
| `libertad_opcion_salud` (SSS — traspasos obras sociales / prepagas) | SSS HTML directo • Playwright headless • datos.gob.ar Padrón Obras Sociales • SSS publicaciones/memorias | SSS usa fingerprinting back-end (`/fwb/first_submit.df`); el endpoint de datos retorna "No se reportan datos" incluso con browser real. `function.js` = 46 bytes (vacío). Padrón obras sociales en datos.gob.ar tiene CSVs **last_modified 2018-2019** (dataset abandonado). Sin alternativa pública. |
| `privatizaciones` (BO — transferencia efectiva de acciones) | BO API JSON • InfoLeg `tipo=1/2/3 texto="privatizacion"/"transferencia acciones"/"Aerolineas"` • ComprAR pliegos | BO no expone API JSON pública (lookups retornan HTML). ComprAR es ASP.NET con `__VIEWSTATE` (scraping frágil). InfoLeg `tipo=3 texto="privatizacion"` = 9 normas pero OR-search ambiguo: contar normas ≠ transferencia completa. |

**Política de actualización:** ambos quedan en `data/gestion/manuales.json` con calendario de revisión trimestral desde anuncios oficiales (Ministerio de Economía / SSS).

### Manuales legítimos (sin alternativa automatizada pero no bloqueados técnicamente)

| Indicador | Por qué manual |
|---|---|
| `concesiones_infraestructura` | Vialidad Nacional / ORSNA publican informes en PDF trimestrales — sin API estructurada. Automatizable a mediano plazo con scraping de PDFs. |
| `asistencia_directa` | ANSES no expone padrón de beneficiarios vía API pública. Pendiente portal transparencia. |
| `fal_modernizacion_laboral` | FAL no entra en operación hasta H2-2026 (postergado). Auto factible cuando MTEySS/ARCA publiquen aportes. |
| `protocolo_antipiquetes` | Ministerio de Seguridad sin registro estructurado público de cortes. Requeriría acuerdo institucional. |

---

## Resumen final de cobertura vs documento 260520

| Cinturón | Total prop. 260520 | ✅ AUTO | 📋 Manual / Placeholder | ❌ Bloqueado | 🔬 No implementado |
|---|---|---|---|---|---|
| Vida Cotidiana | 14 + 1 manual | 14 | 1 (Deserción) | 0 | 0 |
| Macroeconomía | 11 activos + 8 propuestos | 11 | 0 | 0 | 5 (3 ya extraídos en otros cinturones) |
| Política | 10 propuestos | 4 + 3 adicionales | 2 | 0 | 4 |
| Gestión | 12 propuestos | 6 | 4 | 2 | 0 |
| **Totales del 260520** | **47 propuestos** | **35 AUTO** | **7 manual** | **2 bloqueados** | **9 sin implementar** |

**Cobertura efectiva del 260520:** 44/47 cubiertos (94%). De los 3 restantes: 2 bloqueados con razón documentada y 1 cualitativo (Independencia BCRA) sin proxy posible.

**Indicadores adicionales implementados que el 260520 no listaba:** 3 (votómetro electoral en política, patentamiento motos como proxy consumo, brecha CCL como proxy cepo corporativo).
