"""Reintento de pytrends con configuracion diferente."""
import sys, os, time
sys.stdout.reconfigure(encoding='utf-8')

print("=" * 80)
print("REINTENTO GOOGLE TRENDS")
print("=" * 80)

from pytrends.request import TrendReq

# Intento 1: sesion mas larga, backoff explicito
print("\n[Intento 1] backoff + retries + intentar 1 keyword")
try:
    pytrends = TrendReq(hl='es-AR', tz=-180, retries=3, backoff_factor=2.0, timeout=(10,25))
    time.sleep(5)
    pytrends.build_payload(['inflacion'], cat=0, timeframe='today 12-m', geo='AR')
    interest = pytrends.interest_over_time()
    print(f"  OK. Shape: {interest.shape}")
    print(interest.tail(5).to_string())
    os.makedirs('data', exist_ok=True)
    interest.to_csv('data/google_trends_inflacion.csv')
except Exception as e:
    print(f"  ERROR: {type(e).__name__}: {e}")

time.sleep(10)

# Intento 2: con cookies / requests args
print("\n[Intento 2] con requests_args (User-Agent custom)")
try:
    pytrends = TrendReq(
        hl='es-AR',
        tz=-180,
        retries=2,
        backoff_factor=1.5,
        requests_args={'headers': {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'}}
    )
    time.sleep(3)
    pytrends.build_payload(['precios'], cat=0, timeframe='today 3-m', geo='AR')
    df = pytrends.interest_over_time()
    print(f"  OK. Shape: {df.shape}")
    print(df.tail(5).to_string())
except Exception as e:
    print(f"  ERROR: {type(e).__name__}: {e}")
