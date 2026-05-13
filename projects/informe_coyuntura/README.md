# Informe de Coyuntura

Colectores de datos para los 4 cinturones matusianos (macro, político, vida cotidiana, gestión) + generador del informe periódico.

## Cómo correr los colectores

Desde la carpeta `projects/informe_coyuntura/`:

```
python scripts/macro.py
python scripts/politica.py
python scripts/vida_cotidiana/main.py
python scripts/gestion.py
```

Cada colector corre de forma independiente. No es necesario correrlos todos.

> **[Completar en Story 2.2–2.4]** Los scripts `macro.py`, `politica.py` y `gestion.py` se implementan en Epic 2.

## Cómo generar el informe

```
python scripts/generar_informe.py
```

> **[Completar en Story 3.1–3.2]** `generar_informe.py` se implementa en Epic 3.

## Outputs esperados

| Archivo | Descripción |
|---|---|
| `output/cache/macro.json` | Último fetch válido del cinturón macro |
| `output/cache/politica.json` | Último fetch válido del cinturón político |
| `output/cache/vida_cotidiana.json` | Último fetch válido del cinturón vida cotidiana |
| `output/cache/gestion.json` | Último fetch válido del cinturón gestión |
| `output/informe.json` | Informe completo (schema v1.0.0) — para el dev externo |
| `output/informe.md` | Informe markdown — para Drive y reunión |

## Exit codes

| Código | Significado |
|---|---|
| `0` | Todos los indicadores son datos frescos |
| `1` | Mezcla: algunos frescos, algunos del cache |
| `2` | Todos los indicadores vienen del cache (fallo total de fuentes) |

## Parámetros del modelo

Los pesos, umbrales y el mapping de barbarismos se modifican en `config.py`. Documentar cualquier cambio metodológico en el commit con justificación.

## Dependencias

```
pip install -r requirements.txt
```
