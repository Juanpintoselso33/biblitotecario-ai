# Pestaña Política — Lectura matusiana del Cinturón Político

> Análisis del cinturón político del dashboard `https://cigob.k1t.eu/index.html` desde la planificación estratégica situacional. Marco de referencia: `_brief_matus.md` (secciones 2, 4, 5 y 8).

El cinturón político es, en Matus, el continente del **capital político**: el stock de poder, legitimidad y apoyo que el gobernante gana o pierde con cada jugada (brief, sección 4). Su deterioro es la antesala silenciosa de la caída: cuando se rompe, los otros dos cinturones —económico y vida cotidiana— quedan sin contención. Una pestaña política bien diseñada debe permitir leer ese stock en sus cuatro dimensiones clásicas: **imagen, voto, conflicto y eficacia legislativa**, más una quinta que Matus repite en su obra tardía: la **cohesión interna del oficialismo**.

El dashboard CiGob-Matus presenta cuatro indicadores con score declarado **+0 (tensión moderada)**. La lectura preliminar es razonable, pero la composición del set revela un sesgo que conviene explicitar.

---

## A. Indicadores presentes

| Indicador | Valor actual | Fuente probable | Fidelidad matusiana |
|---|---|---|---|
| Aprobación de gobierno | +8 pp (saldo positivo) | Promedio de consultoras (Poliarquía, Opinaia, Zuban-Córdoba, Synopsis) | Alta. Indicador canónico de capital político inmediato. Mide el componente "imagen" del stock. |
| Votómetro 2027 | +6 pp (LLA 38% vs UxP 32%) | **Votómetro propio CIGOB** (`web/votometro.html`) — ponderación quíntuple + Monte Carlo | Alta. Es proyección de voto, segundo indicador clásico de Matus. **Activo institucional propio**: ventaja competitiva del dashboard frente a cualquier otro tablero de coyuntura argentino. |
| Conflictividad política | 58/100 (medio-alta) | Probable: índice compuesto a partir de Diagnóstico Político / CEPA / monitoreos legislativos | Media. Captura "oposición articulada" pero el 58/100 es opaco: no se sabe qué pondera (movilización, denuncias, bloqueos de quórum, declaraciones). |
| Eficacia legislativa | 42% (proyectos aprobados / enviados) | HCDN + Senado, sistema de tracking de proyectos del Ejecutivo | Alta. Indicador duro y verificable. Mide directamente la "capacidad de aprobar leyes" del listado matusiano. |

**Observación de composición**: dos indicadores miden *imagen + voto* (aprobación, Votómetro), uno mide *conflicto* y uno mide *eficacia*. Falta toda la dimensión institucional de capital político: relación con gobernadores, cohesión de bloque, judicialización, confianza institucional comparada. **2 de 4 son la misma familia de variable** (popularidad expresada en encuesta).

---

## B. Indicadores faltantes

Priorizados de mayor a menor relevancia matusiana, con foco en lo construible desde fuentes públicas argentinas. **Marcados [CIGOB]** los que son extensión natural del Votómetro y por lo tanto de **costo bajísimo** porque ya hay activo recolectado.

