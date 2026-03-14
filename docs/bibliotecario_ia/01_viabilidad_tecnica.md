# Bibliotecario IA — Documento de Viabilidad Técnica
**Fundación CIGOB · Marzo 2026**

---

## 1. Qué es el Bibliotecario IA

El Bibliotecario IA es un sistema de consulta conversacional sobre el corpus documental de CIGOB. El usuario escribe una pregunta en lenguaje natural; el sistema responde con información fundamentada en los documentos de la fundación, citando la fuente exacta.

**Analogía operativa:** Google Search para el archivo de CIGOB, pero con síntesis y conversación.

**Doble rol:**
- **Interno:** herramienta de productividad para el equipo (preparar reuniones, responder consultas, sintetizar material)
- **Externo:** producto demostrable ante clientes (provincias, municipios, financiadores) que prueba que CIGOB practica lo que predica

---

## 2. Stack técnico — cuatro niveles de implementación

### Nivel 0 — Prototipo inmediato (sin costo, sin código)
**Herramienta:** Google NotebookLM

| Característica | Detalle |
|---|---|
| Costo | Gratuito |
| Documentos soportados | Hasta 50 fuentes (PDF, DOCX, texto) |
| Funcionalidad | Chat conversacional con citas automáticas al documento fuente |
| Tiempo de setup | 1-2 horas |
| Limitaciones | Sin URL pública, sin personalización de marca, sin API |
| Ideal para | Validar que el concepto funciona con los docs de CIGOB antes de invertir |

**Stack:** Solo navegador. No requiere cuenta de desarrollador.

---

### Nivel 1 — Producto interno robusto (bajo costo, sin código)
**Herramienta:** Claude Projects (Anthropic) o Perplexity Spaces

| Característica | Detalle |
|---|---|
| Costo | USD 20/mes (plan Pro de Claude o Perplexity) |
| Documentos soportados | Hasta 200.000 tokens de contexto (~150 páginas) |
| Funcionalidad | Chat con instrucciones personalizadas, memoria de conversación, citas |
| Tiempo de setup | Mismo día |
| Limitaciones | Sin URL pública propia, acceso limitado a usuarios con cuenta |
| Ideal para | Uso interno del equipo CIGOB durante la fase de aprendizaje |

**Stack:** Claude API (gestionada por Anthropic). Sin infraestructura propia.

---

### Nivel 2 — Producto externo deployable (costo medio, bajo código)
**Herramienta:** Flowise + modelo de embeddings + LLM API

| Componente | Tecnología | Rol |
|---|---|---|
| Interfaz de usuario | Flowise (no-code, drag & drop) | Pipeline RAG visual sin escribir código |
| Embeddings | OpenAI text-embedding-3-small o Nomic (gratis) | Convierte documentos en vectores buscables |
| Vector store | Chroma (local) o Pinecone (cloud) | Base de datos de vectores |
| LLM | Claude Haiku / GPT-4o-mini | Genera la respuesta en lenguaje natural |
| Hosting | VPS básico (DigitalOcean, Hetzner) | Servidor que corre Flowise |
| Dominio | bibliotecario.cigob.org (ejemplo) | URL pública propia |

**Costo mensual estimado:**

| Concepto | Costo USD/mes |
|---|---|
| VPS básico (2GB RAM) | 6-12 |
| LLM API (Claude Haiku, ~500 consultas/mes) | 5-15 |
| Vector DB (Pinecone free tier) | 0 |
| Dominio (prorrateado) | 1 |
| **Total Nivel 2** | **12-28 USD/mes** |

**Tiempo de implementación:** 2-5 días (perfil técnico junior o consultor externo).

---

### Nivel 3 — Producto enterprise escalable (costo alto, desarrollo completo)
**Stack:** LangChain / LlamaIndex + PostgreSQL + pgvector + Next.js + Claude API

| Componente | Tecnología | Rol |
|---|---|---|
| Framework RAG | LangChain o LlamaIndex (Python) | Orquesta el pipeline completo |
| Base de datos | PostgreSQL + extensión pgvector | Almacena documentos y vectores en una sola DB |
| Embeddings | OpenAI o Cohere Embed v3 | Alta precisión semántica |
| LLM | Claude Sonnet / GPT-4o | Respuestas de alta calidad |
| Frontend | Next.js + TailwindCSS | Interfaz web responsive con autenticación |
| Auth | Auth0 o Supabase Auth | Control de acceso por roles (interno/externo) |
| Hosting | Railway o Vercel + Supabase | Infraestructura managed, sin sysadmin |
| Analytics | PostHog (gratis hasta 1M eventos) | Qué preguntan los usuarios, qué respuestas se usan |

