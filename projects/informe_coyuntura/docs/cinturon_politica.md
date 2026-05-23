# Cinturón Político — Indicadores Activos

Script: `scripts/politica.py` | Cache: `output/cache/politica.json`
Peso en score global: **30%** (`config.py → PESOS_CINTURONES["politica"]`)
Barbarismo de riesgo: **político** — confundir popularidad con poder.

> **Nota metodológica (may-2026):** ICG UTDT removido del cinturón. Mide confianza ciudadana en el gobierno (dimensión que pertenece al cinturón vida_cotidiana / Votómetro), no la capacidad de gobernar con actores políticos. Según Luis Babino (reunión 12-may-2026): "yo no lo veo" en este cinturón. Reemplazado por `ratio_dnu` — indicador de debilidad legislativa y exposición judicial.

Fuente conceptual: Carlos Matus, *Política, Planificación y Gobierno* — capital político como
recurso acumulable en 5 dimensiones independientes: imagen, voto, confianza institucional,
cohesión interna del oficialismo, alianzas territoriales, conflicto social.

---

## Indicadores activos (9) — 7 AUTO + 2 manual

| Nombre | Qué mide | Fuente | Frecuencia | Estado |
|---|---|---|---|---|
| `votometro_ventaja_lla` | Brecha ponderada LLA − PJ en intención de voto | Votómetro CIGOB (HTML) | Por encuesta | ✅ AUTO |
| `ratio_dnu` | DNUs / leyes sancionadas — año corriente | InfoLeg sesión POST | Mensual | ✅ AUTO |
| `movilizacion_cepa` | Conflictividad social: conflictos laborales y protesta | centrocepa.com.ar scrape | Por informe | ✅ AUTO |
| `iaf_transferencias` | Variación real YoY de transferencias federales totales (RON) | argentina.gob.ar/hacienda CSV | Anual | ✅ AUTO |
| `eficacia_legislativa` | % proyectos PE aprobados, ventana 12m | datos.hcdn.gob.ar CKAN | Mensual | ✅ AUTO |
| `veto_quorum` | % sesiones frustradas por falta de quórum | datos.hcdn.gob.ar CKAN (`REUNION_TIPO~Fracasada`) | Mensual | ✅ AUTO |
| `comisiones_caidas` | % proyectos con dictamen OD que no llegan al recinto | datos.hcdn.gob.ar CKAN | Mensual | ✅ AUTO |
| `cohesion_bloque` | % diputados LLA que votan alineados con la posición oficial | placeholder 78% — votaciones CKAN congeladas en 2019 (LLA no existía) | Mensual | 📋 manual |
| `gobernadores_alineamiento` | % gobernadores alineados con política nacional | placeholder 55% — sin fuente estructurada | Mensual | 📋 manual |

---

## Descripción por indicador

### `votometro_ventaja_lla` — Brecha electoral LLA−PJ (Votómetro CIGOB)
- **Qué mide:** diferencia ponderada en pp entre LLA y PJ en intención de voto. Sintetiza las encuestas espacio más recientes con decaimiento temporal y ponderación por calidad consultora. Dimensión *imagen/voto* de Matus.
- **Fuente:** `projects/votometro/web/votometro.html` → array `encuestasRaw`
- **Filtros:** solo entradas con `tipo='espacio'`; ventana últimas 60 días desde la encuesta más reciente
- **Peso:** `exp(−0.015 × días) × calidad_mult` donde A=3, B=2, C=1
- **Cálculo:** `gap = LLA_ponderado − PJ_ponderado` en pp
- **Unidad:** pp (puntos porcentuales)
- **Última ejecución exitosa:** gap=+13.3pp (LLA 41.8 / PJ 28.5) — n=11 encuestas (mar-2026)
- **Nota:** se marca `desactualizado=True` si la encuesta espacio más reciente tiene más de 60 días.

