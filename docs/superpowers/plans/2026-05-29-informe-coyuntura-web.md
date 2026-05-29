# Informe de Coyuntura — Web Pública — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Construir una página pública estática del Informe de Coyuntura de CIGOB, estéticamente idéntica al observatorio de klipea, alimentada por `output/informe.json` + `output/series/*.csv`.

**Architecture:** App Astro en `projects/informe_coyuntura/web/` que compila a HTML estático en `web/informe/` (servido por GitHub Pages). Reutiliza el CSS de klipea tal cual. Un script `publicar.py` arma un snapshot de datos commiteado (`src/data/informe.json` enriquecido + `src/data/series.json`) que Astro importa en build. Sin runtime fetch, sin backend.

**Tech Stack:** Astro 4, TypeScript, SVG inline para charts, Python 3 (publicar.py), pytest.

**Referencia de fidelidad (gitignored, ya capturada):**
- `projects/informe_coyuntura/web/reference/klipea-page.decoded.html` — DOM completo renderizado (markup a portar).
- `projects/informe_coyuntura/web/reference/klipea-dashboard.css` — CSS completo.
- `projects/informe_coyuntura/web/reference/klipea-desktop-full.png` y `klipea-mobile-full.png` — screenshots de referencia.

**Política de display (decisión de diseño):** dentro de cada card de cinturón, los indicadores se ordenan: (1) automáticos frescos arriba, con sparkline; (2) carga manual / desactualizados debajo, con aclaración chica ("dato a {fecha}"); (3) placeholders al final, atenuados, con "— pendiente". Los `score` se muestran tal cual los calcula el pipeline (no se recalculan).

---

## File Structure

```
projects/informe_coyuntura/
  scripts/publicar.py                       # NEW — arma el snapshot commiteado
  tests/test_publicar.py                    # NEW — pytest del snapshot
  web/                                      # NEW — app Astro
    package.json, package-lock.json
    astro.config.mjs
    tsconfig.json
    .gitignore                              # node_modules, dist
    public/
      dashboard.css                         # copiado de reference (CSS de klipea)
      logo-cigob.png                        # copiado de docs/template/cigob_logo.png
    src/
      data/informe.json                     # snapshot commiteado (publicar.py)
      data/series.json                      # snapshot commiteado (publicar.py)
      lib/datos.ts                          # tipos + carga + orden + formato + labels
      lib/sparkline.ts                      # generación de paths SVG
      layouts/Layout.astro
      components/Nav.astro Hero.astro Bluf.astro
                 CinturonCard.astro IndicadorRow.astro Sparkline.astro
                 Evolucion.astro MiniChart.astro
                 TensionPanel.astro Recomendaciones.astro
                 Archivo.astro Metodologia.astro Fuentes.astro
                 Footer.astro IndicadorModal.astro
      pages/index.astro
    reference/                              # gitignored (ya existe)
.github/workflows/pages.yml                 # MODIFY — build Astro antes del upload
web/index.html                              # MODIFY — agregar link a /informe
```

---

## Phase 0 — Scaffold + deploy temprano (verificar base path antes de construir)

### Task 1: Scaffold de la app Astro

**Files:**
- Create: `projects/informe_coyuntura/web/package.json`
- Create: `projects/informe_coyuntura/web/astro.config.mjs`
- Create: `projects/informe_coyuntura/web/tsconfig.json`
- Create: `projects/informe_coyuntura/web/.gitignore`
- Create: `projects/informe_coyuntura/web/src/pages/index.astro` (placeholder mínimo)

- [ ] **Step 1: Crear `package.json`**

```json
{
  "name": "informe-coyuntura-web",
  "type": "module",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "astro dev",
    "build": "astro build",
    "preview": "astro preview"
  },
  "dependencies": {
    "astro": "^4.16.0"
  }
}
```

- [ ] **Step 2: Crear `astro.config.mjs`**

```js
import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://juanpintoselso33.github.io',
  base: '/biblitotecario-ai/informe',
  outDir: '../../../web/informe',
  build: { format: 'directory', assets: '_assets' },
});
```

- [ ] **Step 3: Crear `tsconfig.json`**

```json
{ "extends": "astro/tsconfigs/strict" }
```

- [ ] **Step 4: Crear `.gitignore`**

```
node_modules/
dist/
.astro/
```

- [ ] **Step 5: Crear `src/pages/index.astro` (placeholder)**

```astro
---
---
<!DOCTYPE html>
<html lang="es">
  <head><meta charset="utf-8" /><title>Informe de Coyuntura</title></head>
  <body><h1>OK build</h1></body>
</html>
```

- [ ] **Step 6: Instalar y buildear**

Run (desde `projects/informe_coyuntura/web/`): `npm install && npm run build`
Expected: build OK, genera `web/informe/index.html` en la raíz del repo (tres niveles arriba). Verificar: `test -f ../../../web/informe/index.html && echo OK`

- [ ] **Step 7: Commit**

```bash
git add projects/informe_coyuntura/web/package.json projects/informe_coyuntura/web/package-lock.json projects/informe_coyuntura/web/astro.config.mjs projects/informe_coyuntura/web/tsconfig.json projects/informe_coyuntura/web/.gitignore projects/informe_coyuntura/web/src/pages/index.astro
git commit -m "feat(informe-web): scaffold Astro app con base path de Pages"
```

### Task 2: Wiring de deploy en CI (verificar base path con deploy real)

**Files:**
- Modify: `.github/workflows/pages.yml`
- Modify: `web/index.html` (agregar link a la nueva página)

- [ ] **Step 1: Reemplazar el job `deploy` en `pages.yml`**

```yaml
jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm
          cache-dependency-path: projects/informe_coyuntura/web/package-lock.json
      - name: Build informe (Astro)
        working-directory: projects/informe_coyuntura/web
        run: |
          npm ci
          npm run build
      - uses: actions/configure-pages@v5
      - uses: actions/upload-pages-artifact@v3
        with:
          path: web
      - id: deployment
        uses: actions/deploy-pages@v4
```

- [ ] **Step 2: Agregar link a `/informe` en `web/index.html`**

En la `.tools-grid` de `web/index.html`, agregar una card que apunte a `./informe/` (replicar el markup de las cards existentes; href `./informe/index.html`, título "Informe de Coyuntura", descripción "Observatorio mensual de los cinturones matusianos").

- [ ] **Step 3: Commit y push (dispara deploy)**

```bash
git add .github/workflows/pages.yml web/index.html
git commit -m "ci(informe-web): build Astro en Pages + link desde landing"
git push
```

- [ ] **Step 4: Verificar el deploy real**