**Costo mensual estimado:**

| Concepto | Costo USD/mes |
|---|---|
| Hosting (Railway o similar) | 20-40 |
| LLM API (Claude Sonnet, ~2.000 consultas/mes) | 30-80 |
| Embeddings + Vector DB | 10-30 |
| Auth0 (free tier hasta 7.500 usuarios) | 0 |
| **Total Nivel 3** | **60-150 USD/mes** |

**Tiempo de implementación:** 3-6 semanas (desarrollador Python + frontend junior).

---

## 3. Arquitectura RAG — cómo funciona el sistema

```
[Documentos CIGOB]
      |
      v
[Procesamiento]
  - Extracción de texto (docx, pdf, web)
  - Chunking (fragmentos de ~500 tokens con overlap)
      |
      v
[Embeddings]
  - Cada fragmento → vector numérico de 1536 dimensiones
      |
      v
[Vector Store]
  - Base de datos que permite buscar por similitud semántica
      |
      v
[Query del usuario]
  "¿Cuál es la posición de CIGOB sobre la IA?"
      |
      v
[Retrieval]
  - El sistema busca los 5-10 fragmentos más relevantes
      |
      v
[Augmented Generation]
  - Los fragmentos + la pregunta → prompt para Claude/GPT
  - El LLM genera una respuesta fundamentada en esos fragmentos
      |
      v
[Respuesta con citas]
  "Según el documento 'CIGOB frente a la IA' (Babino, 2026),
   la posición es la Anticipación Estratégica: [...cita textual...]"
```

---

## 4. Corpus inicial recomendado (los 5 documentos actuales)

