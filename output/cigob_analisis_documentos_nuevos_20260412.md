# CIGOB — Análisis crítico de los documentos sobre el Votómetro
**Fecha:** 12 de abril 2026  
**Documentos analizados:**
- `260403 COMENTARIOS VOTOMETRO.docx`
- `260407 VOTOMETRO ESQUEMA.pptx`
**Perspectiva:** CIGOB como productor del modelo metodológico

---

## Síntesis

Los dos documentos son valiosos como feedback editorial pero incompletos como insumo estratégico. Responden bien a la pregunta "¿qué muestro y cómo?" pero no responden ninguna de las preguntas que CIGOB necesita responder para que el Votómetro sea un producto institucional sostenible. Lo que falta no es técnico: es estratégico.

---

## 1. No hay definición de audiencia

Los comentarios asumen implícitamente que el Votómetro tiene una audiencia única (el lector general de medios), y desde ahí proponen simplificar. Pero el Votómetro puede servir a tres audiencias muy distintas:

| Audiencia | Qué necesita | Qué le sobra |
|---|---|---|
| Medios / periodistas | Número simple, actualizado, citeable | Metodología, Di Tella, comparativas |
| Operadores políticos | Escenarios, intervalos, probabilidad de ballotage | Nada — quieren todo |
| Posicionamiento institucional de CIGOB | Rigor visible, diferenciación metodológica | Exceso de simplicidad |

**Lo que falta en los documentos:** una decisión explícita sobre cuál es la audiencia primaria. Simplificar todo (sacar Di Tella, sacar comparativas, sacar encuestas individuales) es la respuesta correcta si el target es medios. Es la respuesta incorrecta si el Votómetro es también la vidriera metodológica de CIGOB.

Mientras esta pregunta no esté resuelta, cada decisión de diseño queda en el aire.

---

## 2. No hay propuesta de valor diferencial

Los comentarios proponen acercar el Votómetro a lo que hacen otros agregadores de encuestas (promedio ponderado, gráfico de tendencia, ballotage condicional). El problema: si el Votómetro se simplifica hasta ese punto, ¿qué lo diferencia de Poliarquía, CB Global Data o cualquier medio que publique su propio promedio?

**El diferenciador real del Votómetro es lo que los documentos proponen sacar o poner "a conversar":**
- El prior de fundamentals (ICC Di Tella, EMAE, aprobación) — ningún agregador argentino lo hace
- El sigma tiempo-variable — ningún agregador local calibra su incertidumbre con la distancia electoral
- El blend dinámico encuestas/fundamentals — es la metodología más sofisticada del mercado local

Ninguno de los dos documentos menciona esto como un activo a comunicar. La pregunta que falta es: **¿el Votómetro comunica que tiene un motor metodológico diferente, o se esconde detrás de una interfaz simple?**

CIGOB debería tener una posición explícita sobre esto, porque de ella depende qué tan visible es la caja negra del modelo.

---

## 3. No hay criterio de credibilidad y transparencia

Los comentarios proponen sacar las encuestas individuales, sacar la comparativa histórica, mover el Di Tella. Cada una de estas decisiones reduce la transparencia del modelo. 

Hay una tensión que los documentos no señalan: **a mayor simplificación visual, menor auditabilidad pública del modelo**. Si alguien quiere saber por qué el Votómetro dice 41% y no 38%, no hay forma de verificarlo si las fuentes están ocultas.

Para CIGOB, cuyo posicionamiento se basa en "rigor intelectual como marca", esto no es neutral. El documento de comentarios no tiene ninguna reflexión sobre este trade-off.

**Lo que falta:** un criterio explícito sobre qué nivel de transparencia metodológica quiere mantener el Votómetro en su versión pública. Opciones:
- Transparencia total (todo visible, con notas metodológicas)
- Transparencia selectiva (motor visible en sección técnica, UI simplificada para el público)
- Caja negra con marca (solo el número final, con "metodología en cigob.org")

---

## 4. No hay respuesta a quién actualiza y con qué recursos

Los comentarios identifican correctamente que hay datos hardcodeados (fundamentals desactualizados, encuestas manuales, ballotage fijo). Pero no proponen ninguna solución de sostenibilidad.

