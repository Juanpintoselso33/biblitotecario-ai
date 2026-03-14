# Datos de Fundamentals para el Votómetro
**Research date:** 14 de marzo de 2026
**Fuente:** Tavily (4 búsquedas)
**Propósito:** Calibrar el prior de fundamentals (Mejora 4) con datos reales

---

## Variable 1: Aprobación Presidencial

### Fuentes disponibles

| Consultora | Publicación | Frecuencia | Acceso | Último dato |
|------------|-------------|-----------|--------|-------------|
| **Analogías** | Web / medios | Mensual | Libre (vía medios) | Feb 2026: 38.2% aprobación |
| **Pulso Research** (Brújula Social) | Perfil | Mensual | Libre | Mar 2026: 37.2% positiva |
| **AtlasIntel** (LatAm Pulse) | Bloomberg Línea | Mensual | Libre | Nov 2025: 42.6% |
| **Giacobbe** | iProfesional | Mensual | Libre (vía medios) | Feb 2026: ~42.8% aceptación |

### Serie histórica reciente

| Mes | Aprobación (promedio consultoras) | Contexto |
|-----|----------------------------------|----------|
| Jul 2025 | ~45-47% | Máximo local del año |
| Sep 2025 | ~46% | Pre-elecciones |
| Oct 2025 | ~39.9% (AtlasIntel, mínimo) | Baja pre-elecciones |
| Nov 2025 | 42.6% (AtlasIntel) | Rebote post-victoria legislativa |
| Dic 2025 | ~45% estimado | Festejo |
| Feb 2026 | 38.2% (Analogías) / 42.8% (Giacobbe) | Caída. Peor desde jul 2025 |
| Mar 2026 | 37.2% (Pulso/Brújula Social) | -7pp desde sep 2025 |

**Valor a usar en el modelo (mar 2026):** ~39% (promedio consultoras)

**Tendencia:** Caída sostenida desde sep 2025. -7pp en 6 meses, a pesar de la victoria legislativa de oct 2025. Por primera vez, más personas responsabilizan a Milei (46.9%) que al kirchnerismo (41.6%) por la situación económica.

### Cómo obtenerlo mensualmente

1. **Analogías** → buscar informe mensual en medios (La Voz, iProfesional, Infobae)
2. **Pulso Research / Brújula Social** → buscar en Perfil cada mes
3. **AtlasIntel LatAm Pulse** → `atlasintel.org/polls/latam-pulse` (Bloomberg Línea publica los resúmenes gratis)

No existe un repositorio centralizado con API. El operador debe consolidar manualmente. **Frecuencia recomendada: mensual**, usando el promedio de las 3-4 consultoras disponibles.

---

## Variable 2: Índice de Confianza del Consumidor (ICC)

### Fuente única: Universidad Torcuato Di Tella (CIF)

- **URL:** `utdt.edu/ver_contenido.php?id_contenido=2575&id_item_menu=4982`
- **Contacto para serie histórica:** Agustín Samprón — `cifra2@utdt.edu`
- **Suscripción comunicado de prensa:** gratuita (vía el mismo link)
- **Datos desagregados (por región, ingreso):** tienen costo — contactar al CIF
- **Realizado por:** Poliarquía Consultores, ~1.000 casos en 40 centros urbanos
- **Publicación:** tercer semana de cada mes

### Escala y lectura

El ICC se mide en puntos (0-100). Valor neutral ~50. Por debajo = pesimismo dominante.

### Serie reciente

| Mes | ICC (puntos) | Variación mensual | Contexto |
|-----|-------------|-------------------|---------|
| Oct 2025 | 42.3 | — | Mínimo pre-elecciones |
| Nov 2025 | +8.8% → ~46 | +8.8% | Euforia post-victoria legislativa |
| Dic 2025 | -1.1% → ~45.5 | -1.1% | Estabilización |
| Ene 2026 | **46.57** | +2.2% | Leve recuperación |
| Feb 2026 | **44.4** | -4.7% | Peor desde oct 2025 |

