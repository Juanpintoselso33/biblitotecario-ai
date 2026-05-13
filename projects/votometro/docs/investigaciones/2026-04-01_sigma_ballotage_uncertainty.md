# Investigación: Calibración de σ en pronósticos de ballotage

**Fecha:** 1 de abril de 2026  
**Contexto:** Votómetro Argentina 2027 — revisión metodológica del σ usado en la simulación de segunda vuelta  
**Pregunta:** ¿Por qué la probabilidad condicional de Milei en ballotage es 99.9% pese a datos más adversos?

---

## Hallazgo central

El 99.9% **no cambia con datos adversos de primera vuelta** porque es una probabilidad *condicional* — solo depende de los parámetros del ballotage (μ_Milei, μ_Kicillof, σ), no de aprobación, ICC ni EMAE. El problema es que **σ=4 es imposiblemente bajo para una elección a 18 meses**.

---

## Evidencia empírica: dispersión real entre encuestas de 2ª vuelta

| Encuesta | Fecha | Milei | Kicillof/oponente |
|---|---|---|---|
| Trends | nov-2025 | 50% | 38% |
| Trends | ene-2026 | 49% | 35% |
| Opinaia | ene-2026 | 50% | 30% |
| Opinaia | mar-2026 | 50% | 30% |
| Hugo Haime | mar-2026 | 37.5% | 46% (Kicillof gana) |
| Alaska/Trespuntozero | mar-2026 | 47.9% | 52.1% (Massa, re-run 2023) |

**Rango de Kicillof/oponente: 30% → 52% = 22pp de dispersión.** Con σ=4 el modelo asume una precisión que los datos contradicen.

---

## Qué dice la literatura académica

### Consenso: σ crece con √(días)

Los principales modelos de pronóstico electoral (Gelman/Morris para The Economist, Silver/FiveThirtyEight) usan un **random walk temporal**: la incertidumbre en preferencias electorales crece como √(días al comicio).

> *"The most relevant parameter in the model is the standard deviation of the random walk of national vote preference over time. When implementing their model for The Economist, they set this scale to a value that seemed high enough to allow for plausible changes **during the half year** leading up to the election."*  
> — Gelman & Morris, Harvard Data Science Review, 2020

Ese estándar es para **6 meses**. El Votómetro está a **18 meses** → la incertidumbre debería ser ~3x mayor.

**Fórmula implícita:**
```
σ_total(t) = √(σ²_encuestas + σ²_drift(t))
σ_drift(t) ∝ √(días_restantes)
```

### FiveThirtyEight
- σ = 3.9pp a **1 semana** del comicio  
- A 18 meses, su propio modelo ampliaría a ~12-15pp  

### Contexto argentino
Argentina tiene errores históricos mayores al promedio global: PASO 2023 = 8-13pp de error en primera vuelta. Para una segunda vuelta a 18 meses, la incertidumbre es estructuralmente mayor.

---

## Impacto del cambio en P(Milei gana ballotage)

Con μ_Milei=50%, μ_Kicillof=33%, diferencia=17pp:

| σ (por candidato) | σ_combinado | P(Milei > Kicillof) |
|---|---|---|
| 4 (actual) | 5.7pp | **99.9%** |
| 8 | 11.3pp | ~93.4% |
| 10 | 14.1pp | ~88.1% |
| 12 | 17.0pp | **~84.1%** |
| 15 | 21.2pp | ~79.0% |

**Fórmula:** P = Φ(17 / σ_combinado) donde σ_combinado = √(2) × σ

---

## Implementación recomendada: σ tiempo-variable

```javascript
// En el loop de Monte Carlo, reemplazar:
// let ballM = 50 + randn()*4;
// let ballK = 33 + randn()*4;

// Por:
const diasRef = 90; // ancla: 90 días antes de la elección
const sigmaBallBase = 4; // σ base cuando ya está cerca
const sigmaBall = Math.max(
    sigmaBallBase,
    sigmaBallBase * Math.sqrt(diasParaEleccion / diasRef)
);
// A 570 días: 4 × √(570/90) = 4 × 2.52 ≈ 10pp → P ≈ 88%
// A  90 días: 4 × 1 = 4pp → P ≈ 99.9% (igual que ahora)
// A   0 días: 4pp (capped por Math.max)

let ballM = 50 + randn() * sigmaBall;
let ballK = 33 + randn() * sigmaBall;
```

### Propiedades del cambio
- **Convergente:** a medida que se acerca la elección, el modelo automáticamente gana precisión
- **Calibrado:** anclado a σ=4 en los últimos 90 días (período donde las encuestas son más estables)
- **Consistente con la literatura:** el random walk √(días) es el estándar de Gelman/Morris/Silver

---

## Recomendación para el equipo Redlines

> **Cambiar σ_ballotage de fijo (4) a tiempo-variable (4 × √(días/90), mínimo 4).**
>
> Fundamento: la literatura electoral establece que la incertidumbre crece con √(días). Con σ=4 fijo a 18 meses, el modelo implica una precisión inexistente — las propias encuestas de 2ª vuelta tienen una dispersión de 22pp entre consultoras. Con σ tiempo-variable, P(Milei gana ballotage) baja de 99.9% a ~88%, lo cual es metodológicamente más honesto y da una señal más útil al lector.
>
> El cambio no altera la dirección del resultado (Milei sigue siendo favorito), pero comunica correctamente el nivel de incertidumbre.

---

## Fuentes

- Gelman et al. (2024) — [Grappling with Uncertainty in Forecasting the 2024 U.S. Presidential Election](https://hdsr.mitpress.mit.edu/pub/yoa73r1m)
- Gelman & Morris (2020) — [An Updated Dynamic Bayesian Forecasting Model](https://hdsr.mitpress.mit.edu/pub/nw1dzd02)
- Gelman (2020) — [Thinking about election forecast uncertainty](https://statmodeling.stat.columbia.edu/2020/07/31/thinking-about-election-forecast-uncertainty/)
- Linzer (2013) — [Dynamic Bayesian Forecasting of Presidential Elections](https://www.cambridge.org/core/journals/political-analysis/article/forecasting-elections-in-multiparty-systems-a-bayesian-approach-combining-polls-and-fundamentals/CA929544F672A09A0E34C5529EBFA482)
- El Destape (mar-2026) — [Alaska/TZ: Massa ganaría ballotage hoy](https://www.eldestapeweb.com/politica/elecciones-2027/milei-se-hunde-en-las-encuestas-como-saldria-el-ballotage-con-massa-si-se-hiciera-hoy-202632818131)
