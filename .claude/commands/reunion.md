Preparar material completo para una reunión de CIGOB.

El usuario proporcionará un temario. Para cada punto del temario:

1. Leer los documentos relevantes en `docs/` usando el agente `lector-docs` o el script Python de extracción de .docx
2. Revisar el Votómetro en `web/` si el punto lo requiere
3. Generar un archivo `output/0N_nombre_punto.md` por cada punto
4. Generar `output/00_resumen_ejecutivo.md` al final con síntesis y decisiones pendientes

**Estructura de cada archivo:**
- Contexto (qué dicen los docs sobre este punto)
- Análisis (qué significa para CIGOB)
- Opciones o tensiones (qué hay que resolver)
- Recomendación concreta

**Al final del proceso:** informar qué archivos se generaron y cuáles son las 3-5 decisiones más importantes que la reunión debe resolver.

Temario del usuario: $ARGUMENTS
