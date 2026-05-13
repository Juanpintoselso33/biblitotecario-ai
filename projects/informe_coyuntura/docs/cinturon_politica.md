# Cinturón Político — Indicadores Activos

Script: `scripts/politica.py` | Cache: `output/cache/politica.json`
Peso en score global: **30%** (`config.py → PESOS_CINTURONES["politica"]`)
Barbarismo de riesgo: **político**

---

## Indicadores activos

| Nombre | Serie/ID | Fuente | Frecuencia | Estado |
|---|---|---|---|---|
| `ipc_regulados` | `148.3_IREGULANAL_DICI_M_22` + `148.3_INIVELNAL_DICI_M_26` | datos.gob.ar INDEC | Mensual | ✅ activo |
| `icg_utdt` | Scraping XLS página 16457 | utdt.edu | Mensual | ⚠️ falla graceful (sin XLS en la página) |

### `ipc_regulados` — IPC Regulados (tarifas servicios públicos)
- **API regulados:** `GET https://apis.datos.gob.ar/series/api/series/?ids=148.3_IREGULANAL_DICI_M_22&format=json&limit=2&sort=desc`
- **API total (referencia):** `GET https://apis.datos.gob.ar/series/api/series/?ids=148.3_INIVELNAL_DICI_M_26&format=json&limit=2&sort=desc`
- **Cálculo:** var% mensual del índice regulados + brecha = regulados − total
- **Interpretación:** brecha positiva = gobierno habilitó ajuste de tarifas → mayor tensión política
- **Unidad:** % mensual | brecha en pp
- **Última ejecución exitosa:** 5.08% m/m, brecha +1.70pp (mar-2026)

### `icg_utdt` — Índice de Confianza en el Gobierno (UTDT)
- **URL listado:** `https://www.utdt.edu/listado_contenidos.php?id_item_menu=16457`
- **Estado actual:** la página 16457 no tiene XLS descargable disponible → falla gracefully
- **Cuando funcione:** requiere librería `xlrd`. Busca links `download.php?fname=*.xls` en la página
- **Interpretación:** menor ICG → mayor tensión política. ICG ~40 → score 0; ICG <10 → score 10

---

## Fórmula de score (0–10, mayor = mayor tensión)

```python
# ipc_regulados: var% 0 → 0, 10% → 10. Bonus si brecha > 0 (hasta +3)
base  = min(10.0, max(0.0, ipc_regulados_val))
bonus = min(3.0, max(-3.0, brecha * 0.3))
score_regulados = min(10.0, max(0.0, base + bonus))

# icg_utdt: (40 - ICG) / 4  → ICG=40 → score 0, ICG=0 → score 10
score_icg = min(10.0, max(0.0, (40.0 - icg) / 4.0))

score = promedio(scores disponibles)
```

Umbrales: `0–3` estable | `4–6` en_tension | `7–10` tensionado

---

## Ejecución y exit codes

```bash
cd projects/informe_coyuntura
python scripts/politica.py
# exit 0 → ipc_regulados + icg_utdt frescos
# exit 1 → solo ipc_regulados fresco (ICG falló — ESTADO NORMAL ACTUAL)
# exit 2 → ningún fresco
```

**Exit 1 es el resultado esperado** mientras la página 16457 de UTDT no tenga XLS.

## Notas de mantenimiento

- Si UTDT publica el XLS en la página 16457, instalar `xlrd` (`pip install xlrd`) y el scraping funciona automáticamente
- Diferencia entre ICC (16458, confianza consumidor) e ICG (16457, confianza gobierno): este script usa **ICG**
- Si INDEC reasigna la serie de regulados: buscar en datos.gob.ar con `q=IPC+regulados`
