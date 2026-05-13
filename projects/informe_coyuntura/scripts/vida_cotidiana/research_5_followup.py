"""Follow-up: detalles especificos de las fuentes prometedoras."""
import requests, sys, time
sys.stdout.reconfigure(encoding='utf-8')
headers = {'User-Agent': 'Mozilla/5.0'}

print("=" * 80)
print("FOLLOW-UP: detalles de fuentes prometedoras")
print("=" * 80)

# 1) CABA Delitos: detalle del package y sus recursos
print("\n[1] CABA - Dataset 'Delitos' (detalle completo)")
try:
    r = requests.get('https://data.buenosaires.gob.ar/api/3/action/package_search',
        params={'q': 'delitos', 'rows': 1}, timeout=20, headers=headers)
    if r.status_code == 200:
        pkg = r.json()['result']['results'][0]
        print(f"  Title: {pkg['title']}")
        print(f"  Updated: {pkg.get('metadata_modified','')}")
        print(f"  Frequency: {pkg.get('frequency','')} | accrual: {pkg.get('accrualPeriodicity','')}")
        print(f"  Description: {pkg.get('notes','')[:300]}")
        print(f"  Recursos ({len(pkg.get('resources',[]))}):")
        for res in pkg.get('resources', []):
            print(f"    [{res.get('format','')}] {res.get('name','')[:60]}")
            print(f"      url: {res.get('url','')}")
            print(f"      last_modified: {res.get('last_modified','')}")
except Exception as e:
    print(f"  ERROR: {e}")

# 2) Defunciones Generales Mensuales - frecuencia real
print("\n[2] Defunciones Generales Mensuales - detalle")
try:
    r = requests.get('https://datos.gob.ar/api/3/action/package_search',
        params={'q': 'defunciones generales mensuales', 'rows': 1}, timeout=20)
    if r.status_code == 200:
        results = r.json()['result']['results']
        if results:
            pkg = results[0]
            print(f"  Title: {pkg['title']}")
            print(f"  Updated: {pkg.get('metadata_modified','')}")
            print(f"  Frequency: {pkg.get('frequency','')} | accrual: {pkg.get('accrualPeriodicity','')}")
            print(f"  Notes: {pkg.get('notes','')[:300]}")
            for res in pkg.get('resources', []):
                print(f"    [{res.get('format','')}] {res.get('name','')[:80]}")
                print(f"      url: {res.get('url','')}")
                print(f"      last_modified: {res.get('last_modified','')}")
except Exception as e:
    print(f"  ERROR: {e}")

# 3) Vigilancia IRA + Dengue - frecuencia
print("\n[3] Vigilancia Infecciones Respiratorias Agudas")
for q in ['vigilancia infecciones respiratorias agudas', 'vigilancia dengue zika']:
    try:
        r = requests.get('https://datos.gob.ar/api/3/action/package_search',
            params={'q': q, 'rows': 1}, timeout=20)
        if r.status_code == 200:
            results = r.json()['result']['results']
            if results:
                pkg = results[0]
                print(f"\n  >> {pkg['title']}")
                print(f"     Updated: {pkg.get('metadata_modified','')}")
                print(f"     accrual: {pkg.get('accrualPeriodicity','')}")
                for res in pkg.get('resources', [])[:5]:
                    print(f"     [{res.get('format','')}] {res.get('name','')[:70]}")
                    print(f"        url: {res.get('url','')}")
                    print(f"        modified: {res.get('last_modified','')}")
    except Exception as e:
        print(f"  ERROR: {e}")

# 4) Argentinos por la Educacion - buscar API real
print("\n[4] Argentinos por la Educacion - buscar API/Datos")
# El sitio carga datos via JS. Ver si tiene endpoint expuesto
urls = [
    'https://argentinosporlaeducacion.org/wp-json/wp/v2/posts?per_page=3',
    'https://argentinosporlaeducacion.org/wp-json/',
    'https://argentinosporlaeducacion.org/sitemap.xml',
]
for url in urls:
    try:
        r = requests.get(url, headers=headers, timeout=15)
        print(f"  {url} -> HTTP {r.status_code} | ct={r.headers.get('content-type','')[:60]}")
        if r.status_code == 200 and 'json' in r.headers.get('content-type',''):
            print(f"    Preview: {r.text[:300]}")
    except Exception as e:
        print(f"  ERROR: {e}")

# 5) Aprender 2022 detalle (es bianual)
print("\n[5] Aprender 2022 detalle")
try:
    r = requests.get('https://datos.gob.ar/api/3/action/package_search',
        params={'q': 'aprender 2022', 'rows': 1}, timeout=20)
    if r.status_code == 200:
        results = r.json()['result']['results']
        if results:
            pkg = results[0]
            print(f"  Title: {pkg['title']}")
            print(f"  Updated: {pkg.get('metadata_modified','')}")
            print(f"  accrual: {pkg.get('accrualPeriodicity','')}")
            print(f"  Notes: {pkg.get('notes','')[:300]}")
except Exception as e:
    print(f"  ERROR: {e}")

# 6) SIPA - estadisticas educativas
print("\n[6] datos.gob.ar todos los datasets de educacion (org-level)")
try:
    r = requests.get('https://datos.gob.ar/api/3/action/package_search',
        params={'q': 'organization:secretaria-de-educacion', 'rows': 15}, timeout=20)
    if r.status_code == 200:
        results = r.json()['result']['results']
        print(f"  Total encontrados: {r.json()['result'].get('count',0)}")
        for pkg in results:
            print(f"    - {pkg['title'][:80]} | upd: {pkg.get('metadata_modified','')[:10]}")
except Exception as e:
    print(f"  ERROR: {e}")

# 7) Sala de Lectura / SITEAL UNESCO
print("\n[7] SITEAL - buscar indicadores Argentina")
try:
    r = requests.get('https://siteal.iiep.unesco.org/indicadores',
        headers=headers, timeout=15)
    print(f"  HTTP {r.status_code}")
    # buscar referencias a API o JSON
    if r.status_code == 200:
        if 'application/json' in r.text or '/api/' in r.text:
            print("  Tiene referencias a API")
        print(f"  Tamaño: {len(r.text)} chars")
except Exception as e:
    print(f"  ERROR: {e}")

# 8) Min Salud - listado completo de datasets
print("\n[8] datos.salud.gob.ar - portal propio")
try:
    r = requests.get('http://datos.salud.gob.ar/api/3/action/package_list', timeout=20)
    print(f"  HTTP {r.status_code}")
    if r.status_code == 200:
        pkgs = r.json().get('result', [])
        print(f"  Total datasets en datos.salud.gob.ar: {len(pkgs)}")
        # Mostrar algunos
        for p in pkgs[:20]:
            print(f"    - {p}")
except Exception as e:
    print(f"  ERROR: {e}")
