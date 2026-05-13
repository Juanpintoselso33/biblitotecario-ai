"""
Colector Cinturón Gestión — CIGOB
Patrón estándar: URLs → fetch → score → cache → exit codes
Ejecutar desde projects/informe_coyuntura/: python scripts/gestion.py

Indicadores:
  indice_salarios_publico — Var% mensual del IS sector público (INDEC).
                            Proxy de capacidad fiscal para sostener el aparato estatal.
  isac_construccion       — Var% mensual ISAC insumos cemento (INDEC).
                            Proxy de actividad en obras públicas e inversión del Estado.
"""
import sys
import json
import requests
import logging
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

# ── Paths ─────────────────────────────────────────────────────────────────────
SCRIPT_DIR  = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
CACHE_PATH  = PROJECT_DIR / "output" / "cache" / "gestion.json"

# ── URL Constants (NFR6) ──────────────────────────────────────────────────────
INDEC_SERIES_BASE = "https://apis.datos.gob.ar/series/api/series/"

# INDEC — series IDs verificados en datos.gob.ar
INDEC_IS_PUBLICO_ID  = "149.1_SOR_PUBICO_OCTU_0_14"   # IS sector público (base oct 2016, mensual)
INDEC_ISAC_CEMENTO_ID = "33.4_ISAC_CEMENAND_0_0_21_24"  # ISAC insumos cemento (mensual)

HTTP_TIMEOUT = 30
HTTP_HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; CIGOB-Monitor/1.0)"}

logging.basicConfig(level=logging.WARNING, format="%(message)s")

CINTURON              = "gestion"
INDICADORES_ESPERADOS = ["indice_salarios_publico", "isac_construccion"]


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


def _indec_var_mensual(series_id: str) -> dict:
    """Devuelve variación mensual del último dato disponible."""
    params = {"ids": series_id, "format": "json", "limit": 2, "sort": "desc"}
    r = requests.get(INDEC_SERIES_BASE, params=params, headers=HTTP_HEADERS, timeout=HTTP_TIMEOUT)
    r.raise_for_status()
    data = r.json()["data"]
    actual, anterior = data[0][1], data[1][1]
    var = round((actual / anterior - 1) * 100, 2) if anterior else None
    return {"valor": var, "fecha": data[0][0]}


def fetch_indice_salarios_publico() -> dict | None:
    """
    Variación mensual del Índice de Salarios - Sector Público (INDEC).
    Var% muy baja o negativa: salarios públicos caen → tensión laboral/gestión alta.
    Var% muy alta: catch-up salarial o presión fiscal.
    """
    try:
        res = _indec_var_mensual(INDEC_IS_PUBLICO_ID)
        return {
            "valor": res["valor"],
            "unidad": "% var. mensual",
            "fuente": INDEC_SERIES_BASE,
            "fecha_dato": res["fecha"],
            "desactualizado": False,
        }
    except Exception as e:
        _warn("indice_salarios_publico", e)
        return None


def fetch_isac_construccion() -> dict | None:
    """
    Variación mensual de ISAC insumos cemento (INDEC).
    Proxy de actividad en construcción pública e inversión del Estado.
    Caída sostenida = paralización de obras; suba = gestión activa.
    """
    try:
        res = _indec_var_mensual(INDEC_ISAC_CEMENTO_ID)
        return {
            "valor": res["valor"],
            "unidad": "% var. mensual",
            "fuente": INDEC_SERIES_BASE,
            "fecha_dato": res["fecha"],
            "desactualizado": False,
        }
    except Exception as e:
        _warn("isac_construccion", e)
        return None


def calcular_score(indicadores: dict) -> float:
    """
    Score 0-10: mayor = mayor tensión en capacidad de gestión del Estado.

    indice_salarios_publico (var% mensual):
        Var% muy baja o negativa = salarios reales caen → tensión gestión alta.
        Referencia: 0% → 5, -5% → 8, +15% → 0 (nominal = catch-up lógico, poca tensión).
        score = max(0, min(10, 5 - var/3))

    isac_construccion (var% mensual):
        Caída = obras paralizadas → tensión gestión alta.
        0% → 5, -30% → 10, +30% → 0.
        score = max(0, min(10, 5 - var/6))
    """
    scores = []

    sal = indicadores.get("indice_salarios_publico", {}).get("valor")
    if sal is not None:
        scores.append(min(10.0, max(0.0, 5.0 - float(sal) / 3.0)))

    isac = indicadores.get("isac_construccion", {}).get("valor")
    if isac is not None:
        scores.append(min(10.0, max(0.0, 5.0 - float(isac) / 6.0)))

    return round(sum(scores) / len(scores), 1) if scores else 5.0


def main() -> None:
    cache_anterior         = load_cache()
    indicadores_anteriores = cache_anterior.get("indicadores", {})

    frescos: dict = {}
    frescos_count = 0

    for nombre, fetcher in [
        ("indice_salarios_publico", fetch_indice_salarios_publico),
        ("isac_construccion",       fetch_isac_construccion),
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