### `ratio_dnu` — Ratio DNU / leyes sancionadas
- **Qué mide:** proporción de DNUs emitidos respecto a leyes sancionadas por el Congreso en el año corriente. Mayor ratio = mayor dependencia del decreto → debilidad legislativa y exposición a judicialización. Dimensión *poder legislativo + legitimidad normativa* (Luis Babino: Agregados de Poder).
- **Fuente:** `servicios.infoleg.gob.ar/infolegInternet/buscar` — búsqueda por tipo de norma y período
- **Cálculo:** `ratio = count(DNUs, enero–hoy) / count(leyes sancionadas, enero–hoy)`
- **Unidad:** ratio sin unidad (ej: 0.8 = 80 DNUs por cada 100 leyes)
- **Score:** ratio 0→0, 1.0→5, 2.0+→10 (formula: `ratio × 5`)
- **Referencia histórica:** año normal ~0.3–0.5; gobierno DNU-intensivo ~1.0–2.0+
- **Nota:** se marca `desactualizado=True` si el dato tiene más de 30 días.

### `movilizacion_cepa` — Conflictividad social (CEPA)
- **Qué mide:** intensidad de la protesta social: huelgas, cortes, conflictos laborales y movilizaciones. Dimensión *conflicto social* de Matus.
- **Fuente:** scrape de `centrocepa.com.ar/informes` → último informe con "conflictividad" en URL → extracción de cifra de conflictos
- **Cálculo:** extrae "X casos por mes" o "al menos N conflictos" del texto del informe; normaliza a 0–100 (80 casos/mes = 100 ó 200 conflictos acumulados = 100)
- **Unidad:** índice 0–100 (mayor = mayor conflictividad)
- **Última ejecución exitosa:** 46.0 (92 conflictos laborales en lo que va de 2026 — informe CEPA may-2026)

### `iaf_transferencias` — Variación real de transferencias federales (RON Hacienda)
- **Qué mide:** variación real interanual de las transferencias federales totales al sistema provincial (Régimen de Coparticipación + otros regímenes). Captura la dimensión fiscal del IAF (Índice de Armonía Federal) de Babino: si el gobierno cumple con el flujo de recursos a provincias. Mayor caída real → mayor tensión fiscal federal → mayor presión sobre gobernadores.
- **Fuente:** CSV anual de la Serie RON (Recaudación por Origen y Naturaleza), Ministerio de Hacienda — `serie_ron_2003_2025.csv`
- **Cálculo:** suma de columna `monto` (todos regímenes y provincias) para año de referencia (año actual − 1) vs año anterior (año actual − 2). Deflactada por IPC interanual diciembre INDEC.
- **Unidad:** % variación real YoY (ej.: −15.0 = caída real del 15%)
- **Score:** `+10%→0, 0%→2.5, −10%→5, −20%→7.5, −30%+→10` (formula: `(0.10 − var_real) × 25`)
- **Stale:** 365 días (dato anual — se actualiza con el CSV del año siguiente)
- **IPC configurado:** 2024 = 117.06%, 2025 = 38.3% — actualizar `IPC_ANUAL` en `politica.py` cada enero

### `veto_quorum` — Poder de bloqueo por quórum
- **Qué mide:** % de sesiones ordinarias convocadas donde no se alcanzó quórum (129 diputados). Captura la capacidad de la oposición (y/o desorganización del oficialismo) de frustrar la agenda legislativa antes del debate. Complementa `eficacia_legislativa` — esta mide el bloqueo pre-debate; `eficacia_legislativa` mide el resultado del debate.
- **Fuente:** `data/politica/manuales.json` (actas de sesión hcdn.gob.ar + elaboración CIGOB)
- **Cálculo:** # sesiones donde se intentó abrir pero no se llegó a 129 / # sesiones convocadas, período trimestral
- **Unidad:** % (0 a 100)
- **Score:** 0%→0, 15%→5, 30%+→10 (formula: `float(val) / 3.0`)
- **Valor placeholder (actualizar):** 12%
- **Nota metodológica:** incluye frustraciones tanto por acción opositora activa como por inasistencia del propio bloque oficialista — ambas son señales de debilidad del capital legislativo.

