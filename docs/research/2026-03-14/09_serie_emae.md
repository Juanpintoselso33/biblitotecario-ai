# Serie EMAE — Actividad Economica Mensual
**Fuente:** INDEC - Estimador Mensual de Actividad Economica
**Descarga oficial:** `indec.gob.ar/ftp/cuadros/economia/sh_emae_mensual_base2004.xls`
**XLS descargado:** Si

---

## Serie variacion interanual — Periodo Milei

| Mes | EMAE ia % | Contexto |
|-----|----------|----------|
| 2023-12 | -4.5% | ultimo mes Massa |
| 2024-01 | -4.2% | inicio ajuste Milei |
| 2024-02 | -3.6% |  |
| 2024-03 | -8.3% | piso recesion |
| 2024-04 | -7.5% |  |
| 2024-05 | -3.3% |  |
| 2024-06 | -2.5% |  |
| 2024-07 | -1.7% |  |
| 2024-08 | +0.5% | primer mes positivo |
| 2024-09 | +3.3% |  |
| 2024-10 | +5.0% |  |
| 2024-11 | +5.3% |  |
| 2024-12 | +5.5% | cierre primer año |
| 2025-01 | +6.4% | inicio segundo año |
| 2025-02 | +5.7% |  |
| 2025-03 | +5.5% |  |
| 2025-04 | +7.8% | maximo de la recuperacion |
| 2025-05 | +5.2% |  |
| 2025-06 | +6.3% |  |
| 2025-07 | +2.8% | desaceleracion |
| 2025-08 | +2.2% |  |
| 2025-09 | +4.8% |  |
| 2025-10 | +3.2% |  |
| 2025-11 | -0.1% | unico mes negativo del año |
| 2025-12 | +3.5% | cierre 2025: +4.4% anual |
| 2026-01 | pendiente | pendiente (26-mar-2026) |
| 2026-02 | pendiente |  |

## Lectura para el modelo de fundamentals

```javascript
// EMAE variacion interanual - actualizar cuando INDEC publica (~ultimo dia del mes siguiente)
const EMAE_IA_ACTUAL = 3.5;  // diciembre 2025 (ultimo disponible al 14-mar-2026)
// Escala de referencia:
//   > +5%: crecimiento fuerte (favorece incumbente)
//   0% a +5%: crecimiento moderado
//   < 0%: contraccion (perjudica incumbente)
// Uso en prior de fundamentals:
const ajusteEMAE = (EMAE_IA_ACTUAL - 3.0) * 0.15; // +0.075pp con dato actual
```
