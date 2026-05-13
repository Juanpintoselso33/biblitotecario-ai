---
stepsCompleted: [step-01-init, step-02-discovery, step-02b-vision, step-02c-executive-summary, step-03-success, step-04-journeys, step-05-domain, step-06-innovation-skipped, step-07-project-type, step-08-scoping, step-09-functional, step-10-nonfunctional, step-11-polish]
releaseMode: single-release-iterative
classification:
  projectType: monorepo-analytics-platform
  domain: govtech
  complexity: medium-high
  projectContext: brownfield
  projects:
    - informe-de-coyuntura
    - votometro
    - future-tbd
inputDocuments:
  - output/analisis_realidad_politica/_brief_matus.md
  - output/analisis_realidad_politica/00_resumen_ejecutivo.md
  - output/analisis_realidad_politica/01_marco_metodologico_matusiano.md
  - output/analisis_realidad_politica/02_pestana_macroeconomia.md
  - output/analisis_realidad_politica/03_pestana_politica.md
  - output/analisis_realidad_politica/04_pestana_vida_cotidiana.md
  - output/analisis_realidad_politica/05_pestana_gestion_cinturon_cigob.md
  - output/analisis_realidad_politica/05_monitor_vida_cotidiana_fuentes.md
briefCount: 1
researchCount: 0
brainstormingCount: 0
projectDocsCount: 7
workflowType: 'prd'
---

# Product Requirements Document - CIGOB Análisis

**Autor:** Trico
**Fecha:** 2026-05-13

## Resumen Ejecutivo

La plataforma analítica CIGOB es un monorepo de análisis político-gubernamental argentino que produce insumos estructurados — datos, metodología y reportes periódicos — para reuniones institucionales internas y para los desarrolladores externos que construyen los frontends de cada producto. CIGOB no construye interfaces: construye el conocimiento computacional que las hace posibles.

El problema que resuelve no es técnico sino metodológico: el análisis político argentino disponible es periodismo de opinión o dashboards de KPIs genéricos. Ninguno aplica el marco de Carlos Matus (PES, tres cinturones, juego macroorganizativo) de forma computacional y continua. El resultado es que los equipos de análisis institucional llegan a las reuniones sin una lectura sistemática del riesgo distribuido entre cinturones.

El repositorio contiene dos proyectos activos con sus propios desarrolladores frontend:
- **Informe de Coyuntura** — colectores de datos para los 4 cinturones (macro, político, vida cotidiana, gestión CIGOB) + generador del informe periódico matusiano
- **Votómetro Argentina 2027** — modelo electoral con ponderación quíntuple de encuestas, prior de fundamentals y corrección bayesiana de voto oculto

La arquitectura es abierta para proyectos futuros bajo la misma infraestructura.

### Diferenciador

El diferenciador es el marco conceptual, no la tecnología. El Informe de Coyuntura detecta barbarismos (político, tecnocrático, gerencial) antes de que escalen, aplica la regla matusiana "nunca apretar los tres cinturones a la vez", y distingue diagnóstico estático de situación dinámica.

El Votómetro aplica calibración metodológica rigurosa (error histórico argentino PASO 2023: 8-13pp, Monte Carlo 10.000 simulaciones) donde otros modelos usan promedios simples.

La combinación de los dos productos — anticipación electoral + anticipación de gobierno — es única en el ecosistema analítico argentino.

**Ventana de máxima utilidad:** Las elecciones 2027 se acercan y el gobierno Milei genera presión simultánea en los 3 cinturones — el escenario donde el análisis matusiano diferencia más.

## Clasificación del Proyecto

| Dimensión | Valor |
|---|---|
| Tipo | Monorepo analítico — data pipeline + report generator + electoral model |
| Dominio | GovTech (análisis político-gubernamental argentino) |
| Complejidad | Media-alta |
| Contexto | Brownfield — Votómetro operativo, scripts vida_cotidiana funcionando, 7 documentos de análisis producidos |
| Proyectos activos | `informe-de-coyuntura`, `votometro` |

## Criterios de Éxito

### Usuario

La plataforma funciona cuando el equipo CIGOB llega a cada reunión con datos actualizados y un informe generado — sin trabajo manual de búsqueda. Criterio simple: ¿el output sirvió para la reunión?

### Negocio

- Informe de Coyuntura con cadencia mensual sostenible
- Cada proyecto entrega outputs consumibles por su dev externo
- El monorepo crece una funcionalidad por reunión, no por roadmap anticipado

### Técnico

- Scripts de colección corren sin intervención manual
- Outputs en formato consumible por el dev de cada proyecto
- Arquitectura permite agregar proyectos nuevos sin refactorizar lo existente

### Resultados Medibles

- Colectores funcionando para los 4 cinturones (hoy: vida_cotidiana ✓, falta macro, político, gestión)
- Al menos 1 informe de coyuntura generado automáticamente antes de la próxima reunión

