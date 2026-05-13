# Investigacion Exhaustiva: Agregadores de Encuestas Electorales del Mundo

## Aplicaciones al Votometro Argentina 2027

**Fecha:** 14 de marzo de 2026
**Objetivo:** Identificar metodologias, tecnicas y features de los principales agregadores mundiales que puedan mejorar la calidad predictiva del Votometro.

---

## 1. Tabla Comparativa de Agregadores

| Agregador | Pais | Ponderacion de encuestas | Modelo de incertidumbre | Correccion house effects | Fundamentals | Transparencia | Codigo publico |
|---|---|---|---|---|---|---|---|
| **FiveThirtyEight (ABC News)** | EE.UU. | Multiplicativa: (n/600)^0.5 x rating consultora x recencia. Cap en n=1500. EWMA + regresion polinomial local con kernel | MCMC, decenas de miles de simulaciones. Errores correlacionados entre estados | BD historica desde 1998. Comparacion within-race. Polls partidarios: prior de 4pp de sesgo | Si: economia, aprobacion presidencial, incumbencia. Reducido si incumbente no se presenta | Alta: articulos metodologicos extensos | Parcial (formulas publicas, no todo el codigo) |
| **Silver Bulletin (Nate Silver)** | EE.UU. | Simple/Advanced Plus-Minus, mean-reverted. Desenfasis del sample size. Cap por firma para evitar dominancia | 80.000 simulaciones. Calibracion empirica con error historico real (~2.5-4.5pp nacional) | Mean-reverted bias desde 1998. Distincion explicita entre house effect y bias real | Elasticidad estatal, inferencia nacional-estado. Transferencia cross-state | Alta: explainers detallados de metodologia y ratings | No (explicaciones extensas pero codigo privado) |
| **The Economist** | EE.UU./Global | (n/600)^0.5. Toplines, no microdata | Bayesiano jerarquico dinamico en R/Stan con MCMC. Correlacion entre estados y variacion temporal | Modelado explicito. Errores compartidos entre consultoras. No-respuesta diferencial | Si: prior multivariado desde economia, aprobacion, polarizacion. Blend con polls via estructura jerarquica | Muy alta: papers en Harvard Data Science Review | Si: repositorios GitHub para Alemania 2021, Francia 2022, EE.UU. 2020 |
| **RealClearPolitics** | EE.UU. | **Ninguna**: promedio aritmetico simple. Seleccion editorial de encuestas | Ninguno: solo toplines sin probabilidades ni intervalos | Ninguna: la seleccion editorial sustituye ajustes formales | No incorporados | Baja: criterios de inclusion no formalizados | No |
| **Polling Observatory (U. Manchester)** | Reino Unido | Agregacion historica de series temporales. Sin fundamentals | Enfasis en distinguir ruido vs tendencia. Sin simulaciones documentadas | No formalizado en material publico | Explicitamente NO incorporados (ni aprobacion ni economia) | Media: posts en blog universitario | No |
| **Electoral Calculus** | Reino Unido | MRP (Multilevel Regression and Post-stratification). n_eff = (Sum w_i)^2 / Sum w_i^2 | Incertidumbre via varianza del MRP a nivel circunscripcion | Ponderacion demografica/politica en survey weighting, no correccion multi-ciclo separada | Demographics + voto pasado para mapear swing nacional a circunscripciones | Media-alta: metodologia de muestreo publicada por proyecto | No |
| **AS-COA Poll Trackers** | Latam | Compilacion visual de encuestas por pais (Peru, Colombia, Brasil, Costa Rica). Sin ponderacion formal documentada | No modelado explicitamente | No documentado | No incorporados | Baja: presentacion descriptiva | No |
| **AtlasIntel / Latam Pulse** | Latam | Reclutamiento digital aleatorio. Encuestas propias, no agregacion | Margen de error clasico SRS | N/A (encuestadora, no agregador) | No | Media: fichas tecnicas publicadas | No |
| **Wikipedia Poll Aggregators** | Europa | Compilacion crowdsourced. Algunos con promedios simples | Ninguno formal | No | No | Variable | No |

### Hallazgo clave: No existe un agregador formal de encuestas para Argentina 2027

Las encuestas argentinas para 2027 se publican individualmente por consultoras (Trends, Opinaia, CB, Proyeccion, DC Consultores, Isasi-Burdman) y son compiladas por periodistas (Clarin, iProfesional), pero **no hay un agregador con metodologia estadistica formal**. El Votometro de CIGOB es, hasta donde la investigacion pudo determinar, **el unico proyecto de agregacion ponderada para Argentina**.

---

## 2. Analisis Profundo de los Top 4

### 2.1 FiveThirtyEight (ABC News) / G. Elliott Morris

**Arquitectura del polling average:**

FiveThirtyEight combina dos modelos en paralelo y los mezcla adaptativamente:

1. **EWMA (Exponentially Weighted Moving Average):** Calcula un promedio para cada dia ponderando exponencialmente por antigueedad. El parametro `decay` controla la velocidad de olvido.

2. **Regresion polinomial local con kernel gaussiano:** Similar a LOWESS. Parametros: bandwidth del kernel y grado del polinomio (0, 1 o 2). Detecta movimiento mas rapido que el EWMA.

