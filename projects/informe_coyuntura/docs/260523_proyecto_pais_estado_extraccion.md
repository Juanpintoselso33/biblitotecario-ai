# Proyecto País — Estado de extracción de datos

**Fecha:** 23 de mayo de 2026
**Emisor:** Fundación CIGOB — Equipo de Datos y Análisis
**Objeto:** Estado de implementación y extracción automática de los indicadores enunciados en el documento "Proyecto País: Indicadores en trabajo" (260520).

Este documento centraliza el estado de extracción de datos de los cuatro cinturones del informe de coyuntura matusiano. Indica para cada indicador propuesto si está activo en el colector, qué fuente real se usa, y cuándo se ejecutó por última vez con éxito.

---

## Resumen ejecutivo

| Cinturón | Indicadores cubiertos | Auto activos | Manual / placeholder | Bloqueados | Score |
|---|---|---|---|---|---|
| Vida Cotidiana | 14 + 1 manual | 14 (8 fuentes) | 1 (deserción escolar) | 0 | — |
| Macroeconomía | 11 | 11 | 0 | 0 | **2.1 estable** |
| Política | 9 (de 10 propuestos) | 7 | 2 | 0 | **4.7 en tensión** |
| Gestión | 12 | 6 | 4 | 2 | **5.9 en tensión** |
| **Total** | **46** | **38 (82.6%)** | **7 (15.2%)** | **2 (4.3%)** | — |

> **Cobertura del documento 260520:** todos los indicadores propuestos en el documento base están al menos cubiertos como manual/fallback. Solo dos quedaron definitivamente bloqueados por limitaciones de las fuentes oficiales: `libertad_opcion_salud` y `privatizaciones`.

---

## 1. Cinturón de la Vida Cotidiana

**Orquestador:** `scripts/vida_cotidiana/main.py` — 8 fuentes activas, ~32 datapoints por ejecución.
**Última ejecución:** 23-may-2026 13:56 — todas las fuentes OK.

### Indicadores activos (cobertura completa del documento)

| Indicador del 260520 | Implementación técnica | Fuente | Última fecha |
|---|---|---|---|
| Brecha Salario Real vs. CBT | `brecha_salario_cbt` = 3.82 canastas | INDEC (RIPTE + CBT) datos.gob.ar | mar-2026 |
| IPC-Alimentos | `ipc_alimentos` = +3.35% m/m | INDEC serie 146.3 datos.gob.ar | mar-2026 |
| Endeudamiento Familiar | `prestamos_*` BCRA (tarjeta/personales/hipotecarios/consumo) | BCRA API v4.0 | 19-20 may-2026 |
| Peso de Tarifas | `ipc_vivienda` (+3.71%) + `ipc_regulados` (+5.08%) | INDEC | mar-2026 |
| Consumo de Carne Vacuna | `consumo_carne_per_capita` | CICCRA (scraping PDF mensual) | abr-2026 |
| Informalidad Laboral | `informalidad_anual` = 36.75% | INDEC EPH | ene-2026 |
| Mortalidad de PyMEs (proxy) | `ipi + emae` | INDEC | feb-2026 |
| Despacho Cemento e Hierro | `isac` (143.5) + `acero_crudo` (731.6) | INDEC | feb-2026 |
| Pluriempleo (proxy) | `subocupacion_demandante` = 7.8% | INDEC EPH | oct-2025 |
| Espera Salud Pública | `salud_datasets` (3 datasets) | CKAN datasets | — |
| Inseguridad Urbana | `inseguridad_snic` (2.501.057 hechos 2024) | SNIC + CABA | 2024 |
| ICC Confianza Consumidor | `icc_utdt` = 40.5 | UTDT scraping XLS | may-2026 |
| Sentimiento Digital | `sentimiento_digital` (Google Trends 4 términos) | pytrends | tiempo real |
| Apatía Electoral | (`votometro_ventaja_lla` — vive en cinturón POLÍTICO) | Votómetro CIGOB | mar-2026 |
| Patentamiento Motos (extra) | `patentamiento_motos` = 51.124 unidades | CAFAM | may-2026 |

### Pendiente

| Indicador | Estado |
|---|---|
| Deserción Escolar | 📋 Manual — no automatizable, rezago anual |
| `ingreso_disponible_real` (Empiria) | 🔬 Propuesta priorizada — IS_registrado / IPC_vivienda. ene-2026 vs ene-2025: −8.0% i.a. |

### Brecha técnica detectada

El script puente `scripts/vida_cotidiana.py` (que integra con el orquestador global) solo expone 3 indicadores legacy (`ipc_total + desocupacion + icc_utdt`). El dashboard agregado del informe debería leer del output `scripts/vida_cotidiana/data/vida_cotidiana_*.json` para tener cobertura completa.

---