| # | Indicador | Por qué importa para Matus | Fuente concreta | Frecuencia | Costo |
|---|---|---|---|---|---|
| 1 | **Cohesión del oficialismo en Congreso** (% de disidencias en votaciones nominales del bloque LLA + aliados PRO) | Capital político #5: cohesión interna. Una coalición que pierde votos propios pierde gobernabilidad antes que una imagen pública. Es el indicador que faltó leer en 2001 y en 2008. | HCDN — actas de votación nominales (`votaciones.hcdn.gob.ar`) + Senado. Procesable con scraping simple. | Quincenal en período de sesiones | Bajo |
| 2 | **Posición frente a gobernadores** (índice de alineamiento: votos del bloque del gobernador en Congreso + adhesiones públicas + firmas de pactos como Pacto de Mayo / RIGI) | En el federalismo argentino, el capital político del Ejecutivo se juega en las 24 jurisdicciones. Sin gobernadores no hay leyes ni reformas estructurales. Matus lo hubiera incluido como indicador de gobernabilidad subnacional. | Construcción propia: cruce de votaciones HCDN/Senado por bloque provincial + tracker de declaraciones (Infobae provincias, La Política Online). | Mensual | Medio |
| 3 | **Judicialización del gobierno** (causas activas contra funcionarios del Ejecutivo en CSJ + denuncias en fiscalías federales + medidas cautelares contra DNUs) | Matus (capital político): la oposición articulada moderna actúa por vía judicial tanto como parlamentaria. Cautelares contra DNUs y leyes ómnibus son síntoma temprano de erosión institucional. | CIJ (Centro de Información Judicial) + observatorios (Poder Ciudadano, ACIJ). | Mensual | Medio |
| 4 | **Imagen comparada de líderes opositores** [CIGOB] (Kicillof, CFK, Massa, Macri, Larreta, Schiaretti, Pullaro) | Capital político relativo: la imagen del presidente solo se entiende contra alternativas reales. Si oposición está fragmentada y con imagen baja, +8 pp del oficialismo vale más; si hay líder opositor en alza, vale menos. | Ya existente en consultoras Poliarquía / Opinaia / Zuban-Córdoba — **es el mismo dataset que alimenta el Votómetro**. Reutilizable sin costo adicional. | Mensual | **Bajo** |
| 5 | **Movilización en calle / protesta política** | Cinturón político ≠ cinturón social: la protesta política (marchas universitarias, sindicales con bandera política, federales) es presión sobre el sistema institucional, no sobre la vida cotidiana. Es indicador de "calle" que la imagen y el voto no capturan. | CEPA (Centro de Economía Política Argentina) — informe mensual de conflictividad. Diagnóstico Político (Aronskind). Nueva Mayoría (Fraga). | Mensual | Bajo |
| 6 | **Confianza en instituciones** (Congreso, Justicia, partidos, gobierno) | Capital político de fondo: la imagen de un presidente puede ser alta sobre un piso de desconfianza institucional generalizada — y eso hace cualquier ganancia frágil. Matus lee este indicador como "legitimidad sistémica". | UTDT — Índice de Confianza en el Gobierno (ICG); Latinobarómetro (anual). | Mensual (ICG) / Anual (Latinobarómetro) | Bajo |
| 7 | **Series de Votómetro desagregadas** [CIGOB] (intención por distrito clave: PBA, CABA, Córdoba, Santa Fe, Mendoza) | El voto nacional agregado oculta la geografía política. PBA decide y tiene dinámica propia; Córdoba es bisagra. Matus pediría leer "el mapa, no el promedio". | Votómetro CIGOB ya tiene los datos provinciales en sus encuestas insumo — solo requiere desagregación visual. | Quincenal | **Bajo** |

Las filas 4 y 7 son **ganancia inmediata**: el Votómetro de CIGOB es un activo institucional propio (`web/votometro.html`, ver `CLAUDE.md`) que ya recolecta 99 encuestas con metodología quíntuple y Monte Carlo (σ=6,5 calibrado a error histórico argentino). Cualquier dashboard de CIGOB que use el Votómetro al 100% de su capacidad gana sin trabajo adicional.

---

## C. Indicadores redundantes o débiles

