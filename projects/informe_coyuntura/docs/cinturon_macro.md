# Cinturón Macro — Indicadores Activos

Script: `scripts/macro.py` | Cache: `output/cache/macro.json`
Peso en score global: **30%** (`config.py → PESOS_CINTURONES["macro"]`)
Barbarismo de riesgo: **tecnocrático**

---

## Indicadores activos

| Nombre | Serie/ID | Fuente | Frecuencia | Estado |
|---|---|---|---|---|
| `ipc_total` | `148.3_INIVELNAL_DICI_M_26` | datos.gob.ar INDEC | Mensual | ✅ activo |
| `reservas_bcra` | Variable `1` | api.bcra.gob.ar v4.0 | Diario | ✅ activo |
| `badlar` | Variable `7` | api.bcra.gob.ar v4.0 | Diario | ✅ activo |

### `ipc_total` — Inflación mensual (IPC Nacional)
- **API:** `GET https://apis.datos.gob.ar/series/api/series/?ids=148.3_INIVELNAL_DICI_M_26&format=json&limit=2&sort=desc`
- **Cálculo:** variación % mensual = (actual / anterior - 1) × 100
- **Unidad:** % mensual
- **Última ejecución exitosa:** 3.38% (mar-2026)

### `reservas_bcra` — Reservas internacionales BCRA
- **API:** `GET https://api.bcra.gob.ar/estadisticas/v4.0/Monetarias/1`
- **Cálculo:** último valor disponible (millones USD)
- **Unidad:** millones USD
- **Última ejecución exitosa:** 46.061 mill USD (may-2026)

### `badlar` — Tasa BADLAR bancos privados
- **API:** `GET https://api.bcra.gob.ar/estadisticas/v4.0/Monetarias/7`
- **Cálculo:** último valor disponible (% anual)
- **Unidad:** % anual
- **Última ejecución exitosa:** 20.88% (may-2026)

---

## Fórmula de score (0–10, mayor = mayor tensión)

```python
# ipc_total: 0% → 0, 10% → 10
score_ipc = min(10.0, max(0.0, ipc_val * 0.8))

# reservas: < 20.000 → tensionado, > 50.000 → estable
score_reservas = min(10.0, max(0.0, (50_000 - reservas) / 5_000))

# badlar: 0% → 0, 100% → 10
score_badlar = min(10.0, max(0.0, badlar / 10.0))

score = promedio(scores disponibles)
```

Umbrales: `0–3` estable | `4–6` en_tension | `7–10` tensionado

---

## Ejecución y exit codes

```bash
cd projects/informe_coyuntura
python scripts/macro.py
# exit 0 → todos los indicadores frescos
# exit 1 → al menos 1 fresco (1 o 2 de 3)
# exit 2 → ningún indicador fresco (solo cache)
```

## Notas de mantenimiento

- Si BCRA cambia versión de API (v4.0 → v5.0), actualizar `BCRA_VARIABLES_BASE` en `macro.py`
- Si INDEC reasigna series, buscar nueva ID en `https://apis.datos.gob.ar/series/api/search/?q=IPC+total+nacional&limit=5&format=json`
- El IPC publica ~primer mes posterior; si el dato es de hace 2+ meses, puede estar desactualizado