**Valor a usar en el modelo (feb 2026):** 44.4 puntos

**Interpretación:** Por debajo de 50, indica que la mayoría de los consumidores percibe condiciones desfavorables. Todos los subíndices cayeron en feb 2026: Situación Personal -7.62%, Situación Macroeconómica -5.37%. La confianza está -6.1% interanual respecto a feb 2025.

### Transformación para el modelo

Para usarlo como variable de "percepción económica" en `calcularPriorFundamentals()`, convertir a porcentaje normalizado:

```javascript
// ICC Di Tella: escala 0-100, neutral en ~50
// Transformar a % "optimismo" comparable con otras variables
const icc = 44.4;
const optimismo = icc; // ya está en escala 0-100
// Uso en el modelo: ajusteEconomia = (optimismo - 40) * 0.2
// Con icc=44.4: ajuste = (44.4 - 40) * 0.2 = +0.88pp a LLA
```

---

## Variable 3: Resultados Legislativas 2025

### Datos definitivos (26 octubre 2025)

**Nacional (Cámara de Diputados):**
| Fuerza | Votos nacionales | % votos | Diputados ganados |
|--------|-----------------|---------|-------------------|
| **LLA (La Libertad Avanza)** | 8.890.297 | **40.84%** | 64 (→ 80 en bloque total) |
| Fuerza Patria (peronismo, sello principal) | ~7M | **24.50%** | 44 |
| Peronismo total (todos los sellos) | — | **~31-34%** | — |
| UCR + aliados | — | ~8% | — |
| FIT-U | — | ~3-5% | — |

**Fuente primaria:** CNN Español (con escrutinio 99.4% mesas): LLA 40.84%, Fuerza Patria 24.50%

**Notas:**
- LLA ganó en 15 de 24 provincias
- Participación: 66-67.9% (mínimo histórico desde el retorno de la democracia)
- El peronismo se presentó bajo múltiples sellos → 24.5% es solo Fuerza Patria; contando todos los sellos peronistas el total sube a ~31-34%

**Valor a usar como baseline en el modelo:** LLA = **40.84%** (resultado definitivo diputados nacionales)

> Nota: En la research previa usamos 47% como baseline, tomando proyecciones de intención de voto presidencial. El 40.84% es el resultado real en votos legislativos. Para el prior de fundamentals presidencial, el 40.84% es el dato más sólido disponible; el "salto" presidencial vs legislativo se modela con el bono de incumbencia.

---

## Resumen: valores a hardcodear en el modelo ahora

```javascript
function calcularPriorFundamentals() {
  // === DATOS REALES (actualizar mensualmente) ===
  const baselineLLA = 40.84;  // Resultado definitivo legislativas oct 2025
  const aprobacion = 39;      // Promedio consultoras, mar 2026
  const icc = 44.4;           // Di Tella, feb 2026
  const optimismo = icc;      // 0-100, neutral=50

  // === AJUSTES ===
  const ajusteAprobacion = (aprobacion - 45) * 0.3;  // -1.8pp
  const bonoIncumbencia = 2;                           // pp conservador
  const ajusteEconomia = (optimismo - 40) * 0.2;     // +0.88pp

  return {
    lla: baselineLLA + ajusteAprobacion + bonoIncumbencia + ajusteEconomia,
    // = 40.84 - 1.8 + 2 + 0.88 = 41.92%
  };
}
```

**Prior de fundamentals LLA (mar 2026):** ~41.9%

Comparar con el promedio actual de polls (~40-42%) → los fundamentals y las encuestas están alineados en este momento, lo que da solidez al modelo.

---

## Protocolo de actualización mensual

| Variable | Fuente | Cuándo actualizar | Quién |
|----------|--------|-------------------|-------|
| Aprobación presidencial | Analogías + Pulso (Perfil) | Primer semana del mes | Operador |
| ICC Di Tella | utdt.edu/icc | Tercer semana del mes | Operador |
| Resultados electorales | Solo cambia con elecciones | Post-PASO ago 2027, post-Generales oct 2027 | Operador |
