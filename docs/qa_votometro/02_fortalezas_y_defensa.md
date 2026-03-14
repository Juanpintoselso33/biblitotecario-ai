# Fortalezas del Votómetro: cómo defenderlo

> Para que Luis y el equipo sepan qué argumentar cuando lleguen las críticas.

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

### 2. Monte Carlo con 10.000 simulaciones — comunica incertidumbre

Mostrar probabilidades de primera vuelta en lugar de solo porcentajes puntuales es lo que hacen FiveThirtyEight y The Economist. En Argentina, ningún outlet hace esto sistemáticamente. El Votómetro está 5 años adelantado a la práctica periodística local.

### 3. Verificación constitucional en cada simulación

Chequear Art. 97-98 CN (45% o 40%+10pp) en cada simulación del Monte Carlo es una funcionalidad única que conecta el modelo estadístico con la realidad institucional. Ningún modelo académico internacional hace esto de forma integrada.

### 4. Cobertura de los 24 distritos con datos de imagen

El desglose provincial con imagen de Milei en los 24 distritos es una visualización que ningún medio argentino ofrece de forma integrada. Es la ventaja CIGOB por excelencia: la dimensión subnacional.

### 5. Corrección de voto oculto bayesiana

El ajuste por voto oculto calibrado con legislativas 2025 es un paso metodológico que la literatura recomienda (Gelman, 2024; SEDICI/UNLP, 2022) y que pocas consultoras argentinas documentan explícitamente.

---

## Respuestas preparadas para críticas comunes

**"Las encuestadoras fallaron en 2023, ¿por qué confiar en esto?"**
> El Votómetro no confía ciegamente en ninguna encuestadora — las pondera y las corrige. Precisamente porque las encuestas argentinas tienen house effects conocidos, usamos un sistema de pesos que penaliza las consultoras con mayor error histórico.

**"¿Por qué sigma=3 si el error fue de 13 puntos en 2023?"**
> *(Reconocer la crítica)* Estamos calibrando ese parámetro con la base histórica de PASO 2023. El valor actual refleja el error esperado dada la agregación de múltiples fuentes ponderadas — el error de una consultora individual no es el mismo que el error del agregador. *(Compromiso de mejora)*: actualizaremos ese parámetro con el backtest formal.

**"¿Por qué Kicillof en el ballotage? Puede no ser el candidato del PJ"**
> Es el escenario más probable dado el estado actual de las encuestas. Tenemos planificado incorporar escenarios alternativos (Bullrich, Villarruel, etc.) en la próxima versión.

**"¿Qué diferencia a esto de un promedio de encuestas con gráficos bonitos?"**
> La ponderación de calidad, la simulación de incertidumbre, la verificación constitucional automática y la proyección subnacional. Ningún otro instrumento público en Argentina hace las cuatro cosas juntas.

---

## Comparación con modelos de referencia

| Característica | FiveThirtyEight | The Economist | Votómetro | Gap |
|---|---|---|---|---|
| Decaimiento temporal | Sí (exponencial) | Sí | Sí (lambda=0.015) | [OK] Equivalente |
| House effects | Sí (bayesiano) | Sí (jerárquico) | Parcial (peso calidad) | [~] Mejorable |
| Monte Carlo | Sí (10.000) | Sí | Sí (10.000) | [OK] Equivalente |
| Correlación entre candidatos | Sí (MVNS) | Sí | No | [X] Gap |
| Transferencia de votos | Sí | Sí | Hardcodeado | [X] Gap crítico |
| Backtest público | Sí | Sí | No | [X] Gap |
| Seed reproducible | Sí | Sí | No | [~] Mejorable |
| Sigma calibrado históricamente | Sí | Sí (~3pp EE.UU.) | No (3pp fijo) | [X] Gap crítico |
| Dimensión subnacional (provincias) | Sí (estados) | Sí (estados) | Parcial (imagen) | [~] Mejorable |
| Verificación constitucional | N/A | N/A | **Único** | [OK] Diferencial exclusivo |
| Datos abiertos / reproducibles | Sí | Sí | No | [X] Gap |