Esperar a que termine la GitHub Action. Abrir `https://juanpintoselso33.github.io/biblitotecario-ai/informe/`.
Expected: muestra "OK build". Si 404 o assets rotos → el `base` está mal; ajustar `astro.config.mjs` y re-deploy. **No avanzar hasta que el base path funcione en producción.**

---

## Phase 1 — Capa de datos (publicar.py + snapshot + helpers TS)

### Task 3: `publicar.py` — snapshot enriquecido + series

**Files:**
- Create: `projects/informe_coyuntura/scripts/publicar.py`
- Create: `projects/informe_coyuntura/tests/test_publicar.py`
- Genera: `projects/informe_coyuntura/web/src/data/informe.json`, `series.json`

- [ ] **Step 1: Escribir el test (pytest)**

`tests/test_publicar.py`:

```python
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
```

- [ ] **Step 2: Correr el test y verificar que falla**

Run (desde `projects/informe_coyuntura/`): `python -m pytest tests/test_publicar.py -v`
Expected: FAIL (no existe `scripts/publicar.py`).

- [ ] **Step 3: Escribir `scripts/publicar.py`**

```python
"""Arma el snapshot de datos que consume la web del informe de coyuntura.

Lee output/informe.json + el ultimo vida_cotidiana_*.json + output/series/*.csv
y escribe web/src/data/informe.json (con vida cotidiana enriquecido a ~13
indicadores automaticos) y web/src/data/series.json.
"""
import csv, glob, json, os, sys
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
    _add(out, "endeudamiento_familiar", cc.get("valor"),
         "millones $ (consumo)", "BCRA API v4.0", cc.get("fecha"))
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
    return series


def main():
    informe = json.loads((OUT / "informe.json").read_text(encoding="utf-8"))

    vida_files = sorted(glob.glob(str(ROOT / "scripts" / "vida_cotidiana" / "data" / "vida_cotidiana_*.json")))
    if vida_files:
        raw = json.loads(Path(vida_files[-1]).read_text(encoding="utf-8"))
        enriquecido = build_vida(raw)
        if enriquecido:
            informe["cinturones"]["vida_cotidiana"]["indicadores"] = enriquecido
            informe["cinturones"]["vida_cotidiana"]["fuente_enriquecida"] = os.path.basename(vida_files[-1])

    (DATA / "informe.json").write_text(
        json.dumps(informe, ensure_ascii=False, indent=2), encoding="utf-8")
    (DATA / "series.json").write_text(
        json.dumps(build_series(), ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Snapshot escrito en {DATA}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Correr el test y verificar que pasa**

Run (desde `projects/informe_coyuntura/`): `python -m pytest tests/test_publicar.py -v`
Expected: PASS.

- [ ] **Step 5: Commit (incluye el snapshot generado)**

```bash
git add projects/informe_coyuntura/scripts/publicar.py projects/informe_coyuntura/tests/test_publicar.py projects/informe_coyuntura/web/src/data/informe.json projects/informe_coyuntura/web/src/data/series.json
git commit -m "feat(informe-web): publicar.py arma snapshot enriquecido + series"
```

### Task 4: `lib/datos.ts` — tipos, carga, orden, formato, labels

**Files:**
- Create: `projects/informe_coyuntura/web/src/lib/datos.ts`

- [ ] **Step 1: Escribir `src/lib/datos.ts`**

```ts
import informeRaw from "../data/informe.json";
import seriesRaw from "../data/series.json";

export interface Indicador {
  valor: number | string | null;
  unidad: string;
  fuente: string;
  fecha_dato: string;
  desactualizado: boolean;
  estado?: string;        // "placeholder" cuando aplica
  avance_pct?: number;
  notas?: string;
  [k: string]: unknown;
}
export interface Cinturon {
  score: number;
  estado: string;         // estable | en_tension | critico
  barbarismo_riesgo: string;
  indicadores: Record<string, Indicador>;
  alerta: string | null;
}
export interface Informe {
  schema_version: string;
  generated_at: string;
  period: string;
  score_global: number;
  cinturones: Record<"macro" | "politica" | "vida_cotidiana" | "gestion", Cinturon>;
  barbarismo_activo: string;
  alerta_multicinturon: boolean;
  flags: string[];
}

export const informe = informeRaw as unknown as Informe;
export const series = seriesRaw as Record<string, { fecha: string; valor: number }[]>;

// Orden y metadatos de presentación de los cinturones (mapeo a clases .cg-cint--*)
export const CINTURONES = [
  { key: "macro",          slug: "macro",    nombre: "Macroeconomía",   sub: "El motor económico" },
  { key: "politica",       slug: "politica", nombre: "Política",        sub: "El tablero de poder" },
  { key: "vida_cotidiana", slug: "vida",     nombre: "Vida cotidiana",  sub: "El bolsillo y la calle" },
  { key: "gestion",        slug: "gestion",  nombre: "Gestión",         sub: "La capacidad de ejecutar" },
] as const;

// Semáforo del cinturón a partir de su estado
export function verdictDeCinturon(estado: string): "verde" | "amarillo" | "rojo" {
  if (estado === "estable") return "verde";
  if (estado === "critico" || estado === "alerta") return "rojo";
  return "amarillo"; // en_tension
}

// Clasificación de un indicador para el orden de display
export type Bucket = "fresco" | "manual" | "placeholder";
export function bucketDeIndicador(ind: Indicador): Bucket {
  if (ind.estado === "placeholder" || ind.valor === null) return "placeholder";
  if (ind.desactualizado) return "manual";
  return "fresco";
}

// Devuelve los indicadores de un cinturón ordenados: fresco → manual → placeholder
export function indicadoresOrdenados(c: Cinturon): { key: string; ind: Indicador; bucket: Bucket }[] {
  const orden: Record<Bucket, number> = { fresco: 0, manual: 1, placeholder: 2 };
  return Object.entries(c.indicadores)
    .map(([key, ind]) => ({ key, ind, bucket: bucketDeIndicador(ind) }))
    .sort((a, b) => orden[a.bucket] - orden[b.bucket]);
}

