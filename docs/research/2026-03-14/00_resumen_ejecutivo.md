# Research: Agregadores Electorales Mundiales — Resumen Ejecutivo
**Fecha:** 14 de marzo de 2026
**Fuente:** Investigación con Tavily (12 búsquedas, modelo Opus)
**Propósito:** Roadmap de mejoras al Votómetro Argentina 2027

---

## Hallazgo central

**El Votómetro de CIGOB es el único agregador ponderado de encuestas para la elección presidencial argentina 2027.** No existe ningún equivalente local. Las compilaciones de Clarín, iProfesional y otros medios son listas de encuestas, no agregaciones con metodología estadística formal.

---

## Los 3 cambios que más impacto tendrían en el Votómetro

### 1. Trend line + bandas de incertidumbre
**Esfuerzo: MEDIO | Impacto: MUY ALTO**

Todos los agregadores serios del mundo (538, Silver, Economist) muestran tendencias, no promedios estáticos. La combinación EWMA + regresión local es la más probada. Las bandas de incertidumbre son lo que distingue un modelo probabilístico de una tabla de números.

Pasar de "LLA: 41%" a "LLA: 41% con banda 36-46%" comunica honestidad epistémica.

### 2. Corrección formal de house effects
**Esfuerzo: BAJO | Impacto: ALTO**

Actualmente el Votómetro pondera menos a consultoras sesgadas pero **no corrige el sesgo**. Esto es como bajar el volumen de un parlante desafinado en lugar de afinarlo. La corrección es simple (tabla aditiva) y los datos históricos 2023-2025 ya existen para calibrar.

FiveThirtyEight y Silver coinciden: la corrección de house effects es lo que más mejora la precisión de un promedio de encuestas.

### 3. Prior de fundamentals
**Esfuerzo: MEDIO | Impacto: ALTO**

A >500 días de la elección, las encuestas electorales son indicativas pero volátiles. Un ancla de fundamentals (aprobación presidencial + percepción económica + incumbencia) estabiliza el modelo. The Economist demostró que la combinación polls + fundamentals supera a cualquiera de los dos por separado.

---

## Situación actual del Votómetro vs. estándares mundiales

| Dimensión | Votómetro actual | Estándar mundial (538/Economist) |
|-----------|-----------------|----------------------------------|
| Ponderación | Quíntuple multiplicativa | Multiplicativa + corrección aditiva |
| Incertidumbre | σ=6.5 calibrado, IC90 en número | IC visual como banda sombreada |
| House effects | Como peso (reduce influencia) | Como corrección aditiva del valor |
| Fundamentals | No incorporados | Prior con peso decreciente al E-Day |
| Trend line | Promedio estático | EWMA + regresión local + mezcla |
| Actualización | Manual, hardcoded | Automática (JSON/API) ← ya implementado |
| Herding penalty | No | Sí (538) |
| Transparencia | Alta (código público) | Variable (538: parcial, Economist: sí) |

---

## Sigma: ¿6.5 es correcto para 2027?

El sigma=6.5 se calibró al error histórico de PASO 2023 (8-13pp). Pero el patrón muestra reducción sistemática:
- PASO 2023: ~10pp de error promedio
- General 2023: ~4-5pp
- Legislativas 2025: ~2pp

**El sigma debería ser dinámico (decreciente) a medida que LLA se normaliza como opción electoral y los modelos de las consultoras mejoran.**

---

## Ver documentos completos

- `01_tabla_comparativa_agregadores.md` — tabla de 9 agregadores mundiales
- `02_analisis_profundo_top4.md` — FiveThirtyEight, Silver, Economist, Electoral Calculus
- `03_tecnicas_mejora_votometro.md` — 8 propuestas con código JS
- `04_contexto_argentino.md` — error histórico, efecto PASO, landscape local
- `05_fuentes_bibliografia.md` — papers, código fuente, artículos
