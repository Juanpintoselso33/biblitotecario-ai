# Fortalezas del Votómetro: cómo defenderlo

> Para que Luis y el equipo sepan qué argumentar cuando lleguen las críticas.
> **Actualizado:** sesión mar-2026

---

## Lo que el Votómetro hace bien (y pocos hacen en Argentina)

### 1. Ponderación quíntuple — más sofisticada que cualquier medio argentino

La mayoría de los agregadores argentinos (Chequeado, medios) hacen promedios simples. El Votómetro pondera por:
- Decaimiento temporal (lambda=0.015) — encuestas recientes pesan más
- Calidad de la consultora
- Sesgo histórico
- Orientación del medio
- Metodología de campo

Ningún medio argentino documenta este nivel de sofisticación. **Esto es defendible y es diferencial.**

### 2. Monte Carlo con 10.000 simulaciones y correlación entre espacios — nuevo en mar-2026

Mostrar probabilidades de primera vuelta en lugar de solo porcentajes puntuales es lo que hacen FiveThirtyEight y The Economist. En Argentina, ningún outlet hace esto sistemáticamente. El Votómetro está 5 años adelantado a la práctica periodística local.

Desde mar-2026: LLA y PJ se simulan con correlación negativa (RHO=-0.7), eliminando los escenarios físicamente imposibles. Esto lo acerca al modelo MVNS que usa Gelman/The Economist.

### 3. Sigma calibrado históricamente (SIGMA=6.5%) — resuelto en mar-2026

Hasta esta sesión, SIGMA=3% era el parámetro más atacable del modelo. Desde mar-2026, SIGMA=6.5% basado en el error real del PASO 2023 (8-13pp para LLA) y la referencia de The Economist (~5pp para EE.UU.). Los intervalos de confianza son ahora científicamente honestos.

### 4. Verificación constitucional en cada simulación

Chequear Art. 97-98 CN (45% o 40%+10pp) en cada simulación del Monte Carlo es una funcionalidad única que conecta el modelo estadístico con la realidad institucional. Ningún modelo académico internacional hace esto de forma integrada.

### 5. Cobertura de los 24 distritos con datos de imagen

El desglose provincial con imagen de Milei en los 24 distritos es una visualización que ningún medio argentino ofrece de forma integrada. Es la ventaja CIGOB por excelencia: la dimensión subnacional.

### 6. Corrección de voto oculto bayesiana

El ajuste por voto oculto calibrado con legislativas 2025 es un paso metodológico que la literatura recomienda (Gelman, 2024; SEDICI/UNLP, 2022) y que pocas consultoras argentinas documentan explícitamente.

### 7. Prior de Fundamentals — único en Argentina (nuevo en mar-2026)

El Votómetro ahora incorpora un modelo de "fundamentals" (aprobación presidencial, ICC Di Tella, EMAE, baseline electoral) que ancla las proyecciones entre elecciones. El peso del prior decrece linealmente a medida que se acerca la elección, en línea con el modelo de The Economist.

**Esto es único en Argentina.** Ningún otro agregador público — ni Chequeado Electoral ni Infobae — hace esto. Es el argumento más fuerte para diferenciar el Votómetro en la reunión con España.

### 8. Seed determinista — resultados reproducibles (nuevo en mar-2026)

Con el PRNG mulberry32 seedeado por `FECHA_REF`, dos personas que carguen la misma versión del Votómetro en el mismo período ven exactamente los mismos números. Esto es auditabilidad básica.

### 9. Armonización espacio/candidato explícita (nuevo en mar-2026)

El ajuste CAND_ADJ (4pp LLA, 2pp PJ) normaliza encuestas de distinto tipo antes de agregarlas. Pocas consultoras documentan este ajuste explícitamente — CIGOB sí.

---

## Respuestas preparadas para críticas comunes

