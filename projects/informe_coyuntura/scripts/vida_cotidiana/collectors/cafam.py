"""
Colector CAFAM — Patentamiento de motovehículos
API pública sin autenticación. Verificada 2026-05-10.
Nota: CIAM no existe (DNS falla). La entidad real es CAFAM.
"""
import logging
from datetime import datetime

import requests

from config import CAFAM_API, HTTP_HEADERS, HTTP_TIMEOUT

logger = logging.getLogger(__name__)


def fetch_cafam(year: int | None = None, month: int | None = None) -> dict:
    """
    Descarga el patentamiento de motovehículos del mes indicado (o el actual).
    Retorna total nacional y desglose por provincia.
    """
    now = datetime.today()
    year = year or now.year
    month = month or now.month

    params = {
        "month_start": month,
        "month_end": month,
        "year": year,
        "type": "TODOS",
    }

    try:
        r = requests.get(CAFAM_API, params=params, headers=HTTP_HEADERS, timeout=HTTP_TIMEOUT)
        r.raise_for_status()
        data = r.json()

        total = sum(p["count"] for p in data.get("provinces", []))
        provincias = {p["_id"]: p["count"] for p in data.get("provinces", [])}

        result = {
            "patentamiento_motos": {
                "valor": total,
                "fecha": f"{year}-{month:02d}",
                "unidad": "unidades",
                "provincias": provincias,
                "fuente": "CAFAM API",
            }
        }
        logger.info("CAFAM OK: %d motos en %d-%02d", total, year, month)
        return result

    except Exception as e:
        logger.error("CAFAM FAIL: %s", e)
        return {}
