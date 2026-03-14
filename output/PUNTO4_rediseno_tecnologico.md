# Punto 4 — Rediseño Tecnológico: CIGOB impulsado por IA
*Reunión CIGOB · 10/03/2026*

---

## Resumen ejecutivo del punto

Este documento consolida el análisis y las propuestas para la transformación tecnológica de Fundación CIGOB a través de la incorporación de inteligencia artificial. La tesis central es que CIGOB no puede predicar "Anticipación Estratégica" y operar sin IA: la coherencia entre discurso y práctica es el mensaje. La propuesta se organiza en torno a un primer producto concreto — "El Bibliotecario", un sistema de consulta conversacional sobre el corpus documental de CIGOB — con tres opciones de implementación (RAG sobre documentos propios, asistente conectado al Votómetro, asistente interno para el equipo), una secuencia recomendada de despliegue desde la Semana 1 hasta el Mes 3+, y un horizonte de Fase 2 que incluye escucha social, análisis de encuestas y planes de gobierno asistidos por IA.

El contexto es de urgencia moderada: CIPPEC ya publicó su guía de IA para el sector público (mayo 2025), la Coalición CIIAR nuclea a diez ciudades argentinas trabajando en IA, y municipios como Mendoza, CABA y Tucumán ya tienen iniciativas avanzadas. La ventana de oportunidad para que CIGOB se posicione como actor relevante en este espacio existe, pero se está cerrando. La reunión debe definir: si el Bibliotecario arranca interno o externo, cuál opción técnica se adopta primero, y quién lidera la implementación.

---

## Por qué ahora y por qué CIGOB

### El argumento estratégico: coherencia entre discurso y práctica

Los documentos fundacionales de CIGOB ya construyeron el marco intelectual para este movimiento. El paper de posición de Babino establece tres principios:

- "No somos profetas del fin, somos profetas de la anticipación."
- "El riesgo no es la IA en sí, sino la *simplificación tecnológica* que desplaza a la política" (siguiendo a Innerarity).
- "La responsabilidad de la implementación es política. La tecnología es el motor."

La Propuesta Estratégica 2026-2027 organiza a CIGOB en tres unidades — Centro de Comunicación, Centro de Estudios (CECIG) y Centro de Soluciones — con contenidos diferenciadores como "Federalismo de Precisión", "Profetas de la Anticipación" y "Gobernanza de la Incertidumbre". Toda esta arquitectura narrativa presupone una capacidad tecnológica que hoy no existe operativamente.

Adoptar IA en CIGOB no es un cambio de herramientas: es la demostración viva del posicionamiento. Una fundación que predica anticipación estratégica frente a la disrupción tecnológica y opera sin ninguna herramienta de IA pierde credibilidad ante sus propios interlocutores — gobernadores, intendentes, medios, cooperación internacional. La coherencia entre el discurso y la práctica *es el mensaje*.

Además, la transformación tecnológica interna alimenta directamente el pipeline institucional: lo que CIGOB aprenda implementando IA internamente se convierte en conocimiento transferible al Centro de Soluciones. "Hicimos esto en CIGOB, podemos ayudarte a hacerlo en tu provincia" es una propuesta de valor concreta, verificable y vendible.

### El ecosistema competitivo: CIPPEC, CIIAR, Mendoza, CABA ya se movieron

El análisis del ecosistema revela un panorama más dinámico de lo que los documentos internos de CIGOB reconocen. La brecha subnacional existe, pero no es un vacío:

**Nivel provincial:**
- **Provincia de Buenos Aires (2024):** Creó la Unidad de IA aplicada a la Seguridad (UIAAS), la Dirección de Digitalización e IA, y publicó Directrices de Uso de IA Generativa en la Administración Pública.
- **Chaco (2024):** Ley de regulación de IA en el ámbito del Ministerio de Educación provincial.

**Nivel municipal:**
- **Ciudad de Mendoza (2024):** Comité Local de IA (CLIA) creado por Decreto 832/2024. Espacio institucional pionero con participación de universidades, expertos, empresas y sociedad civil.
- **Ciudad de Buenos Aires:** Boti incorporó IA generativa basada en LLMs en 2024 para turismo. La Procuración creó una Dirección de IA.
- **San Miguel de Tucumán:** Seleccionada por Bloomberg Philanthropies para el programa City Data Alliance.
- **Prometea (Justicia):** Sistema de IA para dictámenes judiciales, citado por la OCDE como caso argentino con control humano.

