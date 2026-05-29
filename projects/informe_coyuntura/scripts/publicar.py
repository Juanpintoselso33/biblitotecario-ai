"""Arma el snapshot de datos que consume la web del informe de coyuntura.

Lee output/informe.json + el ultimo vida_cotidiana_*.json + output/series/*.csv
y escribe web/src/data/informe.json (con vida cotidiana enriquecido a ~13
indicadores automaticos) y web/src/data/series.json.
"""
import csv, glob, json, os, re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]          # projects/informe_coyuntura
OUT = ROOT / "output"
DATA = ROOT / "web" / "src" / "data"
DATA.mkdir(parents=True, exist_ok=True)


def _add(out, key, valor, unidad, fuente, fecha, **extra):
    d = {"valor": valor, "unidad": unidad, "fuente": fuente,
         "fecha_dato": fecha, "desactualizado": False}
    d.update(extra)
    out[key] = d


def build_vida(raw):
    """Mapea el JSON crudo (por fuente) a indicadores estilo informe.json."""
    indec = raw.get("indec", {}); bcra = raw.get("bcra", {})
    utdt = raw.get("utdt", {}); cafam = raw.get("cafam", {})
    ciccra = raw.get("ciccra", {}); snic = raw.get("snic", {})
    trends = raw.get("trends", {})
    ts = raw.get("metadata", {}).get("timestamp", "")[:10]
    out = {}

    bs = indec.get("brecha_salario_cbt", {})
    _add(out, "brecha_salario_cbt", round(bs.get("valor", 0), 2),
         "canastas (RIPTE/CBT)", "INDEC", bs.get("fecha"))
    al = indec.get("ipc_alimentos", {})
    _add(out, "ipc_alimentos", round(al.get("variacion_mensual_pct", 0), 2),
         "% m/m", "INDEC serie 146.3", al.get("fecha"))
    cc = bcra.get("credito_consumo_total", {})
    # El crédito de consumo viene en millones de pesos; pasar a billones para
    # que el número no sea gigante (43.560.544 millones = 43,56 billones).
    cc_val = cc.get("valor")
    _add(out, "endeudamiento_familiar",
         round(cc_val / 1e6, 2) if isinstance(cc_val, (int, float)) else cc_val,
         "billones de pesos (consumo)", "BCRA API v4.0", cc.get("fecha"))
    reg = indec.get("ipc_regulados", {})
    _add(out, "peso_tarifas", round(reg.get("variacion_mensual_pct", 0), 2),
         "% m/m regulados", "INDEC", reg.get("fecha"))
    carne = ciccra.get("consumo_carne_per_capita", {})
    _add(out, "consumo_carne", carne.get("valor"),
         "kg/hab/año", "CICCRA", carne.get("fecha"))
    inf = indec.get("informalidad_anual", {})
    _add(out, "informalidad", round(inf.get("valor", 0) * 100, 1),
         "%", "INDEC EPH", inf.get("fecha"))
    ipi = indec.get("ipi", {})
    _add(out, "mortalidad_pymes", round(ipi.get("variacion_mensual_pct", 0), 2),
         "% m/m (IPI)", "INDEC", ipi.get("fecha"))
    isac = indec.get("isac", {})
    _add(out, "despacho_cemento", round(isac.get("valor", 0), 1),
         "índice ISAC", "INDEC", isac.get("fecha"))
    sub = indec.get("subocupacion_demandante", {})
    _add(out, "pluriempleo", round(sub.get("valor", 0) * 100, 1),
         "%", "INDEC EPH", sub.get("fecha"))
    seg = snic.get("inseguridad_snic", {})
    _add(out, "inseguridad", seg.get("total_hechos"),
         "hechos/año", "SNIC", str(seg.get("anio")))
    icc = utdt.get("icc_utdt", {})
    _add(out, "icc_utdt", round(icc.get("valor", 0), 1),
         "índice", "UTDT", icc.get("fecha"))
    sd = trends.get("sentimiento_digital", {}).get("interes_relativo", {})
    if sd:
        _add(out, "sentimiento_digital", round(sum(sd.values()) / len(sd), 1),
             "interés 0–100", "Google Trends", ts)
    motos = cafam.get("patentamiento_motos", {})
    _add(out, "patentamiento_motos", motos.get("valor"),
         "unidades", "CAFAM", motos.get("fecha"))
    return out


