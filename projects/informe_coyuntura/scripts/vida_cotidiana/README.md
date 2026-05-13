# Monitor Cinturón Vida Cotidiana — CIGOB

Recolecta automáticamente los indicadores del cinturón de vida cotidiana (Matus 1997)
para el dashboard de análisis de realidad política.

## Instalación

```bash
pip install -r requirements.txt
```

## Uso

```bash
python main.py              # Recolecta todos los datos y guarda en data/
python main.py --check      # Estado de fuentes manuales (no automatizadas)
python main.py --search IPC # Busca series en catálogo INDEC datos.gob.ar
```

## Fuentes implementadas (Tier 1 — funcionando)

| Collector | Fuente | Datos |
|---|---|---|
| `indec_series.py` | INDEC via datos.gob.ar API | IPC total, IPC-Alimentos, salarios, desocupación, ISAC, EMAE |
| `bcra.py` | BCRA API v4.0 | Créditos privados, tarjeta, personales, hipotecarios, BADLAR |
| `utdt_icc.py` | UTDT (scraping + XLS) | ICC mensual desde 2001 |
| `cafam.py` | CAFAM API JSON | Patentamiento motos por provincia |

## Fuentes no automatizadas

Ver `collectors/manual.py` para documentación de:
- Carne vacuna (CICCRA — PDF mensual)
- Tarifas (ENRE/ENARGAS — sin API, usar IPC-Vivienda como proxy)
- Mortalidad PyMEs (AFIP no público — usar CAME IPIP como proxy)
- Pluriempleo (EPH microdatos — procesamiento manual)
- Deserción escolar (Ministerio Educación — datos anuales)
- Inseguridad (SNIC — rezago 6-12 meses)
- Sentimiento digital (requiere X API + modelo NLP)

## Outputs

Los datos se guardan en `data/vida_cotidiana_YYYYMMDD_HHMM.json` con estructura:

```json
{
  "metadata": { "timestamp": "...", "fuentes_automatizadas": [...] },
  "indec": { "ipc_total": {"valor": ..., "variacion_mensual_pct": ..., "fecha": ...} },
  "bcra":  { "prestamos_tarjeta": {"valor": ..., "fecha": ...} },
  "utdt":  { "icc_utdt": {"valor": ..., "fecha": ...} },
  "cafam": { "patentamiento_motos": {"valor": ..., "fecha": ..., "provincias": {...}} }
}
```
