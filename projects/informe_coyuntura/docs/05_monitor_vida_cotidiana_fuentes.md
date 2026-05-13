# Monitor de la Vida Cotidiana — Fuentes, Métodos y Estado de Implementación

**Subtítulo:** Respuesta técnica a la propuesta de 15 indicadores para el Cinturón de la Vida Cotidiana (marco Matus)
**Fecha:** 10 de mayo de 2026
**Emisor:** Fundación CIGOB — Equipo de Datos y Análisis

---

## 1. Qué es este documento

El equipo nos acercó una propuesta de **15 indicadores** organizados en cuatro grupos (Bolsillo, Laborales, Servicios, Clima) para monitorear lo que Matus llama el **Cinturón de la Vida Cotidiana** del Triángulo de Gobierno: aquello que el ciudadano siente *antes* de leer un titular macroeconómico.

Este documento reporta el resultado de la investigación de fuentes, la escritura del código de recolección, las pruebas de cada conector y las **sustituciones** que tuvimos que adoptar cuando la fuente original no era viable (sin API, PDFs con hashes opacos, datos pagos, etc.). El criterio rector fue: **toda fuente debe ser pública, gratuita, automatizable y reproducible** desde un único script (`scripts/vida_cotidiana/main.py`).

De los 15 indicadores propuestos:

- **11 quedaron implementados y corriendo** automáticamente (con sustituciones en 6 de ellos).
- **2 quedaron implementados con fuente parcial / proxy** (sentimiento digital vía Google Trends; salud pública vía DEIS).
- **1 quedó fuera del monitor automático** por ser estructuralmente anual con rezago alto (deserción escolar).
- **1 está disponible en otro sistema CIGOB** (apatía electoral → Votómetro).

---

## 2. Tabla resumen de los 15 indicadores

| # | Indicador | Fuente real adoptada | Frecuencia | Último dato | Método | Estado |
|---|---|---|---|---|---|---|
| 1 | Brecha Salario/CBT | datos.gob.ar (RIPTE + CBT) | Mensual | mar-2026 | API JSON | OK |
| 2 | IPC-Alimentos | datos.gob.ar (serie 146.3) | Mensual | mar-2026 | API JSON | OK |
| 3 | Endeudamiento Familiar | BCRA API v4.0 | Diaria | may-2026 | API JSON | OK |
| 4 | Peso de Tarifas | IPC-Vivienda + IPC-Regulados (proxy INDEC) | Mensual | mar-2026 | API JSON | OK (proxy) |
| 5 | Consumo Carne Vacuna | CICCRA (PDF mensual) | Mensual | mar-2026 | Scraping PDF | OK |
| 6 | Informalidad Laboral | datos.gob.ar (serie 52.1) | Anual | 2025 | API JSON | OK (anual) |
| 7 | Mortalidad PyMEs | IPI Manufacturero + EMAE (proxy INDEC) | Mensual | feb-2026 | API JSON | OK (proxy) |
| 8 | Despacho Cemento/Hierro | ISAC + Acero crudo INDEC (proxy) | Mensual | feb-2026 / ene-2026 | API JSON | OK (proxy) |
| 9 | Pluriempleo | Subocupación demandante EPH (proxy) | Trimestral | oct-2025 | API JSON | OK (proxy) |
| 10 | Deserción Escolar | Min. Educación (RA) | Anual + rezago | — | Manual | NO AUTOMATIZABLE |
| 11 | Espera en Salud Pública | datos.salud.gob.ar / DEIS (proxy) | Variable | — | API CKAN | OK (proxy) |
| 12 | Inseguridad Urbana | SNIC + CABA datos abiertos | Anual (5m rezago) | 2024 (nac) / 2025 (CABA) | CSV directo | OK |
| 13 | ICC Confianza | UTDT (XLS download) | Mensual | abr-2026 | Scraping + xlrd | OK |
| 14 | Sentimiento Digital | Google Trends (pytrends) | Tiempo real | may-2026 | API no oficial | OK (rate-limit) |
| 15 | Apatía Electoral | Votómetro CIGOB | Continua | — | Externo | Disponible |

---

## 3. Detalle por indicador

### Grupo I — Bolsillo y Consumo

#### #1 — Brecha Salario Real vs. CBT

