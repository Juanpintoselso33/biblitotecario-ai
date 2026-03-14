import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\Users\trico\OneDrive\UBA\Analisis CIGOB\web\votometro.html'
with open(path, encoding='utf-8') as f:
    c = f.read()
orig = len(c)
done = []

def replace(old, new, label):
    global c
    if old in c:
        c = c.replace(old, new, 1)
        done.append(f'OK  {label}')
    else:
        done.append(f'FAIL {label}  — string not found')

# ─────────────────────────────────────────────────────────────────────────────
# BLOQUE 1 — Agregar campo `url` a cada objeto en encuestasRaw
# Estrategia: reemplazar la parte final de cada objeto (antes del cierre `}`)
# usando la subcadena única de fecha+consultora como ancla.
# ─────────────────────────────────────────────────────────────────────────────

# ── GIACOBBE (todos) ─────────────────────────────────────────────────────────
# URL: https://www.giacobbeconsultora.com.ar/encuestas

replace(
    "{ fecha:'2023-12-15', consultora:'Giacobbe',         LLA:46.5, PJ:28.0, PRO:9.0,  PU:3.0, FIT:5.0, OTROS:8.5,  muestra:1800, tipo:'espacio',   calidad:'C' }",
    "{ fecha:'2023-12-15', consultora:'Giacobbe',         LLA:46.5, PJ:28.0, PRO:9.0,  PU:3.0, FIT:5.0, OTROS:8.5,  muestra:1800, tipo:'espacio',   calidad:'C', url:'https://www.giacobbeconsultora.com.ar/encuestas' }",
    "Giacobbe 2023-12-15 → url"
)

replace(
    "{ fecha:'2024-01-12', consultora:'Giacobbe',         LLA:44.0, PJ:29.5, PRO:8.5,  PU:3.0, FIT:5.5, OTROS:9.5,  muestra:1800, tipo:'espacio',   calidad:'C' }",
    "{ fecha:'2024-01-12', consultora:'Giacobbe',         LLA:44.0, PJ:29.5, PRO:8.5,  PU:3.0, FIT:5.5, OTROS:9.5,  muestra:1800, tipo:'espacio',   calidad:'C', url:'https://www.giacobbeconsultora.com.ar/encuestas' }",
    "Giacobbe 2024-01-12 → url"
)

replace(
    "{ fecha:'2024-02-22', consultora:'Giacobbe',         LLA:41.0, PJ:31.0, PRO:8.5,  PU:3.5, FIT:6.0, OTROS:10.0, muestra:1800, tipo:'espacio',   calidad:'C' }",
    "{ fecha:'2024-02-22', consultora:'Giacobbe',         LLA:41.0, PJ:31.0, PRO:8.5,  PU:3.5, FIT:6.0, OTROS:10.0, muestra:1800, tipo:'espacio',   calidad:'C', url:'https://www.giacobbeconsultora.com.ar/encuestas' }",
    "Giacobbe 2024-02-22 → url"
)

replace(
    "{ fecha:'2024-03-20', consultora:'Giacobbe',         LLA:39.5, PJ:32.5, PRO:8.5,  PU:3.5, FIT:6.0, OTROS:10.0, muestra:1800, tipo:'espacio',   calidad:'C' }",
    "{ fecha:'2024-03-20', consultora:'Giacobbe',         LLA:39.5, PJ:32.5, PRO:8.5,  PU:3.5, FIT:6.0, OTROS:10.0, muestra:1800, tipo:'espacio',   calidad:'C', url:'https://www.giacobbeconsultora.com.ar/encuestas' }",
    "Giacobbe 2024-03-20 → url"
)

replace(
    "{ fecha:'2024-04-18', consultora:'Giacobbe',         LLA:40.5, PJ:31.5, PRO:8.5,  PU:3.5, FIT:6.0, OTROS:10.0, muestra:2500, tipo:'espacio',   calidad:'C' }",
    "{ fecha:'2024-04-18', consultora:'Giacobbe',         LLA:40.5, PJ:31.5, PRO:8.5,  PU:3.5, FIT:6.0, OTROS:10.0, muestra:2500, tipo:'espacio',   calidad:'C', url:'https://www.giacobbeconsultora.com.ar/encuestas' }",
    "Giacobbe 2024-04-18 → url"
)

replace(
    "{ fecha:'2024-05-08', consultora:'Giacobbe',         LLA:41.5, PJ:31.0, PRO:9.0,  PU:3.5, FIT:5.5, OTROS:9.5,  muestra:2500, tipo:'espacio',   calidad:'B' }",
    "{ fecha:'2024-05-08', consultora:'Giacobbe',         LLA:41.5, PJ:31.0, PRO:9.0,  PU:3.5, FIT:5.5, OTROS:9.5,  muestra:2500, tipo:'espacio',   calidad:'B', url:'https://www.giacobbeconsultora.com.ar/encuestas' }",
    "Giacobbe 2024-05-08 → url"
)

