# Punto 3 — Proyecto Votometro Argentina 2027
*Reunion CIGOB -- 10/03/2026*

---

## Resumen ejecutivo del punto

El Votometro es, a la fecha, el unico modelo de agregacion de encuestas con simulacion probabilistica y verificacion constitucional en Argentina. No existe un producto comparable en el ecosistema local. Agrega 78 registros de 17 consultoras, aplica una ponderacion quintuple sofisticada y proyecta una probabilidad de reeleccion de Milei del 87-92% considerando primera vuelta y ballotage combinados. El modelo demostro excelente calibracion en las legislativas 2025 (error de 0.2pp), lo que valida su nucleo metodologico.

Sin embargo, el Votometro tiene cinco problemas tecnicos concretos --el mas critico es la fragilidad de su modelo de ballotage, basado en una sola encuesta-- y opera como un archivo HTML estatico sin actualizacion automatica. La reunion debe decidir tres cosas: (1) si se invierte en profesionalizarlo, (2) quien es el propietario del producto (CIGOB solo o CIGOB+Redlines), y (3) cual es el modelo de distribucion (abierto, premium o alianza con medios). La ventana de oportunidad es ahora: faltan 18 meses para la eleccion y no hay competencia en el mercado argentino.

---

## Que es el Votometro hoy?

El Votometro es una aplicacion web estatica --un unico archivo HTML con JavaScript incrustado-- que proyecta los resultados de las elecciones presidenciales argentinas de 2027. Fue desarrollado como colaboracion entre Fundacion CIGOB y Redlines Estrategia y Comunicacion.

**Arquitectura actual:**

- Un solo archivo HTML que contiene datos, logica de calculo y visualizacion en una misma pieza
- Base de datos interna: 78 registros de encuestas desde diciembre 2023 hasta marzo 2026, provenientes de 17 consultoras
- Motor de calculo: ponderacion quintuple multiplicativa + simulacion Monte Carlo (N=10.000)
- Verificacion automatica de los articulos 97 y 98 de la Constitucion Nacional en cada simulacion
- Modulo descriptivo de correlacion ICG Di Tella - intencion de voto LLA
- Mapa federal de imagen por distrito (24 provincias) basado en CB Global Data (febrero 2026)

**Lo que el Votometro NO es hoy:**

- No es una aplicacion web dinamica: no tiene backend, base de datos externa ni API
- No se actualiza automaticamente: cada nueva encuesta requiere edicion manual del JavaScript
- No tiene URL publica permanente: se distribuye como archivo
- No tiene separacion entre datos, logica y presentacion

A pesar de estas limitaciones arquitectonicas, el Votometro es metodologicamente mas sofisticado que cualquier otra herramienta publica de proyeccion electoral en Argentina. Los medios publican encuestas individuales sin agregar; las consultoras presentan sus propios numeros sin contexto comparativo; los academicos (UdeSA, Di Tella) publican indicadores parciales pero no proyecciones electorales integradas.

---

## Proyecciones electorales actuales

### Estado de la carrera presidencial 2027

La ponderacion quintuple con decaimiento exponencial (lambda=0.015) sobre los 78 registros produce las siguientes medias ponderadas:

| Espacio politico | Media ponderada | Resultado 2025 (legislativas) | Variacion | Candidato probable |
|---|---|---|---|---|
| **La Libertad Avanza** | **~42.0%** | 40.66% | +1.3pp | Javier Milei |
| Peronismo/Fuerza Patria | ~30.0% | 31.70% (incluye aliados) | -1.7pp | Axel Kicillof |
| PRO | ~6.5-7.0% | 6.80% | estable | Bullrich/Macri |
| Provincias Unidas | ~4.5% | 8.0% (provincial) | n/a | Llaryora/Pullaro |
| FIT-Unidad | ~4.0-5.0% | 3.5% | +1.0pp | Del Cano |
| Otros | ~11-13% | 16.0% | variable | --- |

### Escenarios simulados (Monte Carlo, N=10.000, sigma=3%)

**Escenario 1 -- Victoria en primera vuelta (Art. 97/98):** La media de LLA (~42%) supera el 40% y la diferencia con el PJ (~30%) excede los 10pp requeridos por el Art. 98 de la Constitucion. Sin embargo, la volatilidad simulada (sigma=3%) hace que LLA no siempre cumpla ambas condiciones simultaneamente. **Estimacion: 30-40% de probabilidad de victoria en primera vuelta.**

