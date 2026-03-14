# Skill: preparar-reunion

Proceso para preparar material de reunión en el contexto CIGOB.
Invocar cuando el usuario comparta un temario y pida preparar outputs.

---

## Proceso paso a paso

### 1. Leer los documentos fuente
Antes de generar cualquier output, leer los docs relevantes:
```python
import sys, zipfile, os
from xml.etree import ElementTree as ET
sys.stdout.reconfigure(encoding='utf-8')

def extract_docx(path):
    with zipfile.ZipFile(path) as z:
        with z.open('word/document.xml') as f:
            tree = ET.parse(f)
            ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            return '\n'.join(
                ''.join(t.text or '' for t in p.findall('.//w:t', ns))
                for p in tree.findall('.//w:p', ns)
                if ''.join(t.text or '' for t in p.findall('.//w:t', ns)).strip()
            )

docs_dir = r'C:\Users\trico\OneDrive\UBA\Analisis CIGOB\docs'
for fname in sorted(os.listdir(docs_dir)):
    if fname.endswith(('.docx', '.dotx')):
        print(f'=== {fname} ===')
        print(extract_docx(os.path.join(docs_dir, fname)))
```

### 2. Mapear cada punto del temario a los docs relevantes

| Tipo de punto | Docs a leer |
|---|---|
| Estrategia / posicionamiento | Propuesta Estratégica + CIGOB frente a la IA |
| Marco intelectual / narrativa | Hechos y Profecías + Profetas de Anticipación |
| Votómetro / análisis electoral | web/remixed-71df43cf.html |
| Propósito / identidad institucional | El Propósito + Propuesta Estratégica |

### 3. Para cada punto generar un archivo `output/0N_nombre.md`

Estructura de cada output:

```markdown
# Punto N — [Nombre]
*[fecha]*

## Contexto
[Qué dicen los docs sobre este punto — citas si aplica]

## Análisis
[Qué significa para CIGOB — tensiones, oportunidades]

## Opciones
[2-3 alternativas cuando haya decisiones a tomar]

## Recomendación
[Una recomendación concreta y accionable]
```

### 4. Generar `output/00_resumen_ejecutivo.md` al final

```markdown
# Resumen ejecutivo — Reunión [fecha]

## Los N puntos en síntesis
[1 párrafo por punto]

## Decisiones que requiere la reunión
[Lista numerada de preguntas concretas que hay que salir respondidas]

## Archivos de detalle
[Lista de outputs generados]
```

### 5. Verificar coherencia con el marco CIGOB

Antes de cerrar, revisar que todos los outputs:
- [ ] Usan el concepto "Anticipación Estratégica" consistentemente
- [ ] No confunden CIGOB con una consultora tech ni con un think tank puramente académico
- [ ] Las recomendaciones son accionables (no genéricas)
- [ ] Las decisiones pendientes son preguntas concretas, no vagas

---

## Qué NO hacer

- No generar outputs sin leer los docs primero
- No inventar posiciones de CIGOB que no estén en los documentos
- No hacer un único archivo largo — un archivo por punto facilita la reunión
- No omitir tensiones o problemas incómodos — la utilidad está en ser honesto