### `comisiones_caidas` — Proyectos varados post-dictamen
- **Qué mide:** % de proyectos que obtuvieron dictamen favorable de al menos una comisión pero no fueron incluidos en el orden del día del plenario en el trimestre. Captura el "cementerio post-comisión": proyectos que pasan el filtro técnico pero mueren antes del recinto por falta de voluntad política, negociación trunca o bloqueo de la presidencia de la Cámara.
- **Fuente:** `data/politica/manuales.json` (dictámenes hcdn.gob.ar + elaboración CIGOB)
- **Cálculo:** # proyectos con dictamen no convocados al recinto en el trimestre / # proyectos con dictamen en el período
- **Unidad:** % (0 a 100)
- **Score:** 20%→0, 40%→5, 60%+→10 (formula: `(float(val) - 20.0) / 4.0`)
- **Valor placeholder (actualizar):** 48%
- **Nota metodológica:** un 20–30% es normal (no todo dictamen llega de inmediato); por encima del 50% indica bloqueo sistemático. Distinguir si la caída es por vencimiento de mandato de comisión vs. bloqueo activo.

### `cohesion_bloque` — Cohesión del bloque LLA en Diputados
- **Qué mide:** qué tan unido vota el bloque afín al gobierno en Cámara de Diputados. Dimensión *cohesión interna* de Matus.
- **Fuente:** `data/politica/manuales.json` (HCDn.gob.ar + elaboración CIGOB)
- **Cálculo:** % de votaciones nominales donde diputados LLA votaron alineados con posición oficial (últimos 3 meses)
- **Unidad:** % (0 a 100)
- **Valor placeholder (actualizar):** 78%
- **Datos base:** `https://hcdn.gob.ar/diputados/votaciones/` — filtrar por bloque LLA en votaciones nominales

### `eficacia_legislativa` — Eficacia legislativa del Ejecutivo
- **Qué mide:** proporción de proyectos del Ejecutivo aprobados por el Congreso. Dimensión *poder legislativo* de Matus.
- **Fuente:** `data/politica/manuales.json`
- **Unidad:** % (0 a 100)
- **Valor placeholder (actualizar):** 42%

### `gobernadores_alineamiento` — Alineamiento de gobernadores
- **Qué mide:** soporte territorial y federal del gobierno. Dimensión *alianzas territoriales* de Matus.
- **Fuente:** `data/politica/manuales.json`
- **Cálculo:** % de gobernadores (sobre 24) con posición pública de apoyo al programa nacional
- **Unidad:** % (0 a 100)
- **Valor placeholder (actualizar):** 55%

---

## Fórmula de score (0–10, mayor = mayor tensión política)

```python
# votometro_ventaja_lla (gap pp LLA−PJ): +15pp→0, 0→5, −15pp→10
score_vot  = min(10.0, max(0.0, 5.0 - float(gap) / 3.0))

# ratio_dnu (ratio DNUs/leyes): 0→0, 1.0→5, 2.0+→10
score_dnu  = min(10.0, max(0.0, float(ratio) * 5.0))

# movilizacion_cepa (índice 0–100): 0→0, 50→5, 100→10
score_cepa = min(10.0, max(0.0, float(val) / 10.0))

# iaf_transferencias (% variación real YoY): +10%→0, 0%→2.5, −10%→5, −30%+→10
score_iaf  = min(10.0, max(0.0, (0.10 - float(val)/100.0) * 25.0))

# eficacia_legislativa (% 0–100): 70%→0, 35%→5, 0%→10
score_efic = min(10.0, max(0.0, (70.0 - float(val)) / 7.0))

# cohesion_bloque (% 0–100): 95%→0, 60%→5, 25%→10
score_coh  = min(10.0, max(0.0, (95.0 - float(val)) / 7.0))

# gobernadores_alineamiento (% 0–100): 80%→0, 40%→5, 0%→10
score_gob  = min(10.0, max(0.0, (80.0 - float(val)) / 8.0))

# veto_quorum (% 0–100): 0%→0, 15%→5, 30%+→10
score_veto = min(10.0, max(0.0, float(val) / 3.0))

# comisiones_caidas (% 0–100): 20%→0, 40%→5, 60%+→10
score_com  = min(10.0, max(0.0, (float(val) - 20.0) / 4.0))

score = promedio(scores disponibles)  # equal-weight, ignora indicadores ausentes
```

Umbrales: `0–3` estable | `4–6` en_tension | `7–10` tensionado

**Score actual (may-2026):** 4.7 — en_tension *(8/9 frescos — CEPA falló por 404 en url, usó cache)*

