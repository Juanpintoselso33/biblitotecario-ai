# Pestaña Vida Cotidiana — Cinturón de Gestión Cotidiana

> Análisis matusiano del cinturón de vida cotidiana del dashboard `https://cigob.k1t.eu/index.html`. Se aplica el marco de los tres cinturones (Matus 1997) y la propuesta de 15 indicadores revisada en mayo 2026.

---

## Marco conceptual

Para Matus, el **Cinturón de la Vida Cotidiana** es el más sensible de los tres: es donde el ciudadano valida o rechaza el proyecto de gobierno según su realidad inmediata. Si este cinturón se aprieta demasiado, la presión se traslada por vasos comunicantes al cinturón de la política, erosionando la gobernabilidad (y los votos). El cinturón mide condiciones objetivas (ingresos, servicios, seguridad) y tensión emergente (conflictividad, expectativas).

---

## Propuesta de 15 indicadores — Estado de automatización

Los 15 indicadores se organizan en 4 grupos según su impacto en la vida cotidiana.
Cada uno incluye evaluación de factibilidad de automatización para el sistema CIGOB.

---

### I. Bolsillo y Consumo — Presión Económica Directa

| # | Indicador | Construcción | Fuente | Automatizable | Estado |
|---|---|---|---|---|---|
| 1 | **Brecha Salario vs. CBT** | % entre salario promedio (RIPTE) y Canasta Básica Total | INDEC (EPH + Canastas) | **Sí — Tier 1** | RIPTE: CSV directo. CBT: XLS FTP INDEC o serie API |
| 2 | **IPC-Alimentos** | Variación mensual rubro "Alimentos y Bebidas no alcohólicas" | INDEC IPC | **Sí — Tier 1** | Serie API: `146.3_IALIMENNAL_DICI_M_45`. Verificada ✓ |
| 3 | **Endeudamiento Familiar** | Saldo tarjeta de crédito + préstamos personales sobre ingreso disponible | BCRA API v4.0 | **Sí — Tier 1** | Variables 114+115. API verificada ✓. Denominador: RIPTE |
| 4 | **Peso de Tarifas** | Gasto en energía+gas+agua+transporte como % del ingreso neto | ENRE / ENARGAS / entes reguladores | **Parcial — reemplazar** | Ver nota abajo |
| 5 | **Consumo de Carne Vacuna** | Consumo aparente per cápita anual (kg/habitante) | CICCRA | **Pendiente verificar** | ciccra.com.ar — PDF mensual, no investigado aún |

**Nota indicador #4 — Tarifas:** ENRE y ENARGAS no tienen API pública ni descarga estructurada. Las resoluciones tarifarias son PDFs irregulares. **Alternativa recomendada**: usar el rubro `Vivienda, agua, electricidad y combustibles` del IPC INDEC (serie `146.3_IVIVIENDNAL_DICI_M_XX` — buscar ID en catálogo). Es mensual, automatizable, y captura el impacto real de las tarifas en el índice de precios. Si se requiere el peso exacto en el ingreso, combinarlo con RIPTE como denominador.

---

### II. Laborales y Productivos — Seguridad de Sustento

| # | Indicador | Construcción | Fuente | Automatizable | Estado |
|---|---|---|---|---|---|
| 6 | **Informalidad Laboral** | % ocupados sin aportes jubilatorios ni obra social | INDEC EPH | **Sí — Tier 1** | Serie sintética en datos.gob.ar (buscar "empleo no registrado") |
| 7 | **Mortalidad de PyMEs** | Bajas netas de CUITs comerciales/servicios mensuales | AFIP + CAME | **No disponible — reemplazar** | Ver nota abajo |
| 8 | **Despacho de Cemento/Hierro** | Variación mensual de despachos de insumos para construcción privada | AFCP + Cámara del Acero | **Parcial — Tier 2** | AFCP: PDFs con hashes opacos (complejo). Usar ISAC INDEC como proxy. Hierro: Cámara del Acero no investigada |
| 9 | **Tasa de Pluriempleo** | Proporción de ocupados con más de una ocupación | INDEC EPH microdatos | **Manual — Tier 3** | No en serie sintética pública. Requiere descargar base EPH trimestral y procesar variable de multiocupación |

