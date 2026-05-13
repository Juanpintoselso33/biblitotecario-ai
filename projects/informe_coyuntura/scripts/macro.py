"""
Colector Cinturón Macro — CIGOB
Patrón estándar: URLs → fetch → score → cache → exit codes
Ejecutar desde projects/informe_coyuntura/: python scripts/macro.py
"""
import sys
import json
import requests
import urllib3
import logging
from datetime import datetime, timedelta, date
from pathlib import Path

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.stdout.reconfigure(encoding="utf-8")

# ── Paths ─────────────────────────────────────────────────────────────────────
SCRIPT_DIR  = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
CACHE_PATH  = PROJECT_DIR / "output" / "cache" / "macro.json"

# ── URL Constants (NFR6: URLs al inicio del script) ───────────────────────────
INDEC_SERIES_BASE   = "https://apis.datos.gob.ar/series/api/series/"
BCRA_VARIABLES_BASE = "https://api.bcra.gob.ar/estadisticas/v4.0/Monetarias"

# INDEC — series IDs verificados en datos.gob.ar
INDEC_IPC_ID         = "148.3_INIVELNAL_DICI_M_26"     # IPC total nacional mensual
INDEC_EMAE_IA_ID     = "143.3_ICE_SERVIA_2004_A_25"    # EMAE variación i.a. mensual (base 2004)
INDEC_SALDO_COM_ID   = "164.3_SOTALTAL_0_0_8"          # Saldo comercial total mensual (M USD)
INDEC_RECAUDACION_ID = "172.3_TL_RECAION_M_0_0_17"     # Recaudación total mensual (M ARS)
INDEC_TCRM_ID        = "116.3_TCRMA_0_M_36"            # Tipo de Cambio Real Multilateral (base 2010=100)

# BCRA — variable IDs verificados en api.bcra.gob.ar v4.0
BCRA_RESERVAS_ID    = 1    # Reservas internacionales (millones USD)
BCRA_BADLAR_ID      = 7    # BADLAR bancos privados (% anual)
BCRA_REM_IPC_ID     = 29   # REM: mediana expectativas IPC próximos 12 meses (% anual)
BCRA_PRESTAMOS_ID   = 26   # Préstamos sector privado (millones ARS)
BCRA_BASE_MON_ID    = 15   # Base monetaria (millones ARS)
BCRA_TC_MAYOR_ID    = 5    # Tipo de cambio mayorista de referencia (ARS/USD)

HTTP_TIMEOUT = 30
HTTP_HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; CIGOB-Monitor/1.0)"}

logging.basicConfig(level=logging.WARNING, format="%(message)s")

CINTURON = "macro"
INDICADORES_ESPERADOS = [
    "ipc_total", "reservas_bcra", "badlar",
    "emae_ia", "saldo_comercial_12m", "recaudacion", "tcrm",
    "rem_ipc_12m", "prestamos_privados", "base_monetaria", "tc_mayorista",
]


def load_cache() -> dict:
    if CACHE_PATH.exists():
        with open(CACHE_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_cache(data: dict) -> None:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)


def _warn(indicador: str, err: Exception) -> None:
    print(f"[WARN] {CINTURON}.{indicador}: {err}. Usando cache.")


def _indec_serie(series_id: str, limit: int = 2) -> list:
    params = {"ids": series_id, "format": "json", "limit": limit, "sort": "desc"}
    r = requests.get(INDEC_SERIES_BASE, params=params, headers=HTTP_HEADERS, timeout=HTTP_TIMEOUT)
    r.raise_for_status()
    return r.json()["data"]


def _bcra_detalle(var_id: int, dias: int = 60) -> list:
    """Devuelve el detalle diario del BCRA para los últimos `dias` días, ordenado desc."""
    desde = (datetime.today() - timedelta(days=dias)).strftime("%Y-%m-%d")
    url   = f"{BCRA_VARIABLES_BASE}/{var_id}"
    r = requests.get(url, params={"desde": desde},
                     headers=HTTP_HEADERS, timeout=HTTP_TIMEOUT, verify=False)
    r.raise_for_status()
    detalle = r.json()["results"][0]["detalle"]
    return sorted(detalle, key=lambda x: x["fecha"], reverse=True)


