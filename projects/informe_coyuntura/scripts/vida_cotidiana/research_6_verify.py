"""Verificar URLs especificas que parecen funcionar."""
import requests, sys, time
sys.stdout.reconfigure(encoding='utf-8')
headers = {'User-Agent': 'Mozilla/5.0'}

print("=" * 80)
print("VERIFICACION DE URLs DESCARGABLES")
print("=" * 80)

# Test descargas reales con HEAD
urls_to_verify = [
    # Inseguridad
    ('SNIC pais XLSX (2025-05-21)', 'https://cloud-snic.minseg.gob.ar/Bases/SNIC/snic-pais.xlsx'),
    ('SNIC pais CSV (2025-05-21)', 'https://cloud-snic.minseg.gob.ar/Bases/SNIC/snic-pais.csv'),
    ('SNIC provincias XLSX', 'https://cloud-snic.minseg.gob.ar/Bases/SNIC/snic-provincias.xlsx'),
    ('SNIC departamentos XLSX', 'https://cloud-snic.minseg.gob.ar/Bases/SNIC/snic-departamentos-anual.xlsx'),
    ('CABA Delitos 2024 XLSX', 'https://cdn.buenosaires.gob.ar/datosabiertos/datasets/ministerio-de-justicia-y-seguridad/delitos/delitos_2024.xlsx'),
    ('CABA Delitos 2024 CSV', 'https://cdn.buenosaires.gob.ar/datosabiertos/datasets/ministerio-de-justicia-y-seguridad/delitos/delitos_2024.csv'),
    ('CABA Delitos 2025 XLSX (especulativo)', 'https://cdn.buenosaires.gob.ar/datosabiertos/datasets/ministerio-de-justicia-y-seguridad/delitos/delitos_2025.xlsx'),
    # Salud
    ('Defunciones 2023 CSV', 'http://datos.salud.gob.ar/dataset/c1643775-18e1-40fd-9e7f-0cebb5b1abe6/resource/615c454b-c02c-4011-b55a-86e8a28167bf/download/base_def_23_men.csv'),
]

for name, url in urls_to_verify:
    try:
        r = requests.head(url, headers=headers, timeout=15, allow_redirects=True)
        size = r.headers.get('content-length','?')
        last = r.headers.get('last-modified','?')
        print(f"  [{r.status_code}] {name}")
        print(f"    size={size} | last-modified={last}")
        print(f"    url={url}")
    except Exception as e:
        print(f"  ERROR {name}: {type(e).__name__}")

# CABA - buscar archivos para 2025 y 2026 (probables si actualizan rapido)
print("\n[CABA] Probing delitos_2025 / 2026 (formato URL predecible)")
for y in [2024, 2025, 2026]:
    for fmt in ['xlsx', 'csv']:
        url = f'https://cdn.buenosaires.gob.ar/datosabiertos/datasets/ministerio-de-justicia-y-seguridad/delitos/delitos_{y}.{fmt}'
        try:
            r = requests.head(url, headers=headers, timeout=10)
            print(f"  {y}.{fmt} -> HTTP {r.status_code}")
        except Exception as e:
            print(f"  {y}.{fmt} -> ERROR {type(e).__name__}")

# Min Salud - intentar via HTTP
print("\n[Min Salud] Portal datos.salud.gob.ar via HTTP (sin SSL)")
try:
    r = requests.get('http://datos.salud.gob.ar/api/3/action/package_list', timeout=20)
    print(f"  HTTP {r.status_code}")
    if r.status_code == 200:
        pkgs = r.json().get('result', [])
        print(f"  Total datasets: {len(pkgs)}")
        # Buscar los relevantes
        relevantes = [p for p in pkgs if any(k in p.lower() for k in ['mortal', 'defunc', 'vigilancia', 'cobertura', 'aps', 'atencion'])]
        print(f"  Relevantes ({len(relevantes)}):")
        for p in relevantes[:30]:
            print(f"    - {p}")
except Exception as e:
    print(f"  ERROR: {e}")

# Argentinos por la Educacion - probar API mas profunda
print("\n[ArgenPorEdu] Detalle de posts educacion (busqueda de datos)")
try:
    # buscar posts relacionados a abandono/desercion
    r = requests.get('https://argentinosporlaeducacion.org/wp-json/wp/v2/posts',
        params={'search': 'abandono', 'per_page': 5}, headers=headers, timeout=15)
    print(f"  HTTP {r.status_code}")
    if r.status_code == 200:
        posts = r.json()
        print(f"  Posts con 'abandono': {len(posts)}")
        for p in posts:
            print(f"    - {p.get('title',{}).get('rendered','')[:90]}")
            print(f"      modified: {p.get('modified','')}")
except Exception as e:
    print(f"  ERROR: {e}")

# SINIDE/RA - buscar archivos descargables especificos
print("\n[SINIDE/RA] Buscar info-estadistica del Min Educacion")
urls_edu = [
    'https://www.argentina.gob.ar/educacion/evaluacion-e-informacion-educativa/relevamiento-anual',
    'https://www.argentina.gob.ar/educacion/evaluacion-informacion-educativa',
    'https://www.argentina.gob.ar/educacion/evaluacion-informacion-educativa/sistemas-de-evaluacion',
]
for url in urls_edu:
    try:
        r = requests.get(url, headers=headers, timeout=15)
        print(f"  {url} -> {r.status_code}")
    except Exception as e:
        print(f"  ERROR: {e}")
