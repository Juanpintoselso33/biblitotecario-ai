# Diseño — Informe de Coyuntura (web pública)

**Fecha:** 2026-05-29
**Estado:** aprobado para planificación
**Autor:** brainstorming CIGOB + Claude

---

## 1. Objetivo

Construir una página pública del **Informe de Coyuntura** de CIGOB, estéticamente idéntica al observatorio existente de klipea (`https://kbplusv2.klipea.com/portal/cigob/index.html?config=333`), pero **alimentada por nuestros propios datos** — los colectores de `projects/informe_coyuntura/` que producen `output/informe.json` y `output/series/*.csv`.

La página reemplaza la "API de Autoritas" que usa klipea por un snapshot estático de nuestros datos, generado en build.

**Principio rector de contenido:** los **indicadores automáticos y frescos tienen prioridad** — se muestran primero y destacados. Los de carga manual, placeholders y desactualizados se muestran más abajo, cada uno con una aclaración chica. Nada se oculta, pero el dato real manda.

---

## 2. Decisiones tomadas (brainstorming)

| Decisión | Resolución |
|---|---|
| Stack | **Astro** (componentes + output 100% estático). Charts/sparklines en SVG inline, sin librería pesada. |
| Cinturones | **4 con datos reales** (macro, política, vida cotidiana, gestión) + **slot "próximamente"** para el 5º ("Espíritu de la época") que aún no tiene colector. |
| Alcance | **Réplica completa de todas las secciones.** "Completa" = toda la estructura; contenido editorial arranca fino/placeholder. |
| Texto editorial (BLUF, lectura cruzada, recomendaciones) | **Placeholders** por ahora. Se definen después. |
| Fidelidad visual | **Reutilizar el CSS de klipea tal cual** (`dashboard.css`, es el portal de la propia CIGOB) y reconstruir el HTML como componentes Astro. |
| No-automáticos | Automáticos frescos arriba/destacados; manuales y placeholders abajo con aclaración por indicador. |

---

## 3. Hallazgos de la captura de klipea

Capturado con Playwright (HTML + CSS + screenshots desktop/mobile en `web/reference/`, gitignored).

- **Un solo CSS autocontenido** (`dashboard.css`, ~700 líneas) cuya única dependencia externa son Google Fonts. Reutilizable directamente.
- **Fuentes:** DM Sans (body), DM Serif Display (títulos/serif), JetBrains Mono (valores numéricos).
- **Tokens (`:root`):** `--teal #006363`, `--cta #CD7A52`, `--dark #0A1414`, `--bg-page #F7F8F7`, semáforo `--verde #16A34A` / `--amarillo #CA8A04` / `--rojo #DC2626`, y color por cinturón: macro `#1E40AF`, política `#B91C1C`, vida `#92400E`, gestión `#4338CA`, humor/espíritu `#9D174D`.
- **Estructura de secciones (clases `.cg-*`):**
  1. `.cg-nav` — nav sticky: logo pill + título/subtítulo + links (mes actual, evolución, archivo, metodología).
  2. `.cg-hero` — eyebrow + título serif + lead + 4 stat cards + status pill.
  3. `.cg-bluf` — "lectura del mes": card con borde superior arcoíris (5 colores de cinturón) + meta + texto resumen.
  4. `.cg-grid` + `.cg-cint` — grid de cards de cinturón: verdict pill, lista de indicadores con valor + unidad + dot de estado + sparkline, footer. Variantes `--macro/--politica/--vida/--gestion/--humor`.
  5. `.cg-chart-card` + `.cg-chart-grid` + `.cg-chart-mini-card` — evolución: gráfico grande + minis con delta.
  6. `.cg-twocol` → `.cg-panel` (tensión sistémica: matriz de barbarismos + texto + regla) y recomendaciones (`.cg-rec-list`, numeradas).
  7. `.cg-archive` — hemeroteca: cards por período.
  8. `.cg-method` — metodología (grid de artículos) + `.cg-sources` (fuentes en 2 columnas).
  9. `.cg-foot` — footer dark.
  10. `.cg-modal` — modal de indicador con tabla histórica; `.cg-overlay` — estado error/vacío.

