---
stepsCompleted: [step-01-init, step-02-context, step-03-starter, step-04-decisions, step-05-patterns, step-06-structure, step-07-validation, step-08-complete]
inputDocuments:
  - _bmad-output/planning-artifacts/prd.md
  - output/analisis_realidad_politica/_brief_matus.md
workflowType: 'architecture'
lastStep: 8
status: 'complete'
completedAt: '2026-05-13'
project_name: 'CIGOB Análisis'
user_name: 'Trico'
date: '2026-05-13'
---

# Architecture Decision Document

_Este documento se construye colaborativamente paso a paso. Las secciones se agregan a medida que avanzamos en cada decisión arquitectónica._

## Análisis de Contexto del Proyecto

### Resumen de Requerimientos

**Requerimientos Funcionales:**
27 FRs en 6 categorías: recolección de datos (FR1-7), generación del informe (FR8-12), análisis matusiano (FR13-16), gestión del monorepo (FR17-19), integración con devs externos (FR20-22), y Votómetro (FR23-27). Sin UI propia — CIGOB produce outputs que consumen devs externos.

**Requerimientos No Funcionales:**
- Performance: colector <5min por cinturón, generador de informe <1min
- Integración: schema JSON estable sin breaking changes no avisados, outputs en paths predecibles (`projects/<nombre>/output/`)
- Mantenibilidad: URLs de fuentes en variables nombradas, parámetros del modelo separados del código de procesamiento, README-driven usage

**Escala y Complejidad:**
- Dominio primario: data pipeline local + report generator (Python)
- Complejidad: baja-media (sin multi-tenancy, sin real-time, sin cloud, sin auth)
- Componentes arquitectónicos estimados: 4 colectores + 1 generador de informe + Votómetro + infraestructura de fallback + monorepo shell

### Restricciones Técnicas y Dependencias

- Python con dependencias mínimas; `python <script>.py` sin setup previo
- Entorno Windows (máquina de Trico)
- Fuentes de datos públicas argentinas (INDEC, BCRA, Congreso, SEPA) — endpoints inestables, downtime frecuente, publicaciones con demora
- Brownfield: colector vida_cotidiana existente + Votómetro HTML operativo
- Sin internet en runtime excepto durante la colección de datos

### Concerns Transversales Identificados

- **Error handling + fallback**: todo colector debe degradar graciosamente y preservar el último dato válido con timestamp
- **Schema de output estable**: contrato entre CIGOB y los devs externos — ningún cambio breaking sin deprecation notice
- **Externalización de parámetros**: pesos, umbrales y factores de barbarismo fuera del código de procesamiento para auditoría metodológica
- **Aislamiento de proyectos**: cada proyecto en `projects/` es autónomo — sin dependencias cruzadas hasta que haya razón orgánica

## Evaluación de Plantilla Base

### Dominio Tecnológico Primario

Python data pipeline local — sin framework web, sin servidor, sin UI propia. CIGOB produce outputs (JSON + Markdown) que consumen devs externos.

### Decisiones de Fundación

No existe starter template aplicable para este tipo de proyecto. Las decisiones de fundación son convenciones Python y estructura de monorepo:

**Lenguaje y Runtime:**
Python 3.x, scripts planos sin empaquetado formal. Ejecución: `python <script>.py`

**Gestión de Dependencias:**
`requirements.txt` por proyecto en `projects/<nombre>/`. Sin dependencias cruzadas entre proyectos.

**Persistencia de Estado (Fallback):**
JSON por cinturón en `projects/informe_coyuntura/output/cache/<cinturon>.json`. Cada ejecución exitosa sobreescribe el cache; los errores lo preservan y levantan el flag de dato desactualizado.

**Formato de Output:**
- JSON estructurado → para devs externos (`projects/<nombre>/output/data.json`)
- Markdown con frontmatter YAML → para Drive/reuniones (`projects/<nombre>/output/informe.md`)

**Externalización de Parámetros:**
`config.py` por proyecto. Contiene pesos de cinturón, umbrales de barbarismo, URLs de fuentes, y cualquier parámetro metodológico modificable.

**Estructura Monorepo:**
Ver PRD §Arquitectura del Monorepo. Cada proyecto es autónomo con su propio `scripts/`, `output/`, y `README.md`.

## Decisiones Arquitectónicas Centrales

### Análisis de Prioridad

**Decisiones Críticas (bloquean implementación):**
- Schema JSON de output del Informe — contrato con dev externo
- Estrategia de fallback/cache — requisito de dominio (fuentes argentinas inestables)
- Lógica de scoring y detección de barbarismos — núcleo metodológico

**Decisiones Importantes (dan forma a la arquitectura):**
- Externalización de parámetros en `config.py` por proyecto
- Convenciones de naming y paths de output

