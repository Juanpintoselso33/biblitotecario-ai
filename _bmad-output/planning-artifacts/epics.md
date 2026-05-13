---
stepsCompleted: [step-01-validate-prerequisites, step-02-design-epics, step-03-create-stories, step-04-final-validation]
status: complete
completedAt: '2026-05-13'
inputDocuments:
  - _bmad-output/planning-artifacts/prd.md
  - _bmad-output/planning-artifacts/architecture.md
---

# CIGOB Análisis - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for CIGOB Análisis, decomposing the requirements from the PRD and Architecture into implementable stories.

## Requirements Inventory

### Functional Requirements

FR1: Trico ejecuta el colector de cada cinturón de forma independiente sin correr los otros
FR2: El colector macro recolecta indicadores desde fuentes oficiales (INDEC, BCRA, Ministerio de Economía)
FR3: El colector político recolecta indicadores desde fuentes oficiales (Congreso, encuestadoras, medios)
FR4: El colector vida cotidiana recolecta indicadores desde fuentes definidas (ya implementado)
FR5: El colector gestión/CIGOB recolecta indicadores desde fuentes a definir
FR6: El sistema preserva el último valor válido de cada indicador cuando una fuente falla
FR7: El sistema marca con flag explícito los indicadores que usan datos de un período anterior
FR8: Trico genera el Informe ejecutando un único script
FR9: El sistema produce el Informe en formato markdown listo para Drive y reunión
FR10: El sistema produce el Informe en formato JSON con schema estructurado para consumo del dev
FR11: El Informe incluye el estado y score de cada cinturón para el período actual
FR12: El Informe incluye el flag de indicadores desactualizados con la fecha del último dato válido
FR13: El sistema calcula el score de cada cinturón según los indicadores recolectados
FR14: El sistema detecta el barbarismo de riesgo activo (político, tecnocrático, gerencial) según el estado de los cinturones
FR15: El sistema genera alerta cuando más de un cinturón está tensionado (regla matusiana)
FR16: Trico modifica parámetros del modelo (pesos, umbrales) en el código fuente sin afectar la lógica de colección
FR17: Trico agrega un nuevo proyecto al monorepo dentro de `projects/` sin tocar los proyectos existentes
FR18: Cada proyecto tiene README con instrucciones para correr sus scripts
FR19: Los cambios en parámetros metodológicos quedan registrados en el historial de commits con justificación
FR20: El dev del Informe consume el JSON de output sin conocer la metodología interna
FR21: El schema JSON del Informe no introduce breaking changes entre versiones sin aviso explícito en el README del proyecto
FR22: El dev del Votómetro consume el HTML o los datos del Votómetro sin acceso al código de análisis
FR23: Trico agrega nuevas encuestas al Votómetro actualizando el archivo de datos correspondiente
FR24: El Votómetro aplica ponderación quíntuple a las encuestas (decaimiento temporal, calidad, sesgo histórico, orientación del medio, metodología)
FR25: El Votómetro corre simulaciones Monte Carlo y produce estimaciones con intervalos de confianza
FR26: El Votómetro verifica el umbral de los artículos 97-98 CN en cada simulación
FR27: El Votómetro integra el prior de fundamentals con peso decreciente a medida que se acerca la elección

### NonFunctional Requirements

NFR1: Scripts de colección de un cinturón completan en menos de 5 minutos en condiciones normales de red
NFR2: Generador del Informe de Coyuntura completa en menos de 1 minuto una vez disponibles los datos
NFR3: El schema JSON de output del Informe no modifica campos existentes entre versiones sin deprecation notice en el README del proyecto
NFR4: Los outputs del Votómetro (HTML o JSON) mantienen su estructura entre actualizaciones de encuestas
NFR5: Los scripts producen outputs en `projects/<nombre>/output/` sin configuración adicional
NFR6: Las URLs de fuentes de datos están en variables nombradas al inicio de cada script, no dispersas en el código
NFR7: Un desarrollador nuevo corre cualquier script leyendo solo el README del proyecto
NFR8: Los parámetros del modelo (pesos, umbrales de cinturón, factores de barbarismo) están separados del código de procesamiento

