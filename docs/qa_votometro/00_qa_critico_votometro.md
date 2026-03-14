# Q&A Crítico — Votómetro Argentina 2027
**Para llevar a Luis y al equipo de España — semana del 23 de marzo de 2026**
**Generado:** 14 de marzo de 2026 | **Actualizado:** 14 de marzo de 2026 (sesión mar-2026)

---

## Estado rápido por pregunta — marzo 2026

| # | Pregunta | Estado |
|---|----------|--------|
| Q1 | 55% de datos son imputaciones, no encuestas reales | ❌ Pendiente |
| Q2 | Diferencia entre preguntas de espacio vs candidato | ⚠️ Parcial |
| Q3 | Concentración Giacobbe (27% del dataset) | ⚠️ Parcial |
| Q4 | σ=3% vs error histórico de 8-13pp | ✅ Resuelto |
| Q5 | LLA y PJ simulados como variables independientes | ✅ Resuelto |
| Q6 | Probabilidades cambian en cada recarga (sin semilla) | ✅ Resuelto |
| Q7 | Parámetros ballotage hardcodeados (49+randn()*4) | ❌ Pendiente |
| Q8 | Solo escenario Milei vs Kicillof en segunda vuelta | ❌ Pendiente |
| Q9 | Sin backtest formal contra PASO 2023 / legislativas 2025 | ❌ Pendiente |
| Q10 | Pipeline de actualización — datos siguen hardcodeados | ❌ Pendiente |
| Q11 | Propuesta de valor diferencial vs Chequeado / Infobae | ❌ Pendiente |
| Q12 | Propiedad y custodia del dataset (CIGOB vs Redlines) | ❌ Pendiente |
| Q13 | Producto público vs herramienta interna | ❌ Pendiente |
| Q14 | Prior de fundamentals — nueva capacidad | ✅ Nuevo / Resuelto |

---

## Propósito de este documento

Listar las dudas técnicas y metodológicas más incisivas del Votómetro para que la reunión sea productiva. No es una crítica destructiva: es el tipo de escrutinio que un experto o periodista especializado lanzaría. Cada pregunta incluye (a) por qué importa, (b) qué dice la literatura, y (c) la respuesta posible si el modelo está bien diseñado.

---

## BLOQUE I — Arquitectura de datos

### Q1: ¿El 55% de los datos son imputaciones, no encuestas reales?

**Pregunta exacta para la reunión:**
> "De las 96 observaciones en la base, 53 son reconstruidas desde el índice de imagen/ICG — no son encuestas de intención de voto. ¿Cómo validaron ese modelo de imputación? ¿Fue evaluado fuera de muestra contra elecciones reales?"

**Por qué importa:** Si más de la mitad de los datos son derivados de otro indicador mediante supuestos no validados, el modelo está construido sobre arena. El error de imputación se acumula con el error de la encuesta original.

**Literatura relevante:** Gelman et al. (2024) sobre el modelo de The Economist enfatizan que mezclar preguntas de imagen con preguntas de intención de voto requiere corrección explícita como "house effect" en el modelo jerárquico. Sin corrección, la regresión ICG→intención infla artificialmente la R².

**Respuesta esperada del equipo:** Explicitar el modelo de imputación (¿regresión lineal? ¿elasticidad fija?) y mostrar su performance histórica contra PASO 2023 o legislativas 2025.

---

### Q2: ¿Cómo tratan la diferencia entre preguntas de espacio y de candidato?

**Pregunta exacta:**
> "Giacobbe pregunta por 'espacio', CB pregunta por 'candidato', Atlas pregunta a veces por los dos. ¿Las tratan como equivalentes en la agregación? ¿Hay evidencia de cuánto vale esa diferencia en Argentina hoy?"

**Por qué importa:** La literatura argentina (Cambridge LAPS, 2024; Lucardi et al. 2025) documenta que preguntar por "La Libertad Avanza" vs "Javier Milei" produce respuestas sistemáticamente diferentes, especialmente en contextos de alta personalización política. En el ciclo 2023, esa diferencia llegó a 4-6 puntos.

**Literatura relevante:** Microsoft Research / MRP: encuestas no representativas pueden convertirse a estimaciones de candidato mediante modelos de mapeo empírico. FiveThirtyEight lo trata como un "mode effect" en su modelo jerárquico.

