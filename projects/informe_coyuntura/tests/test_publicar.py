import json, subprocess, sys, os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]   # projects/informe_coyuntura
DATA = ROOT / "web" / "src" / "data"
sys.path.insert(0, str(ROOT))                # para importar config.py

def test_publicar_genera_snapshot():
    subprocess.run([sys.executable, "scripts/publicar.py"], cwd=ROOT, check=True)
    informe = json.loads((DATA / "informe.json").read_text(encoding="utf-8"))
    series = json.loads((DATA / "series.json").read_text(encoding="utf-8"))

    # 4 cinturones presentes
    assert set(informe["cinturones"]) == {"macro", "politica", "vida_cotidiana", "gestion"}

    # vida_cotidiana enriquecido: al menos 10 indicadores (no los 3 legacy)
    vida = informe["cinturones"]["vida_cotidiana"]["indicadores"]
    assert len(vida) >= 10, f"vida cotidiana solo tiene {len(vida)} indicadores"
    assert "consumo_carne" in vida and "icc_utdt" in vida

    # cada indicador tiene la forma mínima
    for cint in informe["cinturones"].values():
        for ind in cint["indicadores"].values():
            assert "unidad" in ind and "fecha_dato" in ind and "desactualizado" in ind

    # series: dict de listas {fecha, valor} ordenadas asc
    assert isinstance(series, dict) and "tcrm" in series
    fechas = [p["fecha"] for p in series["tcrm"]]
    assert fechas == sorted(fechas)


def test_aporte_score_reconcilia_con_score_publicado():
    """El promedio de los aportes por indicador debe reproducir el score del
    cinturón. Para macro/política/gestión esto compara contra el score que computa
    el colector de forma independiente: si una fórmula deriva, el test falla.
    Para vida el score se computa acá mismo a partir de los aportes (su scoring
    vive en publicar.py), así que la igualdad confirma coherencia interna."""
    informe = json.loads((DATA / "informe.json").read_text(encoding="utf-8"))
    for ck in ("macro", "politica", "gestion", "vida_cotidiana"):
        c = informe["cinturones"][ck]
        aportes = [i["aporte_score"] for i in c["indicadores"].values()
                   if i.get("aporte_score") is not None]
        assert aportes, f"{ck}: ningún indicador tiene aporte_score"
        promedio = round(sum(aportes) / len(aportes), 1)
        assert abs(promedio - c["score"]) <= 0.1, \
            f"{ck}: promedio de aportes {promedio} != score publicado {c['score']}"


def test_score_global_reconcilia_con_pesos():
    """El score global debe ser el promedio ponderado de los 4 cinturones."""
    from config import PESOS_CINTURONES
    informe = json.loads((DATA / "informe.json").read_text(encoding="utf-8"))
    num = sum(c["score"] * PESOS_CINTURONES.get(k, 0.0)
              for k, c in informe["cinturones"].items())
    den = sum(PESOS_CINTURONES.get(k, 0.0) for k in informe["cinturones"])
    esperado = round(num / den, 1)
    assert abs(esperado - informe["score_global"]) <= 0.1, \
        f"global {informe['score_global']} != ponderado {esperado}"


def test_vida_indicadores_aportan_al_score():
    """Vida: al menos 12 de 13 indicadores entran al score con fórmula."""
    informe = json.loads((DATA / "informe.json").read_text(encoding="utf-8"))
    vida = informe["cinturones"]["vida_cotidiana"]["indicadores"]
    con_aporte = [k for k, i in vida.items() if i.get("aporte_score") is not None]
    assert len(con_aporte) >= 12, f"vida: sólo {len(con_aporte)} con aporte"


def test_endeudamiento_se_puntua_por_variacion_real():
    """Endeudamiento se puntúa sobre su variación interanual real (no el stock
    nominal): debe tener var_real_12m y un aporte derivado de ella."""
    informe = json.loads((DATA / "informe.json").read_text(encoding="utf-8"))
    end = informe["cinturones"]["vida_cotidiana"]["indicadores"]["endeudamiento_familiar"]
    assert isinstance(end.get("var_real_12m"), (int, float)), "falta var_real_12m"
    assert end.get("aporte_score") is not None, "endeudamiento sin aporte"
    # tensión = clamp(5 + var_real/4)
    esperado = max(0.0, min(10.0, round(5 + end["var_real_12m"] / 4, 1)))
    assert abs(end["aporte_score"] - esperado) <= 0.1
