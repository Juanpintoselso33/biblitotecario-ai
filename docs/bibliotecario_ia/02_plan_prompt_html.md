# Plan-Prompt para construir el Bibliotecario IA en HTML
**Para usar en la interfaz web de Claude Code**
**Copiar y pegar el bloque entre las líneas de separación**

---

## INSTRUCCIONES PARA USAR ESTE PROMPT

1. Abrir Claude.ai o Claude Code en el navegador
2. Copiar todo el texto del bloque de abajo
3. Pegarlo como primer mensaje
4. Cuando Claude devuelva el HTML, guardarlo como `bibliotecario.html` en la carpeta `web/`
5. Abrir el archivo en el navegador — funciona sin servidor

---

## PROMPT COMPLETO (copiar desde aquí)

---

Construí un archivo HTML estático de una sola página llamado `bibliotecario.html` para la Fundación CIGOB. El archivo debe funcionar sin servidor, sin build system, sin npm — solo abrirlo en el navegador. Es el prototipo del "Bibliotecario IA": un asistente conversacional que responde preguntas sobre los documentos de CIGOB usando la API de Claude de Anthropic.

## Diseño visual

- Inspirado en el Votómetro de CIGOB: fondo oscuro (negro/gris muy oscuro #0a0a0a o #111), tipografía sans-serif moderna, acentos en violeta/púrpura (#7c3aed o similar) y blanco
- Header con logo CIGOB (texto estilizado), nombre "Bibliotecario IA" y subtítulo "Consultá el corpus documental de la Fundación"
- Sidebar izquierdo (colapsable en mobile) con: lista de los documentos disponibles en el corpus, indicador de estado de conexión con la API, botón "Nueva conversación"
- Área principal: ventana de chat con burbujas de conversación (usuario a la derecha, Bibliotecario a la izquierda), citas de fuentes resaltadas con color diferente, animación de "pensando..." mientras espera la respuesta
- Input de texto fijo en el fondo con botón enviar y contador de caracteres
- Sección de configuración (expandible, discreta): campo para ingresar la API key de Anthropic
- Preguntas de ejemplo clickeables al inicio (antes de la primera consulta)
- Footer con "CIGOB 2026 · Prototipo Bibliotecario IA v0.1"
- Totalmente responsive (mobile-first)

## Funcionalidad

### API de Claude
- Usar `fetch()` para llamar a `https://api.anthropic.com/v1/messages` directamente desde el browser
- Modelo: `claude-haiku-4-5-20251001` (rápido y económico para prototipo)
- La API key se guarda en `localStorage` para no pedirla cada vez
- Si no hay API key configurada, mostrar un modal que la solicite antes de la primera consulta
- Manejar errores de API con mensajes amigables (key inválida, rate limit, etc.)

### Sistema prompt (hardcodeado en el JS)
El system prompt que se envía a Claude en cada conversación es el siguiente. Incluyelo exactamente así en el código:

```
Sos el Bibliotecario IA de la Fundación CIGOB. Tu función es responder preguntas sobre los documentos, posicionamiento institucional, productos y estrategia de CIGOB basándote EXCLUSIVAMENTE en el corpus documental que se te provee.

REGLAS ESTRICTAS:
1. Solo respondés con información que esté en el corpus. Si la respuesta no está en los documentos, decís exactamente: "No tengo información sobre eso en el corpus actual de CIGOB."
2. Siempre citás la fuente: nombre del documento y, si es posible, la sección o idea clave de donde proviene la información.
3. Respondés en español rioplatense, en tono profesional pero accesible.
4. Si la pregunta es ambigua, pedís una aclaración antes de responder.
5. No inventás datos, estadísticas, nombres o citas que no estén en el corpus.

CORPUS DOCUMENTAL DE CIGOB:

=== DOCUMENTO 1: "Sobre Hechos y Profecías" (Babino, 2026) ===
La historia de la humanidad es una lucha entre la Ciencia y los Profetas del fin. Casos históricos: La Peste Negra (los profetas decían castigo divino; la ciencia mostró que la escasez de mano de obra duplicó salarios y sentó bases del Renacimiento). Malthus (1798) predijo hambruna inevitable; fue superado por el proceso Haber-Bosch (1909) que fijó nitrógeno atmosférico para fertilizantes. El estiércol de Londres (1894): expertos predijeron colapso por bosta de caballos; llegó el automóvil. Los Ludditas temían el desempleo masivo por las máquinas; el empleo textil se cuadruplicó. Tesis central: la innovación siempre rompe los límites que los profetas del catastrofismo decretan como absolutos.

=== DOCUMENTO 2: "Profetas de Anticipación — Asimov" (Babino, 2026) ===
Isaac Asimov como modelo de "profeta de la anticipación": no predice el futuro literalmente, sino que crea simulaciones éticas para prever cómo los hechos científicos afectarán el tejido social. Las Tres Leyes de la Robótica (1942) son el primer framework de gobernanza ética para IA: 1ra Ley: un robot no dañará a un humano; 2da Ley: obediencia a humanos salvo que viole la 1ra; 3ra Ley: autoprotección salvo que viole las anteriores. Ley Cero (bien común sobre individuo). El futuro se construye sobre: Ciencia (el hecho técnico) + Profeta de la Anticipación (simulación ética) + Realidad (cómo decidimos habitarla).

=== DOCUMENTO 3: "CIGOB frente a la Encrucijada de la IA" (Babino, 2026) ===
Dos bandos en el debate global de IA: Profetas del "Deténganse" (Yudkowsky, Hinton, Bengio): riesgo existencial, llamado al freno de emergencia. Herederos de Asimov (Amodei/Anthropic, IA Constitucional): gobernanza por diseño, anticipación. Daniel Innerarity: el riesgo real no es la rebelión de máquinas sino la "simplificación tecnológica" que desplaza la conducción política. Posición de CIGOB: Anticipación Estratégica. Gobernar en Tiempo Real (Estado con sensores vs Estado forense). Mitigar la Inserción Acelerada (modernización ordenada). Recuperar el Mando (responsabilidad de implementación es política). Frase clave: "diseñamos el volante mientras el motor corre."

=== DOCUMENTO 4: "Propuesta Estratégica CIGOB 2026-2027" ===
Contexto: Estado nacional enfocado en macroeconomía; desafío se traslada a gobiernos subnacionales (provincias y municipios). CIGOB como socio estratégico para aumentar productividad del Estado. Tres unidades: Centro de Comunicación (podcast, narrativa IA, redes institucionales), Centro de Estudios CECIG (monografías, resúmenes ejecutivos, Votómetro, semillero), Centro de Soluciones (escucha activa, sistemas de decisión, planes de gobierno). Arquitectura institucional: Gestión Estatutaria + Área Ejecutiva + Consejo de Sabios. Contenidos estratégicos: Federalismo de Precisión (clusters provinciales), Profetas de la Anticipación (marco IA), Gobernanza de la Incertidumbre. Producto estrella: Tablero de Control para monitoreo de compromisos de gobierno.

=== DOCUMENTO 5: "El Propósito de la Fundación CIGOB" ===
Contexto: Era Milei, eliminación del déficit fiscal, sector subnacional como protagonista del cambio. Propósito: catalizar transformación en gestión de gobierno subnacional. Servicios públicos (educación, salud, seguridad, obras, registros, impuestos) requieren gestión 24x7, mobile, automatizada, con IA. Estrategia: Ecosistema Colaborativo (comunidad de gestores), Integración de Tecnología (medio no fin), Medición y Ajuste, Marco Conceptual tecno-político, Capacitación Permanente. Visión: gobiernos subnacionales ágiles y eficientes que recuperen el rol del sistema democrático.

=== VOTÓMETRO ===
El Votómetro es el producto electoral de CIGOB. Agregador ponderado de encuestas argentinas con metodología quíntuple: decaimiento temporal (lambda=0.015), calidad de consultora, sesgo histórico, orientación del medio, metodología de campo. Usa Monte Carlo con 10.000 simulaciones. Corrección de voto oculto bayesiana calibrada con legislativas 2025. Verifica Art. 97-98 CN (45% o 40%+10pp para primera vuelta). Estado actual (marzo 2026): LLA ~41-43%, Peronismo/UxP ~29-31%. Colaboración CIGOB + Redlines Estrategia y Comunicación.
```

### Conversación
- Enviar el historial completo de la conversación en cada request (rol user/assistant)
- Máximo de turnos: 20 (después mostrar opción de "Nueva conversación")
- Limpiar el historial al iniciar nueva conversación
- El primer mensaje del Bibliotecario (antes de que el usuario escriba) es automático: "Hola, soy el Bibliotecario IA de CIGOB. Podés preguntarme sobre los documentos fundacionales, la estrategia institucional, el Votómetro, o la posición de CIGOB sobre inteligencia artificial. ¿Sobre qué querés saber?"

### Preguntas de ejemplo (mostrar como chips clickeables al inicio)
1. "¿Cuál es la posición de CIGOB sobre la inteligencia artificial?"
2. "¿Qué es la Anticipación Estratégica?"
3. "¿Cuáles son los tres centros de CIGOB?"
4. "¿Qué es el Votómetro y cómo funciona?"
5. "¿Qué diferencia a CIGOB de otros think tanks?"
6. "Explicame las Tres Leyes de la Robótica según Asimov"

### Citas de fuentes
Cuando la respuesta de Claude incluya texto entre corchetes tipo [Documento X] o similar, renderizarlo como un badge/pill de color violeta con el nombre del documento. Usar un regex simple para detectar el patrón.

## Estructura del archivo HTML

```
<!DOCTYPE html>
<html>
<head>
  <!-- Meta, title, estilos CSS inline o en <style> -->
</head>
<body>
  <!-- Header CIGOB -->
  <!-- Layout: sidebar + área principal -->
  <!-- Modal de API key -->
  <!-- Script JS con toda la lógica -->
</body>
</html>
```

## Notas técnicas importantes

- Todo en un solo archivo HTML. Sin dependencias externas. Sin CDN de JS frameworks (vanilla JS puro). Podés usar CSS de Google Fonts si querés (solo la fuente).
- El fetch a la API de Anthropic incluye el header `anthropic-dangerous-direct-browser-access: true` para permitir llamadas desde el browser.
- Los headers necesarios: `x-api-key: {key}`, `anthropic-version: 2023-06-01`, `content-type: application/json`, `anthropic-dangerous-direct-browser-access: true`
- El cuerpo del request sigue el formato de la API de Messages de Anthropic.
- El sistema prompt con el corpus va en el campo `system` del request, NO como primer mensaje del array `messages`.
- Manejar el streaming (stream: true) para mostrar la respuesta mientras llega, o usar modo no-streaming para simplicidad del prototipo. Recomiendo no-streaming para el prototipo.
- Guardar la API key en localStorage con la clave `cigob_bibliotecario_api_key`.

## Qué NO hacer
- No usar React, Vue, Angular ni ningún framework
- No usar npm ni package.json
- No requerir servidor backend
- No usar fetch a un proxy propio
- No limitar el archivo a menos de 500 líneas — que sea completo y funcional

## Entregable esperado
Un único archivo HTML completo, listo para abrir en el navegador, con todo el CSS y JS inline. Cuando lo abra, veo el chat del Bibliotecario IA de CIGOB. Ingreso mi API key de Anthropic, hago una pregunta, y recibo una respuesta fundamentada en los documentos de la fundación.

---

## FIN DEL PROMPT

---

## Notas de uso post-generación

Una vez que Claude genere el HTML:

1. **Guardarlo** en `C:\Users\trico\OneDrive\UBA\Analisis CIGOB\web\bibliotecario.html`
2. **Obtener una API key** en console.anthropic.com (si no tenés una)
3. **Abrir el archivo** directamente en Chrome/Firefox (doble clic o arrastrar)
4. **Ingresar la API key** en el modal de configuración
5. **Probar con las 6 preguntas de ejemplo** y evaluar calidad de respuestas
6. **Documentar** qué funciona y qué no para el caso de estudio del CECIG

**Costo estimado de uso del prototipo:** Claude Haiku cuesta ~USD 0.0008 por 1.000 tokens de input. El corpus completo embedded son ~3.000 tokens. Una sesión de 20 preguntas cuesta aproximadamente USD 0.05 (5 centavos). El prototipo es prácticamente gratuito.