**Escenario 2 -- Ballotage, Milei gana:** En segunda vuelta, el modelo asigna medias fijas (Milei 49%, Kicillof 35%) con sigma=4%. **Milei gana el ballotage en el 85-90% de las simulaciones** que llegan a segunda vuelta.

**Escenario 3 -- Ballotage, Kicillof gana:** Escenario residual, **10-15% de las simulaciones** de ballotage.

**Probabilidad total de reeleccion de Milei (primera + segunda vuelta combinadas): 87-92%.**

### Tendencia historica: tres fases

La serie temporal desde diciembre 2023 muestra una dinamica clara:

- **Fase 1 -- Luna de miel y caida (dic-23 a sep-24):** LLA pasa de 46.5% a 36.5%. Correlacion con el minimo historico del ICG Di Tella (1.94 en septiembre 2024). Periodo de ajuste economico, devaluacion y caida del poder adquisitivo.
- **Fase 2 -- Recuperacion (oct-24 a abr-25):** LLA sube de 37% a 42.5%, impulsada por la baja de inflacion, acuerdo con el FMI y salida del cepo.
- **Fase 3 -- Meseta alta (may-25 a mar-26):** LLA estabilizada en rango 40-43%. Las legislativas de octubre 2025 confirman 40.66% como piso real, validando la proyeccion del Votometro.

### Calibracion contra resultado real

El unico punto de verificacion disponible son las legislativas de octubre 2025. La media ponderada del Votometro previo a la eleccion fue de ~40.5% (encuestas CB 40.8%, Giacobbe 40.5%, Rubikon 34.6%). El resultado real fue 40.66%. **Error del modelo: 0.2pp.** Esta es una calibracion excelente, aunque se trata de un unico punto de verificacion y no debe sobreinterpretarse.

---

## Evaluacion metodologica completa

### Ponderacion quintuple: como funciona y que tan robusta es

El corazon del Votometro es un sistema de cinco factores multiplicativos que asigna un peso a cada encuesta:

1. **Decaimiento temporal (lambda=0.015):** Ponderacion exponencial con vida media de ~46 dias. Las encuestas recientes pesan significativamente mas, pero las anteriores no se descartan completamente. Es un parametro razonable para un horizonte de 18 meses.

2. **Calidad de la consultora:** Basada en el track record de 2023 y 2025. Poliarquia (1.15) y Giacobbe (1.10) reciben los pesos mas altos; Isasi Burdman (0.80) y DC Consultores (0.75) los mas bajos.

3. **Sesgo historico:** Identifica correctamente outliers sistematicos. Isasi Burdman (0.85) y DC Consultores (0.82) tienen sesgo pro-LLA documentado. Proyeccion (0.90) tiene sesgo pro-oposicion.

4. **Orientacion del medio:** Descuenta encuestas publicadas en medios con orientacion editorial marcada.

5. **Metodologia:** Privilegia encuestas presenciales y telefonicas sobre las online.

**Tabla de ponderacion por consultora (producto de 4 factores, excluyendo temporal):**

| Consultora | Calidad | Sesgo | Medio | Metodologia | Producto final |
|---|---|---|---|---|---|
| Poliarquia | 1.15 | 1.00 | 1.00 | 1.10 | **1.265** |
| Zuban Cordoba | 1.05 | 1.00 | 1.00 | 1.15 | **1.208** |
| CB Consultora | 1.10 | 1.02 | 1.00 | 1.05 | **1.177** |
| Giacobbe | 1.10 | 0.97 | 1.00 | 1.05 | **1.120** |
| Management & Fit | 1.00 | 0.98 | 0.98 | 1.00 | **0.960** |
| Opina Argentina | 1.00 | 1.00 | 1.00 | 0.95 | **0.950** |
| Trends | 0.95 | 0.95 | 0.95 | 0.90 | **0.772** |
| Atlas Intel | 0.90 | 0.95 | 0.98 | 0.90 | **0.754** |
| Proyeccion | 0.88 | 0.90 | 0.92 | 0.90 | **0.655** |
| Isasi Burdman | 0.80 | 0.85 | 0.88 | 0.85 | **0.508** |
| DC Consultores | 0.75 | 0.82 | 0.88 | 0.85 | **0.460** |

