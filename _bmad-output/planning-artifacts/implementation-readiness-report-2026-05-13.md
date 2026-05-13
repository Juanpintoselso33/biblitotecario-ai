---
stepsCompleted: [step-01-document-discovery, step-02-prd-analysis, step-03-epic-coverage, step-04-ux-alignment, step-05-epic-quality-review]
inputDocuments:
  - _bmad-output/planning-artifacts/prd.md
  - _bmad-output/planning-artifacts/architecture.md
  - _bmad-output/planning-artifacts/epics.md
---

# Implementation Readiness Assessment Report

**Date:** 2026-05-13
**Project:** CIGOB Análisis

## Document Inventory

| Tipo | Archivo | Estado |
|---|---|---|
| PRD | `_bmad-output/planning-artifacts/prd.md` | ✅ Encontrado (documento completo) |
| Architecture | `_bmad-output/planning-artifacts/architecture.md` | ✅ Encontrado (documento completo) |
| Epics & Stories | `_bmad-output/planning-artifacts/epics.md` | ✅ Encontrado (documento completo) |
| UX Design | N/A | ✅ No aplica — sin frontend propio |

**Duplicados:** Ninguno
**Documentos faltantes:** Ninguno

## PRD Analysis

### Functional Requirements

FR1: Trico ejecuta el colector de cada cinturón de forma independiente sin correr los otros
FR2: El colector macro recolecta indicadores desde fuentes oficiales (INDEC, BCRA, Ministerio de Economía)
FR3: El colector político recolecta indicadores desde fuentes oficiales (Congreso, encuestadoras, medios)
FR4: El colector vida cotidiana recolecta indicadores desde fuentes definidas (implementado)
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
**Total FRs: 27**

### Non-Functional Requirements

NFR1: Scripts de colección de un cinturón completan en menos de 5 minutos en condiciones normales de red
NFR2: Generador del Informe de Coyuntura completa en menos de 1 minuto una vez disponibles los datos
NFR3: El schema JSON de output del Informe no modifica campos existentes entre versiones sin deprecation notice en el README del proyecto
NFR4: Los outputs del Votómetro (HTML o JSON) mantienen su estructura entre actualizaciones de encuestas
NFR5: Los scripts producen outputs en `projects/<nombre>/output/` sin configuración adicional
NFR6: Las URLs de fuentes de datos están en variables nombradas al inicio de cada script, no dispersas en el código
NFR7: Un desarrollador nuevo corre cualquier script leyendo solo el README del proyecto
NFR8: Los parámetros del modelo (pesos, umbrales de cinturón, factores de barbarismo) están separados del código de procesamiento
**Total NFRs: 8**

### Additional Requirements

- Sin multi-tenancy, sin real-time, sin cloud, sin auth — herramienta local de un solo operador
- Python 3.x, scripts planos, `python <script>.py` sin setup previo
- Entorno Windows (máquina de Trico)
- Fuentes argentinas públicas (INDEC, BCRA, Congreso, SEPA) — endpoints inestables, sin SLA
- Brownfield: vida_cotidiana existente + Votómetro HTML operativo deben ser migrados sin romper funcionalidad

### PRD Completeness Assessment

PRD completo: 12 pasos finalizados, 6 categorías de FRs bien delimitadas, NFRs de performance y mantenibilidad definidos, dominio y restricciones técnicas claras. La única brecha documentada es la definición de indicadores específicos por cinturón (qué series exactas de INDEC/BCRA) — diferida intencionalmente para resolverse story by story.

## Epic Coverage Validation

### Coverage Matrix