replace(
    "{ fecha:'2024-06-12', consultora:'Giacobbe',         LLA:40.5, PJ:31.0, PRO:8.5,  PU:3.5, FIT:6.0, OTROS:10.5, muestra:2500, tipo:'espacio',   calidad:'B' }",
    "{ fecha:'2024-06-12', consultora:'Giacobbe',         LLA:40.5, PJ:31.0, PRO:8.5,  PU:3.5, FIT:6.0, OTROS:10.5, muestra:2500, tipo:'espacio',   calidad:'B', url:'https://www.giacobbeconsultora.com.ar/encuestas' }",
    "Giacobbe 2024-06-12 → url"
)

replace(
    "{ fecha:'2024-07-10', consultora:'Giacobbe',         LLA:39.5, PJ:32.0, PRO:8.5,  PU:3.5, FIT:6.0, OTROS:10.5, muestra:2500, tipo:'espacio',   calidad:'C' }",
    "{ fecha:'2024-07-10', consultora:'Giacobbe',         LLA:39.5, PJ:32.0, PRO:8.5,  PU:3.5, FIT:6.0, OTROS:10.5, muestra:2500, tipo:'espacio',   calidad:'C', url:'https://www.giacobbeconsultora.com.ar/encuestas' }",
    "Giacobbe 2024-07-10 → url"
)

replace(
    "{ fecha:'2024-08-08', consultora:'Giacobbe',         LLA:38.5, PJ:32.5, PRO:8.5,  PU:4.0, FIT:6.5, OTROS:10.0, muestra:2500, tipo:'espacio',   calidad:'C' }",
    "{ fecha:'2024-08-08', consultora:'Giacobbe',         LLA:38.5, PJ:32.5, PRO:8.5,  PU:4.0, FIT:6.5, OTROS:10.0, muestra:2500, tipo:'espacio',   calidad:'C', url:'https://www.giacobbeconsultora.com.ar/encuestas' }",
    "Giacobbe 2024-08-08 → url"
)

replace(
    "{ fecha:'2024-09-10', consultora:'Giacobbe',         LLA:37.0, PJ:33.5, PRO:8.5,  PU:4.0, FIT:6.5, OTROS:10.5, muestra:2500, tipo:'espacio',   calidad:'C' }",
    "{ fecha:'2024-09-10', consultora:'Giacobbe',         LLA:37.0, PJ:33.5, PRO:8.5,  PU:4.0, FIT:6.5, OTROS:10.5, muestra:2500, tipo:'espacio',   calidad:'C', url:'https://www.giacobbeconsultora.com.ar/encuestas' }",
    "Giacobbe 2024-09-10 → url"
)

replace(
    "{ fecha:'2024-10-10', consultora:'Giacobbe',         LLA:37.5, PJ:33.0, PRO:8.5,  PU:4.0, FIT:6.5, OTROS:10.5, muestra:2500, tipo:'espacio',   calidad:'C' }",
    "{ fecha:'2024-10-10', consultora:'Giacobbe',         LLA:37.5, PJ:33.0, PRO:8.5,  PU:4.0, FIT:6.5, OTROS:10.5, muestra:2500, tipo:'espacio',   calidad:'C', url:'https://www.giacobbeconsultora.com.ar/encuestas' }",
    "Giacobbe 2024-10-10 → url"
)

replace(
    "{ fecha:'2024-11-10', consultora:'Giacobbe',         LLA:38.5, PJ:32.5, PRO:8.5,  PU:4.0, FIT:6.5, OTROS:10.0, muestra:2500, tipo:'espacio',   calidad:'C' }",
    "{ fecha:'2024-11-10', consultora:'Giacobbe',         LLA:38.5, PJ:32.5, PRO:8.5,  PU:4.0, FIT:6.5, OTROS:10.0, muestra:2500, tipo:'espacio',   calidad:'C', url:'https://www.giacobbeconsultora.com.ar/encuestas' }",
    "Giacobbe 2024-11-10 → url"
)

replace(
    "{ fecha:'2024-12-15', consultora:'Giacobbe',         LLA:39.0, PJ:31.5, PRO:8.5,  PU:4.0, FIT:6.0, OTROS:11.0, muestra:2500, tipo:'espacio',   calidad:'B' }",
    "{ fecha:'2024-12-15', consultora:'Giacobbe',         LLA:39.0, PJ:31.5, PRO:8.5,  PU:4.0, FIT:6.0, OTROS:11.0, muestra:2500, tipo:'espacio',   calidad:'B', url:'https://www.giacobbeconsultora.com.ar/encuestas' }",
    "Giacobbe 2024-12-15 → url"
)

