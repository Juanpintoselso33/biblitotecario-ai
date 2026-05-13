# Cinturón Macro — Indicadores Activos

Script: `scripts/macro.py` | Cache: `output/cache/macro.json`
Peso en score global: **30%** (`config.py → PESOS_CINTURONES["macro"]`)
Barbarismo de riesgo: **tecnocrático**

Fuente conceptual: Diego Dequino, "Monitor de Sustentabilidad Macroeconómica" (mayo 2026) —
marco en 2 grupos: *agregados macroeconómicos* + *palancas de política económica*.

---

## Indicadores activos (11)

| Nombre | Serie/ID | Fuente | Frecuencia | Estado |
|---|---|---|---|---|
| `ipc_total` | `148.3_INIVELNAL_DICI_M_26` | datos.gob.ar INDEC | Mensual | ✅ activo |
| `reservas_bcra` | Variable BCRA `1` | api.bcra.gob.ar v4.0 | Diario | ✅ activo |
| `badlar` | Variable BCRA `7` | api.bcra.gob.ar v4.0 | Diario | ✅ activo |
| `emae_ia` | `143.3_ICE_SERVIA_2004_A_25` | datos.gob.ar INDEC | Mensual | ✅ activo |
| `saldo_comercial_12m` | `164.3_SOTALTAL_0_0_8` | datos.gob.ar INDEC | Mensual (acum 12m) | ✅ activo |
| `recaudacion` | `172.3_TL_RECAION_M_0_0_17` | datos.gob.ar INDEC | Mensual | ✅ activo |
| `tcrm` | `116.3_TCRMA_0_M_36` | datos.gob.ar INDEC | Mensual | ✅ activo (rezago ~2m) |
| `rem_ipc_12m` | Variable BCRA `29` | api.bcra.gob.ar v4.0 | Mensual | ✅ activo |
| `prestamos_privados` | Variable BCRA `26` | api.bcra.gob.ar v4.0 | Diario | ✅ activo |
| `base_monetaria` | Variable BCRA `15` | api.bcra.gob.ar v4.0 | Diario | ✅ activo |
| `tc_mayorista` | Variable BCRA `5` | api.bcra.gob.ar v4.0 | Diario | ✅ activo |

---

## Descripción por indicador

### `ipc_total` — Inflación mensual (IPC Nacional, INDEC)
- **API:** `GET https://apis.datos.gob.ar/series/api/series/?ids=148.3_INIVELNAL_DICI_M_26&format=json&limit=2&sort=desc`
- **Cálculo:** variación % mensual = (actual / anterior − 1) × 100
- **Unidad:** % mensual
- **Última ejecución exitosa:** 3.38% (mar-2026)

### `reservas_bcra` — Reservas internacionales brutas BCRA
- **API:** `GET https://api.bcra.gob.ar/estadisticas/v4.0/Monetarias/1`
- **Cálculo:** último valor disponible (millones USD). API devuelve datos en orden **descendente**: `detalle[0]` = más reciente.
- **Unidad:** millones USD
- **Última ejecución exitosa:** 46.061 M USD (may-2026)

### `badlar` — Tasa BADLAR bancos privados
- **API:** `GET https://api.bcra.gob.ar/estadisticas/v4.0/Monetarias/7`
- **Cálculo:** último valor disponible (% anual)
- **Unidad:** % anual
- **Última ejecución exitosa:** 20.88% (may-2026)

### `emae_ia` — EMAE variación interanual (INDEC, base 2004)
- **API:** `GET https://apis.datos.gob.ar/series/api/series/?ids=143.3_ICE_SERVIA_2004_A_25&format=json&limit=2&sort=desc`
- **Cálculo:** valor directo en decimal (0.0188 = 1.88% i.a.) × 100
- **Unidad:** % i.a.
- **Interpretación:** caída i.a. → recesión → tensión alta; crecimiento → actividad sana → tensión baja
- **Última ejecución exitosa:** 1.88% (ene-2026)
- **Nota:** series `143.1_*` son anuales; `143.2_*` son trimestrales; `143.3_*` son **mensuales** ✅