**Coaliciones y redes:**
- **CIIAR (Coalición de Ciudades por la IA en Argentina):** Creada en noviembre 2024 por diez municipios (Córdoba, Rosario, Mendoza, Neuquén, Tucumán, Salta, Tres de Febrero, Pilar, Escobar, Catamarca). Convocatoria abierta a nuevos municipios en diciembre 2025. CIGOB no aparece en esta red.
- **CIPPEC:** Publicó en mayo 2025 una "Guía para el uso de IA en el sector público en Argentina" con mapeo detallado de iniciativas provinciales y municipales. Ya está trabajando activamente en IA para gobiernos subnacionales.

**Nivel nacional:**
- Múltiples proyectos de ley en trámite en el Congreso (al menos 7 iniciativas entre 2024-2025), incluyendo propuestas de creación de un Consejo Federal de IA (COFEIA).

**Actores regionales que CIGOB no menciona en sus documentos:**
- **ILIA (Índice Latinoamericano de IA):** Publica informes anuales sobre gobernanza de IA en la región. Su edición 2025 mapea estrategias nacionales, mecanismos de participación ciudadana y brechas regulatorias.
- **DataGénero:** Mapeo de proyectos de ley sobre IA en Argentina.
- **OCDE:** Informe "Gobernar con IA" (2025) con casos argentinos.

**Conclusión del análisis competitivo:** CIGOB corre el riesgo de llegar tarde a un espacio que ya está siendo ocupado. No mapear a estos actores debilita la pretensión de ser relevante en este campo. La prioridad no es solo adoptar IA internamente, sino hacerlo de manera visible, documentada y articulada con el ecosistema existente.

---

## La IA como activo de posicionamiento

### Cómo usar la transición como marketing institucional

La adopción de IA por parte de CIGOB debe ser tratada no solo como un proceso interno, sino como una oportunidad de comunicación estratégica. El análisis identifica cuatro líneas de acción:

**1. Narrar el proceso en público.** No anunciar el resultado final. Documentar la transformación: qué se intentó, qué funcionó, qué no. Un blog, un newsletter, un hilo de posts. Los referentes que comunican su proceso de adopción tecnológica construyen más credibilidad que los que solo muestran el producto terminado. Esto se articula directamente con el Centro de Comunicación de la Propuesta Estratégica, que tiene entre sus funciones la gestión de narrativa y redes institucionales.

**2. El Bibliotecario como caso de estudio propio.** El primer producto de IA de CIGOB debe ser también su primer caso de estudio. "Construimos esto, así funciona, esto aprendimos" — es contenido, es posicionamiento y es demostración de capacidad en simultáneo. El CECIG puede publicar la metodología y los aprendizajes como monografía; Comunicación puede difundirlo como serie de contenido; Soluciones puede usarlo como credencial ante potenciales clientes.

**3. Posicionarse como mediadores, no como evangelistas.** El mercado ya está lleno de vendedores de IA. CIGOB tiene una posición diferencial: está del lado de los gobernantes que tienen que *gestionar* la IA sin necesariamente entenderla. Eso es más valioso y menos transitorio. Esto conecta con la crítica al documento de posición de Babino: la verdadera diferencia de CIGOB no está en el discurso sobre IA, sino en la experiencia acumulada desde 2005 en fortalecimiento de capacidades de gobierno. La IA es el vehículo; la gestión pública es la sustancia.

**4. Vincular la adopción interna con la oferta a gobiernos.** "Hicimos esto en CIGOB, podemos ayudarte a hacerlo en tu provincia/municipio" es una propuesta de valor concreta que el Centro de Soluciones puede ejecutar. Actualmente, el Centro de Soluciones carece de especificidad técnica — "escucha activa", "sistemas de decisión" y "planes de gobierno" son descripciones genéricas. El Bibliotecario y las herramientas de IA le dan contenido concreto a esa oferta.

### Qué hace diferente a CIGOB frente a otros actores

La Propuesta Estratégica identifica una combinación que ningún otro actor ofrece exactamente: análisis político + herramientas tecnológicas (Votómetro, tableros) + consultoría de gestión subnacional, todo desde una narrativa de "anticipación" e IA.

Pero la diferenciación real necesita sustancia. Tres elementos la sostienen:

1. **La experiencia en gestión subnacional desde 2005.** CIPPEC tiene investigación de políticas públicas; Fundación Mediterránea tiene análisis económico regional; Poliarquía tiene encuestas. CIGOB tiene experiencia en la conducción política de los gobiernos. Eso es lo que permite pasar de "implementar IA" (lo que ofrecen los técnicos) a "gobernar con IA" (lo que necesitan los dirigentes).