## Alcance del Producto

**MVP:** Lo necesario para la próxima reunión. Backlog vivo en el Drive (log de reuniones).

**Crecimiento:** Definido reunión a reunión según prioridades emergentes.

**Visión:** Monorepo escalable que soporta proyectos analíticos adicionales sin fricción.

## User Journeys

### Journey 1 — Trico prepara la reunión mensual

Trico abre el repo a fin de mes. Corre los scripts de colección para los 4 cinturones. Los datos se actualizan en sus archivos fuente. Corre el generador de informe. Sale un `.md` (y opcionalmente `.docx`) con el estado de cada cinturón, los scores, y las alertas de barbarismo activas. Lo sube al Drive. El equipo lo lee antes de la reunión. En la reunión no se pierde tiempo buscando datos — se discute la situación.

**Requiere:** runner unificado opcional, formato de output estable, ruta de output predecible para Drive.

---

### Journey 2 — Un colector falla

El script del cinturón macro intenta scrappear INDEC y el endpoint cambió. El script falla con error claro. Trico lo parchea y re-corre solo ese colector. El informe se genera con el dato anterior más un flag `[DATO DESACTUALIZADO - fuente: INDEC]`.

**Requiere:** errores explícitos y recuperables, outputs parciales válidos con advertencias, informe no bloqueado por un dato faltante.

---

### Journey 3 — Dev del Informe consume el output

El dev recibe un archivo estructurado (JSON o markdown con frontmatter) con los valores de cada indicador, su score, la alerta de cinturón, y la fecha de actualización. Con eso construye el frontend sin necesidad de entender la metodología.

**Requiere:** contrato de output estable (schema versionado), separación clara entre datos crudos y análisis, documentación mínima del formato.

---

### Journey 4 — Dev del Votómetro sincroniza encuestas

Trico agrega una encuesta nueva al Votómetro. El dev del Votómetro no toca el modelo — solo consume el HTML actualizado o un JSON con las encuestas. Los dos trabajan en paralelo sin pisarse.

**Requiere:** separación de responsabilidades CIGOB (modelo + datos) ↔ dev (UI), posible extracción del array de encuestas a JSON independiente.

---

### Resumen de Capacidades por Journey

| Capacidad | Journeys |
|---|---|
| Runner unificado de colectores | J1, J2 |
| Outputs con schema estable | J1, J3 |
| Manejo de errores con fallback parcial | J2 |
| Separación datos/análisis | J3 |
| Independencia CIGOB ↔ devs | J3, J4 |

## Requerimientos de Dominio

### Fuentes de datos públicas argentinas

Los colectores dependen de INDEC, BCRA, Congreso, SEPA y otras fuentes oficiales que cambian endpoints sin aviso, tienen downtime frecuente, y publican datos con semanas de demora.

- Scripts manejan errores de fuente con fallback al último dato válido + flag de antigüedad
- URLs de fuentes centralizadas al inicio de cada script para parcheo rápido
- Sin SLA de disponibilidad — el sistema corre cuando la fuente está disponible

### Integridad metodológica (Matus)

El output no es solo datos — es una lectura situacional bajo el marco PES. Cambios en indicadores, pesos o fórmulas de score deben ser documentados para que el informe sea reproducible y auditable.

- Parámetros del modelo (pesos, umbrales, fórmulas de barbarismo) en archivos de configuración, no hardcodeados
- Cambios metodológicos = commit documentado con justificación

### Sin compliance regulatorio

Todo el dato es público. No hay PII en el sistema. No aplica GDPR, HIPAA, ni normativa argentina de protección de datos. Herramienta local/repo sin requisitos de uptime.

## Arquitectura del Monorepo

### Estructura de directorios

```
projects/
  informe_coyuntura/
    scripts/
      macro.py
      politica.py
      vida_cotidiana.py
      gestion.py
    output/
    README.md
  votometro/
    scripts/
      update_polls.py
    web/
      votometro.html
    output/
    README.md
  [futuro_proyecto]/
    ...
docs/           → documentos fuente CIGOB
output/         → outputs globales / Drive sync
```

### Principios de arquitectura

- **Proyectos completamente autónomos:** cada uno tiene sus scripts, outputs y README propios
- **Sin acoplamiento entre proyectos:** si dos proyectos necesitan algo en común, lo resuelven individualmente hasta que haya razón orgánica para extraerlo
- **Scripts independientes:** cada colector corre por separado — `python macro.py`, `python politica.py`, etc.
- **Outputs duales:** JSON (para dev) + markdown con frontmatter (para informe/Drive) — schema definido por proyecto cuando el dev lo necesite
- **Python, dependencias mínimas:** `python <script>.py` sin setup previo; outputs en `projects/<nombre>/output/`

## Estrategia y Alcance

**Approach:** Iterativo por reunión — cada ciclo agrega una capacidad que sirve para la siguiente. Sin roadmap anticipado. Backlog vivo en Drive.