3. **Mezcla adaptativa:** El peso relativo de cada modelo depende de:
   - Cantidad de encuestas en el ultimo mes (mas polls = mas peso al polinomial)
   - Performance relativa en los ultimos 5 dias (via maximum likelihood estimation)

**Pollster ratings (formulas clave):**

```
prior = 0.66 - quality * 0.57 + min(18, disc_pollcount) * (-0.03)
```

Donde `quality = 1` si cumple estandar AAPOR/Roper, `disc_pollcount` es conteo de polls con descuento temporal.

El peso de cada encuesta se calcula como:

```
peso = factor_muestra * rating_consultora * factor_recencia
factor_muestra = (sample / 600)^0.5   // cap en 1500
```

**Penalidad por herding:**

FiveThirtyEight penaliza consultoras que "copian" resultados ajustandose al promedio existente:

```
herding_penalty = 0.5 * (ADPA_real - ADPA_minimo_teorico)
```

Donde ADPA = Average Distance from Polling Average.

**Correccion house effects:**

- Comparan resultados de una consultora con otras contemporaneas en la misma carrera
- Polls mas viejos reciben 1/10 del peso de los del ciclo actual
- Polls partidarios: prior de ~4pp de sesgo hacia el partido sponsor

**Incertidumbre:**

- MCMC (Markov Chain Monte Carlo) para generar decenas de miles de escenarios
- Errores correlacionados entre estados (mas fuerte para presidenciales que para congresistas)
- El modelo reduce el peso del sample size relativo a otros factores basado en evidencia empirica

**Criticas y como las resolvieron:**

- **2016:** Fue el unico modelo grande que le dio ~30% a Trump (otros daban <10%). Aun asi recibio criticas por ser el mas famoso.
- **2020:** Error sistematico pro-Democrata en polls estatales. Respondieron aumentando correlacion asumida entre estados.
- **2022:** Las encuestas fueron las mas precisas historicamente (error promedio 4.8pp).
- **2024:** Error promedio general de 4.5pp, el mas bajo en su base de datos.

### 2.2 Silver Bulletin (Nate Silver)

**Diferencias clave con FiveThirtyEight:**

Silver y 538 comparten ADN pero divergen en puntos criticos:

1. **No es Bayesiano:** Silver usa un enfoque mas "tradicional" de ajustar promedios estatales, aplicar correcciones, y luego simular. 538 bajo Morris es fully Bayesian (prior + evidence = posterior).

2. **Mas enfasis en error sistematico:** Silver calibra explicitamente usando la distribucion historica de errores de encuestas. Su modelo asume que el error sistematico real es ~2.5-4.5pp a nivel nacional.

3. **80.000 simulaciones:** Mas que la mayoria de modelos, para capturar colas de distribucion.

**Metricas de consultoras:**

| Metrica | Descripcion |
|---|---|
| Simple Average Error | Diferencia entre resultado de la encuesta y margen real |
| Simple Plus-Minus | Error simple menos error esperado dadas las condiciones (tipo de carrera, dias al dia E, sample size) |
| Advanced Plus-Minus | Ajuste adicional por performance de otras firmas en las mismas carreras |
| Mean-Reverted Adv. PM | Regresion a la media segun cantidad de polls y recencia |

**Elasticidad estatal:**

Concepto propio: algunos estados son mas "elasticos" (mas swing voters, mas movimiento con el clima nacional). Calculado de microdatos del CES (Cooperative Election Study, 60.000 encuestados):

```
Rango: Mississippi 0.90 (muy inelastico) - Alaska 1.23 / Hawaii 1.25 (muy elastico)
```

**Inferencia cross-state:**

Si Arizona no tiene encuestas recientes pero el clima nacional cambio en base a otros estados, el modelo ajusta la estimacion de Arizona. Esto es especialmente valioso cuando hay pocos datos.

**Leccion para el Votometro:** Este enfoque podria adaptarse para Argentina a nivel provincial/regional. Si no hay encuestas recientes de una provincia pero el clima nacional se movio, se podria inferir el movimiento provincial usando "elasticidades" calculadas de elecciones pasadas.

### 2.3 The Economist (Andrew Gelman / Columbia University)

**El modelo mas academicamente riguroso:**

Implementado en R + Stan, con papers peer-reviewed en Harvard Data Science Review.

**Arquitectura:**

1. **Prediccion por fundamentals:**
   - Crecimiento de ingreso personal
   - Aprobacion presidencial
   - Incumbencia (con ajuste por polarizacion creciente)
   - Produce un prior multivariado para los resultados estatales

2. **Modelo de polls:**
   - Bayesiano jerarquico dinamico
   - Trata la opinion publica como un random walk correlacionado entre estados
   - Incorpora house effects como parametros estimados
   - Modela no-respuesta diferencial (que partisanos responden mas en cada momento)

3. **Combinacion:**
   - El prior de fundamentals se actualiza con los polls via Bayes
   - Lejos de la eleccion: mas peso a fundamentals
   - Cerca de la eleccion: mas peso a polls
   - La transicion es endogena al modelo

**Innovaciones clave (2024):**

- Mejor estimacion de correlaciones estado-estado en errores de encuestas
- Ajuste por la importancia decreciente de la economia como factor predictivo en electorados polarizados
- Mas error de no-muestreo (non-sampling error) incorporado

**Codigo publico:**

- GitHub: `TheEconomist/2021-germany-election-model-PUBLIC`
- GitHub: `TheEconomist/2022-france-election-model`
- Paper: Heidemanns, Gelman & Morris (2020) en HDSR