**Fortalezas del sistema:** Es significativamente mas sofisticado que promediar encuestas sin ponderacion. Captura diferencias reales entre consultoras y penaliza apropiadamente a las menos confiables. Es comparable en concepto a modelos tipo FiveThirtyEight o What UK Thinks.

**Limitaciones criticas:**

- **Los pesos son subjetivos.** No existe una formula objetiva que determine por que Poliarquia vale 1.15 y no 1.20. A diferencia de FiveThirtyEight, que calibra automaticamente sus pollster ratings con 20+ anos de datos historicos, el Votometro codifica juicio de analista en JavaScript.
- **Los factores no son independientes pero se multiplican como si lo fueran.** El sesgo de una consultora esta correlacionado con su medio de publicacion y su metodologia. Multiplicar los tres genera doble o triple penalizacion. Ejemplo concreto: Proyeccion recibe descuento por sesgo (0.90), medio (0.92) y metodologia (0.90), resultando en un factor combinado de 0.655, que posiblemente sobrepenalice a una consultora cuyo problema principal es direccional.
- **No hay intervalo de confianza para los pesos mismos.** El modelo trata los pesos como certezas cuando son estimaciones sujetas a error.

### Monte Carlo (sigma=3%): es adecuado para Argentina?

El parametro sigma=3% controla la incertidumbre en las 10.000 simulaciones. Implica que en el 95% de las simulaciones, el resultado real se espera dentro de +/-6pp de la media.

**Evidencia contra sigma=3%:**

En las PASO 2023, las encuestas subestimaron a Milei por entre 5 y 12 puntos. Ninguna consultora pronostico el 30% que obtuvo. Con sigma=3%, un error de 10pp representaria un evento de 3.3 sigmas (probabilidad 0.1%). En la realidad argentina, errores de esa magnitud han ocurrido en 3 de las ultimas 5 elecciones nacionales.

**Evidencia a favor de sigma=3%:**

En las legislativas 2025, las encuestas fueron notablemente precisas. CB Consultora (40.8%) y Giacobbe (40.5%) acertaron al 40.66% real. Esto sugiere que las consultoras argentinas mejoraron su calibracion post-2023.

**Comparacion internacional:** FiveThirtyEight usa sigmas efectivos de 3-4% para estados individuales de EEUU, pero aplica correlaciones entre estados que amplian la incertidumbre total. El AAPOR Task Force 2024 documento errores promedio de 2-3pp a nivel nacional y 4-5pp a nivel estatal en EEUU.

**Veredicto:** Para primera vuelta, sigma=3% es optimista pero aceptable dada la mejora de calibracion demostrada en 2025. Para el ballotage, donde el modelo usa medias fijas provenientes de una unica encuesta de Trends, sigma=4% es insuficiente para capturar la incertidumbre real. El modelo deberia hacer explicita esta fragilidad.

### Correccion de voto oculto: sigue siendo necesaria post-2025?

**El fenomeno en 2023:** Maria Laura Tagina (UNSAM) atribuyo el error a "altas tasas de no respuesta" y "porcentaje alto de indecisos que resultaron impredecibles ante candidatos nuevos como Milei". Chequeado documento que "existio un voto verguenza porque mucha gente no admitio que votaria a Milei, porque algunos de sus argumentos son considerados politicamente incorrectos". Las fuentes de error fueron multiples: diseno muestral, no respuesta diferencial y asignacion incorrecta de indecisos.

**La situacion post-2025:** Milei ya no es un outsider: es presidente con 40.66% confirmado en urnas. Declarar voto por LLA ya no conlleva estigma social; al contrario, es la posicion mayoritaria. Las legislativas 2025 mostraron errores mucho menores (1-2pp), sugiriendo que el "shy voter effect" se disipo sustancialmente. Sin embargo, persiste un potencial "shy anti-voter": el rechazo a Milei (52.1% segun CB, febrero 2026) podria estar subreportado en contextos donde el encuestado percibe presion social pro-gobierno.

**Conclusion:** El Votometro correctamente no aplica una correccion explicita de voto oculto en su estado actual. Deberia documentar esta decision y monitorear si el contexto cambia a medida que se acerque la campana.

### Verificacion constitucional: por que es un diferencial

El modulo que verifica automaticamente los articulos 97 (victoria directa con 45%) y 98 (victoria con 40% y ventaja de 10pp sobre el segundo) en cada una de las 10.000 simulaciones es un diferenciador genuino. Ningun otro agregador local --ni ningun medio argentino-- incorpora la logica constitucional en la simulacion. La implementacion es precisa y fiel al texto constitucional. Evalua correctamente que LLA podria ganar por Art. 98 sin necesitar el 45% del Art. 97.

