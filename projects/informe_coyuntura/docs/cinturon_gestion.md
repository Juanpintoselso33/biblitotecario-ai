# Cinturón Gestión — Indicadores Activos

Script: `scripts/gestion.py` | Cache: `output/cache/gestion.json`
Peso en score global: **20%** (`config.py → PESOS_CINTURONES["gestion"]`)
Barbarismo de riesgo: **gerencial**

---

## Indicadores activos

| Nombre | Serie/ID | Fuente | Frecuencia | Estado |
|---|---|---|---|---|
| `indice_salarios_publico` | `149.1_SOR_PUBICO_OCTU_0_14` | datos.gob.ar INDEC | Mensual | ✅ activo |
| `isac_construccion` | `33.4_ISAC_CEMENAND_0_0_21_24` | datos.gob.ar INDEC | Mensual | ✅ activo |

### `indice_salarios_publico` — Índice de Salarios Sector Público (INDEC)
- **API:** `GET https://apis.datos.gob.ar/series/api/series/?ids=149.1_SOR_PUBICO_OCTU_0_14&format=json&limit=2&sort=desc`
- **Base:** octubre 2016 = 100
- **Cálculo:** variación % mensual = (actual / anterior - 1) × 100
- **Unidad:** % var. mensual
- **Interpretación:** var% muy baja o negativa → salarios públicos reales caen → tensión laboral y de gestión alta
- **Última ejecución exitosa:** +1.81% (ene-2026)

### `isac_construccion` — ISAC Insumos Cemento (INDEC)
- **API:** `GET https://apis.datos.gob.ar/series/api/series/?ids=33.4_ISAC_CEMENAND_0_0_21_24&format=json&limit=2&sort=desc`
- **Cálculo:** variación % mensual = (actual / anterior - 1) × 100
- **Unidad:** % var. mensual
- **Interpretación:** proxy de actividad en construcción pública e inversión del Estado. Caída sostenida = obras paralizadas → alta tensión de gestión
- **Última ejecución exitosa:** -3.83% (feb-2026)

---

## Fórmula de score (0–10, mayor = mayor tensión en capacidad de gestión)

```python
# indice_salarios_publico:
# var%=0 → score=5, var%=-5 → score~6.7, var%=+15 → score=0 (catch-up nominal, poca tensión)
score_sal = min(10.0, max(0.0, 5.0 - sal / 3.0))

# isac_construccion:
# var%=0 → score=5, var%=-30 → score=10, var%=+30 → score=0
score_isac = min(10.0, max(0.0, 5.0 - isac / 6.0))

score = promedio(scores disponibles)
```

Umbrales: `0–3` estable | `4–6` en_tension | `7–10` tensionado

**Score actual estimado:** 5.0 con IS=+1.81% (score≈4.4) y ISAC=-3.83% (score≈5.6)

---

## Ejecución y exit codes

```bash
cd projects/informe_coyuntura
python scripts/gestion.py
# exit 0 → indice_salarios_publico + isac_construccion frescos
# exit 1 → solo 1 de 2 frescos
# exit 2 → ningún indicador fresco
```

## Notas de mantenimiento

- Si INDEC reasigna la serie de salarios públicos: buscar en `https://apis.datos.gob.ar/series/api/search/?q=indice+salarios+publico&limit=5&format=json`
- Si INDEC reasigna la serie ISAC: buscar con `q=ISAC+cemento`
- El IS sector público publica con rezago de ~2 meses; fechas de datos pueden estar desactualizadas
- Score alto en salarios + score alto en ISAC = tensión gerencial estructural (doble señal: Estado sin capacidad fiscal ni de inversión)
