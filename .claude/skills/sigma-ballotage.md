---
name: sigma-ballotage
description: Calibración de σ tiempo-variable para simulación de ballotage en el Votómetro. Usar cuando se revise metodología de segunda vuelta o se actualice la distancia temporal a la elección.
---

# Skill: σ Ballotage Tiempo-Variable

## Cuándo aplicar

Cuando el Votómetro use σ fijo para la simulación de ballotage y la elección esté a más de 3 meses de distancia. El σ fijo subestima masivamente la incertidumbre real a >90 días.

## El problema

Con σ=4 y una ventaja de 17pp (Milei 50% vs Kicillof 33%), la probabilidad condicional de que Milei gane el ballotage es 99.9% — independientemente de cualquier dato adverso de primera vuelta. Esto es metodológicamente incorrecto a 18 meses de la elección.

**Evidencia:** las encuestas de 2ª vuelta disponibles tienen un rango de 22pp entre consultoras (30% a 52% para el oponente de Milei). σ=4 implica una precisión inexistente.

## La solución: random walk calibrado

La literatura estándar (Gelman/Morris/The Economist, Silver/538) usa σ ∝ √(días_restantes).

### Implementación en el Votómetro

Localizar en `web/votometro.html` el bloque Monte Carlo. Buscar `ballM` y `ballK`. Reemplazar:

```javascript
// ANTES (incorrecto para elecciones lejanas):
let ballM = 50 + randn()*4;
let ballK = 33 + randn()*4;

// DESPUÉS (tiempo-variable):
const diasRef = 90;
const sigmaBallBase = 4;
const sigmaBall = Math.max(
    sigmaBallBase,
    sigmaBallBase * Math.sqrt(diasParaEleccion / diasRef)
);
let ballM = muBallM + randn() * sigmaBall;
let ballK = muBallK + randn() * sigmaBall;
```

Donde `muBallM` y `muBallK` son los promedios de las encuestas de 2ª vuelta disponibles.

### Tabla de referencia σ → P(Milei gana) con spread 17pp

| Días restantes | σ resultante | P(Milei > Kicillof) |
|---|---|---|
| 570 (~abr-2026) | ~10pp | ~88% |
| 365 (~oct-2026) | ~8pp | ~92% |
| 180 (~abr-2027) | ~5.7pp | ~99% |
| 90 (~jul-2027) | 4pp | ~99.9% |

### Actualizar también el texto explicativo

Buscar la nota de ballotage en el HTML y agregar mención de que el σ crece con el tiempo:

```
"σ de simulación tiempo-variable: calibrado al error histórico cercano a elección (σ=4pp)
y ampliado por random walk para elecciones lejanas (σ≈10pp a 18 meses)."
```

## Fuentes de referencia

- `docs/investigaciones/2026-04-01_sigma_ballotage_uncertainty.md` — investigación completa
- Gelman & Morris (2020), Harvard Data Science Review
- FiveThirtyEight methodology 2020/2024
