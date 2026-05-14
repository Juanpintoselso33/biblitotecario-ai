"""
Colector Cinturón Político — CIGOB
Capital político según Carlos Matus: 5 dimensiones independientes.
Ejecutar desde projects/informe_coyuntura/: python scripts/politica.py

Indicadores:
  votometro_ventaja_lla     — Brecha LLA−PJ en intención de voto (Votómetro CIGOB, auto)
  icg_utdt                  — Índice de Confianza en el Gobierno UTDT (datos.gob.ar, auto)
  movilizacion_cepa         — Conflictividad social CEPA 0–100 (scrape centrocepa.com.ar, auto)
  cohesion_bloque           — % cohesión del bloque LLA en Diputados (manual)
  eficacia_legislativa      — % proyectos oficiales aprobados (manual)
  gobernadores_alineamiento — % gobernadores alineados con política nacional (manual)
"""
import sys
import json
import re
import math
import logging
import requests
import urllib3
from datetime import datetime, date, timedelta
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ── Paths ─────────────────────────────────────────────────────────────────────
SCRIPT_DIR    = Path(__file__).parent
PROJECT_DIR   = SCRIPT_DIR.parent
CACHE_PATH    = PROJECT_DIR / "output" / "cache" / "politica.json"
MANUALES_PATH = PROJECT_DIR / "data" / "politica" / "manuales.json"
VOTOMETRO_HTML = PROJECT_DIR.parent / "votometro" / "web" / "votometro.html"

CINTURON              = "politica"
INDICADORES_ESPERADOS = [
    "votometro_ventaja_lla",
    "icg_utdt",
    "movilizacion_cepa",
    "cohesion_bloque",
    "eficacia_legislativa",
    "gobernadores_alineamiento",
]

# Días sin actualización antes de marcar como desactualizado
STALE_MANUAL_DAYS    = 45
STALE_VOTOMETRO_DAYS = 60
STALE_ICG_DAYS       = 120   # ICG es trimestral

HTTP_TIMEOUT = 20
HTTP_HEADERS = {"User-Agent": "CIGOB-InformeCoyuntura/1.0"}

INDEC_BASE      = "https://apis.datos.gob.ar/series/api/series/"
ICG_SERIES_ID   = "370.2_ICG_NIVEL_RAL_0_0_17_40"

CEPA_INFORMES_URL       = "https://centrocepa.com.ar/informes"
CEPA_MAX_CASOS_MES      = 80.0    # 80 casos/mes = 100 en la escala normalizada
CEPA_MAX_CONFLICTOS_TOT = 200.0   # 200 conflictos acumulados = 100 en la escala (total desde inicio de período)

logging.basicConfig(level=logging.WARNING, format="%(message)s")


# ── Cache helpers ─────────────────────────────────────────────────────────────

def load_cache() -> dict:
    if CACHE_PATH.exists():
        with open(CACHE_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_cache(data: dict) -> None:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)


def _warn(indicador: str, msg: str) -> None:
    print(f"[WARN] {CINTURON}.{indicador}: {msg}. Usando cache.")


def _days_old(fecha_str: str) -> int:
    try:
        fecha = date.fromisoformat(str(fecha_str)[:10])
        return (date.today() - fecha).days
    except Exception:
        return 999


# ── Votómetro parser ──────────────────────────────────────────────────────────

