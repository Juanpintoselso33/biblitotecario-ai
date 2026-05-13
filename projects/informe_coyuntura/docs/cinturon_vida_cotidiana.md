# Cinturón Vida Cotidiana — Indicadores Activos

Script: `scripts/vida_cotidiana.py` | Cache: `output/cache/vida_cotidiana.json`
Peso en score global: **20%** (`config.py → PESOS_CINTURONES["vida_cotidiana"]`)
Barbarismo de riesgo: **político**

---

## Indicadores activos

| Nombre | Serie/ID | Fuente | Frecuencia | Estado |
|---|---|---|---|---|
| `ipc_total` | `148.3_INIVELNAL_DICI_M_26` | datos.gob.ar INDEC | Mensual | ✅ activo |
| `desocupacion` | EPH INDEC | datos.gob.ar INDEC | Trimestral | ✅ activo |
| `icc_utdt` | Scraping XLS página 16458 | utdt.edu | Mensual | ⚠️ variable (depende de disponibilidad del XLS) |

### `ipc_total` — Inflación mensual (IPC Nacional)
- **API:** `GET https://apis.datos.gob.ar/series/api/series/?ids=148.3_INIVELNAL_DICI_M_26&format=json&limit=2&sort=desc`
- **Cálculo:** variación % mensual = (actual / anterior - 1) × 100
- **Unidad:** % mensual
- **Última ejecución exitosa:** 3.38% (mar-2026)
- **Nota:** misma serie que cinturón macro — comparten la API pero score se calcula independientemente

### `desocupacion` — Tasa de Desocupación (EPH INDEC)
- **Fuente:** INDEC EPH via datos.gob.ar
- **Colector:** `scripts/vida_cotidiana/collectors/indec_series.py` → función `fetch_indec()`
- **Unidad:** %
- **Frecuencia:** trimestral → puede mostrarse desactualizado entre publicaciones EPH
- **Última ejecución exitosa:** 0.1% (dato anómalo — verificar contra publicación EPH oficial)

### `icc_utdt` — Índice de Confianza del Consumidor (UTDT)
- **URL listado:** `https://www.utdt.edu/listado_contenidos.php?id_item_menu=16458`
- **⚠️ IMPORTANTE:** Página **16458** = ICC (Confianza **Consumidor**). NO confundir con 16457 = ICG (Confianza Gobierno, usado por `politica.py`).
- **Cuando funcione:** busca links `download.php?fname=*.xls` en la página; requiere librería `xlrd`
- **Interpretación:** ICC ~42 → score ~6 | ICC >60 → score 0 | ICC <30 → score 10
- **Última ejecución exitosa:** 38.1 (índice)
- **Colector:** `scripts/vida_cotidiana/collectors/utdt_icc.py`

---

## Fórmula de score (0–10, mayor = peor condición de vida cotidiana)

```python
# ipc_total: 0% → 0, 10% → 10 (lineal)
score_ipc = min(10.0, max(0.0, float(ipc)))

# desocupacion: 0% → 0, 20% → 10 (lineal × 0.5)
score_desoc = min(10.0, max(0.0, float(desoc) / 2))

# icc_utdt: ICC=60 → 0, ICC=30 → 10 (lineal inverso)
score_icc = min(10.0, max(0.0, (60.0 - float(icc)) / 3))

score = promedio(scores disponibles)
```

Umbrales: `0–3` estable | `4–6` en_tension | `7–10` tensionado

**Score actual estimado:** 3.6 con ipc=3.38, desoc≈0.1, icc=38.1

---

## Ejecución y exit codes

```bash
cd projects/informe_coyuntura
python scripts/vida_cotidiana.py
# exit 0 → ipc_total + desocupacion + icc_utdt frescos
# exit 1 → al menos 1 fresco (icc puede fallar → exit 1 normal)
# exit 2 → ningún indicador fresco
```

## Estructura de colectores

```
scripts/
  vida_cotidiana.py           ← orquestador principal
  vida_cotidiana/
    collectors/
      indec_series.py         ← fetch IPC + desocupación (datos.gob.ar)
      utdt_icc.py             ← scraping XLS UTDT página 16458
    config.py                 ← configuración local (importada por collectors)
```

## Notas de mantenimiento

- Si UTDT publica XLS en la página 16458 y el scraping falla: instalar/actualizar `xlrd` (`pip install xlrd`)
- Diferencia clave: ICC = Confianza **Consumidor** (pág. 16458) / ICG = Confianza **Gobierno** (pág. 16457) — no confundir
- Si INDEC reasigna la serie IPC: buscar en `https://apis.datos.gob.ar/series/api/search/?q=IPC+total+nacional&limit=5&format=json`
- La desocupación EPH es trimestral: marcará `desactualizado: true` durante los meses sin publicación
