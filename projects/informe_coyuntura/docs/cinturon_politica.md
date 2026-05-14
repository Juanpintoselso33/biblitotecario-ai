# Cinturón Político — Indicadores Activos

Script: `scripts/politica.py` | Cache: `output/cache/politica.json`
Peso en score global: **30%** (`config.py → PESOS_CINTURONES["politica"]`)
Barbarismo de riesgo: **político** — confundir popularidad con poder.

Fuente conceptual: Carlos Matus, *Política, Planificación y Gobierno* — capital político como
recurso acumulable en 5 dimensiones independientes: imagen, voto, conflicto, eficacia
legislativa, cohesión interna del oficialismo.

---

## Indicadores activos (5)

| Nombre | Qué mide | Fuente | Frecuencia | Estado |
|---|---|---|---|---|
| `votometro_ventaja_lla` | Brecha ponderada LLA − PJ en intención de voto | Votómetro CIGOB (HTML) | Por encuesta | ✅ automático |
| `eficacia_legislativa` | % proyectos del Ejecutivo aprobados en el Congreso | Elaboración CIGOB (manual) | Mensual | ✅ activo |
| `cohesion_bloque` | % diputados LLA que votan alineados con la posición oficial | Elaboración CIGOB / HCDn | Mensual | ✅ activo |
| `gobernadores_alineamiento` | % gobernadores alineados con la política nacional | Elaboración CIGOB | Mensual | ✅ activo |
| `movilizacion_cepa` | Índice de conflictividad social 0–100 (CEPA) | CEPA / elaboración CIGOB | Mensual | ✅ activo |

---

## Descripción por indicador

### `votometro_ventaja_lla` — Brecha electoral LLA−PJ (Votómetro CIGOB)
- **Qué mide:** diferencia ponderada en pp entre LLA y PJ en intención de voto. Sintetiza las encuestas espacio más recientes con decaimiento temporal y ponderación por calidad consultora. Es la dimensión de *imagen/voto* de Matus.
- **Fuente:** `projects/votometro/web/votometro.html` → array `encuestasRaw`
- **Filtros:** solo entradas con `tipo='espacio'`; ventana últimas 60 días desde la encuesta más reciente
- **Peso:** `exp(−0.015 × días) × calidad_mult` donde A=3, B=2, C=1
- **Cálculo:** `gap = LLA_ponderado − PJ_ponderado` en pp
- **Unidad:** pp (puntos porcentuales)
- **Última ejecución exitosa:** gap=+13.3pp (LLA 41.8 / PJ 28.5) — n=11 encuestas (mar-2026)
- **Nota:** se marca `desactualizado=True` si la encuesta espacio más reciente tiene más de 60 días. Actualizar el Votómetro agrega polls automáticamente.

### `eficacia_legislativa` — Eficacia legislativa del Ejecutivo
- **Qué mide:** qué proporción de los proyectos enviados por el Ejecutivo al Congreso obtuvieron aprobación. Baja eficacia = pérdida de capacidad de gobierno real (más allá de la popularidad). Dimensión *poder legislativo* de Matus.
- **Fuente:** `data/politica/manuales.json`
- **Cálculo:** valor directo (%)
- **Unidad:** % (0 a 100)
- **Valor placeholder (actualizar con dato real):** 42% — `estado: placeholder` en manuales.json
- **Desactualizado:** si fecha_dato > 45 días

### `cohesion_bloque` — Cohesión del bloque LLA en Diputados
- **Qué mide:** qué tan unido vota el bloque afín al gobierno en la Cámara de Diputados. Alta fragmentación = señal de fractura interna aunque el gobierno tenga imagen positiva. Dimensión *cohesión interna* de Matus.
- **Fuente:** `data/politica/manuales.json` (datos de HCDn.gob.ar + elaboración CIGOB)
- **Cálculo:** % de votaciones nominales donde los diputados LLA votaron en línea con la posición oficial del bloque (últimos 3 meses)
- **Unidad:** % (0 a 100)
- **Valor placeholder (actualizar con dato real):** 78% — `estado: placeholder` en manuales.json
- **Desactualizado:** si fecha_dato > 45 días