2. **El Votómetro como activo diferenciador.** Es el producto más visible de CIGOB y está subutilizado. Conectar el Votómetro con IA (Opción B del Bibliotecario) crearía algo que nadie tiene en Argentina: un asistente de análisis electoral conversacional basado en datos propios.

3. **Los conceptos narrativos originales.** "Federalismo de Precisión" no existe en la literatura académica ni en el debate público argentino — es un concepto que CIGOB puede apropiar. "Estado forense vs. Estado con sensores" es una metáfora potente que captura la diferencia entre un gobierno que reacciona a posteriori y uno que anticipa. Pero estos conceptos necesitan respaldo: si CIGOB no publica un paper fundacional de Federalismo de Precisión con datos de clusters provinciales antes de fin de Q2 2026, alguien más va a usar la idea.

### Riesgos de llegar tarde

El análisis identifica cinco riesgos concretos:

1. **CIPPEC ya plantó bandera.** Con su guía publicada en mayo 2025, CIPPEC se posicionó como el think tank de referencia en IA para el sector público argentino. Cada mes que CIGOB no produce contenido verificable, esa posición se consolida.

2. **CIIAR ya nuclea a los municipios innovadores.** Si CIGOB quiere ser "el socio estratégico de los gobiernos para IA", debería estar articulando con esta red, no ignorándola. Contactar a CIIAR para explorar alianza o membresía debería ser una acción inmediata.

3. **El tema puede comoditizarse.** Toda la propuesta pivotea sobre "IA en la gestión pública". Si bien es relevante hoy, anclar toda la identidad institucional a una tecnología es riesgoso. En 2-3 años el tema puede volverse commodity. CIGOB necesita que su valor esté en el *método* (análisis territorial, gestión por resultados, escucha ciudadana), no en la *herramienta*.

4. **La credibilidad se sostiene en reputación, no en evidencia.** El documento de posición de Babino no presenta ningún caso concreto de trabajo de CIGOB con IA en territorio, ningún dato empírico sobre la "brecha subnacional", ninguna metodología para la "anticipación". Sin el Bibliotecario u otra implementación concreta, esta debilidad persiste.

5. **El ecosistema regulatorio avanza.** Con múltiples proyectos de ley en el Congreso y la posible creación del COFEIA, el marco normativo puede cristalizar antes de que CIGOB tenga algo que ofrecer al debate.

---

## Fase 1 — El Bibliotecario: análisis completo

### ¿Qué es y qué problema resuelve?

El Bibliotecario es un sistema de IA que permite consultar, buscar y explorar el corpus de documentos, investigaciones y análisis de CIGOB de forma conversacional. El usuario pregunta en lenguaje natural; el sistema responde con información de la base de conocimiento de la fundación, citando fuentes.

**Analogía:** Google Search para el archivo de CIGOB, pero conversacional y con síntesis.

**Problema que resuelve:** CIGOB ha acumulado un corpus de documentos, análisis, informes y contenido que hoy está disperso y es difícil de consultar. Un miembro del equipo que necesita saber "¿cuál es la posición de CIGOB sobre gobernanza de la incertidumbre?" tiene que buscar manualmente en archivos. Un potencial cliente o aliado no tiene forma de acceder a ese conocimiento de manera ágil. El Bibliotecario convierte un archivo pasivo en un activo vivo y consultable.

**Valor estratégico adicional:** El Bibliotecario es simultáneamente un producto interno (mejora la productividad del equipo), un producto externo (demuestra capacidad ante clientes y aliados), un caso de estudio (genera contenido publicable), y una credencial (prueba que CIGOB practica lo que predica).

### Opción A — RAG sobre documentos propios (recomendada)

**Qué es:** Un sistema de Retrieval-Augmented Generation (Generación Aumentada por Recuperación). Los documentos de CIGOB se procesan, se almacenan como vectores en una base de datos, y cuando alguien hace una pregunta, el sistema recupera los fragmentos relevantes y los utiliza para que la IA responda con fundamento en el corpus propio.

**Cómo funciona en la práctica:**
1. Se suben todos los documentos de CIGOB (los .docx, PDFs, artículos, informes, contenido del sitio web).
2. El sistema los "lee" y los indexa, convirtiéndolos en representaciones numéricas (embeddings) que permiten buscar por significado, no solo por palabras clave.
3. El usuario pregunta: "¿Cuál es la posición de CIGOB sobre la IA en la gestión pública?"
4. El sistema busca los fragmentos más relevantes del corpus, los pasa al modelo de lenguaje (Claude, GPT-4), y devuelve una respuesta fundamentada con citas textuales y referencias al documento de origen.

