# CIGOB — Requisitos técnicos para el desarrollo colaborativo del Votómetro
**Fecha:** 13 de abril de 2026  
**Destinatario:** Redlines Estrategia y Comunicación  
**Propósito:** Definir lo que hay que resolver para que el Votómetro pueda desarrollarse en conjunto, sostenerse editorialmente y crecer hacia datos subnacionales

---

## 1. El problema: un solo archivo hace todo

El Votómetro funciona como un único HTML de 2.200 líneas donde conviven el diseño, el motor estadístico, los datos de 99 encuestas, los parámetros del modelo y los textos editoriales. Cualquier edición simultánea de CIGOB y Redlines genera conflictos. No hay forma de que Redlines modifique un color o una frase sin entrar al mismo archivo donde vive la lógica del modelo.

Tres variables críticas están escritas como números fijos en el código y no se actualizan solas:

- **Aprobación presidencial:** 38% (marzo 2026)
- **Ballotage:** Milei 50% / Kicillof 33% (Trends, enero 2026 — pre-Adorni)
- **Índice Di Tella:** 42.03 (marzo 2026)

Para comparar: FiveThirtyEight (el referente mundial en agregación de encuestas) publica todos sus datos como archivos CSV/JSON en GitHub, separados del modelo. Su repositorio público tiene carpetas distintas para encuestas presidenciales, aprobación, favorabilidad y primarias. Cuando encontraron un bug en sus promedios en septiembre de 2024, lo documentaron públicamente y corrigieron los datos históricos sin tocar el modelo. Eso es posible porque los datos y el código están separados. El Votómetro hoy no puede hacer eso.

---

## 2. Lo que hay que cambiar

### 2.1 Repositorio propio

Hay que crear un repositorio dedicado exclusivamente al Votómetro, con acceso para ambos equipos y separación clara de responsabilidades:

- **CIGOB controla:** motor estadístico, parámetros del modelo, base de encuestas
- **Redlines controla:** textos, labels, colores, estructura visual

Esta separación se puede formalizar en el repositorio para que cada equipo edite su parte sin riesgo de romper la del otro.

### 2.2 Separar datos del código

Los datos tienen que salir del HTML y vivir como archivos independientes. Esto permite agregar una encuesta nueva sin tocar el motor, actualizar los fundamentals sin riesgo, y que Redlines edite los textos sin entrar al JavaScript.

### 2.3 Cambio de stack

La propuesta es **Next.js**, con exportación estática para la primera versión. Esto produce el mismo HTML de hoy (sin servidor, deployable en Vercel o GitHub Pages) pero con datos separados del código y validación en build time. Cuando el producto necesite API routes — carga de encuestas vía formulario, datos provinciales dinámicos, módulo de ballotage — se agregan sin cambiar de framework ni hacer una segunda migración. El Votómetro es un dashboard con gráficos interactivos; Next.js está diseñado para eso. Deploy nativo en Vercel, ecosistema React.

---

## 3. Tipos de encuesta: una distinción que hoy no existe

El Votómetro tiene 99 encuestas en un solo array. El campo `tipo` actual solo dice si la pregunta fue por espacio ("LLA") o por candidato ("Milei"), lo que afecta la corrección del motor. Pero no dice **qué está midiendo** cada encuesta.

La literatura de encuestas latinoamericanas (AMAI, IFE México, tribunales electorales) distingue formalmente al menos cinco tipos de medición con objetivos y estructuras distintas:

| Tipo | Qué mide | Uso en el Votómetro |
|---|---|---|
| **Intención de voto** | % estimado por espacio o candidato | Motor principal — proyección 1ra vuelta |
| **Ballotage** | % en segunda vuelta (head-to-head) | Módulo de segunda vuelta — separado |
| **Aprobación de gestión** | % que aprueba / desaprueba al gobierno | Prior de fundamentals |
| **Imagen** | Imagen positiva / negativa de dirigentes | Gráfico de valoración |
| **Distrital / gobernadores** | Intención de voto o imagen por provincia | Módulo subnacional (futuro) |

Hoy el motor hace suposiciones implícitas sobre cuáles son cuáles. La solución es un campo `categoria` que lo haga explícito, independiente del `tipo` de formulación que ya existe.

