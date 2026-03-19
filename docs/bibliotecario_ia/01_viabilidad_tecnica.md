# Bibliotecario IA — Viabilidad Técnica

**Fundación CIGOB · Marzo 2026 · v2.0**

---

## 1. Qué es y para qué

Sistema RAG conversacional sobre el corpus documental de CIGOB. El usuario pregunta, el sistema responde citando fuentes. Corpus inicial: 5 DOCX limpios (~30k tokens). Debe escalar a cientos de PDFs de calidad variable — muchos escaneados — de gobiernos subnacionales argentinos.

Doble rol: herramienta de productividad interna del equipo CIGOB y producto vendible a provincias y municipios como SaaS.

---

## 2. Arquitectura del sistema

```
┌──────────────────────────────────────────────┐
│              CLIENTE (Vercel)                 │
│  Next.js 16                                  │
│  ├── Chat UI (AI SDK v6 + AI Elements)       │
│  ├── Admin: upload de documentos             │
│  └── Auth: Clerk (roles: admin/interno/demo) │
└─────────────────┬────────────────────────────┘
                  │
┌─────────────────▼────────────────────────────┐
│          QUERY LAYER (Next.js API Routes)     │
│  /api/chat → hybrid search + streamText      │
│              via AI Gateway (Claude Sonnet)   │
│  BM25 full-text + pgvector + RRF fusion      │
└────────────┬─────────────────────────────────┘
             │
┌────────────▼──────────────┐  ┌──────────────────┐
│  Neon Postgres             │  │  Vercel Blob      │
│  pgvector (HNSW)          │  │  PDFs/DOCX raw    │
│  tsvector (BM25)          │  │  (source of truth) │
│  tenants / docs / chunks  │  └────────┬─────────┘
└────────────────────────────┘           │
                                          │ trigger
┌─────────────────────────────────────────▼────────┐
│           INGESTION WORKER (Cloud Run / Modal)    │
│  Python                                          │
│  ├── Docling → PDF/DOCX/OCR (scanned)           │
│  ├── PyMuPDF4LLM → PDFs digitales               │
│  ├── Chunking semántico (~512t, overlap 64)      │
│  ├── text-embedding-3-small → vectores           │
│  └── escribe en Neon (chunks + embeddings)       │
└──────────────────────────────────────────────────┘
```

**Tres capas:**

- **Cliente (Vercel + Next.js 16):** UI de chat con streaming via AI SDK v6, panel admin para subir documentos, y autenticación con Clerk. Todo server-side rendering, sin SPA client-heavy.

- **Query Layer (API Routes):** Recibe la pregunta, ejecuta hybrid search (BM25 + vector) contra Neon, arma el contexto con los chunks más relevantes, y llama a Claude Sonnet via AI Gateway con `streamText`. La respuesta sale en streaming directo al cliente.

- **Ingestion Worker (Cloud Run):** Proceso Python asíncrono. Cuando se sube un documento a Vercel Blob, el worker lo descarga, lo parsea (Docling para escaneados, PyMuPDF4LLM para digitales), lo chunkea, genera embeddings con `text-embedding-3-small`, y escribe los chunks en Neon. Escala a cero cuando no hay trabajo.

---

## 3. Stack técnico