**Respuesta esperada:** O se armoniza explícitamente (corrección por tipo de pregunta) o se documenta la incertidumbre adicional que esto agrega.

> **Estado (mar 2026): PARCIALMENTE RESUELTO.** Se implementó un ajuste explícito: `CAND_ADJ_LLA = 4pp` y `CAND_ADJ_PJ = 2pp`. Las encuestas que preguntan por candidato son normalizadas al marco de espacio antes de agregarse. El ajuste es un valor fijo basado en el diferencial documentado de 2023 — no es un modelo dinámico. Queda pendiente validar ese diferencial contra datos de 2025-2026 y convertirlo en una distribución probabilística en lugar de un escalar fijo.

---

### Q3: ¿Por qué Giacobbe tiene 26 de las 96 observaciones (27%)?

**Pregunta exacta:**
> "Giacobbe representa el 27% del dataset. Si esa consultora tiene un sesgo sistemático hacia LLA, ¿cómo aseguran que la media ponderada no está sesgada en la misma dirección?"

**Por qué importa:** La sobrerepresentación de una consultora en un agregador es un riesgo conocido. El rating de FiveThirtyEight penaliza explícitamente la concentración de una sola fuente. En Argentina, el "efecto de casa" (house effect) de Giacobbe vs Poliarquía difiere históricamente en ~4-5 puntos en favor de LLA.

**Respuesta esperada:** El decaimiento temporal (λ=0.015) reduce el peso de encuestas antiguas, pero no corrige el sesgo sistemático de la consultora. La solución correcta es estimar y restar el house effect antes de agregar.

> **Estado (mar 2026): PARCIALMENTE RESUELTO.** Se implementó un cap de 20% de peso total por consultora. Esto limita la influencia máxima de Giacobbe independientemente de la cantidad de encuestas que aporte. El house effect sistemático (sesgo direccional de Giacobbe hacia LLA) sigue sin corregirse — el cap reduce la sobrerepresentación cuantitativa pero no elimina el sesgo cualitativo. La solución completa requiere estimar y restar el house effect en el modelo bayesiano jerárquico.

---

## BLOQUE II — Modelo Monte Carlo y calibración de incertidumbre

### Q4: ¿Por qué σ=3% si el error histórico de las encuestadoras argentinas es 8-13pp?

**Pregunta exacta:**
> "El Votómetro usa sigma=3% en el Monte Carlo, calibrado contra el error histórico argentino. Pero el PASO 2023 tuvo errores de 8-13 puntos para LLA según Infobae y Chequeado. ¿Cómo se justifica ese parámetro?"

**Por qué importa:** Esta es la debilidad más grave para la comunicación pública. Si el intervalo de confianza está subestimado por un factor de 3x, las probabilidades de primera vuelta (actualmente ~20-35%) están sobreestimadas en confianza. Un modelo con σ=3 es matemáticamente más "seguro" como titular, pero científicamente incorrecto.

**Literatura relevante:** Shirani-Mehr, Rothschild, Goel & Gelman (JASA 2018): "nonsampling error is, on average, about as large as sampling error in public polls." El error real en encuestas presidenciales es ~2x el error muestral nominal. Para Argentina, PASO 2023 demostró errores de hasta 13pp en LLA — debería usarse al menos σ=5-7%, posiblemente más.

> **Estado (mar 2026): RESUELTO.** `SIGMA` actualizado a `6.5` (línea ~1526 de `web/votometro.html`). El valor 6.5% es el promedio entre σ=5% (referencia The Economist para EE.UU.) y σ=8% (límite inferior del error PASO 2023 para LLA). La respuesta preparada para esta crítica está ahora sustentada en el valor implementado — ya no es una promesa de mejora futura.

---

### Q5: El modelo Monte Carlo trata LLA y PJ como variables independientes. ¿Es correcto?

**Pregunta exacta:**
> "En las simulaciones, LLA y PJ varían de forma independiente. Pero en datos reales existe una correlación negativa fuerte: cuando LLA sube, PJ baja y viceversa. ¿Modelaron esa covarianza?"

**Por qué importa:** Si LLA y PJ se simulan independientemente, el modelo genera escenarios imposibles (LLA=50%, PJ=40%, total=90%+ antes de sumar otros partidos). Esto infla artificialmente la varianza real del ballotage.

