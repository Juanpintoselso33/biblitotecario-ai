"""Salud: workaround SSL issue para datos.salud.gob.ar y verificar defunciones 2023."""
import requests, sys, urllib3, time
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.stdout.reconfigure(encoding='utf-8')
headers = {'User-Agent': 'Mozilla/5.0'}

print("=" * 80)
print("SALUD - SSL workaround")
print("=" * 80)

# Test con verify=False para datos.salud.gob.ar
print("\n[1] datos.salud.gob.ar/api/3/action/package_list (verify=False)")
try:
    r = requests.get('https://datos.salud.gob.ar/api/3/action/package_list',
        timeout=20, verify=False, headers=headers)
    print(f"  HTTP {r.status_code}")
    if r.status_code == 200:
        pkgs = r.json().get('result', [])
        print(f"  Total datasets: {len(pkgs)}")
        # Buscar relevantes
        for kw in ['mortal', 'defunc', 'vigilancia', 'cobertura', 'natal', 'embaraz']:
            matches = [p for p in pkgs if kw in p.lower()]
            if matches:
                print(f"\n  [{kw}] {len(matches)} datasets:")
                for p in matches[:10]:
                    print(f"    - {p}")
except Exception as e:
    print(f"  ERROR: {e}")

# Defunciones 2023 con SSL bypass
print("\n[2] Defunciones 2023 HEAD (verify=False)")
try:
    r = requests.head('https://datos.salud.gob.ar/dataset/c1643775-18e1-40fd-9e7f-0cebb5b1abe6/resource/615c454b-c02c-4011-b55a-86e8a28167bf/download/base_def_23_men.csv',
        timeout=15, verify=False, headers=headers, allow_redirects=True)
    print(f"  HTTP {r.status_code}")
    print(f"    size={r.headers.get('content-length','?')}")
    print(f"    last-modified={r.headers.get('last-modified','?')}")
    print(f"    content-type={r.headers.get('content-type','?')}")
except Exception as e:
    print(f"  ERROR: {e}")

# DEIS
print("\n[3] deis.msal.gov.ar (verify=False)")
for url in ['https://deis.msal.gov.ar/',
            'https://deis.msal.gov.ar/index.php/base-de-datos/',
            'https://deis.msal.gov.ar/index.php/base-de-datos/2023/']:
    try:
        r = requests.get(url, headers=headers, timeout=15, verify=False, allow_redirects=True)
        print(f"  {url} -> HTTP {r.status_code} | ct={r.headers.get('content-type','')[:50]}")
    except Exception as e:
        print(f"  ERROR: {type(e).__name__}")

# Boletines BIV
print("\n[4] Boletines vigilancia BIV - verify=False")
for url in ['https://bancos.salud.gob.ar/bancos/materiales-para-equipos-de-salud/soporte/boletines-epidemiologicos',
            'https://www.argentina.gob.ar/salud/epidemiologia/boletines',
            'https://www.argentina.gob.ar/salud/epidemiologia']:
    try:
        r = requests.get(url, headers=headers, timeout=15, verify=False)
        print(f"  {url} -> HTTP {r.status_code}")
    except Exception as e:
        print(f"  ERROR: {type(e).__name__}: {str(e)[:80]}")