// Etiquetas legibles por clave de indicador
export const LABELS: Record<string, string> = {
  // macro
  ipc_total: "Inflación mensual (IPC)", reservas_bcra: "Reservas BCRA",
  badlar: "Tasa BADLAR", emae_ia: "Actividad económica (EMAE i.a.)",
  saldo_comercial_12m: "Saldo comercial 12m", recaudacion: "Recaudación tributaria",
  tcrm: "Tipo de cambio real (TCRM)", rem_ipc_12m: "Expectativas inflación (REM 12m)",
  prestamos_privados: "Préstamos al sector privado", base_monetaria: "Base monetaria",
  tc_mayorista: "Tipo de cambio mayorista",
  // politica
  votometro_ventaja_lla: "Ventaja LLA−PJ (Votómetro)", ratio_dnu: "Ratio DNU / leyes",
  movilizacion_cepa: "Tensión social (CEPA)", iaf_transferencias: "Armonía federal (transferencias)",
  eficacia_legislativa: "Eficacia parlamentaria", cohesion_bloque: "Cohesión del bloque LLA",
  gobernadores_alineamiento: "Alineamiento de gobernadores", veto_quorum: "Sesiones caídas por quórum",
  comisiones_caidas: "Comisiones sin sanción",
  // vida cotidiana (claves de publicar.py)
  brecha_salario_cbt: "Salario real vs. canasta", ipc_alimentos: "Inflación de alimentos",
  endeudamiento_familiar: "Endeudamiento de consumo", peso_tarifas: "Peso de tarifas (regulados)",
  consumo_carne: "Consumo de carne per cápita", informalidad: "Informalidad laboral",
  mortalidad_pymes: "Actividad industrial (IPI)", despacho_cemento: "Despacho de cemento (ISAC)",
  pluriempleo: "Subocupación demandante", inseguridad: "Hechos delictivos (SNIC)",
  icc_utdt: "Confianza del consumidor (ICC)", sentimiento_digital: "Sentimiento digital (Trends)",
  patentamiento_motos: "Patentamiento de motos", desocupacion: "Desocupación",
  // gestion
  cepo_mulc: "Brecha cambiaria (cepo)", privatizaciones: "Privatizaciones",
  concesiones_infraestructura: "Concesiones viales", reduccion_estado: "Reducción del Estado",
  reestructuracion_organismos: "Reestructuración de organismos", rigi_inversiones: "Inversiones RIGI",
  desregulacion_normativa: "Desregulación normativa", apertura_comercial: "Apertura comercial",
  asistencia_directa: "Asistencia directa", fal_modernizacion_laboral: "Modernización laboral (FAL)",
  libertad_opcion_salud: "Libertad de opción en salud", protocolo_antipiquetes: "Protocolo antipiquetes",
};
export function label(key: string): string {
  return LABELS[key] ?? key.replace(/_/g, " ");
}

// Formato de valor: números con separador es-AR; strings tal cual; null → "—"
const NF = new Intl.NumberFormat("es-AR", { maximumFractionDigits: 2 });
export function formatValor(valor: unknown): string {
  if (valor === null || valor === undefined) return "—";
  if (typeof valor === "number") return NF.format(valor);
  return String(valor);
}

// Aclaración chica para buckets no-frescos
export function aclaracion(b: Bucket, ind: Indicador): string | null {
  if (b === "placeholder") return "— pendiente";
  if (b === "manual") return `dato a ${ind.fecha_dato}`;
  return null;
}

// Conteo de cinturones "rojos" (para hero + tensión)
export function cinturonesRojos(inf: Informe): number {
  return Object.values(inf.cinturones).filter(c => verdictDeCinturon(c.estado) === "rojo").length;
}
```

- [ ] **Step 2: Verificar que typecheckea en build**

Run (desde `web/`): `npm run build`
Expected: build OK (el placeholder de index.astro aún no usa datos.ts; este step solo valida que el módulo compila — si querés forzar, importalo temporalmente en index.astro).

- [ ] **Step 3: Commit**

```bash
git add projects/informe_coyuntura/web/src/lib/datos.ts
git commit -m "feat(informe-web): capa de datos TS (tipos, orden, labels, formato)"
```

### Task 5: `lib/sparkline.ts` — paths SVG

**Files:**
- Create: `projects/informe_coyuntura/web/src/lib/sparkline.ts`

- [ ] **Step 1: Escribir `src/lib/sparkline.ts`**

```ts
// Genera coordenadas para sparklines y charts SVG a partir de una serie de valores.
export interface PuntoSerie { fecha: string; valor: number; }

export interface SparkPaths {
  linea: string;   // "M x,y L x,y ..."
  area: string;    // path cerrado para el relleno
  ultimo: { x: number; y: number } | null;
  vacio: boolean;
}

// w/h en unidades de viewBox; pad vertical para que la línea no toque los bordes.
export function sparkline(serie: PuntoSerie[], w = 60, h = 22, pad = 3): SparkPaths {
  const vals = serie.map(p => p.valor);
  if (vals.length < 2) return { linea: "", area: "", ultimo: null, vacio: true };
  const min = Math.min(...vals), max = Math.max(...vals);
  const span = max - min || 1;
  const stepX = w / (vals.length - 1);
  const pts = vals.map((v, i) => ({
    x: +(i * stepX).toFixed(2),
    y: +(h - pad - ((v - min) / span) * (h - 2 * pad)).toFixed(2),
  }));
  const linea = pts.map((p, i) => `${i === 0 ? "M" : "L"}${p.x},${p.y}`).join(" ");
  const area = `${linea} L${pts[pts.length - 1].x},${h} L${pts[0].x},${h} Z`;
  return { linea, area, ultimo: pts[pts.length - 1], vacio: false };
}