**Literatura relevante:** Gelman (2024) usa una caminata aleatoria multivariada (MVNS) con matriz de covarianza Σ entre estados o, en este caso, entre partidos. El modelo de The Economist usa correlación explícita entre espacios.

> **Estado (mar 2026): RESUELTO.** Se implementó correlación `RHO = -0.7` en el loop del Monte Carlo. El código usa la descomposición de Cholesky para generar shocks correlacionados: `z1 * SIGMA` para LLA y `(RHO * z1 + sqrt(1 - RHO²) * z2) * SIGMA` para PJ. Esto elimina los escenarios físicamente imposibles de suma total >100%. El valor -0.7 es conservador respecto al -0.85 que muestran datos de 2023 — puede refinarse con el backtest.

---

### Q6: Las probabilidades del Monte Carlo cambian en cada recarga de página. ¿Hay semilla fija?

**Pregunta exacta:**
> "¿Por qué los porcentajes de probabilidad de primera vuelta varían entre 20% y 35% en cada carga de página? ¿No debería haber una semilla fija para reproducibilidad?"

**Por qué importa:** Un modelo que da resultados distintos en cada ejecución no es reproducible ni auditable. Un periodista que recargue la página dos veces verá dos números distintos y cuestionará la seriedad del instrumento.

> **Estado (mar 2026): RESUELTO.** Se implementó el PRNG determinista `mulberry32` seedeado con `FECHA_REF`. Los resultados ahora son reproducibles por fecha de referencia: dos cargas con la misma `FECHA_REF` producen exactamente los mismos números. El seed cambia cuando se actualiza la fecha de referencia del modelo, lo que es el comportamiento correcto.

---

## BLOQUE III — Modelo de segunda vuelta (ballotage)

### Q7: Los parámetros del ballotage son arbitrarios. ¿De dónde salen 49% y 35%?

**Pregunta exacta:**
> "En el código, el ballotage está hardcodeado como Milei=49+randn()*4, Kicillof=35+randn()*4. Eso suma 84%. ¿Qué pasa con el 16% restante? ¿Y de dónde vienen esos valores — son encuestas reales o supuestos?"

**Por qué importa:** Este es el punto más vulnerable del modelo. Si se presentara públicamente y alguien encuentra el código, la credibilidad del instrumento colapsa. Los valores de segunda vuelta deben derivarse del modelo de transferencia de votos, no ser parámetros fijos.

**Literatura relevante:** NBER Working Paper 34430 (2025): matrices de transferencia de votos entre rondas electorales con heterogeneidad provincial. Las matrices deben ser distribuciones probabilísticas (Dirichlet), no puntos fijos. El caso de Salta muestra transferencias de hasta 18pp entre primera vuelta y ballotage para un mismo candidato.

**Respuesta esperada:** Construir una matriz de transferencia 4x2 (votos de PRO, FIT, PU y Otros → Milei/Kicillof en segunda vuelta), informada por encuestas post-PASO y datos históricos de 2023.

**Estado (mar 2026): SIN CAMBIOS — sigue hardcodeado.**

---

### Q8: El modelo solo contempla el escenario Milei vs Kicillof. ¿Qué pasa con otros candidatos de segunda vuelta?

**Pregunta exacta:**
> "El Votómetro asume que el ballotage siempre es Milei vs Kicillof. Pero las encuestas muestran a Bullrich, a Villarruel y a espacios de PU potencialmente relevantes. ¿Por qué no hay escenarios alternativos?"

**Por qué importa:** CB Consultora muestra a Villarruel con 5.2% que, en un escenario de fractura de LLA, podría impedir la victoria en primera vuelta de Milei. Sin modelar estos escenarios, el Votómetro sub-informa la complejidad real de 2027.

**Respuesta esperada:** Al menos 3 escenarios de segunda vuelta: (A) Milei vs Kicillof, (B) Milei vs candidato PRO, (C) escenario de fractura LLA con Milei vs Villarruel.

**Estado (mar 2026): SIN CAMBIOS — el panel de Villarruel fue eliminado del HTML por ser mala UX. No hay escenario alternativo de segunda vuelta actualmente. Queda pendiente diseñar una solución de UX que permita escenarios alternativos sin sobrecargar la interfaz.**

---

## BLOQUE IV — Validación y gobernanza del modelo

### Q9: ¿Corrieron un backtest del modelo contra PASO 2023 y legislativas 2025?

