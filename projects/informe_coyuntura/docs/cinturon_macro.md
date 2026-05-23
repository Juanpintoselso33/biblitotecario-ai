# Cinturón Macro

| Campo | Valor |
|---|---|
| Script | `scripts/macro.py` |
| Cache | `output/cache/macro.json` |
| Peso en score global | 30% |
| Barbarismo de riesgo | tecnocrático |

## Encuadre

Marco conceptual: Diego Dequino, *Monitor de Sustentabilidad Macroeconómica* (mayo 2026). Organiza los indicadores en dos grupos: agregados macroeconómicos y palancas de política económica.

Cada indicador produce un score 0–10 donde mayor implica mayor tensión macro. El score del cinturón es el promedio de los indicadores disponibles, ignorando ausencias.

Umbrales: 0–3 estable, 4–6 en tensión, 7–10 tensionado.

## Indicadores activos

| Indicador | Qué mide | Fuente | Frecuencia | Estado |
|---|---|---|---|---|
| `ipc_total` | Inflación mensual del IPC nacional | INDEC | Mensual | Automático |
| `reservas_bcra` | Reservas internacionales brutas del BCRA (M USD) | BCRA | Diaria | Automático |
| `badlar` | Tasa para depósitos bancarios mayoristas (% anual) | BCRA | Diaria | Automático |
| `emae_ia` | Variación interanual de la actividad económica | INDEC | Mensual | Automático |
| `saldo_comercial_12m` | Balance exportaciones − importaciones acumulado 12m (M USD) | INDEC | Mensual | Automático |
| `recaudacion` | Variación mensual de la recaudación tributaria total | INDEC/AFIP | Mensual | Automático |
| `tcrm` | Tipo de cambio real multilateral (base 2010=100) | INDEC | Mensual | Automático |
| `rem_ipc_12m` | Expectativas de inflación a 12 meses (mediana REM) | BCRA | Mensual | Automático |
| `prestamos_privados` | Variación mensual del crédito bancario al sector privado | BCRA | Diaria | Automático |
| `base_monetaria` | Variación mensual de la base monetaria | BCRA | Diaria | Automático |
| `tc_mayorista` | Variación mensual del tipo de cambio oficial mayorista | BCRA | Diaria | Automático |

Score actual del cinturón: **2.1 (estable)**. Última ejecución: 23 de mayo de 2026, 11 de 11 indicadores frescos.

## Detalle por indicador

### `ipc_total` — Inflación mensual

- Fuente: `GET https://apis.datos.gob.ar/series/api/series/?ids=148.3_INIVELNAL_DICI_M_26&format=json&limit=2&sort=desc`
- Cálculo: variación porcentual mensual = `(actual / anterior − 1) × 100`.
- Score: lineal. 0% equivale a score 0; 10% equivale a score 10.
- Último valor: 3.38% (marzo 2026).

### `reservas_bcra` — Reservas internacionales brutas

- Fuente: `GET https://api.bcra.gob.ar/estadisticas/v4.0/Monetarias/1`
- Cálculo: último valor disponible en millones USD. La API devuelve datos en orden descendente; `detalle[0]` es el dato más reciente.
- Score: ≥40.000 equivale a 0; 20.000 equivale a 5; 0 equivale a 10.
- Último valor: 46.585 millones USD (mayo 2026).

### `badlar` — Tasa BADLAR bancos privados

- Fuente: `GET https://api.bcra.gob.ar/estadisticas/v4.0/Monetarias/7`
- Cálculo: último valor disponible (porcentaje anual).
- Score: 0% equivale a 0; 50% equivale a 5; 100% equivale a 10.
- Último valor: 22.0% (mayo 2026).

### `emae_ia` — EMAE variación interanual

- Fuente: `GET https://apis.datos.gob.ar/series/api/series/?ids=143.3_ICE_SERVIA_2004_A_25&format=json&limit=2&sort=desc`
- Cálculo: valor directo en decimal multiplicado por 100. Por ejemplo, 0.0188 equivale a 1.88% i.a.
- Score: +5% equivale a 0; 0% equivale a 5; −5% equivale a 10.
- Nota técnica: las series `143.1_*` son anuales, `143.2_*` son trimestrales, `143.3_*` son mensuales.
- Último valor: +1.88% i.a. (enero 2026).