### Additional Requirements

- AR1: Restructura del monorepo — crear árbol `projects/informe_coyuntura/` y `projects/votometro/` con estructura completa de directorios definida en architecture.md
- AR2: Migración brownfield — `web/votometro.html` → `projects/votometro/web/votometro.html`; `scripts/vida_cotidiana/` → `projects/informe_coyuntura/scripts/vida_cotidiana.py`
- AR3: Cache de fallback por cinturón en `projects/informe_coyuntura/output/cache/<cinturon>.json` implementado en cada colector
- AR4: Schema JSON v1.0.0 con claves exactas en snake_case: `schema_version`, `generated_at`, `period`, `cinturones.[cinturon].{score, estado, barbarismo_riesgo, indicadores, alerta}`, `barbarismo_activo`, `alerta_multicinturon`, `flags`
- AR5: `config.py` para `informe_coyuntura` con pesos de cinturón, umbrales de estado (0-3 estable / 4-6 en_tension / 7-10 tensionado), URLs de fuentes, mapping barbarismo→cinturón
- AR6: Patrón de colector estándar: constantes URL nombradas → import config → funciones fetch por indicador → calcular_score → load/save_cache → main()
- AR7: Manejo de errores por indicador (granular); exit codes 0/1/2; logging stdout con formato `[WARN] <cinturon>.<indicador>: <desc>. Usando cache.`
- AR8: `generar_informe.py` lee los 4 caches y escribe `informe.json` (schema v1.0.0) + `informe.md` (markdown con frontmatter YAML)
- AR9: Sin starter template — Python puro, `python <script>.py` sin setup previo, `requirements.txt` por proyecto

### UX Design Requirements

N/A — sin UI propia. CIGOB produce outputs (JSON + Markdown) que consumen devs externos.

### FR Coverage Map

FR1 → Epic 2 — Ejecución independiente por cinturón
FR2 → Epic 2 — Colector macro (INDEC, BCRA, Economía)
FR3 → Epic 2 — Colector político (Congreso, encuestadoras, medios)
FR4 → Epic 2 — Colector vida cotidiana (migrado de existente)
FR5 → Epic 2 — Colector gestión/CIGOB
FR6 → Epic 2 — Fallback al último valor válido cuando fuente falla
FR7 → Epic 2 — Flag explícito de indicadores desactualizados
FR8 → Epic 3 — Generación del Informe con un único script
FR9 → Epic 3 — Output Markdown para Drive y reunión
FR10 → Epic 3 — Output JSON schema v1.0.0 para dev externo
FR11 → Epic 3 — Score y estado por cinturón en el período actual
FR12 → Epic 3 — Flag de indicadores desactualizados con fecha último dato
FR13 → Epic 3 — Cálculo de score 0-10 por cinturón
FR14 → Epic 3 — Detección de barbarismo activo (político/tecnocrático/gerencial)
FR15 → Epic 3 — Alerta multicinturón (regla matusiana)
FR16 → Epic 1 — Parámetros del modelo modificables sin tocar lógica de colección
FR17 → Epic 1 — Agregar proyecto al monorepo sin tocar proyectos existentes
FR18 → Epic 1 — README por proyecto con instrucciones para correr scripts
FR19 → Epic 3 — Cambios metodológicos documentados en commits con justificación
FR20 → Epic 3 — Dev del Informe consume JSON sin conocer metodología interna
FR21 → Epic 3 — Schema JSON sin breaking changes sin deprecation notice
FR22 → Epic 4 — Dev del Votómetro consume HTML sin acceso al código de análisis
FR23 → Epic 4 — Trico agrega encuestas actualizando archivo de datos
FR24 → Epic 4 — Ponderación quíntuple (existente, documentar y estabilizar)
FR25 → Epic 4 — Monte Carlo (existente, documentar y estabilizar)
FR26 → Epic 4 — Verificación CN 97-98 (existente, estabilizar)
FR27 → Epic 4 — Prior de fundamentals con peso decreciente (existente, estabilizar)

