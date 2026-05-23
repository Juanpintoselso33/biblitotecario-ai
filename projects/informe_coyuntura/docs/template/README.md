# Template institucional CIGOB para conversión Markdown → Word

Sistema reproducible de conversión de `.md` a `.docx` con identidad visual CIGOB (logo, paleta institucional, tipografía, header y footer).

## Archivos

| Archivo | Propósito |
|---|---|
| `cigob_logo.png` | Logo CIGOB descargado del sitio oficial (cigob.org) |
| `cigob_reference.docx` | Plantilla Word con todos los estilos institucionales aplicados |
| `build_reference.py` | Script que regenera `cigob_reference.docx` desde el default de pandoc |
| `build_all_docx.ps1` | Script PowerShell para regenerar todos los .docx con el template |

## Paleta institucional

Extraída del sitio oficial cigob.org:

| Color | Hex | Uso |
|---|---|---|
| Azul CIGOB | `#1D67CD` | Headings nivel 1 y 2, línea decorativa de header |
| Azul oscuro | `#0F3D7A` | Título principal, Heading 3 |
| Gris texto | `#333333` | Cuerpo de texto, Heading 4 |
| Gris secundario | `#5F6360` | Subtítulos, autor, fecha, footer, captions |

## Tipografía

- **Títulos y cuerpo:** Calibri (default de Word, no requiere instalación)
- **Código:** Consolas

Decisión técnica: el sitio CIGOB usa Montserrat (títulos) y Lato (cuerpo). Para evitar dependencias de fuentes externas que no estén instaladas en la máquina del lector, el template usa Calibri (incluido con Word). El estilo institucional se preserva por colores, espaciado y línea decorativa.

## Estructura del documento generado

- **Header:** logo CIGOB alineado a la derecha, línea separadora azul.
- **Footer:** centrado, "Fundación CiGob · página X de Y" en gris claro, línea separadora superior.
- **Márgenes:** 2.5 cm superior, izquierdo y derecho; 2.0 cm inferior.
- **Title (# en md):** Calibri 26pt, azul oscuro, negrita.
- **Heading 1 (## en md):** Calibri 18pt, azul CIGOB, negrita, con línea decorativa inferior.
- **Heading 2 (### en md):** Calibri 14pt, azul CIGOB, negrita.
- **Heading 3 (#### en md):** Calibri 12pt, azul oscuro, negrita.
- **Cuerpo:** Calibri 11pt, gris texto.
- **Citas (`>`):** Calibri 11pt itálica, gris secundario.
- **Tablas:** bordes finos color gris claro.

## Cómo regenerar el template (si se cambia el estilo)

```powershell
cd projects/informe_coyuntura/docs/template
pandoc -o cigob_reference.docx --print-default-data-file reference.docx
python build_reference.py
```

El primer comando obtiene el reference.docx default de pandoc. El segundo lo modifica aplicando los estilos institucionales.

## Cómo regenerar todos los .docx desde los .md

Desde `projects/informe_coyuntura/docs/`:

**PowerShell (Windows):**
```powershell
./template/build_all_docx.ps1
```

**bash (Linux/Mac/WSL):**
```bash
for f in cinturon_gestion cinturon_macro cinturon_politica cinturon_vida_cotidiana 260523_proyecto_pais_estado_extraccion; do
    pandoc "$f.md" -o "$f.docx" --reference-doc=template/cigob_reference.docx
done
```

## Comando manual para un solo documento

```powershell
pandoc input.md -o output.docx --reference-doc=template/cigob_reference.docx
```

## Dependencias

- `pandoc` >= 3.0 (`F:\miniconda\Scripts\pandoc.exe` en el entorno actual)
- Python con `python-docx` (`pip install python-docx`)
- Python con `requests` y `Pillow` (solo si se vuelve a descargar el logo)