### Comparacion con modelos internacionales

**FiveThirtyEight / Silver Bulletin (EEUU):**

| Dimension | FiveThirtyEight | Votometro |
|---|---|---|
| Pollster ratings | Algoritmo con 20+ anos de datos, ajuste automatico por ciclo | Pesos manuales, sin calibracion formal |
| House effects | Deteccion automatica de sesgos, neutralizacion sistematica | Correccion manual (factor SESGO), subjetiva |
| Correlacion entre jurisdicciones | Modela correlacion estado-estado | No aplica (solo nacional) |
| Incertidumbre | Varia por distancia temporal, calibrada empiricamente | Sigma fijo (3% primera vuelta, 4% ballotage) |
| Fundamentals | Incorpora economia, aprobacion, incumbency | Solo encuestas; ICG como correlato descriptivo, no input |
| N de encuestas | Miles por ciclo | 78 registros, 17 consultoras |

Brecha principal: FiveThirtyEight trata los pesos como parametros estimados estadisticamente. El Votometro los trata como juicio de analista codificado.

**Electoral Calculus / UK Polling Report (Reino Unido):** Los modelos britanicos enfrentan desafios similares (sistema multipartidario, efectos regionales fuertes). Electoral Calculus usa swing uniforme con correcciones regionales. El Votometro no tiene componente regional predictivo. Los modelos britanicos usan approval ratings como predictor directo del voto; el Votometro tiene la correlacion ICG-LLA pero no la usa como input, lo cual es una oportunidad perdida.

**PollyVote (academico):** Promedia multiples metodos (encuestas, mercados de prediccion, modelos econometricos, juicio de expertos). El Votometro es estrictamente un agregador de encuestas, lo que limita su robustez ante escenarios donde las encuestas fallan sistematicamente.

---

## Los cinco problemas tecnicos priorizados

### Problema 1: Parametros de ballotage no fundamentados (CRITICO)

El modelo asigna medias fijas de 49% a Milei y 35% a Kicillof para el ballotage, con sigma=4%. Estos numeros provienen de una unica encuesta de Trends (enero 2026). No existe un modelo de transferencia de votos de primera a segunda vuelta.

**Impacto en confiabilidad:** Cualquier cambio en la dinamica de segunda vuelta (alianzas, campana, debates) no puede ser capturado. El margen de 14pp en ballotage podria comprimirse sustancialmente si PRO, Provincias Unidas o FIT-Unidad apoyaran al candidato peronista --escenario nada improbable historicamente. Esta es la fuente de mayor fragilidad del modelo porque el ballotage es el escenario mas probable (60-70% de las simulaciones llegan a segunda vuelta) y su parametrizacion es la menos fundamentada.

**Solucion:** Construir un modelo de transferencia de votos basado en encuestas de segunda preferencia y datos historicos (ballotage 2003, 2015, 2023). Modelar al menos tres escenarios de transferencia (alta, media, baja hacia cada candidato).

### Problema 2: Datos pre-noviembre 2025 mayoritariamente reconstruidos (ALTO)

De los 78 registros, los datos entre diciembre 2023 y octubre 2024 (26 registros) tienen calidad 'C': fueron reconstruidos desde tendencias de imagen y gestion, no desde encuestas de intencion de voto publicadas. Solo a partir de diciembre 2024 la mayoria de los datos son calidad 'A' o 'B'.

**Impacto en confiabilidad:** La serie historica parece mas solida de lo que es. El decaimiento exponencial mitiga esto parcialmente (esos datos reciben peso ~0.01-0.10), pero siguen influyendo en el grafico de correlacion ICG-LLA y en la narrativa visual del modelo.

**Solucion:** Separar visualmente los datos reconstruidos de los verificados. Incluir un indicador de confianza en la serie temporal. Documentar explicitamente cuales registros son reconstrucciones.

### Problema 3: Mezcla de tipo 'candidato' y tipo 'espacio' sin normalizar (ALTO)

El modelo mezcla encuestas de "intencion de voto por espacio" (LLA como partido) con "intencion de voto por candidato" (Milei como persona). Los datos tipo 'candidato' muestran rangos mucho mas amplios (desde 34.9% de CB hasta 54% de Isasi Burdman) porque miden cosas distintas.