| Componente | Tecnología | Por qué esta y no otra |
|---|---|---|
| **Frontend + API** | Next.js 16 (Vercel) | AI SDK v6 nativo, streaming de primera clase, deploy zero-config en Vercel. No hay razón para separar frontend de API en este caso. |
| **Chat UI** | AI SDK v6 + AI Elements | `useChat` hook maneja streaming, reintentos y estado. AI Elements da componentes pre-armados (citaciones, markdown rendering). Alternativa era armar todo a mano. |
| **LLM** | Claude Sonnet 4.6 via AI Gateway | Mejor comprensión de español que GPT-4o en benchmarks internos. AI Gateway da failover automático, cost tracking y auth OIDC (sin API keys hardcodeadas en el código). |
| **Auth** | Clerk Organizations | Multi-tenant nativo: cada organización = un tenant. Free tier cubre 100 orgs + 50k MAU. Alternativas (Auth.js, Supabase Auth) no tienen multi-org built-in. |
| **Base de datos** | Neon Postgres + pgvector | Una sola base para vectores, full-text y metadata relacional. Sin necesidad de un vector DB separado (Pinecone, Qdrant). HNSW nativo, `tsvector` con diccionario `spanish`. Región São Paulo (~30-50ms desde BA). |
| **Storage** | Vercel Blob | $0.023/GB-mes. Los archivos originales quedan como source of truth. Sin límite práctico de tamaño por archivo. |
| **Embeddings** | text-embedding-3-small (OpenAI) | 1536 dims, $0.02/1M tokens standard, $0.01/1M batch. Buena calidad para español. Alternativa Nomic es gratis pero menor calidad en español. |
| **Worker** | Cloud Run (Python) | Free tier generoso (180k vCPU-seg/mes), región São Paulo, escala a 0, hasta 32 GB RAM y timeout de 60 min. Modal es alternativa si se necesita GPU para OCR pesado. |
| **PDF parsing** | Docling + PyMuPDF4LLM | Ver sección de ingesta. |

---

## 4. Ingesta de documentos

### Flujo completo

```
Upload (Admin UI) → Vercel Blob (almacena raw)
                  → POST /api/ingest (registra doc en Neon, status: pending)
                  → Cloud Run worker (poll o webhook)
                      ├── Detecta tipo: digital vs escaneado
                      ├── Parsea → texto limpio
                      ├── Chunkea: ~512 tokens, overlap 64
                      ├── Genera embeddings (batch API si >100 chunks)
                      └── Escribe chunks + embeddings en Neon
                          → status: indexed
```

### Comparativa de parsers PDF

| Parser | Accuracy tablas | OCR | Velocidad | Cuándo usarlo |
|---|---|---|---|---|
| **Docling (IBM)** | 97.9% | Integrado (Tesseract/EasyOCR) | Lento (~2-5 seg/página) | PDFs escaneados, documentos con tablas complejas, decretos municipales fotografiados. Es el default para todo lo que no sea trivial. |
| **PyMuPDF4LLM** | Buena para simples | No tiene | Rápido (~0.1 seg/página) | PDFs digitales nativos (generados por Word, Google Docs). Salida en Markdown limpio. Usar cuando se sabe que el PDF es digital. |
| **Marker** | Intermedia | Surya (propio) | Medio (~1 seg/página) | Alto volumen mixto donde no se puede clasificar uno por uno. Buen compromiso calidad/velocidad. Mejor soporte multilingual que Docling. |

**Estrategia de detección:** PyMuPDF intenta extraer texto. Si el ratio texto/páginas es <50 caracteres por página, es escaneado → Docling. Si no, PyMuPDF4LLM.

### Chunking

Semántico con fallback a tamaño fijo. Target: ~512 tokens por chunk, overlap de 64 tokens. El overlap garantiza que no se pierda contexto en los bordes. Metadata por chunk: `document_id`, `page_number`, `section_title` (si se puede extraer), `chunk_index`.

---

## 5. Retrieval: hybrid search

Vector-only search tiene un problema conocido: falla con términos técnicos, siglas y nombres propios. Si alguien pregunta "¿Qué dice CIGOB sobre EMAE?", el embedding de "EMAE" no necesariamente es cercano al embedding del chunk que menciona el Estimador Mensual de Actividad Económica. BM25 lo encuentra por coincidencia exacta de término.

La combinación BM25 + vector con Reciprocal Rank Fusion (RRF) resuelve esto sin necesidad de tuning manual de pesos.

### SQL de hybrid search