def _bcra_ultimo(var_id: int) -> dict:
    detalle = _bcra_detalle(var_id, dias=45)
    ultimo  = detalle[0]
    return {"valor": ultimo["valor"], "fecha": ultimo["fecha"]}


def _bcra_variacion_m(var_id: int) -> dict:
    """Variación % mensual: último valor vs valor de hace ~30 días."""
    detalle = _bcra_detalle(var_id, dias=60)
    ultimo  = detalle[0]
    fecha_u = date.fromisoformat(ultimo["fecha"])
    # Buscar el registro más cercano a 30 días atrás
    hace_30 = None
    for d in detalle:
        fecha_d = date.fromisoformat(d["fecha"])
        if (fecha_u - fecha_d).days >= 28:
            hace_30 = d
            break
    if hace_30 is None:
        raise ValueError(f"BCRA var {var_id}: sin datos de hace 30+ días")
    var_m = (float(ultimo["valor"]) / float(hace_30["valor"]) - 1) * 100
    return {"var_m": round(var_m, 2), "fecha": ultimo["fecha"]}


# ── Fetchers ──────────────────────────────────────────────────────────────────

def fetch_ipc() -> dict | None:
    try:
        data = _indec_serie(INDEC_IPC_ID, limit=2)
        actual, anterior = data[0][1], data[1][1]
        var = (actual / anterior - 1) * 100 if anterior else None
        return {
            "valor": round(var, 2) if var is not None else None,
            "unidad": "% mensual",
            "fuente": INDEC_SERIES_BASE,
            "fecha_dato": data[0][0],
            "desactualizado": False,
        }
    except Exception as e:
        _warn("ipc_total", e)
        return None


def fetch_reservas() -> dict | None:
    try:
        ultimo = _bcra_ultimo(BCRA_RESERVAS_ID)
        return {
            "valor": round(float(ultimo["valor"]), 0),
            "unidad": "mill USD",
            "fuente": f"{BCRA_VARIABLES_BASE}/{BCRA_RESERVAS_ID}",
            "fecha_dato": ultimo["fecha"],
            "desactualizado": False,
        }
    except Exception as e:
        _warn("reservas_bcra", e)
        return None


def fetch_badlar() -> dict | None:
    try:
        ultimo = _bcra_ultimo(BCRA_BADLAR_ID)
        return {
            "valor": round(float(ultimo["valor"]), 2),
            "unidad": "% anual",
            "fuente": f"{BCRA_VARIABLES_BASE}/{BCRA_BADLAR_ID}",
            "fecha_dato": ultimo["fecha"],
            "desactualizado": False,
        }
    except Exception as e:
        _warn("badlar", e)
        return None


def fetch_emae_ia() -> dict | None:
    try:
        data = _indec_serie(INDEC_EMAE_IA_ID, limit=2)
        val  = data[0][1]  # ya es variación i.a. en decimal (0.0187 = 1.87%)
        return {
            "valor": round(float(val) * 100, 2),
            "unidad": "% i.a.",
            "fuente": INDEC_SERIES_BASE,
            "fecha_dato": data[0][0],
            "desactualizado": False,
        }
    except Exception as e:
        _warn("emae_ia", e)
        return None


def fetch_saldo_comercial_12m() -> dict | None:
    try:
        data   = _indec_serie(INDEC_SALDO_COM_ID, limit=13)
        meses  = [row[1] for row in data[:12] if row[1] is not None]
        total  = sum(meses)
        return {
            "valor": round(total, 0),
            "unidad": "mill USD acumulado 12m",
            "fuente": INDEC_SERIES_BASE,
            "fecha_dato": data[0][0],
            "desactualizado": False,
        }
    except Exception as e:
        _warn("saldo_comercial_12m", e)
        return None


def fetch_recaudacion() -> dict | None:
    try:
        data     = _indec_serie(INDEC_RECAUDACION_ID, limit=2)
        actual   = data[0][1]
        anterior = data[1][1]
        var_m    = (actual / anterior - 1) * 100 if anterior else None
        return {
            "valor": round(var_m, 2) if var_m is not None else None,
            "unidad": "% var mensual nominal",
            "fuente": INDEC_SERIES_BASE,
            "fecha_dato": data[0][0],
            "desactualizado": False,
        }
    except Exception as e:
        _warn("recaudacion", e)
        return None


