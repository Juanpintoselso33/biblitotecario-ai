# Requisitos técnicos — Votómetro Argentina 2027 (desarrollo colaborativo CIGOB + Redlines)

**Fecha:** 13 de abril de 2026
**Destinatario:** Redlines Estrategia y Comunicación
**Autor:** Fundación CIGOB
**Repositorio actual:** https://github.com/Juanpintoselso33/biblitotecario-ai
**Deploy actual:** https://juanpintoselso33.github.io/biblitotecario-ai/index.html
**Archivo analizado:** `web/votometro.html` (2.232 líneas) + `web/encuestas.json` (1.324 líneas — dual-write parcial)

---

## 0. Resumen ejecutivo

El Votómetro funciona, pero como prototipo de autor. Cada encuesta nueva se toca a mano en un archivo de 2.232 líneas donde conviven HTML, CSS, el motor Monte Carlo, los coeficientes de ponderación, los fundamentals, las cadenas de texto editoriales y las 99 encuestas. El `scripts/actualizar_encuestas.py` existe pero hace dual-write frágil sobre un literal JavaScript del HTML — funciona mientras no cambie el formato de esa línea.

Este documento propone una evolución en tres fases:

1. **Fase 1 (2 semanas)** — separar datos de código sin cambiar de stack. Migrar el HTML actual a un pipeline Astro de archivo único, con los datos en JSON externo y un script de build que inyecta todo. CIGOB conserva control del motor, Redlines edita contenido sin tocar JavaScript.
2. **Fase 2 (4-6 semanas)** — Next.js con API routes para encuestas provinciales, CMS ligero (Decap) para que Redlines edite encuestas desde el navegador, y deploy a Vercel con preview branches.
3. **Fase 3 (cuando haya señal)** — base de datos (Neon o Supabase) si el volumen de encuestas provinciales supera lo que se puede versionar en Git (criterio: más de 500 registros o actualización diaria).

La recomendación fuerte es **empezar por Fase 1 ya mismo**. El HTML actual no es sostenible para el desarrollo colaborativo. Cualquier edición paralela CIGOB/Redlines provoca conflictos de merge en el mismo archivo.

---

## 1. Diagnóstico del estado actual

### 1.1 Qué hay adentro de `web/votometro.html`

Mapeo de lo que encontramos línea por línea:

| Líneas | Contenido | Quién lo toca |
|---|---|---|
| 1–1.040 | HTML estructural + CSS (~1.000 líneas) | Redlines (editorial, diseño) |
| 1.041–1.056 | Constantes del modelo (`LAMBDA`, `FECHA_REF`, `ULTIMA_ACTUALIZACION`) | CIGOB |
| 1.067–1.150 | 4 tablas de ponderación (CALIDAD, SESGO, MEDIO, METODOLOGÍA) por consultora | CIGOB |
| 1.169–1.410 | `encuestasRaw` — 99 encuestas como array literal JS | CIGOB (via script) |
| 1.411–1.497 | Función `calcPeso`, media ponderada, `calcularPriorFundamentals` | CIGOB |
| 1.449–1.471 | **Fundamentals hardcodeados** (`aprobacion=38`, `icc=42.03`, `emaeIa=1.9`) | CIGOB |
| 1.498–1.560 | Monte Carlo (`SIM=10000`, `SIGMA=6.5`, `RHO=-0.7`) + ballotage hardcodeado (`50` Milei, `33` Kicillof) | CIGOB |
| 1.562–1.640 | Inyección de textos analíticos en el DOM (primera vuelta, blend, presData) | Mixto — lógica CIGOB, narrativa Redlines |
| 1.640–2.232 | Gráficos Chart.js, tabla de encuestas, datos de eventos/gobernadores embebidos | Mixto |

### 1.2 Problemas críticos (priorizados por fricción actual)

1. **Dual-write frágil.** `scripts/actualizar_encuestas.py` escribe `web/encuestas.json` y también regex-parchea el literal `encuestasRaw = [...]` en el HTML. Si Redlines reformatea el HTML, el regex se rompe silenciosamente y los datos divergen.
2. **Ballotage hardcodeado.** Línea 1.523: `let ballM = 50 + randn()*sigmaBall`. Línea 1.524: `let ballK = 33 + randn()*sigmaBall`. Estos 50 y 33 son literales numéricos, no parámetros. Cambiar la encuesta de segunda vuelta requiere editar el script inline del HTML.
3. **Fundamentals hardcodeados.** Líneas 1.458–1.461: `baselineLLA = 40.84`, `aprobacion = 38`, `icc = 42.03`, `emaeIa = 1.9`. Comentarios dicen "actualizar mensualmente" — pero nadie garantiza que eso pase porque el lugar de edición es un archivo de 2.000+ líneas.
4. **Textos editoriales mezclados con lógica.** Línea 1.576: `frHTML = '<strong>LLA ganaría...';` — la narrativa de primera vuelta se construye con template literals dentro del motor. Redlines no puede reescribir esa narrativa sin tocar JavaScript.
5. **Eventos del gráfico de aprobación: no existen como datos.** El complemento de CIGOB propone 6 hitos políticos para anotar en el gráfico. Hoy no hay estructura para cargarlos.
6. **Provincias: sola mención, sin estructura.** Línea 743 cita la encuesta CB Global Data feb-2026 (24.690 casos). No hay schema, no hay array, no hay agregación por provincia.
7. **Sin separación UI/lógica.** Todo es un archivo. Los conflictos de merge son inevitables si más de una persona trabaja al mismo tiempo.
8. **Deploy en repositorio mal nombrado.** El remote es `biblitotecario-ai.git` (con typo) y sirve ambos productos (bibliotecario IA + Votómetro). Debería separarse.

