"""
Colector Cinturón Vida Cotidiana — CIGOB
Patrón estándar: URLs → fetch → score → cache → exit codes
Ejecutar desde projects/informe_coyuntura/: python scripts/vida_cotidiana.py
"""
import sys
import json
import logging
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

# ── Paths ─────────────────────────────────────────────────────────────────────
SCRIPT_DIR  = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
CACHE_PATH  = PROJECT_DIR / "output" / "cache" / "vida_cotidiana.json"

# ── URL Constants (NFR6: URLs al inicio del script) ───────────────────────────
DATOS_GOB_BASE   = "https://apis.datos.gob.ar/series/api/series/"
UTDT_ICC_LISTADO = "https://www.utdt.edu/listado_contenidos.php?id_item_menu=16458"
SNIC_CSV         = "https://cloud-snic.minseg.gob.ar/Bases/SNIC/snic-pais.csv"

# Permite que los collectors hagan 'from config import ...' (encuentran vida_cotidiana/config.py)
sys.path.insert(0, str(SCRIPT_DIR / "vida_cotidiana"))

logging.basicConfig(level=logging.WARNING, format="%(message)s")

CINTURON              = "vida_cotidiana"
INDICADORES_ESPERADOS = ["ipc_total", "desocupacion", "icc_utdt"]


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


def fetch_indicadores() -> dict:
    """Llama a los collectors existentes y normaliza al schema estándar."""
    frescos = {}

    # ── INDEC: IPC + desocupación ─────────────────────────────────────────────
    indec_data = {}
    try:
        from collectors.indec_series import fetch_indec
        indec_data = fetch_indec()
    except Exception as e:
        _warn("indec_series", e)

    ipc = indec_data.get("ipc_total", {})
    if ipc and ipc.get("variacion_mensual_pct") is not None:
        frescos["ipc_total"] = {
            "valor": round(ipc["variacion_mensual_pct"], 2),
            "unidad": "% mensual",
            "fuente": DATOS_GOB_BASE,
            "fecha_dato": ipc.get("fecha"),
            "desactualizado": False,
        }
    else:
        _warn("ipc_total", ValueError("dato no disponible"))

    desoc = indec_data.get("desocupacion", {})
    if desoc and desoc.get("valor") is not None:
        frescos["desocupacion"] = {
            "valor": round(float(desoc["valor"]), 1),
            "unidad": "%",
            "fuente": DATOS_GOB_BASE,
            "fecha_dato": desoc.get("fecha"),
            "desactualizado": False,
        }
    else:
        _warn("desocupacion", ValueError("dato no disponible"))

    # ── ICC UTDT ──────────────────────────────────────────────────────────────
    try:
        from collectors.utdt_icc import fetch_icc
        icc_data = fetch_icc()
        icc = icc_data.get("icc_utdt", {})
        if icc and icc.get("valor") is not None:
            frescos["icc_utdt"] = {
                "valor": round(float(icc["valor"]), 2),
                "unidad": "índice",
                "fuente": UTDT_ICC_LISTADO,
                "fecha_dato": icc.get("fecha"),
                "desactualizado": False,
            }
        else:
            raise ValueError("respuesta vacía")
    except Exception as e:
        _warn("icc_utdt", e)

    return frescos


def calcular_score(indicadores: dict) -> float:
    """
    Score 0-10: mayor = peor condición de vida cotidiana.
    ipc_total: 0% → 0, 10% → 10 (lineal)
    desocupacion: 0% → 0, 20% → 10 (lineal × 0.5)
    icc_utdt: ICC ~42 → ~6, ICC >60 → 0, ICC <30 → 10
    """
    scores = []

    ipc = indicadores.get("ipc_total", {}).get("valor")
    if ipc is not None:
        scores.append(min(10.0, max(0.0, float(ipc))))

    desoc = indicadores.get("desocupacion", {}).get("valor")
    if desoc is not None:
        scores.append(min(10.0, max(0.0, float(desoc) / 2)))

    icc = indicadores.get("icc_utdt", {}).get("valor")
    if icc is not None:
        scores.append(min(10.0, max(0.0, (60.0 - float(icc)) / 3)))

    return round(sum(scores) / len(scores), 1) if scores else 5.0


def main() -> None:
    cache_anterior        = load_cache()
    indicadores_anteriores = cache_anterior.get("indicadores", {})

    frescos_nuevos  = fetch_indicadores()
    indicadores: dict = {}
    frescos_count   = 0

    for key in INDICADORES_ESPERADOS:
        if key in frescos_nuevos:
            indicadores[key] = frescos_nuevos[key]
            frescos_count += 1
        elif key in indicadores_anteriores:
            indicadores[key] = {**indicadores_anteriores[key], "desactualizado": True}

    score   = calcular_score(indicadores)
    payload = {
        "cinturon":     CINTURON,
        "generated_at": datetime.now().isoformat(),
        "score":        score,
        "indicadores":  indicadores,
    }

    if indicadores:
        save_cache(payload)
        print(f"[OK] {CINTURON}: score={score} "
              f"frescos={frescos_count}/{len(INDICADORES_ESPERADOS)}")

    total = len(INDICADORES_ESPERADOS)
    if frescos_count == total:
        sys.exit(0)
    elif frescos_count > 0:
        sys.exit(1)
    else:
        sys.exit(2)


if __name__ == "__main__":
    main()