replace(
    "{ fecha:'2025-01-22', consultora:'Giacobbe',         LLA:40.5, PJ:30.5, PRO:8.0,  PU:4.0, FIT:6.0, OTROS:11.0, muestra:2500, tipo:'espacio',   calidad:'C' }",
    "{ fecha:'2025-01-22', consultora:'Giacobbe',         LLA:40.5, PJ:30.5, PRO:8.0,  PU:4.0, FIT:6.0, OTROS:11.0, muestra:2500, tipo:'espacio',   calidad:'C', url:'https://www.giacobbeconsultora.com.ar/encuestas' }",
    "Giacobbe 2025-01-22 → url"
)

replace(
    "{ fecha:'2025-02-08', consultora:'Giacobbe',         LLA:41.0, PJ:30.0, PRO:8.0,  PU:4.0, FIT:6.0, OTROS:11.0, muestra:2500, tipo:'espacio',   calidad:'C' }",
    "{ fecha:'2025-02-08', consultora:'Giacobbe',         LLA:41.0, PJ:30.0, PRO:8.0,  PU:4.0, FIT:6.0, OTROS:11.0, muestra:2500, tipo:'espacio',   calidad:'C', url:'https://www.giacobbeconsultora.com.ar/encuestas' }",
    "Giacobbe 2025-02-08 → url"
)

replace(
    "{ fecha:'2025-03-12', consultora:'Giacobbe',         LLA:42.0, PJ:29.5, PRO:8.0,  PU:4.5, FIT:5.5, OTROS:10.5, muestra:2500, tipo:'espacio',   calidad:'C' }",
    "{ fecha:'2025-03-12', consultora:'Giacobbe',         LLA:42.0, PJ:29.5, PRO:8.0,  PU:4.5, FIT:5.5, OTROS:10.5, muestra:2500, tipo:'espacio',   calidad:'C', url:'https://www.giacobbeconsultora.com.ar/encuestas' }",
    "Giacobbe 2025-03-12 → url"
)

replace(
    "{ fecha:'2025-04-10', consultora:'Giacobbe',         LLA:42.5, PJ:29.0, PRO:8.0,  PU:4.5, FIT:5.5, OTROS:10.5, muestra:2500, tipo:'espacio',   calidad:'C' }",
    "{ fecha:'2025-04-10', consultora:'Giacobbe',         LLA:42.5, PJ:29.0, PRO:8.0,  PU:4.5, FIT:5.5, OTROS:10.5, muestra:2500, tipo:'espacio',   calidad:'C', url:'https://www.giacobbeconsultora.com.ar/encuestas' }",
    "Giacobbe 2025-04-10 → url"
)

replace(
    "{ fecha:'2025-05-12', consultora:'Giacobbe',         LLA:41.5, PJ:30.0, PRO:8.0,  PU:4.5, FIT:5.5, OTROS:10.5, muestra:2500, tipo:'espacio',   calidad:'C' }",
    "{ fecha:'2025-05-12', consultora:'Giacobbe',         LLA:41.5, PJ:30.0, PRO:8.0,  PU:4.5, FIT:5.5, OTROS:10.5, muestra:2500, tipo:'espacio',   calidad:'C', url:'https://www.giacobbeconsultora.com.ar/encuestas' }",
    "Giacobbe 2025-05-12 → url"
)

replace(
    "{ fecha:'2025-06-10', consultora:'Giacobbe',         LLA:42.0, PJ:28.0, PRO:8.5,  PU:4.5, FIT:6.0, OTROS:11.0, muestra:2500, tipo:'espacio',   calidad:'A' }",
    "{ fecha:'2025-06-10', consultora:'Giacobbe',         LLA:42.0, PJ:28.0, PRO:8.5,  PU:4.5, FIT:6.0, OTROS:11.0, muestra:2500, tipo:'espacio',   calidad:'A', url:'https://www.giacobbeconsultora.com.ar/encuestas' }",
    "Giacobbe 2025-06-10 → url"
)

replace(
    "{ fecha:'2025-07-10', consultora:'Giacobbe',         LLA:40.2, PJ:31.3, PRO:6.7,  PU:4.5, FIT:5.5, OTROS:11.8, muestra:2500, tipo:'espacio',   calidad:'A' }",
    "{ fecha:'2025-07-10', consultora:'Giacobbe',         LLA:40.2, PJ:31.3, PRO:6.7,  PU:4.5, FIT:5.5, OTROS:11.8, muestra:2500, tipo:'espacio',   calidad:'A', url:'https://www.giacobbeconsultora.com.ar/encuestas' }",
    "Giacobbe 2025-07-10 → url"
)

