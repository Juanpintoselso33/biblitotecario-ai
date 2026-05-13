"""Research 2: Salud publica - fuentes frecuentes."""
import requests, sys
sys.stdout.reconfigure(encoding='utf-8')
headers = {'User-Agent': 'Mozilla/5.0'}

print("=" * 80)
print("2. SALUD PUBLICA")
print("=" * 80)

# A) URLs SISA / DEIS
print("\n[A] URLs SISA / DEIS / MinSalud")
urls_sisa = [
    'https://sisa.msal.gov.ar/sisa/',
    'https://datos.gob.ar/dataset/salud-sistema-nacional-vigilancia-salud-snvs',
    'https://datos.gob.ar/dataset/salud-establecimientos-servicios-salud',
    'https://deis.msal.gov.ar/',
    'https://datos.gob.ar/dataset/salud-mortalidad-argentina',
    'https://www.argentina.gob.ar/salud/datos-abiertos',
    'https://bancos.salud.gob.ar/recurso/datos-abiertos',
]
for url in urls_sisa:
    try:
        r = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        print(f"  {url}")
        print(f"    -> HTTP {r.status_code} | ct={r.headers.get('content-type','')[:60]}")
    except Exception as e:
        print(f"  {url} -> ERROR {e}")

# B) datos.gob.ar package_search salud
print("\n[B] datos.gob.ar PACKAGE_SEARCH salud")
for q in ['salud mortalidad', 'salud vigilancia epidemiologica', 'salud acceso atencion primaria', 'sala situacion salud']:
    try:
        r = requests.get('https://datos.gob.ar/api/3/action/package_search',
            params={'q': q, 'rows': 5}, timeout=20)
        print(f"\n  Query '{q}' -> HTTP {r.status_code}")
        if r.status_code == 200:
            for pkg in r.json().get('result', {}).get('results', []):
                print(f"    Dataset: {pkg['title']}")
                print(f"      updated: {pkg.get('metadata_modified','')}")
                for res in pkg.get('resources', [])[:2]:
                    print(f"      [{res.get('format','')}] {res.get('last_modified','')[:10]} {res.get('url','')[:90]}")
    except Exception as e:
        print(f"  ERROR: {e}")

# C) Series del INDEC - cobertura salud (EPH)
print("\n[C] Series INDEC - cobertura salud")
for q in ['cobertura salud', 'obra social prepaga', 'gasto bolsillo salud']:
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

# D) Boletines integrados vigilancia (BIV) - el SNVS
print("\n[D] Boletines BIV (vigilancia epidemiologica semanal)")
urls_biv = [
    'https://www.argentina.gob.ar/salud/epidemiologia/boletines',
    'https://bancos.salud.gob.ar/bancos/materiales-para-equipos-de-salud/soporte/boletines-epidemiologicos',
]
for url in urls_biv:
    try:
        r = requests.get(url, headers=headers, timeout=15)
        print(f"  {url} -> HTTP {r.status_code}")
    except Exception as e:
        print(f"  ERROR: {e}")
