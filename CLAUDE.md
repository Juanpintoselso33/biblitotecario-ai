# CIGOB Analysis Project

Espacio de análisis para Fundación CIGOB (contexto UBA). El objetivo es analizar documentos y la página web para producir nuevos documentos e informes destinados a reuniones, posicionamiento institucional y estrategia.

---

## Estructura del proyecto

```
docs/      → 5 documentos Word únicos (ver lista abajo)
web/       → Votómetro Argentina 2027 (HTML estático)
output/    → Outputs generados: análisis, briefs, informes de reunión
.claude/
  agents/  → Agentes especializados para este proyecto
  commands/ → Slash commands locales
```

---

## Los 5 documentos en `docs/`

| Archivo | Contenido | Tipo |
|---|---|---|
| `260216 01 Sobre Hechos y Profecías (1).docx` | Ensayo histórico: ciencia vs profetas del fin (Malthus, Ludditas, Peste). Tesis: la innovación siempre supera el catastrofismo. | Marco intelectual |
| `260216 03 PROFETAS DE ANTICIPACIÓN (1).docx` | Asimov como modelo de "profeta de la anticipación". Las Tres Leyes como primer framework de gobernanza de IA. | Marco intelectual |
| `260216 05 CIGOB FRENTE AL DESAFIO DE LA IA v2 (1).docx` | Posición de CIGOB ante la IA: "Anticipación Estratégica". Entre el freno (Yudkowsky/Hinton) y el avance ciego. Innerarity y la simplificación tecnológica. | Paper de posición |
| `260217 PROPUESTA ESTRATÉGICA CIGOB.dotx` | Plan 2026-2027: 3 centros (Comunicación, Estudios/CECIG, Soluciones). Votómetro, podcast, planes de gobierno. | Documento operativo |
| `El Propósito de la Fundación Cigob (1).docx` | Propósito fundacional: transformar gestión subnacional. Contexto era Milei, tecnología como medio. | Documento fundacional |

**Nota:** Los archivos con `(1)` son los únicos válidos. Los duplicados `(2)` y sin número fueron eliminados (eran triplicados de OneDrive).

---

## Marco conceptual central de CIGOB

- **Anticipación Estratégica**: posición diferencial entre "deténganse" (Yudkowsky) y "avancen sin control". CIGOB diseña el volante mientras el motor corre.
- **Profeta del Fin vs. Profeta de la Anticipación**: Malthus/Ludditas ↔ Asimov/Haber-Bosch. La innovación siempre rompe los límites catastrofistas.
- **Brecha subnacional**: mientras el mundo debate IA en abstracto, CIGOB opera con provincias y municipios argentinos.
- **Estado forense vs. Estado con sensores**: de llegar tarde al daño a prevenirlo en tiempo real.
- **Tecnología como medio, no como fin**: la responsabilidad de implementación es política.

---

## El Votómetro (`web/votometro.html`)

HTML estático puro, sin build. Colaboración CIGOB + Redlines Estrategia y Comunicación.
Archivo activo: `web/votometro.html` (el `web/remixed-71df43cf.html` es la versión original archivada).

**Metodología:**
- Ponderación quíntuple: decaimiento temporal (λ=0.015) × calidad consultora × sesgo histórico × orientación del medio × metodología
- Monte Carlo: 10.000 simulaciones con σ=6.5 calibrado al error histórico argentino (PASO 2023: 8-13pp)
- Corrección de voto oculto: bayesiana, calibrada con legislativas 2025
- Verificación Art. 97-98 CN en cada simulación
- **Prior de fundamentals** (mar 2026): blend dinámico encuestas × prior estructural (aprobación, ICC Di Tella, EMAE). Peso fundamentals decrece desde 50% a >1000 días hasta 0% el día de la elección.

**Estado actual (mar. 2026):** LLA ~41%, PJ ~30%. Prior fundamentals: ~41.9%.

**Problema principal:** datos hardcodeados en el HTML — no se actualiza automáticamente.

---

## Cómo leer los .docx con Python

```python
import zipfile, sys
from xml.etree import ElementTree as ET
sys.stdout.reconfigure(encoding='utf-8')

def extract_docx(path):
    with zipfile.ZipFile(path) as z:
        with z.open('word/document.xml') as f:
            tree = ET.parse(f)
            ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            paragraphs = tree.findall('.//w:p', ns)
            lines = []
            for p in paragraphs:
                texts = p.findall('.//w:t', ns)
                line = ''.join(t.text or '' for t in texts)
                if line.strip():
                    lines.append(line)
            return '\n'.join(lines)
```

Usar siempre rutas Windows (`r'C:\...'`) y `os.listdir()` para iterar archivos — las rutas Unix (`/c/...`) fallan con nombres con tildes.

---

## Outputs generados

Los outputs van en `output/` como archivos `.md`. Nombrar con prefijo numérico según punto de agenda o tipo:
- `00_resumen_ejecutivo.md`
- `01_tema.md`, `02_tema.md`, etc.

---

## Agentes disponibles (`.claude/agents/`)

- **lector-docs**: Extrae y analiza los documentos Word. Identifica conceptos, compara versiones, genera resúmenes.
- **analista-votometro**: Analiza el HTML del Votómetro. Metodología, datos electorales, próximos pasos técnicos.
- **generador-outputs**: Dado un temario o brief, produce archivos de output estructurados en `output/`.

## Comandos disponibles (`.claude/commands/`)

- `/reunion` — prepara outputs para una reunión dado un temario
- `/analizar-docs` — análisis completo de los documentos actuales
- `/votometro` — análisis del estado del Votómetro

## Skills disponibles (`.claude/skills/`)

Guías de proceso que Claude sigue cuando la tarea aplica. Leer antes de ejecutar la tarea correspondiente.

- **preparar-reunion**: paso a paso para generar outputs de reunión — mapeo de docs, estructura de archivos, checklist de coherencia
- **redactar-cigob**: voz, tono, conceptos ancla y estructura según tipo de pieza para cualquier contenido de CIGOB
- **mantener-votometro**: cómo agregar encuestas, dónde está cada cosa en el HTML, roadmap técnico pendiente

---

## Git y deploy

- **Sí es un repositorio git.** Remote: `https://github.com/Juanpintoselso33/biblitotecario-ai.git`
- **Deploy automático** via GitHub Pages en: `https://juanpintoselso33.github.io/biblitotecario-ai/index.html`
- Siempre commitear y pushear a `main` al terminar cambios en el Votómetro.

## Notas técnicas

- Sin package manager ni build system
- Todo el contenido está en español
- Python disponible como `python` (no `python3`)
- Siempre usar `sys.stdout.reconfigure(encoding='utf-8')` en scripts con caracteres especiales