**Impacto en confiabilidad:** La media ponderada promedia manzanas con naranjas. Isasi Burdman reporta 54% para Milei como candidato en un escenario de fragmentacion opositora; CB reporta 34.9% en un escenario mas competitivo. Ambos se promedian con encuestas de espacio que dan 40-43%.

**Solucion:** Normalizar o separar los dos tipos. Opcion A: aplicar un factor de conversion empirico (candidato a espacio) derivado de encuestas que miden ambas cosas. Opcion B: ponderar solo encuestas de espacio para la proyeccion de primera vuelta y reservar las de candidato para analisis complementario.

### Problema 4: Ausencia de modelado de indecisos (MEDIO-ALTO)

Las encuestas reportan niveles de indecisos desde 6% (Trends) hasta 27% (UdeSA), pero el modelo no los incorpora. Los porcentajes se toman como definitivos.

**Impacto en confiabilidad:** En un escenario con 15% de indecisos, la asignacion de ese bloque puede cambiar el resultado. UdeSA (julio 2025) reporto LLA 26%, PJ 25% con 19% de indecisos + 8% NS/NC. El Votometro excluyo correctamente esta encuesta por la distorsion, pero ignorar los indecisos sistematicamente es igualmente problematico.

**Solucion:** Incorporar un modelo de distribucion de indecisos (proporcional al voto declarado, o con sesgo hacia el "challenger" como sugiere la literatura de ciencia politica).

### Problema 5: Correlacion ICG-LLA descriptiva pero no predictiva (MEDIO)

El modulo de correlacion entre el Indice de Confianza en el Gobierno (Di Tella) y la intencion de voto LLA es visualmente impactante pero no alimenta la proyeccion. Es un grafico puramente descriptivo.

**Impacto en confiabilidad:** Se desaprovecha una fuente de informacion valiosa. El ICG tiene una serie mensual continua desde 2001, lo que permitiria modelar la relacion estadistica entre confianza en el gobierno e intencion de voto del oficialismo, generando proyecciones complementarias. La correlacion visual es positiva y significativa, con rezago de ~1 mes.

**Solucion:** Estimar una regresion ICG a voto LLA y usarla como uno de los inputs del modelo, similar al componente "fundamentals" de FiveThirtyEight. Datos del ICG: minimo historico de la gestion Milei en 1.94 (septiembre 2024), dato confirmado de 2.38 (febrero 2026, IC95%: 2.26-2.51).

---

## El contexto politico actualizado

### Milei: imagen y aprobacion (febrero-marzo 2026)

La ventana de encuestas mas reciente muestra un cuadro consistente:

- **Trends (enero 2026, Clarin):** LLA 43%, Peronismo 32%. Ballotage: Milei 49%, Kicillof 35%.
- **Opinaia (enero 2026, Clarin):** LLA 42%, PJ 19% (dato atipico por metodologia).
- **CB Global Data (febrero 2026, n=2.588):** Milei piso seguro 28.7%, techo 39.2%. Rechazo a Milei: 52.1%.
- **AtlasIntel/Bloomberg (enero 2026, n=4.314):** Desaprobacion Milei 52.8%, aprobacion 43.3%.
- **Synopsis (febrero 2026):** LLA espacio 42%, PJ 31%.
- **Perfil/Proyeccion (marzo 2026):** Aprobacion gestion 44.9% positiva, 47.6% negativa.
- **Opina Argentina (enero 2026, n=3.590):** Milei 48% imagen positiva, 51% negativa.

**Sintesis:** LLA esta consolidada en el rango 41-43% como espacio, con una ventaja de 10-12pp sobre el peronismo. La imagen positiva de Milei ronda el 43-48% segun la consultora, con rechazo entre 51-53%. Son numeros estables que no muestran tendencia de deterioro respecto a las legislativas 2025. Milei lidera imagen positiva en 21 de 24 distritos (CB Global Data, febrero 2026, n=24.690).

### Kicillof: el candidato opositor mas consolidado

