# Ficha técnica: Debilidades del Votómetro por código

> Complemento técnico del Q&A crítico. Para usar con el equipo de desarrollo.
> **Actualizado:** sesión mar-2026

---

## Inventario de hardcoding con números de línea

| Elemento hardcodeado | Ubicación (aprox.) | Riesgo | Estado |
|---|---|---|---|
| `ballM = 49 + randn() * 4` | Líneas 1309-1312 | **CRÍTICO** — valor arbitrario para ballotage | ❌ Sin cambios |
| `ballK = 35 + randn() * 4` | Líneas 1331-1332 | **CRÍTICO** — idem Kicillof | ❌ Sin cambios |
| `FECHA_REF = "01-03-2026"` | Header | Alto — requiere actualización manual | ❌ Sin cambios |
| 96 registros de encuestas | JSON inline | Alto — sin pipeline de actualización | ❌ Sin cambios |
| 12 líderes con imágenes | Inline | Medio | ❌ Sin cambios |
| 24 datos distritales | Inline | Medio | ❌ Sin cambios |
| 28 puntos serie ICG | Inline | Medio | ❌ Sin cambios |
| `SIGMA = 0.03` | Línea ~1526 | ~~Alto — subestimaba error histórico x3-4~~ | ✅ Resuelto: ahora `SIGMA = 6.5` |
| Variables Monte Carlo independientes | Loop MC | ~~Alto — escenarios imposibles LLA+PJ>100%~~ | ✅ Resuelto: `RHO = -0.7` implementado |
| Seed aleatoria ausente | Loop MC | ~~Alto — resultados no reproducibles~~ | ✅ Resuelto: PRNG `mulberry32` seedeado con `FECHA_REF` |
| Texto footer | Inline | Bajo | ❌ Sin cambios |

---

## Parámetros del Monte Carlo — estado actual vs anterior

```javascript
// ANTERIOR (sesión inicial — problemático)
const SIGMA = 0.03;  // sigma=3% — subestimaba el error histórico argentino x3-4
// Sin correlación entre LLA y PJ — escenarios imposibles
// Sin seed fija — resultados distintos en cada carga

// ACTUAL (tras sesión mar-2026)
const SIGMA = 6.5;          // sigma=6.5% — promedio entre 5% (The Economist) y 8% (error PASO 2023)
const RHO = -0.7;           // correlación negativa LLA-PJ implementada via Cholesky
// PRNG mulberry32 seedeado con FECHA_REF — resultados reproducibles por fecha
// Loop MC: z1*SIGMA para LLA; (RHO*z1 + sqrt(1-RHO²)*z2)*SIGMA para PJ
```

---

## Resueltos en sesión mar-2026

### SIGMA calibrado históricamente (Q4)

- **Antes:** `SIGMA = 0.03` — justificado como "error del agregador menor que el de una consultora individual", pero sin respaldo empírico
- **Ahora:** `SIGMA = 6.5` en línea ~1526 de `web/votometro.html`
- **Base:** promedio entre σ=5% (referencia The Economist para EE.UU.) y σ=8% (límite inferior del error en LLA durante PASO 2023)
- **Efecto:** los intervalos de confianza son ahora ~2x más amplios; las probabilidades de primera vuelta se reducen, pero son más honestas

### Correlación RHO=-0.7 entre LLA y PJ (Q5)

- **Antes:** LLA y PJ simulados con shocks independientes — podían sumar >95% del voto antes de agregar terceros espacios
- **Ahora:** `RHO = -0.7` implementado mediante descomposición de Cholesky en el loop del Monte Carlo
- **Efecto:** elimina los escenarios físicamente imposibles; la suma LLA+PJ tiene distribución más razonable (media ~72-75%)
- **Nota:** RHO=-0.7 es conservador; los datos de 2023 sugieren correlación de ~-0.85. Ajustar con backtest cuando esté disponible

### Semilla determinista mulberry32 (Q6)

- **Antes:** `Math.random()` sin seed — probabilidades de primera vuelta variaban ±10pp entre cargas de página
- **Ahora:** PRNG `mulberry32` inicializado con `FECHA_REF` — dos cargas con la misma fecha producen resultados idénticos
- **Efecto:** reproducibilidad para periodistas, auditores y presentaciones; el número "congela" por fecha de referencia

### Prior de Fundamentals (nuevo — Q14)

- **Capacidad nueva sin equivalente previo**
- `calcularPriorFundamentals()` combina: aprobación presidencial (39%), ICC Di Tella (44.4 pts), EMAE +3.5% ia, baseline legislativas 2025 (40.84%)
- El peso del prior decrece linealmente de 50% (a 1000 días de la elección) a 0% el día del voto
- Visible en la UI: barra de inputs de fundamentals + histograma con líneas prior/encuestas superpuestas
- Es el único agregador en Argentina con este mecanismo explícito

### Ajuste espacio/candidato — CAND_ADJ (Q2, parcial)

- `CAND_ADJ_LLA = 4pp` y `CAND_ADJ_PJ = 2pp` aplicados a encuestas que preguntan por candidato
- Normaliza al marco de espacio antes de la agregación
- Sigue siendo un escalar fijo, no una distribución — pendiente calibración dinámica

### Cap 20% por consultora (Q3, parcial)

- Ninguna consultora puede superar el 20% del peso total del agregado, independientemente del volumen de encuestas
- Limita la sobrerepresentación cuantitativa de Giacobbe
- No corrige el sesgo cualitativo (house effect direccional) — eso requiere modelo bayesiano jerárquico

---

## Función de ponderación: análisis del rango

Los pesos totales (sin decaimiento) van de **0.460** a **1.265** — diferencia de 2.7x entre consultoras.

Esto es razonable como rango, pero el mecanismo de asignación de pesos es opaco. FiveThirtyEight publica su metodología de ratings públicamente. CIGOB debería documentar los criterios.

---

## La circular del ICG

El modelo calcula R² entre ICG (imagen presidencial) e intención de voto. Pero:
1. 55% de los datos de intención son **imputados desde el ICG** con un modelo lineal
2. Luego ese R² se usa para **validar** la correlación ICG→intención

Esto es circularidad lógica. La R² del gráfico de correlación está inflada porque los datos de validación son, en parte, los mismos datos de entrenamiento.

**Diagnóstico:** Solo los 43 registros de fuente primaria (calidad A+B) deberían usarse para calcular la R² del ICG.

**Estado (mar 2026): SIN CAMBIOS — pendiente.**

---

## Hallazgos técnicos nuevos de la sesión

- `getPixelForIndex` no existe en Chart.js v3/v4 — la referencia correcta es `meta.data[idx].x`
- El proyecto tiene git activo y GitHub Pages con deploy automático desde rama main, carpeta `web/` como root (esto contradice lo que decía CLAUDE.md)
- El panel de Villarruel fue eliminado del HTML como decisión de UX — no hay escenario de fractura de LLA actualmente

---

## Pendientes críticos (sin cambios)

| Elemento | Por qué es urgente |
|---|---|
| Ballotage hardcodeado (49+randn()*4, 35+randn()*4) | El más vulnerable si alguien ve el código |
| Sin backtest formal | No hay validación del modelo |
| Pipeline de actualización | Sin proceso, el instrumento envejece |
| Escenarios alternativos de segunda vuelta | Modelo subestima complejidad de 2027 |
| House effects bayesianos | Sesgo Giacobbe sin corregir en dirección |