**Nota indicador #7 — Mortalidad PyMEs:** AFIP no publica microdatos de altas/bajas de CUIT. **Alternativa recomendada**: CAME publica mensualmente el `Índice de Producción Industrial PyME` (IPIP) y el `Índice de Actividad Comercial PyME`. No mide cierre (mortalidad) sino actividad, pero captura el mismo fenómeno de contracción. Agregar a la pestaña con ese nombre más preciso.

---

### III. Servicios y Bienestar — Calidad de Vida

| # | Indicador | Construcción | Fuente | Automatizable | Estado |
|---|---|---|---|---|---|
| 10 | **Deserción Escolar** | Variación interanual matrícula secundaria en zonas vulnerables | Ministerio de Educación (Relevamiento Anual) | **Manual — Tier 3 / Anual** | Datos anuales con 1 año de rezago. No mensualizable. Usar como indicador estructural |
| 11 | **Espera en Salud Pública** | Promedio días para turno en especialidades críticas | SISA — Ministerio de Salud | **No disponible — reemplazar** | Ver nota abajo |
| 12 | **Inseguridad Urbana** | Tasa de victimización y hechos delictivos en centros urbanos | SNIC — Ministerio de Seguridad | **Parcial — Tier 2 con rezago** | SNIC publica datos anuales con 6-12 meses de retraso. Complementar con encuestas de victimización (LICIP-UTDT, Poliarquía) |

**Nota indicador #11 — Espera en Salud:** El SISA no publica tiempos de espera en datos abiertos. **Alternativa recomendada**: DEIS (Dirección de Estadísticas e Información en Salud) publica mortalidad infantil y por causas en Excel anual (deis.msal.gov.ar). Mide resultado, no proceso, pero es el proxy más robusto disponible. Para cobertura: el INDEC publica acceso a salud en EPH.

---

### IV. Clima y Expectativas — Humor Social

| # | Indicador | Construcción | Fuente | Automatizable | Estado |
|---|---|---|---|---|---|
| 13 | **ICC — Confianza del Consumidor** | Nivel de optimismo sobre situación económica personal y compra de durables | UTDT (serie desde 2001) | **Sí — Tier 1** | Scraping listado UTDT + descarga XLS. Verificado ✓. Abril 2026: 38.1 |
| 14 | **Sentimiento Digital** | Análisis de polaridad sobre "precios", "seguridad", "futuro" en redes | X API + Meta + NLP pipeline | **Futuro — requiere inversión** | Ver nota abajo |
| 15 | **Apatía Electoral** | Voto en blanco + nulo + NS/NC en encuestas recientes | Votómetro CIGOB (109 encuestas) | **Sí — Tier 1** | Ya disponible en el Votómetro. Leer directamente del HTML |

**Nota indicador #14 — Sentimiento Digital:** Requiere suscripción a X API (USD 100+/mes) y pipeline NLP (modelo BERT en español). **Alternativa gratuita inmediata**: Google Trends via `pytrends` para términos como "inflación", "precios", "inseguridad" en Argentina. Sin NLP pero disponible hoy, gratuito, y captura el interés en los temas aunque no la polaridad. Es un buen proxy para detectar picos de alarma social antes de que se conviertan en crisis.

---

## Matriz de factibilidad consolidada

| Tier | Indicadores | Método | Estado |
|---|---|---|---|
| **Tier 1 — Automatizable hoy** | #1 Brecha sal-CBT, #2 IPC-Alimentos, #3 Endeudamiento, #6 Informalidad, #13 ICC, #15 Apatía | API JSON o CSV directo | **6 de 15. Implementados ✓** |
| **Tier 2 — Semi-automático** | #5 Carne (CICCRA-PDF), #8 Cemento/ISAC (PDF/proxy), #12 Inseguridad (SNIC anual) | Scraping + parseo PDF | **3 de 15. Requieren trabajo de implementación** |
| **Tier 3 — Manual / Anual** | #9 Pluriempleo (EPH microdatos), #10 Deserción (anual), #4 Tarifas (proxy IPC) | Procesamiento manual o frecuencia baja | **3 de 15. Incorporar como indicadores estructurales** |
| **Requieren inversión / rediseño** | #7 PyMEs (reemplazar por CAME IPIP), #11 Salud (reemplazar por DEIS), #14 Sentimiento (Google Trends como proxy) | Cambio de fuente o pipeline nuevo | **3 de 15. Propuesta de sustitución arriba** |