// Variante para el gráfico grande / minis (mismo cálculo, distinto tamaño).
export function chartPath(serie: PuntoSerie[], w: number, h: number, pad = 6): SparkPaths {
  return sparkline(serie, w, h, pad);
}
```

- [ ] **Step 2: Commit**

```bash
git add projects/informe_coyuntura/web/src/lib/sparkline.ts
git commit -m "feat(informe-web): generación de paths SVG para sparklines y charts"
```

---

## Phase 2 — Layout + chrome estático

> **Cómo portar markup:** abrir `reference/klipea-page.decoded.html`. Para cada componente, copiar el bloque de markup indicado (clases `.cg-*`), pegarlo en el `.astro`, y reemplazar el texto/valores hardcodeados por las expresiones `{...}` indicadas. El CSS ya está en `public/dashboard.css` — no tocar clases.

### Task 6: Assets + `Layout.astro`

**Files:**
- Create: `projects/informe_coyuntura/web/public/dashboard.css` (copia)
- Create: `projects/informe_coyuntura/web/public/logo-cigob.png` (copia)
- Create: `projects/informe_coyuntura/web/src/layouts/Layout.astro`

- [ ] **Step 1: Copiar assets**

```bash
cp projects/informe_coyuntura/web/reference/klipea-dashboard.css projects/informe_coyuntura/web/public/dashboard.css
cp projects/informe_coyuntura/docs/template/cigob_logo.png projects/informe_coyuntura/web/public/logo-cigob.png
```

Nota: `klipea-dashboard.css` en `reference/` quedó guardado como string JSON. Si abre con comillas/`\n` literales, regenerarlo limpio: `python -c "import json; open('projects/informe_coyuntura/web/public/dashboard.css','w',encoding='utf-8').write(json.loads(open('projects/informe_coyuntura/web/reference/klipea-dashboard.css',encoding='utf-8').read()))"`. Verificar que el archivo arranca con `/*` y `:root {`.

- [ ] **Step 2: Crear `src/layouts/Layout.astro`**

```astro
---
const { title = "Realidad Política Argentina · Observatorio CIGOB" } = Astro.props;
const base = import.meta.env.BASE_URL; // "/biblitotecario-ai/informe"
---
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <link rel="icon" type="image/png" href={`${base}/logo-cigob.png`} />
    <title>{title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link rel="stylesheet"
      href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700;800&family=DM+Serif+Display:wght@400&family=JetBrains+Mono:wght@400;500;700&display=swap" />
    <link rel="stylesheet" href={`${base}/dashboard.css`} />
  </head>
  <body>
    <slot />
  </body>
</html>
```

- [ ] **Step 3: Build de verificación**

Run (desde `web/`): `npm run build` → Expected: OK. Abrir `web/informe/index.html` local y confirmar que el CSS y las fuentes cargan (todavía con el placeholder).

- [ ] **Step 4: Commit**

```bash
git add projects/informe_coyuntura/web/public/dashboard.css projects/informe_coyuntura/web/public/logo-cigob.png projects/informe_coyuntura/web/src/layouts/Layout.astro
git commit -m "feat(informe-web): assets (CSS klipea + logo) y Layout base"
```

### Task 7: `Nav.astro` y `Footer.astro`

**Files:**
- Create: `projects/informe_coyuntura/web/src/components/Nav.astro`
- Create: `projects/informe_coyuntura/web/src/components/Footer.astro`

- [ ] **Step 1: `Nav.astro`** — portar el bloque `nav.cg-nav` del reference.

```astro
---
const base = import.meta.env.BASE_URL;
---
<nav class="cg-nav">
  <div class="cg-nav-inner">
    <a class="cg-nav-brand" href="#top">
      <span class="cg-nav-logo"><img src={`${base}/logo-cigob.png`} alt="CiGob" /></span>
      <span class="cg-nav-titles">
        <span class="cg-nav-title">Realidad Política Argentina</span>
        <span class="cg-nav-sub">Observatorio mensual · Fundación CiGob</span>
      </span>
    </a>
    <div class="cg-nav-links">
      <a href="#snapshot">Mes actual</a>
      <a href="#evolucion">Evolución</a>
      <a href="#archivo">Archivo</a>
      <a href="#metodologia">Metodología</a>
    </div>
  </div>
</nav>
```

- [ ] **Step 2: `Footer.astro`** — portar `footer.cg-foot` del reference. Reemplazar los links de "API/series/PDF" por: link al repo, link a `series.json` (`{base}/_assets/...` no aplica — apuntar a la fuente), y texto legal. Dejar el resto del markup igual. El timestamp: `{informe.generated_at}`.

```astro
---
import { informe } from "../lib/datos.ts";
const base = import.meta.env.BASE_URL;
---
<!-- Portar el markup de footer.cg-foot del reference. Bindings:
     - .cg-foot-legal span#cg-foot-time → {informe.generated_at}
     - links de la 3ª columna → repo GitHub + metodología (#metodologia)
     - mantener .cg-foot-brand, .cg-foot-cols, paleta dark -->
```

> Implementación: copiar el `<footer class="cg-foot">…</footer>` del reference y sustituir esos tres bindings. No inventar links nuevos: usar `https://github.com/Juanpintoselso33/biblitotecario-ai` y anclas internas.

- [ ] **Step 3: Build de verificación**

Run (desde `web/`): `npm run build` → Expected: OK.

- [ ] **Step 4: Commit**

```bash
git add projects/informe_coyuntura/web/src/components/Nav.astro projects/informe_coyuntura/web/src/components/Footer.astro
git commit -m "feat(informe-web): Nav y Footer"
```

---

## Phase 3 — Cinturones (núcleo) + Hero

### Task 8: `Sparkline.astro`

**Files:**
- Create: `projects/informe_coyuntura/web/src/components/Sparkline.astro`

- [ ] **Step 1: Escribir `Sparkline.astro`**

```astro
---
import { sparkline } from "../lib/sparkline.ts";
import { series } from "../lib/datos.ts";
const { indicador, estado = "verde", w = 60, h = 22 } = Astro.props;
const serie = series[indicador] ?? [];
const sp = sparkline(serie, w, h);
---
{!sp.vacio && (
  <svg viewBox={`0 0 ${w} ${h}`} width={w} height={h} preserveAspectRatio="none" aria-hidden="true">
    <path class="cg-spark-area" d={sp.area} />
    <path class="cg-spark-line" d={sp.linea} />
    {sp.ultimo && <circle class={`cg-spark-dot ${estado}`} cx={sp.ultimo.x} cy={sp.ultimo.y} r="2" />}
  </svg>
)}
```

- [ ] **Step 2: Commit**

```bash
git add projects/informe_coyuntura/web/src/components/Sparkline.astro
git commit -m "feat(informe-web): componente Sparkline (SVG)"
```

### Task 9: `IndicadorRow.astro` (con política de display)

**Files:**
- Create: `projects/informe_coyuntura/web/src/components/IndicadorRow.astro`

- [ ] **Step 1: Escribir `IndicadorRow.astro`** — portar el `<li class="cg-ind">` del reference (un indicador). Estructura: `span.cg-ind-name` + `span.cg-ind-sparkline` + `span.cg-ind-value`.

```astro
---
import { label, formatValor, aclaracion } from "../lib/datos.ts";
import Sparkline from "./Sparkline.astro";
const { ikey, ind, bucket } = Astro.props;
const estDot = bucket === "fresco" ? "verde" : bucket === "manual" ? "amarillo" : "rojo";
const nota = aclaracion(bucket, ind);
const clickable = bucket !== "placeholder";
---
<li class:list={["cg-ind", { "cg-ind--clickable": clickable }]} data-indicador={ikey}>
  <span class="cg-ind-name">
    {label(ikey)}
    {nota && <em style="font-style:normal;color:var(--muted-soft);font-size:11px;margin-left:6px;">({nota})</em>}
  </span>
  {bucket === "fresco" && (
    <span class="cg-ind-sparkline"><Sparkline indicador={ikey} estado={estDot} /></span>
  )}
  <span class="cg-ind-value">
    {formatValor(ind.valor)}
    <span class="cg-ind-unit">{ind.unidad}</span>
    <span class:list={["cg-ind-est", estDot]}></span>
  </span>
</li>
```

> El semáforo del dot en v1 refleja **frescura** (fresco=verde, manual=amarillo, placeholder=rojo), no un umbral por indicador (no tenemos umbrales). Documentar como simplificación v1.

- [ ] **Step 2: Commit**

```bash
git add projects/informe_coyuntura/web/src/components/IndicadorRow.astro
git commit -m "feat(informe-web): IndicadorRow con orden fresco/manual/placeholder"
```

### Task 10: `CinturonCard.astro`

**Files:**
- Create: `projects/informe_coyuntura/web/src/components/CinturonCard.astro`

- [ ] **Step 1: Escribir `CinturonCard.astro`** — portar `<article class="cg-cint cg-cint--macro">` del reference.

```astro
---
import { verdictDeCinturon, indicadoresOrdenados } from "../lib/datos.ts";
import IndicadorRow from "./IndicadorRow.astro";
const { slug, nombre, sub, cinturon } = Astro.props;
const verdict = verdictDeCinturon(cinturon.estado);
const verdictLabel = { verde: "Estable", amarillo: "En tensión", rojo: "Crítico" }[verdict];
const filas = indicadoresOrdenados(cinturon);
---
<article class:list={["cg-cint", `cg-cint--${slug}`]}>
  <div class="cg-cint-head">
    <div class="cg-cint-titles">
      <div class="cg-cint-sub">{sub}</div>
      <div class="cg-cint-name">{nombre}</div>
    </div>
    <span class:list={["cg-verdict", verdict]}>
      <span class="cg-verdict-dot"></span>{verdictLabel}
    </span>
  </div>
  <ul class="cg-ind-list">
    {filas.map(({ key, ind, bucket }) => <IndicadorRow ikey={key} ind={ind} bucket={bucket} />)}
  </ul>
  <div class="cg-cint-foot">
    Score <strong>{cinturon.score}/10</strong> · riesgo {cinturon.barbarismo_riesgo}
  </div>
</article>
```

- [ ] **Step 2: Render temporal en index para verificar**

En `src/pages/index.astro`, reemplazar el placeholder por un render mínimo con `Layout`, mapeando `CINTURONES` a `CinturonCard` dentro de `.cg-grid`. Build + abrir local.

```astro
---
import Layout from "../layouts/Layout.astro";
import CinturonCard from "../components/CinturonCard.astro";
import { informe, CINTURONES } from "../lib/datos.ts";
---
<Layout>
  <main class="cg-main">
    <section class="cg-section">
      <div class="cg-grid">
        {CINTURONES.map(c => (
          <CinturonCard slug={c.slug} nombre={c.nombre} sub={c.sub}
            cinturon={informe.cinturones[c.key]} />
        ))}
      </div>
    </section>
  </main>
</Layout>
```

- [ ] **Step 3: Build + verificación visual**

Run (desde `web/`): `npm run build`. Abrir `web/informe/index.html`.
Expected: 4 cards con colores de borde correctos, indicadores automáticos arriba con sparkline, manuales/placeholders abajo con aclaración. Comparar contra `reference/klipea-desktop-full.png` (sección "Diagnóstico por capa").

- [ ] **Step 4: Commit**

```bash
git add projects/informe_coyuntura/web/src/components/CinturonCard.astro projects/informe_coyuntura/web/src/pages/index.astro
git commit -m "feat(informe-web): CinturonCard + grid de los 4 cinturones"
```

### Task 11: `Hero.astro`

**Files:**
- Create: `projects/informe_coyuntura/web/src/components/Hero.astro`

- [ ] **Step 1: Escribir `Hero.astro`** — portar `header.cg-hero` del reference. 4 stats: período, cinturones rojos, score global, "barbarismo activo".

```astro
---
import { informe, cinturonesRojos } from "../lib/datos.ts";
const rojos = cinturonesRojos(informe);
---
<header class="cg-hero" id="top">
  <div class="cg-hero-inner">
    <p class="cg-hero-eyebrow">Observatorio · Fundación CiGob</p>
    <h1 class="cg-hero-title">El clima del país en <em>una sola lectura.</em></h1>
    <p class="cg-hero-lead">
      Cuatro <strong>cinturones</strong> —macro, política, vida cotidiana y gestión— leídos
      como un <strong>sistema interconectado</strong>, no como problemas aislados.
    </p>
    <div class="cg-hero-stats">
      <div class="cg-hero-stat"><div class="cg-hero-stat-num">{informe.period}</div><div class="cg-hero-stat-lbl">Período</div></div>
      <div class="cg-hero-stat"><div class="cg-hero-stat-num">{rojos}</div><div class="cg-hero-stat-lbl">Cinturones en rojo</div></div>
      <div class="cg-hero-stat"><div class="cg-hero-stat-num">{informe.score_global}</div><div class="cg-hero-stat-lbl">Score global /10</div></div>
      <div class="cg-hero-stat"><div class="cg-hero-stat-num" style="font-size:20px;">{informe.barbarismo_activo}</div><div class="cg-hero-stat-lbl">Riesgo dominante</div></div>
    </div>
    <p class="cg-hero-meta">
      <span class:list={["cg-status-pill", informe.alerta_multicinturon ? "is-err" : "is-signed"]}>
        <span class="cg-status-dot"></span>
        <span class="cg-status-text">{informe.alerta_multicinturon ? "Alerta sistémica" : "Estable"}</span>
      </span>
      <span class="cg-hero-since">Datos al {informe.generated_at.slice(0,10)}</span>
    </p>
  </div>
</header>
```

- [ ] **Step 2: Build de verificación**

Run (desde `web/`): `npm run build` → Expected: OK.

- [ ] **Step 3: Commit**

```bash
git add projects/informe_coyuntura/web/src/components/Hero.astro
git commit -m "feat(informe-web): Hero con stats reales"
```

---

## Phase 4 — Secciones restantes

### Task 12: `Bluf.astro` (placeholder editorial)

**Files:**
- Create: `projects/informe_coyuntura/web/src/components/Bluf.astro`

- [ ] **Step 1: Escribir `Bluf.astro`** — portar `section.cg-bluf` del reference. Texto = placeholder explícito.

```astro
---
import { informe } from "../lib/datos.ts";
---
<section class="cg-section cg-bluf" id="snapshot">
  <p class="cg-eyebrow">La lectura del mes</p>
  <h2 class="cg-h2">Argentina · {informe.period}</h2>
  <p class="cg-bluf-meta">
    <strong>Score global {informe.score_global}/10</strong> ·
    <strong>Riesgo dominante: {informe.barbarismo_activo}</strong>
  </p>
  <p class="cg-bluf-text">
    <em style="font-style:normal;color:var(--muted);">[Resumen editorial del mes — pendiente de redacción.]</em>
  </p>
</section>
```

- [ ] **Step 2: Commit**

```bash
git add projects/informe_coyuntura/web/src/components/Bluf.astro
git commit -m "feat(informe-web): Bluf (resumen del mes, placeholder)"
```

### Task 13: `TensionPanel.astro` + `Recomendaciones.astro`

**Files:**
- Create: `projects/informe_coyuntura/web/src/components/TensionPanel.astro`
- Create: `projects/informe_coyuntura/web/src/components/Recomendaciones.astro`

- [ ] **Step 1: `TensionPanel.astro`** — portar `.cg-panel#cg-tension`. Matriz = un chip por cinturón con su color de barbarismo; texto = resumen de barbarismos; regla = la regla "2+ rojos = inestabilidad".

```astro
---
import { informe, CINTURONES, verdictDeCinturon, cinturonesRojos } from "../lib/datos.ts";
const rojos = cinturonesRojos(informe);
---
<div class="cg-panel" id="cg-tension">
  <p class="cg-eyebrow">Tensión sistémica</p>
  <h3>Riesgo dominante: {informe.barbarismo_activo}</h3>
  <div class="cg-matriz">
    {CINTURONES.map(c => {
      const v = verdictDeCinturon(informe.cinturones[c.key].estado);
      const color = v === "rojo" ? "var(--rojo)" : v === "amarillo" ? "var(--amarillo)" : "var(--verde)";
      return (
        <span class="cg-matriz-item">
          <span class="cg-dot" style={`background:${color}`}></span>
          {c.nombre} · {informe.cinturones[c.key].barbarismo_riesgo}
        </span>
      );
    })}
  </div>
  <div class="cg-tension-rule">
    Regla de lectura: <strong>1 cinturón en rojo</strong> es manejable;
    <strong>2 o más</strong> indican inestabilidad sistémica con crisis que se retroalimentan.
    Actualmente: <strong>{rojos} en rojo</strong>.
  </div>
</div>
```

- [ ] **Step 2: `Recomendaciones.astro`** (placeholder) — portar `.cg-rec-list`, una sola entrada placeholder.

```astro
<div class="cg-panel">
  <h3>Recomendaciones</h3>
  <ol class="cg-rec-list">
    <li class="cg-rec">
      <p class="cg-rec-title">[Recomendaciones del mes — pendientes de redacción.]</p>
      <div class="cg-rec-meta"><span class="cg-rec-pill cg-rec-pill--media">placeholder</span></div>
    </li>
  </ol>
</div>
```

- [ ] **Step 3: Commit**

```bash
git add projects/informe_coyuntura/web/src/components/TensionPanel.astro projects/informe_coyuntura/web/src/components/Recomendaciones.astro
git commit -m "feat(informe-web): panel de tensión sistémica + recomendaciones (placeholder)"
```

### Task 14: `MiniChart.astro` + `Evolucion.astro`

**Files:**
- Create: `projects/informe_coyuntura/web/src/components/MiniChart.astro`
- Create: `projects/informe_coyuntura/web/src/components/Evolucion.astro`

- [ ] **Step 1: `MiniChart.astro`** — una mini card de evolución (`.cg-chart-mini-card`).

```astro
---
import { chartPath } from "../lib/sparkline.ts";
import { series, label, formatValor } from "../lib/datos.ts";
const { indicador, slug } = Astro.props;
const serie = series[indicador] ?? [];
const sp = chartPath(serie, 300, 80);
const ahora = serie.at(-1)?.valor ?? null;
const previo = serie.at(-2)?.valor ?? null;
const delta = ahora !== null && previo !== null ? ahora - previo : null;
const dir = delta === null ? "flat" : delta > 0 ? "up" : delta < 0 ? "down" : "flat";
---
<div class:list={["cg-chart-mini-card", slug]}>
  <h3>{label(indicador)}</h3>
  <div class="cg-sub">Últimos {serie.length} datos</div>
  <div class="cg-chart-mini">
    {!sp.vacio && (
      <svg viewBox="0 0 300 80" width="100%" height="80" preserveAspectRatio="none">
        <path class="cg-spark-area" d={sp.area} />
        <path class="cg-spark-line" d={sp.linea} />
      </svg>
    )}
  </div>
  <div class="cg-chart-mini-foot">
    <div class="cg-chart-mini-now">{formatValor(ahora)}</div>
    <span class:list={["cg-chart-mini-delta", dir]}>
      {delta === null ? "—" : `${delta > 0 ? "+" : ""}${formatValor(delta)}`}
    </span>
  </div>
</div>
```

- [ ] **Step 2: `Evolucion.astro`** — portar `section#evolucion`. Gráfico grande = serie del score por cinturón si existe; si no hay multi-mes, mostrar aviso de "histórico en construcción". Grid de minis con indicadores destacados que tengan serie.

```astro
---
import MiniChart from "./MiniChart.astro";
import { series } from "../lib/datos.ts";
// Indicadores destacados por cinturón con su slug de color, solo si tienen serie con >=2 puntos
const DESTACADOS = [
  { indicador: "ipc_total", slug: "macro" },
  { indicador: "tcrm", slug: "macro" },
  { indicador: "ratio_dnu", slug: "politica" },
  { indicador: "icc_utdt", slug: "vida" },
  { indicador: "cepo_mulc", slug: "gestion" },
].filter(d => (series[d.indicador] ?? []).length >= 2);
---
<section class="cg-section" id="evolucion">
  <div class="cg-section-head">
    <p class="cg-eyebrow">Cómo va la película</p>
    <h2 class="cg-h2">Evolución</h2>
    <p class="cg-h2-sub">Series históricas de los indicadores automatizados.</p>
  </div>
  {DESTACADOS.length === 0 ? (
    <div class="cg-chart-card"><p class="cg-chart-sub">Histórico en construcción: se necesita más de un período para graficar tendencias.</p></div>
  ) : (
    <div class="cg-chart-grid" id="cg-chart-grid">
      {DESTACADOS.map(d => <MiniChart indicador={d.indicador} slug={d.slug} />)}
    </div>
  )}
</section>
```

- [ ] **Step 3: Build + verificación visual**

Run (desde `web/`): `npm run build`. Confirmar que las minis muestran líneas (las series macro/vida tienen historia) y los deltas.

- [ ] **Step 4: Commit**

```bash
git add projects/informe_coyuntura/web/src/components/MiniChart.astro projects/informe_coyuntura/web/src/components/Evolucion.astro
git commit -m "feat(informe-web): sección Evolución con mini-charts desde series.json"
```

### Task 15: `Archivo.astro`

**Files:**
- Create: `projects/informe_coyuntura/web/src/components/Archivo.astro`

- [ ] **Step 1: Escribir `Archivo.astro`** — portar `section#archivo`. Una sola card (período actual), marcada `current`.

```astro
---
import { informe, cinturonesRojos } from "../lib/datos.ts";
const rojos = cinturonesRojos(informe);
---
<section class="cg-section" id="archivo">
  <div class="cg-section-head">
    <p class="cg-eyebrow">Informes anteriores</p>
    <h2 class="cg-h2">Archivo</h2>
    <p class="cg-h2-sub">El observatorio arranca en {informe.period}. La hemeroteca crece mes a mes.</p>
  </div>
  <div class="cg-archive">
    <article class="cg-archive-card current">
      <div class="cg-archive-period">{informe.period}</div>
      <div class="cg-archive-bluf">Resumen editorial pendiente. Score global {informe.score_global}/10, riesgo dominante {informe.barbarismo_activo}.</div>
      <div class="cg-archive-foot">
        <span class:list={["cg-archive-score", `rojos-${rojos}`]}>{rojos} en rojo</span>
      </div>
    </article>
  </div>
</section>
```

- [ ] **Step 2: Commit**

```bash
git add projects/informe_coyuntura/web/src/components/Archivo.astro
git commit -m "feat(informe-web): Archivo (período actual)"
```

### Task 16: `Metodologia.astro` + `Fuentes.astro`

**Files:**
- Create: `projects/informe_coyuntura/web/src/components/Metodologia.astro`
- Create: `projects/informe_coyuntura/web/src/components/Fuentes.astro`

- [ ] **Step 1: `Metodologia.astro`** — portar `section.cg-method#metodologia`. 4 artículos con texto fijo del marco Matus (triángulo de gobierno, cinturones, barbarismos, regla de lectura). Mencionar que el 5º cinturón ("Espíritu de la época") está en desarrollo.

```astro
<section class="cg-section cg-method" id="metodologia">
  <div class="cg-section-head">
    <p class="cg-eyebrow">Cómo se construye</p>
    <h2 class="cg-h2">El método de los cinturones</h2>
    <p class="cg-h2-sub">Lectura situacional de la realidad como sistema, según la Planificación Estratégica Situacional (PES) de Carlos Matus.</p>
  </div>
  <div class="cg-method-grid">
    <article><h3>Cuatro cinturones</h3><p>Macro, política, vida cotidiana y gestión. Cada uno agrupa indicadores que, leídos juntos, describen el clima del país. Un quinto cinturón —<strong>Espíritu de la época</strong>— está en desarrollo.</p></article>
    <article><h3>Indicadores automatizados</h3><p>La mayoría de los indicadores se extraen automáticamente de fuentes públicas (<strong>INDEC</strong>, <strong>BCRA</strong>, <strong>InfoLeg</strong>, HCDN). Los de carga manual o pendientes se marcan como tales.</p></article>
    <article><h3>Score y barbarismos</h3><p>Cada cinturón tiene un score 0–10 y un <strong>riesgo de barbarismo</strong> (tecnocrático, político, gerencial). El score global integra los cuatro.</p></article>
    <article><h3>Regla de lectura</h3><p>Un cinturón en rojo es manejable; <strong>dos o más</strong> simultáneos señalan inestabilidad sistémica.</p></article>
  </div>
</section>
```

- [ ] **Step 2: `Fuentes.astro`** — portar `section.cg-sources`. Lista deduplicada de `fuente` de todos los indicadores.

```astro
---
import { informe } from "../lib/datos.ts";
const fuentes = [...new Set(
  Object.values(informe.cinturones).flatMap(c =>
    Object.values(c.indicadores).map(i => i.fuente).filter(Boolean))
)].sort();
---
<section class="cg-section cg-sources" id="cg-sources">
  <p class="cg-eyebrow">Fuentes</p>
  <ul>
    {fuentes.map(f => <li>{f}</li>)}
  </ul>
</section>
```

- [ ] **Step 3: Commit**

```bash
git add projects/informe_coyuntura/web/src/components/Metodologia.astro projects/informe_coyuntura/web/src/components/Fuentes.astro
git commit -m "feat(informe-web): Metodología + Fuentes"
```

### Task 17: `IndicadorModal.astro` + interacción

**Files:**
- Create: `projects/informe_coyuntura/web/src/components/IndicadorModal.astro`

- [ ] **Step 1: Escribir `IndicadorModal.astro`** — portar `.cg-modal#cg-modal` (vacío) + un `<script>` cliente que, al click en `.cg-ind--clickable[data-indicador]`, llena el modal con label + serie (tabla). La serie se embebe en un `<script type="application/json">`.

```astro
---
import { series, label } from "../lib/datos.ts";
const seriesJson = JSON.stringify(series);
const labelsJson = JSON.stringify(
  Object.fromEntries(Object.keys(series).map(k => [k, label(k)]))
);
---
<div class="cg-modal" id="cg-modal" hidden>
  <div class="cg-modal-card">
    <button class="cg-modal-close" id="cg-modal-close" aria-label="Cerrar">×</button>
    <p class="cg-eyebrow" id="cg-modal-eyebrow">Indicador</p>
    <h3 class="cg-modal-title" id="cg-modal-title"></h3>
    <p class="cg-modal-sub" id="cg-modal-sub"></p>
    <table class="cg-modal-table" id="cg-modal-table"></table>
  </div>
</div>
<script type="application/json" id="cg-series-data" set:html={seriesJson}></script>
<script type="application/json" id="cg-labels-data" set:html={labelsJson}></script>
<script>
  const SERIES = JSON.parse(document.getElementById("cg-series-data").textContent);
  const LABELS = JSON.parse(document.getElementById("cg-labels-data").textContent);
  const modal = document.getElementById("cg-modal");
  const close = () => modal.setAttribute("hidden", "");
  document.getElementById("cg-modal-close").addEventListener("click", close);
  modal.addEventListener("click", e => { if (e.target === modal) close(); });
  document.querySelectorAll(".cg-ind--clickable[data-indicador]").forEach(li => {
    li.addEventListener("click", () => {
      const key = li.getAttribute("data-indicador");
      const serie = SERIES[key] || [];
      document.getElementById("cg-modal-title").textContent = LABELS[key] || key;
      document.getElementById("cg-modal-sub").textContent =
        serie.length ? `${serie.length} datos históricos` : "Sin serie histórica disponible";
      const rows = serie.slice(-12).reverse()
        .map(p => `<tr><td>${p.fecha}</td><td>${p.valor.toLocaleString("es-AR")}</td></tr>`).join("");
      document.getElementById("cg-modal-table").innerHTML =
        serie.length ? `<thead><tr><th>Fecha</th><th>Valor</th></tr></thead><tbody>${rows}</tbody>` : "";
      modal.removeAttribute("hidden");
    });
  });
</script>
```

- [ ] **Step 2: Build + verificación de interacción**

Run (desde `web/`): `npm run build`. Abrir local, click en un indicador clickable → abre modal con tabla. Click afuera / × → cierra.

- [ ] **Step 3: Commit**

```bash
git add projects/informe_coyuntura/web/src/components/IndicadorModal.astro
git commit -m "feat(informe-web): modal de indicador con serie histórica"
```

---

## Phase 5 — Ensamblado final + verificación visual

### Task 18: `index.astro` completo

**Files:**
- Modify: `projects/informe_coyuntura/web/src/pages/index.astro`

- [ ] **Step 1: Ensamblar todas las secciones en orden** (mismo orden que el reference)

```astro
---
import Layout from "../layouts/Layout.astro";
import Nav from "../components/Nav.astro";
import Hero from "../components/Hero.astro";
import Bluf from "../components/Bluf.astro";
import CinturonCard from "../components/CinturonCard.astro";
import Evolucion from "../components/Evolucion.astro";
import TensionPanel from "../components/TensionPanel.astro";
import Recomendaciones from "../components/Recomendaciones.astro";
import Archivo from "../components/Archivo.astro";
import Metodologia from "../components/Metodologia.astro";
import Fuentes from "../components/Fuentes.astro";
import Footer from "../components/Footer.astro";
import IndicadorModal from "../components/IndicadorModal.astro";
import { informe, CINTURONES } from "../lib/datos.ts";
---
<Layout>
  <Nav />
  <Hero />
  <main class="cg-main">
    <Bluf />
    <section class="cg-section">
      <div class="cg-section-head">
        <p class="cg-eyebrow">Diagnóstico por capa</p>
        <h2 class="cg-h2">Los cinturones, hoy</h2>
        <p class="cg-h2-sub">Cada card ordena primero los indicadores automatizados con dato fresco.</p>
      </div>
      <div class="cg-grid">
        {CINTURONES.map(c => (
          <CinturonCard slug={c.slug} nombre={c.nombre} sub={c.sub} cinturon={informe.cinturones[c.key]} />
        ))}
        <article class="cg-cint cg-cint--humor" style="opacity:.55;">
          <div class="cg-cint-head">
            <div class="cg-cint-titles">
              <div class="cg-cint-sub">El humor social</div>
              <div class="cg-cint-name">Espíritu de la época</div>
            </div>
            <span class="cg-verdict" style="color:var(--muted);"><span class="cg-verdict-dot" style="background:var(--muted);"></span>Próximamente</span>
          </div>
          <div class="cg-cint-empty">Quinto cinturón en desarrollo — metodología pendiente.</div>
        </article>
      </div>
    </section>
    <Evolucion />
    <section class="cg-section">
      <div class="cg-section-head"><p class="cg-eyebrow">Lectura cruzada</p><h2 class="cg-h2">Tensión sistémica</h2></div>
      <div class="cg-twocol">
        <TensionPanel />
        <Recomendaciones />
      </div>
    </section>
    <Archivo />
    <Metodologia />
    <Fuentes />
  </main>
  <Footer />
  <IndicadorModal />
</Layout>
```

- [ ] **Step 2: Build final**

Run (desde `web/`): `npm run build` → Expected: OK, sin warnings de TS.

- [ ] **Step 3: Commit**

```bash
git add projects/informe_coyuntura/web/src/pages/index.astro
git commit -m "feat(informe-web): ensamblado de todas las secciones"
```

### Task 19: Verificación visual lado a lado

**Files:** (ninguno — verificación)

- [ ] **Step 1: Levantar dev server y screenshot**

Run (desde `web/`): `npm run dev` (anotar la URL local, incluye el base path). Con Playwright MCP: navegar a la URL local, resize 1440×900, screenshot full page `local-desktop.png`; resize 390×844, screenshot `local-mobile.png`.

- [ ] **Step 2: Comparar contra referencia**

Comparar `local-desktop.png` vs `reference/klipea-desktop-full.png` y mobile vs mobile. Checklist: fuentes (DM Serif en títulos), paleta teal, bordes de color por cinturón, hero, grid, footer dark. Anotar diferencias y corregir en los componentes correspondientes (commits puntuales). Diferencias de contenido esperadas (4 vs 5 cinturones, BLUF/recos placeholder, archivo de 1 mes) NO son defectos.

- [ ] **Step 3: Commit de ajustes (si hubo)**

```bash
git add -A && git commit -m "fix(informe-web): ajustes de fidelidad visual vs referencia"
```

### Task 20: Deploy final + verificación en producción

**Files:** (ninguno — verificación)

- [ ] **Step 1: Push y esperar la Action**

```bash
git push
```

- [ ] **Step 2: Verificar producción**

Abrir `https://juanpintoselso33.github.io/biblitotecario-ai/informe/`.
Expected: página completa, CSS/fuentes/logo cargan (base path OK), modal funciona, link desde la landing `…/biblitotecario-ai/` funciona.

- [ ] **Step 3: Actualizar el README del proyecto**

Agregar a `projects/informe_coyuntura/README.md` una sección "Web pública": cómo correr `python scripts/publicar.py` para regenerar el snapshot y que el push dispara el deploy. Commit + push.

```bash
git add projects/informe_coyuntura/README.md
git commit -m "docs(informe): documentar la web pública y el flujo de publicación"
git push
```

---

## Notas de mantenimiento (post-implementación)

Ciclo de actualización mensual:
1. Correr colectores (`python scripts/macro.py`, etc.) y `python scripts/generar_informe.py`.
2. `python scripts/publicar.py` → regenera `web/src/data/{informe,series}.json`.
3. `git commit` del snapshot + `git push` → CI rebuildea y deploya.

Pendientes conocidos (fuera de v1):
- 5º cinturón "Espíritu de la época" (espera documento del usuario).
- Texto editorial: BLUF, lectura cruzada, recomendaciones (hoy placeholders).
- Semáforo por indicador basado en umbrales (hoy refleja frescura).
- Enriquecer vida_cotidiana aguas arriba en `generar_informe.py` (hoy lo hace `publicar.py`).