def build_series():
    """Agrupa output/series/*.csv en {indicador: [{fecha, valor}, ...]} asc."""
    series = {}
    for csv_path in sorted(glob.glob(str(OUT / "series" / "*.csv"))):
        with open(csv_path, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                ind = row["indicador"]
                try:
                    val = float(row["valor"])
                except (TypeError, ValueError):
                    continue
                series.setdefault(ind, []).append({"fecha": row["fecha"], "valor": val})
    for ind in series:
        series[ind].sort(key=lambda p: p["fecha"])
    # Alias: algunos indicadores del informe tienen su serie historica bajo otra
    # clave en los CSV. Exponer la serie tambien bajo la clave del indicador para
    # que el sparkline y el modal la encuentren.
    alias = {
        "despacho_cemento": "isac_construccion",
        "peso_tarifas": "ipc_regulados",
        "saldo_comercial_12m": "saldo_comercial",
    }
    for ind_key, serie_key in alias.items():
        if serie_key in series and ind_key not in series:
            series[ind_key] = series[serie_key]
    return series


_LOCAL_PATH = re.compile(r"^[A-Za-z]:[\\/]|[\\/]Users[\\/]|\\\\")


def sanitizar_fuentes(informe):
    """Reemplaza rutas locales del filesystem en los campos `fuente` para no
    filtrar paths del equipo en el snapshot publico ni en la lista de fuentes."""
    for cint in informe["cinturones"].values():
        for key, ind in cint["indicadores"].items():
            fuente = ind.get("fuente")
            if isinstance(fuente, str) and _LOCAL_PATH.search(fuente):
                ind["fuente"] = ("Votómetro CIGOB" if "votometro" in key.lower()
                                 else "Elaboración propia — CIGOB")
    return informe


# ── Aporte al score por indicador ──────────────────────────────────────────────
# Fuente única de verdad de la transparencia del scoring: replica EXACTAMENTE las
# fórmulas de tensión documentadas en los colectores (macro.py, politica.py,
# gestion.py). El texto de mapeo viene verbatim de esas docstrings. Un test de
# reconciliación (tests/test_publicar.py) verifica que el promedio de los aportes
# reproduce el score publicado de cada cinturón — si una fórmula cambia, el test
# avisa y esto deja de ser una caja negra.

def _clamp10(x):
    return round(max(0.0, min(10.0, x)), 1)

# clave de indicador → (valor → tensión 0–10, texto de mapeo de referencia)
SCORING = {
    # ── macro ──
    "ipc_total":           (lambda v: v,                  "0% → 0 · 5% → 5 · 10% → 10 (mensual)"),
    "reservas_bcra":       (lambda v: (40000 - v) / 4000, "≥40.000 → 0 · 20.000 → 5 · 0 → 10 (US$ M)"),
    "badlar":              (lambda v: v / 10,             "0% → 0 · 50% → 5 · 100% → 10 (anual)"),
    "emae_ia":             (lambda v: 5 - v,              "+5% → 0 · 0% → 5 · −5% → 10 (i.a.)"),
    "saldo_comercial_12m": (lambda v: 5 - v / 1200,       "+6.000 → 0 · 0 → 5 · −6.000 → 10 (US$ M, 12m)"),
    "recaudacion":         (lambda v: 5 - v,              "+5% → 0 · 0% → 5 · −5% → 10 (var. m/m nominal)"),
    "tcrm":                (lambda v: (100 - v) / 5,      "100 → 0 · 75 → 5 · 50 → 10 (índice 2010)"),
    "rem_ipc_12m":         (lambda v: (v - 10) / 9,       "10% → 0 · 55% → 5 · 100% → 9 (anual)"),
    "prestamos_privados":  (lambda v: 5 - v,              "+5% → 0 · 0% → 5 · −5% → 10 (var. m/m nominal)"),
    "base_monetaria":      (lambda v: v / 2,              "0% → 0 · 10% → 5 · 20% → 10 (var. m/m nominal)"),
    "tc_mayorista":        (lambda v: v / 2,              "0% → 0 · 10% → 5 · 20% → 10 (var. m/m)"),
    # ── política ──
    "votometro_ventaja_lla":     (lambda v: 5 - v / 3,          "+15pp → 0 · 0 → 5 · −15pp → 10 (gap LLA−PJ)"),
    "ratio_dnu":                 (lambda v: v * 5,              "0 → 0 · 1,0 → 5 · 2,0+ → 10 (DNU/leyes)"),
    "movilizacion_cepa":         (lambda v: v / 10,             "0 → 0 · 50 → 5 · 100 → 10 (índice)"),
    "iaf_transferencias":        (lambda v: (0.10 - v / 100) * 25, "+10% → 0 · 0% → 2,5 · −10% → 5 · −30% → 10 (var. real i.a.)"),
    "eficacia_legislativa":      (lambda v: (70 - v) / 7,       "70% → 0 · 35% → 5 · 0% → 10"),
    "cohesion_bloque":           (lambda v: (95 - v) / 7,       "95% → 0 · 60% → 5 · 25% → 10"),
    "gobernadores_alineamiento": (lambda v: (80 - v) / 8,       "80% → 0 · 40% → 5 · 0% → 10"),
    "veto_quorum":               (lambda v: v / 3,              "0% → 0 · 15% → 5 · 30%+ → 10 (sesiones caídas)"),
    "comisiones_caidas":         (lambda v: (v - 20) / 4,       "20% → 0 · 40% → 5 · 60%+ → 10"),
    # ── vida cotidiana ── (sólo ICC entra en el score legacy del cinturón)
    "icc_utdt":                  (lambda v: (60 - v) / 3,       "60 → 0 · 45 → 5 · 30 → 10 (índice de confianza)"),
}

GESTION_MAPA = ("10 × (1 − avance/100): a mayor avance ejecutado, menor tensión. "
                "100% → 0 · 50% → 5 · 0% → 10.")

VIDA_CONTEXTO = ("Indicador de contexto. Hoy el score de Vida cotidiana se calcula sobre un "
                 "subconjunto histórico (IPC, desocupación e ICC); este indicador se muestra "
                 "como contexto y todavía no incide en el número del cinturón.")

SCORE_EXPLICACION = {
    "macro":          "Promedio simple de la tensión (0–10) de sus indicadores. Mayor = más tensión macroeconómica.",
    "politica":       "Promedio simple de la tensión (0–10) de sus indicadores. Mayor = más tensión en el capital político.",
    "gestion":        "Promedio simple de la tensión de sus 12 reformas: a mayor avance ejecutado, menor tensión.",
    "vida_cotidiana": "Se calcula hoy sobre un subconjunto histórico (IPC, desocupación e ICC). Los demás indicadores se muestran como contexto y aún no inciden en el número.",
}


def aplicar_scoring(informe):
    """Anota cada indicador con su aporte de tensión (0–10) y el mapeo que lo
    explica, y cada cinturón con cómo se compone su score."""
    for ckey, c in informe["cinturones"].items():
        c["score_explicacion"] = SCORE_EXPLICACION.get(ckey, "")
        for ikey, ind in c["indicadores"].items():
            aporte = formula = nota = None
            valor = ind.get("valor")
            avance = ind.get("avance_pct")
            if ikey in SCORING and isinstance(valor, (int, float)):
                fn, formula = SCORING[ikey]
                aporte = _clamp10(fn(float(valor)))
            elif isinstance(avance, (int, float)):
                aporte = _clamp10(10.0 * (1.0 - float(avance) / 100.0))
                formula = GESTION_MAPA
            elif ckey == "vida_cotidiana":
                nota = VIDA_CONTEXTO
            ind["aporte_score"] = aporte
            ind["aporte_formula"] = formula
            ind["aporte_nota"] = nota
    return informe


def main():
    informe = json.loads((OUT / "informe.json").read_text(encoding="utf-8"))

    vida_files = sorted(glob.glob(str(ROOT / "scripts" / "vida_cotidiana" / "data" / "vida_cotidiana_*.json")))
    if vida_files:
        raw = json.loads(Path(vida_files[-1]).read_text(encoding="utf-8"))
        enriquecido = build_vida(raw)
        if enriquecido:
            informe["cinturones"]["vida_cotidiana"]["indicadores"] = enriquecido
            informe["cinturones"]["vida_cotidiana"]["fuente_enriquecida"] = os.path.basename(vida_files[-1])

    informe = sanitizar_fuentes(informe)
    informe = aplicar_scoring(informe)

    (DATA / "informe.json").write_text(
        json.dumps(informe, ensure_ascii=False, indent=2), encoding="utf-8")
    (DATA / "series.json").write_text(
        json.dumps(build_series(), ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Snapshot escrito en {DATA}")


if __name__ == "__main__":
    main()