**Leccion para el Votometro:** El modelo de The Economist demuestra que incluso con pocos datos (como Argentina), un framework Bayesiano jerarquico puede extraer senales de informacion combinando multiples fuentes. El Votometro podria incorporar un prior de fundamentals (economia, aprobacion presidencial) que se vaya actualizando con las encuestas.

### 2.4 Electoral Calculus (UK) - MRP

**MRP (Multilevel Regression and Post-stratification):**

1. **Paso 1 - Regresion multinivel:** Estima la probabilidad de voto de cada tipo demografico usando datos de encuestas nacionales.

2. **Paso 2 - Post-estratificacion:** Aplica esas probabilidades al perfil demografico real de cada circunscripcion (del censo).

3. **Resultado:** Proyeccion a nivel circunscripcion/distrito a partir de encuestas nacionales.

**Relevancia para Argentina:**

El sistema electoral argentino con PASO + primera vuelta + ballotage opera a nivel nacional (no por distritos como UK/EE.UU.), por lo que MRP es menos directamente relevante. Sin embargo, la tecnica podria aplicarse para:
- Estimar resultados provinciales a partir de encuestas nacionales
- Ajustar por composicion demografica diferencial de las muestras

---

## 3. Features que el Votometro NO Tiene (ordenadas por impacto potencial)

### Impacto ALTO

| # | Feature | Quien la usa | Que aporta | El Votometro hoy |
|---|---|---|---|---|
| 1 | **Trend line (regresion local/EWMA)** | 538, Silver, Economist | Muestra la tendencia subyacente, no solo el promedio puntual. Distingue senal de ruido. | Solo promedio ponderado estatico |
| 2 | **Correcciones house effects formales** | 538, Silver, Economist | Ajusta automaticamente por sesgo sistematico de cada consultora | Tiene "sesgo historico" como factor de ponderacion, pero no corrige el valor de la encuesta |
| 3 | **Intervalos de confianza / bandas de incertidumbre** | 538, Silver, Economist | Comunica la incertidumbre al usuario. Evita falsa precision. | No muestra intervalos de confianza visuales |
| 4 | **Fundamentals-based prior** | 538, Silver, Economist | Ancla las estimaciones cuando hay pocas encuestas o estan muy dispersas | No: solo usa encuestas |
| 5 | **Calibracion empirica de incertidumbre** | Silver, 538 | Usa el error REAL historico (no teorico) para dimensionar sigma | sigma=6.5 es correcto para Argentina pero no se actualiza ni desagrega |

### Impacto MEDIO

| # | Feature | Quien la usa | Que aporta | El Votometro hoy |
|---|---|---|---|---|
| 6 | **Penalidad por herding** | 538 | Detecta y penaliza consultoras que "copian" resultados del promedio existente | No implementado |
| 7 | **Actualizacion diaria automatica** | 538, Economist | Incorpora encuestas nuevas sin intervencion manual | Datos hardcodeados en HTML |
| 8 | **Inferencia cross-regional** | Silver (elasticidad estatal) | Si no hay encuesta de una region, infiere de otras | No aplica (opera solo a nivel nacional) |
| 9 | **Ajuste registered vs likely voters** | 538, Silver | Distingue poblacion encuestada y ajusta diferencia | No documentado |
| 10 | **Descomposicion bias vs varianza** | Gelman et al. | Permite entender si el error es aleatorio o sistematico | No descompuesto |

### Impacto BAJO (pero deseable)

| # | Feature | Quien la usa | Que aporta | El Votometro hoy |
|---|---|---|---|---|
| 11 | **Base de datos descargable** | 538, Silver | Transparencia total, verificabilidad | No disponible |
| 12 | **Visualizacion de incertidumbre tipo dot-plot** | 538, Economist | Mas intuitivo que barras de error | No tiene |
| 13 | **Simulacion de escenarios** | Economist (BridgeStan) | "Que pasa si las encuestas estan sesgadas X puntos?" | No implementado |

---

## 4. Propuestas Concretas de Mejora para el Votometro

### MEJORA 1: Implementar Trend Line con EWMA + Regresion Local

**Descripcion tecnica:**

Reemplazar el promedio ponderado estatico por un sistema dual:
- **EWMA:** Para producir un promedio estable que se actualice incrementalmente
- **Regresion polinomial local:** Para capturar cambios rapidos cuando hay muchos datos nuevos
- **Mezcla adaptativa:** Mas peso al EWMA con pocas encuestas, mas al polinomial con muchas

**Esfuerzo de implementacion:** MEDIO
**Impacto metodologico:** ALTO

**Ejemplo de implementacion en JavaScript:**