**Decisiones diferidas (post-MVP):**
- Extracción del array de encuestas del Votómetro a JSON independiente
- Runner unificado (`run_all.py`)
- Schema versionado con deprecation workflow formal

### Arquitectura de Datos

**Schema JSON del Informe de Coyuntura (v1.0.0):**

```json
{
  "schema_version": "1.0.0",
  "generated_at": "2026-05-13T10:00:00Z",
  "period": "2026-05",
  "cinturones": {
    "macro": {
      "score": 6.8,
      "estado": "tensionado",
      "barbarismo_riesgo": "tecnocrático",
      "indicadores": {
        "inflacion_mensual": {
          "valor": 3.7,
          "unidad": "%",
          "fuente": "INDEC",
          "fecha_dato": "2026-04-30",
          "desactualizado": false
        }
      },
      "alerta": null
    }
  },
  "barbarismo_activo": "tecnocrático",
  "alerta_multicinturon": false,
  "flags": []
}
```

Output path: `projects/informe_coyuntura/output/informe.json`

**Cache de fallback por cinturón:**
Cada colector guarda el último resultado exitoso en `projects/informe_coyuntura/output/cache/<cinturon>.json`. Si la fuente falla, el colector carga el cache, setea `desactualizado: true` en cada indicador afectado, y preserva `fecha_dato` del cache. El informe se genera con los datos disponibles + flags de advertencia.

### Lógica de Scoring Matusiano

**Escala:** 0-10 por cinturón (promedio ponderado de indicadores; pesos en `config.py`)

**Umbrales de estado:**
- 0-3: estable
- 4-6: en tensión
- 7-10: tensionado

**Detección de barbarismo activo:**
El barbarismo activo corresponde al cinturón con score más alto que supera el umbral de tensión (>= 4):
- Score macro dominante → riesgo tecnocrático
- Score político dominante → riesgo político/demagógico
- Score gestión dominante → riesgo gerencial
- 2+ cinturones con score >= 4 → `alerta_multicinturon: true` (regla matusiana)

Toda la lógica de mapeo cinturón → barbarismo vive en `config.py`.

### Error Handling y Logging

**Estrategia:** fallback por indicador (granular). Si un indicador falla, se usa el cache de ese indicador específico. El cinturón puede tener una mezcla de datos frescos y cacheados.

**Logging:** stdout. Sin archivo de log por ahora — herramienta de un solo operador.

**Señalización de errores:** mensajes claros con fuente y URL fallida para facilitar el parcheo.

### Integración Votómetro

**Estado actual:** datos viven en el HTML (`projects/votometro/web/votometro.html`). El output para el dev es el HTML actualizado.

**Interfaz documentada:** el dev del Votómetro consume el HTML directamente. No hay JSON de output por ahora.

**Deferred:** extracción del array de encuestas a `projects/votometro/output/polls.json` — cuando el dev lo necesite.

### Seguridad y Compliance

No aplica. Herramienta local, datos públicos, sin PII, sin auth, sin API expuesta.

### Infraestructura y Deployment

No aplica. Herramienta local. Sin CI/CD, sin cloud, sin contenedores. El "deploy" es `git push` para sincronizar entre máquinas si es necesario.

## Patrones de Implementación y Reglas de Consistencia

### Puntos de Conflicto Identificados

5 áreas donde distintas implementaciones podrían divergir: estructura interna de scripts, manejo de errores, formato de outputs, naming de claves JSON, y convenciones de logging.

### Patrón Estándar de Colector

Todo colector de cinturón (`macro.py`, `politica.py`, etc.) sigue esta estructura:

```python
# 1. Imports y constantes de fuentes (URLs al inicio, nombradas)
INDEC_IPC_URL = "https://..."
BCRA_RESERVAS_URL = "https://..."

# 2. Carga de config
from config import PESOS_MACRO, UMBRALES

# 3. Funciones de fetch — una por indicador, aisladas
def fetch_inflacion():
    ...

# 4. Función de score — llama a config, no hardcodea
def calcular_score(indicadores):
    ...

# 5. Funciones de cache — leer/escribir
def load_cache():
    ...
def save_cache(data):
    ...

# 6. main() — orquesta, maneja errores, escribe output
def main():
    ...

if __name__ == "__main__":
    main()
```

### Patrones de Naming

**Archivos y módulos:** snake_case — `macro.py`, `vida_cotidiana.py`, `config.py`

**Claves JSON:** snake_case — `inflacion_mensual`, `fecha_dato`, `desactualizado`, `schema_version`

**Strings de estado** (literales exactos para match del dev):
- `"estable"` | `"en_tension"` | `"tensionado"`

**Strings de barbarismo:**
- `"político"` | `"tecnocrático"` | `"gerencial"` | `null`

### Patrones de Formato