## Epic List

### Epic 1: Monorepo Foundation & Configuración
El monorepo tiene la estructura definida en la arquitectura, con proyectos autónomos, archivos existentes migrados y `config.py` listo para parametrizar el análisis matusiano. Trico puede clonar el repo y saber exactamente dónde vive cada cosa; cualquier dev puede correr cualquier script leyendo solo el README del proyecto.
**FRs cubiertos:** FR16, FR17, FR18
**ARs cubiertos:** AR1, AR2, AR5, AR9
**NFRs cubiertos:** NFR5, NFR7, NFR8

### Epic 2: Informe de Coyuntura — Colección de Datos
Trico puede ejecutar el colector de cualquier cinturón de forma independiente y el sistema preserva el último dato válido cuando una fuente argentina falla, con flags claros sobre qué datos son frescos y cuáles son del cache.
**FRs cubiertos:** FR1, FR2, FR3, FR4, FR5, FR6, FR7
**ARs cubiertos:** AR3, AR6, AR7
**NFRs cubiertos:** NFR1, NFR6

### Epic 3: Informe de Coyuntura — Generación del Informe
Trico ejecuta un script único que lee los caches, calcula scores matusianos y detecta barbarismos activos, y genera el informe completo en JSON (para el dev externo) y Markdown (para Drive y reunión).
**FRs cubiertos:** FR8, FR9, FR10, FR11, FR12, FR13, FR14, FR15, FR19, FR20, FR21
**ARs cubiertos:** AR4, AR8
**NFRs cubiertos:** NFR2, NFR3, NFR8

### Epic 4: Votómetro — Migración y Estabilización
El Votómetro vive en su path definitivo dentro del monorepo, el workflow de actualización de encuestas está documentado, y el dev puede consumir el HTML actualizado sin fricción ni acceso al código de análisis.
**FRs cubiertos:** FR22, FR23, FR24, FR25, FR26, FR27
**ARs cubiertos:** AR2 (Votómetro)
**NFRs cubiertos:** NFR4

---

## Epic 1: Monorepo Foundation & Configuración

El monorepo tiene la estructura definida en la arquitectura, con proyectos autónomos, archivos existentes migrados y `config.py` listo para parametrizar el análisis matusiano. Trico puede clonar el repo y saber exactamente dónde vive cada cosa; cualquier dev puede correr cualquier script leyendo solo el README del proyecto.

### Story 1.1: Crear estructura de directorios del monorepo

Como Trico,
quiero que el monorepo tenga la estructura de carpetas definida en la arquitectura (`projects/informe_coyuntura/` y `projects/votometro/` con todos sus subdirectorios),
para que cada proyecto sea autónomo y cualquier dev pueda orientarse en el repo sin ayuda.

**Acceptance Criteria:**

**Given** el repo clonado en la máquina de Trico
**When** se lista el árbol de directorios
**Then** existe `projects/informe_coyuntura/scripts/`, `projects/informe_coyuntura/output/cache/`, `projects/votometro/web/`, `projects/votometro/scripts/`, `projects/votometro/output/`
**And** cada directorio vacío tiene un `.gitkeep` para que git lo trackee
**And** existe un `requirements.txt` vacío en `projects/informe_coyuntura/`
**And** el `.gitignore` raíz excluye los outputs generados: `projects/*/output/*.json`, `projects/*/output/*.md`, `projects/*/output/cache/*.json`

### Story 1.2: Migrar archivos brownfield a sus paths definitivos

Como Trico,
quiero que los archivos existentes del Votómetro y del colector vida_cotidiana estén en sus paths definitivos dentro de `projects/`,
para que la migración al monorepo no rompa el trabajo existente.

**Acceptance Criteria:**

**Given** los archivos brownfield en sus ubicaciones actuales (`web/votometro.html`, `scripts/vida_cotidiana/`)
**When** se completa la migración
**Then** `projects/votometro/web/votometro.html` existe y es idéntico al original
**And** el contenido de `scripts/vida_cotidiana/` está disponible en `projects/informe_coyuntura/scripts/` para ser adaptado en Epic 2
**And** las rutas antiguas (`web/`, `scripts/vida_cotidiana/`) no existen más en el repo
**And** el commit documenta la migración sin cambios de lógica

