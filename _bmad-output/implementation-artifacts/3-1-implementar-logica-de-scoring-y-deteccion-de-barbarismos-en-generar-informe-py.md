---
story: 3-1-implementar-logica-de-scoring-y-deteccion-de-barbarismos-en-generar-informe-py
status: done
stepsCompleted: [implement, test]
---

# Story 3.1 + 3.2 — generar_informe.py (scoring + serialización)

Implementado en un único script ya que las dos stories son inseparables en ejecución.

## Resultado

Script: `projects/informe_coyuntura/scripts/generar_informe.py`
Outputs: `output/informe.json` + `output/informe.md`
Exit: 0 (4/4 caches encontrados)

## Lógica de scoring

- Score global: promedio ponderado de 4 cinturones según `PESOS_CINTURONES` en config.py
- Estado por cinturón: 0-3 estable | 4-6 en_tension | 7-10 tensionado (umbrales en `config.py`)
- Barbarismo activo: cinturón dominante con score > 3 → mapeado por `BARBARISMO_MAP`
- Alerta multicinturón: True si 2+ cinturones con score >= 7 (regla matusiana)

## Informe 2026-05

```
score_global: 3.9
barbarismo_activo: político
alerta_multicinturon: false
cinturones: macro=1.8 (estable), politica=5.6 (en_tension), vida_cotidiana=3.6 (en_tension), gestion=5.0 (en_tension)
```

## Schema v1.0.0

Claves: `schema_version`, `generated_at`, `period`, `score_global`, `cinturones.*`, `barbarismo_activo`, `alerta_multicinturon`, `flags`
