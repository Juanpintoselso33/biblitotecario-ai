"""Research 1: Inseguridad urbana - fuentes mas frecuentes que SNIC."""
import requests, sys, json
sys.stdout.reconfigure(encoding='utf-8')
headers = {'User-Agent': 'Mozilla/5.0'}

print("=" * 80)
print("1. INSEGURIDAD URBANA")
print("=" * 80)

# A) datos.gob.ar Series API
print("\n[A] datos.gob.ar SERIES API")
for q in ['delitos hechos delictivos seguridad', 'victimizacion inseguridad urbana', 'snic estadisticas criminales']:
    try:
        r = requests.get('https://apis.datos.gob.ar/series/api/search/',
            params={'q': q, 'limit': 5}, timeout=20)
        print(f"\n  Query '{q}' -> HTTP {r.status_code}")
        data = r.json().get('data', [])
        if not data:
            print("    (sin resultados)")
        for s in data:
            f = s.get('field', {})
            print(f"    id={f.get('id','')} | end={f.get('time_index_end','')}")
            print(f"      desc: {f.get('description','')[:100]}")
    except Exception as e:
        print(f"  ERROR: {e}")

# B) datos.gob.ar package_search
print("\n[B] datos.gob.ar PACKAGE_SEARCH")
for q in ['delitos seguridad criminalidad', 'snic victimizacion', 'homicidios criminales']:
    try:
        r2 = requests.get('https://datos.gob.ar/api/3/action/package_search',
            params={'q': q, 'rows': 5}, timeout=20)
        print(f"\n  Query '{q}' -> HTTP {r2.status_code}")
        if r2.status_code == 200:
            for pkg in r2.json().get('result', {}).get('results', []):
                print(f"    Dataset: {pkg['title']}")
                print(f"      org: {pkg.get('organization',{}).get('title','')}")
                print(f"      updated: {pkg.get('metadata_modified','')}")
                for res in pkg.get('resources', [])[:3]:
                    print(f"      [{res.get('format','')}] {res.get('last_modified','')[:10]} {res.get('url','')[:90]}")
    except Exception as e:
        print(f"  ERROR: {e}")

# C) URLs directas
print("\n[C] URLs DIRECTAS")
urls_seguridad = [
    'https://www.argentina.gob.ar/seguridad/estadisticascriminales',
    'https://datos.gob.ar/dataset/seguridad-estadisticas-criminales',
    'https://datos.gob.ar/dataset/sistema-nacional-informacion-criminal',
    'https://estadisticascriminales.minseg.gob.ar/',
]
for url in urls_seguridad:
    try:
        r3 = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        print(f"  {url}")
        print(f"    -> HTTP {r3.status_code} | final={r3.url[:90]} | ct={r3.headers.get('content-type','')[:60]}")
    except Exception as e:
        print(f"  {url} -> ERROR {e}")

# D) Ciudad de Buenos Aires - tiene portal abierto BA Data
print("\n[D] CABA - portal BA Data (estadisticas frecuentes)")
try:
    r = requests.get('https://data.buenosaires.gob.ar/api/3/action/package_search',
        params={'q': 'delitos', 'rows': 5}, timeout=20, headers=headers)
    print(f"  HTTP {r.status_code}")
    if r.status_code == 200:
        for pkg in r.json().get('result', {}).get('results', []):
            print(f"    Dataset: {pkg['title']}")
            print(f"      updated: {pkg.get('metadata_modified','')}")
            for res in pkg.get('resources', [])[:3]:
                print(f"      [{res.get('format','')}] {res.get('url','')[:100]}")
except Exception as e:
    print(f"  ERROR: {e}")

# E) Provincia de Buenos Aires
print("\n[E] PBA - portal datos provincia")
try:
    r = requests.get('https://catalogo.datos.gba.gob.ar/api/3/action/package_search',
        params={'q': 'delitos seguridad', 'rows': 5}, timeout=20, headers=headers)
    print(f"  HTTP {r.status_code}")
    if r.status_code == 200:
        for pkg in r.json().get('result', {}).get('results', []):
            print(f"    Dataset: {pkg['title']}")
            print(f"      updated: {pkg.get('metadata_modified','')}")
            for res in pkg.get('resources', [])[:3]:
                print(f"      [{res.get('format','')}] {res.get('url','')[:100]}")
except Exception as e:
    print(f"  ERROR: {e}")