**Fechas:** ISO 8601 string — `"2026-04-30"` (solo fecha para datos periódicos)

**Timestamps de generación:** ISO 8601 con hora — `"2026-05-13T10:00:00Z"`

**Scores:** float con 1 decimal — `6.8` (no enteros, no más de 1 decimal)

**Período del informe:** `"YYYY-MM"` — `"2026-05"`

### Patrones de Error Handling

**Por indicador — nunca por cinturón completo:**

```python
try:
    valor = fetch_inflacion()
    indicadores["inflacion_mensual"]["valor"] = valor
    indicadores["inflacion_mensual"]["desactualizado"] = False
except Exception as e:
    print(f"[WARN] macro.inflacion_mensual: {e}. Usando cache.")
    indicadores["inflacion_mensual"]["desactualizado"] = True
```

**Stdout para warnings y errores.** Sin archivo de log.

**Formato de mensaje:** `[WARN] <cinturon>.<indicador>: <descripcion>. Usando cache.`

**Exit codes:** `0` = todos frescos | `1` = parcial (algunos del cache) | `2` = total desde cache

### Patrones de Output

**El colector escribe el cache** en `projects/informe_coyuntura/output/cache/<cinturon>.json` solo cuando hay al menos un dato fresco. No sobreescribir si el fallo es total.

**El generador del informe** lee de los caches y escribe:
- `projects/informe_coyuntura/output/informe.json` (schema v1.0.0)
- `projects/informe_coyuntura/output/informe.md` (markdown con frontmatter YAML)

### Todos los Agentes DEBEN

- Definir URLs de fuentes como constantes nombradas al inicio del script
- Cargar pesos y umbrales desde `config.py`, nunca hardcodear
- Manejar errores por indicador, no por cinturón completo
- Preservar el cache existente si el fetch completo falla
- Usar las claves JSON exactas del schema v1.0.0
- Escribir outputs en los paths predecibles definidos arriba

## Estructura del Proyecto y Límites Arquitectónicos

### Árbol de Directorios Completo

```
CIGOB-Análisis/                         ← raíz del monorepo
├── README.md                           ← instrucciones del monorepo + lista de proyectos
├── .gitignore
├── projects/
│   ├── informe_coyuntura/
│   │   ├── README.md                   ← cómo correr cada script
│   │   ├── config.py                   ← pesos, umbrales, factores de barbarismo, URLs
│   │   ├── requirements.txt
│   │   ├── scripts/
│   │   │   ├── macro.py               ← FR2: colector cinturón macroeconómico
│   │   │   ├── politica.py            ← FR3: colector cinturón político
│   │   │   ├── vida_cotidiana.py      ← FR4: colector vida cotidiana (existente)
│   │   │   ├── gestion.py             ← FR5: colector gestión/CIGOB
│   │   │   └── generar_informe.py     ← FR8-15: leer caches → calcular → escribir output
│   │   └── output/
│   │       ├── cache/
│   │       │   ├── macro.json         ← último fetch válido cinturón macro
│   │       │   ├── politica.json
│   │       │   ├── vida_cotidiana.json
│   │       │   └── gestion.json
│   │       ├── informe.json           ← FR10: output JSON para dev (schema v1.0.0)
│   │       └── informe.md             ← FR9: output Markdown para Drive y reunión
│   └── votometro/
│       ├── README.md
│       ├── web/
│       │   └── votometro.html         ← FR23-27: modelo electoral completo (existente)
│       ├── scripts/
│       │   └── update_polls.py        ← nice-to-have: helper para agregar encuestas
│       └── output/                    ← reservado para polls.json (deferred)
├── docs/                              ← 5 documentos fuente CIGOB (.docx)
├── output/                            ← outputs globales / sync con Drive
│   └── analisis_realidad_politica/    ← análisis matusiano existente
└── _bmad-output/                      ← artefactos BMAD
    └── planning-artifacts/
        ├── prd.md
        └── architecture.md
```

### Mapeo de Requerimientos a Estructura

| FR Category | Archivos |
|---|---|
| Recolección de datos (FR1-7) | `projects/informe_coyuntura/scripts/[macro,politica,vida_cotidiana,gestion].py` |
| Generación del informe (FR8-12) | `projects/informe_coyuntura/scripts/generar_informe.py` |
| Análisis matusiano (FR13-16) | `config.py` (parámetros) + `generar_informe.py` (lógica) |
| Gestión del monorepo (FR17-19) | Estructura `projects/` + `README.md` por proyecto |
| Integración devs (FR20-22) | `output/informe.json` + `votometro/web/votometro.html` |
| Votómetro (FR23-27) | `projects/votometro/web/votometro.html` |

### Límites Arquitectónicos

**Límite CIGOB ↔ Dev del Informe:**
`projects/informe_coyuntura/output/informe.json` — schema v1.0.0, no breaking changes sin aviso en README.