Scores individuales (may-2026):
| Indicador | Valor | Score |
|---|---|---|
| `votometro_ventaja_lla` | +13.3pp (LLA 41.8 / PJ 28.5, n=11) | 0.6 |
| `ratio_dnu` | 3.14 (22 DNUs / 7 leyes período 144) | 10.0 |
| `movilizacion_cepa` | 46.0 (cache — 404 en informes CEPA) | 4.6 |
| `iaf_transferencias` | +1.8% real i.a. | 2.1 |
| `eficacia_legislativa` | 4.8% (1/21 proyectos PE aprobados 12m) | 9.3 |
| `veto_quorum` | 0.0% (0/2 sesiones Diputados período 144 fracasadas) | 0.0 |
| `comisiones_caidas` | 99.6% (519/521 con OD sin sanción — alto estructural) | 10.0 |
| `cohesion_bloque` | 78% (placeholder) | 2.4 |
| `gobernadores_alineamiento` | 55% (placeholder) | 3.1 |

---

## Estructura de datos

```
data/politica/
  manuales.json     ← fallback para cohesion_bloque, gobernadores_alineamiento (los demás son AUTO via CKAN)

scripts/
  politica.py       ← 7 AUTO (votometro, ratio_dnu, movilizacion_cepa, iaf_transferencias, eficacia_legislativa, veto_quorum, comisiones_caidas) + 2 manuales
```

### Formato `manuales.json`

Cada entrada:
```json
{
  "valor": 42,
  "unidad": "% proyectos oficiales aprobados",
  "fuente": "descripción de la fuente",
  "notas": "metodología o aclaraciones",
  "fecha_dato": "YYYY-MM-DD"
}
```

Actualizar `fecha_dato` junto con `valor` en cada ciclo de actualización.

---

## Ejecución y exit codes

```bash
cd projects/informe_coyuntura
python scripts/politica.py
# exit 0 → 6/6 frescos
# exit 1 → al menos 1 fresco (normal si Votómetro no tiene polls recientes)
# exit 2 → ningún fresco (todos desde cache)
```

## Notas de mantenimiento

- **Votómetro desactualizado:** si `votometro_ventaja_lla.desactualizado=true`, agregar encuestas al Votómetro en `projects/votometro/web/votometro.html` → array `encuestasRaw` (campo `tipo:'espacio'`)
- **ratio_dnu falla:** verificar que `servicios.infoleg.gob.ar/infolegInternet/` responde (la sesión requiere GET previo para obtener jsessionid). Si el formulario cambia estructura, actualizar `action_m` regex en `fetch_ratio_dnu()`. El texto "necesidad y urgencia" en el campo `texto` filtra los DNUs dentro de tipo "Decreto"
- **CEPA:** si el scraper falla, revisar que `centrocepa.com.ar/informes` siga publicando links con "conflictividad" en la URL. Si cambia la estructura del texto del informe, ajustar los patrones regex en `fetch_cepa_movilizacion()`
- **IAF transferencias:** el CSV de Hacienda se publica anualmente. Si el año cambia y no hay datos (`sin datos para AAAA`), actualizar `RON_CSV_URL` con el nuevo nombre de archivo. Actualizar `IPC_ANUAL` cada enero con la variación dic-dic INDEC del año que cierra. El CSV usa separador `;` y decimal `,` — si Hacienda cambia el formato, ajustar `fetch_iaf_transferencias()`.
- **Manuales:** actualizar `data/politica/manuales.json` con nuevos valores y `fecha_dato` actualizada en cada ciclo
- **Cohesión:** datos base en `https://hcdn.gob.ar/diputados/votaciones/` — filtrar por bloque LLA en votaciones nominales
- **Veto quórum:** contar sesiones donde se convocó pero no se abrió por falta de quórum. Fuente: actas en `hcdn.gob.ar/sesiones/` o seguimiento de cobertura periodística cuando no hay acta formal. Distinguir sesiones especiales de ordinarias.
- **Comisiones caídas:** listar dictámenes publicados en `hcdn.gob.ar/comisiones/` y cruzar contra orden del día del período. Un dictamen "cae" si vence el período o si pasan 3 meses sin ser convocado.
- **Barbarismo político:** el cinturón deliberadamente no duplica `ipc` ni indicadores de bienestar — esos corresponden al cinturón `vida_cotidiana`. El barbarismo a evitar es medir solo imagen/popularidad ignorando las dimensiones institucionales del capital político. ICG UTDT removido por esta razón.