### `saldo_comercial_12m` — Balance comercial acumulado 12 meses (INDEC)
- **API:** `GET https://apis.datos.gob.ar/series/api/series/?ids=164.3_SOTALTAL_0_0_8&format=json&limit=13&sort=desc`
- **Cálculo:** suma de los 12 últimos valores mensuales del saldo comercial total
- **Unidad:** millones USD acumulado 12 meses
- **Interpretación:** superávit sostenido → menos tensión externa; déficit → restricción externa
- **Última ejecución exitosa:** +17.125 M USD (12m hasta feb-2025)
- **Nota:** publicación con rezago de ~3 meses. Usa 12m móviles para eliminar estacionalidad energética/sojera.

### `recaudacion` — Recaudación tributaria total (INDEC/AFIP)
- **API:** `GET https://apis.datos.gob.ar/series/api/series/?ids=172.3_TL_RECAION_M_0_0_17&format=json&limit=2&sort=desc`
- **Cálculo:** variación % mensual nominal = (actual / anterior − 1) × 100
- **Unidad:** % var mensual nominal
- **Interpretación:** proxy de actividad económica y consumo. Si var_m nominal < IPC → caída real → tensión fiscal.
- **Última ejecución exitosa:** −0.99% (mar-2026)
- **Nota:** tiene ruido estacional (enero tiene grandes vencimientos). En futuras versiones: usar variación i.a. para eliminar estacionalidad.

### `tcrm` — Tipo de Cambio Real Multilateral (INDEC, base 2010=100)
- **API:** `GET https://apis.datos.gob.ar/series/api/series/?ids=116.3_TCRMA_0_M_36&format=json&limit=2&sort=desc`
- **Cálculo:** último valor índice (base 2010=100)
- **Unidad:** índice base 2010=100
- **Interpretación:** TCRM < 100 = apreciación cambiaria → erosión de competitividad → tensión externa futura. TCRM > 100 = depreciación real → competitividad.
- **Última ejecución exitosa:** 79.77 (dic-2024)
- **Nota:** rezago de ~2-3 meses en INDEC; requiere deflactores de socios comerciales.

### `rem_ipc_12m` — Expectativas de inflación 12 meses (REM BCRA)
- **API:** `GET https://api.bcra.gob.ar/estadisticas/v4.0/Monetarias/29`
- **Cálculo:** mediana de expectativas de variación i.a. del IPC para los próximos 12 meses (% anual)
- **Unidad:** % anual esperado
- **Interpretación:** expectativas bajas → desinflación creíble → tensión baja. Expectativas altas → inflación inercial → tensión alta.
- **Última ejecución exitosa:** 24.2% (abr-2026)

### `prestamos_privados` — Préstamos sector privado (BCRA)
- **API:** `GET https://api.bcra.gob.ar/estadisticas/v4.0/Monetarias/26?desde=YYYY-MM-DD`
- **Cálculo:** variación % mensual nominal (último valor vs valor de hace 30 días)
- **Unidad:** % var mensual nominal
- **Interpretación:** crecimiento superior a IPC → crédito expansivo → menor tensión. Caída real → contracción crediticia → tensión financiera.
- **Última ejecución exitosa:** +2.63% (may-2026)

### `base_monetaria` — Base monetaria (BCRA)
- **API:** `GET https://api.bcra.gob.ar/estadisticas/v4.0/Monetarias/15?desde=YYYY-MM-DD`
- **Cálculo:** variación % mensual nominal (último vs hace 30 días)
- **Unidad:** % var mensual nominal
- **Interpretación:** expansión muy rápida vs IPC → riesgo inflacionario. Contracción → ajuste monetario.
- **Última ejecución exitosa:** −1.25% (may-2026)

### `tc_mayorista` — Tipo de cambio mayorista de referencia (BCRA)
- **API:** `GET https://api.bcra.gob.ar/estadisticas/v4.0/Monetarias/5?desde=YYYY-MM-DD`
- **Cálculo:** variación % mensual (último vs hace 30 días)
- **Unidad:** % var mensual
- **Interpretación:** salto mensual grande → devaluación abrupta → tensión cambiaria. Var% baja y estable → crawling peg controlado.
- **Última ejecución exitosa:** +2.06% (may-2026)