def fetch_tcrm() -> dict | None:
    try:
        data = _indec_serie(INDEC_TCRM_ID, limit=2)
        val  = data[0][1]
        return {
            "valor": round(float(val), 2),
            "unidad": "índice base 2010=100",
            "fuente": INDEC_SERIES_BASE,
            "fecha_dato": data[0][0],
            "desactualizado": False,
        }
    except Exception as e:
        _warn("tcrm", e)
        return None


def fetch_rem_ipc_12m() -> dict | None:
    try:
        ultimo = _bcra_ultimo(BCRA_REM_IPC_ID)
        return {
            "valor": round(float(ultimo["valor"]), 1),
            "unidad": "% anual esperado (mediana REM)",
            "fuente": f"{BCRA_VARIABLES_BASE}/{BCRA_REM_IPC_ID}",
            "fecha_dato": ultimo["fecha"],
            "desactualizado": False,
        }
    except Exception as e:
        _warn("rem_ipc_12m", e)
        return None


def fetch_prestamos_privados() -> dict | None:
    try:
        result = _bcra_variacion_m(BCRA_PRESTAMOS_ID)
        return {
            "valor": result["var_m"],
            "unidad": "% var mensual nominal",
            "fuente": f"{BCRA_VARIABLES_BASE}/{BCRA_PRESTAMOS_ID}",
            "fecha_dato": result["fecha"],
            "desactualizado": False,
        }
    except Exception as e:
        _warn("prestamos_privados", e)
        return None


def fetch_base_monetaria() -> dict | None:
    try:
        result = _bcra_variacion_m(BCRA_BASE_MON_ID)
        return {
            "valor": result["var_m"],
            "unidad": "% var mensual nominal",
            "fuente": f"{BCRA_VARIABLES_BASE}/{BCRA_BASE_MON_ID}",
            "fecha_dato": result["fecha"],
            "desactualizado": False,
        }
    except Exception as e:
        _warn("base_monetaria", e)
        return None


def fetch_tc_mayorista() -> dict | None:
    try:
        result = _bcra_variacion_m(BCRA_TC_MAYOR_ID)
        return {
            "valor": result["var_m"],
            "unidad": "% var mensual",
            "fuente": f"{BCRA_VARIABLES_BASE}/{BCRA_TC_MAYOR_ID}",
            "fecha_dato": result["fecha"],
            "desactualizado": False,
        }
    except Exception as e:
        _warn("tc_mayorista", e)
        return None


# ── Scoring ───────────────────────────────────────────────────────────────────