- **Descripción:** cuántas canastas básicas totales cubre el salario formal promedio. Indicador-síntesis de poder adquisitivo.
- **Fuente original propuesta:** INDEC (EPH + canastas).
- **Resultado de la investigación:** las series sintéticas mensuales están publicadas en **datos.gob.ar** (sin necesidad de tocar microdatos EPH). RIPTE como proxy de salario formal (mensual, sin rezago largo) y CBT como denominador.
- **Fuente final adoptada:**
  - RIPTE: CSV directo de `infra.datos.gob.ar` (dataset 158, distribución 158.1). Serie mensual desde jul-1994.
  - CBT: serie `150.1_CSTA_BATAL_0_D_20` vía API datos.gob.ar.
- **Frecuencia:** mensual.
- **Último valor:** RIPTE $1.734.357 (feb-2026) / CBT $464.227,77 (mar-2026) → **brecha 3,74 canastas**.
- **Método técnico:** `GET` JSON + parsing.
- **Notas:** dado que RIPTE corre un mes detrás de CBT, la brecha se calcula con el último mes común. En el monitor se reporta el ratio explícito + la fecha de cada componente.

#### #2 — IPC-Alimentos

- **Descripción:** variación de precios de alimentos y bebidas no alcohólicas. Es el componente del IPC que el ciudadano siente con mayor velocidad.
- **Fuente original propuesta:** INDEC IPC.
- **Resultado:** disponible en datos.gob.ar. El ID inicialmente buscado era incorrecto; se localizó en el catálogo filtrando por `?q=alimentos`.
- **Fuente final:** serie `146.3_IALIMENNAL_DICI_M_45`.
- **Frecuencia:** mensual.
- **Último valor:** índice 12.014,7 (base dic-2016) — **+3,35 % m/m** en mar-2026.
- **Método:** `GET` JSON, variación calculada con los dos últimos puntos.

#### #3 — Endeudamiento Familiar

- **Descripción:** stock de crédito a familias (tarjeta + personales) y costo de financiarse (BADLAR).
- **Fuente original propuesta:** BCRA + CAME.
- **Resultado de la investigación:**
  - BCRA: solo **API v4.0** funciona. v1, v2 y v3 retornan HTTP 400 ("método deprecado").
  - CAME: `www.came.com.ar` cae por DNS. El sitio operativo es `redcame.org.ar` pero **no expone API ni datos estructurados** (solo PDFs e infografías). Se descartó como fuente automatizable.
- **Fuente final adoptada:** BCRA API v4.0 (`https://api.bcra.gob.ar/estadisticas/v4.0/Monetarias`). Variables consumidas:
  - id=115 (tarjeta), id=114 (personales), id=112 (hipotecarios), id=26 (total sector privado), id=7 (BADLAR).
- **Frecuencia:** diaria.
- **Último valor:** crédito consumo = $24.344 M (tarjeta) + $20.837 M (personales) = **$45.182 M** (may-2026). BADLAR **21,375 %** (may-2026).
- **Método:** `GET` JSON, un endpoint por variable.
- **Notas:** BCRA cubre el indicador. CAME aporta valor cualitativo pero no entra al pipeline automático.

#### #4 — Peso de Tarifas (sustitución por IPC-Vivienda + IPC-Regulados)

- **Descripción:** carga de tarifas de servicios públicos en el bolsillo.
- **Fuente original propuesta:** ENRE / ENARGAS.
- **Resultado de la investigación:** ENRE y ENARGAS **no exponen API pública**. Las resoluciones tarifarias salen como **PDFs con hashes opacos en la URL**, lo que rompe cualquier scraping por patrón. No automatizable bajo restricciones razonables de mantenimiento.
- **Sustitución adoptada:** dos series del IPC-INDEC que capturan el impacto efectivo de las tarifas sobre el índice de precios:
  - **IPC-Vivienda** (agua, electricidad, gas): serie `146.3_IVIVIENNAL_DICI_M_52` → +3,71 % m/m (mar-2026).
  - **IPC-Regulados** (tarifas directas): serie `148.3_IREGULANAL_DICI_M_22` → +5,08 % m/m (mar-2026).
- **Frecuencia:** mensual.
- **Método:** `GET` JSON datos.gob.ar.
- **Limitación reconocida:** mide el impacto inflacionario de las tarifas, no el peso exacto en el ingreso de un hogar tipo. Si se desea un cociente "tarifa/salario", se puede dividir por RIPTE en una segunda capa de cálculo.

#### #5 — Consumo de Carne Vacuna per Cápita