| FR | Requerimiento (resumen) | Epic / Story | Estado |
|---|---|---|---|
| FR1 | Ejecución independiente por cinturón | Epic 2, Stories 2.1-2.4 | ✅ Cubierto |
| FR2 | Colector macro (INDEC, BCRA, Economía) | Epic 2, Story 2.2 | ✅ Cubierto |
| FR3 | Colector político (Congreso, encuestadoras) | Epic 2, Story 2.3 | ✅ Cubierto |
| FR4 | Colector vida cotidiana (existente) | Epic 2, Story 2.1 | ✅ Cubierto |
| FR5 | Colector gestión/CIGOB | Epic 2, Story 2.4 | ✅ Cubierto |
| FR6 | Preservar último valor válido ante fallo | Epic 2, Stories 2.1-2.4 | ✅ Cubierto |
| FR7 | Flag explícito de indicadores desactualizados | Epic 2, Stories 2.1-2.4 | ✅ Cubierto |
| FR8 | Generar Informe con un único script | Epic 3, Stories 3.1+3.2 | ✅ Cubierto |
| FR9 | Output Markdown para Drive y reunión | Epic 3, Story 3.2 | ✅ Cubierto |
| FR10 | Output JSON con schema estructurado | Epic 3, Story 3.2 | ✅ Cubierto |
| FR11 | Score y estado por cinturón en el período | Epic 3, Story 3.1 | ✅ Cubierto |
| FR12 | Flag indicadores desactualizados + fecha | Epic 3, Story 3.2 | ✅ Cubierto |
| FR13 | Calcular score 0-10 por cinturón | Epic 3, Story 3.1 | ✅ Cubierto |
| FR14 | Detectar barbarismo activo | Epic 3, Story 3.1 | ✅ Cubierto |
| FR15 | Alerta multicinturón (regla matusiana) | Epic 3, Story 3.1 | ✅ Cubierto |
| FR16 | Modificar parámetros sin afectar lógica | Epic 1, Story 1.3 | ✅ Cubierto |
| FR17 | Agregar proyecto sin tocar otros | Epic 1, Story 1.1 | ✅ Cubierto |
| FR18 | README por proyecto con instrucciones | Epic 1, Story 1.4 | ✅ Cubierto |
| FR19 | Cambios metodológicos documentados en commits | Epic 1, Story 1.2 AC + práctica transversal | ✅ Cubierto |
| FR20 | Dev Informe consume JSON sin conocer metodología | Epic 3, Story 3.2 | ✅ Cubierto |
| FR21 | Schema JSON sin breaking changes sin aviso | Epic 3, Story 3.2 | ✅ Cubierto |
| FR22 | Dev Votómetro consume HTML sin código análisis | Epic 4, Story 4.2 | ✅ Cubierto |
| FR23 | Trico agrega encuestas al Votómetro | Epic 4, Story 4.2 | ✅ Cubierto |
| FR24 | Ponderación quíntuple (existente) | Epic 4, Story 4.1 | ✅ Cubierto |
| FR25 | Monte Carlo (existente) | Epic 4, Story 4.1 | ✅ Cubierto |
| FR26 | Verificación CN 97-98 (existente) | Epic 4, Story 4.1 | ✅ Cubierto |
| FR27 | Prior de fundamentals con peso decreciente (existente) | Epic 4, Story 4.1 | ✅ Cubierto |

### Missing Requirements

Ninguno.

### Coverage Statistics

- Total PRD FRs: 27
- FRs cubiertos en epics: 27
- **Cobertura: 100%**

## UX Alignment Assessment

### UX Document Status

No encontrado — **no aplica por diseño**. CIGOB Análisis es un data pipeline local sin UI propia. Los outputs (JSON + Markdown) son consumidos por devs externos que construyen sus propios frontends. No hay componentes de UI en el alcance de este proyecto.

### Alignment Issues

Ninguno.

### Warnings

Ninguno. La ausencia de UX es correcta y documentada en PRD y Architecture.

## Epic Quality Review

### User Value Focus Check

| Epic | Título | ¿Entrega valor de usuario? | Evaluación |
|---|---|---|---|
| Epic 1 | Monorepo Foundation & Configuración | Sí — Trico puede clonar y orientarse; devs pueden ejecutar scripts sin ayuda | ✅ Aceptable en contexto brownfield |
| Epic 2 | Informe de Coyuntura — Colección de Datos | Sí — Trico ejecuta colectores independientemente con fallback automático | ✅ Valor de usuario claro |
| Epic 3 | Informe de Coyuntura — Generación del Informe | Sí — Trico genera el informe completo con un script | ✅ Valor de usuario claro |
| Epic 4 | Votómetro — Migración y Estabilización | Sí — dev externo consume HTML sin fricciones; workflow de actualización documentado | ✅ Aceptable en contexto brownfield |