```sql
-- Reciprocal Rank Fusion: BM25 + vector similarity
WITH vector_search AS (
  SELECT id, content, metadata,
    1 - (embedding <=> $1::vector) AS score,
    ROW_NUMBER() OVER (ORDER BY embedding <=> $1::vector) AS rank
  FROM chunks
  WHERE tenant_id = $2
  ORDER BY embedding <=> $1::vector
  LIMIT 30
),
text_search AS (
  SELECT id, content, metadata,
    ts_rank(to_tsvector('spanish', content), plainto_tsquery('spanish', $3)) AS score,
    ROW_NUMBER() OVER (ORDER BY ts_rank(to_tsvector('spanish', content),
                       plainto_tsquery('spanish', $3)) DESC) AS rank
  FROM chunks
  WHERE tenant_id = $2
    AND to_tsvector('spanish', content) @@ plainto_tsquery('spanish', $3)
  LIMIT 30
)
SELECT COALESCE(v.id, t.id) AS id,
       COALESCE(v.content, t.content) AS content,
       COALESCE(v.metadata, t.metadata) AS metadata,
       (1.0 / (60 + COALESCE(v.rank, 1000))) +
       (1.0 / (60 + COALESCE(t.rank, 1000))) AS rrf_score
FROM vector_search v
FULL OUTER JOIN text_search t ON v.id = t.id
ORDER BY rrf_score DESC
LIMIT 8;
```

**Parámetros:**
- `$1`: vector embedding de la query del usuario
- `$2`: UUID del tenant (filtro de aislamiento)
- `$3`: texto de la query (para BM25)
- `k=60` en RRF: valor estándar, penaliza menos a los resultados de ranking medio
- `LIMIT 30` por rama: suficiente para que RRF tenga material; más de 30 no mejora calidad
- `LIMIT 8` final: 8 chunks × ~512 tokens = ~4k tokens de contexto, dentro de lo que Claude maneja con precisión de citas

### Índices requeridos

```sql
CREATE INDEX ON chunks USING hnsw (embedding vector_cosine_ops);
CREATE INDEX ON chunks USING gin (to_tsvector('spanish', content));
CREATE INDEX ON chunks (tenant_id);
```

El índice HNSW es más rápido que IVFFlat para consultas y no requiere re-entrenamiento al agregar datos. El GIN sobre `tsvector('spanish', ...)` usa el diccionario de stemming en español (incluido en Postgres), lo que significa que "anticipación" y "anticipar" matchean.

---

## 6. Multi-tenancy

### Estrategia: Pool con filtro por tenant_id

Todos los tenants comparten la misma base de datos. El aislamiento es por `WHERE tenant_id = $X` en cada query. Es la estrategia correcta para este caso porque:

- Los datos no son ultra-sensibles (documentos institucionales, no datos personales regulados)
- Simplifica operaciones: una sola base, un solo backup, un solo schema migration
- Escala a cientos de tenants sin overhead de infraestructura
- Si en el futuro un municipio exige aislamiento físico, se puede migrar a schema-per-tenant sin cambiar la aplicación

### Schema

```sql
CREATE TABLE tenants (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  slug TEXT UNIQUE NOT NULL,  -- 'cigob', 'municipio-cordoba', etc.
  name TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE documents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID REFERENCES tenants(id) NOT NULL,
  title TEXT NOT NULL,
  source_url TEXT,  -- Vercel Blob URL
  file_type TEXT,   -- 'pdf', 'docx'
  status TEXT DEFAULT 'pending',  -- pending | processing | indexed | error
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE chunks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  document_id UUID REFERENCES documents(id) NOT NULL,
  tenant_id UUID REFERENCES tenants(id) NOT NULL,  -- denormalizado para perf
  content TEXT NOT NULL,
  embedding VECTOR(1536),
  chunk_index INTEGER NOT NULL,
  metadata JSONB DEFAULT '{}',  -- page_number, section, etc.
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX ON chunks USING hnsw (embedding vector_cosine_ops);
CREATE INDEX ON chunks USING gin (to_tsvector('spanish', content));
CREATE INDEX ON chunks (tenant_id);
```

`tenant_id` está denormalizado en `chunks` para evitar un JOIN con `documents` en cada query de búsqueda. Es la tabla que más se consulta y el JOIN penaliza latencia.

### Mapping con Clerk

Cada Clerk Organization tiene un `slug` que matchea con `tenants.slug`. El middleware de Next.js extrae el `organizationId` del token JWT, lo resuelve a `tenant_id` con un cache en memoria, y lo inyecta en el contexto de cada request. Ningún endpoint de la API funciona sin `tenant_id`.