**Límite CIGOB ↔ Dev del Votómetro:**
`projects/votometro/web/votometro.html` — el dev consume el HTML actualizado directamente.

**Límite interno colectores ↔ generador:**
`projects/informe_coyuntura/output/cache/<cinturon>.json` — interfaz interna, no expuesta a devs.

**Límite CIGOB ↔ Drive:**
`output/` raíz — los archivos generados se sincronizan manualmente a Drive.

### Flujo de Datos

```
[fuentes argentinas] → macro.py → cache/macro.json ─┐
[fuentes argentinas] → politica.py → cache/politica.json ─┤
[fuentes argentinas] → vida_cotidiana.py → cache/vida_cotidiana.json ─┤ → generar_informe.py
[fuentes argentinas] → gestion.py → cache/gestion.json ─┘
                                                            ↓
                                              output/informe.json  (→ Dev Informe)
                                              output/informe.md    (→ Drive → Reunión)

[Trico agrega encuesta] → votometro.html (edición manual)  (→ Dev Votómetro)
```

### Notas de Migración (Brownfield)

Archivos existentes que se mueven en la restructura:
- `web/votometro.html` → `projects/votometro/web/votometro.html`
- `scripts/vida_cotidiana/` → `projects/informe_coyuntura/scripts/vida_cotidiana.py`
- El resto de `scripts/` se evalúa en el momento de la restructura

## Validación de la Arquitectura

### Validación de Coherencia Interna

- [x] Los patrones de colector son consistentes entre los 4 cinturones
- [x] El schema JSON v1.0.0 está completamente especificado y es implementable sin ambigüedad
- [x] El mecanismo de cache es determinista: éxito parcial escribe cache, fallo total preserva cache
- [x] La lógica de scoring y barbarismo en `config.py` es auditable y separada del código de procesamiento
- [x] Los límites arquitectónicos (CIGOB ↔ Dev Informe, CIGOB ↔ Dev Votómetro, colectores ↔ generador) son claros y no se superponen
- [x] La estructura de monorepo permite agregar proyectos sin tocar los existentes

### Cobertura de Requerimientos

Todos los 27 FRs del PRD están cubiertos:

| FR Category | Cobertura |
|---|---|
| FR1-7 (Recolección) | Patrón de colector estándar + fallback/cache + exit codes |
| FR8-12 (Generación) | `generar_informe.py` + schema v1.0.0 + outputs duales JSON/MD |
| FR13-16 (Análisis Matusiano) | Scoring 0-10 + barbarismo detection + alerta_multicinturon + config.py |
| FR17-19 (Gestión Monorepo) | Estructura `projects/` + README por proyecto + commit policy |
| FR20-22 (Integración Devs) | Schema versionado + paths predecibles + contrato HTML Votómetro |
| FR23-27 (Votómetro) | HTML existente como límite; extracción polls.json deferred |

NFRs cubiertos: performance (<5min colectores, <1min generador), integración (schema estable, paths predecibles), mantenibilidad (URLs nombradas, config.py, README-driven).

### Análisis de Brechas

**Brechas Críticas (bloquean implementación):** Ninguna.

**Brechas Importantes (resolver en implementación):**
- Los indicadores específicos por cinturón (qué series exactas de INDEC/BCRA/Congreso) no están definidos en la arquitectura. Se resolverán story por story durante la implementación, usando los scripts `vida_cotidiana` existentes como referencia de patrón.

**Elementos Diferidos (post-MVP, no bloquean):**
- Extracción del array de encuestas del Votómetro a `polls.json`
- Runner unificado `run_all.py`
- Schema versionado con deprecation workflow formal

### Checklist Final

- [x] Dominio tecnológico correcto identificado (Python data pipeline local)
- [x] Starter template evaluado (no aplica; fundaciones documentadas)
- [x] Decisiones críticas tomadas (schema, cache, scoring, barbarismo)
- [x] Patrones de implementación definidos (colector, naming, error handling, outputs)
- [x] Estructura de proyecto completa con árbol de directorios
- [x] Límites arquitectónicos explícitos
- [x] Flujo de datos documentado
- [x] Notas de migración brownfield incluidas
- [x] NFRs contemplados en las decisiones
- [x] Coherencia interna verificada
- [x] Cobertura de FRs verificada
- [x] Brechas identificadas y clasificadas
- [x] Sin brechas críticas

### Estado General

**READY FOR IMPLEMENTATION**

**Primera prioridad de implementación:**
1. Restructura física del monorepo (crear árbol `projects/`, migrar archivos existentes)
2. `config.py` skeleton para `informe_coyuntura` (pesos, umbrales, barbarismo mapping)
3. `macro.py` — primer colector nuevo
4. `generar_informe.py` — lector de caches + generador de output dual
