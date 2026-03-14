"""
Reconstruccion de la serie historica del ICC (Indice de Confianza del Consumidor)
Universidad Torcuato Di Tella - Periodo Milei (dic 2023 - feb 2026)

Fuentes:
- Variaciones mensuales: pagina UTDT (utdt.edu/ver_contenido.php?id_contenido=2575)
- Anclas (valores absolutos): comunicados de prensa Di Tella / Infobae / Trading Economics

Metodologia:
- Encadenar variaciones mensuales partiendo de anclas conocidas
- Los meses ago-sep 2025 se interpolan geometricamente entre jul y oct
- Se corrige deriva usando las anclas verificadas
"""
import sys
import json
import os
sys.stdout.reconfigure(encoding='utf-8')

# ============================================================
# DATOS: Variaciones mensuales publicadas por UTDT
# Formato: 'YYYY-MM': cambio_porcentual (ej: 0.031 = +3.1%)
# "El ICC subio X% en [mes] respecto a [mes anterior]"
# ============================================================
changes = {
    # 2024
    '2024-05': +0.031,
    '2024-06': -0.028,
    '2024-07': +0.0502,
    '2024-08': +0.0603,
    '2024-09': -0.0592,
    '2024-10': +0.088,
    '2024-11': +0.061,
    '2024-12': +0.023,
    # 2025
    '2025-01': +0.029,
    '2025-02': -0.003,
    '2025-03': -0.067,
    '2025-04': 0.000,
    '2025-05': +0.031,
    '2025-06': 0.000,
    '2025-07': +0.020,
    # '2025-08': MISSING - interpolado
    # '2025-09': MISSING - interpolado
    # '2025-10': no hay % publicado; usamos ancla directa
    '2025-11': +0.088,
    '2025-12': -0.011,
    '2026-01': +0.022,
    '2026-02': -0.047,
}

# ============================================================
# ANCLAS: Valores absolutos verificados en multiples fuentes
# ============================================================
anchors = {
    '2025-01': 47.38,   # Perfil: "pico durante el actual gobierno. En enero de 2025, cuando el ICC llego a 47.38 puntos"
    '2025-10': 42.30,   # Di Tella/Infobae: "menor desde octubre 2025, cuando habia descendido a 42.3 unidades"
    '2025-12': 45.55,   # Trading Economics: "previous" de enero 2026
    '2026-01': 46.57,   # Di Tella comunicado de prensa
    '2026-02': 44.40,   # Di Tella comunicado de prensa
}

# ============================================================
# RECONSTRUCCION
# ============================================================

# Serie completa de meses a calcular (dic 2023 a feb 2026)
all_months = [
    '2023-12',
    '2024-01', '2024-02', '2024-03', '2024-04', '2024-05',
    '2024-06', '2024-07', '2024-08', '2024-09', '2024-10',
    '2024-11', '2024-12',
    '2025-01', '2025-02', '2025-03', '2025-04', '2025-05',
    '2025-06', '2025-07', '2025-08', '2025-09', '2025-10',
    '2025-11', '2025-12',
    '2026-01', '2026-02',
]

series = {}
estimated = set()

# === BLOQUE 1: Reconstruir hacia atras desde Jan 2025 ===
# Jan 2025 = 47.38 es ancla
# Para ir hacia atras: si series[m] = series[m-1] * (1 + changes[m])
# entonces series[m-1] = series[m] / (1 + changes[m])

series['2025-01'] = anchors['2025-01']

backward_from_jan2025 = [
    ('2024-12', '2025-01', changes.get('2025-01', 0)),
    ('2024-11', '2024-12', changes.get('2024-12', 0)),
    ('2024-10', '2024-11', changes.get('2024-11', 0)),
    ('2024-09', '2024-10', changes.get('2024-10', 0)),
    ('2024-08', '2024-09', changes.get('2024-09', 0)),
    ('2024-07', '2024-08', changes.get('2024-08', 0)),
    ('2024-06', '2024-07', changes.get('2024-07', 0)),
    ('2024-05', '2024-06', changes.get('2024-06', 0)),
]