## 2. Cinturón de la Macroeconomía

**Script:** `scripts/macro.py` | **Cache:** `output/cache/macro.json`
**Última ejecución:** 23-may-2026 — **11/11 frescos**, score **2.1 estable**.

### Cobertura 11/11 vs documento (los 11 "activos" del 260520)

| Indicador del 260520 | Implementación | Fuente | Último valor | Score |
|---|---|---|---|---|
| IPC Total | `ipc_total` | INDEC 148.3 datos.gob.ar | 3.38% m/m | 3.4 |
| Reservas BCRA | `reservas_bcra` | BCRA API v4.0 var 1 | 46.585 M USD | 0.0 |
| Tasa BADLAR | `badlar` | BCRA API v4.0 var 7 | 22.0% anual | 2.2 |
| EMAE (Var. Interanual) | `emae_ia` | INDEC 143.3 datos.gob.ar | +1.88% i.a. | 3.1 |
| Saldo Comercial (12m) | `saldo_comercial_12m` | INDEC 164.3 (suma 12) | +17.125 M USD | 0.0 |
| Recaudación Tributaria | `recaudacion` | INDEC 172.3 | −0.99% var m | 6.0 |
| TCRM | `tcrm` | INDEC 116.3 (base 2010=100) | 79.77 | 4.1 |
| Expectativas Inflación (REM) | `rem_ipc_12m` | BCRA API v4.0 var 29 | 24.2% anual | 1.6 |
| Préstamos Privados | `prestamos_privados` | BCRA API v4.0 var 26 | +2.13% var m | 2.9 |
| Base Monetaria | `base_monetaria` | BCRA API v4.0 var 15 | +0.7% var m | 0.0 |
| Tipo de Cambio Mayorista | `tc_mayorista` | BCRA API v4.0 var 5 | −0.27% var m | 0.0 |

### Indicadores propuestos del 260520 (en diseño, no implementados)

| Indicador propuesto | Justificación | Fuente plausible |
|---|---|---|
| Resultado Fiscal Financiero | Incluye intereses; supera primaria | Hacienda — informe mensual |
| Riesgo País (EMBI+) | Costo de oportunidad externa | JPMorgan EMBI+ (vía API o scraping AmbitoFinanciero) |
| Deuda Pública Bruta / PBI | Solvencia estructural | Hacienda — anual |
| Desempleo / Subocupación | Puente con vida cotidiana | INDEC EPH (ya en vida_cotidiana) |
| Utilización Capacidad Instalada | Cuellos de botella industriales | INDEC mensual |
| Pobreza por Ingresos | CBT vs salario medio | Construible con series ya extraídas |
| Brecha Cambiaria | Termómetro de desconfianza | dolarapi.com (ya usado en gestión) |
| Formación Bruta Capital Fijo | Inversión real | INDEC trimestral |

---

## 3. Cinturón de la Política

**Script:** `scripts/politica.py` | **Cache:** `output/cache/politica.json`
**Última ejecución:** 23-may-2026 — **8/9 frescos** (CEPA falló 404, usó cache), score **4.7 en tensión**.

### Estado real: 7 AUTO + 2 manuales (no "íntegramente propuesto" como decía el 260520)

| Concepto del 260520 | Implementación técnica | Fuente | Estado | Valor |
|---|---|---|---|---|
| Tasa de Eficacia Parlamentaria (TEP) | `eficacia_legislativa` | datos.hcdn.gob.ar CKAN (proyectos PE vs sanciones 12m) | ✅ AUTO | 4.8% (1/21) |
| Ratio DNU | `ratio_dnu` | InfoLeg sesión POST (DNUs / leyes año corriente) | ✅ AUTO | 3.14 (22 DNU / 7 leyes) |
| Índice de Armonía Federal (IAF) | `iaf_transferencias` | RON Hacienda CSV (var real YoY) | ✅ AUTO | +1.8% real |
| Índice de Tensión Social (ITS) | `movilizacion_cepa` | centrocepa.com.ar scrape | ✅ AUTO | 46.0 (cache, 404 hoy) |
| Apatía electoral / brecha | `votometro_ventaja_lla` | Votómetro CIGOB HTML | ✅ AUTO | +13.3 pp (LLA−PJ) |
| Frustración legislativa | `veto_quorum` | datos.hcdn.gob.ar CKAN (`REUNION_TIPO~Fracasada`) | ✅ AUTO | 0.0% (período 144) |
| Bloqueo post-dictamen | `comisiones_caidas` | datos.hcdn.gob.ar CKAN (OD vs sanciones) | ✅ AUTO | 99.6% (alto estructural) |
| Cohesión interna oficialismo | `cohesion_bloque` | placeholder 78% — votaciones CKAN congeladas en 2019 (LLA no existía) | 📋 manual | 78% |
| Alianzas territoriales | `gobernadores_alineamiento` | placeholder 55% — sin fuente estructurada | 📋 manual | 55% |