def fetch_votometro() -> dict | None:
    """
    Parsea encuestasRaw del Votómetro CIGOB y calcula la brecha ponderada LLA−PJ.

    Filtros:
    - tipo='espacio' (porcentajes de espacio político, no candidatos individuales)
    - últimos STALE_VOTOMETRO_DAYS días desde la encuesta más reciente

    Peso = exp(−0.015 × días) × calidad_mult  donde A=3, B=2, C=1
    """
    try:
        if not VOTOMETRO_HTML.exists():
            raise FileNotFoundError(f"Votómetro no encontrado: {VOTOMETRO_HTML}")

        with open(VOTOMETRO_HTML, encoding="utf-8") as f:
            html = f.read()

        m = re.search(r"const\s+encuestasRaw\s*=\s*\[(.*?)\];", html, re.DOTALL)
        if not m:
            raise ValueError("No se encontró encuestasRaw en el HTML")

        raw_block = m.group(1)

        entries = []
        for obj in re.finditer(r"\{([^}]+)\}", raw_block):
            fields = {}
            for kv in re.finditer(r"(\w+)\s*:\s*'([^']*)'|(\w+)\s*:\s*([\d.]+)", obj.group(1)):
                if kv.group(1):
                    fields[kv.group(1)] = kv.group(2)
                else:
                    fields[kv.group(3)] = float(kv.group(4))
            if fields:
                entries.append(fields)

        espacios = [e for e in entries if str(e.get("tipo", "")).strip() == "espacio"]
        if not espacios:
            raise ValueError("Sin encuestas tipo='espacio' en Votómetro")

        fechas = []
        for e in espacios:
            try:
                fechas.append(date.fromisoformat(str(e["fecha"])[:10]))
            except Exception:
                pass
        if not fechas:
            raise ValueError("Sin fechas válidas en encuestas espacio")
        fecha_max = max(fechas)

        cutoff = (fecha_max - timedelta(days=STALE_VOTOMETRO_DAYS)).isoformat()
        recientes = [e for e in espacios if str(e.get("fecha", "")) >= cutoff]
        if not recientes:
            raise ValueError("Sin encuestas espacio recientes en ventana de tiempo")

        CALIDAD_MULT = {"A": 3.0, "B": 2.0, "C": 1.0}
        LAMBDA = 0.015

        suma_peso = 0.0
        suma_lla  = 0.0
        suma_pj   = 0.0

        for e in recientes:
            try:
                fecha_enc = date.fromisoformat(str(e["fecha"])[:10])
                dias = (date.today() - fecha_enc).days
                wT = math.exp(-LAMBDA * dias)
                cal = str(e.get("calidad", "B")).strip().upper()
                wC = CALIDAD_MULT.get(cal, 2.0)
                w  = wT * wC

                lla = float(e.get("LLA", 0))
                pj  = float(e.get("PJ", 0))

                suma_peso += w
                suma_lla  += w * lla
                suma_pj   += w * pj
            except Exception:
                continue

        if suma_peso == 0:
            raise ValueError("Suma de pesos = 0")

        lla_pond = round(suma_lla / suma_peso, 1)
        pj_pond  = round(suma_pj / suma_peso, 1)
        gap      = round(lla_pond - pj_pond, 1)

        return {
            "valor": gap,
            "lla_ponderado": lla_pond,
            "pj_ponderado": pj_pond,
            "n_encuestas": len(recientes),
            "unidad": "pp (LLA − PJ)",
            "fuente": str(VOTOMETRO_HTML),
            "fecha_dato": str(fecha_max),
            "desactualizado": _days_old(str(fecha_max)) > STALE_VOTOMETRO_DAYS,
        }

    except Exception as e:
        _warn("votometro_ventaja_lla", str(e))
        return None


# ── ICG UTDT ──────────────────────────────────────────────────────────────────

def fetch_icg_utdt() -> dict | None:
    """
    Índice de Confianza en el Gobierno — UTDT, escala 0–5 (mayor = mayor confianza).
    Serie trimestral publicada en datos.gob.ar.
    Dimensión: confianza institucional (Matus).
    """
    try:
        r = requests.get(
            INDEC_BASE,
            params={"ids": ICG_SERIES_ID, "format": "json", "limit": 1, "sort": "desc"},
            headers=HTTP_HEADERS,
            timeout=HTTP_TIMEOUT,
        )
        r.raise_for_status()
        data = r.json().get("data", [])
        if not data or data[0][1] is None:
            raise ValueError("Sin datos en la respuesta de la API")

        fecha, valor = data[0][0], data[0][1]
        return {
            "valor": round(float(valor), 2),
            "unidad": "índice 0–5 (ICG Nivel General UTDT, mayor = mayor confianza)",
            "fuente": f"datos.gob.ar series {ICG_SERIES_ID}",
            "fecha_dato": str(fecha)[:10],
            "desactualizado": _days_old(str(fecha)[:10]) > STALE_ICG_DAYS,
        }

    except Exception as e:
        _warn("icg_utdt", str(e))
        return None


# ── CEPA conflictividad ───────────────────────────────────────────────────────

def fetch_cepa_movilizacion() -> dict | None:
    """
    Conflictividad social CEPA — índice 0–100 normalizado.
    Estrategia: listar centrocepa.com.ar/informes → encontrar el último informe
    con "conflictividad" en la URL → parsear HTML del informe buscando
    "X casos por mes" → normalizar (80 casos/mes = 100).
    Dimensión: conflicto social (Matus).
    """
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        _warn("movilizacion_cepa", "beautifulsoup4 no disponible")
        return None

    try:
        # Paso 1: página de listado de informes
        r = requests.get(CEPA_INFORMES_URL, headers=HTTP_HEADERS, timeout=HTTP_TIMEOUT)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        links = [
            a for a in soup.find_all("a", href=True)
            if "conflictividad" in a.get("href", "").lower()
        ]
        if not links:
            raise ValueError("No se encontraron links de conflictividad en la página de informes CEPA")

        # Ordenar por número en la URL (mayor número = más reciente)
        def url_num(a):
            m = re.search(r"/(\d+)[/-]", a["href"])
            return int(m.group(1)) if m else 0

        links.sort(key=url_num, reverse=True)
        href = links[0]["href"]
        informe_url = ("https://centrocepa.com.ar" + href) if href.startswith("/") else href

        # Paso 2: página del informe
        r2 = requests.get(informe_url, headers=HTTP_HEADERS, timeout=HTTP_TIMEOUT)
        r2.raise_for_status()

        # Paso 3: extraer cifra de conflictividad — varios patrones posibles en los informes CEPA

        # Patrón A: "X casos por mes" o "promedio de X casos mensuales"
        m_mes = re.search(
            r"(\d+(?:[.,]\d+)?)\s+casos?\s+por\s+mes"
            r"|promedio\s+de\s+(\d+(?:[.,]\d+)?)\s+casos?\s+mensuales?",
            r2.text, re.IGNORECASE
        )
        # Patrón B: "al menos[,] N conflictos" o "se registraron[,] N conflictos"
        m_tot = re.search(
            r"(?:al menos,?\s+|se registraron,?\s+al menos,?\s+|se registraron\s+)"
            r"(\d+)\s+conflictos?",
            r2.text, re.IGNORECASE
        )

        if m_mes:
            raw = (m_mes.group(1) or m_mes.group(2)).replace(",", ".")
            cifra = float(raw)
            val = round(min(100.0, (cifra / CEPA_MAX_CASOS_MES) * 100.0), 1)
            metrica = f"{cifra} casos/mes"
        elif m_tot:
            cifra = float(m_tot.group(1))
            val = round(min(100.0, (cifra / CEPA_MAX_CONFLICTOS_TOT) * 100.0), 1)
            metrica = f"{cifra} conflictos acumulados"
        else:
            raise ValueError(f"No se encontró patrón de conflictividad en {informe_url}")

        return {
            "valor": val,
            "cifra_cruda": cifra,
            "metrica": metrica,
            "unidad": "índice 0–100 (normalizado)",
            "fuente": informe_url,
            "fecha_dato": str(date.today()),
            "desactualizado": False,
        }

    except Exception as e:
        _warn("movilizacion_cepa", str(e))
        return None


