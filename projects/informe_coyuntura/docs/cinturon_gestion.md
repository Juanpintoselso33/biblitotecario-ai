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
| `cepo_mulc` | ✅ auto | dolarapi.com — brecha blue/oficial | Daily | ~100% |
| `privatizaciones` | ⚠ manual | Boletín Oficial — transferencia de acciones | Manual | ~15% |
| `concesiones_infraestructura` | ⚠ manual | Vialidad Nacional / ORSNA | Manual | ~35% |
| `reduccion_estado` | ✅ auto | datos.gob.ar `324.1_TOTAL_SECTAJO__36` | Trimestral | ~3% |
| `reestructuracion_organismos` | ⚠ manual | Boletín Oficial — decretos disolución/fusión | Manual | ~40% |
| `rigi_inversiones` | ⚠ manual | Portal RIGI / prensa oficial | Manual | ~29% |
| `desregulacion_normativa` | ⚡ scrape | InfoLeg `buscarNormas.do` | Mensual | ~45% |
| `apertura_comercial` | ✅ auto | datos.gob.ar `163.3_MTALTAL_0_0_7` | Mensual | ~100% |
| `asistencia_directa` | ⚠ manual | ANSES — padrón Volver al Trabajo | Manual | ~35% |
| `fal_modernizacion_laboral` | ⚠ manual | MTEySS — operación FAL | Manual | ~10% |
| `libertad_opcion_salud` | ⚡ scrape | SSS — opciones captadas | Mensual | ~40% |
| `protocolo_antipiquetes` | ⚠ manual | Min. Seguridad — elaboración CIGOB | Manual | ~55% |

---

## Detalle por indicador

### `cepo_mulc` — Desmantelamiento del Cepo
- **Fuente:** `GET https://dolarapi.com/v1/dolares`
- **Cálculo:** brecha = (blue_venta − oficial_venta) / oficial_venta × 100%
- **Avance:** `max(0, 100 − brecha × 2)` → brecha 0% = avance 100%; brecha 50% = avance 0%
- **Interpretación:** Brecha cambiaria como proxy del grado de liberalización. Unificación cambiaria realizada en abr-2025 (acuerdo FMI). Brecha ≈ 0% confirma cepo desmantelado a nivel mayorista.
- **Última ejecución:** brecha = 0.0% → avance 100%

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
- **Fuente:** Boletín Oficial — decretos de disolución/fusión APN
- **Cálculo:** % organismos reestructurados / plan original
- **Avance:** ~40% (secretarías: de 106 a ~54 en may-2026)
- **Pendiente automatizar:** Scraping BO + conteo acumulado de decretos de disolución

### `rigi_inversiones` — Inversiones RIGI
- **Fuente:** Portal RIGI + Ministerio de Economía / prensa
- **Cálculo:** USD aprobados / (USD aprobados + USD en carpeta) × 100
- **Datos may-2026:** 13 proyectos aprobados — USD 27.210M | 22 en carpeta — USD 67.755M → avance 28.7%
- **Pendiente automatizar:** Scraping `argentina.gob.ar/economia/industria/rigi` (URL cambia, actualmente 404)

### `desregulacion_normativa` — Desregulación Normativa
- **Fuente:** `https://servicios.infoleg.gob.ar/infolegInternet/buscarNormas.do?estado=DEROGADA&fechaDesde=01/12/2023`
- **Cálculo:** total normas derogadas acum. desde dic-2023. 2000 = avance 100%.
- **Avance:** ~45% (estimado — scraper activo pero regex no siempre matchea el total del HTML)
- **Nota:** DL 70/23 derogó miles de artículos. Para mejor automatización: usar dataset InfoLeg CSV de datos.jus.gob.ar

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

## Roadmap de automatización pendiente

| Prioridad | Indicador | Acción |
|---|---|---|
| Alta | `reduccion_estado` | Identificar serie ONP headcount en datos.gob.ar (buscar "nomina sector publico") |
| Alta | `desregulacion_normativa` | Usar dataset CSV InfoLeg de datos.jus.gob.ar (actualización diaria) |
| Alta | `rigi_inversiones` | Encontrar URL correcta del portal RIGI (actualmente 404) |
| Media | `privatizaciones` | Scraping BO acumulado con keywords empresa + transferencia acciones |
| Media | `reestructuracion_organismos` | Scraping BO decretos de disolución/fusión + conteo histórico |
| Media | `libertad_opcion_salud` | Parsear tabla SSS con serie temporal post-dic-2023 |
| Baja | `concesiones_infraestructura` | API Vialidad Nacional o scraping PDF informes |
| Baja | `asistencia_directa` | Portal transparencia ANSES |
| — | `fal_modernizacion_laboral` | Auto cuando FAL sea operativo (H2-2026): MTEySS aportes |
| — | `protocolo_antipiquetes` | Sin fuente pública estructurada — requiere acuerdo Min. Seguridad |