**Pregunta exacta:**
> "¿Cuál habría sido la proyección del Votómetro si existiera en agosto de 2023, con los datos disponibles en ese momento? ¿Y en octubre de 2025? ¿Cuánto se habría equivocado?"

**Por qué importa:** Sin backtest, no hay validación. Un modelo sin validación histórica es una opinión gráfica, no un instrumento técnico. El backtest es lo que separa al Votómetro de un análisis periodístico normal.

**Literatura relevante:** forosur.com.ar (2024): "Argentina's first survey of pollsters seeks to answer what went wrong." El paper de SEDICI/UNLP (2022) establece el framework para evaluar errores de encuestadoras argentinas con métricas estandarizadas (RMSE, bias absoluto medio).

**Respuesta esperada:** Mostrar un gráfico de "proyección retroactiva" para PASO 2023 con intervalos de confianza reales, y comparar cuánto del resultado real cae dentro del intervalo.

**Estado (mar 2026): SIN CAMBIOS — no implementado.**

---

### Q10: ¿Qué mecanismo garantiza que los datos se actualicen? ¿Hay SLA?

**Pregunta exacta:**
> "Todo el dataset está hardcodeado en el HTML. ¿Con qué frecuencia se actualiza? ¿Quién lo hace? ¿Hay un proceso definido o depende de disponibilidad personal?"

**Por qué importa:** Un agregador que no se actualiza pierde credibilidad más rápido que uno que no existe. La fecha más reciente en el dataset es 01-mar-2026 (con el dato de 13 días de antigüedad). Sin proceso de actualización, el instrumento muere.

**Propuesta concreta:** Pipeline mínimo viable: CSV en GitHub → cron semanal → deploy automático. Costo estimado: 1 sprint de 2 semanas.

**Estado (mar 2026): SIN CAMBIOS — los datos siguen hardcodeados en el HTML. Nota nueva: el proyecto SÍ tiene git y deploy automático desde GitHub Pages (rama main, carpeta `web/` como root). Esto simplifica el pipeline futuro: solo falta externalizar los datos a un CSV en el repo.**

---

## BLOQUE V — Preguntas estratégicas para Luis

### Q11: ¿Cuál es la propuesta de valor diferencial del Votómetro vs Chequeado Electoral o Infobae Encuestas?

**Pregunta exacta:**
> "Chequeado Electoral ya agrega encuestas, Infobae las publica semanalmente. ¿Qué hace el Votómetro que ellos no hacen? ¿La metodología ponderada es suficiente diferencial, o necesitamos proyección provincial, análisis de segunda vuelta, o la dimensión subnacional de CIGOB?"

**Por qué importa:** Sin propuesta de valor clara, el Votómetro es un tracker más. La ventaja competitiva de CIGOB es la expertise subnacional — ningún otro agregador modela 24 provincias con datos propios.

---

### Q12: ¿Es el Votómetro un producto de CIGOB o de CIGOB+Redlines? ¿Quién controla los datos?

**Pregunta exacta:**
> "El footer dice 'CIGOB + Redlines Estrategia y Comunicación'. ¿Quién es el custodio del dataset? ¿Si mañana Redlines no puede actualizar, puede CIGOB hacerlo de forma autónoma?"

**Por qué importa:** La propiedad intelectual y operativa del instrumento define si CIGOB puede escalarlo, licenciarlo o convertirlo en producto independiente. Si los datos viven en la laptop de alguien de Redlines, el instrumento tiene un punto único de falla.

---

### Q13: ¿El Votómetro es un producto público o una herramienta interna?

**Pregunta exacta:**
> "¿Está pensado para publicación pública, para clientes de CIGOB, o para uso interno en reuniones? La respuesta cambia completamente el nivel de rigor metodológico requerido."

**Por qué importa:** Si es público, necesita documentación metodológica, reproducibilidad y backtest. Si es interno, puede ser más flexible. Actualmente está construido como si fuera interno pero presentado como si fuera público — esa ambigüedad es un riesgo reputacional.

---

## BLOQUE V-b — Nueva capacidad: Prior de Fundamentals

### Q14: ¿Qué es el Prior de Fundamentals y cómo afecta las proyecciones?

**Contexto:**
> El Votómetro ahora incorpora un modelo de "fundamentals" — variables macroeconómicas e institucionales que predicen resultados electorales independientemente de las encuestas.