**Decisiones tomadas:**
- Las encuestas de ballotage van en un archivo separado. Son una elección distinta con lógica de cálculo distinta. El valor actual (50%/33%) es de enero 2026 — pre-Adorni. Hay que incorporar más encuestas de segunda vuelta recientes antes de publicar el módulo condicional.
- El array de ballotage necesita además un segundo componente: los **coeficientes de transferencia de voto** por espacio. El complemento de CIGOB (260412) identificó: PRO transfiere ~85% a LLA, UCR/Provincias Unidas ~75%, FIT ~15%. Sin estos coeficientes el modelo no puede simular correctamente la segunda vuelta — hoy están hardcodeados implícitamente en el motor.
- El ICC Di Tella sigue siendo input del motor interno pero **no aparece en la interfaz pública**. El gráfico de valoración usará encuestas de aprobación e imagen de consultoras.

**Un tipo de dato que no existe todavía — eventos políticos:**

El gráfico de aprobación de gestión necesita anotaciones de hitos para que la curva sea legible. Eso requiere un array de eventos con fecha y descripción corta, separado de las encuestas. Los hitos identificados hasta ahora:

| Fecha | Hito | Efecto en la curva |
|---|---|---|
| Ago 2024 | Veto presidencial a reforma jubilatoria | Caída — primer punto de inflexión |
| Feb 2025 | Escándalo $LIBRA | Caída marcada — mínimo del período |
| Abr 2025 | Acuerdo FMI + salida del cepo | Recuperación |
| Oct 2025 | Legislativas — LLA 40.66% | Pico de aprobación |
| Feb 2026 | Caso Adorni | Caída — segundo punto de inflexión |
| Mar 2026 | Piso histórico (~37-38%) | Mínimo actual |

Este array lo mantiene CIGOB (criterio político) y lo edita Redlines si necesita ajustar los labels para comunicación. Es un tipo de dato completamente nuevo que hoy no tiene lugar en el HTML.

---

## 4. Encuestas provinciales: el vacío más estratégico

La misión central de CIGOB es la gestión subnacional. El Votómetro tiene una sección de gobernadores que no está activa por falta de datos sistemáticos.

**Lo que existe hoy en Argentina:**

- **CB Global Data** es la fuente más completa para el nivel subnacional. Hace un estudio mensual de imagen de los 24 gobernadores con entre 892 y 1.179 casos por jurisdicción. Mide imagen positiva por provincia, no intención de voto. Su encuesta de abril 2026 (1 al 4 del mes) posicionó a Passalacqua (Misiones, 55.8%), Poggi (San Luis, 55.3%) y Sáenz (Salta, 55.1%) como los de mejor imagen; Quintela (La Rioja, 42.8%) en el último lugar.

- **Mercados & Estrategia** hace estudios provinciales bonaerenses (692 casos, margen ±3.73%). Su encuesta de nov-2025 sobre intención de voto 2027 en PBA da LLA 43.9% / PJ 32.6%.

- **Consultoras locales** (Reale Dalla Torre en Mendoza, PGD en la Patagonia, DC Consultores en La Plata) hacen estudios departamentales esporádicos para clientes privados o municipios. No publican sistemáticamente.

- **Trends** declara trabajar "en distintas provincias y con dirigentes locales" pero sin publicación regular.

**El problema real:** la cobertura provincial existe pero es fragmentada y no homologada. No hay un campo estándar para "partido provincial" (el Frente Renovador de Misiones no es comparable con LLA, y ambos compiten contra candidatos propios en sus distritos). Requiere una estructura de datos flexible, no campos fijos como los de la elección nacional.

**Criterio de activación propuesto:** mostrar la sección de gobernadores cuando haya al menos tres encuestas distintas con cobertura de ocho de las diez provincias más grandes por padrón (Buenos Aires, CABA, Córdoba, Santa Fe, Mendoza, Tucumán, Entre Ríos, Salta, Chaco, Misiones).

---

## 5. Pipeline de actualización

El Votómetro promete ser un termómetro actualizado. Para que esa promesa sea sostenible hay que resolver quién hace qué y cuándo:

| Dato | Frecuencia | Fuente disponible | Estado actual |
|---|---|---|---|
| Encuestas de intención de voto | Semanal / mensual | Múltiples consultoras | Manual — editar el HTML |
| Aprobación presidencial | Mensual | UdeSA, Haime, AtlasIntel, CB Global Data | Hardcodeado en 38% |
| ICC Di Tella | Mensual | UTDT (sitio público) | Hardcodeado en 42.03 |
| EMAE | Mensual con 2 meses de rezago | INDEC | Hardcodeado en 1.9% |
| Encuestas de ballotage | Esporádico | Trends, Isasi Burdman y otras | No incorporadas |
| Imagen de gobernadores | Mensual (CB Global Data) | cbglobaldata.com | No incorporadas |