# ── Colectores manuales ───────────────────────────────────────────────────────

def load_manuales() -> dict:
    if not MANUALES_PATH.exists():
        return {}
    with open(MANUALES_PATH, encoding="utf-8") as f:
        data = json.load(f)
    data.pop("_meta", None)
    return data


def fetch_manual(nombre: str, stale_days: int = STALE_MANUAL_DAYS) -> dict | None:
    manuales = load_manuales()
    entry = manuales.get(nombre)
    if entry is None:
        _warn(nombre, f"No encontrado en {MANUALES_PATH}")
        return None
    if entry.get("valor") is None:
        _warn(nombre, "valor = null en manuales.json")
        return None

    dias = _days_old(str(entry.get("fecha_dato", "")))
    return {
        **entry,
        "desactualizado": dias > stale_days,
    }


# ── Score ─────────────────────────────────────────────────────────────────────

def calcular_score(indicadores: dict) -> float:
    """
    Score 0–10: mayor = mayor tensión en capital político.
    Cada dimensión de Matus pesa igual (1/N disponibles).

    votometro_ventaja_lla (gap LLA−PJ en pp):
        +15pp→0, 0→5, −15pp→10
    icg_utdt (ICG 0–5, mayor = mayor confianza):
        3.5→0, 1.75→5, 0→10 (menor confianza = mayor tensión)
    movilizacion_cepa (índice 0–100):
        0→0, 50→5, 100→10
    eficacia_legislativa (% 0–100):
        70%→0, 35%→5, 0%→10
    cohesion_bloque (% 0–100):
        95%→0, 60%→5, 25%→10
    gobernadores_alineamiento (% 0–100):
        80%→0, 40%→5, 0%→10
    """
    scores = []

    vot = indicadores.get("votometro_ventaja_lla", {}).get("valor")
    if vot is not None:
        scores.append(min(10.0, max(0.0, 5.0 - float(vot) / 3.0)))

    icg = indicadores.get("icg_utdt", {}).get("valor")
    if icg is not None:
        scores.append(min(10.0, max(0.0, (3.5 - float(icg)) / 0.35)))

    cepa = indicadores.get("movilizacion_cepa", {}).get("valor")
    if cepa is not None:
        scores.append(min(10.0, max(0.0, float(cepa) / 10.0)))

    efic = indicadores.get("eficacia_legislativa", {}).get("valor")
    if efic is not None:
        scores.append(min(10.0, max(0.0, (70.0 - float(efic)) / 7.0)))

    coh = indicadores.get("cohesion_bloque", {}).get("valor")
    if coh is not None:
        scores.append(min(10.0, max(0.0, (95.0 - float(coh)) / 7.0)))

    gob = indicadores.get("gobernadores_alineamiento", {}).get("valor")
    if gob is not None:
        scores.append(min(10.0, max(0.0, (80.0 - float(gob)) / 8.0)))

    return round(sum(scores) / len(scores), 1) if scores else 5.0


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    cache_anterior         = load_cache()
    indicadores_anteriores = cache_anterior.get("indicadores", {})

    frescos: dict = {}
    frescos_count = 0

    colectores = [
        ("votometro_ventaja_lla",       fetch_votometro),
        ("icg_utdt",                    fetch_icg_utdt),
        ("movilizacion_cepa",           fetch_cepa_movilizacion),
        ("cohesion_bloque",             lambda: fetch_manual("cohesion_bloque")),
        ("eficacia_legislativa",        lambda: fetch_manual("eficacia_legislativa")),
        ("gobernadores_alineamiento",   lambda: fetch_manual("gobernadores_alineamiento")),
    ]

    for nombre, fetcher in colectores:
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
