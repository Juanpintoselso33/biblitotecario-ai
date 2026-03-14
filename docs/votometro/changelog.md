# Votómetro Argentina 2027 — Changelog

Registro de cambios técnicos y metodológicos al Votómetro.

---

## [2026-03-14] Sesión de desarrollo completo — issues #2-#9

### Bugs corregidos

| Bug | Síntoma | Fix |
|-----|---------|-----|
| `diasDesdeRef` siempre = 0 | Counter "Actualizado hace X días" siempre mostraba 0 | Separar `ULTIMA_ACTUALIZACION = new Date('2026-03-01')` de `FECHA_REF = new Date()`. El counter usa `ULTIMA_ACTUALIZACION`, la ponderación temporal sigue usando `FECHA_REF` (= hoy) |
| Footer fecha hardcodeada | "Actualizado: 1 de marzo de 2026" era un string fijo | Footer ahora usa `ULTIMA_ACTUALIZACION.toLocaleDateString('es-AR', ...)` — se actualiza solo al cambiar la constante |
| Warning Giacobbe nunca disparaba | Threshold era `pct > 25%` pero el cap limita a 20% | Reemplazado por badge informativo (threshold 15%) que muestra qué consultora concentra más peso post-cap |

### Correcciones metodológicas (basadas en track record real)

Investigación de sesgos históricos (PASO 2023, Oct 2023, Ballotage 2023, Legislativas 2025):

| Consultora | Cambio CALIDAD | Cambio SESGO | Motivo |
|------------|---------------|-------------|--------|
| Giacobbe | 1.05 → 0.92 | 0.97 → 0.88 | Subestimó LLA: −11.2pp PASO 2023, −5pp leg.2025. No era "pro-LLA" como se asumía |
| Management & Fit | 1.00 → 0.90 | 0.95 → 0.92 | PASO 2023: −13pp; leg.2025: +0.24pp (mejora metodológica post-2023) |
| Isasi Burdman | 0.80 → 0.55 | 0.85 → 0.68 | Error 24pp en margen PBA legislativas 2025; sesgo pro-oficialismo extremo |
| DC Consultores | 0.75 → 0.92 | 0.88 → 0.93 | Más precisa en 2025 (+0.36pp error); era incorrectamente penalizada |

### Nuevas encuestas agregadas

| Fecha campo | Consultora | LLA | PJ | Tipo | Muestra | Calidad |
|-------------|------------|-----|----|------|---------|---------|
| 2026-02-13 | CB Global Data | 35.7% | 22.5% | candidato | 2.588 | A |
| 2026-02-23 | Analogías | 31.7% | 27.9% | candidato | 2.691 | A |

**Nota Analogías**: NsNc 23.6% sugiere poll tipo candidato (Milei persona vs. coalición). Primera aparición de esta consultora en el modelo.

### Nuevas funcionalidades UX

**Panel de filtros sobre tabla de encuestas** (`#6`)
- Filtros por calidad (Todas / Solo A / Solo A+B), período (30d / 60d / 90d / Todos) y tipo (Espacio / Candidato)
- Re-renderiza las filas en tiempo real sin tocar el modelo Monte Carlo

**Indicador de divergencia entre consultoras** (`#7`)
- Badge sobre la tabla: rango max−min LLA en las últimas 6 encuestas
- Amarillo `⚠ Alta dispersión: Xpp` si rango > 8pp; verde `✓ Baja dispersión: Xpp` si ≤ 8pp

**Escenario Villarruel como candidata** (`#5`)
- Panel colapsable con toggle después del análisis de primera vuelta
- Re-corre 10.000 simulaciones Monte Carlo con `LLA_adj = LLA_media − 5.2pp`
- Muestra comparación side-by-side: escenario base vs. con Villarruel
- PRNG independiente con prefijo `'vill-'` para reproducibilidad separada

**Links a fuente primaria** (`#8`)
- Campo `url` agregado a todos los objetos de `encuestasRaw` (~40 entradas con URL)
- Nueva columna "Fuente" en la tabla con ícono SVG external-link
- Muestra guión gris si no hay URL disponible

### Infraestructura y mantenimiento

**JSON externo como fuente canónica** (`#2`)
- `web/encuestas.json`: 98 encuestas exportadas del HTML, orden cronológico
- Permite edición directa sin tocar JS del HTML
- El HTML sigue teniendo los datos inline (dual-write) — no hay riesgo de rotura por fetch asíncrono

**Script de actualización** (`#3`)
- `scripts/actualizar_encuestas.py`: 3 modos (interactivo / CSV / JSON)
- 9 validaciones: formato fecha, suma campos (85-115%), duplicados por fecha+consultora, etc.
- Dual-write: actualiza `web/encuestas.json` + `encuestasRaw` inline en HTML + `ULTIMA_ACTUALIZACION`
- Backup automático del HTML antes de cada escritura

```bash
# Uso
python scripts/actualizar_encuestas.py              # modo interactivo
python scripts/actualizar_encuestas.py nueva.csv    # desde CSV
python scripts/actualizar_encuestas.py nueva.json   # desde JSON
```

**Protocolo de actualización** (`#9`)
- `docs/protocolo_actualizacion.md`: manual para operadores no-técnicos
- Incluye: checklist por encuesta, criterios A/B/C, tabla de consultoras, roles CIGOB/Redlines, pasos de deploy

### Estado del modelo (al 14 mar 2026)

- **98 encuestas** en el modelo (desde dic-2023 a mar-2026)
- **LLA**: ~40-42% (escenario espacio) / ~31-36% (escenario candidato)
- **PJ/Kirchnerismo**: ~28-31%
- **Última actualización de datos**: 1 de marzo de 2026
- **Última actualización técnica**: 14 de marzo de 2026

---

## [2026-03-xx] Sesión anterior — dark mode, σ calibrado, RNG reproducible

- Dark mode corregido en múltiples elementos
- σ = 3% calibrado al error histórico argentino (PASO 2023: 8-13pp)
- PRNG reproducible por día (mulberry32, seed por fecha string)
- Corrección de voto oculto bayesiana
- Verificación Arts. 97-98 CN en cada simulación

---

*Para agregar una nueva encuesta: `python scripts/actualizar_encuestas.py`*
*Para entender la metodología: ver comentarios inline en `web/votometro.html`*
