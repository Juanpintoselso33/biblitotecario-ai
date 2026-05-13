# Marco metodológico: fidelidad matusiana del dashboard CiGob

> Análisis crítico del andamiaje metodológico del tablero `https://cigob.k1t.eu/index.html` desde la planificación estratégica situacional (PES) de Carlos Matus. Brief de referencia: `_brief_matus.md`. Foco: el método, no los indicadores.

---

## 1. Qué es el "Método CiGob-Matus" — la declaración del sitio

El dashboard se presenta como una adaptación operativa del enfoque PES. La pieza explícita aparece en la introducción del tablero, donde se afirma que la herramienta *"organiza la realidad en tres cinturones de la situación"* siguiendo a Matus, y agrega un cuarto cinturón propio (CIGOB / Gestión) que captura la *"capacidad técnica de operacionalizar las decisiones"*. La regla operativa más visible es la del semáforo: la alerta se activa cuando *"dos o más cinturones entran en zona tensionada simultáneamente"*, situación leída como *"pérdida de grados de libertad y aproximación a punto de ajuste"*.

Hay entonces dos capas que conviene separar para el análisis:

- Una capa **fiel a Matus 1997**: tres cinturones, regla de no apretarlos a todos a la vez, semáforo como traducción de "pérdida de grados de libertad".
- Una capa de **adaptación CiGob**: un 4º cinturón propio, scoring numérico binario por indicador, renombramiento de "gestión cotidiana" como "Vida Cotidiana — Licencia Social", énfasis en datos cuantitativos públicos.

El resto de este análisis disecta cada capa.

---

## 2. Fidelidades

| Componente del dashboard | Fuente matusiana | Fidelidad |
|---|---|---|
| Tres cinturones (Político / Económico / Vida Cotidiana) | *Los Tres Cinturones del Gobierno*, Matus 1997 | Alta |
| Regla "1 cinturón tensionado = amarillo, 2+ = rojo" | Regla matusiana: los tres cinturones no pueden estar apretados a la vez | Alta como traducción operativa |
| Umbrales de score (≥+30 holgado / 0–29 tensión moderada / <0 tensionado) | Noción matusiana de "grados de presión" sobre el sistema | Razonable, aunque el quiebre numérico es arbitrario |
| Lectura del aprieto como pérdida de grados de libertad | Concepto central de PES: el actor pierde maniobra a medida que el sistema se tensiona | Fiel |
| Inclusión de un 4º juego macroorganizativo (CIGOB / Gestión) | Matus tardío / Teoría del Juego Social — 4º juego macroorganizativo | Fiel en la idea, débil en la operacionalización |

El núcleo conceptual del tablero está bien anclado. Los tres cinturones no son una etiqueta decorativa: el dashboard efectivamente computa balances separados por cinturón y lee el sistema en función del número de cinturones simultáneamente apretados. Esa traducción semafórica es probablemente la mejor decisión metodológica del producto, porque captura sin pérdida la regla de oro de Matus: la gobernabilidad no consiste en estar bien en todo, consiste en no estar mal en todo.

---

## 3. Adaptaciones y desviaciones

Hay tres adaptaciones que el dashboard introduce sobre Matus original. Cada una tiene un costo metodológico que conviene declarar.

**3.1 Renombramiento "gestión cotidiana → Vida Cotidiana — Licencia Social"**

El término "licencia social" inclina la lectura del cinturón hacia conflictividad y consumo, dejando en segundo plano lo que Matus llamaba "los problemas terminales del ciudadano": educación, salud, seguridad, pobreza estructural. El tablero refleja ese sesgo: de los cinco indicadores del cinturón, cuatro son de coyuntura (salario real, conflictividad social, PyME, cemento) y solo uno (gasto en seguridad social) toca el plano estructural. La consecuencia es un cinturón con buena lectura de pulso pero pobre lectura de problemas.

**3.2 Adición del 4º cinturón "CIGOB / Gestión"**

El agregado es legítimo: corresponde al juego macroorganizativo de Matus tardío (TJS). Pero está subponderado. Dos indicadores frente a siete del cinturón macro y cinco del cinturón cotidiano. Y, además, no se le calcula score público en la síntesis del propio dashboard. Es un cinturón presente pero mudo. El riesgo es de exhibición sin lectura: aparecer con la bandera matusiana del 4º juego sin pagar el costo de medirlo.

**3.3 Operacionalización por datos cuantitativos públicos**