```javascript
// EWMA (Exponentially Weighted Moving Average)
function calcularEWMA(encuestas, decay = 0.05) {
  // Ordenar por fecha (mas reciente primero)
  const sorted = [...encuestas].sort((a, b) => b.fecha - a.fecha);
  const hoy = new Date();

  let sumaPesos = 0;
  let sumaValores = 0;

  sorted.forEach(enc => {
    const diasAtras = (hoy - enc.fecha) / (1000 * 60 * 60 * 24);
    const peso = Math.exp(-decay * diasAtras) * enc.pesoBase;
    sumaPesos += peso;
    sumaValores += enc.valor * peso;
  });

  return sumaPesos > 0 ? sumaValores / sumaPesos : null;
}

// Regresion polinomial local con kernel gaussiano
function regresionLocalKernel(encuestas, fechaObjetivo, bandwidth = 30, grado = 1) {
  // bandwidth en dias, grado 0=constante, 1=lineal, 2=cuadratico
  const t0 = fechaObjetivo.getTime();

  // Calcular pesos del kernel gaussiano
  const datos = encuestas.map(enc => {
    const t = enc.fecha.getTime();
    const diasDif = (t - t0) / (1000 * 60 * 60 * 24);
    const u = diasDif / bandwidth;
    const kernelPeso = Math.exp(-0.5 * u * u) * enc.pesoBase;
    return { t: diasDif, valor: enc.valor, peso: kernelPeso };
  }).filter(d => d.peso > 0.001); // Filtrar pesos negligibles

  if (datos.length < grado + 1) return null;

  // Regresion ponderada (WLS) via ecuaciones normales
  // Para grado 1: y = a + b*t
  // Resolver sistema de ecuaciones normales ponderadas
  if (grado === 0) {
    let sw = 0, swy = 0;
    datos.forEach(d => { sw += d.peso; swy += d.peso * d.valor; });
    return swy / sw;
  }

  if (grado === 1) {
    let sw = 0, swt = 0, swt2 = 0, swy = 0, swty = 0;
    datos.forEach(d => {
      sw += d.peso;
      swt += d.peso * d.t;
      swt2 += d.peso * d.t * d.t;
      swy += d.peso * d.valor;
      swty += d.peso * d.t * d.valor;
    });
    const det = sw * swt2 - swt * swt;
    if (Math.abs(det) < 1e-10) return swy / sw;
    const a = (swt2 * swy - swt * swty) / det;
    return a; // Valor estimado en t=0 (la fecha objetivo)
  }

  return null;
}

// Mezcla adaptativa (como 538)
function promedioAdaptativo(encuestas, fecha, ventanaMes = 30) {
  const ewma = calcularEWMA(encuestas);
  const poly = regresionLocalKernel(encuestas, fecha);

  // Contar encuestas en el ultimo mes
  const recientes = encuestas.filter(e =>
    (fecha - e.fecha) / (1000*60*60*24) <= ventanaMes
  ).length;

  // Mas encuestas recientes = mas peso al polinomial
  const pesoPoly = Math.min(0.8, recientes / 15); // Satura en ~15 encuestas
  const pesoEWMA = 1 - pesoPoly;

  if (poly === null) return ewma;
  return pesoEWMA * ewma + pesoPoly * poly;
}
```

### MEJORA 2: Correccion Formal de House Effects

**Descripcion tecnica:**

En lugar de usar "sesgo historico" como peso multiplicativo (que reduce la influencia de encuestas sesgadas pero no corrige su valor), implementar una correccion aditiva que ajuste el valor reportado.

**Metodo:**

1. Para cada consultora con historial, calcular la diferencia sistematica entre sus resultados y el promedio de otras consultoras en el mismo periodo.
2. Almacenar este "house effect" (ej: Consultora X tiende a darle +3pp a LLA).
3. Al incorporar una nueva encuesta de esa consultora, restar el house effect del valor reportado.
4. Mean-revert: con pocas encuestas historicas, asumir house effect cercano a 0.

**Esfuerzo de implementacion:** BAJO
**Impacto metodologico:** ALTO

**Ejemplo de implementacion:**

```javascript
// Base de datos de house effects por consultora
const houseEffects = {
  // house_effect = sesgo promedio de la consultora vs otras contemporaneas
  // Positivo = le da mas a LLA de lo que dan las demas
  // Se calcula de las legislativas 2025 y encuestas 2024-2026
  'Opinaia':     { lla: +2.1, pj: -1.8, n_polls: 12 },
  'Trends':      { lla: +0.5, pj: +0.3, n_polls: 8 },
  'CB':          { lla: -1.2, pj: +0.8, n_polls: 15 },
  'DC':          { lla: +0.8, pj: -0.5, n_polls: 6 },
  'Proyeccion':  { lla: -0.3, pj: +0.2, n_polls: 10 },
  'Isasi':       { lla: +1.5, pj: -1.0, n_polls: 4 },
  'Zuban':       { lla: -2.5, pj: +2.0, n_polls: 18 },
  'Atlas':       { lla: +1.0, pj: -0.7, n_polls: 7 },
};

function corregirHouseEffect(valorEncuesta, consultora, partido) {
  const he = houseEffects[consultora];
  if (!he) return valorEncuesta; // Sin datos, no corregir

  // Mean reversion: con pocos datos, atenuar la correccion
  // Factor de confianza basado en cantidad de polls historicos
  const factorConfianza = Math.min(1.0, he.n_polls / 15);

  const correccion = (he[partido] || 0) * factorConfianza;
  return valorEncuesta - correccion;
}

// Ejemplo: Si Opinaia reporta LLA=44%, el valor corregido seria:
// 44 - (2.1 * min(1, 12/15)) = 44 - 1.68 = 42.32%
```

### MEJORA 3: Bandas de Incertidumbre Visuales

**Descripcion tecnica:**

Mostrar un intervalo de confianza alrededor del promedio ponderado que refleje:
1. La dispersion de las encuestas entre si
2. El error historico de las encuestas argentinas vs resultado real
3. La cantidad de encuestas disponibles (menos encuestas = banda mas ancha)