### Story 1.3: Crear config.py para informe_coyuntura

Como Trico,
quiero un `config.py` en `projects/informe_coyuntura/` con todos los parámetros del modelo matusiano externalizados,
para poder ajustar pesos y umbrales sin tocar el código de procesamiento.

**Acceptance Criteria:**

**Given** `projects/informe_coyuntura/config.py`
**When** Trico lo abre
**Then** contiene `PESOS_CINTURONES` dict con pesos para macro, politica, vida_cotidiana, gestion (suman 1.0)
**And** contiene `UMBRALES` dict: `ESTABLE_MAX = 3`, `EN_TENSION_MAX = 6`
**And** contiene `BARBARISMO_MAP` dict: `"macro" → "tecnocrático"`, `"politica" → "político"`, `"gestion" → "gerencial"`, `"vida_cotidiana" → "político"`
**And** contiene sección `URLS_FUENTES` con constantes placeholder (`INDEC_IPC_URL = ""`, etc.) para completar en Epic 2
**And** cada parámetro tiene un comentario de una línea explicando su rol metodológico

### Story 1.4: Crear READMEs del monorepo y por proyecto

Como dev externo (o Trico en otra máquina),
quiero que cada proyecto tenga un README con instrucciones claras para correr sus scripts,
para poder ejecutar cualquier script sin preguntar a nadie.

**Acceptance Criteria:**

**Given** el README de `projects/informe_coyuntura/`
**When** un dev nuevo lo lee
**Then** contiene instrucciones para correr cada colector: `python scripts/macro.py`, `python scripts/politica.py`, etc.
**And** describe los outputs esperados y dónde encontrarlos (`output/cache/<cinturon>.json`)
**And** explica cómo interpretar los exit codes (0 = todos frescos, 1 = parcial desde cache, 2 = total desde cache)

**Given** el README de `projects/votometro/`
**When** Trico lo lee
**Then** describe cómo agregar una encuesta al HTML (qué campo del array actualizar)
**And** indica el path del HTML que consume el dev externo

**Given** el README raíz del monorepo
**When** alguien lo abre por primera vez
**Then** lista los proyectos activos con una línea de descripción cada uno
**And** indica que cada proyecto tiene su propio README con instrucciones de ejecución

---

## Epic 2: Informe de Coyuntura — Colección de Datos

Trico puede ejecutar el colector de cualquier cinturón de forma independiente y el sistema preserva el último dato válido cuando una fuente argentina falla, con flags claros sobre qué datos son frescos y cuáles son del cache.

### Story 2.1: Adaptar colector vida_cotidiana.py al patrón estándar

Como Trico,
quiero que el colector vida_cotidiana existente siga el patrón estándar de la arquitectura (URLs nombradas, config, cache, exit codes),
para que sea consistente con los otros colectores y el sistema de fallback funcione uniformemente.

**Acceptance Criteria:**

**Given** el script de vida_cotidiana migrado en Epic 1.2
**When** se ejecuta `python scripts/vida_cotidiana.py`
**Then** el script sigue la estructura estándar: constantes URL → import config → fetch por indicador → calcular_score → load/save_cache → main()
**And** ante fallo de una fuente, imprime `[WARN] vida_cotidiana.<indicador>: <error>. Usando cache.` y continúa
**And** escribe `output/cache/vida_cotidiana.json` si al menos un indicador es fresco
**And** retorna exit code 0 (todos frescos), 1 (parcial cache) o 2 (total desde cache)
**And** completa en menos de 5 minutos en red normal

### Story 2.2: Implementar colector macro.py

Como Trico,
quiero un colector `macro.py` que recolecte los indicadores del cinturón macroeconómico desde fuentes oficiales,
para tener datos frescos de inflación, reservas y actividad económica con fallback automático.

**Acceptance Criteria:**

