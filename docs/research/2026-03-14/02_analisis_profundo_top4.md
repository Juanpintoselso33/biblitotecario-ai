# Análisis Profundo: Los 4 Agregadores más Sofisticados
**Research date:** 14 de marzo de 2026

---

## 1. FiveThirtyEight (ABC News) / G. Elliott Morris

### Arquitectura del polling average

FiveThirtyEight combina dos modelos en paralelo y los mezcla adaptativamente:

**EWMA (Exponentially Weighted Moving Average)**
Calcula un promedio para cada día ponderando exponencialmente por antigüedad. El parámetro `decay` controla la velocidad de olvido.

**Regresión polinomial local con kernel gaussiano**
Similar a LOWESS. Parámetros: bandwidth del kernel y grado del polinomio (0, 1 o 2). Detecta movimiento más rápido que el EWMA.

**Mezcla adaptativa**
El peso relativo de cada modelo depende de:
- Cantidad de encuestas en el último mes (más polls = más peso al polinomial)
- Performance relativa en los últimos 5 días (via maximum likelihood estimation)

### Pollster ratings (fórmula clave)

```
prior = 0.66 - quality * 0.57 + min(18, disc_pollcount) * (-0.03)
```

El peso de cada encuesta se calcula como:
```
peso = factor_muestra * rating_consultora * factor_recencia
factor_muestra = (sample / 600)^0.5   // cap en 1500
```

### Penalidad por herding

FiveThirtyEight penaliza consultoras que "copian" resultados ajustándose al promedio existente:
```
herding_penalty = 0.5 * (ADPA_real - ADPA_mínimo_teórico)
```
Donde ADPA = Average Distance from Polling Average.

### Corrección house effects

- Comparan resultados de una consultora con otras contemporáneas en la misma carrera
- Polls más viejos reciben 1/10 del peso de los del ciclo actual
- Polls partidarios: prior de ~4pp de sesgo hacia el partido sponsor

### Críticas y evoluciones

| Año | Crítica | Respuesta |
|-----|---------|-----------|
| 2016 | Único modelo en dar ~30% a Trump | Aun así fue el más preciso |
| 2020 | Error sistemático pro-Demócrata en polls estatales | Aumentaron correlación asumida entre estados |
| 2022 | — | Error promedio 4.8pp, el más preciso históricamente |
| 2024 | — | Error promedio 4.5pp |

---

## 2. Silver Bulletin (Nate Silver)

### Diferencias clave con FiveThirtyEight

Silver y 538 comparten ADN pero divergen en puntos críticos:

1. **No es Bayesiano:** Silver usa un enfoque más "tradicional" de ajustar promedios y simular. 538 bajo Morris es fully Bayesian.
2. **Más énfasis en error sistemático:** Silver calibra usando la distribución histórica de errores. Su modelo asume error sistemático real ~2.5-4.5pp nacional.
3. **80.000 simulaciones:** Más que la mayoría de modelos, para capturar colas de distribución.

### Métricas de consultoras

| Métrica | Descripción |
|---------|-------------|
| Simple Average Error | Diferencia entre resultado de la encuesta y margen real |
| Simple Plus-Minus | Error simple menos error esperado (tipo de carrera, días al E-Day, sample size) |
| Advanced Plus-Minus | Ajuste por performance de otras firmas en las mismas carreras |
| Mean-Reverted Adv. PM | Regresión a la media según cantidad de polls y recencia |

### Elasticidad estatal (concepto propio)

Algunos estados son más "elásticos" (más swing voters, más movimiento con el clima nacional). Calculado de microdatos del CES:
```
Rango: Mississippi 0.90 (inelástico) ↔ Alaska 1.23 / Hawaii 1.25 (elástico)
```

**Lección para el Votómetro:** Este enfoque podría adaptarse para Argentina a nivel provincial/regional. Si no hay encuestas recientes de una provincia pero el clima nacional se movió, se podría inferir el movimiento provincial usando "elasticidades" calculadas de elecciones pasadas.

---

## 3. The Economist (Andrew Gelman / Columbia University)

### El modelo más académicamente riguroso

Implementado en R + Stan, con papers peer-reviewed en Harvard Data Science Review.

### Arquitectura de tres capas

**Capa 1 — Prior de fundamentals:**
- Crecimiento de ingreso personal
- Aprobación presidencial
- Incumbencia (con ajuste por polarización creciente)
- Produce un prior multivariado para los resultados

**Capa 2 — Modelo de polls (Bayesiano jerárquico dinámico):**
- Trata la opinión pública como un random walk correlacionado
- Incorpora house effects como parámetros estimados
- Modela no-respuesta diferencial (qué partisanos responden más en cada momento)

**Capa 3 — Combinación endógena:**
- Lejos de la elección: más peso a fundamentals
- Cerca de la elección: más peso a polls
- La transición es endógena al modelo (no fijada a mano)

### Innovaciones 2024

- Mejor estimación de correlaciones en errores de encuestas
- Ajuste por la importancia decreciente de la economía en electorados polarizados
- Más error de no-muestreo incorporado

### Código público disponible

- `github.com/TheEconomist/2021-germany-election-model-PUBLIC`
- `github.com/TheEconomist/2022-france-election-model`
- Paper: Heidemanns, Gelman & Morris (2020) en HDSR

**Lección para el Votómetro:** El framework Bayesiano jerárquico puede extraer señales de información combinando múltiples fuentes. El prior de fundamentals + polls es el núcleo replicable.

---

## 4. Electoral Calculus (UK) — MRP

### MRP: Multilevel Regression and Post-stratification

**Paso 1 — Regresión multinivel:** Estima la probabilidad de voto de cada tipo demográfico usando datos de encuestas nacionales.

**Paso 2 — Post-estratificación:** Aplica esas probabilidades al perfil demográfico real de cada circunscripción (del censo).

**Resultado:** Proyección a nivel circunscripción a partir de encuestas nacionales.

### Relevancia para Argentina

El sistema electoral argentino opera a nivel nacional (no por distritos como UK/EE.UU.), por lo que MRP es menos directamente aplicable. Sin embargo, la técnica podría usarse para:
- Estimar resultados **provinciales** a partir de encuestas nacionales
- Ajustar por composición demográfica diferencial de las muestras (mayor representación de CABA/GBA en encuestas online)