- Es el unico dirigente del peronismo que se mueve activamente hacia 2027 (Infobae, enero 2026).
- Asumio la presidencia del PJ bonaerense tras una cesion de Maximo Kirchner (febrero 2026), lo que consolida su posicion pero no resuelve la interna con La Campora.
- Debate sobre desdoblamiento: el peronismo bonaerense discute si repetir la estrategia de 2025 (TN, marzo 2026).
- **Principal limitacion:** 59.3% de "nunca lo votaria" (CB, febrero 2026) contra 52.1% de Milei. Ambos tienen techos bajos, pero el de Kicillof es mas restrictivo.
- CB midio piso seguro de Kicillof en 19.1%, techo en 26.9%. Estos numeros son significativamente inferiores a los de Milei.

### Villarruel como variable

CB midio que Victoria Villarruel obtendria 5.2% si compitiera como candidata separada. Este escenario es un "cisne gris" que el Votometro no modela: una candidatura de Villarruel podria restar votos suficientes a Milei para impedir la victoria en primera vuelta e incluso alterar la dinamica del ballotage. No hay encuestas de transferencia de votos que contemplen este escenario.

### Factores de riesgo para la proyeccion

- **Economia:** La evaluacion economica negativa supera la positiva (53.6% negativo segun encuesta de febrero 2026, 4.068 casos). El 40% declara no llegar a fin de mes. Por primera vez, quienes creen que la economia personal empeorara supera a los optimistas (46.7% vs 43%). Si esta tendencia se profundiza, podria erosionar la base electoral de LLA.
- **Fragmentacion opositora:** El peronismo no ha resuelto la tension Kicillof-Cristina-La Campora. La candidatura de Unac (senador sanjuanino) fragmentaria aun mas al espacio opositor.
- **PRO:** Mantiene perfil bajo con 6.5-7% pero podria diferenciar oferta electoral, restando votos a LLA en primera vuelta.

---

## El Votometro como producto: analisis de mercado

### Existe competencia en Argentina?

No. El Votometro opera en un vacio de mercado:

- **RealClearPolitics** no cubre Argentina.
- **FiveThirtyEight / Silver Bulletin** solo cubren EEUU.
- **Los medios argentinos** publican encuestas individuales sin agregar: Clarin publica Giacobbe y Trends, Perfil publica Proyeccion, cada uno sin contexto comparativo.
- **Las consultoras** presentan sus numeros sin integrarlos en un modelo probabilistico.
- **Los academicos** (UdeSA con ESPOP, Di Tella con ICG) publican indicadores parciales pero no proyecciones electorales integradas.
- **No existe otro agregador de encuestas argentino** que combine ponderacion por calidad, simulacion Monte Carlo y verificacion constitucional.

### Que lo haria la referencia del pais

Si se resuelven los problemas tecnicos de Nivel 1, el Votometro puede ser:

1. **La referencia publica de proyeccion electoral 2027 mas transparente metodologicamente de Argentina.** Al documentar su modelo, sus pesos y sus limitaciones, se posiciona como alternativa seria a las encuestas individuales que los medios publican sin contexto.

2. **Un caso concreto de "anticipacion estrategica" con datos.** CIGOB que mide y proyecta, no solo opina. Esto vincula directamente con la mision del Centro de Soluciones.

3. **Un vehiculo de visibilidad para CIGOB en medios especializados.** El Cronista, La Nacion Data, Chequeado, Cenital son medios que valoran productos de datos y podrian difundirlo.

4. **El primer paso hacia un servicio de analisis politico de datos para gobiernos.** Las proyecciones electorales son la puerta de entrada; el analisis de gestion basado en datos es el negocio a largo plazo.

### Modelo de distribucion: abierto, premium o alianza con medios?

Tres opciones no mutuamente excluyentes:

**Opcion A -- Abierto:** Publicar el Votometro como herramienta de acceso libre. Ventaja: maximiza visibilidad y credibilidad. Riesgo: no genera ingresos directos. Es el modelo de FiveThirtyEight pre-ABC News.

**Opcion B -- Premium:** Version basica abierta con proyecciones generales; version premium con escenarios ajustables, proyecciones distritales y reportes detallados. Ventaja: modelo de negocio claro. Riesgo: limita el alcance y complica el posicionamiento como referencia publica.

**Opcion C -- Alianza con medios:** Acuerdo con uno o dos medios nacionales (Infobae, Clarin) para publicacion exclusiva o preferencial de las actualizaciones del Votometro. Ventaja: distribucion masiva garantizada, legitimacion por asociacion. Riesgo: perdida de independencia percibida.

**Recomendacion:** Un modelo hibrido. Proyecciones generales abiertas para posicionamiento; informes detallados y escenarios customizados como producto premium o de alianza. El codigo del modelo deberia ser open source para generar credibilidad y contribuciones externas.