**Herramientas disponibles hoy, sin escribir código:**

| Herramienta | Costo | Capacidad | Ideal para |
|-------------|-------|-----------|------------|
| **NotebookLM** (Google) | Gratuito | Hasta 50 documentos, chat conversacional, citas automáticas | Empezar esta semana. Prototipo inmediato |
| **Perplexity Spaces** (premium) | ~US$ 20/mes | Similar a NotebookLM, mejor interfaz | Alternativa si NotebookLM no satisface |
| **Claude Projects** (Anthropic) | US$ 20/mes (plan Pro) | Muy bueno para iteración de análisis, documentos de trabajo | Uso interno del equipo |

**Para una versión más robusta, con algo de desarrollo:**

| Herramienta | Costo | Desarrollo necesario | Ventaja |
|-------------|-------|---------------------|---------|
| **Flowise** (no-code, open source) | US$ 10-20/mes (VPS básico) | Bajo (1-2 días) | Construye el pipeline RAG visualmente, sin código. Se puede alojar en servidor propio |
| **LangChain + Chroma/Pinecone** (open source) | US$ 50-200/mes (según uso de API) | Medio (1-2 semanas) | Mayor control, escalable, puede desplegarse en web con URL propia |

**Pros:**
- Responde con base en los propios textos de CIGOB, no inventa datos.
- Cita fuentes específicas (qué documento, qué párrafo).
- Es el caso de uso más confiable para una organización de conocimiento.
- Permite que cualquier miembro del equipo acceda al corpus sin entrenamiento previo.
- Escalable: a medida que CIGOB produce más contenido, el Bibliotecario se enriquece.

**Contras:**
- Requiere mantener actualizada la base documental (alguien tiene que subir los documentos nuevos).
- La calidad de las respuestas depende de la calidad y cobertura del corpus.
- Las herramientas sin código (NotebookLM, Claude Projects) tienen limitaciones de personalización y no permiten URL pública propia.

**Costo estimado:** Desde $0 (NotebookLM) hasta US$ 200/mes (solución custom con API).

**Tiempo de implementación:** Prototipo funcional en NotebookLM: 1-2 horas. Versión robusta con Flowise: 1-2 días. Solución custom deployable en web: 1-2 semanas.

### Opción B — Asistente conectado al Votómetro

**Qué es:** Un chatbot especializado en análisis electoral que usa los datos del Votómetro para responder preguntas conversacionales. Ejemplos: "¿Qué pasó con LLA en septiembre 2024?", "¿Qué consultoras tienen mejor track record?", "Comparame las últimas tres elecciones en Córdoba".

**Cómo funciona:** Se conecta la API de Claude o GPT-4 con los datos del Votómetro en formato estructurado (JSON, CSV). El modelo de lenguaje interpreta la pregunta, consulta los datos y genera una respuesta con análisis y visualizaciones.

**Requisitos técnicos:**
- Los datos del Votómetro deben estar separados del HTML (actualmente están embebidos en la interfaz web). Este es el prerrequisito técnico más importante.
- Se necesita una API o un export estructurado de los datos.
- Requiere desarrollo: conexión de la API del LLM con la base de datos del Votómetro.

**Cuándo tiene sentido:** Cuando los datos del Votómetro estén limpios y accesibles. Esta es la Opción B en secuencia temporal, no el primer paso.

**Pros:**
- Muy diferencial: nadie tiene esto en Argentina. Un asistente de análisis electoral conversacional basado en datos propios.
- Vincula el activo más visible de CIGOB (Votómetro) con IA, multiplicando su valor.
- Conecta las tres unidades: CECIG valida los datos, Comunicación lo difunde, Soluciones lo usa como herramienta de diagnóstico electoral para clientes.

**Contras:**
- Requiere que el Votómetro primero tenga los datos separados del HTML.
- Necesita desarrollo técnico (no es no-code).
- Los datos electorales son sensibles y los errores tienen alto costo reputacional.

**Costo estimado:** US$ 50-200/mes (API) + costo de desarrollo inicial.

**Tiempo de implementación:** 2-4 semanas después de que los datos estén estructurados.

### Opción C — Asistente interno para el equipo

**Qué es:** Un setup de IA interno para el equipo de CIGOB orientado a productividad: redacción de documentos, síntesis de encuestas, análisis de textos, generación de borradores, preparación de informes, transcripción de entrevistas.