### 1.3 Qué conviene conservar

- **La lógica del motor.** El modelo quíntuple + Monte Carlo + prior fundamentals está bien calibrado y validado. No hay que reescribirlo — hay que separarlo del HTML.
- **Chart.js 4.4.0.** Cumple bien, no hay razón para migrar a D3 o Recharts en esta etapa.
- **Fuentes y paleta.** DM Serif Display + DM Sans + JetBrains Mono + paleta celeste/violeta/azul. Son identidad de producto, se mantienen.
- **Dark mode.** Ya está implementado con `data-theme="dark"`, funciona.
- **El script `actualizar_encuestas.py`.** La lógica de validación (suma 85-115, fecha no futura, detección de duplicados, backup .bak) sirve — hay que extraerla a una librería y usarla en todos los endpoints de escritura.

---

## 2. Propuesta de stack

### 2.1 Criterios de decisión

- CIGOB no tiene equipo de desarrollo dedicado — el proyecto lo mantienen 1-2 personas que programan medio tiempo.
- El producto se actualiza 2-4 veces por semana (encuestas nuevas) y una vez por mes (fundamentals).
- Redlines debe poder editar contenido sin saber JavaScript.
- El deploy debe ser rápido (<5 min de commit a producción) y reversible.
- No tiene que haber backend con base de datos en la primera iteración — los datos caben en Git.

### 2.2 Recomendación: Astro + TypeScript + JSON en Git

**Astro** es el punto dulce para este caso:

- Genera HTML estático (igual que hoy, funciona sin servidor, deployable en GitHub Pages, Vercel o Cloudflare Pages).
- Tiene el modelo de "islas" — podemos dejar Chart.js como JS cliente sin tener que migrar todo a un framework.
- Permite importar JSON directamente en componentes en build time.
- Tiene Content Collections con validación Zod, que es exactamente lo que necesitamos para las encuestas.
- Curva de aprendizaje mínima si se viene de HTML+JS — no hay JSX obligatorio, los componentes son `.astro` con sintaxis HTML.
- Construye en 2-5 segundos. Dev server con hot reload.

**TypeScript** mínimo: solo para los schemas de datos (encuesta, fundamentals, evento). No hace falta tipar todo el proyecto — los schemas Zod dan el 80% del beneficio con el 20% del esfuerzo.

**Por qué no las alternativas:**

- **Next.js** — overkill para Fase 1. Requiere entender App Router, server components, caching. Recomendado para Fase 2 cuando haya API routes (encuestas provinciales con formulario).
- **Vue/Nuxt** — buen framework pero no aporta sobre Astro para este caso y suma dependencia de ecosistema.
- **HTML puro + JS + un build script Python** — tentador pero regresivo. Perdemos validación de schemas, hot reload, typechecking.
- **React SPA (Vite)** — cliente-side rendering innecesario para un dashboard estático. Peor SEO, peor performance inicial.

### 2.3 Versión del stack propuesto

```
astro@4.x
@astrojs/check
typescript@5.x
zod@3.x           (validación de schemas de datos)
chart.js@4.4.x    (ya en uso — conservar)
```

**Sin React, sin Vue, sin Tailwind.** El CSS actual está bien y es parte de la identidad. Migrar a Tailwind sería un side-quest que no agrega valor en esta etapa.

---

## 3. Arquitectura de datos

Todos los datos se separan del HTML y se versionan como JSON en `src/data/`. Astro los importa en build time. La estructura propuesta:

```
src/
  data/
    encuestas/
      nacionales.json          # voto presidencial nacional (las 99 actuales)
      ballotage.json           # encuestas de segunda vuelta
      provinciales/
        buenos-aires.json
        cordoba.json
        ...                    # un archivo por provincia (24 archivos máx.)
    fundamentals/
      historico.json           # serie mensual de aprobación, ICC, EMAE
      actual.json              # snapshot del mes corriente (para el prior)
    eventos/
      aprobacion.json          # hitos políticos para anotar gráficos
    consultoras.json           # metadata de ponderación
    config/
      modelo.json              # λ, σ, ρ, SIM, CAND_ADJ, ELECTION_DATE
      copy.json                # textos editoriales (Redlines edita aquí)
  schemas/
    encuesta.ts                # Zod schema nacional
    encuesta-provincial.ts
    fundamentals.ts
    evento.ts
    consultora.ts
```

### 3.0 Taxonomía de encuestas — dos ejes independientes

El campo `tipo` actual (`espacio`/`candidato`) responde a una pregunta metodológica: *¿cómo estaba formulada la pregunta?* Esto afecta directamente el motor del modelo (corrección +4pp LLA para encuestas tipo candidato). **No dice qué se está midiendo.**

Se necesita un segundo eje, `categoria`, que clasifica qué variable está midiendo la encuesta. Son ortogonales:

| | `tipo: espacio` | `tipo: candidato` | sin `tipo` |
|---|---|---|---|
| `categoria: intencion_voto` | ✓ (mayoría del corpus) | ✓ (ej. Isasi Burdman dic-2024) | — |
| `categoria: ballotage` | ✓ si pregunta LLA vs PJ | ✓ si pregunta Milei vs Kicillof | — |
| `categoria: aprobacion` | — | — | ✓ estructura distinta |
| `categoria: imagen` | — | — | ✓ estructura distinta |
| `categoria: gobernadores` | ✓ | ✓ | — |

**Regla de uso en el motor:**
- El modelo de intención de voto solo consume encuestas con `categoria: 'intencion_voto'`.
- El mini-modelo de segunda vuelta solo consume `categoria: 'ballotage'` (array separado).
- Las encuestas de `categoria: 'aprobacion'` alimentan el prior de fundamentals (junto con ICC y EMAE).
- Las encuestas de `categoria: 'imagen'` son para el gráfico de valoración de gestión.
- Las encuestas de `categoria: 'gobernadores'` alimentan el módulo provincial futuro.

Esto permite tener **un solo repositorio de encuestas** (`src/data/encuestas/`) con tipo enumerado, en lugar de carpetas separadas por tipo de medición. El motor filtra por `categoria` al inicio de cada cálculo.

---

### 3.1 Schema — Encuesta nacional (intención de voto)

Archivo: `src/schemas/encuesta.ts`

```typescript
import { z } from 'zod';

export const CategoriaEncuesta = z.enum([
  'intencion_voto',  // pregunta por partido/espacio o candidato presidencial
  'ballotage',       // pregunta de segunda vuelta (head-to-head)
  'aprobacion',      // aprobación/desaprobación de la gestión
  'imagen',          // imagen positiva/negativa del presidente u otro actor
  'gobernadores',    // intención de voto o imagen a nivel provincial
]);

// 'tipo' responde a cómo está formulada la pregunta (afecta corrección del motor)
export const TipoFormulacion = z.enum([
  'espacio',    // la pregunta menciona LLA, PJ, PRO como espacios
  'candidato',  // la pregunta menciona nombres (Milei, Kicillof, Bullrich)
  'real',       // resultado electoral oficial (no encuesta)
]);

export const EncuestaIntencionVoto = z.object({
  fecha: z.string().regex(/^\d{4}-\d{2}-\d{2}$/),
  consultora: z.string().min(1),
  categoria: z.literal('intencion_voto'),
  tipo: TipoFormulacion,
  LLA: z.number().min(0).max(100),
  PJ: z.number().min(0).max(100),
  PRO: z.number().min(0).max(100),
  PU: z.number().min(0).max(100),
  FIT: z.number().min(0).max(100),
  OTROS: z.number().min(0).max(100),
  muestra: z.number().int().positive(),
  calidad: z.enum(['A', 'B', 'C']),
  url: z.string().url().optional(),
  notas: z.string().optional()
}).refine(e => {
  const suma = e.LLA + e.PJ + e.PRO + e.PU + e.FIT + e.OTROS;
  return suma >= 85 && suma <= 115;
}, { message: 'suma de partidos debe estar entre 85 y 115' });

export type EncuestaIntencionVoto = z.infer<typeof EncuestaIntencionVoto>;
```

### 3.1b Schema — Encuesta de ballotage (array separado)

**Decisión tomada:** las encuestas de segunda vuelta van en `src/data/encuestas/ballotage.json`, separadas del array nacional. Son elecciones distintas, con lógica de modelo distinta.

```typescript
export const EncuestaBallotage = z.object({
  fecha: z.string().regex(/^\d{4}-\d{2}-\d{2}$/),
  consultora: z.string().min(1),
  categoria: z.literal('ballotage'),
  tipo: TipoFormulacion,   // candidato (Milei vs Kicillof) o espacio (LLA vs PJ)
  LLA: z.number().min(0).max(100),  // % para LLA en 2da vuelta
  PJ: z.number().min(0).max(100),
  NS_NC: z.number().min(0).max(100).optional(),
  muestra: z.number().int().positive(),
  calidad: z.enum(['A', 'B', 'C']),
  url: z.string().url().optional(),
  notas: z.string().optional()
});
```

Ejemplo de entrada:
```json
{
  "fecha": "2026-03-01",
  "consultora": "Isasi Burdman",
  "categoria": "ballotage",
  "tipo": "candidato",
  "LLA": 51.0,
  "PJ": 33.0,
  "NS_NC": 16.0,
  "muestra": 1400,
  "calidad": "A",
  "url": "https://www.isasiburdman.com.ar"
}
```

El motor lee `ballotage.json`, calcula la media ponderada (mismo algoritmo quíntuple que intención de voto), y reemplaza los valores actualmente hardcodeados en líneas 1.523–1.524 del HTML.

### 3.1c Schema — Aprobación de gestión

