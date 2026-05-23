# Cinturón Macro — Indicadores Activos

Script: `scripts/macro.py` | Cache: `output/cache/macro.json`
Peso en score global: **30%** (`config.py → PESOS_CINTURONES["macro"]`)
Barbarismo de riesgo: **tecnocrático**

Fuente conceptual: Diego Dequino, "Monitor de Sustentabilidad Macroeconómica" (mayo 2026) —
marco en 2 grupos: *agregados macroeconómicos* + *palancas de política económica*.

---

## Indicadores activos (11)

| Nombre | Qué mide | Fuente | Frecuencia | Estado |
|---|---|---|---|---|
| `ipc_total` | Inflación mensual del IPC nacional | INDEC | Mensual | ✅ activo |
| `reservas_bcra` | Reservas internacionales brutas del BCRA (M USD) | BCRA | Diario | ✅ activo |
| `badlar` | Tasa de interés para depósitos bancarios mayoristas (% anual) | BCRA | Diario | ✅ activo |
| `emae_ia` | Variación interanual de la actividad económica general | INDEC | Mensual | ✅ activo |
| `saldo_comercial_12m` | Balance exportaciones − importaciones acumulado 12 meses (M USD) | INDEC | Mensual | ✅ activo |
| `recaudacion` | Variación mensual de la recaudación tributaria total | INDEC/AFIP | Mensual | ✅ activo |
| `tcrm` | Tipo de cambio real multilateral frente a socios comerciales (base 2010=100) | INDEC | Mensual | ✅ activo |
| `rem_ipc_12m` | Expectativas de inflación del mercado para los próximos 12 meses (mediana REM) | BCRA | Mensual | ✅ activo |
| `prestamos_privados` | Variación mensual del crédito bancario al sector privado | BCRA | Diario | ✅ activo |
| `base_monetaria` | Variación mensual de la base monetaria (billetes + reservas bancarias) | BCRA | Diario | ✅ activo |
| `tc_mayorista` | Variación mensual del tipo de cambio oficial mayorista (crawling peg) | BCRA | Diario | ✅ activo |

---

## Descripción por indicador

### `ipc_total` — Inflación mensual (IPC Nacional, INDEC)
- **Qué mide:** cuánto subieron los precios al consumidor en el último mes. Es el termómetro más directo del bienestar de la población y del ancla nominal del programa económico.
- **API:** `GET https://apis.datos.gob.ar/series/api/series/?ids=148.3_INIVELNAL_DICI_M_26&format=json&limit=2&sort=desc`
- **Cálculo:** variación % mensual = (actual / anterior − 1) × 100
- **Unidad:** % mensual
- **Última ejecución exitosa:** 3.38% (mar-2026)

### `reservas_bcra` — Reservas internacionales brutas BCRA
- **Qué mide:** el stock de dólares y activos líquidos del Banco Central. Es el respaldo del sistema financiero y el indicador más sensible de vulnerabilidad externa: si caen, sube la presión cambiaria.
- **API:** `GET https://api.bcra.gob.ar/estadisticas/v4.0/Monetarias/1`
- **Cálculo:** último valor disponible (millones USD). API devuelve datos en orden **descendente**: `detalle[0]` = más reciente.
- **Unidad:** millones USD
- **Última ejecución exitosa:** 46.061 M USD (may-2026)

### `badlar` — Tasa BADLAR bancos privados
- **Qué mide:** el costo del dinero en el sistema bancario para depósitos mayoristas (más de $1M). Cuando la BADLAR sube mucho, el crédito se encarece y la actividad se frena; cuando cae, señala relajamiento monetario.
- **API:** `GET https://api.bcra.gob.ar/estadisticas/v4.0/Monetarias/7`
- **Cálculo:** último valor disponible (% anual)
- **Unidad:** % anual
- **Última ejecución exitosa:** 20.88% (may-2026)

### `emae_ia` — EMAE variación interanual (INDEC, base 2004)
- **Qué mide:** si la economía argentina creció o cayó respecto al mismo mes del año anterior. El indicador adelantado del PBI mensual: una caída sostenida es recesión, un rebote señala recuperación.
- **API:** `GET https://apis.datos.gob.ar/series/api/series/?ids=143.3_ICE_SERVIA_2004_A_25&format=json&limit=2&sort=desc`
- **Cálculo:** valor directo en decimal (0.0188 = 1.88% i.a.) × 100
- **Unidad:** % i.a.
- **Interpretación:** caída i.a. → recesión → tensión alta; crecimiento → actividad sana → tensión baja
- **Última ejecución exitosa:** 1.88% (ene-2026)
- **Nota:** series `143.1_*` son anuales; `143.2_*` son trimestrales; `143.3_*` son **mensuales** ✅

### `saldo_comercial_12m` — Balance comercial acumulado 12 meses (INDEC)
- **Qué mide:** la diferencia entre lo que exporta e importa Argentina en los últimos 12 meses. Superávit sostenido = el país genera dólares propios; déficit = depende de financiamiento externo y presiona el tipo de cambio.
- **API:** `GET https://apis.datos.gob.ar/series/api/series/?ids=164.3_SOTALTAL_0_0_8&format=json&limit=13&sort=desc`
- **Cálculo:** suma de los 12 últimos valores mensuales del saldo comercial total
- **Unidad:** millones USD acumulado 12 meses
- **Interpretación:** superávit sostenido → menos tensión externa; déficit → restricción externa
- **Última ejecución exitosa:** +17.125 M USD (12m hasta feb-2025)
- **Nota:** publicación con rezago de ~3 meses. Usa 12m móviles para eliminar estacionalidad energética/sojera.