**Herramientas:** Claude Team o ChatGPT Team. Sin código, contrato mensual, cada miembro del equipo tiene su cuenta.

**Descripción del valor inmediato:**
- Un analista del CECIG puede sintetizar un informe de 50 páginas en 5 minutos.
- El Centro de Comunicación puede generar borradores de posts, newsletters y guiones de podcast.
- El Centro de Soluciones puede preparar propuestas comerciales y diagnósticos más rápido.
- Todo el equipo aprende a usar IA con sus propios materiales, lo que genera conocimiento tácito para las fases siguientes.

**Pros:**
- Valor inmediato, sin desarrollo.
- Sube la productividad del equipo en días, no semanas.
- Bajo costo (US$ 20-30/mes por usuario).
- El equipo desarrolla competencias de IA que luego aplica en las fases siguientes.
- No requiere decisiones arquitectónicas: se contrata y se usa.

**Limitaciones:**
- No es un producto visible hacia afuera. No construye posicionamiento externo.
- No genera un caso de estudio publicable (es uso genérico de herramientas comerciales).
- No resuelve el problema de acceso al corpus documental de CIGOB (cada consulta requiere subir los documentos manualmente).

**Costo estimado:** US$ 20-30/mes por usuario.

**Tiempo de implementación:** Mismo día.

### Comparación de opciones

| Criterio | Opción A (RAG) | Opción B (Votómetro) | Opción C (Interno) |
|----------|---------------|---------------------|-------------------|
| **Valor inmediato** | Alto (prototipo en horas) | Bajo (requiere preparación de datos) | Muy alto (mismo día) |
| **Visibilidad externa** | Alta (producto demostrable) | Muy alta (diferencial único) | Nula |
| **Costo mensual** | $0-200 | $50-200 + desarrollo | $20-30/usuario |
| **Desarrollo necesario** | Bajo a medio | Medio a alto | Ninguno |
| **Riesgo técnico** | Bajo | Medio (datos electorales sensibles) | Nulo |
| **Posicionamiento de marca** | Alto (caso de estudio) | Muy alto (nadie lo tiene) | Bajo |
| **Escalabilidad** | Alta (crece con el corpus) | Alta (crece con los datos) | Baja (uso individual) |
| **Alimenta al Centro de Soluciones** | Sí (metodología transferible) | Sí (herramienta vendible) | Indirectamente |
| **Tiempo al primer resultado** | 1-2 horas (NotebookLM) | 2-4 semanas mínimo | Inmediato |
| **Requiere decisión arquitectónica** | Sí (interno vs. externo) | Sí (estructura de datos) | No |

### Recomendación y secuencia

La recomendación es ejecutar las tres opciones en secuencia, no elegir una sola:

**Semana 1-2: Opción C (interno) + Prototipo de Opción A con NotebookLM**

- Contratar Claude Team o ChatGPT Team para el equipo. Costo: ~US$ 80-120/mes (3-4 usuarios).
- En paralelo, subir los documentos disponibles a NotebookLM (gratis) y crear un primer prototipo del Bibliotecario.
- Resultado: el equipo empieza a usar IA el día 1, y hay un prototipo conversacional del corpus documental para evaluar.
- Decisión necesaria: nada más que la aprobación del gasto (~US$ 100/mes).

**Mes 1-2: Opción A con versión robusta (Flowise o LangChain)**

- Migrar el prototipo de NotebookLM a una solución más controlada.
- Si se decide que el Bibliotecario será externo: deploy en web con URL propia (requiere Flowise o LangChain).
- Si se decide que será solo interno: Claude Projects puede ser suficiente por más tiempo.
- Incorporar más documentos al corpus, incluyendo contenido del Votómetro, transcripciones, informes de gestión.
- Documentar el proceso para el caso de estudio (alimenta al Centro de Comunicación y al CECIG).
- Decisión necesaria: interno vs. externo (ver sección "La pregunta política").

**Mes 3+: Opción B (Votómetro + IA)**

- Solo cuando los datos del Votómetro estén separados del HTML y en formato estructurado.
- Conectar el asistente del Bibliotecario con los datos electorales.
- Crear una versión del Bibliotecario especializada en análisis electoral.
- Este es el producto de mayor diferenciación y el que más posiciona a CIGOB en el mapa.

---

## Fase 2 — Más allá del Bibliotecario

Una vez que el Bibliotecario esté funcionando y el equipo haya desarrollado competencias básicas en IA, CIGOB puede avanzar hacia aplicaciones más ambiciosas. Estas conectan directamente con la oferta del Centro de Soluciones y con los conceptos estratégicos de la Propuesta 2026-2027:

**Escucha social con IA.** Monitoreo automatizado de redes sociales, medios y foros para detectar el "humor social" en tiempo real. Esto es lo que la Propuesta Estratégica llama "escucha activa" pero sin especificar cómo. Con IA, se pueden analizar miles de publicaciones diarias, detectar tendencias emergentes, identificar temas de conversación en distritos específicos. Conecta con "Estado con sensores" vs. "Estado forense": en lugar de reaccionar a la crisis, el gobierno la detecta en formación. Herramientas: modelos de análisis de sentimiento (disponibles via API), dashboards en tiempo real. Diferenciación frente a Poliarquía y Giacobbe: la escucha social por IA es continua y de bajo costo; las encuestas son periódicas y caras.

**Análisis automatizado de encuestas y datos.** El equipo de CIGOB puede usar IA para procesar encuestas de terceros, datos del INDEC, informes provinciales y producir síntesis analíticas en una fracción del tiempo. Esto alimenta al CECIG con capacidad de producción intelectual que hoy requeriría un equipo mucho mayor. Un analista con acceso a Claude o GPT-4 puede sintetizar un informe de 100 páginas del BID en 15 minutos con análisis crítico incluido.

**Planes de gobierno asistidos por IA.** El Centro de Soluciones puede ofrecer a gobiernos subnacionales un servicio donde, a partir de datos del distrito (Votómetro, encuestas, indicadores socioeconómicos), la IA genera un borrador de plan de gobierno que el equipo humano de CIGOB refina y personaliza. Esto convierte un servicio artesanal y caro en uno escalable. Conecta directamente con "Federalismo de Precisión": los clusters provinciales alimentan al modelo, y el resultado es un plan diferenciado por territorio.

**Tablero de Control inteligente.** El "producto estrella" de la Propuesta Estratégica — el Tablero de Control para monitoreo de compromisos de gobierno — puede incorporar IA predictiva: alertas tempranas cuando un indicador se desvía, sugerencias de acción correctiva, comparación automática con distritos similares. Esto convierte un tablero descriptivo en una herramienta de anticipación.

**Simulación de escenarios.** Conectando con la idea de Innerarity de "preparar a la democracia para gestionar lo que no sabemos", CIGOB podría desarrollar herramientas de simulación que permitan a un gobernante explorar "¿qué pasa si...?" — qué pasa si sube el desempleo 3 puntos, qué pasa si hay una emergencia climática, qué pasa si se recorta una transferencia nacional. No es predicción; es preparación institucional para la incertidumbre.

---

## Presupuesto y recursos

### Inversión inmediata (Semana 1-2)

| Concepto | Costo mensual | Requiere desarrollo | Tiempo de implementación |
|----------|--------------|--------------------|-----------------------|
| Claude Team o ChatGPT Team (3-4 usuarios) | US$ 80-120 | No | Mismo día |
| NotebookLM (prototipo Bibliotecario) | Gratuito | No | 1-2 horas |
| **Total Semana 1** | **US$ 80-120/mes** | **No** | **1 día** |

### Inversión Fase 1 completa (Mes 1-2)

| Concepto | Costo mensual | Requiere desarrollo | Tiempo de implementación |
|----------|--------------|--------------------|-----------------------|
| Herramientas de equipo (Claude/ChatGPT Team) | US$ 80-120 | No | Ya activo |
| Claude Projects (para Bibliotecario interno) | US$ 20 | No | Inmediato |
| Flowise + VPS básico (si se decide deploy externo) | US$ 10-20 | Bajo (1-2 días) | 1-2 días |
| Solución custom RAG (si se necesita más control) | US$ 50-200 (según uso de API) | Sí (1-2 semanas) | 1-2 semanas |
| **Total Fase 1 (rango)** | **US$ 110-360/mes** | **Bajo a medio** | **1-2 semanas** |

### Inversión Fase 1 + Votómetro (Mes 3+)

| Concepto | Costo mensual | Requiere desarrollo | Tiempo de implementación |
|----------|--------------|--------------------|-----------------------|
| Todo lo anterior | US$ 110-360 | Ya implementado | - |
| API para Votómetro + IA | US$ 50-200 adicionales | Sí (2-4 semanas) | 2-4 semanas |
| **Total con Votómetro** | **US$ 160-560/mes** | **Medio** | **Acumulado: ~2-3 meses** |

### Recursos humanos necesarios

