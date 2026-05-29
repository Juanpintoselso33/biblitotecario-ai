import json, subprocess, sys, os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]   # projects/informe_coyuntura
DATA = ROOT / "web" / "src" / "data"

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
    cinturón. Esto mantiene honesto el desglose: si una fórmula del colector
    cambia, el score publicado se mueve y este test falla."""
    informe = json.loads((DATA / "informe.json").read_text(encoding="utf-8"))
    for ck in ("macro", "politica", "gestion"):
        c = informe["cinturones"][ck]
        aportes = [i["aporte_score"] for i in c["indicadores"].values()
                   if i.get("aporte_score") is not None]
        assert aportes, f"{ck}: ningún indicador tiene aporte_score"
        promedio = round(sum(aportes) / len(aportes), 1)
        assert abs(promedio - c["score"]) <= 0.1, \
            f"{ck}: promedio de aportes {promedio} != score publicado {c['score']}"


def test_vida_solo_icc_aporta_resto_es_contexto():
    """En vida cotidiana sólo ICC entra al score; el resto se marca contexto."""
    informe = json.loads((DATA / "informe.json").read_text(encoding="utf-8"))
    vida = informe["cinturones"]["vida_cotidiana"]["indicadores"]
    assert vida["icc_utdt"]["aporte_score"] is not None
    contexto = [k for k, i in vida.items()
                if i.get("aporte_score") is None and i.get("aporte_nota")]
    assert len(contexto) >= 10, f"vida: sólo {len(contexto)} marcados como contexto"