| Documento | Tipo | Tokens estimados | Valor para el sistema |
|---|---|---|---|
| CIGOB frente al desafío de la IA | Paper de posición | ~2.500 | Alto — posicionamiento institucional |
| Propuesta Estratégica 2026-2027 | Documento operativo | ~1.800 | Alto — productos, estructura, plan |
| El Propósito de la Fundación CIGOB | Fundacional | ~1.200 | Alto — misión, valores |
| Profetas de Anticipación (Asimov) | Marco intelectual | ~1.500 | Medio — marco conceptual |
| Sobre Hechos y Profecías | Marco intelectual | ~2.000 | Medio — marco conceptual |
| Outputs de reuniones (output/*.md) | Análisis aplicados | ~15.000 | Muy alto — conocimiento operativo |
| Votómetro (metodología) | Producto técnico | ~5.000 | Alto — credencial técnica |

**Total corpus inicial:** ~29.000 tokens (~22 páginas). Perfectamente manejable para todos los niveles.

---

## 5. Funciones del sistema

### Funciones core (Nivel 0-1)
- Respuesta conversacional en lenguaje natural basada en los documentos
- Citas automáticas con referencia al documento y sección de origen
- Historial de conversación dentro de la sesión
- Reconocimiento de preguntas fuera del corpus ("no tengo información sobre eso en los documentos de CIGOB")

### Funciones extendidas (Nivel 2)
- URL pública con branding CIGOB
- Múltiples conversaciones simultáneas
- Panel de administración para agregar/actualizar documentos
- Preguntas sugeridas para guiar al usuario nuevo
- Modo "cita exacta" vs "síntesis"

### Funciones avanzadas (Nivel 3)
- Autenticación: acceso diferenciado (equipo interno vs. clientes externos)
- Historial persistente por usuario
- Analytics: qué preguntan los usuarios, qué documentos se usan más
- Integración con Votómetro: preguntas sobre datos electorales
- API propia para que otros sistemas de CIGOB consuman el Bibliotecario
- Modo multilenguaje (español rioplatense / neutro)
- Exportar conversación como resumen en PDF

---

## 6. Plan de escalado en fases

### Fase 0 — Validación (Semana 1-2)
**Objetivo:** Confirmar que el concepto funciona con los documentos reales de CIGOB.
**Acción:** Subir los 5 documentos a NotebookLM. Hacer 20 preguntas de prueba. Evaluar calidad de respuestas.
**Inversión:** $0. Tiempo: 2 horas.
**Criterio de paso:** Al menos 15 de 20 respuestas son correctas y citan la fuente.

### Fase 1 — MVP interno (Mes 1)
**Objetivo:** El equipo CIGOB usa el Bibliotecario en su trabajo diario.
**Acción:** Migrar a Claude Projects. Subir todos los outputs de reuniones y el corpus completo. Definir responsable de mantenimiento.
**Inversión:** USD 20/mes. Tiempo de setup: 1 día.
**Criterio de paso:** 3+ miembros del equipo lo usan al menos 2 veces por semana.

### Fase 2 — Producto externo (Mes 2-3)
**Objetivo:** Lanzar versión pública demostrable ante clientes y aliados.
**Acción:** Deploy en Flowise + VPS. URL propia. Branding CIGOB. Documentar el proceso como caso de estudio.
**Inversión:** USD 20-30/mes + 2-5 días de desarrollo.
**Criterio de paso:** El Bibliotecario tiene URL funcional y fue presentado a al menos 1 interlocutor externo.

### Fase 3 — Integración con Votómetro (Mes 3-4)
**Objetivo:** Crear el diferencial competitivo único: asistente de análisis electoral conversacional.
**Prerrequisito:** Los datos del Votómetro deben estar separados del HTML (ver QA técnico del Votómetro).
**Acción:** Conectar el corpus del Bibliotecario con los datos del Votómetro via API estructurada.
**Inversión:** USD 50-100 adicionales/mes + 2-4 semanas de desarrollo.
**Criterio de paso:** El sistema responde preguntas tipo "¿Cómo evolucionó LLA en Córdoba en los últimos 6 meses?" con datos reales.

### Fase 4 — Producto para gobiernos subnacionales (Mes 6+)
**Objetivo:** Ofrecer el Bibliotecario como servicio a provincias y municipios.
**Propuesta de valor:** "Un municipio sube sus ordenanzas, planes de gobierno y documentos de gestión. Sus funcionarios los consultan en lenguaje natural."
**Acción:** Refactorizar el sistema para corpus multi-tenant (un Bibliotecario por cliente). Autenticación. Soporte.
**Inversión:** USD 150-300/mes (infraestructura) + desarrollo inicial de 4-6 semanas.
**Modelo de negocio posible:** USD 200-500/mes por municipio cliente (SaaS) o incluido en contrato de consultoría.

---

## 7. Riesgos técnicos y mitigación

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| Alucinaciones (el sistema inventa datos) | Media | Alto | Configurar el sistema para responder solo con documentos propios. Modo strict: "si no está en el corpus, decirlo" |
| Calidad del corpus insuficiente | Alta inicial | Medio | Proceso de curación de documentos antes de subir. Formato limpio (sin tablas complejas, sin imágenes) |
| Costo de API escala sin control | Baja | Medio | Usar modelos económicos (Claude Haiku) para el frontend. Rate limiting. Monitoreo de uso |
| Documentos desactualizados | Alta | Medio | Proceso semanal de actualización. Fecha de última actualización visible en la interfaz |
| Dependencia de proveedor (Anthropic, OpenAI) | Baja | Alto | Arquitectura que permite cambiar el LLM sin reescribir el sistema (LangChain/Flowise abstrae esto) |

---

## 8. Resumen ejecutivo de costos

| Fase | Nivel | Costo mensual | Tiempo al primer resultado | Audiencia |
|---|---|---|---|---|
| Validación | 0 (NotebookLM) | USD 0 | 2 horas | Solo interno |
| MVP interno | 1 (Claude Projects) | USD 20 | 1 día | Equipo CIGOB |
| Producto externo | 2 (Flowise) | USD 20-30 | 2-5 días | Clientes, aliados |
| Integración Votómetro | 2-3 | USD 70-130 | 2-4 semanas | Usuarios especializados |
| Producto para gobiernos | 3 (Enterprise) | USD 150-300 | 4-8 semanas | Provincias, municipios |

**Punto de entrada recomendado:** Fase 0 esta semana (USD 0, 2 horas). Decisión de escalar a Fase 1 basada en los resultados de la validación.