---

## 4. Arquitectura

### 4.1 Ubicación y deploy

- **Fuente Astro:** `projects/informe_coyuntura/web/` (junto a los colectores que la alimentan).
- **Build output:** `web/informe/` (raíz del repo) → servido por GitHub Pages en `https://juanpintoselso33.github.io/biblitotecario-ai/informe/`.
- **Astro config:** `base: '/biblitotecario-ai/informe'`, `site: 'https://juanpintoselso33.github.io'`, `outDir` apuntando a la `web/informe` de la raíz (desde `projects/informe_coyuntura/web/` son tres niveles: `../../../web/informe`). A confirmar en el plan si conviene `outDir` relativo o un paso de copia post-build.
- **CI:** modificar `.github/workflows/pages.yml` para, antes del `upload-pages-artifact` (que sigue subiendo `web/`):
  1. `actions/setup-node`
  2. `npm ci` en `projects/informe_coyuntura/web/`
  3. `npm run build` → genera `web/informe/`
- El **Votómetro y el bibliotecario no se tocan.** Siguen como HTML estático en `web/`.
- **Base path:** verificar contra el deploy real (pitfall clásico de Pages; no se ve en local).

### 4.2 Flujo de datos

**Dos problemas a resolver (confirmados):**
1. `output/informe.json` y `output/series/*.csv` están **gitignored** → CI no los vería.
2. `informe.json` trae **solo 3 de 14** indicadores de vida cotidiana (puente legacy); la riqueza está en `scripts/vida_cotidiana/data/vida_cotidiana_*.json`.

**Solución — paso de publicación (`scripts/publicar.py`):**
- Lee `output/informe.json` + el último `vida_cotidiana_*.json` + `output/series/*.csv`.
- Hace **merge**: enriquece el cinturón vida_cotidiana con sus 14 indicadores reales.
- Escribe un **snapshot commiteado** en `projects/informe_coyuntura/web/src/data/`:
  - `informe.json` (enriquecido, los 4 cinturones completos)
  - `series.json` (series por indicador, para evolución + sparklines)
- Astro **importa ese snapshot en build** (no fetch en runtime — evita el problema de base-path).

**Ciclo de actualización:** correr colectores → `python scripts/generar_informe.py` → `python scripts/publicar.py` → commit + push → CI rebuildea y deploya.

> Nota: a futuro se puede empujar el enrichment de vida_cotidiana aguas arriba a `generar_informe.py` y que `informe.json` ya sea completo. Para v1, `publicar.py` es el seam de menor riesgo y no toca el schema existente.

### 4.3 Scores

Los `score` por cinturón y `score_global` se **muestran tal como los calcula el pipeline** (consistencia metodológica). No se recalculan en la web. La jerarquía automático/manual es solo de **presentación**, no de cálculo.

---

## 5. Componentes Astro

Mapeo 1:1 con las clases `.cg-*` de klipea (reutilizamos su CSS):

| Componente | Clase base | Datos |
|---|---|---|
| `Nav.astro` | `.cg-nav` | estático |
| `Hero.astro` | `.cg-hero` | `score_global`, conteo de cinturones rojos, período, días desde inicio |
| `Bluf.astro` | `.cg-bluf` | **placeholder** |
| `CinturonCard.astro` | `.cg-cint` | un cinturón de `informe.json` |
| `IndicadorRow.astro` | `.cg-ind` | un indicador + su sparkline desde `series.json` |
| `Sparkline.astro` | `.cg-spark-*` (SVG) | serie de un indicador |
| `EvolucionChart.astro` + `MiniChart.astro` | `.cg-chart-*` (SVG) | `series.json` |
| `TensionPanel.astro` | `.cg-panel` / `.cg-matriz` | `barbarismo_activo`, `barbarismo_riesgo`, `alerta_multicinturon` |
| `Recomendaciones.astro` | `.cg-rec-list` | **placeholder** |
| `Archivo.astro` | `.cg-archive` | solo período actual (2026-05) |
| `Metodologia.astro` | `.cg-method` | texto fijo (brief Matus + 5 cinturones) |
| `Fuentes.astro` | `.cg-sources` | URLs de `fuente` en `informe.json` |
| `Footer.astro` | `.cg-foot` | estático |
| `IndicadorModal.astro` | `.cg-modal` | tabla histórica desde `series.json` |

