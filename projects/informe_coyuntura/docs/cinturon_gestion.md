# Cinturón Gestión — Indicadores Activos

Script: `scripts/gestion.py` | Cache: `output/cache/gestion.json`
Peso en score global: **20%** (`config.py → PESOS_CINTURONES["gestion"]`)
Barbarismo de riesgo: **gerencial**
Data: `data/gestion/manuales.json`

---

## Encuadre

Mide el **cumplimiento de reformas del Estado y compromisos de la Administración Pública Nacional** del programa Milei (dic-2023–). Score 0–10: mayor = mayor brecha compromisos/ejecución (tensión gerencial).

Cada indicador tiene `avance_pct` (0–100%) que representa el % del objetivo de reforma ejecutado.
`score_tension = 10 × (1 − avance_pct/100)`.
Score global = promedio de scores de indicadores disponibles.

---

## Indicadores activos (12)

| Nombre | Estado | Fuente | Tipo | Avance actual |
|---|---|---|---|---|
| `cepo_mulc` | ✅ auto | dolarapi.com — brecha **CCL**/oficial | Daily | ~78% (brecha 4.3%) |
| `privatizaciones` | ❌ bloqueado | Contar normas ≠ privatización completa; sin proxy confiable | Manual fallback | ~15% |
| `concesiones_infraestructura` | ⚠ manual | Vialidad Nacional / ORSNA | Manual | ~35% |
| `reduccion_estado` | ✅ auto | datos.gob.ar `324.1_TOTAL_SECTAJO__36` | Trimestral | ~3% |
| `reestructuracion_organismos` | ✅ auto | InfoLeg sesión POST — `texto="disolucion"` + rango dic-2023 | Mensual | ~40% (18 normas) |
| `rigi_inversiones` | ✅ auto | InfoLeg sesión POST — tipo=3 + `texto="VPU"` desde jul-2024 | Mensual | ~28% (28 normas VPU) |
| `desregulacion_normativa` | ✅ auto | InfoLeg sesión POST — `texto="deroga"` + rango dic-2023 | Mensual | ~55% (55 normas) |
| `apertura_comercial` | ✅ auto | datos.gob.ar `163.3_MTALTAL_0_0_7` | Mensual | ~100% |
| `asistencia_directa` | ⚠ manual | ANSES — padrón Volver al Trabajo | Manual | ~35% |
| `fal_modernizacion_laboral` | ⚠ manual | MTEySS — operación FAL | Manual | ~10% |
| `libertad_opcion_salud` | ❌ bloqueado | SSS fingerprinting back-end — "No se reportan datos" incluso Playwright | Manual fallback | ~40% |
| `protocolo_antipiquetes` | ⚠ manual | Min. Seguridad — elaboración CIGOB | Manual | ~55% |

---

## Detalle por indicador

### `cepo_mulc` — Cepo Corporativo
- **Fuente:** `GET https://dolarapi.com/v1/dolares`
- **Cálculo:** brecha = (CCL_venta − oficial_venta) / oficial_venta × 100%
- **Avance:** `max(0, 100 − brecha × 5)` → brecha 0% = avance 100%; brecha 20% = avance 0%
- **Interpretación:** El cepo minorista se levantó en abr-2025. Para **empresas** persiste la restricción: giro de dividendos, remesa de utilidades, acceso al MULC para capital. El CCL (contado con liquidación) refleja esta brecha. Blue ≈ 0% es engañoso — debe usarse CCL.
- **Última ejecución (may-2026):** CCL=1486.6, oficial=1425 → brecha=4.3% → avance=78.4%

### `privatizaciones` — Privatizaciones
- **Fuente:** Boletín Oficial — transferencia efectiva de acciones
- **Cálculo:** % empresas privatizadas efectivamente del listado DL 70/23
- **Avance:** ~15% (Aerolíneas y Correo en proceso parlamentario sin transferencia)
- **Pendiente automatizar:** Scraping BO con keywords "transferencia de acciones" + empresa

### `concesiones_infraestructura` — Concesiones de Infraestructura
- **Fuente:** Vialidad Nacional / ORSNA — informes periódicos
- **Cálculo:** % corredores viales concesionados / 9 corredores del plan
- **Avance:** ~35% (algunos en licitación activa)
- **Pendiente automatizar:** API Vialidad Nacional o scraping de informes ORSNA