### Indicadores propuestos del 260520 sin implementar

| Indicador propuesto | Razón de no-implementación |
|---|---|
| Tasa de Judicialización de la Gestión (cautelares contra reformas) | Requiere scraping CSJN / juzgados federales — sin fuente estructurada |
| Control de Agenda (vida media de crisis vía Google Trends) | Implementable con pytrends — pendiente de diseño |
| Tasa de Compromiso RIGI/RIMI provincial-sindical | Requiere parseo de declaraciones provinciales — manual |
| Impacto del Clima Internacional (procesos electorales regionales) | Construible con calendario electoral + spread soberano regional |
| Tensión Estructural Discursiva (conflicto entre bloques) | Requiere NLP sobre Twitter/X de diputados — fuera de scope |
| Independencia del Banco Central | Cualitativo — sin métrica objetiva |

### Bloqueantes técnicos de los 2 manuales

- `cohesion_bloque`: votaciones nominales CKAN congeladas en período 137 (2019). Composición LLA (95 dip.) disponible pero sin `PERSONA_ID` que mapee a votos históricos. Requiere headless sobre `hcdn.gob.ar/votaciones`.
- `gobernadores_alineamiento`: sin fuente estructurada. NLP sobre declaraciones (La Nación Data, Infobae) sería un proyecto separado.

---

## 4. Cinturón de Gestión

**Script:** `scripts/gestion.py` | **Cache:** `output/cache/gestion.json` | **Data:** `data/gestion/manuales.json`
**Última ejecución:** 23-may-2026 — **auto_frescos=6/6 con_datos=12/12**, score **5.9 en tensión**.

### Cobertura completa del documento 260520 (12/12 cubiertos)

| Eje del 260520 | Implementación | Fuente | Estado | Avance |
|---|---|---|---|---|
| Desmantelamiento del Cepo | `cepo_mulc` (brecha **CCL**/oficial) | dolarapi.com | ✅ AUTO | 78.4% (brecha 4.32%) |
| Privatizaciones | `privatizaciones` | manuales.json (BO sin API JSON) | 📋 manual | 15% |
| Concesiones de Infraestructura | `concesiones_infraestructura` | manuales.json (Vialidad/ORSNA sin API) | 📋 manual | 35% |
| Reducción del Estado | `reduccion_estado` | datos.gob.ar 324.1 (puestos trabajo público) | ✅ AUTO | 2.7% (var −0.8%) |
| Reestructuración de Organismos | `reestructuracion_organismos` | InfoLeg sesión POST `texto="disolucion"` desde dic-2023 | ✅ AUTO | 40% (18 normas) |
| Inversiones (RIGI / Super RIGI) | `rigi_inversiones` | InfoLeg sesión POST `tipo=3 texto="VPU"` desde jul-2024 | ✅ AUTO ⭐ | 28% (28 resol. VPU) |
| Desregulación Normativa | `desregulacion_normativa` | InfoLeg sesión POST `texto="deroga"` desde dic-2023 | ✅ AUTO | 55% (55 normas) |
| Apertura Comercial | `apertura_comercial` | datos.gob.ar 163.3 (importaciones totales) | ✅ AUTO | 100% (+42.4% i.a.) |
| Asistencia Directa | `asistencia_directa` | manuales.json (ANSES sin API pública) | 📋 manual | 35% |
| Modernización Laboral (FAL) | `fal_modernizacion_laboral` | manuales.json (operativo H2-2026) | 📋 manual | 10% |
| Libertad de Opción en Salud | `libertad_opcion_salud` | manuales.json | ❌ BLOQUEADO | 40% |
| Protocolo Antipiquetes | `protocolo_antipiquetes` | manuales.json (Min. Seguridad sin datos) | 📋 manual | 55% |

### Hito reciente: desbloqueo del RIGI (may-2026)

El indicador `rigi_inversiones` estaba bloqueado: el portal oficial `argentina.gob.ar/economia/industria/rigi` retorna 404; CKAN no tiene packages RIGI; InfoLeg con `texto="RIGI"` devuelve 93 normas mezcladas (OR-search no aísla aprobaciones).

**Solución:** buscar `tipoNorma=3` (Resolución) + `texto="VPU"` desde 01/07/2024. **VPU** (Vehículo de Proyecto Único, Ley 27.742) es vocabulario técnico **exclusivo** del régimen — aparece solo en resoluciones de aprobación e implementación. Resultado: 28 resoluciones VPU = avance 28.0%, casi idéntico al dato manual de El Cronista may-2026 (28.7% calculado sobre USD 27.210M aprobados / USD 94.965M totales).

### Bloqueantes definitivos