---

## Propiedad y gobernanza

### La cuestion CIGOB vs. CIGOB+Redlines

El Votometro es actualmente una colaboracion entre Fundacion CIGOB y Redlines Estrategia y Comunicacion. No existe (hasta donde se ha documentado) un acuerdo formal que defina:

- Quien es el propietario intelectual del producto
- Quien tiene derecho a publicarlo, distribuirlo o licenciarlo
- Quien es responsable de la actualizacion y el mantenimiento
- Como se distribuyen eventuales ingresos o reconocimiento publico

**Opciones y consecuencias:**

| Opcion | Ventaja | Riesgo |
|---|---|---|
| **CIGOB propietario unico** | Control total, alineacion con la mision institucional, decision unilateral sobre modelo de negocio | Posible conflicto con Redlines, perdida de colaborador tecnico |
| **CIGOB+Redlines copropietarios** | Continuidad del equipo actual, costos compartidos | Necesita acuerdo escrito, decisiones requieren consenso, complejidad si hay divergencia de intereses |
| **CIGOB propietario, Redlines licenciatario** | CIGOB mantiene control, Redlines puede usar el producto en su consultoria con atribucion | Requiere contrato formal, definicion de alcance de la licencia |

**Recomendacion:** Definir la propiedad antes de escalar. Si la respuesta es copropiedad, debe existir un acuerdo escrito que cubra: propiedad intelectual, responsabilidades de actualizacion, modelo de ingresos, derecho de publicacion y clausula de salida. Esto es prerequisito para cualquier alianza con medios o publicacion abierta.

---

## Roadmap tecnico completo

### Fase 1 -- Correcciones de credibilidad (inmediato, 0-4 semanas)

Objetivo: que el Votometro sea publicable sin riesgo reputacional.

| Tarea | Responsable sugerido | Costo estimado | Impacto |
|---|---|---|---|
| Separar datos tipo 'candidato' de tipo 'espacio' y documentar la decision | Analista CIGOB | Interno | Elimina mezcla metodologica (Problema 3) |
| Publicar la metodologia en documento separado, legible, no solo en comentarios de JS | Analista CIGOB + revisor academico | Interno | Credibilidad ante medios y academia |
| Realizar backtest formal contra legislativas 2025 y publicar resultados | Analista CIGOB | Interno | Valida el modelo (ya hay resultado: error 0.2pp) |
| Agregar seccion "ultima actualizacion" visible en el producto | Desarrollador | Interno | El usuario sabe que tan fresco es el dato |
| Incorporar bandas de confianza en todos los graficos | Desarrollador | Interno | Transparencia sobre incertidumbre |
| Documentar por que el modelo NO aplica correccion de voto oculto post-2025 | Analista CIGOB | Interno | Anticipacion de criticas |

**Costo total Fase 1:** Principalmente horas internas. Si se terceriza desarrollo web: 1-2 jornadas de un desarrollador frontend.

### Fase 2 -- Profesionalizacion del modelo (1-3 meses)

Objetivo: que el modelo sea robusto frente a critica tecnica y capture escenarios que hoy ignora.

| Tarea | Responsable sugerido | Costo estimado | Impacto |
|---|---|---|---|
| Construir modelo de transferencia de votos para ballotage con multiples escenarios | Estadistico / data scientist | Medio-tiempo, 1-2 meses | Resuelve Problema 1 (critico) |
| Calibrar pesos de consultora con formula objetiva (error cuadratico medio vs resultado real oct-25) | Estadistico | Incluido en lo anterior | Elimina subjetividad de la ponderacion |
| Incorporar modelo de distribucion de indecisos | Estadistico | Incluido en lo anterior | Resuelve Problema 4 |
| Integrar ICG Di Tella como variable predictiva (no solo descriptiva) | Estadistico | Incluido en lo anterior | Resuelve Problema 5, agrega "fundamentals" |
| Migrar de HTML estatico a aplicacion web con backend (Python/R para modelo, API REST) | Desarrollador backend | 2-3 meses medio-tiempo | Escalabilidad, actualizacion automatica |
| Separar datos en CSV/JSON actualizable sin tocar el codigo | Desarrollador | Incluido en migracion | Sostenibilidad operativa |
| Definir protocolo de actualizacion: quien, frecuencia, criterio de calidad | CIGOB direccion | Interno | Gobernanza del producto |