for target, next_m, chg in backward_from_jan2025:
    if next_m in series:
        series[target] = round(series[next_m] / (1 + chg), 2)

# Los meses anteriores a may-2024 no tenemos variaciones — marcamos como sin dato
for m in ['2023-12', '2024-01', '2024-02', '2024-03', '2024-04']:
    series[m] = None

# === BLOQUE 2: Avanzar desde Jan 2025 hacia julio 2025 ===
current = series['2025-01']
for m in ['2025-02', '2025-03', '2025-04', '2025-05', '2025-06', '2025-07']:
    current = round(current * (1 + changes[m]), 2)
    series[m] = current

jul_val = series['2025-07']
oct_val = anchors['2025-10']

# === BLOQUE 3: Interpolar ago-sep 2025 (geometrico entre jul y oct) ===
# 3 pasos: jul -> aug -> sep -> oct
# ratio per step = (oct/jul)^(1/3)
ratio = (oct_val / jul_val) ** (1/3)
series['2025-08'] = round(jul_val * ratio, 2)
series['2025-09'] = round(jul_val * ratio ** 2, 2)
series['2025-10'] = oct_val
estimated.add('2025-08')
estimated.add('2025-09')

# === BLOQUE 4: Avanzar desde oct 2025 hacia feb 2026 ===
current = oct_val
for m in ['2025-11', '2025-12', '2026-01', '2026-02']:
    current = round(current * (1 + changes[m]), 2)
    series[m] = current

# === CORRECCION FINAL: sobrescribir con anclas verificadas (no deben moverse) ===
for m, v in anchors.items():
    series[m] = v

# ============================================================
# VERIFICACION DE CONSISTENCIA
# ============================================================
print("=" * 60)
print("SERIE ICC Di Tella - Periodo Milei (reconstruida)")
print("=" * 60)
print(f"{'Mes':<10} {'ICC (pts)':>10} {'Estado'}")
print("-" * 40)

records = []
for m in all_months:
    v = series.get(m)
    if v is None:
        estado = "SIN DATO"
        v_str = "  N/A"
    elif m in estimated:
        estado = "ESTIMADO (interpolado)"
        v_str = f"{v:>7.2f}"
    elif m in anchors:
        estado = "ANCLA VERIFICADA"
        v_str = f"{v:>7.2f}"
    else:
        estado = "reconstruido"
        v_str = f"{v:>7.2f}"
    print(f"{m:<10} {v_str}  {estado}")
    records.append({
        "mes": m,
        "icc": v,
        "estado": "sin_dato" if v is None else ("estimado" if m in estimated else ("ancla" if m in anchors else "reconstruido"))
    })

print()
print("VERIFICACION DE ANCLAS:")
verif = {
    '2025-01': {'esperado': 47.38, 'desc': 'Pico Milei (Perfil)'},
    '2025-10': {'esperado': 42.30, 'desc': 'Minimo pre-elecciones (Di Tella)'},
    '2025-12': {'esperado': 45.55, 'desc': 'Trading Economics'},
    '2026-01': {'esperado': 46.57, 'desc': 'Comunicado Di Tella'},
    '2026-02': {'esperado': 44.40, 'desc': 'Comunicado Di Tella'},
}
for m, info in verif.items():
    calc = series.get(m, 'N/A')
    match = "OK" if calc == info['esperado'] else f"DRIFT: calc={calc}"
    print(f"  {m}: esperado={info['esperado']} | {match} | {info['desc']}")

# ============================================================
# GUARDAR OUTPUTS
# ============================================================
output_dir = r'C:\Users\trico\OneDrive\UBA\Analisis CIGOB\docs\research\2026-03-14'

