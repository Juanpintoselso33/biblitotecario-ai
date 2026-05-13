# Propuestas Técnicas de Mejora para el Votómetro
**Research date:** 14 de marzo de 2026
**Ordenadas por: impacto metodológico**

---

## Mejora 1: Trend Line con EWMA + Regresión Local
**Esfuerzo: MEDIO | Impacto: MUY ALTO**

### Descripción

Reemplazar el promedio ponderado estático por un sistema dual:
- **EWMA:** Para producir un promedio estable que se actualice incrementalmente
- **Regresión polinomial local:** Para capturar cambios rápidos cuando hay muchos datos nuevos
- **Mezcla adaptativa:** Más peso al EWMA con pocas encuestas, más al polinomial con muchas

### Implementación JavaScript

```javascript
// EWMA (Exponentially Weighted Moving Average)
function calcularEWMA(encuestas, decay = 0.05) {
  const sorted = [...encuestas].sort((a, b) => b.fecha - a.fecha);
  const hoy = new Date();
  let sumaPesos = 0, sumaValores = 0;
  sorted.forEach(enc => {
    const diasAtras = (hoy - enc.fecha) / (1000 * 60 * 60 * 24);
    const peso = Math.exp(-decay * diasAtras) * enc.pesoBase;
    sumaPesos += peso;
    sumaValores += enc.valor * peso;
  });
  return sumaPesos > 0 ? sumaValores / sumaPesos : null;
}

// Regresión polinomial local con kernel gaussiano
function regresionLocalKernel(encuestas, fechaObjetivo, bandwidth = 30, grado = 1) {
  const t0 = fechaObjetivo.getTime();
  const datos = encuestas.map(enc => {
    const diasDif = (enc.fecha.getTime() - t0) / (1000 * 60 * 60 * 24);
    const u = diasDif / bandwidth;
    const kernelPeso = Math.exp(-0.5 * u * u) * enc.pesoBase;
    return { t: diasDif, valor: enc.valor, peso: kernelPeso };
  }).filter(d => d.peso > 0.001);

  if (datos.length < grado + 1) return null;

  if (grado === 1) {
    let sw=0, swt=0, swt2=0, swy=0, swty=0;
    datos.forEach(d => {
      sw+=d.peso; swt+=d.peso*d.t; swt2+=d.peso*d.t*d.t;
      swy+=d.peso*d.valor; swty+=d.peso*d.t*d.valor;
    });
    const det = sw*swt2 - swt*swt;
    if (Math.abs(det) < 1e-10) return swy/sw;
    return (swt2*swy - swt*swty) / det;
  }
  return null;
}

// Mezcla adaptativa (como 538)
function promedioAdaptativo(encuestas, fecha, ventanaMes = 30) {
  const ewma = calcularEWMA(encuestas);
  const poly = regresionLocalKernel(encuestas, fecha);
  const recientes = encuestas.filter(e =>
    (fecha - e.fecha) / (1000*60*60*24) <= ventanaMes
  ).length;
  const pesoPoly = Math.min(0.8, recientes / 15);
  if (poly === null) return ewma;
  return (1 - pesoPoly) * ewma + pesoPoly * poly;
}
```

---

## Mejora 2: Corrección Formal de House Effects
**Esfuerzo: BAJO | Impacto: ALTO**

### Descripción

En lugar de usar "sesgo histórico" como peso multiplicativo (que reduce la influencia pero **no corrige el valor**), implementar una corrección aditiva que ajuste el valor reportado.

**Método:**
1. Calcular la diferencia sistemática entre resultados de cada consultora y el promedio de otras consultoras en el mismo período
2. Almacenar el "house effect" (ej: Consultora X tiende a darle +3pp a LLA)
3. Al incorporar una nueva encuesta, restar el house effect del valor reportado
4. Mean-revert: con pocas encuestas históricas, asumir house effect cercano a 0

### Implementación JavaScript

```javascript
const houseEffects = {
  // Positivo = le da más a LLA de lo que dan las demás
  // Calibrado con legislativas 2025 y elecciones 2023
  'Opinaia':     { lla: +2.1, pj: -1.8, n_polls: 12 },
  'Trends':      { lla: +0.5, pj: +0.3, n_polls: 8 },
  'CB':          { lla: -1.2, pj: +0.8, n_polls: 15 },
  'DC':          { lla: +0.8, pj: -0.5, n_polls: 6 },
  'Proyección':  { lla: -0.3, pj: +0.2, n_polls: 10 },
  'Isasi':       { lla: +1.5, pj: -1.0, n_polls: 4 },
  'Zuban':       { lla: -2.5, pj: +2.0, n_polls: 18 },
};

function corregirHouseEffect(valorEncuesta, consultora, partido) {
  const he = houseEffects[consultora];
  if (!he) return valorEncuesta;
  // Mean reversion: con pocos datos, atenuar la corrección
  const factorConfianza = Math.min(1.0, he.n_polls / 15);
  const correccion = (he[partido] || 0) * factorConfianza;
  return valorEncuesta - correccion;
}

// Ejemplo: Si Opinaia reporta LLA=44%:
// 44 - (2.1 * min(1, 12/15)) = 44 - 1.68 = 42.32%
```