### `saldo_comercial_12m` — Balance comercial acumulado 12 meses

- Fuente: `GET https://apis.datos.gob.ar/series/api/series/?ids=164.3_SOTALTAL_0_0_8&format=json&limit=13&sort=desc`
- Cálculo: suma de los 12 últimos valores mensuales del saldo comercial total.
- Score: +6000 equivale a 0; 0 equivale a 5; −6000 equivale a 10.
- Nota: la publicación tiene rezago de aproximadamente 3 meses. El acumulado 12 meses elimina estacionalidad energética y sojera.
- Último valor: +17.125 millones USD (12 meses hasta febrero 2025).

### `recaudacion` — Recaudación tributaria total

- Fuente: `GET https://apis.datos.gob.ar/series/api/series/?ids=172.3_TL_RECAION_M_0_0_17&format=json&limit=2&sort=desc`
- Cálculo: variación porcentual mensual nominal.
- Score: +5% equivale a 0; 0% equivale a 5; −5% equivale a 10.
- Nota: tiene ruido estacional (enero presenta grandes vencimientos). Considerar migrar a variación interanual en futura versión.
- Último valor: −0.99% var. m (marzo 2026).

### `tcrm` — Tipo de cambio real multilateral

- Fuente: `GET https://apis.datos.gob.ar/series/api/series/?ids=116.3_TCRMA_0_M_36&format=json&limit=2&sort=desc`
- Cálculo: último valor índice (base 2010=100).
- Score: 100 equivale a 0; 75 equivale a 5; 50 equivale a 10.
- Nota: rezago de 2-3 meses en INDEC.
- Último valor: 79.77 (diciembre 2024).

### `rem_ipc_12m` — Expectativas de inflación a 12 meses

- Fuente: `GET https://api.bcra.gob.ar/estadisticas/v4.0/Monetarias/29`
- Cálculo: mediana de expectativas de variación interanual del IPC a 12 meses (porcentaje anual).
- Score: 10% equivale a 0; 55% equivale a 5; 100% equivale a 9.
- Último valor: 24.2% anual (abril 2026).

### `prestamos_privados` — Préstamos sector privado

- Fuente: `GET https://api.bcra.gob.ar/estadisticas/v4.0/Monetarias/26?desde=YYYY-MM-DD`
- Cálculo: variación porcentual mensual nominal (último valor vs. valor de hace 30 días).
- Score: +5% equivale a 0; 0% equivale a 5; −5% equivale a 10.
- Último valor: +2.13% var. m (mayo 2026).

### `base_monetaria` — Base monetaria

- Fuente: `GET https://api.bcra.gob.ar/estadisticas/v4.0/Monetarias/15?desde=YYYY-MM-DD`
- Cálculo: variación porcentual mensual nominal.
- Score: 0% equivale a 0; 10% equivale a 5; 20% equivale a 10.
- Último valor: +0.7% var. m (mayo 2026).

### `tc_mayorista` — Tipo de cambio mayorista

- Fuente: `GET https://api.bcra.gob.ar/estadisticas/v4.0/Monetarias/5?desde=YYYY-MM-DD`
- Cálculo: variación porcentual mensual.
- Score: 0% equivale a 0; 10% equivale a 5; 20% equivale a 10.
- Último valor: −0.27% var. m (mayo 2026).

## Ejecución

```bash
cd projects/informe_coyuntura
python scripts/macro.py
```

Códigos de salida:

| Código | Significado |
|---|---|
| 0 | Todos los indicadores frescos (11/11) |
| 1 | Al menos uno fresco (algunos fallaron, usó cache) |
| 2 | Ningún indicador fresco (todo desde cache) |

## Notas de mantenimiento

- El BCRA requiere `verify=False` y `urllib3.disable_warnings()` por la configuración SSL del servidor.
- Los datos del BCRA vienen en orden descendente: `detalle[0]` es el dato más reciente; no usar `detalle[-1]`.
- Para series INDEC, los prefijos indican frecuencia: `143.3_*` mensual, `143.2_*` trimestral, `143.1_*` anual.
- Si INDEC reasigna alguna serie, buscar en `https://apis.datos.gob.ar/series/api/search/?q=<nombre>&limit=5&format=json`.
- Si BCRA migra la versión de la API (v4.0 a v5.0), actualizar `BCRA_VARIABLES_BASE` en `macro.py`.