El Votómetro tal como está requiere actualizaciones manuales del HTML cada vez que:
- Sale una encuesta nueva (semanal/mensual)
- El INDEC publica el EMAE (mensual, con 2 meses de rezago)
- Di Tella publica el ICC (mensual)
- Cambia la aprobación presidencial

**Lo que falta:** una posición de CIGOB sobre si el Votómetro es un producto con dedicación editorial regular o un producto de publicación esporádica. No es un detalle operativo — define si el producto puede cumplir la promesa implícita de ser un "termómetro" actualizado.

---

## 5. No hay reflexión sobre el Votómetro dentro de la estrategia CIGOB

La Propuesta Estratégica 2026-2027 lista el Votómetro como un producto del CECIG, junto a monografías y resúmenes ejecutivos. Los dos documentos nuevos tratan el Votómetro como un producto independiente, sin ninguna referencia a esa estrategia.

Preguntas que CIGOB debería responder y que los documentos no tocan:

- ¿El Votómetro es el producto que posiciona al CECIG en medios? Si es así, la simplificación tiene sentido.
- ¿El Votómetro es la demostración de capacidades metodológicas de CIGOB para gobernantes? Si es así, la simplificación es contraproducente.
- ¿El Votómetro es un producto de colaboración con Redlines o es un producto propio de CIGOB con soporte de comunicación de Redlines? La respuesta define quién toma las decisiones editoriales.

---

## 6. La pregunta de gobernadores no está resuelta conceptualmente

El comentario "no la usaría con una sola encuesta, a conversar cuándo usarla" es correcto metodológicamente. Pero la pregunta de fondo es más importante: **¿el Votómetro debería tener datos subnacionales?**

CIGOB trabaja con provincias y municipios. La "brecha subnacional" es uno de sus conceptos ancla. Si el Votómetro incorpora proyecciones distritales, se convierte en una herramienta directamente conectada con la audiencia primaria de CIGOB (gobernantes subnacionales). Si solo mide la elección nacional, es un producto para medios nacionales.

Los documentos nuevos tratan esto como una decisión técnica (cuántas encuestas hay). Es una decisión estratégica.

---

## 7. No hay criterio para comunicar incertidumbre

El modelo tiene intervalos de confianza explícitos (±10.7pp al 90% con 560 días de distancia). Los documentos no mencionan en ningún momento cómo comunicar esa incertidumbre al público. 

Opciones que los documentos deberían evaluar y no evalúan:
- Mostrar solo el número central (simple pero engañoso)
- Mostrar rango ("entre 35% y 47%")
- Mostrar probabilidad ("LLA gana en primera vuelta en 6 de cada 10 simulaciones")
- No mostrar incertidumbre y agregar una nota de advertencia

La decisión de mostrar el ballotage como "condicional" toca este tema sin resolverlo.

---

## 8. Lo que los documentos hacen bien (y vale reconocer)

- Identifican correctamente que la comparativa 2023/2025/2027 no es legible para el público general
- La propuesta de ballotage condicional es metodológicamente más honesta que el formato actual
- Señalan el problema de nombres de candidatos vs. espacios (esto tiene implicancias en el modelo: la corrección +4pp LLA es sobre encuestas "tipo candidato", no sobre nombres)
- La pregunta sobre el Di Tella ("conversar para entender qué expresa") es legítima: si quien comunica el producto no entiende qué es el ICC, el público tampoco lo va a entender

---

## Síntesis: lo que CIGOB necesita definir antes de implementar el feedback

| Pregunta | Por qué es urgente | Opciones |
|---|---|---|
| ¿Cuál es la audiencia primaria? | Define qué simplificar y qué mantener | Medios / Operadores / Vidriera CIGOB |
| ¿Qué diferencia al Votómetro? | Define qué mostrar del motor metodológico | Transparencia total / selectiva / caja negra |
| ¿Quién actualiza y con qué frecuencia? | Define si el producto puede sostener su promesa | Dedicación regular / publicación esporádica |
| ¿El Votómetro es nacional o también subnacional? | Define el vínculo con la misión central de CIGOB | Solo nacional / con módulo provincial futuro |
| ¿Quién toma las decisiones editoriales? | Define la relación con Redlines | CIGOB decide, Redlines comunica / co-decisión |

---

*Análisis producido desde la perspectiva estratégica de CIGOB, en respuesta a los documentos de feedback de `docs/documentos_nuevos/`*
