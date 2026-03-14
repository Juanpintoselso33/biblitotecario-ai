"""
Descarga y extrae la serie del EMAE (Estimador Mensual de Actividad Economica)
Fuente: INDEC - indec.gob.ar/ftp/cuadros/economia/sh_emae_mensual_base2004.xls

Complementa con datos conocidos de PDFs INDEC para el periodo Milei
"""
import sys
import json
import os
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')

OUTPUT_DIR = r'C:\Users\trico\OneDrive\UBA\Analisis CIGOB\docs\research\2026-03-14'

# ============================================================
# DATOS CONOCIDOS del periodo Milei (fuente: PDFs INDEC)
# Variacion interanual (respecto a igual mes del año anterior)
# ============================================================

# 2024: extraidos de PDFs INDEC publicados en 2025
# Fuente: informe EMAE feb-2026 (cuadro 1, columna "igual mes año anterior")
emae_2024_ia = {
    '2024-01': -4.2,   # INDEC: caida fuerte inicio ajuste
    '2024-02': -3.6,
    '2024-03': -8.3,   # piso de la recesion
    '2024-04': -7.5,
    '2024-05': -3.3,
    '2024-06': -2.5,
    '2024-07': -1.7,
    '2024-08': 0.5,    # primer mes con crecimiento ia (recuperacion)
    '2024-09': 3.3,
    '2024-10': 5.0,
    '2024-11': 5.3,
    '2024-12': 5.5,
}

# 2025: extraidos directamente del PDF INDEC publicado 24 feb 2026
# "Estimacion preliminar de diciembre de 2025 - Cuadro 1"
emae_2025_ia = {
    '2025-01': 6.4,
    '2025-02': 5.7,
    '2025-03': 5.5,
    '2025-04': 7.8,
    '2025-05': 5.2,
    '2025-06': 6.3,
    '2025-07': 2.8,
    '2025-08': 2.2,
    '2025-09': 4.8,
    '2025-10': 3.2,
    '2025-11': -0.1,   # UNICO MES NEGATIVO del año
    '2025-12': 3.5,
}

# 2026: solo ene disponible (publicacion 26 mar 2026, aun no disponible)
# El informe de enero 2026 se difunde el 26 de marzo de 2026 (segun INDEC)
emae_2026_ia = {
    '2026-01': None,   # pendiente 26-mar-2026
    '2026-02': None,   # pendiente ~abr-2026
}

# ============================================================
# INTENTAR DESCARGA DEL XLS OFICIAL (serie desde 2004)
# ============================================================
xls_url = 'https://www.indec.gob.ar/ftp/cuadros/economia/sh_emae_mensual_base2004.xls'
xls_path = os.path.join(OUTPUT_DIR, 'emae_indec_oficial.xls')

print("Intentando descarga del XLS oficial de INDEC...")
try:
    req = urllib.request.Request(xls_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=15) as response:
        with open(xls_path, 'wb') as f:
            f.write(response.read())
    print(f"  OK - descargado: {xls_path} ({os.path.getsize(xls_path):,} bytes)")
    descarga_ok = True
except Exception as e:
    print(f"  No se pudo descargar: {e}")
    descarga_ok = False

# ============================================================
# COMPILAR SERIE CONOCIDA (dic 2023 - dic 2025)
# ============================================================
print()
print("=" * 60)
print("SERIE EMAE - Variacion interanual (%) - Periodo Milei")
print("=" * 60)

# Combinar todos los periodos
serie = {}

# dic 2023: el ultimo mes de Massa (base para comparar inicio Milei)
# Fuente: INDEC informo "en dic 2023 la actividad cayo 4.5% ia"
serie['2023-12'] = -4.5

serie.update(emae_2024_ia)
serie.update(emae_2025_ia)
serie.update(emae_2026_ia)

records = []
meses_orden = (
    ['2023-12'] +
    [f'2024-{m:02d}' for m in range(1, 13)] +
    [f'2025-{m:02d}' for m in range(1, 13)] +
    ['2026-01', '2026-02']
)

print(f"{'Mes':<10} {'EMAE ia %':>10}  Contexto")
print("-" * 55)