---

## Fórmula de score (0–10, mayor = mayor tensión macro)

```python
# ipc_total: 0%→0, 5%→5, 10%→10
score_ipc = min(10.0, max(0.0, float(ipc)))

# reservas_bcra: ≥40000→0, 20000→5, 0→10
score_res = min(10.0, max(0.0, (40000.0 - float(reservas)) / 4000.0))

# badlar: 0%→0, 50%→5, 100%→10
score_badlar = min(10.0, max(0.0, float(badlar) / 10.0))

# emae_ia: +5%→0, 0%→5, -5%→10
score_emae = min(10.0, max(0.0, 5.0 - float(emae)))

# saldo_comercial_12m (M USD acum): +6000→0, 0→5, -6000→10
score_sc = min(10.0, max(0.0, 5.0 - float(saldo) / 1200.0))

# recaudacion (% var_m nominal): +5%→0, 0%→5, -5%→10
score_rec = min(10.0, max(0.0, 5.0 - float(recaudacion)))

# tcrm (índice base 2010=100): 100→0, 75→5, 50→10
score_tcrm = min(10.0, max(0.0, (100.0 - float(tcrm)) / 5.0))

# rem_ipc_12m (% anual): 10%→0, 55%→5, 100%→9
score_rem = min(10.0, max(0.0, (float(rem) - 10.0) / 9.0))

# prestamos_privados (% var_m nominal): +5%→0, 0%→5, -5%→10
score_prest = min(10.0, max(0.0, 5.0 - float(prestamos)))

# base_monetaria (% var_m nominal): 0%→0, 10%→5, 20%→10
score_bm = min(10.0, max(0.0, float(base_mon) / 2.0))

# tc_mayorista (% var_m): 0%→0, 10%→5, 20%→10
score_tc = min(10.0, max(0.0, float(tc_mayor) / 2.0))

score = promedio(scores disponibles)  # equal-weight, ignora indicadores ausentes
```

Umbrales: `0–3` estable | `4–6` en_tension | `7–10` tensionado

**Score actual (may-2026):** 2.1 — estable

Scores individuales estimados (may-2026):
| Indicador | Valor | Score |
|---|---|---|
| `ipc_total` | 3.38% | 3.4 |
| `reservas_bcra` | 46.061 M | 0.0 |
| `badlar` | 20.88% | 2.1 |
| `emae_ia` | 1.88% | 3.1 |
| `saldo_comercial_12m` | +17.125 M | 0.0 |
| `recaudacion` | −0.99% | 6.0 |
| `tcrm` | 79.77 | 4.1 |
| `rem_ipc_12m` | 24.2% | 1.6 |
| `prestamos_privados` | +2.63% | 2.4 |
| `base_monetaria` | −1.25% | 0.0 |
| `tc_mayorista` | +2.06% | 1.0 |

---

## Ejecución y exit codes

```bash
cd projects/informe_coyuntura
python scripts/macro.py
# exit 0 → todos los indicadores frescos (11/11)
# exit 1 → al menos 1 fresco (algunos fallaron → usó cache)
# exit 2 → ningún indicador fresco (todo desde cache)
```

## Notas de mantenimiento

- **BCRA API SSL:** requiere `verify=False` + `urllib3.disable_warnings()` — ya implementado
- **BCRA datos en orden descendente:** `detalle[0]` = más reciente (NO usar `detalle[-1]`)
- **EMAE frecuencias:** prefijo `143.3_*` = mensual | `143.2_*` = trimestral | `143.1_*` = anual
- **Saldo comercial:** rezago de ~3 meses; acumulado 12m reduce estacionalidad sojera/energética
- **TCRM:** rezago de ~2-3 meses en INDEC; requiere deflactores de socios comerciales para calcularlo
- **Recaudación:** ruido estacional (enero siempre alto por vencimientos). Considerar pasar a variación i.a. en futura versión.
- Si INDEC reasigna alguna serie: buscar en `https://apis.datos.gob.ar/series/api/search/?q=<nombre>&limit=5&format=json`
- Si BCRA cambia versión de API (v4.0 → v5.0): actualizar `BCRA_VARIABLES_BASE` en `macro.py`