### `reduccion_estado` — Reducción del Estado
- **Fuente:** `GET https://apis.datos.gob.ar/series/api/series/?ids=324.1_TOTAL_SECTAJO__36&sort=desc&limit=16`
- **Serie:** "Total sector público puestos trabajo" — trimestral
- **Cálculo:** var% vs baseline Q4-2023/Q1-2024. Meta de referencia: -30% = avance 100%.
- **Nota:** La serie mide **insumo de mano de obra** (puede ser índice, no headcount). Variación -0.8% vs Q1-2024 sugiere reducción modesta. Para mayor precisión, buscar serie de nómina ONP en datos.gob.ar.
- **Última ejecución:** -0.8% vs 2024-01-01 → avance 2.7%

### `reestructuracion_organismos` — Reestructuración de Organismos
- **Fuente:** InfoLeg sesión POST — `texto="disolucion"` + rango dic-2023/hoy
- **Cálculo:** count de normas con "disolucion" publicadas desde dic-2023. 45 = avance 100%.
- **Nota técnica:** DNU 70/23 (el mega-decreto de dic-2023 que redujo secretarías de 106 a ~54) NO aparece en la búsqueda de texto libre de InfoLeg (no está indexado como full-text). Los 18 documentos capturados son acciones de disolución/fusión POSTERIORES al megadecreto.
- **Calibración:** 18 actos = avance 40% validado contra estimación manual. Objetivo 45 = 100%.
- **Avance (may-2026):** 18 normas → avance 40.0%

### `rigi_inversiones` — Inversiones RIGI
- **Fuente:** InfoLeg sesión POST — `tipoNorma=3` (Resolución) + `texto="VPU"` desde 01/07/2024
- **Cálculo:** count Resoluciones con "VPU" (Vehículo de Proyecto Único — término técnico exclusivo del RIGI, Ley 27.742). Fórmula directa: `avance_pct = min(100, count)`.
- **Calibración:** 28 resoluciones VPU ≈ 16 proyectos aprobados ≈ USD 27.210M (mayo-2026). Ratio ~1.7 resoluciones por proyecto (aprobación + complementarias). Calibrado contra dato manual El Cronista/La Nueva may-2026.
- **Nota técnica:** Búsqueda OR-search en InfoLeg falla con "RIGI" (93 normas mezcladas) o "adhesion" (164). "VPU" es palabra técnica que aparece SOLO en resoluciones de aprobación e implementación del régimen. Confirmado: search sin filtro tipo = 34 (similar al 28 con tipo=3 → casi todas son Resoluciones, como se espera).
- **Avance (may-2026):** 28 normas VPU → avance 28.0%

### `desregulacion_normativa` — Desregulación Normativa
- **Fuente:** InfoLeg sesión POST — GET home → extraer jsessionid → POST con `texto="deroga"` y fechas dic-2023/hoy
- **Cálculo:** count de normas con "deroga" en el texto publicadas desde dic-2023. 100 = avance 100% (escala lineal).
- **Avance (may-2026):** 55 normas derogantes → avance 55%
- **Nota técnica:** El buscador InfoLeg requiere sesión activa (jsessionid). GET simple falla. Mismo patrón que `politica.py → fetch_ratio_dnu`. Cada documento cuenta como 1 independientemente de cuántos artículos derogue (DL 70/23 = 1 acción con cientos de derogaciones).
- **Calibración:** 100 normas derogantes = avance 100%. Ajustable si se quiere mayor granularidad.

### `apertura_comercial` — Apertura Comercial
- **Fuente:** `GET https://apis.datos.gob.ar/series/api/series/?ids=163.3_MTALTAL_0_0_7&sort=desc&limit=14`
- **Serie:** "Importaciones. Total. Millones USD. Mensual." (INDEC)
- **Cálculo:** var% i.a. → +30% = avance 100%; flat = avance 50%; -30% = avance 0%
- **Nota:** Proxy imperfecto — mide recuperación del comercio, no directamente eliminación de aranceles/NTBs.
- **Última ejecución:** +42.4% i.a. (feb-2025) → avance 100% (rebote desde recesión 2024)

### `asistencia_directa` — Asistencia Directa
- **Fuente:** ANSES / MDS — programa Volver al Trabajo (ex Potenciar Trabajo)
- **Cálculo:** % beneficiarios que cobran directamente / total beneficiarios
- **Avance:** ~35% (estimado)
- **Pendiente automatizar:** Portal de datos ANSES (no disponible vía API pública)