**Esfuerzo de implementacion:** BAJO
**Impacto metodologico:** ALTO (en comunicacion de resultados)

**Ejemplo de implementacion:**

```javascript
function calcularBandaIncertidumbre(encuestas, promedioActual) {
  // 1. Dispersion entre encuestas (desviacion estandar ponderada)
  let sumPesos = 0, sumPesosDifCuad = 0;
  encuestas.forEach(e => {
    sumPesos += e.peso;
    sumPesosDifCuad += e.peso * Math.pow(e.valor - promedioActual, 2);
  });
  const sdEncuestas = Math.sqrt(sumPesosDifCuad / sumPesos);

  // 2. Error historico argentino (calibrado empiricamente)
  // PASO 2023: error promedio ~5pp, General 2023: ~3.5pp
  // Legislativas 2025: ~2pp
  const errorHistorico = 3.5; // pp, promedio ponderado reciente

  // 3. Factor por cantidad de encuestas
  const n = encuestas.length;
  const factorN = 1 + 2 / Math.sqrt(n); // Se achica con mas datos

  // 4. Combinar fuentes de incertidumbre
  const incertidumbreTotal = Math.sqrt(
    Math.pow(sdEncuestas, 2) +
    Math.pow(errorHistorico, 2)
  ) * factorN;

  // Intervalo 90% (1.645 sigmas)
  return {
    bajo90: promedioActual - 1.645 * incertidumbreTotal,
    alto90: promedioActual + 1.645 * incertidumbreTotal,
    // Intervalo 50% (0.674 sigmas) - "rango mas probable"
    bajo50: promedioActual - 0.674 * incertidumbreTotal,
    alto50: promedioActual + 0.674 * incertidumbreTotal,
    sigma: incertidumbreTotal
  };
}

// Con LLA ~41% y ~15 encuestas recientes:
// sdEncuestas ~ 3pp, errorHistorico = 3.5pp
// incertidumbre = sqrt(9 + 12.25) * (1 + 2/sqrt(15)) = 4.6 * 1.52 = ~7pp
// Intervalo 90%: 41 +/- 11.5pp => [29.5%, 52.5%]
// Intervalo 50%: 41 +/- 4.7pp => [36.3%, 45.7%]
```

**Visualizacion sugerida:** Usar un area sombreada alrededor de la trend line, con dos niveles de opacidad (50% y 90% de confianza), similar a como lo hace The Economist.

### MEJORA 4: Prior de Fundamentals

**Descripcion tecnica:**

Incorporar un "ancla" basada en variables politico-economicas que ayude cuando hay pocas encuestas o mucha dispersion. Para Argentina, las variables relevantes serian:

1. **Aprobacion presidencial** (dato mensual, multiples fuentes)
2. **Situacion economica percibida** (optimismo/pesimismo)
3. **Resultado de la ultima eleccion** (legislativas 2025: LLA ~47%, PJ ~30%)
4. **Incumbencia** (Milei busca reeleccion: historicamente ventajoso)

**Metodo simplificado (sin Bayesiano completo):**

```javascript
function calcularPriorFundamentals() {
  // Baseline: resultado legislativas 2025 (ajustado por tipo de eleccion)
  const baselineLLA = 47; // Resultado legislativas 2025
  const baselinePJ = 30;

  // Ajuste por aprobacion (regresion historica argentina)
  // Aprobacion actual: ~50% positiva (dato Trends ene-2026)
  const aprobacion = 50;
  const ajusteAprobacion = (aprobacion - 45) * 0.3; // +0.3pp por cada punto arriba de 45%

  // Ajuste por incumbencia en reeleccion (historico argentino)
  // Menem 1995, CFK 2011 mostraron ventaja de ~3-5pp
  const bonoIncumbencia = 2; // pp, conservador

  // Ajuste por economia (si hay datos de expectativa economica)
  const optimismo = 45; // % que espera mejora
  const ajusteEconomia = (optimismo - 40) * 0.2;

  return {
    lla: baselineLLA + ajusteAprobacion + bonoIncumbencia + ajusteEconomia,
    pj: baselinePJ - ajusteAprobacion * 0.5 // Correlacion negativa parcial
  };
}

function blendPollsYFundamentals(promedioPollsLLA, promedioPollsPJ, diasParaEleccion) {
  const fundamentals = calcularPriorFundamentals();

  // Peso de fundamentals: alto cuando falta mucho, bajo cuando falta poco
  // Inspirado en The Economist
  const pesoFundamentals = Math.min(0.5, diasParaEleccion / 1000);
  const pesoPolls = 1 - pesoFundamentals;

  return {
    lla: pesoPolls * promedioPollsLLA + pesoFundamentals * fundamentals.lla,
    pj: pesoPolls * promedioPollsPJ + pesoFundamentals * fundamentals.pj
  };
}

// A 500 dias de la eleccion (mar 2026):
// pesoFundamentals = 0.5, pesoPolls = 0.5
// Si polls dicen LLA=41, fundamentals dicen LLA=50.5
// Blend: 0.5*41 + 0.5*50.5 = 45.75

// A 30 dias de la eleccion:
// pesoFundamentals = 0.03, pesoPolls = 0.97
// Blend: 0.97*41 + 0.03*50.5 = 41.3 (casi todo polls)
```