def calcular_score(indicadores: dict) -> float:
    """
    Score 0-10: mayor = mayor tensión macroeconómica.
    Cada indicador aporta 1 voto al promedio (equal-weight).

    ipc_total       (% mensual):     0% → 0 | 5% → 5 | 10% → 10
    reservas_bcra   (mill USD):      ≥40000 → 0 | 20000 → 5 | 0 → 10
    badlar          (% anual):       0% → 0 | 50% → 5 | 100% → 10
    emae_ia         (% i.a.):        +5% → 0 | 0% → 5 | -5% → 10
    saldo_com_12m   (mill USD 12m):  +6000 → 0 | 0 → 5 | -6000 → 10
    recaudacion     (% var_m nom.):  +5% → 0 | 0% → 5 | -5% → 10
    tcrm            (índice 2010):   100 → 0 | 75 → 5 | 50 → 10
    rem_ipc_12m     (% anual):       10% → 0 | 55% → 5 | 100% → 9
    prestamos_priv  (% var_m nom.):  +5% → 0 | 0% → 5 | -5% → 10
    base_monetaria  (% var_m nom.):  0% → 0 | 10% → 5 | 20% → 10
    tc_mayorista    (% var_m):       0% → 0 | 10% → 5 | 20% → 10
    """
    scores = []

    ipc = indicadores.get("ipc_total", {}).get("valor")
    if ipc is not None:
        scores.append(min(10.0, max(0.0, float(ipc))))

    reservas = indicadores.get("reservas_bcra", {}).get("valor")
    if reservas is not None:
        scores.append(min(10.0, max(0.0, (40000.0 - float(reservas)) / 4000.0)))

    badlar = indicadores.get("badlar", {}).get("valor")
    if badlar is not None:
        scores.append(min(10.0, max(0.0, float(badlar) / 10.0)))

    emae = indicadores.get("emae_ia", {}).get("valor")
    if emae is not None:
        # +5%→0, 0%→5, -5%→10
        scores.append(min(10.0, max(0.0, 5.0 - float(emae))))

    sc = indicadores.get("saldo_comercial_12m", {}).get("valor")
    if sc is not None:
        # +6000→0, 0→5, -6000→10
        scores.append(min(10.0, max(0.0, 5.0 - float(sc) / 1200.0)))

    rec = indicadores.get("recaudacion", {}).get("valor")
    if rec is not None:
        # var_m +5%→0, 0%→5, -5%→10
        scores.append(min(10.0, max(0.0, 5.0 - float(rec))))

    tcrm = indicadores.get("tcrm", {}).get("valor")
    if tcrm is not None:
        # 100→0, 75→5, 50→10
        scores.append(min(10.0, max(0.0, (100.0 - float(tcrm)) / 5.0)))

    rem = indicadores.get("rem_ipc_12m", {}).get("valor")
    if rem is not None:
        # 10%→0, 55%→5, 100%→9
        scores.append(min(10.0, max(0.0, (float(rem) - 10.0) / 9.0)))

    prest = indicadores.get("prestamos_privados", {}).get("valor")
    if prest is not None:
        # var_m +5%→0, 0%→5, -5%→10
        scores.append(min(10.0, max(0.0, 5.0 - float(prest))))

    bm = indicadores.get("base_monetaria", {}).get("valor")
    if bm is not None:
        # var_m 0%→0, 10%→5, 20%→10
        scores.append(min(10.0, max(0.0, float(bm) / 2.0)))

    tc = indicadores.get("tc_mayorista", {}).get("valor")
    if tc is not None:
        # var_m 0%→0, 10%→5, 20%→10
        scores.append(min(10.0, max(0.0, float(tc) / 2.0)))

    return round(sum(scores) / len(scores), 1) if scores else 5.0


def main() -> None:
    cache_anterior         = load_cache()
    indicadores_anteriores = cache_anterior.get("indicadores", {})

    frescos: dict = {}
    frescos_count = 0

    for nombre, fetcher in [
        ("ipc_total",          fetch_ipc),
        ("reservas_bcra",      fetch_reservas),
        ("badlar",             fetch_badlar),
        ("emae_ia",            fetch_emae_ia),
        ("saldo_comercial_12m", fetch_saldo_comercial_12m),
        ("recaudacion",        fetch_recaudacion),
        ("tcrm",               fetch_tcrm),
        ("rem_ipc_12m",        fetch_rem_ipc_12m),
        ("prestamos_privados", fetch_prestamos_privados),
        ("base_monetaria",     fetch_base_monetaria),
        ("tc_mayorista",       fetch_tc_mayorista),
    ]:
        resultado = fetcher()
        if resultado is not None and resultado.get("valor") is not None:
            frescos[nombre] = resultado
            frescos_count  += 1
        elif nombre in indicadores_anteriores:
            frescos[nombre] = {**indicadores_anteriores[nombre], "desactualizado": True}

    score   = calcular_score(frescos)
    payload = {
        "cinturon":     CINTURON,
        "generated_at": datetime.now().isoformat(),
        "score":        score,
        "indicadores":  frescos,
    }

    if frescos:
        save_cache(payload)
        total = len(INDICADORES_ESPERADOS)
        print(f"[OK] {CINTURON}: score={score} frescos={frescos_count}/{total}")

    if frescos_count == len(INDICADORES_ESPERADOS):
        sys.exit(0)
    elif frescos_count > 0:
        sys.exit(1)
    else:
        sys.exit(2)


if __name__ == "__main__":
    main()
