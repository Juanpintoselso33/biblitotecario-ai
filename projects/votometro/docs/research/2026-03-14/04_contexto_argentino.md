# Contexto Argentino: Encuestas y Elecciones 2023-2027
**Research date:** 14 de marzo de 2026

---

## 1. Patrón de Error Histórico de las Encuestadoras

### PASO agosto 2023
- **Error promedio en LLA: ~8-13pp** — ninguna encuesta predijo el 30%
- Zuban Córdoba fue la más cercana: 24.5% (vs 30.3% real) → error 5.8pp
- Causa principal: voto oculto, no-respuesta diferencial, muestras inadecuadas
- Sigma implícito del error: ~6.5pp (base del parámetro actual del Votómetro)

### General octubre 2023
- **Error promedio en LLA: ~4-5pp** — mejora significativa post-PASO
- DC Consultores la más precisa: LLA 41.2% vs 40.84% real (error 0.36pp)
- La mayoría subestimó la brecha LLA-PJ

### Ballotage noviembre 2023
- Error menor: competencia binaria simplificó la medición
- Las encuestas promediaron un resultado más cercano al real

### Legislativas 2025
- **Error promedio: ~2pp** — reducción sistemática respecto a 2023
- Milei ya era "voto conocido", no oculto
- Las consultoras que invirtieron en metodología post-PASO 2023 mostraron resultados notablemente mejores

### Implicación para el Votómetro

| Elección | Error promedio LLA | Sigma implícito |
|----------|--------------------|--------------------|
| PASO 2023 | ~10pp | ~6.5 |
| General 2023 | ~4-5pp | ~3 |
| Legislativas 2025 | ~2pp | ~1.2 |

**El sigma=6.5 calibrado a PASO 2023 es progresivamente excesivo.** Para 2027, un sigma dinámico que decrezca a medida que se acerca la elección y que refleje la "normalización" de LLA como opción electoral sería más preciso.

---

## 2. El "Efecto PASO" en Argentina

Las PASO (Primarias Abiertas Simultáneas y Obligatorias) son únicas en el mundo. Sus características como predictor:

- **Funcionan como encuesta real obligatoria**: con ~30 millones de votantes, son el "polling" más grande posible
- **Alta correlación general→PASO**: históricamente, la PASO predice bien la general
- **Excepción 2019**: Macri recuperó terreno post-PASO, mostrando que la caída de PASO puede no ser definitiva
- **Para el Votómetro 2027**: cuando se celebren las PASO (estimado agosto 2027), deberían funcionar como un "superdatapoint" que recalibra todo el modelo:
  - Resetear el sigma al error observado en las PASO
  - Ponderar las PASO como N=10.000.000+ (o simplemente como dato privilegiado con peso muy alto)
  - Actualizar los house effects basados en el delta real vs predicho de cada consultora

---

## 3. Landscape de Encuestadoras Activas en Argentina (2025-2026)

| Consultora | Metodología | Calificación estimada | Presencia 2025-2026 |
|------------|------------|----------------------|---------------------|
| DC Consultores | Mixta | A+ | Alta |
| CB Consultora | Telefónica | A | Alta |
| Atlas Intel | Digital aleatoria | A | Alta |
| Opinaia | Online | B+ | Alta |
| Trends | Online | B+ | Media |
| Proyección | Presencial | B | Media |
| Zuban Córdoba | Telefónica | B- | Alta |
| Equipo Mide | Online | B+ | Media |
| Analogías | Presencial | A- | Alta |
| Isasi | Presencial | B | Baja |

---

## 4. No Existe un Agregador Formal para Argentina

La investigación confirma que:

- **No hay FiveThirtyEight argentino.** Las compilaciones de Clarín, iProfesional y otros medios son listas de encuestas con promedios simples, sin metodología estadística formal.
- **CELAG** (Centro Estratégico Latinoamericano de Geopolítica) realiza encuestas propias en Argentina pero no agrega las de otras consultoras.
- **AtlasIntel** (Brasil) incluye Argentina en su Latam Pulse como **encuestadora**, no como agregador.
- **AS-COA** tiene poll trackers para Perú, Colombia, Brasil y Costa Rica, pero no para Argentina.
- **Wikipedia** tiene una lista de encuestas argentinas pero sin ponderación ni metodología.

**El Votómetro de CIGOB es, hasta donde la investigación pudo determinar, el único proyecto de agregación ponderada para la elección presidencial argentina 2027.**

---

## 5. Variables Fundamentals Relevantes para Argentina

Para una eventual implementación de prior de fundamentals (ver Mejora 4 en `03_tecnicas_mejora_votometro.md`), las variables más relevantes para Argentina son:

| Variable | Fuente | Frecuencia | Valor actual (mar. 2026) |
|----------|--------|-----------|--------------------------|
| Aprobación presidencial | Múltiples consultoras | Mensual | ~50% positiva (Trends, ene-2026) |
| Percepción económica | Opinaia, CB, Trends | Mensual | ~45% espera mejora |
| Resultado elecciones previas | INDEC/Justicia Electoral | Por elección | LLA ~47% (leg. 2025) |
| Inflación anual | INDEC | Mensual | En descenso sostenido |
| Desempleo | INDEC/EPH | Trimestral | ~7% |

**Baseline para el modelo de fundamentals:** LLA=47% (legislativas 2025) + ajuste por aprobación + bono incumbencia (~2pp conservador).
