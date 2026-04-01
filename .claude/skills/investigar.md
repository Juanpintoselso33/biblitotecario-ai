---
name: investigar
description: Proceso completo para realizar una investigación con MCPs (Tavily, ScholarAI, WebSearch), indexarla correctamente y dejar registro duradero como fuente. Usar cuando haya una pregunta metodológica, técnica o conceptual que requiera evidencia externa.
---

# Skill: Investigar con MCPs y dejar registro indexado

## Cuándo aplicar

Cuando haya una pregunta que requiere evidencia externa — metodológica, técnica, académica o de contexto — y no alcanza con el conocimiento interno. Ejemplos:
- "¿Cómo hacen esto en otros modelos?"
- "¿Hay literatura sobre X?"
- "Investiga con Tavily qué se hace en estos casos"

## Proceso paso a paso

### 1. Formular preguntas de búsqueda (3-5 queries)

Antes de buscar, descomponé el tema en ángulos distintos:
- **Técnico/académico**: terminología formal, papers, modelos de referencia
- **Aplicado**: cómo lo implementan proyectos reales (538, Economist, etc.)
- **Contexto local**: si aplica, buscar evidencia en el dominio específico (ej: Argentina)
- **Contraejemplos**: buscar también la perspectiva contraria o limitaciones

### 2. Buscar en paralelo

Usar **Tavily y WebSearch simultáneamente** con las queries formuladas. Si está disponible ScholarAI, usarlo para papers académicos.

```
- tavily_search: query técnica/académica
- WebSearch: query aplicada (modelos reales)
- WebSearch: contexto local / evidencia empírica
- tavily_search: contraejemplos o críticas
```

### 3. Sintetizar hallazgos

Antes de escribir el archivo, identificar:
- **Consenso**: qué dice la mayoría de las fuentes
- **Disidencia**: qué fuentes van en contra y por qué
- **Aplicabilidad**: qué es relevante para el problema concreto
- **Vacíos**: qué no encontraste y por qué importa

### 4. Guardar el resultado en `docs/investigaciones/`

Nombre del archivo: `YYYY-MM-DD_tema_slug.md`

Estructura mínima del archivo:

```markdown
# Investigación: [título descriptivo]

**Fecha:** DD de mes de YYYY
**Contexto:** [qué problema motivó la búsqueda]
**Pregunta:** [la pregunta exacta que se intentó responder]

---

## Hallazgo central

[1-3 oraciones. La respuesta directa a la pregunta.]

---

## Evidencia

[tablas, datos, citas textuales relevantes]

---

## Qué dice la literatura / fuentes de referencia

[por fuente o por tema, con citas textuales cuando sea posible]

---

## Aplicabilidad al proyecto

[cómo se traduce esto en una acción o cambio concreto para CIGOB/Votómetro]

---

## Limitaciones y vacíos

[qué no se encontró, qué habría que buscar más]

---

## Fuentes

- [Título](URL)
- [Título](URL)
```

### 5. Referenciar desde MEMORY.md si es un hallazgo duradero

Si la investigación produce un hallazgo que cambia cómo se trabaja el proyecto (no solo un dato puntual), guardar también una memoria de referencia:

```markdown
---
name: investigacion_TEMA
type: reference
description: Investigación sobre X — hallazgo central y dónde está el archivo
---
Ver docs/investigaciones/YYYY-MM-DD_tema.md
Hallazgo: [una línea]
```

### 6. Si corresponde: implementar y testear

Si la investigación lleva a un cambio técnico:
1. Implementar en el código
2. Testear con Playwright u otra herramienta
3. Documentar el resultado del test en el mismo archivo de investigación (sección "Resultado implementado")
4. Commitear todo junto: código + investigación + skill si aplica

---

## Errores comunes a evitar

- **No buscar solo una vez**: siempre al menos 3 queries desde ángulos distintos
- **No confundir fuente con verdad**: anotar cuándo hay consenso vs. disidencia
- **No guardar solo el resultado**: guardar también el razonamiento y las fuentes
- **No omitir el contexto local**: para Argentina/CIGOB, buscar siempre evidencia local además de la académica internacional
- **No dejar la investigación suelta**: siempre queda en `docs/investigaciones/` con fecha