- **Aprobación de gobierno + Votómetro 2027** son señales correlacionadas. No son redundantes en sentido estricto —imagen presente vs proyección de voto futuro—, pero como **2 de 4 indicadores miden lo mismo desde lados parecidos**, sobreponderan la dimensión "popularidad" sobre las dimensiones "institucional" y "coalicional". Recomendación: mantener ambos, pero **reducir su peso conjunto** dentro del score y agregar al menos uno de los 1-3 de la sección B.
- **Conflictividad política 58/100** es un score sintético cuya construcción no se publica. En la metodología matusiana, los índices opacos son trampa: parecen objetivos pero en realidad encapsulan decisiones del autor. Recomendación: **abrir el indicador** en sus componentes (movilización, denuncias, obstrucción legislativa) o reemplazarlo por #5 de la sección B (movilización en calle, fuente CEPA + Diagnóstico Político — explícita y trazable).
- **Eficacia legislativa 42%** es sólido como indicador, pero el numerador "proyectos aprobados / enviados" puede sesgarse: un gobierno que envía pocos proyectos pero los hace pasar todos tendrá 100%, y un gobierno que envía muchos por estrategia de inundación tendrá 30% sin que eso sea fracaso. Sugerencia: complementarlo con **tasa de DNU** (cuántos decretos de necesidad y urgencia firma el Ejecutivo) — mide la **vía alternativa** que toma el gobierno cuando no logra aprobar por ley.

---

## D. Lectura matusiana del cinturón

**Estado actual**: tensión moderada (+0 en el scoring del propio dashboard) es lectura razonable. Hay dos indicadores en verde —aprobación +8, Votómetro +6— y dos en amarillo/rojo —conflictividad 58/100, eficacia 42%—. El cuadro coincide con la fase típica del segundo año de un gobierno de minoría: aún sostiene imagen pero ya empieza a pagar costos legislativos y de calle. Es exactamente la zona donde, según Matus, **el capital político se gasta más rápido de lo que se acumula**: cada veto judicial a un DNU, cada gobernador que se corre, cada disidencia en el bloque, descuenta del stock sin que la imagen lo refleje en tiempo real.

**Barbarismo al que está expuesto**: el barbarismo **político** (brief, sección 3 y 5; en literatura secundaria también llamado "demagógico-político"). El observador que solo mira esta pestaña ve dos indicadores de imagen/voto —aprobación y Votómetro—, uno opaco —conflictividad— y uno legislativo. Concluye, razonablemente, que el gobierno está "en tensión moderada pero arriba". Lo que **no ve** es: el bloque oficialista pierde votaciones por adentro, dos gobernadores clave bajaron del Pacto de Mayo, hay 14 cautelares contra DNUs, y la imagen de Kicillof creció 6 puntos. Toda la maquinaria institucional del capital político queda fuera de cuadro. **Eso es el barbarismo político operando en su forma demagógica: confundir popularidad con poder**, "departamentalizar la eficacia política e ignorar los problemas económicos y gerenciales para dar beneficios y favores políticos hoy que crearán mañana una crisis por agotamiento de la base económica y organizativa" (Matus, citado en brief §3). Es la misma lectura que hizo Macri en 2018 (alta imagen + parálisis legislativa + pérdida de gobernadores → derrota 2019) o Alberto Fernández en 2022.

**Recomendación de rediseño** (concreta):

1. **Sustituir uno de los dos indicadores de popularidad** (aprobación o Votómetro nacional) por el indicador #1: cohesión del bloque oficialista. El Votómetro nacional puede mantenerse como gráfico secundario; lo que el cuadro principal pierde en redundancia, lo gana en lectura institucional.
2. **Agregar el indicador #2 (gobernadores)** como cuarto fijo. En Argentina federal, sin gobernadores no hay capital político operativo. Es la diferencia entre "tener buena imagen" y "poder gobernar".
3. **Explicitar la metodología del 58/100 de conflictividad** o reemplazarlo por movilización en calle CEPA, que sí es público y auditable.
4. **Activar plenamente el Votómetro propio**: desagregar por provincia (#7) e incorporar imagen comparada de líderes opositores (#4). Son insumos que CIGOB ya recolecta — el dashboard está subutilizando un activo institucional propio. Esto es, además, un punto de diferenciación frente a cualquier tablero competidor de coyuntura argentina: nadie más tiene la serie histórica del Votómetro CIGOB con calibración Monte Carlo y prior de fundamentals.

Con esos cuatro cambios la pestaña política gana **dimensión institucional, federal y coalicional**, queda blindada contra el barbarismo político/demagógico, y capitaliza el activo que el propio proyecto ya construyó.
