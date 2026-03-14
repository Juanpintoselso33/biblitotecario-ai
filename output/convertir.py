"""
Convierte todos los archivos .md en output/ a .docx y .pdf usando pandoc.
Ejecutar desde la carpeta output/ o desde cualquier lugar.
"""
import subprocess, os, sys
sys.stdout.reconfigure(encoding='utf-8')

OUTPUT_DIR = r'C:\Users\trico\OneDrive\UBA\Analisis CIGOB\output'

# Estilo Word con formato CIGOB-ish
REFERENCE_DOCX_ARGS = []  # podemos agregar --reference-doc si hay una plantilla

def convert_file(md_path):
    base = os.path.splitext(md_path)[0]
    name = os.path.basename(base)

    # Skip self
    if name == 'convertir':
        return

    docx_path = base + '.docx'
    pdf_path  = base + '.pdf'

    # → DOCX
    result = subprocess.run(
        ['pandoc', md_path, '-o', docx_path,
         '--from', 'markdown',
         '-V', 'lang=es',
         '--wrap=none'],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f'✓ DOCX: {name}.docx')
    else:
        print(f'✗ DOCX falló: {name} — {result.stderr.strip()}')

    # → PDF via pdflatex
    result = subprocess.run(
        ['pandoc', md_path, '-o', pdf_path,
         '--from', 'markdown',
         '--pdf-engine=pdflatex',
         '-V', 'lang=es',
         '-V', 'geometry:margin=2.5cm',
         '-V', 'fontsize=11pt',
         '-V', 'mainfont=Arial',
         '--wrap=none'],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f'✓ PDF:  {name}.pdf')
    else:
        # fallback sin fuente personalizada
        result2 = subprocess.run(
            ['pandoc', md_path, '-o', pdf_path,
             '--from', 'markdown',
             '--pdf-engine=pdflatex',
             '-V', 'lang=es',
             '-V', 'geometry:margin=2.5cm',
             '-V', 'fontsize=11pt',
             '--wrap=none'],
            capture_output=True, text=True
        )
        if result2.returncode == 0:
            print(f'✓ PDF:  {name}.pdf')
        else:
            print(f'✗ PDF falló: {name} — {result2.stderr.strip()[:200]}')

def main():
    md_files = [
        os.path.join(OUTPUT_DIR, f)
        for f in sorted(os.listdir(OUTPUT_DIR))
        if f.endswith('.md')
    ]

    if not md_files:
        print('No hay archivos .md en output/')
        return

    print(f'Convirtiendo {len(md_files)} archivos...\n')
    for md in md_files:
        convert_file(md)

    print('\nListo.')

if __name__ == '__main__':
    main()
