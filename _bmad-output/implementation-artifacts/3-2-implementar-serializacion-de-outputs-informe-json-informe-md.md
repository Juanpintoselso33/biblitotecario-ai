---
story: 3-2-implementar-serializacion-de-outputs-informe-json-informe-md
status: done
stepsCompleted: [implement, test]
---

# Story 3.2 — Serialización outputs informe.json + informe.md

Implementado junto con Story 3.1 en `generar_informe.py`.

## Outputs verificados

### informe.json (schema v1.0.0)
- Path: `projects/informe_coyuntura/output/informe.json`
- Claves exactas según architecture.md: `schema_version`, `generated_at`, `period`, `score_global`, `cinturones`, `barbarismo_activo`, `alerta_multicinturon`, `flags`
- Incluye `valor_brecha_vs_ipc` en indicadores que lo calculan (ipc_regulados)

### informe.md (markdown con frontmatter YAML)
- Path: `projects/informe_coyuntura/output/informe.md`
- Frontmatter: `periodo`, `generado`, `score_global`, `barbarismo_activo`, `alerta_multicinturon`, `schema_version`
- Tabla por cinturón con emoji de estado (🟢/🟡/🔴), score, indicadores, flag de cache
- Alerta matusiana visible si `alerta_multicinturon: true`
- Sección de advertencias con flags de caches ausentes o indicadores desactualizados
