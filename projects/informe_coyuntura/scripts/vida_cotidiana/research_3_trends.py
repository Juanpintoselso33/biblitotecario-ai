"""Research 3: Google Trends via pytrends."""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')

print("=" * 80)
print("3. GOOGLE TRENDS (pytrends)")
print("=" * 80)

try:
    from pytrends.request import TrendReq
    import time

    pytrends = TrendReq(hl='es-AR', tz=-180)

    # Test 1: keywords vida cotidiana
    kw_list = ['inflación', 'precios', 'inseguridad']
    print(f"\n[A] Build payload con {kw_list} | timeframe='today 12-m' | geo='AR'")
    pytrends.build_payload(kw_list, cat=0, timeframe='today 12-m', geo='AR')

    interest = pytrends.interest_over_time()
    print(f"  Shape: {interest.shape}")
    print(f"  Columnas: {list(interest.columns)}")
    print(f"\n  Ultimas 6 filas:")
    print(interest.tail(6).to_string())

    os.makedirs('data', exist_ok=True)
    interest.to_csv('data/google_trends_test.csv')
    print(f"\n  CSV guardado: data/google_trends_test.csv")

    # Test 2: related queries
    time.sleep(2)
    print(f"\n[B] interest_by_region (top 5 provincias para 'inflación')")
    try:
        region = pytrends.interest_by_region(resolution='REGION', inc_low_vol=True, inc_geo_code=False)
        print(region.sort_values('inflación', ascending=False).head(8).to_string())
    except Exception as e:
        print(f"  region ERROR: {e}")

    # Test 3: trending searches
    time.sleep(2)
    print(f"\n[C] trending_searches Argentina")
    try:
        trending = pytrends.trending_searches(pn='argentina')
        print(trending.head(10).to_string())
    except Exception as e:
        print(f"  trending ERROR: {e}")

    # Test 4: keyword adicional politico
    time.sleep(2)
    print(f"\n[D] Tema politico: ['Milei', 'CFK', 'dolar', 'jubilaciones'] timeframe='today 3-m'")
    try:
        pytrends.build_payload(['Milei', 'CFK', 'dolar', 'jubilaciones'], cat=0, timeframe='today 3-m', geo='AR')
        pol = pytrends.interest_over_time()
        print(f"  Shape: {pol.shape}")
        print(pol.tail(6).to_string())
        pol.to_csv('data/google_trends_politico_test.csv')
        print(f"  CSV: data/google_trends_politico_test.csv")
    except Exception as e:
        print(f"  politico ERROR: {e}")

except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"pytrends ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
