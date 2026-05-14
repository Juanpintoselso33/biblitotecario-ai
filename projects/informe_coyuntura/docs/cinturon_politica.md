# Cinturón Político — Indicadores Activos

Script: `scripts/politica.py` | Cache: `output/cache/politica.json`
Peso en score global: **30%** (`config.py → PESOS_CINTURONES["politica"]`)
Barbarismo de riesgo: **político** — confundir popularidad con poder.

Fuente conceptual: Carlos Matus, *Política, Planificación y Gobierno* — capital político como
recurso acumulable en 5 dimensiones independientes: imagen, voto, confianza institucional,
cohesión interna del oficialismo, alianzas territoriales, conflicto social.

---

## Indicadores activos (6)

| Nombre | Qué mide | Fuente | Frecuencia | Estado |
|---|---|---|---|---|
| `votometro_ventaja_lla` | Brecha ponderada LLA − PJ en intención de voto | Votómetro CIGOB (HTML) | Por encuesta | ✅ automático |
| `icg_utdt` | Índice de Confianza en el Gobierno — escala 0–5 (UTDT) | datos.gob.ar series API | Trimestral | ✅ automático |
| `movilizacion_cepa` | Conflictividad social: conflictos laborales y protesta (CEPA) | centrocepa.com.ar scrape | Por informe | ✅ automático |
| `cohesion_bloque` | % diputados LLA que votan alineados con la posición oficial | Elaboración CIGOB / HCDn | Mensual | 📋 manual |
| `eficacia_legislativa` | % proyectos del Ejecutivo aprobados en el Congreso | Elaboración CIGOB (manual) | Mensual | 📋 manual |
| `gobernadores_alineamiento` | % gobernadores alineados con la política nacional | Elaboración CIGOB | Mensual | 📋 manual |

---

## Descripción por indicador

### `votometro_ventaja_lla` — Brecha electoral LLA−PJ (Votómetro CIGOB)
- **Qué mide:** diferencia ponderada en pp entre LLA y PJ en intención de voto. Sintetiza las encuestas espacio más recientes con decaimiento temporal y ponderación por calidad consultora. Dimensión *imagen/voto* de Matus.
- **Fuente:** `projects/votometro/web/votometro.html` → array `encuestasRaw`
- **Filtros:** solo entradas con `tipo='espacio'`; ventana últimas 60 días desde la encuesta más reciente
- **Peso:** `exp(−0.015 × días) × calidad_mult` donde A=3, B=2, C=1
- **Cálculo:** `gap = LLA_ponderado − PJ_ponderado` en pp
- **Unidad:** pp (puntos porcentuales)
- **Última ejecución exitosa:** gap=+13.3pp (LLA 41.8 / PJ 28.5) — n=11 encuestas (mar-2026)
- **Nota:** se marca `desactualizado=True` si la encuesta espacio más reciente tiene más de 60 días.

### `icg_utdt` — Índice de Confianza en el Gobierno (UTDT)
- **Qué mide:** confianza ciudadana en el gobierno, medida por UTDT en escala 0–5 (mayor = más confianza). Dimesión *confianza institucional* de Matus. Histórico reciente: 0.7–3.5.
- **API:** `GET https://apis.datos.gob.ar/series/api/series/?ids=370.2_ICG_NIVEL_RAL_0_0_17_40&format=json&limit=1&sort=desc`
- **Frecuencia:** trimestral
- **Unidad:** índice 0–5
- **Última ejecución exitosa:** 2.36 (2026-01)
- **Nota:** se marca `desactualizado=True` si el dato tiene más de 120 días (un cuatrimestre de gracia sobre la frecuencia trimestral).

### `movilizacion_cepa` — Conflictividad social (CEPA)
- **Qué mide:** intensidad de la protesta social: huelgas, cortes, conflictos laborales y movilizaciones. Dimensión *conflicto social* de Matus.
- **Fuente:** scrape de `centrocepa.com.ar/informes` → último informe con "conflictividad" en URL → extracción de cifra de conflictos
- **Cálculo:** extrae "X casos por mes" o "al menos N conflictos" del texto del informe; normaliza a 0–100 (80 casos/mes = 100 ó 200 conflictos acumulados = 100)
- **Unidad:** índice 0–100 (mayor = mayor conflictividad)
- **Última ejecución exitosa:** 46.0 (92 conflictos laborales en lo que va de 2026 — informe CEPA may-2026)

### `cohesion_bloque` — Cohesión del bloque LLA en Diputados
- **Qué mide:** qué tan unido vota el bloque afín al gobierno en Cámara de Diputados. Dimensión *cohesión interna* de Matus.
- **Fuente:** `data/politica/manuales.json` (HCDn.gob.ar + elaboración CIGOB)
- **Cálculo:** % de votaciones nominales donde diputados LLA votaron alineados con posición oficial (últimos 3 meses)
- **Unidad:** % (0 a 100)
- **Valor placeholder (actualizar):** 78%
- **Datos base:** `https://hcdn.gob.ar/diputados/votaciones/` — filtrar por bloque LLA en votaciones nominales