replace(
    "{ fecha:'2025-08-10', consultora:'Giacobbe',         LLA:40.5, PJ:31.0, PRO:6.5,  PU:5.0, FIT:5.5, OTROS:11.5, muestra:2500, tipo:'espacio',   calidad:'B' }",
    "{ fecha:'2025-08-10', consultora:'Giacobbe',         LLA:40.5, PJ:31.0, PRO:6.5,  PU:5.0, FIT:5.5, OTROS:11.5, muestra:2500, tipo:'espacio',   calidad:'B', url:'https://www.giacobbeconsultora.com.ar/encuestas' }",
    "Giacobbe 2025-08-10 → url"
)

# Brief says "Giacobbe 2025-09-10" — actual entry is Giacobbe 2025-09-18
replace(
    "{ fecha:'2025-09-18', consultora:'Giacobbe',         LLA:40.9, PJ:31.2, PRO:7.0,  PU:4.5, FIT:5.5, OTROS:10.9, muestra:2500, tipo:'espacio',   calidad:'B' }",
    "{ fecha:'2025-09-18', consultora:'Giacobbe',         LLA:40.9, PJ:31.2, PRO:7.0,  PU:4.5, FIT:5.5, OTROS:10.9, muestra:2500, tipo:'espacio',   calidad:'B', url:'https://www.giacobbeconsultora.com.ar/encuestas' }",
    "Giacobbe 2025-09-18 → url (brief ref: 2025-09-10)"
)

# Brief says "Giacobbe 2025-10-15" — EXISTS
replace(
    "{ fecha:'2025-10-15', consultora:'Giacobbe',         LLA:40.5, PJ:30.8, PRO:6.8,  PU:4.5, FIT:5.5, OTROS:11.9, muestra:2500, tipo:'espacio',   calidad:'A' }",
    "{ fecha:'2025-10-15', consultora:'Giacobbe',         LLA:40.5, PJ:30.8, PRO:6.8,  PU:4.5, FIT:5.5, OTROS:11.9, muestra:2500, tipo:'espacio',   calidad:'A', url:'https://www.giacobbeconsultora.com.ar/encuestas' }",
    "Giacobbe 2025-10-15 → url"
)

replace(
    "{ fecha:'2025-12-20', consultora:'Giacobbe',         LLA:40.0, PJ:28.0, PRO:7.0,  PU:5.5, FIT:4.5, OTROS:15.0, muestra:1800, tipo:'espacio',   calidad:'B' }",
    "{ fecha:'2025-12-20', consultora:'Giacobbe',         LLA:40.0, PJ:28.0, PRO:7.0,  PU:5.5, FIT:4.5, OTROS:15.0, muestra:1800, tipo:'espacio',   calidad:'B', url:'https://www.giacobbeconsultora.com.ar/encuestas' }",
    "Giacobbe 2025-12-20 → url"
)

# Brief says "Giacobbe 2026-01-15" — no such entry; skipped (no match)
# Brief says "Giacobbe 2026-02-10" — actual entry is Giacobbe 2026-02-12
replace(
    "{ fecha:'2026-02-12', consultora:'Giacobbe',         LLA:42.5, PJ:29.5, PRO:6.5,  PU:4.5, FIT:4.0, OTROS:13.0, muestra:1800, tipo:'espacio',   calidad:'B' }",
    "{ fecha:'2026-02-12', consultora:'Giacobbe',         LLA:42.5, PJ:29.5, PRO:6.5,  PU:4.5, FIT:4.0, OTROS:13.0, muestra:1800, tipo:'espacio',   calidad:'B', url:'https://www.giacobbeconsultora.com.ar/encuestas' }",
    "Giacobbe 2026-02-12 → url (brief ref: 2026-02-10)"
)

# Brief says "Giacobbe 2026-03-01" — EXISTS
replace(
    "{ fecha:'2026-03-01', consultora:'Giacobbe',         LLA:42.0, PJ:29.5, PRO:6.5,  PU:4.5, FIT:4.0, OTROS:13.5, muestra:1800, tipo:'espacio',   calidad:'B' }",
    "{ fecha:'2026-03-01', consultora:'Giacobbe',         LLA:42.0, PJ:29.5, PRO:6.5,  PU:4.5, FIT:4.0, OTROS:13.5, muestra:1800, tipo:'espacio',   calidad:'B', url:'https://www.giacobbeconsultora.com.ar/encuestas' }",
    "Giacobbe 2026-03-01 → url"
)

# ── TRENDS (todos) ────────────────────────────────────────────────────────────
# URL: https://www.trendsarg.com.ar