El objetivo mínimo del desarrollo colaborativo es que **CIGOB pueda cargar una encuesta nueva sin tocar el motor** y que **los fundamentals se actualicen con un proceso documentado**. GitHub Actions permite automatizar la construcción y publicación del sitio cada vez que alguien agrega un dato — el mismo mecanismo que usa FiveThirtyEight para reflejar encuestas nuevas sin intervención manual en el código.

---

## 6. Decisiones pendientes

| Pregunta | Por qué importa |
|---|---|
| ¿Repo en organización CIGOB, Redlines, o compartida? | Define permisos y ownership del código |
| ¿Deploy en GitHub Pages o Vercel? | Vercel permite preview por rama — ver cambios antes de publicar |
| ¿Dominio propio o subdominio CIGOB? | `votometro.cigob.org` vs dominio independiente |
| ¿Rolling release o versiones mensuales etiquetadas? | Define cuándo se publica cada cambio |
| ¿Umbral para activar ballotage condicional? | A partir de qué probabilidad de segunda vuelta se muestra el módulo |
| ¿CMS para que Redlines cargue encuestas desde el navegador? | Alternativa a editar archivos JSON directamente |

---

## 7. Tres cosas que nadie mencionó y son importantes

### 7.0 El Votómetro no tiene competidor directo en Argentina

La búsqueda sistemática de agregadores de encuestas electorales argentinas no encontró ninguno. Los medios (Clarín, Perfil, Cronista, La Nación) citan encuestas individuales de consultoras. CELAG produce sus propias encuestas pero no agrega las de terceros. Poliarquía publica indicadores propios. Atlas Intel es una consultora brasileña con presencia local. Ninguno hace ponderación metodológica de múltiples encuestas con modelo explícito y publicación continua.

El Votómetro ocupa un nicho vacío en el ecosistema de información política argentina. Eso es un activo estratégico real, no una aspiración. El desarrollo colaborativo no apura al producto — lo consolida antes de que alguien más lo haga.

Sobre los derechos de los datos: reproducir el número de una encuesta pública (LLA: 41%) es análogo a citar un dato del INDEC o una cotización de Bolsa. La práctica es universal en medios y academia. No hay jurisprudencia argentina que lo restrinja para datos numéricos de encuestas publicadas por las propias consultoras.

---

### 7.1 La veda electoral es un requisito legal, no un detalle

El Código Nacional Electoral (Art. 71) prohíbe publicar y difundir encuestas y sondeos preelectorales desde **48 horas antes del inicio de los comicios hasta el cierre**. Las proyecciones sobre resultados solo pueden publicarse tres horas después del cierre. Las sanciones incluyen multas e inhabilitación para cargos públicos.

El Votómetro hoy no tiene ningún mecanismo para cumplir con esto. Si el sitio está publicado y activo el día antes de las elecciones, incumple la ley. Hay que incorporar un **modo de veda**: detectar automáticamente la ventana de 48 horas previa a cada comicio (PASO y elección general) y ocultar o reemplazar el contenido proyectivo por una pantalla neutra. Esto no es opcional.

### 7.2 Hay fuentes de datos oficiales que el Votómetro no usa

**DINE — API de Resultados Electorales** (`argentina.gob.ar/dine`): la Dirección Nacional Electoral tiene una API pública con resultados electorales históricos desde 2011, consultable por año, tipo de elección, distrito, sección, circuito y mesa. Está bajo licencia MIT. Esto permite dos cosas concretas:

- Alimentar automáticamente los puntos de "resultado real" en la serie histórica del Votómetro (2023 PASO, 2023 general, 2025 legislativas) sin carga manual.
- Comparar la proyección del modelo con el resultado oficial una vez cerrada cada elección — una funcionalidad de auditoría post-electoral que hoy no existe.

**Data CP** (`datacp.ar`): plataforma argentina de datos electorales abiertos con resultados presidenciales y legislativos desde 1983, descarga en CSV/Excel y GeoJSON por provincia y sección. Ya tiene construidas las comparativas por distrito que el Votómetro está intentando hacer a mano. Antes de reinventar esa capa, vale revisar si se puede consumir directamente.

---

*Documento producido por CIGOB para definir el alcance técnico del desarrollo colaborativo antes de la reunión con Redlines.*