Matus original era explícitamente más cualitativo-situacional. El método PES privilegiaba el análisis del actor, el cálculo interactivo y la situación como construcción narrativa. El dashboard CiGob, en cambio, depende de series públicas (INDEC, BCRA, encuestas) que se agregan como un balance binario. La ganancia es enorme en transparencia y monitoreo en tiempo real. El costo es la pérdida del momento situacional: el dashboard sabe qué pasó pero no sabe quién está jugando contra quién.

**3.4 Diagnóstico vs situación — la distinción matusiana clave**

Matus distingue tajantemente entre **diagnóstico** (lectura técnica, externa, "objetiva" del estado de cosas, del tipo que produce un consultor o un organismo internacional) y **situación** (lectura desde un actor con proyecto, donde los hechos importan en función de cómo afectan o son afectados por ese proyecto). Toda la PES descansa en ese giro: la sala de situación matusiana **no es un tablero de diagnóstico** sino un dispositivo donde un actor concreto lee la realidad desde su propio cálculo. Ver brief, §7.

El dashboard CiGob, por construcción, opera en clave de diagnóstico: es un panel sin actor inscrito, leíble del mismo modo por un funcionario, un consultor opositor o un periodista. Eso es defendible como producto público, pero no es ortodoxia matusiana. La consecuencia es que el dashboard no responde a la pregunta canónica de Matus —*¿quién juega contra quién, con qué recursos, en qué tablero?*— sino a una más débil: *¿cómo están las variables?*. Un futuro upgrade hacia ortodoxia situacional requeriría inscribir un actor, un proyecto y una hipótesis sobre los oponentes. Sin eso, el tablero sirve para alertar pero no para planificar.

---

## 4. Limitaciones del scoring actual frente a Matus

La fórmula reportada — `(positivos − negativos) / total × 100` — es un balance estático que pierde información matusianamente crítica.

| Dimensión perdida | Por qué importa en Matus | Cómo se manifiesta el problema |
|---|---|---|
| **Dirección** | Un indicador rojo mejorando y uno verde empeorando son situaciones opuestas | El score no distingue; ambos cuentan igual |
| **Velocidad** | La PES razona en tasa de cambio, no en stock | Una caída de 5 pp en un mes y 5 pp en un año pesan igual |
| **Interacción entre cinturones** | El apriete económico genera apriete cotidiano con rezago, que erosiona el político | El score es ortogonal por cinturón; no hay matriz de transmisión |
| **Stocks vs flujos** | Aprobación es stock; IPC mes es flujo. No son comparables al mismo nivel | El balance los agrega como si lo fueran |
| **Capital político acumulado** | Variable transversal de Matus, condiciona la maniobra | No aparece como variable: se infiere indirectamente desde aprobación |
| **Ponderación intra-cinturón** | No todos los indicadores presionan igual | Reservas y brecha cambiaria pesan lo mismo en macro |
| **Reducción binaria** | La PES lee gradiente, no umbral | Cada indicador es positivo o negativo; se pierde la zona gris |

La consecuencia práctica es que el score puede dar una lectura tranquilizadora cuando varios indicadores están en deterioro simultáneo pero todavía del lado positivo, y puede dar una lectura alarmista cuando varios indicadores cruzan el cero por márgenes pequeños sin mover la situación real. El dashboard captura niveles, no dinámicas.

**Doble criterio de eficacia (Weber, recogido por Matus)**: la PES distingue entre *eficacia formal o técnica* (cumplimiento de metas medibles, indicadores en verde) y *eficacia material o política* (¿la acción produjo el resultado político buscado, sostuvo capital político, viabilizó el proyecto?). Un gobierno puede tener indicadores macro impecables (eficacia técnica) y desplomarse políticamente (eficacia material baja) — el caso clásico es Macri 2018-2019. El scoring del dashboard mide solo la primera dimensión. Para incorporar la segunda haría falta cruzar cada indicador con su impacto sobre capital político del actor de gobierno — algo más cercano a la sala de situación matusiana que al diagnóstico actual. Ver brief, §5 y §7.

---

## 5. Lo que falta en términos del Triángulo de Gobierno

El tablero mide bien un solo vértice del triángulo matusiano.

| Vértice | Cobertura del dashboard | Observación |
|---|---|---|
| **Gobernabilidad** (variables del entorno) | Alta | Es el grueso de los 18 indicadores; macro, política externa, vida cotidiana son lectura de entorno |
| **Proyecto de Gobierno** (qué se quiere hacer) | Marginal | Solo aparece como "cumplimiento de proyectos estratégicos" (64%) en el cinturón CIGOB. No hay mapeo de objetivos declarados vs ejecutados |
| **Capacidad de Gobierno** (experticia, métodos, dominio del equipo) | Ausente | Ningún indicador toca dominio técnico-político, calidad de planificación, ni profesionalización de equipos |

