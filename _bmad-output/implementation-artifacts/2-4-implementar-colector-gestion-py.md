---
story: 2-4-implementar-colector-gestion-py
status: done
stepsCompleted: [implement, test, commit]
---

# Story 2.4 — Implementar colector gestion.py

## Resultado

Script: `projects/informe_coyuntura/scripts/gestion.py`
Cache: `projects/informe_coyuntura/output/cache/gestion.json`
Exit: 0 (todos los indicadores frescos)

## Indicadores

| Indicador | Fuente | Valor (ene/feb-2026) | Estado |
|---|---|---|---|
| `indice_salarios_publico` | datos.gob.ar `149.1_SOR_PUBICO_OCTU_0_14` | +1.81% m/m (ene-2026) | OK |
| `isac_construccion` | datos.gob.ar `33.4_ISAC_CEMENAND_0_0_21_24` | -3.83% m/m (feb-2026) | OK |

## Score

```
salarios_publico: 5 - 1.81/3 = 4.4
isac_construccion: 5 - (-3.83)/6 = 5.64
score final: round(avg([4.4, 5.64]), 1) = 5.0
```

## Notas Dev

- `api.presupuestoabierto.gob.ar` no resuelve DNS — descartado.
- EPH empleo público ID original `41.1_PJPUBNA1T_2016_T_31` era inválido.
- Reemplazado con IS sector público (IS disponible hasta ene-2026) e ISAC cemento (feb-2026).
- Ambas series en datos.gob.ar, mismo patrón que macro.py y politica.py.
- ISAC cemento es proxy válido de construcción pública (Matus: capacidad operativa del Estado).