**Esfuerzo de implementacion:** MEDIO
**Impacto metodologico:** ALTO (especialmente ahora, a >500 dias de la eleccion)

### MEJORA 5: Sistema de Rating de Consultoras Argentinas

**Descripcion tecnica:**

Crear un sistema de calificacion formal de consultoras argentinas basado en su performance historica, similar al Pollster Rating de FiveThirtyEight/Silver.

**Variables para el rating:**

```javascript
const calcularRatingConsultora = (consultora) => {
  // 1. Error promedio historico (PASO 2023 + General 2023 + Legislativas 2025)
  // Ponderacion: 50% al ciclo mas reciente, 25% al anterior, etc.

  // 2. Sesgo (bias): tendencia sistematica hacia un partido
  // Un bias alto no es tan malo si es consistente y se puede corregir

  // 3. Metodologia (bonus)
  //   +0.2 si es presencial (mejor que solo online en Argentina)
  //   +0.1 si tiene muestra > 2000
  //   +0.1 si publica ficha tecnica completa
  //   -0.2 si es solo IVR/robotizada

  // 4. Transparencia
  //   +0.1 si publica cruces demograficos
  //   +0.1 si publica ficha con detalle de muestreo

  // 5. Herding penalty (si se acercan mucho al promedio existente)

  // Output: score 0-3, donde 3 = mejor
};

// Ratings estimados basados en performance 2023-2025:
const ratingsConsultoras = {
  'DC Consultores':  2.5,  // Mas precisa en general 2023 (+0.36 error LLA)
  'CB Consultora':   2.3,  // Consistentemente cercana
  'Atlas Intel':     2.0,  // Buena muestra, metodologia digital solida
  'Opinaia':         1.8,  // Pionera online, tendencia a sobreestimar oficialismo
  'Trends':          1.7,  // Reciente, buenos datos pero poco historial
  'Proyeccion':      1.6,  // Aceptable
  'Zuban Cordoba':   1.5,  // Errores significativos en PASO 2023
  'Nueva Comunicacion': 1.0, // Error grande en PBA 2023
  'Equipo Mide':     1.8,  // Le dio alto a Milei antes de PASO (buena senal)
};
```

**Esfuerzo de implementacion:** MEDIO (requiere recopilar datos historicos)
**Impacto metodologico:** MEDIO-ALTO

### MEJORA 6: Modelo de Voto Oculto Mejorado

**Contexto argentino:**

Las PASO 2023 mostraron que el voto a Milei estaba sistematicamente subestimado en las encuestas. Las posibles causas:

1. **Voto oculto clasico:** Encuestados no declaran su voto real (por verguenza social, desconfianza)
2. **Sesgo de no-respuesta:** Los votantes de Milei son menos propensos a responder encuestas (jovenes, desafectos, sectores populares desconectados de la politica tradicional)
3. **Sesgo de muestra:** Las encuestas online/telefonicas no llegan a ciertos segmentos que votan LLA

**Mejora propuesta:**

Reemplazar la correccion fija actual (+4pp LLA, +2pp PJ para polls tipo candidato) por un modelo calibrado que se actualice:

```javascript
function correccionVotoOculto(partido, tipoEncuesta, anio) {
  // Base: calibracion con resultados reales
  const calibracion = {
    // PASO 2023: LLA subestimado ~8pp promedio, PJ sobreestimado ~3pp
    // General 2023: LLA subestimado ~4pp, PJ subestimado ~1pp
    // Legislativas 2025: LLA subestimado ~2pp, PJ ~0
    // Tendencia: el sesgo se reduce a medida que LLA se "normaliza"
    'LLA': {
      base: 2.0,  // Reducido de 4pp: el "efecto sorpresa" ya no existe
      tendencia: -0.5,  // Se reduce 0.5pp por anio desde 2023
      factor_metodologia: {
        'online': 1.2,  // Sesgo mayor en online
        'telefonico': 1.0,
        'presencial': 0.6,  // Menor sesgo en presencial
        'mixto': 0.8
      }
    },
    'PJ': {
      base: 0.5,
      tendencia: -0.2,
      factor_metodologia: {
        'online': 0.8,
        'telefonico': 1.0,
        'presencial': 1.2,  // Presencial captura mejor el voto peronista
        'mixto': 1.0
      }
    }
  };

  const config = calibracion[partido];
  if (!config) return 0;

  const anosDesde2023 = anio - 2023;
  const baseAjustada = Math.max(0, config.base + config.tendencia * anosDesde2023);
  const factorMet = config.factor_metodologia[tipoEncuesta] || 1.0;

  return baseAjustada * factorMet;
}

// Para una encuesta online de LLA en 2026:
// base = max(0, 2.0 + (-0.5)*3) = max(0, 0.5) = 0.5pp
// factor = 1.2
// correccion = 0.5 * 1.2 = 0.6pp
// (vs los 4pp fijos actuales, que probablemente ya son excesivos)
```

**Esfuerzo de implementacion:** BAJO
**Impacto metodologico:** MEDIO

### MEJORA 7: Automatizacion de Actualizacion de Datos

**Descripcion tecnica:**

El problema mas critico del Votometro es que los datos estan hardcodeados en el HTML. Propuesta en dos fases:

**Fase 1 (sin backend): Archivo JSON externo**