replace(
    "{ fecha:'2025-03-28', consultora:'Trends',           LLA:41.0, PJ:31.5, PRO:7.5,  PU:4.5, FIT:5.5, OTROS:10.0, muestra:2000, tipo:'espacio',   calidad:'C' }",
    "{ fecha:'2025-03-28', consultora:'Trends',           LLA:41.0, PJ:31.5, PRO:7.5,  PU:4.5, FIT:5.5, OTROS:10.0, muestra:2000, tipo:'espacio',   calidad:'C', url:'https://www.trendsarg.com.ar' }",
    "Trends 2025-03-28 → url"
)

replace(
    "{ fecha:'2025-05-28', consultora:'Trends',           LLA:40.0, PJ:32.0, PRO:7.5,  PU:5.0, FIT:5.5, OTROS:10.0, muestra:2000, tipo:'espacio',   calidad:'C' }",
    "{ fecha:'2025-05-28', consultora:'Trends',           LLA:40.0, PJ:32.0, PRO:7.5,  PU:5.0, FIT:5.5, OTROS:10.0, muestra:2000, tipo:'espacio',   calidad:'C', url:'https://www.trendsarg.com.ar' }",
    "Trends 2025-05-28 → url"
)

replace(
    "{ fecha:'2025-06-25', consultora:'Trends',           LLA:40.5, PJ:31.0, PRO:7.5,  PU:5.0, FIT:5.5, OTROS:10.5, muestra:2000, tipo:'espacio',   calidad:'C' }",
    "{ fecha:'2025-06-25', consultora:'Trends',           LLA:40.5, PJ:31.0, PRO:7.5,  PU:5.0, FIT:5.5, OTROS:10.5, muestra:2000, tipo:'espacio',   calidad:'C', url:'https://www.trendsarg.com.ar' }",
    "Trends 2025-06-25 → url"
)

replace(
    "{ fecha:'2025-07-25', consultora:'Trends',           LLA:40.0, PJ:31.0, PRO:7.0,  PU:5.0, FIT:5.0, OTROS:12.0, muestra:2000, tipo:'espacio',   calidad:'B' }",
    "{ fecha:'2025-07-25', consultora:'Trends',           LLA:40.0, PJ:31.0, PRO:7.0,  PU:5.0, FIT:5.0, OTROS:12.0, muestra:2000, tipo:'espacio',   calidad:'B', url:'https://www.trendsarg.com.ar' }",
    "Trends 2025-07-25 → url"
)

replace(
    "{ fecha:'2025-09-28', consultora:'Trends',           LLA:39.0, PJ:33.0, PRO:7.0,  PU:5.0, FIT:5.5, OTROS:10.5, muestra:2000, tipo:'espacio',   calidad:'C' }",
    "{ fecha:'2025-09-28', consultora:'Trends',           LLA:39.0, PJ:33.0, PRO:7.0,  PU:5.0, FIT:5.5, OTROS:10.5, muestra:2000, tipo:'espacio',   calidad:'C', url:'https://www.trendsarg.com.ar' }",
    "Trends 2025-09-28 → url"
)

replace(
    "{ fecha:'2025-12-14', consultora:'Trends',           LLA:43.0, PJ:33.0, PRO:4.0,  PU:4.0, FIT:3.0, OTROS:13.0, muestra:2000, tipo:'espacio',   calidad:'A' }",
    "{ fecha:'2025-12-14', consultora:'Trends',           LLA:43.0, PJ:33.0, PRO:4.0,  PU:4.0, FIT:3.0, OTROS:13.0, muestra:2000, tipo:'espacio',   calidad:'A', url:'https://www.trendsarg.com.ar' }",
    "Trends 2025-12-14 → url"
)

# Brief says "Trends 2026-01-16" — EXISTS
replace(
    "{ fecha:'2026-01-16', consultora:'Trends',           LLA:43.0, PJ:32.0, PRO:4.0,  PU:4.0, FIT:3.0, OTROS:14.0, muestra:2000, tipo:'espacio',   calidad:'A' }",
    "{ fecha:'2026-01-16', consultora:'Trends',           LLA:43.0, PJ:32.0, PRO:4.0,  PU:4.0, FIT:3.0, OTROS:14.0, muestra:2000, tipo:'espacio',   calidad:'A', url:'https://www.trendsarg.com.ar' }",
    "Trends 2026-01-16 → url"
)