### `eficacia_legislativa` — Eficacia legislativa del Ejecutivo
- **Qué mide:** proporción de proyectos del Ejecutivo aprobados por el Congreso. Dimensión *poder legislativo* de Matus.
- **Fuente:** `data/politica/manuales.json`
- **Unidad:** % (0 a 100)
- **Valor placeholder (actualizar):** 42%

### `gobernadores_alineamiento` — Alineamiento de gobernadores
- **Qué mide:** soporte territorial y federal del gobierno. Dimensión *alianzas territoriales* de Matus.
- **Fuente:** `data/politica/manuales.json`
- **Cálculo:** % de gobernadores (sobre 24) con posición pública de apoyo al programa nacional
- **Unidad:** % (0 a 100)
- **Valor placeholder (actualizar):** 55%

---

## Fórmula de score (0–10, mayor = mayor tensión política)

```python
# votometro_ventaja_lla (gap pp LLA−PJ): +15pp→0, 0→5, −15pp→10
score_vot  = min(10.0, max(0.0, 5.0 - float(gap) / 3.0))

# icg_utdt (índice 0–5, mayor confianza = menor tensión): 3.5→0, 1.75→5, 0→10
score_icg  = min(10.0, max(0.0, (3.5 - float(icg)) / 0.35))

# movilizacion_cepa (índice 0–100): 0→0, 50→5, 100→10
score_cepa = min(10.0, max(0.0, float(val) / 10.0))

# eficacia_legislativa (% 0–100): 70%→0, 35%→5, 0%→10
score_efic = min(10.0, max(0.0, (70.0 - float(val)) / 7.0))

# cohesion_bloque (% 0–100): 95%→0, 60%→5, 25%→10
score_coh  = min(10.0, max(0.0, (95.0 - float(val)) / 7.0))

# gobernadores_alineamiento (% 0–100): 80%→0, 40%→5, 0%→10
score_gob  = min(10.0, max(0.0, (80.0 - float(val)) / 8.0))

score = promedio(scores disponibles)  # equal-weight, ignora indicadores ausentes
```

Umbrales: `0–3` estable | `4–6` en_tension | `7–10` tensionado

**Score actual (may-2026):** 3.0 — estable (borde)

Scores individuales (may-2026):
| Indicador | Valor | Score |
|---|---|---|
| `votometro_ventaja_lla` | +13.3pp | 0.6 |
| `icg_utdt` | 2.36 | 3.1 |
| `movilizacion_cepa` | 46.0 | 4.6 |
| `eficacia_legislativa` | 42% | 4.0 |
| `cohesion_bloque` | 78% | 2.4 |
| `gobernadores_alineamiento` | 55% | 3.1 |

---

## Estructura de datos

```
data/politica/
  manuales.json     ← cohesion_bloque, eficacia_legislativa, gobernadores_alineamiento

scripts/
  politica.py       ← colector principal (auto: votometro, icg_utdt, movilizacion_cepa + manuales)
```

### Formato `manuales.json`

Cada entrada:
```json
{
  "valor": 42,
  "unidad": "% proyectos oficiales aprobados",
  "fuente": "descripción de la fuente",
  "notas": "metodología o aclaraciones",
  "fecha_dato": "YYYY-MM-DD"
}
```

Actualizar `fecha_dato` junto con `valor` en cada ciclo de actualización.

---

## Ejecución y exit codes

```bash
cd projects/informe_coyuntura
python scripts/politica.py
# exit 0 → 6/6 frescos
# exit 1 → al menos 1 fresco (normal si Votómetro no tiene polls recientes)
# exit 2 → ningún fresco (todos desde cache)
```

## Notas de mantenimiento

- **Votómetro desactualizado:** si `votometro_ventaja_lla.desactualizado=true`, agregar encuestas al Votómetro en `projects/votometro/web/votometro.html` → array `encuestasRaw` (campo `tipo:'espacio'`)
- **ICG desactualizado:** el ICG se publica cada trimestre. Si `icg_utdt.desactualizado=true`, esperar la próxima publicación en `datos.gob.ar` o verificar la serie en `https://apis.datos.gob.ar/series/api/series/?ids=370.2_ICG_NIVEL_RAL_0_0_17_40&format=json&limit=4&sort=desc`
- **CEPA:** si el scraper falla, revisar que `centrocepa.com.ar/informes` siga publicando links con "conflictividad" en la URL. Si cambia la estructura del texto del informe, ajustar los patrones regex en `fetch_cepa_movilizacion()`
- **Manuales:** actualizar `data/politica/manuales.json` con nuevos valores y `fecha_dato` actualizada en cada ciclo
- **Cohesión:** datos base en `https://hcdn.gob.ar/diputados/votaciones/` — filtrar por bloque LLA en votaciones nominales
- **Barbarismo político:** el cinturón deliberadamente no duplica `ipc` ni indicadores de bienestar — esos corresponden al cinturón `vida_cotidiana`. El barbarismo a evitar es medir solo imagen/popularidad ignorando las dimensiones institucionales del capital político