### `gobernadores_alineamiento` — Alineamiento de gobernadores
- **Qué mide:** soporte territorial y federal del gobierno. Un gobierno con pocas provincias alineadas tiene baja capacidad de implementación subnacional aunque tenga imagen nacional alta. Dimensión *alianzas y apoyo territorial* de Matus.
- **Fuente:** `data/politica/manuales.json` (elaboración CIGOB en base a declaraciones y acuerdos)
- **Cálculo:** % de gobernadores (sobre 24) cuya posición pública es de alineamiento o apoyo al programa del gobierno nacional
- **Unidad:** % (0 a 100)
- **Valor placeholder (actualizar con dato real):** 55% — `estado: placeholder` en manuales.json
- **Desactualizado:** si fecha_dato > 45 días

### `movilizacion_cepa` — Conflictividad social (CEPA)
- **Qué mide:** intensidad de la protesta social: huelgas, cortes, movilizaciones. Alta conflictividad = capital político bajo presión desde abajo. Dimensión *conflicto social* de Matus.
- **Fuente:** `data/politica/manuales.json` (base CEPA sistematizada por CIGOB)
- **Cálculo:** índice 0–100; 0 = sin conflicto; 100 = conflicto máximo histórico registrado
- **Unidad:** índice 0–100
- **Valor placeholder (actualizar con dato real):** 58 — `estado: placeholder` en manuales.json
- **Desactualizado:** si fecha_dato > 45 días

---

## Fórmula de score (0–10, mayor = mayor tensión política)

```python
# votometro_ventaja_lla (gap pp LLA−PJ): +15pp→0, 0→5, −15pp→10
score_vot  = min(10.0, max(0.0, 5.0 - float(gap) / 3.0))

# eficacia_legislativa (% 0–100): 70%→0, 35%→5, 0%→10
score_efic = min(10.0, max(0.0, (70.0 - float(val)) / 7.0))

# cohesion_bloque (% 0–100): 95%→0, 60%→5, 25%→10
score_coh  = min(10.0, max(0.0, (95.0 - float(val)) / 7.0))

# gobernadores_alineamiento (% 0–100): 80%→0, 40%→5, 0%→10
score_gob  = min(10.0, max(0.0, (80.0 - float(val)) / 8.0))

# movilizacion_cepa (índice 0–100): 0→0, 50→5, 100→10
score_mov  = min(10.0, max(0.0, float(val) / 10.0))

score = promedio(scores disponibles)  # equal-weight, ignora indicadores ausentes
```

Umbrales: `0–3` estable | `4–6` en_tension | `7–10` tensionado

**Score actual (abr/may-2026):** 3.2 — en_tension (límite: ≤3.0 = estable)

Scores individuales estimados:
| Indicador | Valor | Score |
|---|---|---|
| `votometro_ventaja_lla` | +13.3pp | 0.6 |
| `eficacia_legislativa` | 42% | 4.0 |
| `cohesion_bloque` | 78% | 2.4 |
| `gobernadores_alineamiento` | 55% | 3.1 |
| `movilizacion_cepa` | 58 | 5.8 |

---

## Estructura de datos

```
data/politica/
  manuales.json     ← indicadores manuales: eficacia, cohesion, gobernadores, movilizacion

scripts/
  politica.py       ← colector principal (auto + manuales)
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
# exit 0 → 5/5 frescos (incluyendo Votómetro parseado)
# exit 1 → al menos 1 fresco (normal si Votómetro no tiene polls recientes)
# exit 2 → ningún fresco (todos desde cache)
```

## Notas de mantenimiento

- **Actualizar manuales:** editar `data/politica/manuales.json` con nuevos valores y `fecha_dato` actualizada
- **Votómetro desactualizado:** si `votometro_ventaja_lla.desactualizado=true`, es porque no hay encuestas espacio en los últimos 60 días. Agregar encuestas al Votómetro en `projects/votometro/web/votometro.html` → array `encuestasRaw` (campo `tipo:'espacio'`)
- **Barbarismo político:** el cinturón deliberadamente no duplica `ipc` ni otros indicadores de bienestar — esos corresponden al cinturón `vida_cotidiana`. El barbarismo a evitar es medir solo imagen/popularidad ignorando las dimensiones institucionales del capital político
- **Fuente CEPA:** si CEPA publica índices propios directamente descargables, priorizar eso sobre la codificación manual. Buscar en `https://centrocepa.com.ar`
- **Cohesión:** datos base en `https://hcdn.gob.ar/diputados/votaciones/` — filtrar por bloque LLA en votaciones nominales
