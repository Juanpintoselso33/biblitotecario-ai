# Ficha técnica: Debilidades del Votómetro por código

> Complemento técnico del Q&A crítico. Para usar con el equipo de desarrollo.

## Inventario de hardcoding con números de línea

| Elemento hardcodeado | Ubicación (aprox.) | Riesgo |
|---|---|---|
| `ballM = 49 + randn() * 4` | Líneas 1309-1312 | **CRÍTICO** — valor arbitrario para ballotage |
| `ballK = 35 + randn() * 4` | Líneas 1331-1332 | **CRÍTICO** — idem Kicillof |
| `FECHA_REF = "01-03-2026"` | Header | Alto — requiere actualización manual |
| 96 registros de encuestas | JSON inline | Alto — sin pipeline de actualización |
| 12 líderes con imágenes | Inline | Medio |
| 24 datos distritales | Inline | Medio |
| 28 puntos serie ICG | Inline | Medio |
| Texto footer | Inline | Bajo |

## Parámetros del Monte Carlo que necesitan revisión

```javascript
// ACTUAL (problemático)
const SIGMA = 0.03;  // sigma=3% — subestima el error histórico argentino x3-4

// RECOMENDADO basado en literatura
const SIGMA = 0.065; // sigma=6.5% — promedio entre sigma=5% (The Economist) y sigma=8% (error PASO 2023)
```

## Función de ponderación: análisis del rango

Los pesos totales (sin decaimiento) van de **0.460** a **1.265** — diferencia de 2.7x entre consultoras.

Esto es razonable como rango, pero el mecanismo de asignación de pesos es opaco. FiveThirtyEight publica su metodología de ratings públicamente. CIGOB debería documentar los criterios.

## La circular del ICG

El modelo calcula R² entre ICG (imagen presidencial) e intención de voto. Pero:
1. 55% de los datos de intención son **imputados desde el ICG** con un modelo lineal
2. Luego ese R² se usa para **validar** la correlación ICG→intención

Esto es circularidad lógica. La R² del gráfico de correlación está inflada porque los datos de validación son, en parte, los mismos datos de entrenamiento.

**Diagnóstico:** Solo los 43 registros de fuente primaria (calidad A+B) deberían usarse para calcular la R² del ICG.