```typescript
export const EncuestaAprobacion = z.object({
  fecha: z.string().regex(/^\d{4}-\d{2}-\d{2}$/),
  consultora: z.string().min(1),
  categoria: z.literal('aprobacion'),
  aprueba: z.number().min(0).max(100),
  desaprueba: z.number().min(0).max(100),
  ns_nc: z.number().min(0).max(100).optional(),
  muestra: z.number().int().positive(),
  calidad: z.enum(['A', 'B', 'C']),
  url: z.string().url().optional(),
  notas: z.string().optional()
}).refine(e => {
  const suma = e.aprueba + e.desaprueba + (e.ns_nc ?? 0);
  return suma >= 85 && suma <= 115;
}, { message: 'suma aprueba + desaprueba + NS/NC debe estar entre 85 y 115' });
```

**Uso en el motor:** `aprueba` reemplaza el valor actualmente hardcodeado (`aprobacion = 38`) en el prior de fundamentals. Se calcula como media ponderada de las encuestas con `categoria: 'aprobacion'` de los últimos 60 días.

### 3.1d Schema — Imagen / valoración

**Decisión tomada:** el ICC Di Tella se mantiene como referencia interna del motor (input del prior de fundamentals) pero **no se muestra en la UI pública**. El gráfico de valoración de gestión usa encuestas de `categoria: 'imagen'` de consultoras, no el ICC directamente.

```typescript
export const EncuestaImagen = z.object({
  fecha: z.string().regex(/^\d{4}-\d{2}-\d{2}$/),
  consultora: z.string().min(1),
  categoria: z.literal('imagen'),
  sujeto: z.string(),           // 'Milei', 'gobierno', 'gestión económica', etc.
  imagen_positiva: z.number().min(0).max(100),
  imagen_negativa: z.number().min(0).max(100),
  ns_nc: z.number().min(0).max(100).optional(),
  muestra: z.number().int().positive(),
  calidad: z.enum(['A', 'B', 'C']),
  url: z.string().url().optional(),
  notas: z.string().optional()
});
```

**Uso en la UI:** el gráfico de saldo neto (aprobación − desaprobación) en la sección Valoración se construye con este array. No con el ICC. El ICC alimenta el motor en silencio.

### 3.1e Unión discriminada — un solo archivo si se prefiere

Si se quiere mantener un único `encuestas.json` en lugar de archivos separados, se puede usar un union discriminado Zod:

```typescript
export const Encuesta = z.discriminatedUnion('categoria', [
  EncuestaIntencionVoto,
  EncuestaBallotage,
  EncuestaAprobacion,
  EncuestaImagen,
  EncuestaProvincial,
]);

export type Encuesta = z.infer<typeof Encuesta>;
```

El motor filtra al inicio: `encuestas.filter(e => e.categoria === 'intencion_voto')`. Cada módulo solo ve su slice. **Recomendación:** archivos separados por categoria en Fase 1 (más legible para Redlines, menos riesgo de mezclar datos), union discriminada en Fase 2 si se implementa un CMS o API.

**Ventaja clave:** Astro ejecuta la validación en build time. Si alguien comitea una encuesta inválida (ej. una de ballotage en el archivo de intención de voto), el build falla antes de deployear.

### 3.2 Schema — Encuesta provincial

```typescript
export const EncuestaProvincial = z.object({
  fecha: z.string().regex(/^\d{4}-\d{2}-\d{2}$/),
  provincia: z.enum([
    'buenos-aires', 'caba', 'catamarca', 'chaco', 'chubut', 'cordoba',
    'corrientes', 'entre-rios', 'formosa', 'jujuy', 'la-pampa', 'la-rioja',
    'mendoza', 'misiones', 'neuquen', 'rio-negro', 'salta', 'san-juan',
    'san-luis', 'santa-cruz', 'santa-fe', 'santiago-del-estero',
    'tierra-del-fuego', 'tucuman'
  ]),
  consultora: z.string().min(1),
  tipo: z.enum(['intencion_voto', 'imagen', 'aprobacion']),
  // estructura flexible — cada provincia tiene sus propios espacios
  espacios: z.record(z.string(), z.number().min(0).max(100)),
  muestra: z.number().int().positive(),
  calidad: z.enum(['A', 'B', 'C']),
  url: z.string().url().optional(),
  notas: z.string().optional()
});
```

**Nota estratégica:** como los partidos provinciales varían (ej. Frente de Todos Santafesino, Hacemos por Córdoba), usamos `espacios: Record<string, number>` en vez de campos fijos LLA/PJ. El frontend muestra los top 3-4 espacios por provincia.

### 3.3 Schema — Fundamentals

Archivo: `src/data/fundamentals/historico.json`

```json
{
  "series": [
    {
      "mes": "2026-03",
      "aprobacion": {
        "valor": 38,
        "fuente": "Promedio ponderado AtlasIntel (36.4%, n=5037) + M&F (46.8%)",
        "tipo": "aprobacion_gestion"
      },
      "imagen_positiva": {
        "valor": 42,
        "fuente": "CB Global Data mar-2026",
        "tipo": "imagen_personal"
      },
      "icc": {
        "valor": 42.03,
        "variacion_mom": -5.3,
        "fuente": "UTDT CIF, 4-13 mar 2026"
      },
      "emae": {
        "valor": 1.9,
        "tipo": "variacion_ia",
        "mes_medicion": "2026-01",
        "fuente": "INDEC, pub. 26-mar-2026"
      }
    }
  ]
}
```

Decisión deliberada: separar `aprobacion_gestion` de `imagen_personal` (punto 9 del complemento CIGOB — hay 5pp de diferencia entre ambas).