**Costo total Fase 2:** Un estadistico/data scientist medio-tiempo por 2-3 meses + un desarrollador backend medio-tiempo por 2-3 meses. Estimacion: pueden ser perfiles universitarios (convenio con Di Tella o UdeSA) o freelance.

### Fase 3 -- Producto publico y alianzas (3-6 meses)

Objetivo: que el Votometro sea la referencia electoral argentina para 2027.

| Tarea | Responsable sugerido | Costo estimado | Impacto |
|---|---|---|---|
| Landing page propia con URL permanente y compartible | Desarrollador frontend | 2-4 semanas | Presencia digital profesional |
| Dashboard interactivo con escenarios ajustables por el usuario | Desarrollador frontend | 4-6 semanas | Diferenciacion y engagement |
| Alianza con 1-2 medios nacionales para publicacion exclusiva/preferencial | Direccion CIGOB | Negociacion | Distribucion masiva |
| Informe quincenal "Estado de la carrera" publicable en medios | Analista CIGOB | Produccion continua | Presencia mediatica sostenida |
| Proyecciones por distrito (no solo imagen por provincia) | Estadistico + datos | Requiere datos distritales | Diferenciacion maxima |
| Incorporacion de mercados de prediccion (Polymarket) como input complementario | Estadistico | Medio | Robustez del modelo |
| Publicar codigo como open source | Equipo tecnico | Interno | Credibilidad, contribuciones externas |
| Convenio con Di Tella (ICG) o UdeSA (ESPOP) para acceso a microdatos y co-autoria | Direccion CIGOB | Negociacion | Validacion academica |
| Version en ingles para audiencia internacional/diplomatica | Traductor + desarrollador | 1-2 semanas | Alcance global |
| Modelo en vivo con actualizacion diaria en los ultimos 60 dias de campana | Equipo completo | Requiere infraestructura | Referencia en tiempo real |
| Nowcasting el dia de la eleccion | Equipo completo | Extension del modelo | Evento de posicionamiento maximo |

**Costo total Fase 3:** Variable segun ambicion. El nucleo (landing, dashboard, alianza con medio) requiere 1 desarrollador frontend por 2 meses + gestion de alianzas.

### Riesgos del roadmap

| Riesgo | Probabilidad | Impacto | Mitigacion |
|---|---|---|---|
| El modelo falla en 2027 (error >5pp) | Media | Alto | Ampliar sigma, documentar incertidumbre, comunicar siempre como probabilidades |
| Consultoras se niegan a ser calificadas publicamente | Media | Medio | Publicar metodologia de rating como transparente y replicable |
| Un competidor entra al mercado argentino | Baja | Medio | First-mover advantage, alianza con medio de primer nivel |
| Cambio regulatorio (prohibicion o restriccion de encuestas) | Baja | Alto | Modelo de fundamentals como backup (ICG, economia) |

---

## Decisiones que requiere la reunion

La reunion debe resolver o al menos encaminar las siguientes cinco decisiones:

**1. Se invierte en profesionalizar el Votometro?**
La recomendacion del equipo de analisis es si. El costo es bajo comparado con el impacto potencial en posicionamiento de CIGOB. El producto cubre un vacio real y verificable en el ecosistema argentino. La ventana de oportunidad es ahora (18 meses a la eleccion).

**2. Quien es el propietario?**
Definir si el Votometro es un producto de CIGOB, de CIGOB+Redlines, o de CIGOB con licencia a Redlines. Esta definicion es prerequisito para cualquier decision posterior sobre distribucion, alianzas o inversion.

**3. Se aprueba la Fase 1 (correcciones inmediatas)?**
Son tareas de bajo costo y alto impacto que pueden ejecutarse con recursos internos en 4 semanas. No requieren presupuesto externo significativo.

**4. Se busca un estadistico/data scientist para la Fase 2?**
El perfil puede ser universitario (convenio con Di Tella o UdeSA), freelance o medio-tiempo. Es la inversion clave para pasar de prototipo a producto.

**5. Cual es el modelo de distribucion objetivo?**
Abierto, premium, alianza con medios, o un hibrido. Esta decision condiciona la Fase 3 completa y el tipo de alianzas a buscar.

---

*Documento preparado por el equipo de analisis electoral de Fundacion CIGOB. Integra los analisis 03_votometro.md y analisis_06_votometro_profundo.md. Marzo 2026.*
