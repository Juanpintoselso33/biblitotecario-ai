# Votómetro Argentina 2027 — Análisis cruzado con documentos nuevos
**Fecha:** 12 de abril 2026  
**Documentos cruzados:**
- `docs/documentos_nuevos/260403 COMENTARIOS VOTOMETRO.docx` — feedback editorial/metodológico
- `docs/documentos_nuevos/260407 VOTOMETRO ESQUEMA.pptx` — propuesta de índice revisado

---

## 1. Estado actual del modelo (resumen técnico)

| Variable | Valor actual |
|---|---|
| LLA (Milei) — proyección central | ~41.0–41.2% |
| PJ/UxP (Kicillof) | ~29.5–30.0% |
| Prior fundamentals LLA | 40.98% |
| Blend encuestas/fundamentals | 50/50 (560 días restantes) |
| Escenario central | Primera vuelta Art. 98 (sobre la media) |
| Sigma 1ra vuelta | 6.5pp |
| Sigma ballotage (tiempo-variable) | ~9.98pp |
| Última encuesta incorporada | CB Global Data, 25-mar-2026 |
| Fundamentals hardcodeados hasta | marzo 2026 (aprobación 38%, ICC 42.03, EMAE 1.9%) |

---

## 2. Feedback del documento 260403 — comentarios al Votómetro

### 2.1 Sobre la sección VALORACIÓN

**Lo que dice el documento:**
- La tendencia va, pero no debería mostrar "primera"
- El saldo neto no debería ser "neto histórico" — sugiere vincularlo a hechos relevantes (aumento del dólar, caso Adorni, caso Libra)
- Propone sacar las consultoras que participan de la muestra del gráfico
- El índice Di Tella: "para conversar o tenerlo solo como referencia"

**Implicancias técnicas:**
- El gráfico de valoración actual usa un saldo neto simple (aprobación − desaprobación) sin eventos anotados
- Requiere: agregar un array de `eventos` con fecha + label, y renderizarlos como marcadores en el gráfico de tendencia
- La aprobación en el modelo (38%) es un input de fundamentals, no solo visual — cualquier cambio en la fuente afecta la proyección

### 2.2 Sobre la sección INTENCIÓN DE VOTO

**Lo que dice el documento:**
- Las encuestas individuales: no mostrarlas (o mostrarlas solo al final)
- Evolución temporal: dejar solo intención de voto, sin mezclar valoración. Ventanas: último año, 3 meses, 1 mes
- "¿Quiénes están representados por el violeta y el azul?" — hay confusión de colores en el gráfico actual
- Primera vuelta: dejarla como intención de voto, **no poner nombres** (PRO: Bullrich no iría hoy, solo espacio)
- Ballotage: presentarlo como **condicional** ("si hubiera segunda vuelta...")
- Sacar los escenarios
- Comparativa 23/25/27: no se entiende, sacarla
- Mapa federal: no se entiende si es una sola encuesta (Global Data), a conversar

**Implicancias técnicas:**
- La distinción espacio/candidato del modelo (+4pp LLA, +2pp PJ) ya anticipa el problema de los nombres, pero la UI actual muestra nombres
- El ballotage como sección condicional implica un rediseño de la sección: pasaría de ser un resultado paralelo a ser un módulo secundario que se activa cuando la simulación Monte Carlo arroja >X% de probabilidad de ballotage
- La comparativa 2023/2025/2027 usa datos interpolados (período dic-2023 a oct-2024 son encuestas tipo C, reconstruidas) — es razonable sacarla de la UI pública aunque se mantenga como input del modelo

### 2.3 Sobre GOBERNADORES

**Lo que dice el documento:**
- No usarla con una sola encuesta, "a conversar cuándo usarla"

**Implicancias técnicas:**
- El modelo tiene un objeto `districts` con imagen positiva en 21/24 jurisdicciones, pero es solo 1 encuesta (Global Data)
- Correcto: no publicar hasta tener al menos 3 encuestas por provincia o una serie temporal mínima

### 2.4 Sobre la estructura propuesta (PPTX 260407)

El esquema revisado propone este índice:

| Sección | Propuesta del documento | Estado actual | Acción |
|---|---|---|---|
| Portada | Poner el mes | Fijo "2027" | Agregar `mesActual` dinámico |
| Intención de voto | Poner "intención de voto", sacar apellidos | Muestra nombres | Cambiar labels a espacios |
| 2da vuelta | "Si hubiera ballotage, este sería el resultado" | Sección fija con escenarios | Rediseñar como condicional |
| Ballotage detalle | Milei vs Kisi, sacar PRO, dividir "otros" en cercanos a LLA y cercanos a PJ | Hoy: escenario único con PRO | Requiere array de transferencias |
| Valoración | Solo aprobación de gestión, sin Di Tella por ahora | Muestra Di Tella prominente | Mover Di Tella a sección técnica o sacar |
| Índice Di Tella | "conversar para entender qué expresa" | Aparece como fundamentals | Explicación de uso interno vs. público |

---

## 3. Diagnóstico cruzado: técnico vs. editorial

### Tensiones identificadas