- **Descripción:** kg de carne vacuna por habitante al año. Termómetro cultural y económico simultáneo.
- **Fuente original propuesta:** CICCRA.
- **Resultado:** CICCRA publica un informe mensual en PDF con **numeración correlativa** (Informe 300 = ene-2026, 301 = feb-2026, 302 = mar-2026). Las URLs siguen patrón regular, lo que permite construirlas a partir del número y la fecha.
- **Fuente final:** PDF en `ciccra.com.ar/wp-content/uploads/{pub_year}/{pub_month:02d}/Inf-No-{num}-{year}-{mes}.pdf`.
- **Frecuencia:** mensual (con ~1 mes de delay).
- **Último valor:** **47,3 kg/hab/año** (mar-2026, PDF del informe 302).
- **Método:** construcción de URL → `requests` GET → extracción con `pdfplumber` + regex.

### Grupo II — Laborales y Productivos

#### #6 — Informalidad Laboral

- **Fuente final:** datos.gob.ar, serie `52.1_ASDJ_0_0_37` (asalariados sin descuento jubilatorio).
- **Frecuencia:** **ANUAL.** No existe serie sintética mensual ni trimestral de informalidad en el catálogo. Una versión trimestral exigiría procesar microdatos EPH.
- **Último valor:** **36,75 %** (2025).
- **Limitación:** indicador estructural, no de coyuntura. Útil como telón de fondo, no para detectar shocks de corto plazo.

#### #7 — Mortalidad de PyMEs (sustitución por IPI Manufacturero)

- **Fuente original propuesta:** AFIP + CAME.
- **Resultado:** AFIP **no publica microdatos de altas/bajas de CUIT**. CAME publica el Índice PyME en HTML/PDF sin API.
- **Sustitución adoptada:**
  - **IPI Manufacturero** (INDEC): serie `453.1_SERIE_ORIGNAL_0_0_14_46`. Captura contracción productiva del segmento donde se concentra la PyME industrial.
  - **EMAE mensual:** serie `143.3_ICE_SERVIA_2004_A_25` como proxy adicional de actividad general.
- **Frecuencia:** mensual.
- **Último valor:** IPI = 100,5; **−6,11 % m/m** (feb-2026). EMAE arroja −43,06 % (revisar: dato volátil por revisión de base, monitorear).
- **Notas:** la lectura PyME debe combinarse con datos cualitativos de CAME publicados con menor frecuencia.

#### #8 — Despacho de Cemento e Hierro (proxy ISAC + Acero crudo)

- **Fuente original propuesta:** AFCP + Cámara del Acero.
- **Resultado:** AFCP publica PDFs con URLs de hashes opacos (no automatizable). Cámara del Acero publica PDFs mensuales sin API.
- **Sustitución adoptada:**
  - **ISAC** (Índice Sintético de Actividad de la Construcción): serie `33.2_ISAC_SIN_EDAD_0_M_23_56`.
  - **Acero crudo (miles ton):** serie `41.3_AC_0_A_11`.
- **Frecuencia:** mensual.
- **Último valor:** ISAC 143,5; **−1,35 % m/m** (feb-2026). Acero crudo 731,6 mil ton; **−9,0 % m/m** (ene-2026).
- **Método:** `GET` JSON datos.gob.ar.

#### #9 — Pluriempleo (proxy: subocupación demandante)

- **Fuente original propuesta:** microdatos EPH cruzados.
- **Resultado:** no existe serie sintética publicada del fenómeno "personas con más de un empleo".
- **Sustitución adoptada:** **Subocupación demandante**, serie `47.2_ECTSDT_0_T_47`. Capta la insuficiencia de ingresos laborales — el motor económico del pluriempleo.
- **Series complementarias incluidas:** desocupación (`42.3_EPH_PUNTUATAL_0_M_30`), empleo (`42.3_EPH_PUNTUATAL_0_M_24`).
- **Frecuencia:** trimestral (EPH).
- **Último valor:** subocupación demandante **7,8 %**, desocupación **7,5 %**, empleo **45,0 %** (oct-2025).

### Grupo III — Servicios y Bienestar

#### #10 — Deserción Escolar

- **Fuente propuesta:** Ministerio de Educación — Relevamiento Anual.
- **Resultado:** publicación **anual con 12–18 meses de rezago**. No hay API, los archivos Excel no tienen URL estable.
- **Diagnóstico:** **estructuralmente no automatizable** como indicador de coyuntura. Se recomienda incorporarlo como **dato de contexto fijo**, actualizable manualmente una vez por año.
- **Alternativa de menor rezago:** Ministerio de Educación GCBA publica datos de CABA con mayor agilidad, también anuales.

#### #11 — Espera en Salud Pública (sustitución por DEIS / CKAN)

