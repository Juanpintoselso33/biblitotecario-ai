"""
Colector Salud — datos.salud.gob.ar (CKAN API)
IMPORTANTE: SSL cert roto en el servidor -> verify=False en todos los requests.
Frecuencia: variable (semanas a meses segun dataset).
Datos: defunciones (DEIS), notificaciones epidemiologicas (SNVS), embarazo adolescente.
"""
import logging
import warnings

import requests
from urllib3.exceptions import InsecureRequestWarning

from config import SALUD_CKAN_BASE, HTTP_HEADERS, HTTP_TIMEOUT

warnings.filterwarnings("ignore", category=InsecureRequestWarning)
logger = logging.getLogger(__name__)

_DATASETS_PRIORITARIOS = [
    "defunciones-por-causa",
    "notificaciones-enfermedades",
    "embarazo-adolescente",
    "mortalidad-infantil",
    "mortalidad-materna",
]


def _ckan_get(action: str, params: dict = None) -> dict:
    url = SALUD_CKAN_BASE + action
    r = requests.get(url, params=params or {}, headers=HTTP_HEADERS,
                     timeout=HTTP_TIMEOUT, verify=False)
    r.raise_for_status()
    data = r.json()
    if not data.get("success"):
        raise ValueError(f"CKAN error: {data.get('error', 'unknown')}")
    return data["result"]


def _buscar_recurso_csv(package_id: str) -> dict | None:
    """Devuelve el primer recurso CSV de un package o None."""
    try:
        result = _ckan_get("package_show", {"id": package_id})
        recursos = result.get("resources", [])
        for r in recursos:
            if r.get("format", "").upper() in ("CSV", "XLS", "XLSX"):
                return {
                    "url": r.get("url"),
                    "format": r.get("format"),
                    "name": r.get("name"),
                    "last_modified": r.get("last_modified", r.get("created", "")),
                }
    except Exception as e:
        logger.debug("package_show %s FAIL: %s", package_id, e)
    return None


def _buscar_datasets() -> list[dict]:
    """Busca datasets de salud relevantes en CKAN."""
    try:
        result = _ckan_get("package_search", {"q": "defunciones OR mortalidad OR epidemiologica",
                                               "rows": 20})
        return [{"id": p["id"], "title": p.get("title",""), "name": p.get("name","")}
                for p in result.get("results", [])]
    except Exception as e:
        logger.debug("package_search FAIL: %s", e)
        return []


def fetch_salud() -> dict:
    """Conecta con la API CKAN de datos.salud.gob.ar y retorna metadata de datasets disponibles."""
    results = {}

    # 1) Intentar encontrar datasets prioritarios directamente
    recursos_encontrados = []
    for dataset_name in _DATASETS_PRIORITARIOS:
        recurso = _buscar_recurso_csv(dataset_name)
        if recurso:
            recursos_encontrados.append({"dataset": dataset_name, **recurso})
            logger.info("Salud dataset OK: %s (%s)", dataset_name, recurso.get("last_modified",""))

    if recursos_encontrados:
        results["salud_datasets"] = {
            "valor": len(recursos_encontrados),
            "datasets_disponibles": recursos_encontrados,
            "fuente": "datos.salud.gob.ar — CKAN API",
            "nota": "Datasets DEIS/SNVS disponibles para descarga. Ver 'datasets_disponibles' para URLs directas.",
        }
        return results

    # 2) Fallback: busqueda general
    datasets = _buscar_datasets()
    if datasets:
        results["salud_datasets"] = {
            "valor": len(datasets),
            "datasets_disponibles": datasets[:5],
            "fuente": "datos.salud.gob.ar — CKAN API (busqueda general)",
            "nota": "Usar las URLs de CKAN para descargar microdatos DEIS o SNVS.",
        }
        logger.info("Salud fallback: %d datasets encontrados", len(datasets))
    else:
        logger.error("Salud CKAN: sin resultados")

    return results