### `recaudacion` — Recaudación tributaria total (INDEC/AFIP)
- **Qué mide:** cuánto recaudó el Estado en el mes (IVA, Ganancias, aportes, etc.). Es un proxy de la actividad económica real: si cae en términos reales (menos que la inflación), hay deterioro fiscal o caída de consumo.
- **API:** `GET https://apis.datos.gob.ar/series/api/series/?ids=172.3_TL_RECAION_M_0_0_17&format=json&limit=2&sort=desc`
- **Cálculo:** variación % mensual nominal = (actual / anterior − 1) × 100
- **Unidad:** % var mensual nominal
- **Interpretación:** proxy de actividad económica y consumo. Si var_m nominal < IPC → caída real → tensión fiscal.
- **Última ejecución exitosa:** −0.99% (mar-2026)
- **Nota:** tiene ruido estacional (enero tiene grandes vencimientos). En futuras versiones: usar variación i.a. para eliminar estacionalidad.

### `tcrm` — Tipo de Cambio Real Multilateral (INDEC, base 2010=100)
- **Qué mide:** qué tan competitivos son los precios argentinos frente a los socios comerciales, ajustando por inflación de ambos lados. Por debajo de 100 = Argentina está cara en dólares; por encima = competitiva. Es la foto de la brecha cambiaria estructural.
- **API:** `GET https://apis.datos.gob.ar/series/api/series/?ids=116.3_TCRMA_0_M_36&format=json&limit=2&sort=desc`
- **Cálculo:** último valor índice (base 2010=100)
- **Unidad:** índice base 2010=100
- **Interpretación:** TCRM < 100 = apreciación cambiaria → erosión de competitividad → tensión externa futura. TCRM > 100 = depreciación real → competitividad.
- **Última ejecución exitosa:** 79.77 (dic-2024)
- **Nota:** rezago de ~2-3 meses en INDEC; requiere deflactores de socios comerciales.

### `rem_ipc_12m` — Expectativas de inflación 12 meses (REM BCRA)
- **Qué mide:** cuánta inflación esperan los economistas del mercado para el próximo año. Si las expectativas son altas, la inflación tiene inercia y el programa desinflacionario pierde credibilidad; si bajan, el ancla funciona.
- **API:** `GET https://api.bcra.gob.ar/estadisticas/v4.0/Monetarias/29`
- **Cálculo:** mediana de expectativas de variación i.a. del IPC para los próximos 12 meses (% anual)
- **Unidad:** % anual esperado
- **Interpretación:** expectativas bajas → desinflación creíble → tensión baja. Expectativas altas → inflación inercial → tensión alta.
- **Última ejecución exitosa:** 24.2% (abr-2026)

### `prestamos_privados` — Préstamos sector privado (BCRA)
- **Qué mide:** si los bancos están prestando más o menos al sector productivo y a las familias. El crédito privado creciendo por encima de la inflación señala expansión económica; cayendo en términos reales, contracción financiera.
- **API:** `GET https://api.bcra.gob.ar/estadisticas/v4.0/Monetarias/26?desde=YYYY-MM-DD`
- **Cálculo:** variación % mensual nominal (último valor vs valor de hace 30 días)
- **Unidad:** % var mensual nominal
- **Interpretación:** crecimiento superior a IPC → crédito expansivo → menor tensión. Caída real → contracción crediticia → tensión financiera.
- **Última ejecución exitosa:** +2.63% (may-2026)

### `base_monetaria` — Base monetaria (BCRA)
- **Qué mide:** la cantidad de pesos en circulación más las reservas que los bancos tienen en el BCRA. Es la "materia prima" de la inflación: si crece mucho más rápido que la economía, hay riesgo de emisión descontrolada.
- **API:** `GET https://api.bcra.gob.ar/estadisticas/v4.0/Monetarias/15?desde=YYYY-MM-DD`
- **Cálculo:** variación % mensual nominal (último vs hace 30 días)
- **Unidad:** % var mensual nominal
- **Interpretación:** expansión muy rápida vs IPC → riesgo inflacionario. Contracción → ajuste monetario.
- **Última ejecución exitosa:** −1.25% (may-2026)

### `tc_mayorista` — Tipo de cambio mayorista de referencia (BCRA)
- **Qué mide:** el precio oficial del dólar para el comercio exterior. Su variación mensual indica si el gobierno mantiene el crawling peg (devaluación gradual) o si hubo un salto cambiario abrupto.
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

**Score actual (may-2026):** 2.1 — estable (11/11 indicadores frescos)

Scores individuales (may-2026):
| Indicador | Valor | Score |
|---|---|---|
| `ipc_total` | 3.38% | 3.4 |
| `reservas_bcra` | 46.585 M USD | 0.0 |
| `badlar` | 22.0% | 2.2 |
| `emae_ia` | 1.88% i.a. | 3.1 |
| `saldo_comercial_12m` | +17.125 M USD | 0.0 |
| `recaudacion` | −0.99% var m | 6.0 |
| `tcrm` | 79.77 (base 2010=100) | 4.1 |
| `rem_ipc_12m` | 24.2% anual | 1.6 |
| `prestamos_privados` | +2.13% var m | 2.9 |
| `base_monetaria` | +0.7% var m | 0.0 |
| `tc_mayorista` | −0.27% var m | 0.0 |

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