- **Fuente original propuesta:** SISA.
- **Resultado:** SISA **no publica tiempos de espera en datos abiertos**. No hay endpoint público.
- **Sustitución adoptada:** **`datos.salud.gob.ar`** — API CKAN con datasets de mortalidad (DEIS), notificaciones epidemiológicas (SNVS) y embarazo adolescente. Mide resultado del sistema sanitario, no proceso — pero es el proxy más robusto disponible en abierto.
- **Método:** CKAN `package_show` / `package_search`. **Nota técnica:** el servidor tiene SSL cert roto → `verify=False` en todos los requests.
- **Resultado actual:** 3 datasets disponibles en primera búsqueda.

#### #12 — Inseguridad Urbana

- **Fuente final:**
  - **SNIC (Ministerio de Seguridad):** CSV directo en `cloud-snic.minseg.gob.ar/Bases/SNIC/snic-pais.csv`.
  - **CABA datos abiertos:** `cdn.buenosaires.gob.ar/datosabiertos/.../delitos_{year}.csv` (hechos geolocalizados).
- **Columnas reales del CSV nacional:** `anio, codigo_delito_snic_id, codigo_delito_snic_nombre, cantidad_hechos, cantidad_victimas, tasa_hechos, tasa_victimas` (+ desagregados por sexo).
- **Frecuencia:** SNIC nacional **anual con ~5 meses de rezago**; CABA ya tiene 2025 publicado (may-2026, 14,6 MB).
- **Último dato nacional:** **2.501.057 hechos** (2024). Top 5 categorías: Robos 460.618 / Hurtos 376.498 / Otros contra la propiedad 259.044 / Amenazas 204.599 / Lesiones dolosas 169.511.

### Grupo IV — Clima y Expectativas

#### #13 — ICC Confianza del Consumidor

- **Fuente final:** UTDT — listado de informes + descarga XLS.
- **URL base:** `https://www.utdt.edu/listado_contenidos.php?id_item_menu=16458`.
- **Método:** `requests` + `BeautifulSoup` para localizar el XLS más reciente, descarga vía `download.php?fname=...`, parsing con **`xlrd==1.2.0`** (las versiones ≥2.0 no soportan `.xls` OLE2).
- **Detalle técnico:** las celdas de fecha en el XLS tienen `ctype=3` (XL_CELL_DATE), no `ctype=2`. El parser debe contemplarlo.
- **Frecuencia:** mensual.
- **Último valor:** **ICC 38,1** (abr-2026).

#### #14 — Sentimiento Digital (sustitución por Google Trends)

- **Fuente original propuesta:** X API + Meta API + NLP.
- **Resultado:** X cuesta USD 100+/mes; Meta requiere aprobación previa para investigación. Inviable sin presupuesto y sin rol institucional formal.
- **Sustitución adoptada:** **Google Trends vía `pytrends`** (gratuito, sin API key).
- **Palabras clave (geo: AR):** `inflacion`, `precios`, `inseguridad`, `trabajo`.
- **Detalle técnico:** `urllib3` v2 rompe `pytrends` (renombró `method_whitelist` → `allowed_methods`). Se aplica monkey-patch antes de instanciar `TrendReq`.
- **Frecuencia:** tiempo real (ventana móvil últimos 3 meses).
- **Limitación:** **sujeto a rate limits de Google** — puede devolver HTTP 429. El collector tiene fallback que retorna resultado documentado sin crashear.
- **Último valor:** trabajo=14, precios=8,8, inflacion=1,5, inseguridad=0,0 (may-2026, escala 0–100).

#### #15 — Apatía Electoral

- **Fuente:** Votómetro CIGOB (109 encuestas agregadas).
- **Dónde vive el dato:** ya está disponible en `web/votometro.html`. No se duplica en este monitor.
- **Lectura actual:** NS/NC + blanco/nulo ~10–15 % persistente en encuestas recientes.

---

## 4. Arquitectura técnica del monitor

**Repositorio local:**

```
scripts/vida_cotidiana/
├── main.py                  # Orquestador: corre los 8 colectores en serie
├── collectors/
│   ├── indec_series.py      # datos.gob.ar (RIPTE, CBT, IPC, IPI, ISAC, EMAE, EPH, informalidad)
│   ├── bcra.py              # BCRA API v4.0 (crédito, BADLAR)
│   ├── utdt_icc.py          # ICC mensual (XLS)
│   ├── cafam.py             # Patentamiento motos (proxy consumo durable)
│   ├── ciccra.py            # Carne vacuna (PDF mensual)
│   ├── snic.py              # Inseguridad (CSV nacional + CABA)
│   ├── salud.py             # datos.salud.gob.ar (CKAN, DEIS, SNVS)
│   └── trends.py            # Google Trends (pytrends)
└── data/
    └── vida_cotidiana_YYYYMMDD_HHMM.json
```