### 5.1 Política de presentación dentro de cada `CinturonCard`

Orden de los indicadores en la lista:
1. **Automáticos y frescos** (`desactualizado: false`, sin `estado: "placeholder"`) — arriba, con sparkline cuando hay serie.
2. **Carga manual con dato real** (ej. avances de Gestión) — debajo, con aclaración chica: badge "carga manual" + fecha del dato.
3. **Placeholders** (`estado: "placeholder"`) y **desactualizados** (`desactualizado: true`) — al final, atenuados, con aclaración: "— pendiente" o "dato a {fecha}".

El dot de estado (verde/amarillo/rojo) y el badge de frescura usan los flags que ya trae `informe.json`.

---

## 6. Mapeo sección → dato (qué es real / fino / placeholder en v1)

| Sección | Fuente | Estado v1 |
|---|---|---|
| Hero stats | `informe.json` | **Real** |
| BLUF / resumen del mes | — | **Placeholder** |
| Cards 4 cinturones | `informe.json` (vida enriquecido) | **Real** |
| 5º cinturón "Espíritu de época" | — | **Slot "próximamente"** |
| Sparklines + Evolución | `series.json` | **Real** donde hay serie (macro, vida, parte de gestión); **fino** donde no |
| Tensión sistémica + barbarismos | `informe.json` | **Real** |
| Recomendaciones | — | **Placeholder** |
| Archivo / hemeroteca | `informe.json` | Solo **mayo 2026** (klipea tiene desde feb; el nuestro arranca ahora) |
| Metodología + Fuentes | brief Matus + `informe.json` | **Real** |

---

## 7. Límites de alcance (YAGNI)

- Sin backend ni API en runtime — todo build-time estático.
- Sin auth/admin — la edición editorial es por archivos + commit.
- Reutilizamos el CSS de klipea; **no rediseñamos**.
- Sin migración del Votómetro ni del bibliotecario.
- El 5º cinturón no se diseña metodológicamente acá (queda pendiente el documento del usuario).
- Los archivos de referencia (`klipea-page.html`, `klipea-dashboard.css`, `klipea-*.png`) se mueven de la raíz del repo a `projects/informe_coyuntura/web/reference/` (gitignored).

---

## 8. Verificación de fidelidad

- Levantar la página local y comparar lado a lado con los screenshots `web/reference/klipea-desktop-full.png` y `klipea-mobile-full.png`.
- Verificar el `base path` contra un deploy real de Pages (preview o rama), no solo en local.
- Confirmar que las fuentes Google cargan y los tokens de color coinciden.

---

## 9. Riesgos conocidos

| Riesgo | Mitigación |
|---|---|
| Base path mal configurado (pitfall de Pages) | Import en build (no fetch), `base` explícito, test en deploy real |
| Datos gitignored no llegan a CI | `publicar.py` escribe snapshot commiteado en `web/src/data/` |
| Vida cotidiana incompleta (3/14) | merge desde `vida_cotidiana_*.json` en `publicar.py` |
| "Réplica completa" malinterpretada como contenido completo | Documentado: completa = estructura; BLUF/recos/archivo arrancan finos |
| Reutilizar CSS ajeno | Es el portal de la propia CIGOB; el usuario confirmó autorización |