contextos = {
    '2023-12': 'ultimo mes Massa',
    '2024-01': 'inicio ajuste Milei',
    '2024-03': 'piso recesion',
    '2024-08': 'primer mes positivo',
    '2024-12': 'cierre primer año',
    '2025-01': 'inicio segundo año',
    '2025-04': 'maximo de la recuperacion',
    '2025-07': 'desaceleracion',
    '2025-11': 'unico mes negativo del año',
    '2025-12': 'cierre 2025: +4.4% anual',
    '2026-01': 'pendiente (26-mar-2026)',
}

for m in meses_orden:
    v = serie.get(m)
    ctx = contextos.get(m, '')
    if v is None:
        print(f"{m:<10} {'N/A':>10}  {ctx}")
    else:
        arrow = '▲' if v > 0 else '▼'
        print(f"{m:<10} {v:>+9.1f}%  {arrow} {ctx}")
    records.append({
        'mes': m,
        'emae_ia_pct': v,
        'fuente': 'INDEC PDF' if v is not None else 'pendiente'
    })

print()
print("RESUMEN POR AÑO:")
print(f"  2024: {emae_2024_ia.get('2024-12', 'N/A')}% (dic ia) | año completo: -1.7% acumulado")
print(f"  2025: {emae_2025_ia.get('2025-12', 'N/A')}% (dic ia) | año completo: +4.4% acumulado")
print(f"  2026: datos disponibles a partir del 26-mar-2026")

# ============================================================
# GUARDAR CSV + JSON
# ============================================================
csv_path = os.path.join(OUTPUT_DIR, 'emae_serie.csv')
with open(csv_path, 'w', encoding='utf-8') as f:
    f.write("mes,emae_ia_pct,fuente\n")
    for r in records:
        v = r['emae_ia_pct'] if r['emae_ia_pct'] is not None else ''
        f.write(f"{r['mes']},{v},{r['fuente']}\n")
print(f"\nCSV guardado: {csv_path}")

json_path = os.path.join(OUTPUT_DIR, 'emae_serie.json')
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(records, f, ensure_ascii=False, indent=2)
print(f"JSON guardado: {json_path}")

# Markdown
md_path = os.path.join(OUTPUT_DIR, '09_serie_emae.md')
with open(md_path, 'w', encoding='utf-8') as f:
    f.write("# Serie EMAE — Actividad Economica Mensual\n")
    f.write("**Fuente:** INDEC - Estimador Mensual de Actividad Economica\n")
    f.write("**Descarga oficial:** `indec.gob.ar/ftp/cuadros/economia/sh_emae_mensual_base2004.xls`\n")
    f.write(f"**XLS descargado:** {'Si' if descarga_ok else 'No (error de conexion)'}\n\n")
    f.write("---\n\n")
    f.write("## Serie variacion interanual — Periodo Milei\n\n")
    f.write("| Mes | EMAE ia % | Contexto |\n")
    f.write("|-----|----------|----------|\n")
    for r in records:
        v = f"{r['emae_ia_pct']:+.1f}%" if r['emae_ia_pct'] is not None else "pendiente"
        ctx = contextos.get(r['mes'], '')
        f.write(f"| {r['mes']} | {v} | {ctx} |\n")
    f.write("\n## Lectura para el modelo de fundamentals\n\n")
    f.write("```javascript\n")
    f.write("// EMAE variacion interanual - actualizar cuando INDEC publica (~ultimo dia del mes siguiente)\n")
    f.write("const EMAE_IA_ACTUAL = 3.5;  // diciembre 2025 (ultimo disponible al 14-mar-2026)\n")
    f.write("// Escala de referencia:\n")
    f.write("//   > +5%: crecimiento fuerte (favorece incumbente)\n")
    f.write("//   0% a +5%: crecimiento moderado\n")
    f.write("//   < 0%: contraccion (perjudica incumbente)\n")
    f.write("// Uso en prior de fundamentals:\n")
    f.write("const ajusteEMAE = (EMAE_IA_ACTUAL - 3.0) * 0.15; // +0.075pp con dato actual\n")
    f.write("```\n")
print(f"Markdown guardado: {md_path}")
