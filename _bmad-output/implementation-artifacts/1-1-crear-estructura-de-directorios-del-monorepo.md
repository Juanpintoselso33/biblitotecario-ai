# Story 1.1: Crear estructura de directorios del monorepo

**Status:** ready-for-dev
**Epic:** 1 — Monorepo Foundation & Configuración
**Story:** 1.1

## Story

Como Trico,
quiero que el monorepo tenga la estructura de carpetas definida en la arquitectura (`projects/informe_coyuntura/` y `projects/votometro/` con todos sus subdirectorios),
para que cada proyecto sea autónomo y cualquier dev pueda orientarse en el repo sin ayuda.

## Acceptance Criteria

**Given** el repo clonado en la máquina de Trico
**When** se lista el árbol de directorios
**Then** existe `projects/informe_coyuntura/scripts/`, `projects/informe_coyuntura/output/cache/`, `projects/votometro/web/`, `projects/votometro/scripts/`, `projects/votometro/output/`
**And** cada directorio vacío tiene un `.gitkeep` para que git lo trackee
**And** existe un `requirements.txt` vacío en `projects/informe_coyuntura/`
**And** el `.gitignore` raíz excluye los outputs generados: `projects/*/output/*.json`, `projects/*/output/*.md`, `projects/*/output/cache/*.json`

## Brownfield State — Qué existe hoy

**El directorio `projects/` NO existe.** Hay que crearlo desde cero.

Archivos brownfield en sus ubicaciones ACTUALES (se moverán en Story 1.2, NO en esta story):
- `web/votometro.html` — Votómetro operativo (NO mover aquí)
- `web/encuestas.json`, `web/index.html`, `web/bibliotecario.html`, `web/remixed-71df43cf.html`, `web/votometro-original.html` — NO mover
- `scripts/vida_cotidiana/` — colector existente con `main.py`, `collectors/`, `config.py`, `data/`, `requirements.txt` (NO mover aquí)
- `scripts/actualizar_encuestas.py`, `scripts/descargar_emae.py`, etc. — scripts sueltos (NO mover)

**Esta story solo crea estructura vacía.** Story 1.2 hace la migración.

## Árbol objetivo completo

```
projects/
├── informe_coyuntura/
│   ├── requirements.txt        ← vacío por ahora
│   ├── scripts/
│   │   └── .gitkeep
│   └── output/
│       └── cache/
│           └── .gitkeep
└── votometro/
    ├── web/
    │   └── .gitkeep
    ├── scripts/
    │   └── .gitkeep
    └── output/
        └── .gitkeep
```

**Nota:** `projects/informe_coyuntura/` no tiene `.gitkeep` raíz — `requirements.txt` ya trackea el directorio. `projects/votometro/` tampoco necesita `.gitkeep` raíz porque sus subdirectorios están trackeados.

## Cambios en `.gitignore`

El `.gitignore` actual existe en la raíz. Hay que **agregar al final** las siguientes líneas (NO reemplazar el archivo — solo agregar):

```gitignore
# CIGOB Análisis — outputs generados por colectores e informes
projects/*/output/*.json
projects/*/output/*.md
projects/*/output/cache/*.json
```

**No borrar** las entradas existentes. El `.gitignore` actual ya maneja `__pycache__/`, `*.pyc`, `node_modules/`, etc.

## Implementación paso a paso

### 1. Crear árbol de directorios

```bash
mkdir -p projects/informe_coyuntura/scripts
mkdir -p projects/informe_coyuntura/output/cache
mkdir -p projects/votometro/web
mkdir -p projects/votometro/scripts
mkdir -p projects/votometro/output
```

### 2. Crear `.gitkeep` en directorios vacíos

```bash
touch projects/informe_coyuntura/scripts/.gitkeep
touch projects/informe_coyuntura/output/cache/.gitkeep
touch projects/votometro/web/.gitkeep
touch projects/votometro/scripts/.gitkeep
touch projects/votometro/output/.gitkeep
```

### 3. Crear `requirements.txt` vacío

```bash
touch projects/informe_coyuntura/requirements.txt
```

El archivo permanece vacío. Las dependencias se agregarán cuando se implementen los colectores (Story 2.2+). Las dependencias probables son `requests` para HTTP — se documentan en Story 2.2, no aquí.

### 4. Actualizar `.gitignore`

Agregar al final del `.gitignore` raíz existente:

```gitignore
# CIGOB Análisis — outputs generados por colectores e informes
projects/*/output/*.json
projects/*/output/*.md
projects/*/output/cache/*.json
```

**Crítico:** los `.gitkeep` dentro de `output/` y `output/cache/` quedan trackeados a pesar del gitignore — los patterns `*.json` y `*.md` no afectan a `.gitkeep`. Verificar con `git status` que los `.gitkeep` aparecen como untracked/staged, no ignorados.

## Verificación de ACs

Después de implementar, verificar:

```bash
# Verificar estructura
ls projects/informe_coyuntura/scripts/.gitkeep    # debe existir
ls projects/informe_coyuntura/output/cache/.gitkeep  # debe existir
ls projects/votometro/web/.gitkeep                # debe existir
ls projects/votometro/scripts/.gitkeep            # debe existir
ls projects/votometro/output/.gitkeep             # debe existir
ls projects/informe_coyuntura/requirements.txt    # debe existir

# Verificar gitignore no ignora gitkeep
git status projects/  # todos los .gitkeep deben aparecer como untracked
```

## Límites de esta story — qué NO hacer

- **NO crear** `config.py` — eso es Story 1.3
- **NO mover** `web/votometro.html` ni `scripts/vida_cotidiana/` — eso es Story 1.2
- **NO crear** READMEs — eso es Story 1.4
- **NO instalar** dependencias en `requirements.txt` — se llenan en Epic 2
- **NO crear** archivos en `projects/votometro/scripts/` más allá del `.gitkeep`

## Commit

El commit de esta story debe documentar únicamente la creación de estructura. Mensaje sugerido:

```
feat(monorepo): crear estructura de directorios projects/ (Story 1.1)

- Árbol projects/informe_coyuntura/ y projects/votometro/ con subdirectorios
- .gitkeep en directorios vacíos para tracking git
- requirements.txt vacío en informe_coyuntura/
- .gitignore actualizado con exclusiones de outputs generados
```

## Dev Notes

- Plataforma: Windows (máquina de Trico). Los comandos `mkdir -p` y `touch` funcionan en Git Bash / WSL. En PowerShell: `New-Item -ItemType Directory -Force` y `New-Item -ItemType File`.
- `python` disponible como `python`, no `python3`.
- Git remote: `https://github.com/Juanpintoselso33/biblitotecario-ai.git`, rama actual: `feat/bmad-method-install`. No pushear hasta que Trico lo indique.
- No hay tests automatizados en este proyecto — la verificación es manual con `ls` y `git status`.
