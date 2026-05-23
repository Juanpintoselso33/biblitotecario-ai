# Cinturón Vida Cotidiana — Indicadores Activos

Orquestador: `scripts/vida_cotidiana/main.py` | Cache: `scripts/vida_cotidiana/data/vida_cotidiana_*.json`
Script puente (legacy): `scripts/vida_cotidiana.py` (expone 3 indicadores al orquestador global)
Peso en score global: **20%** (`config.py → PESOS_CINTURONES["vida_cotidiana"]`)
Barbarismo de riesgo: **político** (confundir popularidad con poder, o ignorar el malestar material)

Fuente conceptual: marco Matusiano de los cinturones de gobierno + propuesta de 15 indicadores documento "Monitor de la Vida Cotidiana" (CIGOB, may-2026).

---

## Indicadores activos (14 + manuales)

Orquestador `main.py` recolecta 8 fuentes con 32 datapoints. Mapeo contra el documento "Proyecto País" 260520:

| Concepto del doc | Indicador técnico | Fuente | Frecuencia | Estado |
|---|---|---|---|---|
| Brecha Salario Real vs. CBT | `brecha_salario_cbt` | INDEC (RIPTE + CBT) | Mensual | ✅ AUTO |
| IPC-Alimentos | `ipc_alimentos` | INDEC serie 146.3 | Mensual | ✅ AUTO |
| Endeudamiento Familiar | `prestamos_*` (tarjeta + personales + hipotecarios + consumo) | BCRA API v4.0 | Diario | ✅ AUTO |
| Peso de Tarifas | `ipc_vivienda + ipc_regulados` | INDEC | Mensual | ✅ AUTO |
| Consumo de Carne Vacuna | `consumo_carne_per_capita` | CICCRA (scraping PDF) | Mensual | ✅ AUTO |
| Informalidad Laboral | `informalidad_anual` | INDEC (asalariados sin descuento) | Anual | ✅ AUTO |
| Mortalidad de PyMEs (proxy) | `ipi + emae` | INDEC | Mensual | ✅ AUTO (proxy) |
| Despacho Cemento e Hierro | `isac + acero_crudo` | INDEC | Mensual | ✅ AUTO |
| Pluriempleo (proxy) | `subocupacion_demandante` | INDEC EPH | Trimestral | ✅ AUTO |
| Espera en Salud Pública | `salud_datasets` | DEIS / CKAN | Variable | ⚠ proxy débil |
| Inseguridad Urbana | `inseguridad_snic + delitos_caba_disponible` | SNIC + CABA abiertos | Anual | ✅ AUTO |
| ICC Confianza del Consumidor | `icc_utdt` | UTDT (scraping XLS) | Mensual | ✅ AUTO |
| Sentimiento Digital | `sentimiento_digital` (Google Trends) | pytrends | Tiempo real | ✅ AUTO |
| Patentamiento Motos (proxy consumo) | `patentamiento_motos` | CAFAM | Mensual | ✅ AUTO (extra) |
| Deserción Escolar | — | — | — | 📋 manual (rezago anual) |

**Indicador "Apatía Electoral" del doc:** está en cinturón POLÍTICO (`votometro_ventaja_lla`), no en vida_cotidiana.

---

## Estado de extracción (may-2026)

8 fuentes activas, todas devolvieron datos en última ejecución:

| Fuente | Indicadores | Última fecha |
|---|---|---|
| INDEC (datos.gob.ar) | 19 (IPC variantes, CBT/CBA, RIPTE, salario real, EPH, EMAE/IPI, faena/acero) | mar-2026 |
| BCRA API v4.0 | 6 (préstamos privados, tarjeta, personales, hipotecarios, consumo, BADLAR) | may-2026 (diaria) |
| UTDT | ICC (40.5) | may-2026 |
| CAFAM | Patentamiento motos (51.124 en may) | may-2026 |
| CICCRA | Consumo carne (PDF scraping) | abr-2026 |
| SNIC + CABA | Inseguridad (2.501.057 hechos 2024) | 2024 (anual) |
| Salud datasets | 3 datasets CKAN | — |
| Google Trends | inflación, precios, inseguridad, trabajo | tiempo real |

---

## Ejecución

```bash
cd projects/informe_coyuntura/scripts/vida_cotidiana
python main.py
# Output: data/vida_cotidiana_YYYYMMDD_HHMM.json
```

El orquestador global `scripts/vida_cotidiana.py` (legacy) expone solo `ipc_total + desocupacion + icc_utdt`. Para el dashboard completo, usar el output del `main.py`.

---

## Indicadores propuestos (no implementados)

### `ingreso_disponible_real` — Salario real vs gastos fijos del hogar ⚡ PRIORITARIO

Inspiración: [Empiria Consultores](https://empiriaconsultores.com/) (Hernán Lacunza). Captura el efecto tarifas post-subsidios que el IPC general oculta.

**Fórmula automática (sin EPH):**
```
ingreso_disponible_real(t) = IS_registrado(t) / IPC_vivienda(t)
variacion_ia = (idx_t / idx_t-12 - 1) × 100
```

| Serie | ID datos.gob.ar | Última fecha |
|---|---|---|
| IS_registrado | `149.1_TL_REGIADO_OCTU_0_16` | ene-2026 |
| IPC_vivienda | `146.3_IVIVIENNAL_DICI_M_52` | mar-2026 |

**Cálculo may-2026 (ene-2026 vs ene-2025):** −8.0% i.a. — salario perdió contra gastos fijos pese a desinflación general.

Implementar como `collectors/ingreso_disponible.py`. Score sugerido: `+3%→0, 0%→5, −5%→10`.

---

## Fórmula de score (legacy, solo 3 indicadores)

```python
score_ipc   = min(10.0, max(0.0, float(ipc)))              # 0%→0, 10%→10
score_desoc = min(10.0, max(0.0, float(desoc) / 2))         # 0%→0, 20%→10
score_icc   = min(10.0, max(0.0, (60.0 - float(icc)) / 3))  # 60→0, 30→10
score = promedio(disponibles)
```

Umbrales: `0–3` estable | `4–6` en_tension | `7–10` tensionado

**Pendiente:** scorer compuesto sobre los 14+ indicadores del orquestador `main.py` para reemplazar el legacy.

---

## Notas de mantenimiento

- **UTDT XLS:** `xlrd` requerido para parsear. ICC = pág. 16458 (Consumidor). NO confundir con ICG = pág. 16457 (Gobierno).
- **CICCRA:** scraping del PDF mensual desde `ciccra.com.ar/wp-content/uploads/YYYY/MM/`. Si cambia la estructura del PDF, ajustar `collectors/ciccra.py`.
- **BCRA SSL:** requiere `verify=False` + `urllib3.disable_warnings()`.
- **Salud datasets:** colector actual solo lista cuántos datasets hay; no procesa contenido. Mejorable.
- **Google Trends:** `pytrends` requiere rate limiting; si falla con 429, esperar y reintentar.
