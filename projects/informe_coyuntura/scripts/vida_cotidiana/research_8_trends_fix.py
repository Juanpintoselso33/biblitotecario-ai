"""Fix pytrends para urllib3 v2: monkey-patch + retry sin retries kwarg."""
import sys, os, time
sys.stdout.reconfigure(encoding='utf-8')

# Monkey-patch urllib3 Retry para aceptar method_whitelist (alias de allowed_methods)
import urllib3.util.retry
_orig_init = urllib3.util.retry.Retry.__init__
def _patched_init(self, *args, **kwargs):
    if 'method_whitelist' in kwargs:
        kwargs['allowed_methods'] = kwargs.pop('method_whitelist')
    return _orig_init(self, *args, **kwargs)
urllib3.util.retry.Retry.__init__ = _patched_init

print("=" * 80)
print("PYTRENDS con monkey-patch urllib3 v2")
print("=" * 80)

from pytrends.request import TrendReq

# Esperar para evitar 429 residual
print("Esperando 30s para evitar rate limit...")
time.sleep(30)

# Test 1: keyword unica
print("\n[Test 1] 1 keyword | timeframe='today 12-m' | geo='AR'")
try:
    pytrends = TrendReq(hl='es-AR', tz=-180, timeout=(15, 30))
    pytrends.build_payload(['inflacion'], cat=0, timeframe='today 12-m', geo='AR')
    interest = pytrends.interest_over_time()
    print(f"  OK. Shape: {interest.shape}")
    print(f"  Columnas: {list(interest.columns)}")
    print("  Ultimas 6 filas:")
    print(interest.tail(6).to_string())
    os.makedirs('data', exist_ok=True)
    interest.to_csv('data/google_trends_inflacion.csv')
    print(f"\n  Guardado en data/google_trends_inflacion.csv")
except Exception as e:
    print(f"  ERROR: {type(e).__name__}: {e}")

time.sleep(20)

# Test 2: multiple keywords (max 5 segun API)
print("\n[Test 2] 3 keywords | timeframe='today 3-m'")
try:
    pytrends = TrendReq(hl='es-AR', tz=-180, timeout=(15, 30))
    pytrends.build_payload(['Milei', 'dolar', 'jubilaciones'], cat=0, timeframe='today 3-m', geo='AR')
    df = pytrends.interest_over_time()
    print(f"  OK. Shape: {df.shape}")
    print("  Ultimas 6 filas:")
    print(df.tail(6).to_string())
    df.to_csv('data/google_trends_politico.csv')
except Exception as e:
    print(f"  ERROR: {type(e).__name__}: {e}")

time.sleep(20)

# Test 3: interest_by_region
print("\n[Test 3] interest_by_region (provincias)")
try:
    pytrends = TrendReq(hl='es-AR', tz=-180, timeout=(15, 30))
    pytrends.build_payload(['inseguridad'], cat=0, timeframe='today 3-m', geo='AR')
    region = pytrends.interest_by_region(resolution='REGION', inc_low_vol=True, inc_geo_code=False)
    print(f"  OK. Shape: {region.shape}")
    print(region.sort_values('inseguridad', ascending=False).head(10).to_string())
except Exception as e:
    print(f"  ERROR: {type(e).__name__}: {e}")

time.sleep(15)

# Test 4: trending_searches argentina
print("\n[Test 4] trending_searches Argentina")
try:
    pytrends = TrendReq(hl='es-AR', tz=-180, timeout=(15, 30))
    trending = pytrends.trending_searches(pn='argentina')
    print(f"  OK. Top 10 trending hoy:")
    print(trending.head(10).to_string())
except Exception as e:
    print(f"  ERROR: {type(e).__name__}: {e}")

time.sleep(15)

# Test 5: related_queries
print("\n[Test 5] related_queries para 'inseguridad'")
try:
    pytrends = TrendReq(hl='es-AR', tz=-180, timeout=(15, 30))
    pytrends.build_payload(['inseguridad'], cat=0, timeframe='today 12-m', geo='AR')
    rq = pytrends.related_queries()
    print(f"  OK. Keys: {list(rq.keys())}")
    for kw, data in rq.items():
        print(f"\n  >> {kw}")
        if data:
            for k, df in data.items():
                if df is not None:
                    print(f"     {k}:")
                    print(df.head(5).to_string() if not df.empty else "     (vacio)")
except Exception as e:
    print(f"  ERROR: {type(e).__name__}: {e}")