### 3.4 Schema — Eventos (anotaciones en el gráfico de aprobación)

```typescript
export const Evento = z.object({
  fecha: z.string().regex(/^\d{4}-\d{2}-\d{2}$/),
  titulo: z.string().max(60),
  descripcion: z.string().max(300),
  efecto: z.enum(['positivo', 'negativo', 'neutro']),
  categoria: z.enum(['economico', 'politico', 'institucional', 'electoral', 'escandalo']),
  mostrar_en: z.array(z.enum(['aprobacion', 'icg', 'intencion_voto']))
});
```

Los 6 hitos del complemento CIGOB (veto jubilatorio, $LIBRA, acuerdo FMI, legislativas 2025, Adorni, piso aprobación mar-2026) se cargan como items iniciales.

### 3.5 Schema — Configuración del modelo

Archivo: `src/data/config/modelo.json`

```json
{
  "version": "2026.04.01",
  "lambda": 0.015,
  "sigma_primera_vuelta": 6.5,
  "sigma_ballotage_base": 4,
  "sigma_ballotage_anchor_dias": 90,
  "rho_lla_pj": -0.7,
  "simulaciones": 10000,
  "candidato_adj_lla": 4.0,
  "candidato_adj_pj": 2.0,
  "election_date": "2027-10-24",
  "peso_fundamentals_max": 0.50,
  "peso_fundamentals_anchor_dias": 1000,
  "cap_consultora_porcentaje": 0.20,
  "umbral_ballotage_probabilidad": 0.30
}
```

**Clave:** `umbral_ballotage_probabilidad` es nuevo — corresponde al feedback de Redlines ("ballotage como sección condicional"). Si `pMilei1 < 70%` (o sea, probabilidad de ballotage > 30%), se muestra el módulo. Parametrizable.

### 3.6 Schema — Textos editoriales (lo que Redlines edita)

Archivo: `src/data/config/copy.json`

```json
{
  "meta": {
    "titulo": "VOTÓMETRO ARGENTINA 2027",
    "subtitulo": "Fundación CIGOB & Redlines Estrategia y Comunicación"
  },
  "hero": {
    "kicker": "Edición mensual · Modelo predictivo electoral",
    "mes_dinamico": true
  },
  "primera_vuelta": {
    "escenario_art97": "Si LLA supera el 45%, gana en primera vuelta sin necesidad de ballotage.",
    "escenario_art98": "Con más del 40% y diferencia mayor a 10pp, LLA gana por Art. 98.",
    "escenario_ballotage": "Sin alcanzar ni 45% ni 40%+10pp, el escenario más probable es segunda vuelta."
  },
  "ballotage": {
    "mostrar": "condicional",
    "titulo": "Si hubiera segunda vuelta",
    "texto": "Los datos proyectan un escenario Milei vs. Kicillof. Transferencias: PRO ~85% a LLA, UCR/PU ~75% a LLA, FIT ~60% a PJ."
  },
  "disclaimer": "Este Votómetro no es una encuesta. Es un modelo estadístico que agrega encuestas públicas con ponderación por calidad y decaimiento temporal."
}
```

Todos los strings que hoy están dentro de template literals en el HTML pasan acá. El motor lee del JSON, Redlines edita sin tocar código.

---

## 4. Repositorio GitHub — estructura y flujo

### 4.1 Repositorio nuevo, nombre nuevo

**Acción inmediata:** crear `github.com/cigob-ar/votometro-2027` (organización propia CIGOB) o, si Redlines es co-autor formal, `github.com/redlines-cigob/votometro-2027`. El repo actual (`biblitotecario-ai`) queda para el bibliotecario IA. Separación limpia.

### 4.2 Estructura propuesta del repo

```
votometro-2027/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                  # lint + typecheck + validación de schemas
│   │   ├── deploy.yml              # build + deploy a Vercel
│   │   └── validate-pr.yml         # corre validaciones en cada PR
│   └── CODEOWNERS                  # ver sección 4.4
├── src/
│   ├── components/                 # componentes Astro reusables
│   │   ├── HeroBanner.astro
│   │   ├── ProbabilityCards.astro
│   │   ├── IntencionVoto.astro
│   │   ├── BallotageCondicional.astro
│   │   ├── AprobacionChart.astro
│   │   ├── MapaFederal.astro
│   │   └── TablaEncuestas.astro
│   ├── data/                       # JSON versionado (ver sección 3)
│   ├── lib/
│   │   ├── motor.ts                # calcPeso, mediaPonderada, MonteCarlo
│   │   ├── fundamentals.ts         # calcularPriorFundamentals
│   │   └── format.ts               # formatters, labels
│   ├── schemas/                    # Zod schemas
│   ├── pages/
│   │   └── index.astro             # página principal
│   └── styles/
│       └── votometro.css           # CSS actual extraído
├── scripts/
│   ├── agregar-encuesta.ts         # wrapper CLI — valida y commitea
│   ├── actualizar-fundamentals.ts  # pull de ICC, EMAE
│   └── migrar-html-actual.ts       # one-shot — corre una vez para extraer datos del HTML
├── tests/
│   ├── motor.test.ts               # snapshot de probabilidades conocidas
│   └── schemas.test.ts
├── docs/
│   ├── metodologia.md              # pública
│   ├── contribuir.md               # cómo agregar una encuesta
│   └── arquitectura.md             # este documento
├── astro.config.mjs
├── package.json
├── tsconfig.json
└── README.md
```