**Given** `projects/informe_coyuntura/scripts/macro.py`
**When** se ejecuta `python scripts/macro.py`
**Then** intenta recolectar al menos 3 indicadores macro (inflación mensual INDEC, reservas BCRA, y uno adicional a definir durante implementación)
**And** las URLs de fuentes están definidas como constantes nombradas al inicio del script
**And** ante fallo de una fuente, usa el valor cacheado para ese indicador específico y continúa con los demás
**And** escribe `output/cache/macro.json` con el schema: `{indicador: {valor, unidad, fuente, fecha_dato, desactualizado}}`
**And** el score del cinturón se calcula usando `PESOS_CINTURONES` de `config.py`, nunca hardcodeado
**And** retorna exit codes 0/1/2 según proporción de datos frescos vs cache

### Story 2.3: Implementar colector politica.py

Como Trico,
quiero un colector `politica.py` que recolecte indicadores del cinturón político,
para tener datos frescos sobre actividad legislativa, aprobación y conflictividad con fallback automático.

**Acceptance Criteria:**

**Given** `projects/informe_coyuntura/scripts/politica.py`
**When** se ejecuta `python scripts/politica.py`
**Then** intenta recolectar al menos 2 indicadores políticos (aprobación presidencial y actividad legislativa/Congreso — fuentes exactas a definir durante implementación)
**And** las URLs están como constantes nombradas al inicio del script
**And** ante fallo parcial, imprime `[WARN] politica.<indicador>: <error>. Usando cache.` y continúa
**And** escribe `output/cache/politica.json` con mismo schema que macro.json
**And** el score usa `PESOS_CINTURONES["politica"]` de config.py
**And** retorna exit codes 0/1/2

### Story 2.4: Implementar colector gestion.py

Como Trico,
quiero un colector `gestion.py` que recolecte indicadores del cinturón de gestión/CIGOB,
para completar los 4 cinturones del análisis matusiano con fallback automático.

**Acceptance Criteria:**

**Given** `projects/informe_coyuntura/scripts/gestion.py`
**When** se ejecuta `python scripts/gestion.py`
**Then** intenta recolectar al menos 2 indicadores de gestión (fuentes exactas a definir durante implementación — SEPA, ejecución presupuestaria, o similares)
**And** las URLs están como constantes nombradas al inicio del script
**And** ante fallo parcial, imprime `[WARN] gestion.<indicador>: <error>. Usando cache.` y continúa
**And** escribe `output/cache/gestion.json` con mismo schema que los otros cinturones
**And** el score usa `PESOS_CINTURONES["gestion"]` de config.py
**And** retorna exit codes 0/1/2
**And** si no se pueden definir fuentes confiables, retorna exit code 2 con datos mínimos plausibles para que el generador funcione

---

## Epic 3: Informe de Coyuntura — Generación del Informe

Trico ejecuta un script único que lee los caches, calcula scores matusianos y detecta barbarismos activos, y genera el informe completo en JSON (para el dev externo) y Markdown (para Drive y reunión).

### Story 3.1: Implementar lógica de scoring y detección de barbarismos en generar_informe.py

Como Trico,
quiero un script `generar_informe.py` que lea los 4 caches de cinturón, calcule scores matusianos y detecte el barbarismo activo,
para que el análisis situacional sea completamente computacional y reproducible.

**Acceptance Criteria:**

**Given** los 4 archivos de cache (`output/cache/macro.json`, `politica.json`, `vida_cotidiana.json`, `gestion.json`)
**When** se ejecuta `python scripts/generar_informe.py`
**Then** carga cada cache y calcula el score 0-10 de cada cinturón como promedio ponderado de sus indicadores (pesos desde `config.py`)
**And** clasifica cada cinturón: score ≤ 3 → `"estable"`, 4-6 → `"en_tension"`, > 6 → `"tensionado"`
**And** detecta el barbarismo activo: cinturón con score más alto que supera umbral de tensión → `BARBARISMO_MAP[cinturon]`
**And** si 2 o más cinturones tienen score > 6, setea `alerta_multicinturon: true`
**And** si algún cache no existe, usa valores mínimos y agrega a `flags: ["cache_faltante: <cinturon>"]`
**And** produce un dict interno con la estructura completa del schema v1.0.0 lista para serializar

