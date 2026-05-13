# Story 2.1: Adaptar colector vida_cotidiana.py al patrón estándar

**Status:** in-progress
**Epic:** 2 — Informe de Coyuntura — Colección de Datos

## User Story

Como Trico, quiero que el colector vida_cotidiana existente siga el patrón estándar de la arquitectura (URLs nombradas, config, cache, exit codes), para que sea consistente con los otros colectores y el sistema de fallback funcione uniformemente.

## Acceptance Criteria

- `python scripts/vida_cotidiana.py` ejecuta desde `projects/informe_coyuntura/`
- El script sigue la estructura estándar: URL constants → fetch por indicador → calcular_score → load/save_cache → main()
- Ante fallo de una fuente, imprime `[WARN] vida_cotidiana.<indicador>: <error>. Usando cache.` y continúa
- Escribe `output/cache/vida_cotidiana.json` si al menos un indicador es fresco
- Retorna exit code 0 (todos frescos), 1 (parcial cache), 2 (total desde cache)
- Completa en menos de 5 minutos en red normal

## Technical Context

### Estructura existente (migrada en Story 1.2)

```
scripts/vida_cotidiana/
├── main.py              # entry point original (NO usar directamente)
├── config.py            # URLs y constantes específicas del cinturón
├── collectors/
│   ├── __init__.py
│   ├── indec_series.py  # IPC, desocupación, RIPTE, EMAE, etc.
│   ├── bcra.py          # Créditos privados, BADLAR
│   ├── utdt_icc.py      # Índice de Confianza del Consumidor (scraping + xlrd)
│   ├── cafam.py
│   ├── ciccra.py
│   ├── snic.py
│   ├── salud.py
│   └── trends.py
└── data/                # Outputs históricos del colector viejo (JSON timestamped)
```

### Indicadores clave a extraer

| Indicador | Fuente | Dato último |
|---|---|---|
| `ipc_total` | INDEC vía datos.gob.ar | 3.38% m/m (mar-2026) |
| `desocupacion` | INDEC EPH | % (trimestral) |
| `icc_utdt` | UTDT scraping + xlrd | índice |

### Cache schema estándar

```json
{
  "cinturon": "vida_cotidiana",
  "generated_at": "ISO 8601",
  "score": 4.2,
  "indicadores": {
    "ipc_total": {
      "valor": 3.38,
      "unidad": "% mensual",
      "fuente": "https://apis.datos.gob.ar/series/api/series/",
      "fecha_dato": "2026-03-01",
      "desactualizado": false
    }
  }
}
```

### Scoring vida_cotidiana (0-10, mayor = peor)

- `ipc_total` (% mensual): score = min(10, ipc_pct) — 0% → 0, 10% → 10
- `desocupacion` (%): score = min(10, desoc/2) — 0% → 0, 20% → 10
- `icc_utdt`: score = min(10, (60 - icc)/3) — ICC ~42 → ~6, ICC >60 → 0

Score final = promedio de los disponibles.

### Dependencias Python

Las mismas que `scripts/vida_cotidiana/requirements.txt`:
- `requests>=2.31.0`
- `xlrd==1.2.0` (OJO: no usar >=2.0)
- `beautifulsoup4>=4.12`
- `pdfplumber>=0.10.0`
- `pytrends>=4.9.2`

Deben quedar en `projects/informe_coyuntura/requirements.txt`.

### Resolución de imports

El wrapper `scripts/vida_cotidiana.py` usa:
```python
sys.path.insert(0, str(Path(__file__).parent / "vida_cotidiana"))
```
Esto pone `scripts/vida_cotidiana/` en sys.path, permitiendo `from collectors.X import Y` y que los collectors hagan `from config import ...` (encuentran `vida_cotidiana/config.py`).

La `vida_cotidiana/` necesita `__init__.py` vacío para ser un paquete Python.

## Files to Create/Modify

| Archivo | Acción |
|---|---|
| `scripts/vida_cotidiana.py` | CREAR — entry point estándar |
| `scripts/vida_cotidiana/__init__.py` | CREAR — vacío, para hacer el directorio un paquete |
| `requirements.txt` | ACTUALIZAR — copiar deps de vida_cotidiana/requirements.txt |

## Dev Notes

- NO tocar nada dentro de `scripts/vida_cotidiana/` — son los collectors existentes que funcionan
- El `scripts/vida_cotidiana/main.py` original queda como legacy, no se borra
- El script nuevo `vida_cotidiana.py` es el que se ejecuta con `python scripts/vida_cotidiana.py`
- El `fetch_indec()` hace muchas requests internamente; la mayoría pueden fallar parcialmente. Llamarlo UNA sola vez y extraer los campos que nos interesan
- ICC UTDT usa `verify=False` por cert roto — normal para esta fuente
- Exit code se hace con `sys.exit(n)` en el main
