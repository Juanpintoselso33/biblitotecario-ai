"""
Colector Cinturón Político — CIGOB
Capital político según Carlos Matus: 5 dimensiones independientes.
Ejecutar desde projects/informe_coyuntura/: python scripts/politica.py

Indicadores:
  votometro_ventaja_lla   — Brecha LLA−PJ en intención de voto (Votómetro CIGOB, auto)
  eficacia_legislativa    — % proyectos oficiales aprobados (manual)
  cohesion_bloque         — % cohesión del bloque LLA en Diputados (manual)
  gobernadores_alineamiento — % gobernadores alineados con política nacional (manual)
  movilizacion_cepa       — Índice de conflictividad social CEPA 0–100 (manual)
"""
import sys
import json
import re
import math
import logging
from datetime import datetime, date, timedelta
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

# ── Paths ─────────────────────────────────────────────────────────────────────
SCRIPT_DIR    = Path(__file__).parent
PROJECT_DIR   = SCRIPT_DIR.parent
CACHE_PATH    = PROJECT_DIR / "output" / "cache" / "politica.json"
MANUALES_PATH = PROJECT_DIR / "data" / "politica" / "manuales.json"
VOTOMETRO_HTML = PROJECT_DIR.parent / "votometro" / "web" / "votometro.html"

CINTURON              = "politica"
INDICADORES_ESPERADOS = [
    "votometro_ventaja_lla",
    "eficacia_legislativa",
    "cohesion_bloque",
    "gobernadores_alineamiento",
    "movilizacion_cepa",
]

# Días sin actualización antes de marcar como desactualizado
STALE_MANUAL_DAYS    = 45
STALE_VOTOMETRO_DAYS = 60

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

        # Extraer bloque encuestasRaw
        m = re.search(r"const\s+encuestasRaw\s*=\s*\[(.*?)\];", html, re.DOTALL)
        if not m:
            raise ValueError("No se encontró encuestasRaw en el HTML")

        raw_block = m.group(1)

        # Parsear cada objeto JS: { campo:valor, ... }
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

        # Filtrar solo tipo espacio
        espacios = [e for e in entries if str(e.get("tipo", "")).strip() == "espacio"]
        if not espacios:
            raise ValueError("Sin encuestas tipo='espacio' en Votómetro")

        # Fecha más reciente entre las de espacio
        fechas = []
        for e in espacios:
            try:
                fechas.append(date.fromisoformat(str(e["fecha"])[:10]))
            except Exception:
                pass
        if not fechas:
            raise ValueError("Sin fechas válidas en encuestas espacio")
        fecha_max = max(fechas)

        # Usar solo encuestas dentro de la ventana de tiempo
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

    Cada dimensión de Matus pesa igual (1/5 del total, o 1/N si hay ausentes).

    votometro_ventaja_lla (gap LLA−PJ en pp):
        gap=+15pp→0, gap=0→5, gap=−15pp→10
    eficacia_legislativa (% 0–100):
        70%→0, 35%→5, 0%→10
    cohesion_bloque (% 0–100):
        95%→0, 60%→5, 25%→10
    gobernadores_alineamiento (% 0–100):
        80%→0, 40%→5, 0%→10
    movilizacion_cepa (índice 0–100):
        0→0, 50→5, 100→10
    """
    scores = []

    vot = indicadores.get("votometro_ventaja_lla", {}).get("valor")
    if vot is not None:
        scores.append(min(10.0, max(0.0, 5.0 - float(vot) / 3.0)))

    efic = indicadores.get("eficacia_legislativa", {}).get("valor")
    if efic is not None:
        scores.append(min(10.0, max(0.0, (70.0 - float(efic)) / 7.0)))

    coh = indicadores.get("cohesion_bloque", {}).get("valor")
    if coh is not None:
        scores.append(min(10.0, max(0.0, (95.0 - float(coh)) / 7.0)))

    gob = indicadores.get("gobernadores_alineamiento", {}).get("valor")
    if gob is not None:
        scores.append(min(10.0, max(0.0, (80.0 - float(gob)) / 8.0)))

    mov = indicadores.get("movilizacion_cepa", {}).get("valor")
    if mov is not None:
        scores.append(min(10.0, max(0.0, float(mov) / 10.0)))

    return round(sum(scores) / len(scores), 1) if scores else 5.0


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    cache_anterior         = load_cache()
    indicadores_anteriores = cache_anterior.get("indicadores", {})

    frescos: dict = {}
    frescos_count = 0

    colectores = [
        ("votometro_ventaja_lla",       fetch_votometro),
        ("eficacia_legislativa",        lambda: fetch_manual("eficacia_legislativa")),
        ("cohesion_bloque",             lambda: fetch_manual("cohesion_bloque")),
        ("gobernadores_alineamiento",   lambda: fetch_manual("gobernadores_alineamiento")),
        ("movilizacion_cepa",           lambda: fetch_manual("movilizacion_cepa")),
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
