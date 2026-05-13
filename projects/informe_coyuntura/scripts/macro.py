"""
Colector Cinturón Macro — CIGOB
Patrón estándar: URLs → fetch → score → cache → exit codes
Ejecutar desde projects/informe_coyuntura/: python scripts/macro.py
"""
import sys
import json
import requests
import logging
from datetime import datetime, timedelta
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

# ── Paths ─────────────────────────────────────────────────────────────────────
SCRIPT_DIR  = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
CACHE_PATH  = PROJECT_DIR / "output" / "cache" / "macro.json"

# ── URL Constants (NFR6: URLs al inicio del script) ───────────────────────────
INDEC_SERIES_BASE   = "https://apis.datos.gob.ar/series/api/series/"
BCRA_VARIABLES_BASE = "https://api.bcra.gob.ar/estadisticas/v4.0/Monetarias"

# INDEC — series IDs verificados en datos.gob.ar
INDEC_IPC_ID   = "148.3_INIVELNAL_DICI_M_26"  # IPC total nacional mensual

# BCRA — variable IDs verificados en api.bcra.gob.ar v4.0
BCRA_RESERVAS_ID = 1   # Reservas internacionales del BCRA (millones USD)
BCRA_BADLAR_ID   = 7   # BADLAR bancos privados (tasa anual %)

HTTP_TIMEOUT = 30
HTTP_HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; CIGOB-Monitor/1.0)"}

logging.basicConfig(level=logging.WARNING, format="%(message)s")

CINTURON              = "macro"
INDICADORES_ESPERADOS = ["ipc_total", "reservas_bcra", "badlar"]


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


def _bcra_ultimo(var_id: int) -> dict:
    desde = (datetime.today() - timedelta(days=45)).strftime("%Y-%m-%d")
    url   = f"{BCRA_VARIABLES_BASE}/{var_id}"
    r = requests.get(url, params={"desde": desde, "limit": 10},
                     headers=HTTP_HEADERS, timeout=HTTP_TIMEOUT, verify=False)
    r.raise_for_status()
    detalle = r.json()["results"][0]["detalle"]
    ultimo  = sorted(detalle, key=lambda x: x["fecha"], reverse=True)[0]
    return {"valor": ultimo["valor"], "fecha": ultimo["fecha"]}


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


def calcular_score(indicadores: dict) -> float:
    """
    Score 0-10: mayor = mayor tensión macroeconómica.
    ipc_total: 0% → 0, 10% → 10 (lineal)
    reservas_bcra: >40000 mill USD → 0, 10000 → 6.7, 0 → 10
    badlar: 0% → 0, 100% → 10 (tasa anual de referencia)
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

    return round(sum(scores) / len(scores), 1) if scores else 5.0


def main() -> None:
    cache_anterior        = load_cache()
    indicadores_anteriores = cache_anterior.get("indicadores", {})

    frescos: dict   = {}
    frescos_count   = 0

    for nombre, fetcher in [
        ("ipc_total",     fetch_ipc),
        ("reservas_bcra", fetch_reservas),
        ("badlar",        fetch_badlar),
    ]:
        resultado = fetcher()
        if resultado is not None and resultado.get("valor") is not None:
            frescos[nombre] = resultado
            frescos_count += 1
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