**Dependencias:** `requests`, `xlrd==1.2.0`, `beautifulsoup4`, `pdfplumber`, `pytrends`.

**Ejecución:**

```bash
cd scripts/vida_cotidiana
python main.py
```

Tarda **~30 segundos**. Cada corrida deja un snapshot timestamped en `data/`. La serie histórica se reconstruye agregando los JSON sucesivos.

---

## 5. Lectura matusiana del momento (snapshot may-2026)

**Cinturón de la Vida Cotidiana — qué está sintiendo el ciudadano hoy:**

- **Bolsillo bajo presión sostenida pero contenida.** IPC general +3,38 % m/m; alimentos +3,35 %; vivienda/tarifas +3,71 % a +5,08 %. La inflación dejó de ser estallido pero no dejó de ser fricción mensual. La brecha salario/CBT en 3,74 canastas indica que el trabajador formal promedio cubre holgadamente la canasta total — pero el margen lo erosiona el rubro tarifas/vivienda, que corre por encima del promedio.
- **Crédito al consumo activo, costo alto.** $45.182 M en tarjeta + personales con BADLAR en 21,4 % anual: el endeudamiento es funcional al sostenimiento del consumo, pero a tasas que comprimen el ingreso disponible futuro. Señal típica de "fin de mes financiado".
- **Frente productivo: contracción.** IPI manufacturero −6,11 % m/m, ISAC −1,35 %, acero crudo −9 %. La construcción y la industria — donde se concentran el empleo PyME y el ingreso informal — están en zona negativa. Riesgo de traslado al cinturón laboral en próximos trimestres.
- **Empleo formal estable, subempleo demandante en alerta.** Desocupación 7,5 %, empleo 45 %, subocupación demandante 7,8 %. La población que trabaja menos horas de las que quiere supera a la desocupada: es el indicador típico de "trabajo sin sueldo suficiente".
- **Confianza débil pero no en pánico.** ICC UTDT 38,1 — territorio bajo, sin colapso. Google Trends muestra que "trabajo" es la búsqueda dominante (14), por encima de "precios" (8,8) e "inflación" (1,5): el eje de preocupación se está desplazando de precios a ingreso/empleo.
- **Inseguridad como dato de fondo.** 2,5 M de hechos a nivel nacional (2024). Robos y hurtos siguen siendo las categorías más densas. CABA 2025 disponible para análisis comparativo.

**Síntesis matusiana:** el ciudadano vive un momento de **fricción cotidiana sin estallido**. La macro mostró desinflación pero la micro mantiene tensión: tarifas que corren, crédito caro, industria fría. El cinturón de vida cotidiana está más estresado que el cinturón macro — la brecha entre titular y bolsillo es justamente lo que un gobierno con sensores debería estar leyendo.

---

## 6. Recomendaciones operativas

1. **Aceptar las sustituciones técnicas como decisiones de arquitectura, no como concesiones.** ENRE/ENARGAS, AFIP, AFCP y X API no son automatizables hoy bajo restricciones razonables. Los proxies adoptados (IPC-Vivienda, IPI, ISAC, Google Trends) son robustos y trazables.
2. **Tratar deserción escolar como dato de contexto anual.** Pedirle al equipo educativo una actualización manual una vez por año, no forzar su entrada al monitor mensual.
3. **Schedule sugerido:** corrida automática **semanal** del monitor, con publicación de tablero mensual al cierre del mes calendario (cuando INDEC ya tiene IPC y EPH del mes anterior).
4. **Próximos desarrollos (cuando haya capacidad):**
   - Capa de cálculo "tarifa/RIPTE" para complementar IPC-Vivienda con un cociente sobre salario.
   - Procesamiento de microdatos EPH para reconstruir pluriempleo real (trimestral).
   - Integración del dato del Votómetro al mismo dashboard.
   - Monitoreo de redes social con presupuesto: evaluar Brand24, Talkwalker o licencia X si CIGOB decide invertir.
5. **Mantener la disciplina del "dato público y automatizable".** Es lo que diferencia un monitor sostenible de un dashboard de demo. Cada decisión documentada en este informe sirve de criterio para futuras incorporaciones.

---

*Documento técnico — Fundación CIGOB, 10 de mayo de 2026.*