### `fal_modernizacion_laboral` — Modernización Laboral (FAL)
- **Fuente:** MTEySS + normativa (La Nación 22-may-2026)
- **Cálculo:** % etapas implementadas (ley → reglamentación → operación)
- **Estado may-2026:** FAL aprobado en ley, reglamentación incompleta (ARCA/CNV/ANSES pendiente). Entrada en vigencia postergada a H2-2026.
- **Avance:** 10% (legislación vigente, operación pendiente)

### `libertad_opcion_salud` — Libertad de Opción en Salud
- **Fuente:** `https://www.sssalud.gob.ar/index.php?page=opciones&cat=institucion`
- **Cálculo:** opciones captadas acumuladas desde dic-2023 / baseline estimado
- **Avance:** ~40% (estimado — scraper no puede distinguir opciones pre/post dic-2023)
- **Pendiente:** Obtener serie temporal SSS post-2023 para calcular variación correcta

### `protocolo_antipiquetes` — Protocolo Antipiquetes
- **Fuente:** Ministerio de Seguridad — elaboración CIGOB
- **Cálculo:** % cortes con carril libre garantizado / total cortes registrados desde dic-2023
- **Avance:** ~55% (estimado)
- **Sin fuente automatizable:** Requiere relevamiento propio o acceso a datos Min. Seguridad / Policía Federal

---

## Fórmula de score (0–10, mayor = mayor tensión de gestión)

```python
# Por indicador:
score_i = 10.0 × (1 − avance_pct / 100.0)

# Cinturón:
score = promedio(score_i para todos los indicadores con avance_pct ≠ null)
```

Umbrales: `0–3` estable | `4–6` en_tension | `7–10` tensionado

**Score actual (may-2026):** 5.8

---

## Ejecución y exit codes

```bash
cd projects/informe_coyuntura
python scripts/gestion.py
# exit 0 → todos los colectores auto devolvieron datos frescos
# exit 1 → al menos 1 colector auto fresco (parcial)
# exit 2 → ningún colector auto fresco
```

---

## Estado de automatización (may-2026)

| Indicador | Estado | Notas |
|---|---|---|
| `cepo_mulc` | ✅ AUTO | CCL/oficial brecha. Fix may-2026: blue→CCL. |
| `reduccion_estado` | ✅ AUTO | datos.gob.ar serie INDEC. Avance bajo (~3%). |
| `apertura_comercial` | ✅ AUTO | datos.gob.ar serie INDEC. |
| `desregulacion_normativa` | ✅ AUTO | InfoLeg sesión POST. Implementado may-2026. |
| `reestructuracion_organismos` | ✅ AUTO | InfoLeg sesión POST `disolucion`. Implementado may-2026. |
| `rigi_inversiones` | ✅ AUTO | InfoLeg sesión POST `texto="VPU"` desde jul-2024. Calibrado 28=28% (vs 28.7% manual). Implementado may-2026. |
| `libertad_opcion_salud` | ❌ BLOQUEADO | SSS fingerprinting back-end. Padrón datos.gob.ar congelado en 2019. Sin alternativa. |
| `privatizaciones` | ❌ BLOQUEADO | BO sin API JSON. ComprAR ASP.NET con __VIEWSTATE. tipo=3 'privatizacion'=9 ambiguo (OR-search). |
| `concesiones_infraestructura` | ⚠ MANUAL | Sin API. Baja prioridad. |
| `asistencia_directa` | ⚠ MANUAL | ANSES sin API pública. |
| `fal_modernizacion_laboral` | ⚠ MANUAL | Auto posible desde H2-2026 (FAL operativo). |
| `protocolo_antipiquetes` | ⚠ MANUAL | Sin fuente pública estructurada. |

## Próximos pasos de automatización

| Prioridad | Indicador | Acción |
|---|---|---|
| Alta | `reduccion_estado` | Identificar serie ONP headcount en datos.gob.ar (buscar "nomina sector publico") |
| Baja | `concesiones_infraestructura` | API Vialidad Nacional o scraping PDF informes |
| Baja | `asistencia_directa` | Portal transparencia ANSES |
| H2-2026 | `fal_modernizacion_laboral` | Auto cuando FAL sea operativo: MTEySS aportes vía ANSES |
| — | `protocolo_antipiquetes` | Sin fuente pública estructurada — requiere acuerdo Min. Seguridad |
| — | `libertad_opcion_salud` | BLOQUEADO definitivo (SSS fingerprinting). Carga manual desde reporte SSS trimestral |
| — | `privatizaciones` | BLOQUEADO definitivo (BO sin API). Carga manual desde anuncios oficiales |