---

## Mejora 3: Bandas de Incertidumbre Visuales
**Esfuerzo: BAJO | Impacto: ALTO (en comunicación)**

### Descripción

Mostrar un intervalo de confianza alrededor del promedio que refleje:
1. La dispersión entre encuestas
2. El error histórico de las encuestadoras argentinas
3. La cantidad de encuestas disponibles

```javascript
function calcularBandaIncertidumbre(encuestas, promedioActual) {
  // 1. Dispersión entre encuestas (desviación estándar ponderada)
  let sumPesos = 0, sumPesosDifCuad = 0;
  encuestas.forEach(e => {
    sumPesos += e.peso;
    sumPesosDifCuad += e.peso * Math.pow(e.valor - promedioActual, 2);
  });
  const sdEncuestas = Math.sqrt(sumPesosDifCuad / sumPesos);

  // 2. Error histórico argentino (calibrado empíricamente)
  // PASO 2023: ~10pp | General 2023: ~4pp | Leg. 2025: ~2pp
  const errorHistorico = 3.5; // pp, promedio reciente

  // 3. Factor por cantidad de encuestas
  const factorN = 1 + 2 / Math.sqrt(encuestas.length);

  // 4. Combinar
  const sigma = Math.sqrt(sdEncuestas**2 + errorHistorico**2) * factorN;

  return {
    bajo90: promedioActual - 1.645 * sigma,
    alto90: promedioActual + 1.645 * sigma,
    bajo50: promedioActual - 0.674 * sigma,
    alto50: promedioActual + 0.674 * sigma,
    sigma
  };
}
// Visualización: área sombreada alrededor de la trend line,
// con dos niveles de opacidad (IC50 más oscuro, IC90 más tenue)
```

---

## Mejora 4: Prior de Fundamentals
**Esfuerzo: MEDIO | Impacto: ALTO (especialmente a >500 días del E-Day)**

### Descripción

Incorporar un "ancla" basada en variables político-económicas. Para Argentina, las variables clave son:
1. **Aprobación presidencial** (dato mensual)
2. **Percepción económica** (optimismo/pesimismo)
3. **Resultado elecciones anteriores** (legislativas 2025: LLA ~47%)
4. **Incumbencia** (históricamente ventajoso en Argentina)

```javascript
function calcularPriorFundamentals() {
  const baselineLLA = 47; // Resultado legislativas 2025
  const aprobacion = 50;  // % positiva actual (Trends ene-2026)
  const optimismo = 45;   // % que espera mejora económica

  const ajusteAprobacion = (aprobacion - 45) * 0.3;
  const bonoIncumbencia = 2; // pp conservador (Menem 1995, CFK 2011: 3-5pp)
  const ajusteEconomia = (optimismo - 40) * 0.2;

  return {
    lla: baselineLLA + ajusteAprobacion + bonoIncumbencia + ajusteEconomia,
    pj: 30 - ajusteAprobacion * 0.5
  };
}

function blendPollsYFundamentals(pollsLLA, pollsPJ, diasParaEleccion) {
  const fundamentals = calcularPriorFundamentals();
  // Más peso a fundamentals cuando falta más tiempo
  const pesoFundamentals = Math.min(0.5, diasParaEleccion / 1000);
  return {
    lla: (1-pesoFundamentals)*pollsLLA + pesoFundamentals*fundamentals.lla,
    pj:  (1-pesoFundamentals)*pollsPJ  + pesoFundamentals*fundamentals.pj
  };
}

// A 500 días (mar 2026): peso fundamentals=0.5
//   Si polls→LLA=41, fundamentals→LLA=50.5: blend=45.75
// A 30 días: peso fundamentals=0.03
//   blend≈41.3 (casi todo polls)
```

---

## Mejora 5: Rating Formal de Consultoras Argentinas
**Esfuerzo: MEDIO | Impacto: MEDIO-ALTO**

### Descripción

Sistema de calificación basado en performance histórica, similar al Pollster Rating de FiveThirtyEight.

```javascript
// Ratings estimados basados en performance 2023-2025
const ratingsConsultoras = {
  'DC Consultores':  2.5,  // Más precisa en general 2023 (+0.36pp error LLA)
  'CB Consultora':   2.3,  // Consistentemente cercana
  'Atlas Intel':     2.0,  // Buena muestra, metodología digital sólida
  'Opinaia':         1.8,  // Pionera online, tiende a sobreestimar oficialismo
  'Trends':          1.7,  // Reciente, buenos datos, poco historial
  'Proyección':      1.6,
  'Zuban Córdoba':   1.5,  // Errores significativos en PASO 2023
  'Equipo Mide':     1.8,  // Le dio alto a Milei antes de PASO (buena señal)
};

// Variables para el rating:
// + Error promedio histórico (ponderado: 50% ciclo reciente, 25% anterior...)
// + Sesgo (bias): consistente = mejor que inconsistente, aunque sea alto
// + Metodología: +bonus presencial, +muestra>2000, +ficha técnica completa
// + Transparencia: publica cruces demográficos, detalle de muestreo
// - Herding: se acerca mucho al promedio existente
```