El análisis de la Propuesta Estratégica identifica un riesgo de sobreextensión: tres centros con múltiples productos requieren al menos 8-10 personas dedicadas. Para la implementación de IA específicamente:

- **Mínimo:** Una persona del equipo dedicada parcialmente a gestionar el Bibliotecario (subir documentos, evaluar calidad de respuestas, iterar). No requiere perfil técnico.
- **Recomendable:** Un perfil técnico junior o consultor externo part-time para la implementación de Flowise/LangChain si se decide el deploy externo.
- **Para Fase 2:** Un perfil de datos/IA dedicado que pueda conectar el Votómetro, implementar escucha social y desarrollar los productos del Centro de Soluciones.

### Relación costo-beneficio

Para poner en contexto: el costo total de la Fase 1 completa (US$ 110-360/mes) es comparable a una suscripción mensual de software estándar, o a menos de un día de consultoría de cualquier firma mediana. Si CIGOB consigue un solo contrato de consultoría subnacional en IA gracias al posicionamiento que genera el Bibliotecario, el retorno sobre la inversión es de órdenes de magnitud.

---

## Criterios de éxito del Bibliotecario (Fase 1)

### Checkpoints de funcionalidad (verificables en Mes 2)

- [ ] Cualquier miembro del equipo puede preguntarle al Bibliotecario sin entrenamiento previo.
- [ ] Las respuestas citan la fuente: qué documento y qué sección.
- [ ] El sistema no inventa datos que no estén en los documentos de CIGOB (cero alucinaciones verificadas en las primeras 50 consultas de prueba).
- [ ] Hay un proceso definido para agregar documentos nuevos (quién lo hace, con qué frecuencia, qué formato).
- [ ] El corpus incluye al menos los documentos fundacionales, el paper de posición sobre IA, la propuesta estratégica, y los informes del Votómetro.

### Checkpoints de adopción interna (verificables en Mes 2)

- [ ] Al menos 3 miembros del equipo lo usan regularmente (mínimo 2 veces por semana).
- [ ] Se ha identificado al menos un caso de uso concreto donde el Bibliotecario ahorra tiempo significativo (ej: preparar una presentación, responder una consulta de un potencial cliente).
- [ ] El equipo puede articular qué funciona y qué no — hay feedback documentado.

### Checkpoints de posicionamiento (verificables en Mes 3)

- [ ] Se ha publicado al menos una pieza de contenido (post, artículo, sección de newsletter) describiendo la experiencia de implementación.
- [ ] Se ha presentado el Bibliotecario (aunque sea en versión interna) a al menos un interlocutor externo (aliado, potencial cliente, medio).
- [ ] Hay una decisión tomada sobre si y cuándo se lanza la versión externa.

### Checkpoints de escalabilidad (verificables en Mes 4-6)

- [ ] El Bibliotecario está conectado o en proceso de conexión con los datos del Votómetro (Opción B).
- [ ] Se ha evaluado la viabilidad de ofrecer el Bibliotecario (o una versión adaptada) como producto del Centro de Soluciones para gobiernos.
- [ ] El caso de estudio está publicado o en borrador avanzado.

---

## La pregunta política detrás de la tecnológica

Antes de elegir la herramienta, hay que definir una cuestión que es política, no técnica: **¿el Bibliotecario es para adentro (equipo CIGOB) o para afuera (clientes, público)?**

Esta decisión determina la arquitectura, el costo, el riesgo y la velocidad de todo lo que sigue.

### Opción 1: Solo interno (primero)

- **Qué implica:** El Bibliotecario es una herramienta del equipo. No tiene URL pública. Se usa NotebookLM o Claude Projects.
- **Ventajas:** Velocidad máxima (funcional en horas), costo mínimo ($0-20/mes), riesgo cero (si falla, nadie lo ve), permite iterar sin presión.
- **Desventajas:** No construye posicionamiento externo. No genera caso de estudio visible. No demuestra capacidad ante clientes.
- **Cuándo tiene sentido:** Si el equipo no tiene experiencia previa con IA y necesita un período de aprendizaje. Si la prioridad es productividad interna antes que comunicación.

### Opción 2: Externo desde el día 1

- **Qué implica:** El Bibliotecario se lanza con URL propia, accesible para clientes o público.
- **Ventajas:** Posicionamiento inmediato. Genera tráfico, prensa, conversación. Demuestra que CIGOB practica lo que predica.
- **Desventajas:** Requiere desarrollo (Flowise o similar), más costo, más tiempo, y más riesgo (si las respuestas son malas, el daño reputacional es real). Las herramientas no-code gratuitas no permiten URL pública personalizada.
- **Cuándo tiene sentido:** Si hay urgencia competitiva y CIGOB quiere plantar bandera antes que otro actor lo haga.