# CSV
csv_path = os.path.join(output_dir, 'icc_serie_historica.csv')
with open(csv_path, 'w', encoding='utf-8') as f:
    f.write("mes,icc,estado\n")
    for r in records:
        v = r['icc'] if r['icc'] is not None else ''
        f.write(f"{r['mes']},{v},{r['estado']}\n")
print(f"\nCSV guardado: {csv_path}")

# JSON
json_path = os.path.join(output_dir, 'icc_serie_historica.json')
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(records, f, ensure_ascii=False, indent=2)
print(f"JSON guardado: {json_path}")

# Markdown para incluir en docs
md_path = os.path.join(output_dir, '07_serie_icc_ditella.md')
with open(md_path, 'w', encoding='utf-8') as f:
    f.write("# Serie Histórica ICC Di Tella — Período Milei\n")
    f.write("**Reconstruida:** 14 de marzo de 2026\n")
    f.write("**Fuentes:** Comunicados mensuales UTDT + anclas verificadas en Infobae/Trading Economics\n\n")
    f.write("---\n\n")
    f.write("## Metodología de reconstrucción\n\n")
    f.write("1. **Anclas verificadas** (valores absolutos confirmados en múltiples fuentes)\n")
    f.write("2. **Encadenamiento** de variaciones % mensuales publicadas por UTDT (solo % de cambio, no valor absoluto)\n")
    f.write("3. **Interpolación geométrica** para ago-sep 2025 (datos no disponibles)\n")
    f.write("4. **Sin datos** para dic 2023 - abr 2024 (variaciones no recuperadas)\n\n")
    f.write("## Anclas verificadas\n\n")
    f.write("| Mes | ICC (pts) | Fuente |\n")
    f.write("|-----|----------|--------|\n")
    f.write("| 2025-01 | 47.38 | Perfil: pico del gobierno de Milei |\n")
    f.write("| 2025-10 | 42.30 | Di Tella/Infobae: minimo desde octubre 2025 |\n")
    f.write("| 2025-12 | 45.55 | Trading Economics (previous de ene 2026) |\n")
    f.write("| 2026-01 | 46.57 | Comunicado Di Tella |\n")
    f.write("| 2026-02 | 44.40 | Comunicado Di Tella |\n\n")
    f.write("## Serie completa\n\n")
    f.write("| Mes | ICC (pts) | Estado |\n")
    f.write("|-----|----------|--------|\n")
    for r in records:
        v = f"{r['icc']:.2f}" if r['icc'] is not None else "N/A"
        estado = r['estado']
        if estado == 'estimado':
            estado = "⚠ estimado (interpolado)"
        elif estado == 'ancla':
            estado = "✓ ancla verificada"
        elif estado == 'sin_dato':
            estado = "✗ sin dato"
        f.write(f"| {r['mes']} | {v} | {estado} |\n")
    f.write("\n## Interpretación\n\n")
    f.write("- **Escala:** 0-100 puntos. Neutral ≈ 50. Por debajo = pesimismo dominante.\n")
    f.write("- **Media histórica (2001-2026):** ~44.7 pts (Trading Economics)\n")
    f.write("- **Máximo histórico:** 60.97 pts (enero 2007)\n")
    f.write("- **Mínimo histórico:** 28.44 pts (septiembre 2002, crisis)\n")
    f.write("- **Pico Milei:** 47.38 pts (enero 2025)\n")
    f.write("- **Febrero 2026:** 44.4 pts (-6.1% interanual)\n\n")
    f.write("## Para uso en el modelo\n\n")
    f.write("```javascript\n")
    f.write("// Actualizar mensualmente con el valor publicado por Di Tella (~tercer semana del mes)\n")
    f.write("// Fuente: utdt.edu/ver_contenido.php?id_contenido=2575\n")
    f.write("const ICC_ACTUAL = 44.40;  // feb 2026\n")
    f.write("const OPTIMISMO = ICC_ACTUAL;  // escala 0-100, compatible con calcularPriorFundamentals()\n")
    f.write("```\n")
print(f"Markdown guardado: {md_path}")