replace(
    "{ fecha:'2026-02-24', consultora:'Trends',           LLA:43.0, PJ:31.0, PRO:5.0,  PU:4.5, FIT:3.5, OTROS:13.0, muestra:2000, tipo:'espacio',   calidad:'B' }",
    "{ fecha:'2026-02-24', consultora:'Trends',           LLA:43.0, PJ:31.0, PRO:5.0,  PU:4.5, FIT:3.5, OTROS:13.0, muestra:2000, tipo:'espacio',   calidad:'B', url:'https://www.trendsarg.com.ar' }",
    "Trends 2026-02-24 → url"
)

# ── MANAGEMENT & FIT ─────────────────────────────────────────────────────────
# URL: https://www.managementfit.com.ar
# Brief says "Management & Fit 2026-01-20" — file has Opinaia 2026-01-20, not M&F.
# Applying URL to all Management & Fit entries.

replace(
    "{ fecha:'2024-01-20', consultora:'Management & Fit', LLA:43.5, PJ:30.0, PRO:8.0,  PU:3.5, FIT:5.0, OTROS:10.0, muestra:1500, tipo:'espacio',   calidad:'C' }",
    "{ fecha:'2024-01-20', consultora:'Management & Fit', LLA:43.5, PJ:30.0, PRO:8.0,  PU:3.5, FIT:5.0, OTROS:10.0, muestra:1500, tipo:'espacio',   calidad:'C', url:'https://www.managementfit.com.ar' }",
    "Management & Fit 2024-01-20 → url"
)

replace(
    "{ fecha:'2024-05-15', consultora:'Management & Fit', LLA:40.0, PJ:31.5, PRO:8.5,  PU:3.5, FIT:6.0, OTROS:10.5, muestra:1500, tipo:'espacio',   calidad:'C' }",
    "{ fecha:'2024-05-15', consultora:'Management & Fit', LLA:40.0, PJ:31.5, PRO:8.5,  PU:3.5, FIT:6.0, OTROS:10.5, muestra:1500, tipo:'espacio',   calidad:'C', url:'https://www.managementfit.com.ar' }",
    "Management & Fit 2024-05-15 → url"
)

replace(
    "{ fecha:'2024-08-20', consultora:'Management & Fit', LLA:37.5, PJ:33.0, PRO:8.5,  PU:4.0, FIT:6.5, OTROS:10.5, muestra:1500, tipo:'espacio',   calidad:'C' }",
    "{ fecha:'2024-08-20', consultora:'Management & Fit', LLA:37.5, PJ:33.0, PRO:8.5,  PU:4.0, FIT:6.5, OTROS:10.5, muestra:1500, tipo:'espacio',   calidad:'C', url:'https://www.managementfit.com.ar' }",
    "Management & Fit 2024-08-20 → url"
)

replace(
    "{ fecha:'2024-11-20', consultora:'Management & Fit', LLA:38.0, PJ:32.0, PRO:9.0,  PU:4.0, FIT:6.0, OTROS:11.0, muestra:1500, tipo:'espacio',   calidad:'C' }",
    "{ fecha:'2024-11-20', consultora:'Management & Fit', LLA:38.0, PJ:32.0, PRO:9.0,  PU:4.0, FIT:6.0, OTROS:11.0, muestra:1500, tipo:'espacio',   calidad:'C', url:'https://www.managementfit.com.ar' }",
    "Management & Fit 2024-11-20 → url"
)

replace(
    "{ fecha:'2025-01-16', consultora:'Management & Fit', LLA:42.1, PJ:26.5, PRO:8.0,  PU:4.0, FIT:5.0, OTROS:14.4, muestra:2600, tipo:'espacio',   calidad:'A' }",
    "{ fecha:'2025-01-16', consultora:'Management & Fit', LLA:42.1, PJ:26.5, PRO:8.0,  PU:4.0, FIT:5.0, OTROS:14.4, muestra:2600, tipo:'espacio',   calidad:'A', url:'https://www.managementfit.com.ar' }",
    "Management & Fit 2025-01-16 → url"
)

replace(
    "{ fecha:'2025-04-28', consultora:'Management & Fit', LLA:41.0, PJ:31.0, PRO:7.5,  PU:4.5, FIT:5.5, OTROS:10.5, muestra:1500, tipo:'espacio',   calidad:'C' }",
    "{ fecha:'2025-04-28', consultora:'Management & Fit', LLA:41.0, PJ:31.0, PRO:7.5,  PU:4.5, FIT:5.5, OTROS:10.5, muestra:1500, tipo:'espacio',   calidad:'C', url:'https://www.managementfit.com.ar' }",
    "Management & Fit 2025-04-28 → url"
)

