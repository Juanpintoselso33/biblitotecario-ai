"""
Colector Google Trends — sentimiento / interes digital en Argentina
Usa pytrends (no requiere API key).
IMPORTANTE: urllib3 v2 rompe pytrends — monkey-patch aplicado aqui.
Rate limits: Google bloquea requests frecuentes. Aceptar fallas silenciosas.
Frecuencia: tiempo real (promedio 7-90 dias segun escala elegida).
"""
import logging
import time

from config import TRENDS_KEYWORDS, TRENDS_GEO

logger = logging.getLogger(__name__)


def _patch_urllib3():
    """
    pytrends usa Retry(method_whitelist=...) que fue renombrado a allowed_methods en urllib3 v2.
    Patch aplicado antes de importar pytrends para evitar TypeError en runtime.
    """
    try:
        import urllib3.util.retry as _retry_mod
        retry_cls = _retry_mod.Retry
        if not hasattr(retry_cls, "_default_allowed_methods_compat_applied"):
            _orig_init = retry_cls.__init__

            def _patched_init(self, *args, **kwargs):
                if "method_whitelist" in kwargs:
                    kwargs.setdefault("allowed_methods", kwargs.pop("method_whitelist"))
                _orig_init(self, *args, **kwargs)

            retry_cls.__init__ = _patched_init
            retry_cls._default_allowed_methods_compat_applied = True
    except Exception as e:
        logger.debug("urllib3 patch SKIP: %s", e)


def _fetch_trends(keywords: list[str], geo: str, timeframe: str = "today 3-m") -> dict:
    """Retorna interes relativo (0-100) para cada keyword en el periodo."""
    _patch_urllib3()
    from pytrends.request import TrendReq

    pt = TrendReq(hl="es-AR", tz=-180, timeout=(10, 30), retries=2, backoff_factor=0.5)
    pt.build_payload(keywords, cat=0, timeframe=timeframe, geo=geo, gprop="")
    df = pt.interest_over_time()

    if df is None or df.empty:
        return {}

    # Promedio de los ultimos 4 periodos por keyword
    tail = df[keywords].tail(4)
    return {kw: round(float(tail[kw].mean()), 1) for kw in keywords if kw in tail.columns}


def fetch_trends() -> dict:
    """Descarga interes relativo en Google Trends para palabras clave de vida cotidiana."""
    results = {}

    try:
        interes = _fetch_trends(TRENDS_KEYWORDS, TRENDS_GEO, timeframe="today 3-m")
        if not interes:
            raise ValueError("DataFrame vacio — posible rate limit")

        results["sentimiento_digital"] = {
            "interes_relativo": interes,
            "keywords": TRENDS_KEYWORDS,
            "geo": TRENDS_GEO,
            "timeframe": "ultimos 3 meses",
            "escala": "0-100 (100 = maximo historico en el periodo)",
            "fuente": "Google Trends via pytrends",
            "nota": (
                "Proxy de urgencia percibida. Alto 'inseguridad'/'precios' = presion ciudadana. "
                "Sujeto a rate limits de Google — puede fallar silenciosamente."
            ),
        }
        logger.info("Trends OK: %s", interes)

    except Exception as e:
        logger.warning("Trends FAIL (normal si hay rate limit): %s", e)
        # Fallback: retornar estructura vacia pero documentada
        results["sentimiento_digital"] = {
            "interes_relativo": None,
            "keywords": TRENDS_KEYWORDS,
            "geo": TRENDS_GEO,
            "fuente": "Google Trends via pytrends",
            "nota": f"Rate limit o error de conexion: {e}. Reintentar en 1h.",
        }

    return results
