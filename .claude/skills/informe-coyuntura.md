# Skill: Informe de Coyuntura — Mantenimiento y Operación

## Cuándo usar este skill

Cuando el usuario pide: correr el informe, actualizar datos de coyuntura, agregar un indicador a un cinturón, entender cómo funciona un colector, o diagnosticar por qué un dato está desactualizado.

---

## Estructura del proyecto

```
projects/informe_coyuntura/
  config.py                    ← pesos, umbrales, barbarismos
  scripts/
    macro.py                   ← colector cinturón macro
    politica.py                ← colector cinturón político
    vida_cotidiana.py          ← colector cinturón vida cotidiana
    gestion.py                 ← colector cinturón gestión
    generar_informe.py         ← genera informe.json + informe.md
    vida_cotidiana/
      collectors/
        indec_series.py        ← fetch IPC + desocupación
        utdt_icc.py            ← scraping XLS UTDT (ICC)
      config.py
  output/
    cache/
      macro.json               ← cache del colector macro
      politica.json
      vida_cotidiana.json
      gestion.json
    informe.json               ← output schema v1.0.0
    informe.md                 ← output markdown para reunión
  docs/
    cinturon_macro.md          ← referencia técnica indicadores macro
    cinturon_politica.md       ← referencia técnica indicadores político
    cinturon_vida_cotidiana.md ← referencia técnica indicadores vida cotidiana
    cinturon_gestion.md        ← referencia técnica indicadores gestión
```

---

## Mapa de indicadores por cinturón

| Cinturón | Peso | Barbarismo | Indicadores | Estado |
|---|---|---|---|---|
| `macro` | 30% | tecnocrático | `ipc_total`, `reservas_bcra`, `badlar` | ✅ todos activos |
| `politica` | 30% | político | `ipc_regulados`, `icg_utdt` | `ipc_regulados` ✅, `icg_utdt` ⚠️ falla graceful |
| `vida_cotidiana` | 20% | político | `ipc_total`, `desocupacion`, `icc_utdt` | `ipc_total`+`desoc` ✅, `icc_utdt` ⚠️ variable |
| `gestion` | 20% | gerencial | `indice_salarios_publico`, `isac_construccion` | ✅ todos activos |

### Series INDEC activas (datos.gob.ar)

| Serie ID | Indicador | Cinturón |
|---|---|---|
| `148.3_INIVELNAL_DICI_M_26` | IPC total nacional | macro + vida_cotidiana |
| `148.3_IREGULANAL_DICI_M_22` | IPC regulados | politica |
| `149.1_SOR_PUBICO_OCTU_0_14` | IS sector público (base oct 2016) | gestion |
| `33.4_ISAC_CEMENAND_0_0_21_24` | ISAC insumos cemento | gestion |

### APIs externas

| URL base | Variables | Cinturón |
|---|---|---|
| `https://apis.datos.gob.ar/series/api/series/` | ver series arriba | macro, politica, vida_cotidiana, gestion |
| `https://api.bcra.gob.ar/estadisticas/v4.0/Monetarias/1` | Reservas internacionales | macro |
| `https://api.bcra.gob.ar/estadisticas/v4.0/Monetarias/7` | BADLAR bancos privados | macro |
| `https://www.utdt.edu/listado_contenidos.php?id_item_menu=16457` | ICG — confianza gobierno | politica |
| `https://www.utdt.edu/listado_contenidos.php?id_item_menu=16458` | ICC — confianza consumidor | vida_cotidiana |

---

## Cómo correr el informe completo

```bash
cd projects/informe_coyuntura

# 1. Correr los 4 colectores (orden no importa)
python scripts/macro.py
python scripts/politica.py       # exit 1 es normal (ICG UTDT falla graceful)
python scripts/vida_cotidiana.py
python scripts/gestion.py

# 2. Generar el informe
python scripts/generar_informe.py

# Outputs:
#   output/informe.json   → schema v1.0.0 para dev externo
#   output/informe.md     → markdown para reunión/Drive
```

### Exit codes de los colectores

- `exit 0` → todos los indicadores del cinturón frescos
- `exit 1` → al menos 1 fresco (uno o más fallaron → usó cache para los demás)
- `exit 2` → ningún indicador fresco (todo desde cache)

**`politica.py` con exit 1 es el estado normal** mientras UTDT no publique XLS en página 16457.

---

## Lógica de scoring y barbarismos (config.py)

```python
PESOS_CINTURONES = {"macro": 0.30, "politica": 0.30, "vida_cotidiana": 0.20, "gestion": 0.20}
UMBRALES = {"ESTABLE_MAX": 3, "EN_TENSION_MAX": 6}
BARBARISMO_MAP = {
    "macro":          "tecnocrático",
    "politica":       "político",
    "gestion":        "gerencial",
    "vida_cotidiana": "político",
}
```

**Score global** = promedio ponderado de los 4 cinturones con sus pesos.

**Barbarismo activo** = cinturón con score más alto que supera umbral de tensión (>3). Corresponde al riesgo de decisión desequilibrada según el PES de Matus.

**Alerta multicinturón** = 2+ cinturones con score ≥ 7. Señal matusiana de máxima: no apretar tres cinturones a la vez.

---

## Schema del informe.json (v1.0.0)

```json
{
  "schema_version": "1.0.0",
  "generated_at": "ISO timestamp",
  "period": "YYYY-MM",
  "score_global": 0.0,
  "cinturones": {
    "<nombre>": {
      "score": 0.0,
      "estado": "estable | en_tension | tensionado",
      "barbarismo_riesgo": "tecnocrático | político | gerencial",
      "indicadores": { "<nombre>": { "valor": ..., "unidad": ..., "fuente": ..., "fecha_dato": ..., "desactualizado": false } },
      "alerta": null
    }
  },
  "barbarismo_activo": "tecnocrático | político | gerencial | null",
  "alerta_multicinturon": false,
  "flags": ["desactualizado:macro:ipc_total", "cache_ausente:politica"]
}
```

---

## Diagnóstico rápido

| Síntoma | Causa probable | Solución |
|---|---|---|
| Dato desactualizado en output | Colector falló y usó cache | Correr el colector individualmente y ver el error |
| `icg_utdt` siempre falla | UTDT no publica XLS en pág 16457 | Normal — exit 1 esperado en politica.py |
| `icc_utdt` falla | UTDT no publica XLS en pág 16458 | Verificar `pip install xlrd` y disponibilidad del XLS |
| BCRA API error 5xx | API BCRA inestable | Reintentar; datos quedan en cache |
| Serie INDEC no encontrada (404) | INDEC reasignó la serie | Buscar nueva ID en datos.gob.ar con `q=...` |
| Score global inesperadamente alto | Verificar cache con datos viejos | Revisar `fecha_dato` en cada cache JSON |

---

## Para agregar un nuevo indicador

1. Elegir el cinturón al que pertenece
2. Verificar la serie en datos.gob.ar o la URL de la API
3. Agregar la constante de URL/ID al inicio del script del cinturón correspondiente
4. Implementar la función `fetch_<indicador>()` siguiendo el patrón estándar
5. Agregar el nombre a `INDICADORES_ESPERADOS`
6. Agregar la fórmula de score en `calcular_score()`
7. Actualizar el doc `docs/cinturon_<nombre>.md`