replace(
    "{ fecha:'2025-12-28', consultora:'Management & Fit', LLA:42.0, PJ:29.0, PRO:7.0,  PU:4.0, FIT:4.0, OTROS:14.0, muestra:1200, tipo:'espacio',   calidad:'B' }",
    "{ fecha:'2025-12-28', consultora:'Management & Fit', LLA:42.0, PJ:29.0, PRO:7.0,  PU:4.0, FIT:4.0, OTROS:14.0, muestra:1200, tipo:'espacio',   calidad:'B', url:'https://www.managementfit.com.ar' }",
    "Management & Fit 2025-12-28 → url"
)

replace(
    "{ fecha:'2026-02-15', consultora:'Management & Fit', LLA:41.0, PJ:30.5, PRO:6.0,  PU:4.5, FIT:4.0, OTROS:14.0, muestra:1500, tipo:'espacio',   calidad:'B' }",
    "{ fecha:'2026-02-15', consultora:'Management & Fit', LLA:41.0, PJ:30.5, PRO:6.0,  PU:4.5, FIT:4.0, OTROS:14.0, muestra:1500, tipo:'espacio',   calidad:'B', url:'https://www.managementfit.com.ar' }",
    "Management & Fit 2026-02-15 → url"
)

# ── ISASI BURDMAN ─────────────────────────────────────────────────────────────
# URL: https://www.isasiburdman.com.ar
# Brief says "Isasi Burdman 2026-01-30" — no such entry in file.
# Applying URL to all Isasi Burdman entries.

replace(
    "{ fecha:'2024-12-10', consultora:'Isasi Burdman',    LLA:37.0, PJ:25.0, PRO:8.0,  PU:4.0, FIT:5.0, OTROS:21.0, muestra:1722, tipo:'candidato', calidad:'A' }",
    "{ fecha:'2024-12-10', consultora:'Isasi Burdman',    LLA:37.0, PJ:25.0, PRO:8.0,  PU:4.0, FIT:5.0, OTROS:21.0, muestra:1722, tipo:'candidato', calidad:'A', url:'https://www.isasiburdman.com.ar' }",
    "Isasi Burdman 2024-12-10 → url"
)

replace(
    "{ fecha:'2025-11-15', consultora:'Isasi Burdman',    LLA:54.0, PJ:18.0, PRO:5.0,  PU:3.0, FIT:3.0, OTROS:17.0, muestra:1722, tipo:'candidato', calidad:'A' }",
    "{ fecha:'2025-11-15', consultora:'Isasi Burdman',    LLA:54.0, PJ:18.0, PRO:5.0,  PU:3.0, FIT:3.0, OTROS:17.0, muestra:1722, tipo:'candidato', calidad:'A', url:'https://www.isasiburdman.com.ar' }",
    "Isasi Burdman 2025-11-15 → url"
)

replace(
    "{ fecha:'2025-12-04', consultora:'Isasi Burdman',    LLA:52.0, PJ:18.0, PRO:5.0,  PU:3.0, FIT:3.0, OTROS:19.0, muestra:1722, tipo:'candidato', calidad:'A' }",
    "{ fecha:'2025-12-04', consultora:'Isasi Burdman',    LLA:52.0, PJ:18.0, PRO:5.0,  PU:3.0, FIT:3.0, OTROS:19.0, muestra:1722, tipo:'candidato', calidad:'A', url:'https://www.isasiburdman.com.ar' }",
    "Isasi Burdman 2025-12-04 → url"
)

# ── DC CONSULTORES ────────────────────────────────────────────────────────────
# URL: https://www.dcconsultores.com.ar
# Brief says "DC Consultores 2026-02-05" — actual entry is DC Consultores 2025-11-28.

replace(
    "{ fecha:'2025-11-28', consultora:'DC Consultores',   LLA:52.1, PJ:18.8, PRO:6.0,  PU:3.5, FIT:3.0, OTROS:16.6, muestra:1200, tipo:'candidato', calidad:'A' }",
    "{ fecha:'2025-11-28', consultora:'DC Consultores',   LLA:52.1, PJ:18.8, PRO:6.0,  PU:3.5, FIT:3.0, OTROS:16.6, muestra:1200, tipo:'candidato', calidad:'A', url:'https://www.dcconsultores.com.ar' }",
    "DC Consultores 2025-11-28 → url (brief ref: 2026-02-05)"
)

# ── SYNOPSIS ──────────────────────────────────────────────────────────────────
# URL: https://www.synopsis.com.ar
# Brief says "Synopsis 2026-02-08" — actual entry is Synopsis 2026-02-05.

replace(
    "{ fecha:'2026-02-05', consultora:'Synopsis',         LLA:42.0, PJ:31.0, PRO:5.0,  PU:4.0, FIT:4.0, OTROS:14.0, muestra:1500, tipo:'espacio',   calidad:'B' }",
    "{ fecha:'2026-02-05', consultora:'Synopsis',         LLA:42.0, PJ:31.0, PRO:5.0,  PU:4.0, FIT:4.0, OTROS:14.0, muestra:1500, tipo:'espacio',   calidad:'B', url:'https://www.synopsis.com.ar' }",
    "Synopsis 2026-02-05 → url (brief ref: 2026-02-08)"
)

