# Serie Histórica ICC Di Tella — Período Milei
**Reconstruida:** 14 de marzo de 2026
**Fuentes:** Comunicados mensuales UTDT + anclas verificadas en Infobae/Trading Economics

---

## Metodología de reconstrucción

1. **Anclas verificadas** (valores absolutos confirmados en múltiples fuentes)
2. **Encadenamiento** de variaciones % mensuales publicadas por UTDT (solo % de cambio, no valor absoluto)
3. **Interpolación geométrica** para ago-sep 2025 (datos no disponibles)
4. **Sin datos** para dic 2023 - abr 2024 (variaciones no recuperadas)

## Anclas verificadas

| Mes | ICC (pts) | Fuente |
|-----|----------|--------|
| 2025-01 | 47.38 | Perfil: pico del gobierno de Milei |
| 2025-10 | 42.30 | Di Tella/Infobae: minimo desde octubre 2025 |
| 2025-12 | 45.55 | Trading Economics (previous de ene 2026) |
| 2026-01 | 46.57 | Comunicado Di Tella |
| 2026-02 | 44.40 | Comunicado Di Tella |

## Serie completa

| Mes | ICC (pts) | Estado |
|-----|----------|--------|
| 2023-12 | N/A | ✗ sin dato |
| 2024-01 | N/A | ✗ sin dato |
| 2024-02 | N/A | ✗ sin dato |
| 2024-03 | N/A | ✗ sin dato |
| 2024-04 | N/A | ✗ sin dato |
| 2024-05 | 38.27 | reconstruido |
| 2024-06 | 37.20 | reconstruido |
| 2024-07 | 39.07 | reconstruido |
| 2024-08 | 41.43 | reconstruido |
| 2024-09 | 38.98 | reconstruido |
| 2024-10 | 42.41 | reconstruido |
| 2024-11 | 45.00 | reconstruido |
| 2024-12 | 46.04 | reconstruido |
| 2025-01 | 47.38 | ✓ ancla verificada |
| 2025-02 | 47.24 | reconstruido |
| 2025-03 | 44.07 | reconstruido |
| 2025-04 | 44.07 | reconstruido |
| 2025-05 | 45.44 | reconstruido |
| 2025-06 | 45.44 | reconstruido |
| 2025-07 | 46.35 | reconstruido |
| 2025-08 | 44.96 | ⚠ estimado (interpolado) |
| 2025-09 | 43.61 | ⚠ estimado (interpolado) |
| 2025-10 | 42.30 | ✓ ancla verificada |
| 2025-11 | 46.02 | reconstruido |
| 2025-12 | 45.55 | ✓ ancla verificada |
| 2026-01 | 46.57 | ✓ ancla verificada |
| 2026-02 | 44.40 | ✓ ancla verificada |

## Interpretación

- **Escala:** 0-100 puntos. Neutral ≈ 50. Por debajo = pesimismo dominante.
- **Media histórica (2001-2026):** ~44.7 pts (Trading Economics)
- **Máximo histórico:** 60.97 pts (enero 2007)
- **Mínimo histórico:** 28.44 pts (septiembre 2002, crisis)
- **Pico Milei:** 47.38 pts (enero 2025)
- **Febrero 2026:** 44.4 pts (-6.1% interanual)

## Para uso en el modelo

```javascript
// Actualizar mensualmente con el valor publicado por Di Tella (~tercer semana del mes)
// Fuente: utdt.edu/ver_contenido.php?id_contenido=2575
const ICC_ACTUAL = 44.40;  // feb 2026
const OPTIMISMO = ICC_ACTUAL;  // escala 0-100, compatible con calcularPriorFundamentals()
```
