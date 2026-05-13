"""
Colector INDEC via API datos.gob.ar/series
Sin autenticacion. Todos los IDs verificados al 2026-05-10.
"""
import logging
import requests

from config import DATOS_GOB_BASE, DATOS_GOB_SEARCH, INDEC_SERIES, RIPTE_CSV, HTTP_HEADERS, HTTP_TIMEOUT

logger = logging.getLogger(__name__)


def _get_serie(series_id: str, limit: int = 2) -> list:
    params = {"ids": series_id, "format": "json", "limit": limit, "sort": "desc"}
    r = requests.get(DATOS_GOB_BASE, params=params, headers=HTTP_HEADERS, timeout=HTTP_TIMEOUT)
    r.raise_for_status()
    return r.json()["data"]


def _ultimo(series_id: str) -> dict:
    data = _get_serie(series_id, limit=1)
    return {"valor": data[0][1], "fecha": data[0][0]}


def _var_mensual(series_id: str) -> dict:
    data = _get_serie(series_id, limit=2)
    actual, anterior = data[0][1], data[1][1]
    var = (actual / anterior - 1) * 100 if anterior else None
    return {"valor": actual, "variacion_mensual_pct": var, "fecha": data[0][0]}


def search_serie(query: str, limit: int = 10) -> list[dict]:
    r = requests.get(DATOS_GOB_SEARCH, params={"q": query, "limit": limit},
                     headers=HTTP_HEADERS, timeout=HTTP_TIMEOUT)
    r.raise_for_status()
    return [{"id": s["field"]["id"], "description": s["field"].get("description",""),
             "frequency": s["field"].get("frequency",""), "end": s["field"].get("time_index_end","")}
            for s in r.json().get("data", [])]


def _get_ripte() -> dict:
    """RIPTE via CSV directo. Mensual desde jul-1994."""
    import io
    r = requests.get(RIPTE_CSV, headers=HTTP_HEADERS, timeout=HTTP_TIMEOUT)
    r.raise_for_status()
    lines = [l for l in r.text.strip().split("\n") if l.strip() and not l.startswith("indice")]
    if not lines:
        raise ValueError("RIPTE CSV vacio")
    last = lines[-1].split(",")
    return {"valor": float(last[1]), "fecha": last[0]}


def fetch_indec() -> dict:
    results = {}

    # ── Precios ──────────────────────────────────────────────────────────────
    for key in ["ipc_total", "ipc_alimentos", "ipc_vivienda", "ipc_regulados"]:
        try:
            results[key] = _var_mensual(INDEC_SERIES[key])
            logger.info("%s OK: %s", key, results[key]["fecha"])
        except Exception as e:
            logger.error("%s FAIL: %s", key, e)

    # ── Canasta Basica Total ─────────────────────────────────────────────────
    for key in ["cbt", "cba"]:
        try:
            results[key] = _var_mensual(INDEC_SERIES[key])
            logger.info("%s OK: $%s", key, results[key]["valor"])
        except Exception as e:
            logger.error("%s FAIL: %s", key, e)

    # ── RIPTE + Brecha salario vs CBT ────────────────────────────────────────
    try:
        ripte = _get_ripte()
        results["ripte"] = ripte
        if "cbt" in results:
            cbt_val = results["cbt"]["valor"]
            brecha = (ripte["valor"] / cbt_val) if cbt_val else None
            results["brecha_salario_cbt"] = {
                "valor": brecha,
                "ripte_pesos": ripte["valor"],
                "cbt_pesos": cbt_val,
                "canastas_que_cubre": brecha,
                "fecha": ripte["fecha"],
                "nota": "RIPTE / CBT: canastas cubiertas por el salario imponible promedio",
            }
            logger.info("Brecha sal/CBT OK: %.2f canastas", brecha)
    except Exception as e:
        logger.error("RIPTE FAIL: %s", e)

    # ── Salarios ─────────────────────────────────────────────────────────────
    try:
        results["isalarios_total"] = _var_mensual(INDEC_SERIES["isalarios_total"])
    except Exception as e:
        logger.error("isalarios FAIL: %s", e)

    # ── Salario real (deflactado por IPC) ────────────────────────────────────
    if "ipc_total" in results and "isalarios_total" in results:
        sal = results["isalarios_total"]["valor"]
        ipc = results["ipc_total"]["valor"]
        results["salario_real_indice"] = {
            "valor": sal / ipc * 100,
            "fecha": results["isalarios_total"]["fecha"],
            "nota": "Salario nominal / IPC * 100",
        }

    # ── Empleo y mercado laboral ──────────────────────────────────────────────
    for key in ["desocupacion", "empleo", "subocupacion_demandante"]:
        try:
            results[key] = _ultimo(INDEC_SERIES[key])
            logger.info("%s OK: %s", key, results[key]["valor"])
        except Exception as e:
            logger.error("%s FAIL: %s", key, e)

    # Informalidad (anual)
    try:
        results["informalidad_anual"] = _ultimo(INDEC_SERIES["informalidad_anual"])
        logger.info("informalidad OK: %s%%", results["informalidad_anual"]["valor"])
    except Exception as e:
        logger.error("informalidad FAIL: %s", e)

    # ── Actividad / Industria ─────────────────────────────────────────────────
    for key in ["isac", "emae", "ipi"]:
        try:
            results[key] = _var_mensual(INDEC_SERIES[key])
        except Exception as e:
            logger.error("%s FAIL: %s", key, e)

    # ── Faena vacuna (proxy consumo carne) ───────────────────────────────────
    try:
        results["faena_vacuna"] = _var_mensual(INDEC_SERIES["faena_vacuna"])
        logger.info("faena_vacuna OK")
    except Exception as e:
        logger.error("faena_vacuna FAIL: %s", e)

    # ── Acero crudo (hierro/construccion) ────────────────────────────────────
    try:
        results["acero_crudo"] = _var_mensual(INDEC_SERIES["acero_crudo"])
        logger.info("acero_crudo OK")
    except Exception as e:
        logger.error("acero_crudo FAIL: %s", e)

    return results