# ── CB GLOBAL DATA ────────────────────────────────────────────────────────────
# URL: https://www.cbglobaldata.com.ar
# Brief says "CB Global Data 2026-02-13" — EXISTS.

replace(
    "{ fecha:'2026-02-13', consultora:'CB Global Data',   LLA:35.7, PJ:22.5, PRO:0.0,  PU:3.7, FIT:4.2, OTROS:33.9, muestra:2588, tipo:'candidato', calidad:'A' }",
    "{ fecha:'2026-02-13', consultora:'CB Global Data',   LLA:35.7, PJ:22.5, PRO:0.0,  PU:3.7, FIT:4.2, OTROS:33.9, muestra:2588, tipo:'candidato', calidad:'A', url:'https://www.cbglobaldata.com.ar' }",
    "CB Global Data 2026-02-13 → url"
)

# ─────────────────────────────────────────────────────────────────────────────
# BLOQUE 2 — Agregar columna "Fuente" al <thead> de la tabla de encuestas
# ─────────────────────────────────────────────────────────────────────────────

replace(
    "<thead><tr><th>Consultora</th><th>Fecha</th><th>LLA</th><th>PJ</th><th>Peso</th></tr></thead>",
    "<thead><tr><th>Consultora</th><th>Fecha</th><th>LLA</th><th>PJ</th><th>Peso</th><th style=\"text-align:center;\">Fuente</th></tr></thead>",
    "thead — agregar columna Fuente"
)

# ─────────────────────────────────────────────────────────────────────────────
# BLOQUE 3 — Modificar el render de filas para incluir celda de link/fuente
#
# El render actual termina con:
#   ...${(e.peso*100).toFixed(0)}%</span></td></tr>`
#
# Reemplazamos ese cierre por uno que agrega una nueva <td> con el ícono SVG
# (si e.url existe) o un guión gris (si no).
# ─────────────────────────────────────────────────────────────────────────────

# El SVG se insertará literalmente en el HTML (dentro de un template literal JS con backtick).
# Los atributos del SVG usan comillas dobles normales — sin escapes.
SVG_ICON = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" '
    'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
    'stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>'
    '<polyline points="15 3 21 3 21 9"/>'
    '<line x1="10" y1="14" x2="21" y2="3"/>'
    '</svg>'
)

# OLD_ROW_CLOSE: fin exacto de la línea de render actual (dentro del template literal JS)
OLD_ROW_CLOSE = '${(e.peso*100).toFixed(0)}%</span></td></tr>`'

# NEW_ROW_CLOSE: agrega <td> con ícono SVG (si hay url) o guión gris (si no).
# La expresión JS usada:
#   e.url
#     ? `<a href="${e.url}" target="_blank" ...>SVG</a>`
#     : '<span style="...">-</span>'
# Todo dentro del template literal externo que ya usa backtick.
# El template literal interno también usa backtick, así que hay que escapar
# el backtick interno con \` en la cadena Python (que lo escribe tal cual en el HTML).
NEW_ROW_CLOSE = (
    '${(e.peso*100).toFixed(0)}%</span></td>'
    '<td style="text-align:center;">'
    # JS ternary: si e.url → <a> con SVG; si no → guión gris.
    # Se usa comillas simples JS para el <a> (evita template literals anidados).
    # La expresión JS emitida será:
    #   ${e.url
    #     ? '<a href="' + e.url + '" target="_blank" rel="noopener" ...>SVG</a>'
    #     : '<span style="color:#9CA3AF;font-size:12px;">-</span>'}
    "${e.url"
    ' ? \'<a href="\' + e.url + \'" target="_blank" rel="noopener" '
    'title="Ver publicaci\u00f3n original" '
    'style="color:#1D4ED8;display:inline-flex;align-items:center;">'
    + SVG_ICON
    + '</a>\''
    ' : \'<span style="color:#9CA3AF;font-size:12px;">-</span>\'}'
    '</td></tr>`'
)

replace(OLD_ROW_CLOSE, NEW_ROW_CLOSE, "render fila — agregar celda Fuente con ícono SVG")

# ─────────────────────────────────────────────────────────────────────────────
# Guardar y reportar
# ─────────────────────────────────────────────────────────────────────────────

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

print('=== patch_issue8.py — resultados ===')
for d in done:
    print(f'  {d}')
print(f'\nArchivo: {len(c):,} chars  (era {orig:,} chars, delta +{len(c)-orig:,})')