### Epic Independence Validation

| Test | Resultado |
|---|---|
| Epic 1 funciona standalone | ✅ Sin dependencias externas |
| Epic 2 funciona usando solo output de Epic 1 (config.py, directorios, vida_cotidiana migrado) | ✅ Dependencias hacia atrás correctas |
| Epic 3 funciona usando output de Epics 1 y 2 (config.py + caches de cinturón) | ✅ Dependencias hacia atrás correctas |
| Epic 4 funciona usando solo output de Epic 1 (votometro.html migrado en Story 1.2) | ✅ Sin dependencias en Epics 2 o 3 |
| Ningún epic requiere output de un epic posterior | ✅ Sin forward dependencies entre epics |

### Story Dependency Analysis

**Epic 1 — Order:** 1.1 → 1.2 → 1.3 → 1.4 (cada una usa output de las anteriores, sin saltos)
**Epic 2 — Order:** 2.1 puede hacerse en paralelo con 2.2/2.3/2.4 (colectores independientes)
**Epic 3 — Order:** 3.1 → 3.2 (3.2 depende del dict interno de 3.1 — apropiado)
**Epic 4 — Order:** 4.1 → 4.2 (4.2 verifica el resultado de 4.1)

Sin forward dependencies detectadas dentro de los epics.

### Acceptance Criteria Review

| Story | G/W/T Format | Testable | Complete | Hallazgo |
|---|---|---|---|---|
| 1.1 | ✅ | ✅ | ✅ | Sin issues |
| 1.2 | ✅ | ✅ | ✅ | Sin issues |
| 1.3 | ✅ | ✅ | ⚠️ | Ver Major Issue #1 |
| 1.4 | ✅ | ✅ | ⚠️ | Ver Major Issue #2 |
| 2.1 | ✅ | ✅ | ✅ | Sin issues |
| 2.2 | ✅ | ⚠️ | ⚠️ | Ver Minor Concern #1 |
| 2.3 | ✅ | ⚠️ | ⚠️ | Ver Minor Concern #1 |
| 2.4 | ✅ | ⚠️ | ⚠️ | Ver Minor Concerns #1 y #3 |
| 3.1 | ✅ | ✅ | ✅ | Sin issues |
| 3.2 | ✅ | ✅ | ✅ | Sin issues — muy específica |
| 4.1 | ✅ | ✅ | ✅ | Sin issues |
| 4.2 | ✅ | ✅ | ✅ | Sin issues |

### Quality Violations

#### 🔴 Critical Violations

Ninguno.

#### 🟠 Major Issues

**Major Issue #1 — Story 1.3: URLS_FUENTES en config.py contradice NFR6**

Story 1.3 define una sección `URLS_FUENTES` en `config.py` con constantes placeholder. Sin embargo, NFR6 establece explícitamente: "Las URLs de fuentes de datos están en variables nombradas **al inicio de cada script**, no dispersas en el código." La arquitectura refuerza esto. Tener URLs en `config.py` Y en cada script genera duplicación y contradice el requisito de mantenibilidad.

**Remediation:** Eliminar `URLS_FUENTES` de Story 1.3 / `config.py`. Las URLs van al inicio de cada script colector (Stories 2.2–2.4). `config.py` queda exclusivamente con `PESOS_CINTURONES`, `UMBRALES` y `BARBARISMO_MAP`.

**Major Issue #2 — Story 1.4: README referencia scripts inexistentes (forward reference)**

El AC de Story 1.4 para el README de `informe_coyuntura` incluye instrucciones como `python scripts/macro.py`, `python scripts/politica.py` — scripts que no existen hasta Epic 2. Story 1.4 debe completarse en Epic 1 sin depender del output de Epics futuras.

**Remediation:** Story 1.4 crea el README con la estructura y secciones definidas, pero con comentarios `# [A completar en Epic 2 — Story 2.2]` para las instrucciones de scripts no implementados aún. El README se considera completo cuando la sección de instrucciones está presente, aunque las rutas de scripts sean stubs.

#### 🟡 Minor Concerns

**Minor Concern #1 — Stories 2.2, 2.3, 2.4: Indicadores "a definir durante implementación"**