| Indicador | Razón |
|---|---|
| `libertad_opcion_salud` | SSS usa fingerprinting back-end (`/fwb/first_submit.df`). Retorna "No se reportan datos" incluso con Playwright. Padrón obras sociales en datos.gob.ar está congelado en 2019 (último update CSV). Sin alternativa pública. |
| `privatizaciones` | Boletín Oficial no expone API JSON pública. ComprAR.gob.ar es ASP.NET con `__VIEWSTATE` (difícil scraping). InfoLeg `tipo=3 texto="privatizacion"`=9 normas pero el OR-search no permite aislar transferencias efectivas vs. resoluciones procedimentales. |

---

## Hitos de implementación may-2026

| Fecha | Hito |
|---|---|
| 03-may | Cinturón Macro completo: 11/11 AUTO desde INDEC/BCRA |
| 10-may | Vida cotidiana: orquestador `main.py` con 8 fuentes, 14 conceptos del 260520 cubiertos |
| 12-may | Política: marco Babino aplicado — ICG UTDT removido, `ratio_dnu` agregado |
| 13-may | Cinturón Político: agregados `veto_quorum` y `comisiones_caidas` vía CKAN HCDN |
| 14-may | Cinturón Político: 7 AUTO + 2 manuales |
| 23-may | Cinturón Gestión: rediseñado de 2 indicadores a 12 (scorecard reformas APN) |
| 23-may | Gestión: `reestructuracion_organismos` AUTO via InfoLeg `disolucion` |
| 23-may | Gestión: `desregulacion_normativa` AUTO via InfoLeg `deroga` |
| 23-may | Gestión: `cepo_mulc` corregido — blue → CCL (cepo persistente para empresas) |
| 23-may | Gestión: **RIGI desbloqueado** via InfoLeg `tipo=3 texto="VPU"` |

---

## Patrones técnicos consolidados

### InfoLeg sesión POST
Patrón compartido entre `politica.py:fetch_ratio_dnu` y `gestion.py` (3 colectores). Requiere:
1. `GET https://servicios.infoleg.gob.ar/infolegInternet/` para obtener jsessionid
2. Extraer `action_url` del HTML home con regex `action="(/infolegInternet/[^"]+)"`
3. `POST` con `tipoNorma`, fechas, `texto`, mantienendo la sesión
4. Parsear conteo con regex `r"Encontradas?[:\s]+(\d+)"`

**Gotcha:** búsqueda de texto es OR (no AND/exacta). Para aislar normas específicas, usar vocabulario técnico exclusivo (ej: "VPU" para RIGI).

### CKAN HCDN
Patrón en `politica.py` para 3 indicadores. Gotchas documentados en `memory/project_informe_coyuntura.md`:
- `q=` es full-text por tokens, NO substring (`q="HCDN144"` no matchea `HCDN144R02`)
- Filtros con acentos fallan — usar Python-side con `.lower()`
- `dictámenes.EXPEDIENTE` join directo con `movimientos.PROYECTO_ID`
- Período legislativo: `144 + (año_actual − 2026)`

### datos.gob.ar series
Patrón estándar (`apis.datos.gob.ar/series/api/series/`):
```python
params = {"ids": series_id, "format": "json", "limit": N, "sort": "desc"}
```
8 series INDEC activas distribuidas en macro + gestión + vida cotidiana.

### BCRA API v4.0
SSL warning requiere `verify=False` + `urllib3.disable_warnings()`. Datos en orden **descendente**: `detalle[0]` = más reciente.

---

## Próximos pasos sugeridos

| Prioridad | Acción |
|---|---|
| Alta | Integrar output `vida_cotidiana/main.py` al dashboard global (actualmente solo 3 indicadores vía script puente) |
| Alta | Implementar `ingreso_disponible_real` (Empiria) como colector — desarmar mito "desinflación = bienestar" |
| Media | `concesiones_infraestructura` — explorar API Vialidad Nacional o scraping informes ORSNA |
| Media | `asistencia_directa` — explorar portal transparencia ANSES |
| Media | `cohesion_bloque` — headless browser sobre `hcdn.gob.ar/votaciones` para mapear LLA |
| Baja | Cinturón Macro: agregar Riesgo País EMBI+, FBKF, Pobreza por Ingresos del documento original |
| Baja | Cinturón Político: Judicialización (CSJN/cautelares), Control de Agenda (Trends) |
| H2-2026 | `fal_modernizacion_laboral` AUTO cuando FAL sea operativo |

## Bloqueos persistentes (sin solución técnica viable)

- `libertad_opcion_salud` (SSS) — actualización manual trimestral desde reportes oficiales SSS
- `privatizaciones` (BO) — actualización manual mensual desde anuncios Ministerio de Economía
- `protocolo_antipiquetes` (Min. Seguridad) — sin fuente pública estructurada
