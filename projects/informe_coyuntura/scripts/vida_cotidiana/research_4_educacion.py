"""Research 4: Desercion escolar - fuentes mas frecuentes que el Relevamiento Anual."""
import requests, sys
sys.stdout.reconfigure(encoding='utf-8')
headers = {'User-Agent': 'Mozilla/5.0'}

print("=" * 80)
print("4. DESERCION ESCOLAR / EDUCACION")
print("=" * 80)

# A) datos.gob.ar
print("\n[A] datos.gob.ar PACKAGE_SEARCH educacion")
for q in ['matricula escolar', 'desercion abandono escolar', 'educacion secundaria', 'aprendizajes pruebas', 'sinide siteal']:
    try:
        r = requests.get('https://datos.gob.ar/api/3/action/package_search',
            params={'q': q, 'rows': 5}, timeout=20)
        print(f"\n  Query '{q}' -> HTTP {r.status_code}")
        if r.status_code == 200:
            for pkg in r.json().get('result', {}).get('results', []):
                print(f"    Dataset: {pkg['title']}")
                print(f"      org: {pkg.get('organization',{}).get('title','')}")
                print(f"      updated: {pkg.get('metadata_modified','')}")
                for res in pkg.get('resources', [])[:2]:
                    print(f"      [{res.get('format','')}] {res.get('last_modified','')[:10]} {res.get('url','')[:90]}")
    except Exception as e:
        print(f"  ERROR: {e}")

# B) Ministerio Educacion / SINIDE / SITEAL
print("\n[B] URLs DIRECTAS MIN EDUCACION")
urls_edu = [
    'https://www.argentina.gob.ar/educacion/planeamiento/info-estadistica',
    'https://www.argentina.gob.ar/educacion/evaluacion-e-informacion-educativa',
    'https://datos.gob.ar/dataset/educacion-matricula-nivel-educativo',
    'https://siteal.iiep.unesco.org/',
    'https://www.argentina.gob.ar/educacion/aprender',
]
for url in urls_edu:
    try:
        r = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        print(f"  {url}")
        print(f"    -> HTTP {r.status_code} | ct={r.headers.get('content-type','')[:60]}")
    except Exception as e:
        print(f"  {url} -> ERROR {e}")

# C) Argentinos por la Educacion
print("\n[C] Argentinos por la Educacion")
urls_ape = [
    'https://argentinosporlaeducacion.org/',
    'https://argentinosporlaeducacion.org/datos/',
    'https://observatorio.argentinosporlaeducacion.org/',
    'https://cms.argentinosporlaeducacion.org/api/',
]
for url in urls_ape:
    try:
        r = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        print(f"  {url}")
        print(f"    -> HTTP {r.status_code} | final={r.url[:90]} | ct={r.headers.get('content-type','')[:60]}")
    except Exception as e:
        print(f"  {url} -> ERROR {e}")

# D) UNICEF / Observatorio de la Deuda Social (UCA)
print("\n[D] UCA-ODSA / UNICEF")
urls_uca = [
    'https://wadmin.uca.edu.ar/public/ckeditor/Observatorio%20Deuda%20Social/Documentos/',
    'https://uca.edu.ar/es/observatorio-de-la-deuda-social-argentina',
    'https://www.unicef.org/argentina/informes',
]
for url in urls_uca:
    try:
        r = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        print(f"  {url}")
        print(f"    -> HTTP {r.status_code} | ct={r.headers.get('content-type','')[:60]}")
    except Exception as e:
        print(f"  {url} -> ERROR {e}")

# E) Series INDEC - educacion
print("\n[E] Series INDEC educacion (EPH)")
for q in ['asistencia escolar', 'tasa escolarizacion', 'nivel educativo']:
    try:
        r = requests.get('https://apis.datos.gob.ar/series/api/search/',
            params={'q': q, 'limit': 5}, timeout=20)
        print(f"\n  Query '{q}' -> HTTP {r.status_code}")
        for s in r.json().get('data', []):
            f = s.get('field', {})
            print(f"    id={f.get('id','')} | end={f.get('time_index_end','')}")
            print(f"      desc: {f.get('description','')[:100]}")
    except Exception as e:
        print(f"  ERROR: {e}")