---

## 7. Costos reales por fase

### Fase 1 — CIGOB solo (MVP)

| Recurso | Servicio | Costo/mes |
|---|---|---|
| App + API | Vercel Pro | $20 |
| Base de datos | Neon Free (0.5 GB) | $0 |
| Storage | Vercel Blob (~0.1 GB) | ~$0 |
| Embeddings | text-embedding-3-small (ingesta única ~30k tokens) | ~$0.01 |
| LLM | Claude Sonnet via AI Gateway (~200 queries/día) | ~$8-12 |
| Auth | Clerk Free (1 org) | $0 |
| Worker | Script CLI local (sin hosting) | $0 |
| **Total** | | **~$20-32/mes** |

### Fase 2 — Demos externas

| Recurso | Servicio | Costo/mes |
|---|---|---|
| App + API | Vercel Pro | $20 |
| Base de datos | Neon Launch (50 GB) | $19 |
| Storage | Vercel Blob (~1 GB) | ~$0.02 |
| Embeddings | Ingesta 50+ docs | ~$0.10 |
| LLM | Claude Sonnet (~500 queries/día) | ~$15-25 |
| Auth | Clerk Free | $0 |
| Worker | Cloud Run Free Tier | $0 |
| **Total** | | **~$55-65/mes** |

### Fase 4 — SaaS municipios (20 clientes)

| Recurso | Servicio | Costo/mes |
|---|---|---|
| App + API | Vercel Pro | $20 |
| Base de datos | Neon Launch (50 GB) | $19 |
| Storage | Vercel Blob (~6 GB, 500 PDFs) | ~$0.14 |
| Embeddings | Ingesta ~50M tokens (batch) | ~$0.50 (único) |
| LLM | Claude Sonnet (~1000 queries/día) | ~$50-80 |
| Auth | Clerk Free (20 orgs < 100 límite) | $0 |
| Worker | Cloud Run (puede salir del free tier) | ~$10-20 |
| **Total** | | **~$100-140/mes** |

**Ingreso potencial:** 20 municipios × $300/mes promedio = $6.000/mes. Margen bruto >95%.

---

## 8. Riesgos y mitigación

### PDFs escaneados de baja calidad

El riesgo más real. Municipios argentinos van a subir escaneos torcidos de resoluciones de los 90s. Docling con OCR maneja la mayoría, pero la accuracy baja con documentos muy degradados.

**Mitigación:** Pipeline de validación post-OCR. Si el texto extraído tiene >30% de tokens irreconocibles (heurística simple: ratio de palabras fuera de diccionario español), marcar el documento como `quality: low` y alertar al admin. No indexar basura.

### Alucinaciones en respuestas

Claude puede inventar contenido que no está en los chunks recuperados, especialmente cuando la pregunta es ambigua y los chunks son tangencialmente relevantes.

**Mitigación:** System prompt estricto: "Respondé SOLO con información presente en los fragmentos proporcionados. Si la información no está, decí que no la encontrás." Agregar al prompt los chunks con numeración explícita y pedir que cite por número. Validar en la UI que cada afirmación tiene cita.

### Latencia de cold start en Cloud Run

Si el worker escala a 0 y llega un upload, el cold start puede ser 10-30 segundos (Python + dependencias pesadas como Docling).

**Mitigación:** El upload es asíncrono. El usuario sube el archivo y ve status "procesando". No hay expectativa de respuesta instantánea. Si el cold start se vuelve problemático, configurar `min-instances: 1` en Cloud Run (costo: ~$15/mes adicionales).

### Neon cold start en free tier

Las bases Neon en free tier suspenden el compute después de 5 minutos de inactividad. El wake-up agrega 500ms-2s a la primera query.

**Mitigación:** En Fase 1 es aceptable (uso interno, baja frecuencia). En Fase 2+ con Neon Launch ($19/mes) el compute no suspende.

### Calidad del retrieval con corpus chico

Con solo 5 documentos (~60 chunks), el hybrid search puede devolver chunks irrelevantes simplemente porque no hay suficientes candidatos para que el ranking discrimine.