### 4.3 Branches

- `main` — producción. Deploy automático a dominio principal.
- `staging` — rama de integración. Deploy automático a subdominio `staging.votometro.cigob.org`.
- `feature/*` — ramas de trabajo. Deploy automático de preview (Vercel crea URL efímera por PR).

### 4.4 CODEOWNERS — quién aprueba qué

```
# .github/CODEOWNERS
# Motor metodológico — solo CIGOB aprueba
/src/lib/motor.ts               @cigob-team
/src/lib/fundamentals.ts        @cigob-team
/src/schemas/                   @cigob-team
/src/data/config/modelo.json    @cigob-team
/src/data/consultoras.json      @cigob-team

# Datos de encuestas — ambos pueden editar, revisión mutua
/src/data/encuestas/            @cigob-team @redlines-team
/src/data/fundamentals/         @cigob-team

# Contenido editorial — Redlines conduce, CIGOB revisa
/src/data/config/copy.json      @redlines-team
/src/data/eventos/              @redlines-team @cigob-team
/src/components/                @redlines-team @cigob-team
/src/styles/                    @redlines-team
```

### 4.5 Flujo de trabajo típico

**Redlines agrega un evento en el gráfico de aprobación:**
1. Desde GitHub web (sin clonar), editar `src/data/eventos/aprobacion.json`.
2. Crear pull request a `staging`.
3. GitHub Actions corre validación Zod + build.
4. Vercel genera URL de preview — Redlines ve el cambio en vivo.
5. CIGOB aprueba el PR (por CODEOWNERS).
6. Merge a `staging` → deploy a staging.
7. Merge de `staging` a `main` (semanal) → producción.

**CIGOB agrega una encuesta:**
1. `npm run agregar-encuesta` desde terminal (wrapper del script actual).
2. El script crea una rama, valida, commitea, abre PR.
3. GitHub Actions corre validación Zod.
4. Review por un segundo miembro del equipo.
5. Merge automático si CI pasa.

**CIGOB cambia σ o λ:**
1. Editar `src/data/config/modelo.json`.
2. Correr `npm test` — verifica que los tests de snapshot de probabilidades no cambien más de lo esperado.
3. PR con descripción del motivo del cambio.
4. Review obligatorio por segundo miembro CIGOB.
5. Merge.

---

## 5. Encuestas provinciales — punto estratégico

Esto es lo que diferencia al Votómetro en el contexto CIGOB: la brecha subnacional. Es donde CIGOB opera (provincias y municipios), y donde el resto del mercado no está. La activación del módulo provincial es probablemente **el hito más importante** del 2026 para el producto.

### 5.1 Criterios de activación (según complemento CIGOB)

- **Mapa federal de imagen:** ≥2 encuestas distintas con cobertura ≥15/24 distritos.
- **Sección gobernadores:** ≥3 encuestas por provincia en ≥8 de las 10 provincias mayores.

Hasta que no se cumplan, el módulo no se publica. Se construye en rama `feature/provinciales` con deploy a preview, pero no se mergea a `main`.

### 5.2 Fuentes de datos conocidas

| Fuente | Tipo | Cobertura | Costo |
|---|---|---|---|
| CB Global Data | Imagen presidencial georreferenciada | 24 distritos (ya usada, feb-2026, n=24.690) | Publicación en medios |
| Proyección Consultores | Intención de voto PBA + CABA | 2 distritos | Publicación |
| Reale Dalla Torre | PBA principalmente | 1-2 distritos | Privado |
| Delfos | PBA y federal | Variable | Publicación |
| Federico González | Santa Fe, Córdoba | 2-3 distritos | Publicación |
| Sondeos de medios provinciales (La Voz, El Litoral, El Día) | Intención local | 1 distrito c/u | Publicación |
| CIGOB (propio, proyectado) | A desarrollar con aliados subnacionales | TBD | Interno |

**Recomendación estratégica para CIGOB:** construir una red de consultoras provinciales aliadas que cedan datos crudos al Votómetro a cambio de atribución visible en el producto. Esa red sería una ventaja competitiva difícil de replicar y un activo institucional propio.

### 5.3 Dónde colocar cada archivo provincial

`src/data/encuestas/provinciales/buenos-aires.json`:

```json
{
  "provincia": "buenos-aires",
  "nombre": "Buenos Aires",
  "padron": 13200000,
  "encuestas": [
    {
      "fecha": "2026-02-15",
      "consultora": "Proyección",
      "tipo": "intencion_voto",
      "espacios": {
        "LLA": 38.5,
        "PJ": 41.2,
        "PRO": 6.1,
        "FIT": 7.0,
        "OTROS": 7.2
      },
      "muestra": 1200,
      "calidad": "B",
      "categoria_eleccion": "presidencial",
      "notas": "Encuesta de intención presidencial 2027 en PBA"
    }
  ],
  "actualizacion": "2026-04-13"
}
```

### 5.4 UI — cómo mostrar sin engañar

Mientras no haya 3 encuestas por provincia:
- Mostrar mapa "en construcción" con cobertura actual.
- Etiquetar provincias con insuficiente data como "en espera de datos".
- Nunca extrapolar — si no hay datos, el distrito queda en gris.