### Story 3.2: Implementar serialización de outputs (informe.json + informe.md)

Como dev externo del Informe y como Trico,
quiero que `generar_informe.py` escriba el informe en JSON estructurado y en Markdown con frontmatter,
para que el dev consuma el JSON sin conocer la metodología y Trico tenga el informe listo para subir a Drive.

**Acceptance Criteria:**

**Given** el dict interno generado en Story 3.1
**When** `generar_informe.py` completa su ejecución (menos de 1 minuto desde que los caches están disponibles)
**Then** escribe `output/informe.json` con el schema v1.0.0 exacto: claves `schema_version`, `generated_at` (ISO 8601), `period` (YYYY-MM), `cinturones`, `barbarismo_activo`, `alerta_multicinturon`, `flags`
**And** los scores en `informe.json` son floats con 1 decimal (ej: `6.8`, no `7`, no `6.82`)
**And** los strings de estado son exactamente `"estable"`, `"en_tension"` o `"tensionado"` (sin variantes)
**And** los strings de barbarismo son exactamente `"político"`, `"tecnocrático"`, `"gerencial"` o `null`
**And** escribe `output/informe.md` con frontmatter YAML que incluye `period`, `generated_at`, `barbarismo_activo`, `alerta_multicinturon`
**And** el cuerpo del Markdown incluye una sección por cinturón con su score, estado, y tabla de indicadores marcando los desactualizados con `⚠️`
**And** los campos opcionales ausentes en `informe.json` aparecen como `null`, nunca se omiten (NFR3)

---

## Epic 4: Votómetro — Migración y Estabilización

El Votómetro vive en su path definitivo dentro del monorepo, el workflow de actualización de encuestas está documentado, y el dev puede consumir el HTML actualizado sin fricción ni acceso al código de análisis.

### Story 4.1: Verificar y estabilizar el Votómetro en su path definitivo

Como Trico y como dev externo del Votómetro,
quiero confirmar que el Votómetro funciona correctamente desde su nuevo path en el monorepo,
para que la migración brownfield no haya roto nada y el dev pueda consumir el HTML con confianza.

**Acceptance Criteria:**

**Given** `projects/votometro/web/votometro.html` (migrado en Story 1.2)
**When** se abre el HTML en un browser
**Then** el modelo carga sin errores de consola
**And** las 99 encuestas existentes se muestran correctamente y el Votómetro calcula los resultados
**And** el prior de fundamentals está activo y correctamente ponderado
**And** las simulaciones Monte Carlo corren y producen intervalos de confianza visibles
**And** no hay rutas relativas rotas por el cambio de path
**And** se registra en el README de votometro el resultado de esta verificación (fecha, resultado, qué se chequeó)

### Story 4.2: Documentar workflow de actualización de encuestas y contrato con el dev

Como Trico,
quiero documentación clara del proceso para agregar encuestas y del contrato con el dev externo del Votómetro,
para que el workflow de actualización sea repetible y el dev pueda consumir el HTML sin necesitar acceso al código de análisis.

**Acceptance Criteria:**

**Given** el README de `projects/votometro/`
**When** Trico necesita agregar una encuesta nueva
**Then** el README describe exactamente qué objeto agregar al array de encuestas en el HTML: campos requeridos (`fecha`, `empresa`, `candidato`, `valor`, `muestra`), campos opcionales, y ejemplo concreto
**And** describe cómo funciona la ponderación quíntuple en términos no técnicos — suficiente para que Trico entienda el efecto de cada campo
**And** indica el path exacto que el dev externo consume: `projects/votometro/web/votometro.html`
**And** documenta que el HTML es el único artefacto de output — no hay JSON de encuestas separado por ahora (deferred)
**And** incluye una nota sobre la verificación CN 97-98: qué umbral verifica y dónde se puede leer el resultado en la UI