La omisión de la Capacidad de Gobierno es paradójica: es exactamente el vértice donde CIGOB tiene tradición y diferencial. Un dashboard que se autodeclara "CiGob-Matus" y no mide capacidad estatal en sentido fuerte renuncia a su propio activo de marca. Aquí hay espacio de mejora con alto retorno reputacional.

---

## 6. Propuestas concretas de mejora metodológica

1. **Agregar deltas a cada indicador.** Variación 30 / 90 / 365 días, visible al lado del valor. Permite leer dirección y velocidad sin tocar el score base.
2. **Ponderar dentro del cinturón.** Una matriz de pesos sencilla (alto / medio / bajo) por indicador. En macro: reservas y EMBI pesan más que despacho de cemento.
3. **Matriz de interacción entre cinturones.** Tabla 4×4 con coeficientes simples que muestren cómo un apriete en macro presiona vida cotidiana con rezago t+1, y cómo eso impacta sobre político en t+2. No requiere modelo econométrico: una visualización con flechas y pesos cualitativos ya añade lectura matusiana.
4. **Hacer transparente el método de cálculo de los compuestos.** Conflictividad política (58/100), conflictividad social (64/100) y productividad estatal (47/100) son los tres indicadores opacos. Publicar la fórmula y las fuentes los vuelve auditables.
5. **Incorporar el Triángulo de Gobierno completo.** Una pestaña adicional con dos secciones: (a) Proyecto — objetivos declarados del gobierno con grado de avance; (b) Capacidad — indicadores de calidad técnica del equipo (perfiles, rotación, profesionalización, sistemas de planificación).
6. **Dashboard de barbarismos.** Alerta automática que identifique sesgo de gobierno según la triada canónica matusiana — **político** (solo política e imagen, también llamado "demagógico-político" en literatura secundaria), **tecnocrático** (solo macro), **gerencial-burocrático** (solo gestión). Es la lectura matusiana clásica que el tablero hoy no devuelve. Ver `_brief_matus.md` §3 para nomenclatura y §13 para nota sobre la variante "demagógico".
7. **Versión histórica retrospectiva.** Reconstruir el cuadro con datos de Macri, Fernández y Milei en momentos críticos. Calibra los umbrales y permite que el usuario lea el presente con referencia comparada en lugar de absoluta.

---

## 7. Tradición de mediciones similares — referencia comparada

Hay tres tradiciones útiles para situar al dashboard CiGob:

- **Fundación Altadir y la red Matus.** Altadir, fundada por Matus, mantuvo el método PES en clave consultiva sin dashboards públicos: la PES es performativa, no monitora. Un tablero matusiano público es, en ese sentido, una innovación; el costo es la tensión inevitable con el carácter situacional del método original.
- **Tradición académica de gobernabilidad cuantitativa.** El Worldwide Governance Indicators del Banco Mundial mide seis dimensiones (voz y rendición de cuentas, estabilidad política, efectividad gubernamental, calidad regulatoria, Estado de derecho, control de corrupción) con metodología agregativa de fuentes secundarias. Es el contrapunto natural: alto rigor estadístico, baja lectura situacional. Un dashboard CiGob-Matus debería distinguirse por lo segundo, no competir con lo primero.
- **Latinobarómetro y los barómetros regionales.** Capturan percepción ciudadana con series largas. Útiles como insumo del cinturón político y del cinturón vida cotidiana, no como reemplazo del método. El dashboard CiGob no los usa hoy; podría incorporarlos como serie de calibración.

La oportunidad de posicionamiento de CiGob es clara: ser el único tablero argentino que opera con el método situacional, no con el método agregativo. Para sostener esa diferencia hay que profundizar lo que el dashboard hace distinto (interacción entre cinturones, lectura del actor, dinámica) y dejar de competir en el terreno donde los WGI ganan por escala.

---

## 8. Cierre

El dashboard CiGob-Matus tiene un núcleo conceptual bien plantado: los tres cinturones, la regla del semáforo y la incorporación del juego macroorganizativo como 4º cinturón son fieles a la tradición. El costo de la operacionalización pública y cuantitativa es real pero asumible. Las dos brechas más serias son metodológicas y reparables: el scoring estático que pierde dirección, velocidad e interacción, y la cobertura parcial del Triángulo de Gobierno que deja sin medir Proyecto y Capacidad. Cubrir esas dos brechas convierte al tablero de una buena traducción de Matus a una herramienta diferencial. Sin esa cobertura, el riesgo es exhibir la bandera del método sin pagar el costo de su rigor.