### Opción 3: Interno primero, externo cuando funcione (recomendada)

- **Qué implica:** Se arranca con versión interna (Semana 1), se itera, se documenta, y se lanza la versión externa cuando la calidad sea verificada (Mes 2-3).
- **Ventajas:** Combina velocidad con prudencia. El equipo aprende, el corpus se enriquece, y cuando se lanza al público ya funciona bien.
- **Desventajas:** El posicionamiento externo se demora 2-3 meses. Requiere disciplina para no quedarse solo en lo interno.
- **Cuándo tiene sentido:** En la mayoría de los casos. Es el camino más seguro y el que genera mejor relación entre riesgo y recompensa.

### Consecuencias de cada opción para la reunión

La elección no es solo técnica. Tiene implicancias organizacionales:

- **Si es interno:** El responsable es el equipo operativo. No requiere aprobación de diseño ni comunicación.
- **Si es externo:** Requiere decisiones de marca (¿cómo se llama? ¿dónde se aloja? ¿cómo se presenta?), comunicación (¿se anuncia o se lanza en silencio?), y gestión de expectativas (¿qué pasa si la calidad inicial no es buena?).
- **Si es ambos en secuencia:** Requiere un compromiso explícito con fechas. "Empezamos interno y vemos" es la fórmula para que nunca se lance al público.

**Recomendación para la reunión:** Aprobar la Opción 3 (interno primero, externo después) con una fecha límite explícita para la decisión de lanzamiento externo: no más de 60 días desde la activación del prototipo interno. Asignar un responsable que reporte quincenalmente sobre el avance.

---

## Decisiones que requiere la reunión

La reunión del 10/03/2026 debe resolver las siguientes cuestiones para que el rediseño tecnológico avance:

### Decisión 1: ¿Se aprueba el gasto inicial?
- Monto: ~US$ 100-120/mes (Claude Team o ChatGPT Team para el equipo + NotebookLM gratuito para el prototipo).
- Esto cubre la Semana 1-2 completa y no requiere desarrollo.
- **Acción requerida:** Aprobación del gasto y asignación presupuestaria.

### Decisión 2: ¿Quién es el responsable de la implementación?
- Se necesita una persona del equipo que gestione el Bibliotecario: suba documentos, evalúe respuestas, documente el proceso, y reporte avance.
- No requiere perfil técnico. Requiere dedicación parcial (~5 horas/semana).
- **Acción requerida:** Designar al responsable con nombre y apellido.

### Decisión 3: ¿El Bibliotecario arranca interno, externo, o interno con fecha de lanzamiento externo?
- La recomendación es la Opción 3: interno primero, con compromiso de decidir sobre lanzamiento externo en un plazo de 60 días.
- **Acción requerida:** Elegir la opción y, si es la 3, fijar la fecha de revisión (no más allá de mayo 2026).

### Decisión 4: ¿Se contacta a CIIAR?
- CIGOB no aparece en la Coalición de Ciudades por la IA en Argentina. Contactar a CIIAR para explorar alianza o membresía es una acción de bajo costo y alto potencial.
- **Acción requerida:** Designar quién hace el contacto y con qué propuesta.

### Decisión 5: ¿Se publica el paper de Federalismo de Precisión en Q2 2026?
- El concepto no existe en la literatura y es apropiable. Pero si no se publica con datos y rigor, pierde valor. Un paper fundacional con clusters provinciales antes de junio 2026 plantaría bandera intelectual.
- **Acción requerida:** Confirmar si el CECIG tiene capacidad para producirlo en ese plazo y asignar recursos.

### Decisión 6: ¿Se narra el proceso en público?
- Documentar la transformación tecnológica de CIGOB como contenido institucional (blog, newsletter, redes) tiene alto valor de posicionamiento.
- **Acción requerida:** Definir si el Centro de Comunicación asume esta tarea y con qué formato (serie de posts, newsletter dedicada, sección del podcast).

---

*Documento producido integrando los análisis del paper de posición de Babino, la propuesta estratégica 2026-2027, y la propuesta de rediseño tecnológico. Fuentes de contexto competitivo actualizadas al 10/03/2026. Las referencias incluyen: CIPPEC (2025), CIIAR (2024-2026), ILIA (2025), Innerarity (2025), OCDE (2025), DataGénero (2025).*