---

## Datos actuales del sistema (verificados 2026-05-10)

Estos valores provienen del monitor automático (`scripts/vida_cotidiana/main.py`):

| Indicador | Valor | Fecha | Var. m/m |
|---|---|---|---|
| IPC total | 11.077 (base dic-2016) | mar-2026 | +3.38% |
| IPC Alimentos | 12.014 (base dic-2016) | mar-2026 | +3.35% |
| Índice de Salarios (total) | 8.171 (base oct-2016) | ene-2026 | +2.54% |
| Salario real (índice) | 73.77 | ene-2026 | — |
| Desocupación | 7.5% | oct-2025 (trim.) | — |
| ISAC (construcción) | 143.5 (desest.) | feb-2026 | −1.35% |
| Crédito de consumo (BCRA) | $45.2 B | may-2026 | — |
| BADLAR | 21.375% | may-2026 | — |
| ICC UTDT | 38.1 | abr-2026 | −6.7% |
| Patentamiento motos (CAFAM) | 14.815 unidades | may-2026 | — |

**Lectura matusiana del momento:** El salario real está en 73.77% del nivel base (2016), mientras la inflación en alimentos supera a la general (+3.35% vs +3.38% — aún no divergente pero sostenida). El ICC UTDT cayó 6.7% en un mes y se ubica en 38, nivel de pesimismo consistente con cinturón tensionado. La construcción baja (ISAC −1.35% m/m). El crédito de consumo sube, señal de endeudamiento sostenido. **Diagnóstico: cinturón tensionado, signo consistente con el −20 del panel anterior.**

---

## Proyecto de automatización

El monitor está implementado en `scripts/vida_cotidiana/`:

```
scripts/vida_cotidiana/
├── main.py              # Orquestador — ejecutar para recolectar datos
├── config.py            # Todos los IDs de series y endpoints
├── requirements.txt     # requests, xlrd==1.2.0, beautifulsoup4
├── collectors/
│   ├── indec_series.py  # INDEC via datos.gob.ar (IPC, salarios, EPH, ISAC)
│   ├── bcra.py          # BCRA API v4.0 (créditos, BADLAR)
│   ├── utdt_icc.py      # ICC UTDT (scraping + XLS)
│   ├── cafam.py         # Patentamiento motos (API JSON directa)
│   └── manual.py        # Documentación de fuentes manuales
└── data/                # JSONs con timestamp guardados automáticamente
```

**Comandos:**
```bash
python main.py              # Recolecta todos los indicadores automáticos
python main.py --check      # Muestra estado de fuentes manuales
python main.py --search IPC # Busca series en catálogo INDEC
```

---

## Recomendaciones de rediseño del dashboard

1. **Incorporar Tier 1 primero**: IPC-Alimentos, endeudamiento familiar (BCRA), ICC UTDT son los más potentes y están disponibles hoy.
2. **Reemplazar indicadores con fuente rota**: mortalidad PyMEs → actividad CAME IPIP; espera salud → DEIS mortalidad infantil; tarifas → rubro vivienda del IPC.
3. **Mantener como estructurales (anuales)**: deserción escolar y pluriempleo — son indicadores de contexto, no de coyuntura.
4. **Sentimiento digital**: arrancar con Google Trends (pytrends, gratuito) como primera versión. Evaluar X API cuando haya presupuesto.
5. **Direccionalidad**: añadir flecha de tendencia por indicador (mejora/empeora/estable). El score estático no captura velocidad, que es el dato matusianamente decisivo para detectar puntos de quiebre antes de la crisis.