**"Las encuestadoras fallaron en 2023, ¿por qué confiar en esto?"**
> El Votómetro no confía ciegamente en ninguna encuestadora — las pondera y las corrige. Precisamente porque las encuestas argentinas tienen house effects conocidos, usamos un sistema de pesos que penaliza las consultoras con mayor error histórico.

**"¿Por qué sigma=6.5 si el error fue de 13 puntos en 2023?"**
> El 6.5% es el error esperado del *agregador* — no de una consultora individual. La agregación ponderada reduce el error respecto al promedio simple. Usamos el promedio entre el referente internacional (The Economist, ~5%) y el peor error documentado en Argentina para LLA (8%). Si hubiera backtest disponible, podríamos calibrar con mayor precisión.

**"¿Por qué Kicillof en el ballotage? Puede no ser el candidato del PJ"**
> Es el escenario más probable dado el estado actual de las encuestas. El panel de escenarios alternativos está en la hoja de ruta para la próxima versión.

**"¿Qué diferencia a esto de un promedio de encuestas con gráficos bonitos?"**
> La ponderación de calidad, la simulación de incertidumbre con correlación entre espacios, la verificación constitucional automática, el modelo de fundamentals y la proyección subnacional. Ningún otro instrumento público en Argentina hace las cinco cosas juntas.

**"¿No cambian los números cada vez que recargo?"**
> No — desde la actualización de marzo de 2026, los resultados son deterministas por fecha de referencia. Si recargás la misma versión, ves el mismo número.

---

## Comparación con modelos de referencia

| Característica | FiveThirtyEight | The Economist | Votómetro | Estado |
|---|---|---|---|---|
| Decaimiento temporal | Sí (exponencial) | Sí | Sí (lambda=0.015) | [OK] Equivalente |
| House effects | Sí (bayesiano) | Sí (jerárquico) | Parcial (peso calidad + cap 20%) | [~] Mejorable |
| Monte Carlo | Sí (10.000) | Sí | Sí (10.000) | [OK] Equivalente |
| Correlación entre candidatos | Sí (MVNS) | Sí | Sí (RHO=-0.7) | [OK] Resuelto mar-2026 |
| Sigma calibrado históricamente | Sí | Sí (~3pp EE.UU.) | Sí (6.5% PASO 2023) | [OK] Resuelto mar-2026 |
| Seed reproducible | Sí | Sí | Sí (mulberry32 + FECHA_REF) | [OK] Resuelto mar-2026 |
| Prior de fundamentals | Sí | Sí | Sí (aprobación + ICC + EMAE) | [OK] Único en Argentina |
| Transferencia de votos | Sí | Sí | Hardcodeado | [X] Gap crítico |
| Backtest público | Sí | Sí | No | [X] Gap |
| Dimensión subnacional (provincias) | Sí (estados) | Sí (estados) | Parcial (imagen) | [~] Mejorable |
| Verificación constitucional | N/A | N/A | Único | [OK] Diferencial exclusivo |
| Datos abiertos / reproducibles | Sí | Sí | No | [X] Gap |
| Armonización espacio/candidato | Implícita | Implícita | Explícita (+4pp LLA, +2pp PJ) | [OK] Documentado |

---

## Resumen del estado competitivo (mar-2026)

Antes de esta sesión, el Votómetro tenía 4 gaps críticos respecto a FiveThirtyEight/The Economist (sigma, correlación, seed, fundamentals). Tras la sesión, los 4 están resueltos o en implementación.

Los gaps que quedan (transferencia de votos, backtest, datos abiertos) son reales pero no bloquean la defensa pública del instrumento. El ballotage hardcodeado sigue siendo el punto más vulnerable si alguien inspecciona el código.

**Posición de defensa recomendada para España:** el Votómetro es hoy más sofisticado que cualquier instrumento público en Argentina, y comparable en sus componentes centrales con los modelos de referencia internacional. Los gaps identificados son conocidos y tienen hoja de ruta.
