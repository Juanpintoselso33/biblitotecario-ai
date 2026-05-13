---
story: 2-3-implementar-colector-politica-py
status: done
stepsCompleted: [implement, test, commit]
---

# Story 2.3 — Implementar colector politica.py

## Resultado

Script: `projects/informe_coyuntura/scripts/politica.py`
Cache: `projects/informe_coyuntura/output/cache/politica.json`
Exit: 1 (parcial — ipc_regulados OK, icg_utdt sin XLS en fuente)

## Indicadores

| Indicador | Fuente | Valor (mar-2026) | Estado |
|---|---|---|---|
| `ipc_regulados` | datos.gob.ar series `148.3_IREGULANAL_DICI_M_22` | 5.08% m/m, brecha +1.70pp | OK |
| `icg_utdt` | utdt.edu listado 16457 | N/A (sin XLS en página) | WARN→cache |

## Score

```
ipc_regulados: base=5.08 + bonus=1.70*0.3=0.51 → 5.59
icg_utdt: ausente (sin cache previo)
score final: 5.6
```

## Notas Dev

- UTDT página 16457 (ICG) no expone XLS descargable como 16458 (ICC). El ICG queda en cache cuando esté disponible.
- IPC regulados es proxy válido de decisiones gubernamentales sobre tarifas (subsidios/servicios públicos).
- Exit 1 es correcto: AC permite "continúa con los disponibles ante fallo parcial".
