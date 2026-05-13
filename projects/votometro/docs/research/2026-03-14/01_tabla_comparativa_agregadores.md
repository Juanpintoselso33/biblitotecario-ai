# Tabla Comparativa de Agregadores Electorales Mundiales
**Research date:** 14 de marzo de 2026

---

| Agregador | País | Ponderación | Modelo de incertidumbre | House effects | Fundamentals | Código público |
|-----------|------|------------|------------------------|--------------|-------------|----------------|
| **FiveThirtyEight (ABC News)** | EE.UU. | Multiplicativa: (n/600)^0.5 × rating × recencia. Cap n=1500. EWMA + regresión polinomial local con kernel | MCMC, decenas de miles de simulaciones. Errores correlacionados entre estados | BD histórica desde 1998. Comparación within-race. Polls partidarios: prior 4pp de sesgo | Sí: economía, aprobación, incumbencia. Reducido si incumbente no se presenta | Parcial |
| **Silver Bulletin (Nate Silver)** | EE.UU. | Simple/Advanced Plus-Minus, mean-reverted. Cap por firma | 80.000 simulaciones. Calibración empírica con error histórico real (~2.5-4.5pp nacional) | Mean-reverted bias desde 1998. Distinción house effect vs. bias real | Elasticidad estatal, inferencia cross-state | No |
| **The Economist** | EE.UU./Global | (n/600)^0.5. Toplines, no microdata | Bayesiano jerárquico dinámico en R/Stan con MCMC. Correlación entre estados y variación temporal | Modelado explícito. Errores compartidos entre consultoras. No-respuesta diferencial | Sí: prior multivariado desde economía, aprobación, polarización. Blend endógeno | Sí (GitHub) |
| **RealClearPolitics** | EE.UU. | **Ninguna**: promedio aritmético simple. Selección editorial | Ninguno: solo toplines | Ninguna | No | No |
| **Polling Observatory (U. Manchester)** | Reino Unido | Series temporales. Sin fundamentals | Énfasis en distinguir ruido vs. tendencia | No formalizado | Explícitamente NO | No |
| **Electoral Calculus** | Reino Unido | MRP (Multilevel Regression and Post-stratification) | Varianza del MRP a nivel circunscripción | Ponderación demográfica/política en survey weighting | Demographics + voto pasado | No |
| **AS-COA Poll Trackers** | Latam | Compilación visual. Sin ponderación formal | No modelado | No | No | No |
| **AtlasIntel / Latam Pulse** | Latam | Reclutamiento digital aleatorio. Encuestas propias, no agregación | Margen de error clásico SRS | N/A (encuestadora, no agregador) | No | No |
| **Wikipedia Poll Aggregators** | Europa | Compilación crowdsourced. Algunos promedios simples | Ninguno formal | No | No | No |

---

## Hallazgo clave

**No existe un agregador formal de encuestas para Argentina 2027.**

Las encuestas argentinas se publican individualmente y son compiladas por periodistas (Clarín, iProfesional), pero no hay un agregador con metodología estadística formal. El Votómetro de CIGOB es, hasta donde la investigación pudo determinar, **el único proyecto de agregación ponderada para Argentina**.

---

## Ranking metodológico

1. **The Economist** — más académicamente riguroso (Bayesiano jerárquico, código público, papers peer-reviewed)
2. **FiveThirtyEight** — más robusto en producción, mejor documentado operativamente
3. **Silver Bulletin** — mejor calibración empírica de incertidumbre
4. **Electoral Calculus** — innovador en MRP, único con proyección a nivel circunscripción
5. **RealClearPolitics** — más simple, más popular, metodológicamente débil