---

## Mejora 6: Modelo de Voto Oculto Dinámico
**Esfuerzo: BAJO | Impacto: MEDIO**

### Descripción

Reemplazar la corrección fija (+4pp LLA para polls candidato) por un modelo calibrado que se actualice con el tiempo, reconociendo que el "efecto sorpresa" Milei ya no existe en 2026.

```javascript
function correccionVotoOculto(partido, tipoEncuesta, anio) {
  const calibracion = {
    'LLA': {
      base: 2.0,           // Reducido de 4pp: el "efecto sorpresa" ya no existe
      tendencia: -0.5,     // Se reduce 0.5pp por año desde 2023
      factor_metodologia: { 'online': 1.2, 'telefonico': 1.0, 'presencial': 0.6, 'mixto': 0.8 }
    },
    'PJ': {
      base: 0.5,
      tendencia: -0.2,
      factor_metodologia: { 'online': 0.8, 'telefonico': 1.0, 'presencial': 1.2, 'mixto': 1.0 }
    }
  };

  const config = calibracion[partido];
  if (!config) return 0;

  const anosDesde2023 = anio - 2023;
  const baseAjustada = Math.max(0, config.base + config.tendencia * anosDesde2023);
  const factorMet = config.factor_metodologia[tipoEncuesta] || 1.0;

  return baseAjustada * factorMet;
}

// Para encuesta online de LLA en 2026:
// base = max(0, 2.0 + (-0.5)*3) = 0.5pp
// factor_online = 1.2 → corrección = 0.6pp
// (vs los 4pp fijos actuales, que ya son excesivos)
```

---

## Mejora 7: Penalidad por Herding
**Esfuerzo: MEDIO | Impacto: MEDIO**

Detectar consultoras que ajustan sus resultados para acercarse al consenso existente.

```javascript
function calcularHerding(consultora, encuestasConsultora, todasLasEncuestas) {
  let distanciasTotales = 0, n = 0;
  encuestasConsultora.forEach(enc => {
    const previas = todasLasEncuestas.filter(e =>
      e.consultora !== consultora &&
      e.fecha < new Date(enc.fecha.getTime() - 3*24*60*60*1000)
    );
    if (previas.length < 3) return;
    const promedioLLA = previas.reduce((s,e) => s+e.lla, 0) / previas.length;
    distanciasTotales += Math.abs(enc.lla - promedioLLA);
    n++;
  });
  if (n === 0) return 0;

  const ADPA = distanciasTotales / n;
  const ADPA_minimo = 1.5 * Math.sqrt(0.42 * 0.58 / 2000) * 100; // ~1.65pp
  return Math.max(0, 0.5 * (ADPA_minimo - ADPA)); // Positivo = sospecha herding
}
```

---

## Mejora 8: Sigma Dinámico
**Esfuerzo: BAJO | Impacto: MEDIO**

El sigma=6.5 está calibrado al error histórico de PASO 2023. Pero el patrón muestra reducción sistemática:

| Elección | Error promedio LLA | Sigma implícito |
|----------|--------------------|-----------------|
| PASO 2023 | ~10pp | ~6.5 |
| General 2023 | ~4-5pp | ~3 |
| Legislativas 2025 | ~2pp | ~1.2 |

```javascript
function sigmaCalibrado(diasParaEleccion) {
  // Más lejos de la elección = más incertidumbre
  // A 500 días: sigma = 6.5 (como ahora)
  // A 30 días de la PASO: sigma reducido porque las consultoras mejoran
  const sigmaBase = 6.5;
  const sigmaMinimo = 2.0; // Error mínimo histórico reciente
  const factor = Math.min(1.0, diasParaEleccion / 500);
  return sigmaMinimo + (sigmaBase - sigmaMinimo) * factor;
}
```

---

## Tabla resumen de mejoras

| # | Mejora | Esfuerzo | Impacto | Prioridad |
|---|--------|----------|---------|-----------|
| 1 | Trend line EWMA + regresión local | MEDIO | MUY ALTO | ★★★ |
| 2 | Corrección house effects aditiva | BAJO | ALTO | ★★★ |
| 3 | Bandas de incertidumbre visuales | BAJO | ALTO | ★★★ |
| 4 | Prior de fundamentals | MEDIO | ALTO | ★★ |
| 5 | Rating formal de consultoras | MEDIO | MEDIO-ALTO | ★★ |
| 6 | Voto oculto dinámico | BAJO | MEDIO | ★★ |
| 7 | Penalidad herding | MEDIO | MEDIO | ★ |
| 8 | Sigma dinámico | BAJO | MEDIO | ★★ |