**Mitigación:** Threshold mínimo de relevancia. Si el `rrf_score` máximo está por debajo de un umbral (a calibrar empíricamente), responder "No encontré información suficiente" en vez de forzar una respuesta con chunks mediocres.

---

## 9. Plan de implementación

### Fase 1 — MVP CIGOB solo

**Criterio de entrada:** Decisión tomada, dev disponible.

**Entregable:** Chat funcional deployado en Vercel, corpus de CIGOB indexado, equipo usándolo.

**Criterio de paso a Fase 2:** El equipo CIGOB usa el sistema al menos 3 veces por semana durante 2 semanas consecutivas y la calidad de respuestas es aceptable (>80% de las respuestas son correctas y citadas).

**Componentes a construir:**
1. Proyecto Next.js 16 con AI SDK v6 — chat UI con streaming
2. Schema en Neon (las 3 tablas + índices)
3. Script CLI Python de ingesta (no necesita Cloud Run todavía)
4. API route `/api/chat` con hybrid search + `streamText`
5. Clerk básico (un tenant, sin multi-org todavía)

### Fase 2 — Demos externas

**Criterio de entrada:** Fase 1 validada internamente.

**Entregable:** Admin UI para upload, worker de ingesta en Cloud Run, roles diferenciados (admin/interno/demo).

**Criterio de paso a Fase 3:** Al menos una demo externa exitosa y feedback recogido.

**Componentes a construir:**
1. Admin UI: upload de documentos con drag & drop, lista de docs, status de ingesta
2. Worker Python en Cloud Run con detección automática digital/escaneado
3. Webhook o polling para trigger de ingesta post-upload
4. Roles en Clerk: admin (upload + chat), interno (chat completo), demo (chat limitado, sin historial)

### Fase 3 — Integración Votómetro

**Criterio de entrada:** Datos del Votómetro extraídos del HTML a una estructura consultable (API o tabla en Neon).

**Entregable:** El Bibliotecario responde preguntas sobre datos electorales con la misma interfaz.

**Criterio de paso a Fase 4:** Queries electorales funcionan con accuracy verificable contra datos conocidos.

**Componentes a construir:**
1. Extracción de datos del Votómetro a tablas estructuradas en Neon
2. Router de queries: detectar si la pregunta es documental o electoral
3. Para queries electorales: SQL directo sobre tablas estructuradas (no RAG)
4. Combinar respuestas de ambas fuentes cuando la pregunta es mixta

### Fase 4 — SaaS municipios

**Criterio de entrada:** Al menos 2 municipios confirmaron interés y tienen documentos listos.

**Entregable:** Onboarding self-service (o asistido), aislamiento de datos, facturación.

**Componentes a construir:**
1. Flujo de onboarding: crear Clerk Organization → crear tenant en Neon → subir documentos
2. Dashboard por tenant: uso, documentos indexados, queries frecuentes
3. Límites por plan: cantidad de documentos, queries/mes
4. Landing page comercial

---

## 10. Por dónde empezar hoy

**Acción 1: Scaffold del proyecto Next.js + primera query funcionando.**

```bash
npx create-next-app@latest bibliotecario-ia --typescript --tailwind --app
cd bibliotecario-ia
npm install ai @ai-sdk/anthropic @neondatabase/serverless
```

Crear `/api/chat/route.ts` que reciba un mensaje y responda con `streamText` usando Claude Sonnet. Sin RAG todavía — solo verificar que el streaming funciona end-to-end en Vercel.

**Acción 2: Schema en Neon + script de ingesta.**

Crear la base en Neon (free tier, región sa-east-1). Correr el schema SQL de la sección 6. Escribir un script Python que tome los 5 DOCX de `docs/`, los chunkee y los indexe. Verificar con una query SQL manual que el hybrid search devuelve chunks relevantes.

**Acción 3: Conectar retrieval al chat.**

Modificar `/api/chat` para que antes de llamar a Claude, ejecute el hybrid search con la pregunta del usuario, arme un prompt con los chunks recuperados, y pase todo a `streamText`. Cuando esto funcione con los 5 DOCX, Fase 1 está esencialmente terminada.