**Recursos:** Trico como operador principal. Dos devs externos (uno por proyecto) que consumen outputs.

### Must-Have

- Restructura del repo en `projects/informe_coyuntura/` y `projects/votometro/`
- Colectores de datos para macro, político y gestión (vida_cotidiana ya existe)
- Generador del informe de coyuntura (markdown + JSON)
- Manejo de errores con fallback parcial y flag de dato desactualizado

### Nice-to-Have

- Runner unificado (`python run_all.py`)
- Config centralizado de parámetros del modelo
- Schema versionado para el JSON de output
- Extracción del array de encuestas del Votómetro a JSON independiente

### Mitigación de riesgos

| Riesgo | Mitigación |
|---|---|
| Fuentes argentinas cambian sin aviso | URLs centralizadas, errores claros, fallback al último dato válido |
| Solo Trico corre el sistema | Scripts simples, `python <script>.py` sin setup, README por proyecto |
| Cambios en parámetros Matus | Documentar en commits con justificación |

## Requerimientos Funcionales

### Recolección de Datos

- **FR1:** Trico ejecuta el colector de cada cinturón de forma independiente sin correr los otros
- **FR2:** El colector macro recolecta indicadores desde fuentes oficiales (INDEC, BCRA, Ministerio de Economía)
- **FR3:** El colector político recolecta indicadores desde fuentes oficiales (Congreso, encuestadoras, medios)
- **FR4:** El colector vida cotidiana recolecta indicadores desde fuentes definidas (implementado)
- **FR5:** El colector gestión/CIGOB recolecta indicadores desde fuentes a definir
- **FR6:** El sistema preserva el último valor válido de cada indicador cuando una fuente falla
- **FR7:** El sistema marca con flag explícito los indicadores que usan datos de un período anterior

### Generación del Informe de Coyuntura

- **FR8:** Trico genera el Informe ejecutando un único script
- **FR9:** El sistema produce el Informe en formato markdown listo para Drive y reunión
- **FR10:** El sistema produce el Informe en formato JSON con schema estructurado para consumo del dev
- **FR11:** El Informe incluye el estado y score de cada cinturón para el período actual
- **FR12:** El Informe incluye el flag de indicadores desactualizados con la fecha del último dato válido

### Análisis Matusiano

- **FR13:** El sistema calcula el score de cada cinturón según los indicadores recolectados
- **FR14:** El sistema detecta el barbarismo de riesgo activo (político, tecnocrático, gerencial) según el estado de los cinturones
- **FR15:** El sistema genera alerta cuando más de un cinturón está tensionado (regla matusiana)
- **FR16:** Trico modifica parámetros del modelo (pesos, umbrales) en el código fuente sin afectar la lógica de colección

### Gestión del Monorepo

- **FR17:** Trico agrega un nuevo proyecto al monorepo dentro de `projects/` sin tocar los proyectos existentes
- **FR18:** Cada proyecto tiene README con instrucciones para correr sus scripts
- **FR19:** Los cambios en parámetros metodológicos quedan registrados en el historial de commits con justificación

### Integración con Devs Externos

- **FR20:** El dev del Informe consume el JSON de output sin conocer la metodología interna
- **FR21:** El schema JSON del Informe no introduce breaking changes entre versiones sin aviso explícito en el README del proyecto
- **FR22:** El dev del Votómetro consume el HTML o los datos del Votómetro sin acceso al código de análisis

### Votómetro

- **FR23:** Trico agrega nuevas encuestas al Votómetro actualizando el archivo de datos correspondiente
- **FR24:** El Votómetro aplica ponderación quíntuple a las encuestas (decaimiento temporal, calidad, sesgo histórico, orientación del medio, metodología)
- **FR25:** El Votómetro corre simulaciones Monte Carlo y produce estimaciones con intervalos de confianza
- **FR26:** El Votómetro verifica el umbral de los artículos 97-98 CN en cada simulación
- **FR27:** El Votómetro integra el prior de fundamentals con peso decreciente a medida que se acerca la elección

## Requerimientos No Funcionales

### Performance

- Scripts de colección de un cinturón completan en menos de 5 minutos en condiciones normales de red
- Generador del Informe de Coyuntura completa en menos de 1 minuto una vez disponibles los datos

### Integración

- El schema JSON de output del Informe no modifica campos existentes entre versiones sin deprecation notice en el README del proyecto
- Los outputs del Votómetro (HTML o JSON) mantienen su estructura entre actualizaciones de encuestas
- Los scripts producen outputs en `projects/<nombre>/output/` sin configuración adicional

### Mantenibilidad

- Las URLs de fuentes de datos están en variables nombradas al inicio de cada script, no dispersas en el código
- Un desarrollador nuevo corre cualquier script leyendo solo el README del proyecto
- Los parámetros del modelo (pesos, umbrales de cinturón, factores de barbarismo) están separados del código de procesamiento