Los ACs de tres colectores dejan las fuentes específicas abiertas con la frase "fuentes exactas a definir durante implementación". Esto reduce la testabilidad: no se puede verificar antes de comenzar si el indicador recolectado cumple el requisito.

**Remediation:** Aceptable dado que las fuentes argentinas son inestables y la arquitectura lo prevé. Sin embargo, cada story debe documentar la fuente elegida en el commit que la implementa (FR19). No requiere cambio en epics.md.

**Minor Concern #2 — Story 1.4: Tres entregables en una story**

Story 1.4 produce tres READMEs distintos (informe_coyuntura, votometro, root). Borderline en tamaño. No bloquea implementación — los tres READMEs son documentación relacionada y la story es completable de forma independiente.

**Remediation:** No requiere split. Aceptable.

**Minor Concern #3 — Story 2.4: Escape hatch explícito**

El último AC de Story 2.4 permite que el colector retorne exit code 2 con "datos mínimos plausibles" si no se pueden definir fuentes. Esto podría resultar en un stub que nunca implementa colección real.

**Remediation:** El AC es correcto por diseño (gestion.py no debe bloquear Epic 3). Sin embargo, la story debe incluir en su commit la justificación de por qué se usó el fallback (FR19). No requiere cambio en epics.md.

### Best Practices Compliance Checklist

| Criterio | Epic 1 | Epic 2 | Epic 3 | Epic 4 |
|---|---|---|---|---|
| Entrega valor de usuario | ✅ | ✅ | ✅ | ✅ |
| Funciona de forma independiente | ✅ | ✅ | ✅ | ✅ |
| Stories apropiadamente dimensionadas | ✅ | ✅ | ✅ | ✅ |
| Sin forward dependencies entre stories | ✅ | ✅ | ✅ | ✅ |
| Acceptance criteria en Given/When/Then | ✅ | ✅ | ✅ | ✅ |
| Trazabilidad a FRs mantenida | ✅ | ✅ | ✅ | ✅ |
| Contexto brownfield contemplado | ✅ | ✅ | N/A | ✅ |

### Epic Quality Summary

**Epics aprobados:** 4/4
**Stories aprobadas:** 12/12
**Critical violations:** 0
**Major issues:** 2 (remediation clara, no bloquean implementación)
**Minor concerns:** 3 (aceptables, sin cambios requeridos en epics.md)

**Acción requerida antes de implementar Story 1.3:** eliminar `URLS_FUENTES` del scope de config.py.
**Acción requerida antes de implementar Story 1.4:** README de informe_coyuntura se genera con stubs para scripts no implementados.

## Summary and Recommendations

### Overall Readiness Status

**✅ READY** — con dos correcciones menores a aplicar durante implementación de Epic 1.

### Critical Issues Requiring Immediate Action

**Ninguno.** No hay violaciones críticas que bloqueen el inicio de la implementación.

### Recommended Next Steps

1. **Corregir scope de Story 1.3** — Eliminar la sección `URLS_FUENTES` de `config.py`. Las URLs van al inicio de cada script colector (Story 2.2, 2.3, 2.4), no en config.py. Esto alinea con NFR6 y evita duplicación.

2. **Corregir Story 1.4** — Al crear el README de `informe_coyuntura`, incluir stubs con comentarios `# [Completar en Epic 2]` para las secciones de instrucciones de scripts que aún no existen. El README es completable sin Epic 2.

3. **Proceder al Sprint Planning** — Ejecutar `bmad-sprint-planning` para planificar el primer sprint de implementación. La secuencia recomendada es: Epic 1 completo → Epic 2 en paralelo → Epic 3 → Epic 4 (puede hacerse en paralelo con Epics 2-3 dado que es independiente).

### Final Note

Este assessment identificó **5 issues en total** (0 críticos, 2 mayores, 3 menores) en **3 categorías** (scope de config.py, forward references en README, indicadores abiertos en colectores). Los dos issues mayores tienen remediación inmediata y específica. Los documentos de planificación — PRD, Architecture y Epics — están completos con cobertura del 100% de los 27 FRs. El proyecto está listo para iniciar implementación.

**Assessor:** Claude Sonnet 4.6 / BMAD Check Implementation Readiness
**Fecha:** 2026-05-13

