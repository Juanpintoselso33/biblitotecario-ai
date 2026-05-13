"""
Colector Cinturón Político — CIGOB
Patrón estándar: URLs → fetch → score → cache → exit codes
Ejecutar desde projects/informe_coyuntura/: python scripts/politica.py

Indicadores:
  icg_utdt       — Índice de Confianza en el Gobierno (UTDT, mensual)
  ipc_regulados  — Variación IPC regulados (tarifas/subsidios, INDEC)
                   Proxy de decisiones gubernamentales sobre servicios públicos.
"""
import sys
import json
import re
import requests
import logging
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

# ── Paths ─────────────────────────────────────────────────────────────────────
SCRIPT_DIR  = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
CACHE_PATH  = PROJECT_DIR / "output" / "cache" / "politica.json"

# ── URL Constants (NFR6) ──────────────────────────────────────────────────────
INDEC_SERIES_BASE       = "https://apis.datos.gob.ar/series/api/series/"
UTDT_ICG_LISTADO        = "https://www.utdt.edu/listado_contenidos.php?id_item_menu=16457"
UTDT_ICG_DOWNLOAD_BASE  = "https://www.utdt.edu/download.php?fname="

# INDEC — series IDs verificados en datos.gob.ar
INDEC_IPC_REGULADOS_ID  = "148.3_IREGULANAL_DICI_M_22"  # IPC Regulados (tarifas)
INDEC_IPC_TOTAL_ID      = "148.3_INIVELNAL_DICI_M_26"   # IPC total (referencia)

HTTP_TIMEOUT = 30
HTTP_HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; CIGOB-Monitor/1.0)"}

logging.basicConfig(level=logging.WARNING, format="%(message)s")

CINTURON              = "politica"
INDICADORES_ESPERADOS = ["ipc_regulados", "icg_utdt"]


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
    params = {"ids": series_id, "format": "json", "limit": 2, "sort": "desc"}
    r = requests.get(INDEC_SERIES_BASE, params=params, headers=HTTP_HEADERS, timeout=HTTP_TIMEOUT)
    r.raise_for_status()
    data = r.json()["data"]
    actual, anterior = data[0][1], data[1][1]
    var = (actual / anterior - 1) * 100 if anterior else None
    return {"valor": round(var, 2) if var else None, "fecha": data[0][0]}


def fetch_ipc_regulados() -> dict | None:
    """
    IPC Regulados (tarifas de servicios públicos).
    Var% elevada = gobierno habilitó ajuste de tarifas → señal de tension política.
    Comparado con IPC total: si regulados sube más → gobierno transfiriendo costos.
    """
    try:
        reg = _indec_var_mensual(INDEC_IPC_REGULADOS_ID)
        tot = _indec_var_mensual(INDEC_IPC_TOTAL_ID)
        brecha = round(reg["valor"] - tot["valor"], 2) if reg["valor"] and tot["valor"] else None
        return {
            "valor": reg["valor"],
            "valor_brecha_vs_ipc": brecha,
            "unidad": "% mensual",
            "fuente": INDEC_SERIES_BASE,
            "fecha_dato": reg["fecha"],
            "desactualizado": False,
        }
    except Exception as e:
        _warn("ipc_regulados", e)
        return None


def fetch_icg() -> dict | None:
    """
    Índice de Confianza en el Gobierno (UTDT).
    Busca XLS en la página de listado; fallback graceful si no hay descarga.
    """
    try:
        import xlrd
        r = requests.get(UTDT_ICG_LISTADO, headers=HTTP_HEADERS, timeout=HTTP_TIMEOUT, verify=False)
        r.raise_for_status()
        matches = re.findall(r"download\.php\?fname=([^\"'\s>]+\.(?:xls|xlsx))", r.text, re.IGNORECASE)
        if not matches:
            raise ValueError("Sin descarga XLS en página ICG UTDT")

        url = UTDT_ICG_DOWNLOAD_BASE + matches[0]
        r2 = requests.get(url, headers=HTTP_HEADERS, timeout=HTTP_TIMEOUT, verify=False)
        r2.raise_for_status()

        wb = xlrd.open_workbook(file_contents=r2.content)
        ws = wb.sheets()[0]

        for row_idx in range(ws.nrows - 1, -1, -1):
            fc, vc = ws.cell(row_idx, 0), ws.cell(row_idx, 1)
            if fc.ctype == xlrd.XL_CELL_DATE and vc.ctype == xlrd.XL_CELL_NUMBER:
                try:
                    t = xlrd.xldate_as_tuple(fc.value, wb.datemode)
                    return {
                        "valor": round(vc.value, 2),
                        "unidad": "índice",
                        "fuente": UTDT_ICG_LISTADO,
                        "fecha_dato": f"{t[0]}-{t[1]:02d}-{t[2]:02d}",
                        "desactualizado": False,
                    }
                except Exception:
                    continue
        raise ValueError("Sin filas válidas en XLS ICG")
    except Exception as e:
        _warn("icg_utdt", e)
        return None


def calcular_score(indicadores: dict) -> float:
    """
    Score 0-10: mayor = mayor tensión política.
    ipc_regulados: tarifas subiendo más que inflación → más decisiones políticas costosas
        var% 0 → 0, 10% → 10. Penaliza más si supera IPC total (brecha positiva).
    icg_utdt: menor confianza en gobierno → mayor tensión
        ICG ~20 → 5, ICG ~40 → 0, ICG <10 → 10
    """
    scores = []

    reg = indicadores.get("ipc_regulados", {})
    reg_val = reg.get("valor")
    if reg_val is not None:
        brecha = reg.get("valor_brecha_vs_ipc", 0) or 0
        base = min(10.0, max(0.0, float(reg_val)))
        bonus = min(3.0, max(-3.0, float(brecha) * 0.3))
        scores.append(min(10.0, max(0.0, base + bonus)))

    icg = indicadores.get("icg_utdt", {}).get("valor")
    if icg is not None:
        scores.append(min(10.0, max(0.0, (40.0 - float(icg)) / 4.0)))

    return round(sum(scores) / len(scores), 1) if scores else 5.0


def main() -> None:
    cache_anterior        = load_cache()
    indicadores_anteriores = cache_anterior.get("indicadores", {})

    frescos: dict  = {}
    frescos_count  = 0

    for nombre, fetcher in [
        ("ipc_regulados", fetch_ipc_regulados),
        ("icg_utdt",      fetch_icg),
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