**Cómo funciona:**
- `calcularPriorFundamentals()` integra: aprobación presidencial (39%), ICC Di Tella (44.4 pts), EMAE +3.5% ia, y baseline de legislativas 2025 (40.84%)
- El peso de los fundamentals decrece linealmente desde 50% (a 1000 días de la elección) hasta 0% el día de la elección
- Visible en la UI como barra de inputs + histograma con líneas prior/encuestas superpuestas

**Por qué importa positivamente:** Este es el único agregador en Argentina que usa un modelo de fundamentals explícito. FiveThirtyEight y The Economist hacen esto — CIGOB ahora está en esa liga. Es el argumento más fuerte para la reunión con España.

**Preguntas pendientes sobre el prior:**
- ¿Qué modelo liga aprobación presidencial + ICC + EMAE a intención de voto? ¿Regresión histórica sobre qué elecciones?
- ¿El baseline de legislativas 2025 (40.84%) es directamente comparable con proyecciones presidenciales?
- ¿Con qué frecuencia se actualizan las variables de fundamentals?

---

## BLOQUE VI — Propuestas de robustecimiento (para el debate con España)

Basadas en la literatura revisada (Gelman 2024, FiveThirtyEight, The Economist, NBER 2025):

| # | Mejora | Impacto | Dificultad | Prioridad | Estado |
|---|--------|---------|------------|-----------|--------|
| 1 | Aumentar σ a 6-8% basado en error histórico argentino | Corrige la subestimación de incertidumbre | Baja | **ALTA** | ✅ RESUELTO (σ=6.5%) |
| 2 | Fijar semilla aleatoria (mulberry32) | Reproducibilidad básica | Muy baja | **ALTA** | ✅ RESUELTO |
| 3 | Correlación LLA-PJ en Monte Carlo (RHO=-0.7) | Elimina escenarios imposibles | Alta | **ALTA** | ✅ RESUELTO |
| 4 | Prior de fundamentals (macro + aprobación) | Ancla el modelo entre elecciones | Alta | **ALTA** | ✅ RESUELTO (nuevo) |
| 5 | Armonización espacio/candidato (+4pp LLA, +2pp PJ) | Reduce sesgo de tipo de pregunta | Media | **MEDIA** | ⚠️ PARCIAL |
| 6 | Cap 20% por consultora | Reduce sobrerepresentación Giacobbe | Baja | **MEDIA** | ⚠️ PARCIAL |
| 7 | Separar imputaciones de encuestas reales en visualización | Transparencia metodológica | Baja | **MEDIA** | ❌ Pendiente |
| 8 | Pipeline de actualización semanal (CSV → GitHub → deploy) | Sostenibilidad operativa | Media | **MEDIA** | ❌ Pendiente |
| 9 | Construir matriz de transferencia para ballotage | Reemplaza valores hardcodeados | Media | **ALTA** | ❌ Pendiente |
| 10 | Agregar escenarios alternativos de segunda vuelta | Completitud analítica | Media | **MEDIA** | ❌ Pendiente |
| 11 | Backtest formal contra PASO 2023 con métricas (RMSE, Brier score) | Validación científica | Alta | **BAJA** | ❌ Pendiente |
| 12 | House effects bayesianos (Giacobbe vs Poliarquía) | Eliminar sesgo de concentración | Alta | **MEDIA** | ❌ Pendiente |

---

## Referencias clave para citar en la reunión

- **Shirani-Mehr et al. (JASA 2018):** error de no-muestreo ≈ error muestral → σ real debe duplicarse
- **Gelman et al. (HDSR 2024):** modelo The Economist — caminata aleatoria multivariada, house effects, correlación entre candidatos
- **FiveThirtyEight Methodology (2024):** decaimiento exponencial, Bayesian combination, pollster ratings
- **NBER WP 34430 (2025):** matrices de transferencia de votos con heterogeneidad provincial en Argentina
- **SEDICI/UNLP (2022):** evaluación sistemática de encuestadoras argentinas — bias absoluto medio por consultora
- **Chequeado (2023):** "ninguna encuesta pronosticó el 30% de Milei" — diagnóstico del fallo de PASO 2023
- **Lucardi, Vallejo & Feierherd (2025):** impacto del margen PASO en turnout y votos de segunda vuelta