```javascript
// encuestas.json - archivo separado actualizable
{
  "ultima_actualizacion": "2026-03-14",
  "encuestas": [
    {
      "id": 99,
      "consultora": "Trends",
      "fecha": "2026-01-16",
      "tipo": "espacio",
      "muestra": 2000,
      "metodologia": "online",
      "resultados": {
        "LLA": 43,
        "PJ": 32,
        "PU": 4,
        "Otros": 11,
        "Blanco": 4,
        "NSNC": 6
      },
      "ficha_tecnica": "2000 casos, CAWI, margen +-2.2%, 95% conf"
    }
  ]
}

// En el HTML, cargar asi:
async function cargarEncuestas() {
  const response = await fetch('encuestas.json');
  const data = await response.json();
  return data.encuestas;
}
```

**Fase 2 (con backend ligero): Google Sheets como base de datos**

```javascript
// Usar Google Sheets API para leer datos en vivo
const SHEET_ID = 'tu_sheet_id';
const API_KEY = 'tu_api_key';

async function cargarDesdeSheets() {
  const url = `https://sheets.googleapis.com/v4/spreadsheets/${SHEET_ID}/values/Encuestas!A:Z?key=${API_KEY}`;
  const response = await fetch(url);
  const data = await response.json();
  return parsearFilas(data.values);
}
```

**Esfuerzo de implementacion:** BAJO (Fase 1) / MEDIO (Fase 2)
**Impacto metodologico:** BAJO (no cambia la metodologia, pero habilita todas las demas mejoras)

### MEJORA 8: Penalidad por Herding

**Descripcion tecnica:**

Detectar consultoras que ajustan sus resultados para acercarse al consenso existente, en lugar de reportar lo que realmente miden.

```javascript
function calcularHerding(consultora, encuestasConsultora, todasLasEncuestas) {
  let distanciasTotales = 0;
  let n = 0;

  encuestasConsultora.forEach(enc => {
    // Calcular promedio de otras encuestas publicadas ANTES de esta
    // (con fecha de campo al menos 3 dias antes)
    const previas = todasLasEncuestas.filter(e =>
      e.consultora !== consultora &&
      e.fecha < new Date(enc.fecha.getTime() - 3 * 24*60*60*1000)
    );

    if (previas.length < 3) return; // Necesitamos al menos 3 encuestas previas

    const promedioLLA = previas.reduce((s, e) => s + e.lla, 0) / previas.length;
    const distancia = Math.abs(enc.lla - promedioLLA);
    distanciasTotales += distancia;
    n++;
  });

  if (n === 0) return 0;

  const ADPA = distanciasTotales / n; // Average Distance from Polling Average

  // Distancia minima teorica basada en error de muestreo
  const muestraPromedio = 2000;
  const ADPA_minimo = 1.5 * Math.sqrt(0.42 * 0.58 / muestraPromedio) * 100;
  // ~1.5 * 1.1 = ~1.65pp

  // Penalidad: mitad de la diferencia entre ADPA real y minimo
  const penalidad = Math.max(0, 0.5 * (ADPA_minimo - ADPA));

  return penalidad; // Positivo = sospecha de herding
}
```

**Esfuerzo de implementacion:** MEDIO
**Impacto metodologico:** MEDIO

---

## 5. Especificidades del Caso Argentino

### 5.1 El Error de las Encuestadoras Argentinas: Patron Historico

**PASO 2023:**
- Error promedio en LLA: **subestimacion de ~8-13pp** (ninguna encuesta previo el 30%)
- Zuban Cordoba la mas cercana con 24.5% (vs 30.3% real): error de 5.8pp
- Causa principal: voto oculto + no-respuesta diferencial + muestras inadecuadas

**General octubre 2023:**
- Error promedio en LLA: ~4-5pp (mejoro significativamente vs PASO)
- DC Consultores la mas precisa: LLA 41.2% vs 40.84% real (error 0.36pp)
- La mayoria subestimo la brecha LLA-PJ

**Ballotage noviembre 2023:**
- Las encuestas promediaron un resultado mas cercano al real
- La competencia binaria (Milei vs Massa) simplifico la medicion

**Legislativas 2025:**
- Error significativamente menor (~2pp promedio)
- Milei ya era "voto conocido", no oculto

**Implicacion para el Votometro:** El sigma=6.5 calibrado a PASO 2023 ya puede ser excesivo para 2027. Un sigma decreciente en el tiempo (que refleje la "normalizacion" de LLA como opcion electoral) seria mas preciso.

### 5.2 El "Efecto PASO" en Argentina

Las PASO (Primarias Abiertas Simultaneas y Obligatorias) son unicas en el mundo:
- Funcionan como una "encuesta real" obligatoria
- Historicamente, el resultado de las PASO predice bien la general (pero no siempre: 2019 fue la excepcion, con Macri recuperando terreno post-PASO)
- Para el Votometro 2027: cuando se celebren las PASO (agosto 2027), deberian funcionar como un "superdata point" que recalibra todo el modelo

### 5.3 No Existe un Agregador Formal para Argentina

La investigacion confirma que:
- **No hay FiveThirtyEight argentino.** Las compilaciones de Clarin y otros medios son listas de encuestas, no agregaciones ponderadas.
- **CELAG (Centro Estrategico Latinoamericano de Geopolitica)** hace encuestas propias en Argentina pero no agrega.
- **AtlasIntel** (Brasil) incluye Argentina en su Latam Pulse pero como encuestadora, no agregador.
- **AS-COA** tiene poll trackers para Peru, Colombia, Brasil y Costa Rica pero no para Argentina.

**Esto posiciona al Votometro como unico en su tipo para la eleccion argentina 2027.**

---

## 6. Conclusion: Los 3 Cambios de Mayor Impacto

Basado en el analisis comparativo de todos los agregadores mundiales y las especificidades del contexto argentino, los tres cambios que mas mejorarian la calidad del Votometro son:

### 1. Implementar Trend Line + Bandas de Incertidumbre (Mejoras 1 + 3)

**Por que es el cambio #1:**
- Todos los agregadores serios del mundo (538, Silver, Economist) muestran tendencias, no promedios estaticos.
- Las bandas de incertidumbre son lo que distingue un modelo probabilistico de una tabla de numeros.
- La combinacion EWMA + regresion local es la mas probada y no requiere infraestructura Bayesiana compleja.
- Visualmente, es lo que mas impacto genera: pasar de "LLA: 41%" a "LLA: 41% (rango 36-46%)" comunica honestidad epistemica.

**Esfuerzo total:** MEDIO | **Impacto total:** MUY ALTO

### 2. Correccion Formal de House Effects (Mejora 2)

**Por que es el cambio #2:**
- Actualmente, el Votometro pondera menos a consultoras sesgadas pero NO corrige el sesgo. Esto es como bajar el volumen de un parlante desafinado en lugar de afinarlo.
- Con solo ~10-15 consultoras activas en Argentina, los house effects pueden distorsionar significativamente el promedio.
- La implementacion es simple (tabla de correcciones aditivas) y los datos historicos de 2023-2025 ya existen para calibrar.
- FiveThirtyEight y Silver coinciden: la correccion de house effects es lo que mas mejora la precision de un promedio de encuestas.

**Esfuerzo total:** BAJO | **Impacto total:** ALTO

### 3. Prior de Fundamentals (Mejora 4)

**Por que es el cambio #3:**
- A >500 dias de la eleccion, las encuestas electorales son indicativas pero volatiles. Un ancla de fundamentals (aprobacion + economia + incumbencia) estabiliza el modelo.
- The Economist demostro que la combinacion polls + fundamentals supera a cualquiera de los dos por separado.
- Para Argentina especificamente: la aprobacion presidencial y la percepcion economica son datos que se publican mensualmente y tienen alta correlacion con resultados electorales (especialmente para incumbentes que buscan reeleccion).
- La implementacion no requiere un modelo Bayesiano completo: un blend simple con pesos que varian segun la distancia a la eleccion es suficiente para una primera version.

**Esfuerzo total:** MEDIO | **Impacto total:** ALTO

---

## Apendice: Fuentes Principales

### Documentacion Metodologica
- FiveThirtyEight, "How Our Polling Averages Work" (2023): fivethirtyeight.com/methodology/how-our-polling-averages-work/
- FiveThirtyEight, "How Our Pollster Ratings Work": fivethirtyeight.com/methodology/how-our-pollster-ratings-work/
- Silver Bulletin, "How Silver Bulletin calculates our polling averages": natesilver.net/p/silver-bulletin-polling-average-methodology
- Silver Bulletin, "2024 presidential election model methodology update": natesilver.net/p/model-methodology-2024
- Heidemanns, Gelman & Morris, "An Updated Dynamic Bayesian Forecasting Model for the US Presidential Election", Harvard Data Science Review (2020): hdsr.mitpress.mit.edu/pub/nw1dzd02
- Gelman et al., "Grappling With Uncertainty in Forecasting the 2024 U.S. Presidential Election", HDSR (2024): hdsr.mitpress.mit.edu/pub/yoa73r1m

### Codigo Fuente
- The Economist Germany 2021: github.com/TheEconomist/2021-germany-election-model-PUBLIC
- The Economist France 2022: github.com/TheEconomist/2022-france-election-model
- Silver Bulletin 2024 Data: eli-mckown-dawson.github.io/sbreadme24/readme.html

### Analisis de Error Argentino
- Perfil, "Por cuanto erraron las principales encuestadoras" (2023)
- Chequeado, "Ninguna encuesta pronostico que Milei obtendria el 30%" (2023)
- Clarin, "Las 10 encuestas electorales que adelantan la pelea 2027" (2026)
- AAPOR Task Force on 2024 Pre-Election Polling (2025)

### Papers Academicos
- Shirani-Mehr et al., "Disentangling Bias and Variance in Election Polls" (Columbia/Stanford)
- Bon, Ballard & Baffour, "Polling bias and undecided voter allocations" (Duke)
- Bayesian Forecasting of Electoral Outcomes with New Parties (Barcelona School of Economics)
- Montgomery et al., "Polls, Context, and Time: A Dynamic Hierarchical Bayesian Forecasting Model for US Senate Elections", Political Analysis (2022)

### Agregadores Latinoamericanos
- AS-COA Poll Trackers (Peru, Colombia, Brasil, Costa Rica): as-coa.org/content/guide-2026-latin-american-elections
- AtlasIntel Latam Pulse: atlasintel.org/polls/latam-pulse
- SoMEN framework para prediccion electoral en LATAM: sciencedirect.com/science/article/abs/pii/S0740624X22001186