Cuando se active:
- Mapa coroplético con intención de voto del espacio líder.
- Tooltip por distrito con las 3 encuestas más recientes.
- Sección "Gobernadores" con candidatos conocidos y probabilidad de reelección (criterio CIGOB — requiere modelo separado).

---

## 6. Pipeline de actualización

### 6.1 Encuestas nacionales — semi-automático con revisión humana

**Flujo recomendado:**

1. Script `npm run agregar-encuesta -- --desde-url <url>` o modo interactivo.
2. El script (TypeScript) pide los campos, valida con Zod en vivo, muestra el peso calculado antes de commitear.
3. Crea una rama `add-encuesta/<consultora>-<fecha>`, hace commit firmado con metadata (quién, cuándo, de dónde).
4. Abre PR con plantilla pre-llenada.
5. Otra persona revisa (2 ojos).
6. Merge automático si CI pasa.

**Por qué no full automatic:** las encuestas tienen matices (fuente primaria vs secundaria, tipo espacio vs candidato, notas metodológicas) que requieren criterio humano. Scraping ciego genera basura.

### 6.2 Fundamentals — scraping agendado

Script `scripts/actualizar-fundamentals.ts` se corre como GitHub Action el día 5 y el día 25 de cada mes:

- **ICC Di Tella:** scraping de `www.utdt.edu/cif` (ya hay script Python reconstruido en `scripts/reconstruir_icc.py` — portar a TypeScript).
- **EMAE:** API del INDEC (hay endpoint JSON público).
- **Aprobación:** promedio de las últimas 3 encuestas de gestión (AtlasIntel, M&F, UdeSA) — extraído de `encuestas.json` automáticamente.

La action abre un PR con el update. Un humano lo aprueba. Merge.

### 6.3 Eventos — manual, editorial

No hay escala. Son 6-12 eventos por año. Redlines los edita en `src/data/eventos/aprobacion.json` desde GitHub web.

### 6.4 Encuestas provinciales — formulario web (Fase 2)

En Fase 2 (con Next.js), agregar una ruta `/admin/encuesta-provincial` con autenticación básica (password en env var, o magic link vía Clerk/Auth.js) donde Redlines carga encuestas sin tocar Git directamente. El formulario hace un commit automático al repo vía GitHub API. Staging automático.

### 6.5 Sobre el script Python actual

`scripts/actualizar_encuestas.py` se mantiene funcionando durante Fase 1 (compatibilidad). En Fase 1 se agrega un wrapper TypeScript que llama al mismo Python pero también valida contra Zod. En Fase 2 se deprecta el Python — queda todo en TypeScript.

---

## 7. Deploy y publicación

### 7.1 Recomendación: Vercel (en lugar de GitHub Pages)

**Razones:**

| Criterio | GitHub Pages | Vercel |
|---|---|---|
| Soporte Astro | Necesita action extra | Nativo |
| Preview por PR | No | Sí, URL única por PR |
| Dominio custom | Sí | Sí |
| Tiempo de build | 1-3 min | 30-60 seg |
| Analytics | Externo | Incluido |
| Rollback | Via revert de git | Un click en dashboard |
| Autenticación (Fase 2) | No | Sí, nativa |
| Edge functions (Fase 2) | No | Sí |
| Costo para este volumen | Gratis | Gratis (hobby tier) |

Vercel es gratis para este caso de uso (proyecto no-comercial, <100GB bandwidth/mes). El día que se quiera monetizar, se paga o se migra.

### 7.2 Dominio

Hoy: `juanpintoselso33.github.io/biblitotecario-ai/index.html` — no institucional, con typo. Recomendación:

- **Dominio propio:** `votometro.cigob.org` (subdominio del dominio institucional de CIGOB) o `votometro2027.com.ar`.
- **Staging:** `staging.votometro.cigob.org`.
- **Preview por PR:** Vercel genera automáticamente `votometro-<pr-number>.vercel.app`.

Si no hay dominio institucional CIGOB todavía, se puede comprar `votometro-argentina.com` o `votometro2027.ar` (~USD 15/año).

### 7.3 SEO y metadatos

Faltan hoy. Agregar en `src/pages/index.astro`:

```html
<meta property="og:title" content="Votómetro Argentina 2027" />
<meta property="og:description" content="Modelo predictivo electoral · 99 encuestas · Monte Carlo · Actualización mensual" />
<meta property="og:image" content="https://votometro.cigob.org/og-image.png" />
<meta property="og:url" content="https://votometro.cigob.org" />
<meta name="twitter:card" content="summary_large_image" />
<link rel="canonical" href="https://votometro.cigob.org" />
```

Generar `og-image.png` dinámico por mes (Astro lo soporta con `@vercel/og`).

### 7.4 Analytics

Plausible o Umami — no Google Analytics (privacidad, relevancia política). Ambos son gratis auto-hosteados o tienen hobby tier pago bajo (~USD 9/mes).

---

## 8. Priorización — qué hacer primero

### Fase 0 — Antes de migrar (esta semana)

Cosas que se pueden resolver sin cambiar stack, que destraban el resto:

1. **Separar repo.** Crear `votometro-2027` como repo propio. El bibliotecario IA queda en `biblitotecario-ai`.
2. **Congelar el HTML.** No editar más el archivo manualmente. Toda edición va por PR con reviewer.
3. **Incorporar feedback editorial obvio de Redlines** (al HTML actual, una sola vez):
   - Sacar nombres de candidatos en primera vuelta (dejar espacios).
   - Ocultar sección "Última Encuesta destacada" (punto 11 complemento CIGOB).
   - Ocultar sección "Comparativa 2023/2025/2027" (punto 12).
   - Mes dinámico en el hero (ya hay `Date()`, falta render).
   - Clarificar leyenda de colores (tooltip o label al lado).
4. **Conseguir 2-3 encuestas de ballotage adicionales** (post-caso Adorni). El 49%/35% actual está desactualizado (punto 7 complemento CIGOB).

### Fase 1 — Migración a Astro (2-3 semanas)

1. Scaffold de repo Astro.
2. Extraer encuestas, consultoras, config, copy a JSON.
3. Portar motor (`calcPeso`, `calcularPriorFundamentals`, Monte Carlo) a `src/lib/motor.ts` en TypeScript.
4. Componentizar el HTML en 8-10 componentes `.astro`.
5. Montar gráficos Chart.js como islas.
6. Setup CI (validación Zod + typecheck).
7. Deploy a Vercel con dominio nuevo.
8. Tests de snapshot del motor — el porcentaje de LLA con la misma data no debe cambiar entre versión actual y versión migrada (excepto variación de RNG seed esperada).
9. Migrar `actualizar_encuestas.py` a `agregar-encuesta.ts`.

### Fase 2 — Capacidades colaborativas (4-6 semanas)

1. Módulo de ballotage condicional (activación por umbral de probabilidad).
2. Anotaciones de eventos en el gráfico de aprobación.
3. Formulario web para que Redlines cargue encuestas sin tocar Git (con GitHub API).
4. Script de scraping de fundamentals agendado (GitHub Actions mensual).
5. OG image dinámica por mes.
6. Analytics (Plausible).

### Fase 3 — Encuestas provinciales (cuando haya data suficiente)

1. Schema y estructura de datos provinciales.
2. Componente de mapa coroplético (D3 o Leaflet).
3. Red de consultoras provinciales aliadas (trabajo institucional, no técnico).
4. Activación pública del módulo cuando se cumplan los criterios de cobertura.

### Fase 4 — Opcional / deseable

1. RSS o newsletter con updates semanales del Votómetro.
2. Export PDF del estado actual para reuniones.
3. API pública read-only (`/api/estado-actual.json`) para que medios y académicos citen.
4. Dashboard interno para CIGOB con serie histórica del modelo y tracking de performance.
5. Base de datos (Neon/Supabase) si los datos superan lo razonable para versionar en Git.

---

## 9. Decisiones

### Resueltas

- **ICC Di Tella:** solo referencia interna. No se muestra en la UI pública. Sigue siendo input del prior de fundamentals en el motor, pero la sección Valoración usa encuestas de `categoria: 'imagen'` de consultoras, no el ICC directamente.
- **Encuestas de ballotage:** array separado (`src/data/encuestas/ballotage.json`). Son elecciones distintas con lógica distinta — no van mezcladas con el array de intención de voto nacional.
- **Taxonomía de encuestas:** campo `categoria` + campo `tipo` como ejes ortogonales (ver sección 3.0).

### Pendientes (para conversar con Redlines)

1. **Nombre del repo y organización GitHub.** ¿Organización CIGOB propia? ¿Co-ownership con Redlines?
2. **Dominio.** ¿Subdominio institucional CIGOB o dominio propio del Votómetro?
3. **Atribución visual.** ¿Logo CIGOB + logo Redlines siempre presentes? ¿En qué proporción?
4. **Periodicidad de release.** ¿Rolling release (deploy por commit) o versiones mensuales (ej. "Votómetro abril 2026")?
5. **Umbral de activación del ballotage condicional.** ¿P(ballotage) > 30%? > 35%? > 40%?
6. **Criterio de activación del módulo provincial.** ¿≥3 encuestas por provincia y ≥8 de las top-10 jurisdicciones?
7. **Política de encuestas excluidas.** Hoy se pondera baja calidad/sesgo pero no se excluye nada. ¿Qué hacer con encuestas claramente no metodológicas?
8. **Licencia del código.** ¿MIT? ¿Custom (libre para leer, no redistribuir la data)? ¿Datos CC-BY?

---

## 10. Siguiente paso concreto

Propuesta de reunión Redlines + CIGOB con esta agenda:

1. Validar el diagnóstico técnico (sección 1).
2. Decidir stack — ¿Astro o alguna alternativa que Redlines prefiera?
3. Revisar división de responsabilidades del CODEOWNERS (sección 4.4) — ¿queda cómodo para ambos equipos?
4. Definir quién arranca Fase 0 (los cambios editoriales inmediatos al HTML actual) y quién Fase 1 (la migración).
5. Cerrar las decisiones pendientes (sección 9).
6. Timeline: objetivo realista de pasar a Astro a fines de mayo 2026, con los cambios editoriales de Fase 0 aplicados la próxima semana.

---

*Documento técnico producido por CIGOB para Redlines. Base del desarrollo colaborativo del Votómetro Argentina 2027.*