| Tema | Posición editorial (docs nuevos) | Estado técnico actual | Tensión |
|---|---|---|---|
| Nombres de candidatos | Sacarlos, mostrar solo espacio | Los nombres están en labels y en la corrección espacio/candidato | La corrección +4pp usa la categoría candidato/espacio, no el nombre. Separable. |
| Ballotage condicional | Solo si hay >X% prob. de segunda vuelta | Siempre se muestra en paralelo | Requiere umbral: ¿activar si P(ballotage) > 30%? 40%? |
| Encuestas visibles | No mostrarlas en la UI | El modelo las usa como input central | No hay tensión en el modelo, solo en la UI — se pueden ocultar sin afectar el cálculo |
| Di Tella | Solo referencia interna | Es un input del prior de fundamentals | Si se saca de la UI, sigue siendo un input del modelo. Decisión: ¿se comunica o no? |
| Comparativa histórica | Sacarla | Es la base de la corrección de sesgo y el prior | Se puede sacar de la UI sin sacarla del modelo |

### Lo que el feedback NO cuestiona

- La metodología de ponderación temporal (decaimiento λ=0.015)
- El Monte Carlo y el sigma calibrado
- El blend con fundamentals
- El prior de incumbencia

Esto sugiere que **el motor del modelo está validado**; lo que está en discusión es la capa de comunicación pública.

---

## 4. Problemas técnicos urgentes (independientes del feedback editorial)

### Alta urgencia

1. **Actualizar fundamentals de abril 2026**: aprobación (datos nuevos de imagen de gestión), ICC Di Tella de marzo-abril, EMAE de febrero 2026. Los valores actuales son de marzo 2026.
2. **CB Global Data 25-mar-2026 sobrepondera**: calidad A + 18 días = peso 0.899. Con las demás encuestas del período en peso 0.35-0.48, una sola encuesta tipo candidato con LLA 28.3% (→ 32.3% tras corrección) está ejerciendo influencia desproporcionada. Monitorear si la próxima actualización normaliza o amplifica esto.

### Media urgencia

3. **Ballotage hardcodeado como constante**: los valores 50% (Milei) y 33% (Kicillof) en 2da vuelta son literales en la simulación Monte Carlo. Construir un mini-array de encuestas de ballotage separado para que el valor central sea dinámico.
4. **Etiquetas de colores en gráficos**: el feedback señala confusión sobre qué representa el violeta y el azul. Requiere revisión de la leyenda en el HTML.
5. **Ballotage como sección condicional**: definir el umbral de activación (P(ballotage) > 35% como propuesta) y refactorizar la sección de UI.

### Baja urgencia (roadmap futuro)

6. **Eventos en gráfico de valoración**: array `eventos` con fecha + descripción corta (dólar, caso Adorni, etc.), renderizados como anotaciones verticales en el gráfico de aprobación.
7. **Encuestas de gobernadores**: esperar hasta tener ≥3 encuestas por provincia. No publicar antes.
8. **Comparativa 23/25/27**: mover a sección técnica/metodológica o eliminar de la UI pública. Mantener como input del modelo.

---

## 5. Pregunta estratégica: propiedad del producto

El feedback viene claramente de un actor con criterio editorial fuerte (uso de primera persona, propuestas concretas de diseño). Dado que el Votómetro es "colaboración CIGOB + Redlines Estrategia y Comunicación":

- **Las decisiones de comunicación** (qué mostrar, cómo nombrar, qué es condicional) son del dominio editorial → Redlines / socio externo
- **Las decisiones metodológicas** (sigma, λ, prior de fundamentals, corrección candidato/espacio) son del dominio técnico → CIGOB

El documento de comentarios no cuestiona ninguna decisión metodológica. Solo cuestiona decisiones de comunicación. Esto sugiere que **la división de trabajo está funcionando correctamente** y que la próxima iteración del HTML debería incorporar los cambios editoriales de este feedback sin alterar el motor del modelo.

**Próximo paso concreto sugerido:** reunión de 30 minutos para alinear en tres preguntas abiertas del feedback:
1. ¿Activar ballotage como condicional con qué umbral?
2. ¿Mover Di Tella a referencia interna o mantenerlo visible?
3. ¿Cuándo usar gobernadores (criterio de activación)?

---

## 6. Checklist de implementación (para próxima versión del HTML)

### Cambios de UI (no afectan el motor)
- [ ] Portada: agregar mes dinámico
- [ ] Primera vuelta: labels a espacio (LLA, PJ, PRO, etc.) sin nombres de candidato
- [ ] Ballotage: rediseñar como sección condicional con umbral definido
- [ ] Ballotage detalle: Milei vs. Kisi directamente, sin PRO como tercero
- [ ] Gráfico valoración: agregar anotaciones de eventos relevantes
- [ ] Gráfico evolución: clarificar leyenda de colores (violeta = LLA, azul = PJ?)
- [ ] Sacar comparativa 23/25/27 de la vista pública
- [ ] Mover encuestas individuales al pie o sacarlas
- [ ] Di Tella: mover a sección técnica/nota metodológica

### Cambios de datos (afectan el motor)
- [ ] Actualizar aprobación presidential (abril 2026)
- [ ] Actualizar ICC Di Tella (publicación más reciente)
- [ ] Actualizar EMAE ia (dato de febrero, publicado por INDEC)
- [ ] Construir mini-array de encuestas de ballotage

---

*Generado a partir del análisis técnico del modelo + documentos `260403 COMENTARIOS VOTOMETRO.docx` y `260407 VOTOMETRO ESQUEMA.pptx`*
