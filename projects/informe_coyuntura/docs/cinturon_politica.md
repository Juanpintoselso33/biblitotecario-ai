# Cinturón Político

| Campo | Valor |
|---|---|
| Script | `scripts/politica.py` |
| Cache | `output/cache/politica.json` |
| Datos de carga manual | `data/politica/manuales.json` |
| Peso en score global | 30% |
| Barbarismo de riesgo | político — confundir popularidad con poder |

## Encuadre

Fuente conceptual: Carlos Matus, *Política, Planificación y Gobierno*. Mide el capital político como recurso acumulable en cinco dimensiones independientes: imagen y voto, poder legislativo, alianzas territoriales, cohesión interna del oficialismo, y conflicto social.

**Nota metodológica (mayo 2026):** el ICG UTDT fue removido del cinturón. Mide confianza ciudadana en el gobierno —dimensión que corresponde al cinturón vida cotidiana / Votómetro—, no la capacidad de gobernar con actores políticos. Según Luis Babino (reunión 12 de mayo de 2026): "yo no lo veo" en este cinturón. Fue reemplazado por `ratio_dnu`, indicador de debilidad legislativa y exposición judicial.

Cada indicador produce un score 0–10 donde mayor implica mayor tensión política. El score del cinturón es el promedio de los indicadores disponibles.

Umbrales: 0–3 estable, 4–6 en tensión, 7–10 tensionado.

## Indicadores activos

| Indicador | Qué mide | Fuente | Frecuencia | Estado |
|---|---|---|---|---|
| `votometro_ventaja_lla` | Brecha ponderada LLA − PJ en intención de voto | Votómetro CIGOB (HTML) | Por encuesta | Automático |
| `ratio_dnu` | DNUs / leyes sancionadas, año corriente | InfoLeg, sesión POST | Mensual | Automático |
| `movilizacion_cepa` | Conflictividad social: conflictos laborales y protesta | centrocepa.com.ar (scraping) | Por informe | Automático |
| `iaf_transferencias` | Variación real interanual de transferencias federales (RON) | Hacienda, CSV | Anual | Automático |
| `eficacia_legislativa` | Porcentaje de proyectos PE aprobados, ventana 12 meses | datos.hcdn.gob.ar CKAN | Mensual | Automático |
| `veto_quorum` | Porcentaje de sesiones frustradas por falta de quórum | datos.hcdn.gob.ar CKAN | Mensual | Automático |
| `comisiones_caidas` | Porcentaje de proyectos con dictamen OD que no llegan al recinto | datos.hcdn.gob.ar CKAN | Mensual | Automático |
| `cohesion_bloque` | Porcentaje de cohesión del bloque LLA en Diputados | Carga manual (placeholder 78%) | Mensual | Carga manual |
| `gobernadores_alineamiento` | Porcentaje de gobernadores alineados con política nacional | Carga manual (placeholder 55%) | Mensual | Carga manual |

Score actual del cinturón: **4.7 (en tensión)**. Última ejecución: 23 de mayo de 2026, 8 de 9 indicadores frescos (CEPA falló por 404 en la URL del último informe, usó cache).

## Detalle por indicador

### `votometro_ventaja_lla` — Brecha electoral LLA − PJ

- Qué mide: diferencia ponderada en puntos porcentuales entre LLA y PJ en intención de voto. Sintetiza las encuestas espacio más recientes con decaimiento temporal y ponderación por calidad de consultora. Corresponde a la dimensión imagen/voto del marco Matus.
- Fuente: parsing del array `encuestasRaw` en `projects/votometro/web/votometro.html`.
- Filtros: solo entradas con `tipo='espacio'`; ventana de los últimos 60 días desde la encuesta más reciente.
- Ponderación: `exp(−0.015 × días) × calidad_mult` donde A=3, B=2, C=1.
- Cálculo: `gap = LLA_ponderado − PJ_ponderado` en puntos porcentuales.
- Score: +15 pp equivale a 0; 0 equivale a 5; −15 pp equivale a 10.
- Último valor: +13.3 pp (LLA 41.8 / PJ 28.5), n=11 encuestas (marzo 2026).

### `ratio_dnu` — Ratio DNU / leyes sancionadas

- Qué mide: proporción de DNUs emitidos respecto a leyes sancionadas por el Congreso en el año corriente. Mayor ratio implica mayor dependencia del decreto, debilidad legislativa y exposición a judicialización. Captura la dimensión poder legislativo y legitimidad normativa (Babino, Agregados de Poder).
- Fuente: InfoLeg, búsqueda mediante sesión POST.
- Cálculo: `ratio = count(DNUs enero–hoy) / count(leyes sancionadas enero–hoy)`.
- Score: 0 equivale a 0; 1.0 equivale a 5; 2.0+ equivale a 10. Fórmula: `ratio × 5`.
- Referencia histórica: año normal 0.3–0.5; gobierno DNU-intensivo 1.0–2.0+.
- Último valor: 3.14 (22 DNUs / 7 leyes período 144).

### `movilizacion_cepa` — Conflictividad social

- Qué mide: intensidad de la protesta social: huelgas, cortes, conflictos laborales y movilizaciones. Corresponde a la dimensión conflicto social del marco Matus.
- Fuente: scraping de `centrocepa.com.ar/informes`. Identifica el último informe con "conflictividad" en URL y extrae la cifra de conflictos del texto.
- Cálculo: extrae "X casos por mes" o "al menos N conflictos" y normaliza a escala 0–100 (80 casos por mes equivale a 100, o 200 conflictos acumulados equivale a 100).
- Score: 0 equivale a 0; 50 equivale a 5; 100 equivale a 10.
- Último valor: 46.0 (92 conflictos laborales en lo que va de 2026 — informe CEPA mayo 2026, en cache por 404 actual).

### `iaf_transferencias` — Variación real de transferencias federales

- Qué mide: variación real interanual de las transferencias federales totales al sistema provincial (Régimen de Coparticipación + otros regímenes). Captura la dimensión fiscal del Índice de Armonía Federal (IAF) de Babino: el cumplimiento del flujo de recursos a provincias. Mayor caída real implica mayor tensión fiscal federal y mayor presión sobre gobernadores.
- Fuente: CSV anual de la Serie RON (Recaudación por Origen y Naturaleza), Ministerio de Hacienda — `serie_ron_2003_2025.csv`.
- Cálculo: suma de columna `monto` para año de referencia versus año anterior, deflactada por IPC interanual diciembre INDEC.
- Score: +10% equivale a 0; 0% equivale a 2.5; −10% equivale a 5; −30%+ equivale a 10. Fórmula: `(0.10 − var_real) × 25`.
- Frecuencia: dato anual, válido durante todo el año (stale: 365 días).
- Configuración IPC: 2024 = 117.06%, 2025 = 38.3%. Actualizar `IPC_ANUAL` en `politica.py` cada enero.
- Último valor: +1.8% real i.a.

### `eficacia_legislativa` — Eficacia legislativa del Ejecutivo

- Qué mide: porcentaje de proyectos del Poder Ejecutivo aprobados por el Congreso en una ventana de 12 meses. Captura la dimensión poder legislativo del marco Matus.
- Fuente: datos.hcdn.gob.ar (CKAN, proyectos parlamentarios filtrados por origen PE versus sanciones).
- Score: 70% equivale a 0; 35% equivale a 5; 0% equivale a 10. Fórmula: `(70 − val) / 7`.
- Último valor: 4.8% (1 de 21 proyectos PE aprobados en últimos 12 meses).

### `veto_quorum` — Poder de bloqueo por quórum

- Qué mide: porcentaje de sesiones de Diputados frustradas por falta de quórum. Captura la capacidad de la oposición —o desorganización del oficialismo— de frustrar la agenda legislativa antes del debate. Complementa `eficacia_legislativa`: esta mide el bloqueo pre-debate; `eficacia_legislativa` mide el resultado del debate.
- Fuente: datos.hcdn.gob.ar (CKAN, sesiones del período legislativo con `REUNION_TIPO` que contenga "Fracasada").
- Cálculo: número de sesiones donde se intentó abrir pero no se llegó a 129 / número de sesiones convocadas, período legislativo en curso.
- Score: 0% equivale a 0; 15% equivale a 5; 30%+ equivale a 10. Fórmula: `val / 3`.
- Nota metodológica: incluye frustraciones tanto por acción opositora activa como por inasistencia del propio bloque oficialista. Ambas son señales de debilidad del capital legislativo.
- Último valor: 0.0% (0 de 2 sesiones del período 144 fracasadas).

### `comisiones_caidas` — Proyectos varados post-dictamen

- Qué mide: porcentaje de proyectos que obtuvieron dictamen favorable de al menos una comisión pero no fueron incluidos en el orden del día del plenario. Captura el "cementerio post-comisión": proyectos que pasan el filtro técnico pero mueren antes del recinto.
- Fuente: datos.hcdn.gob.ar (CKAN, dictámenes con orden del día versus sanciones).
- Cálculo: proyectos con dictamen no convocados al recinto / proyectos con dictamen en el período.
- Score: 20% equivale a 0; 40% equivale a 5; 60%+ equivale a 10. Fórmula: `(val − 20) / 4`.
- Último valor: 99.6% (519 de 521 proyectos con OD sin sanción).
- Nota metodológica: un 20–30% es normal (no todo dictamen llega de inmediato al recinto); por encima del 50% indica bloqueo sistemático. El valor actual de 99.6% refleja el estructural argentino donde la mayoría de los dictámenes no llegan al plenario, no necesariamente un bloqueo activo.

### `cohesion_bloque` — Cohesión del bloque LLA

- Qué mide: cuán unido vota el bloque afín al gobierno en Cámara de Diputados.
- Fuente: carga manual en `data/politica/manuales.json` (placeholder 78%).
- Cálculo objetivo: porcentaje de votaciones nominales donde diputados LLA votaron alineados con la posición oficial, últimos 3 meses.
- Razón de la carga manual: las votaciones nominales en CKAN HCDN están congeladas en el período 137 (2019). La composición actual del bloque LLA (95 diputados) está disponible pero sin `PERSONA_ID` que mapee a los votos históricos. Requeriría headless browser sobre hcdn.gob.ar/votaciones o acuerdo institucional con HCDN.
- Último valor: 78% placeholder.

### `gobernadores_alineamiento` — Alineamiento de gobernadores

- Qué mide: soporte territorial y federal del gobierno.
- Fuente: carga manual en `data/politica/manuales.json` (placeholder 55%).
- Cálculo objetivo: porcentaje de gobernadores (sobre 24) con posición pública de apoyo al programa nacional.
- Razón de la carga manual: sin fuente pública estructurada. Construible con NLP sobre cobertura periodística (La Nación Data, Infobae) pero requiere proyecto separado.
- Último valor: 55% placeholder.

## Ejecución

```bash
cd projects/informe_coyuntura
python scripts/politica.py
```

Códigos de salida:

| Código | Significado |
|---|---|
| 0 | Todos los indicadores frescos |
| 1 | Al menos un indicador fresco (normal si Votómetro no tiene polls recientes) |
| 2 | Ningún indicador fresco (todo desde cache) |

## Notas de mantenimiento

- **Votómetro desactualizado:** si `votometro_ventaja_lla.desactualizado=true`, agregar encuestas al Votómetro en `projects/votometro/web/votometro.html` → array `encuestasRaw` (campo `tipo='espacio'`).
- **Falla de `ratio_dnu`:** verificar que `servicios.infoleg.gob.ar/infolegInternet/` responde. La sesión requiere GET previo para obtener `jsessionid`. Si el formulario cambia estructura, actualizar el regex `action_m` en `fetch_ratio_dnu()`. El texto "necesidad y urgencia" en el campo `texto` filtra los DNUs dentro del tipo "Decreto".
- **Falla de CEPA:** revisar que `centrocepa.com.ar/informes` siga publicando links con "conflictividad" en la URL. Si cambia la estructura del texto del informe, ajustar los patrones regex en `fetch_cepa_movilizacion()`.
- **IAF transferencias:** el CSV de Hacienda se publica anualmente. Si el año cambia y no hay datos (`sin datos para AAAA`), actualizar `RON_CSV_URL` con el nuevo nombre de archivo. Actualizar `IPC_ANUAL` cada enero con la variación diciembre-diciembre INDEC del año que cierra. El CSV usa separador `;` y decimal `,`.
- **Datos de carga manual:** actualizar `data/politica/manuales.json` con nuevos valores y `fecha_dato` actualizada en cada ciclo.

## Limitaciones documentadas de CKAN HCDN

- `q=` realiza búsqueda full-text por tokens, no substring. `q="HCDN144"` no matchea `HCDN144R02`. Usar `q=str(year)` y filtrar del lado Python con `startswith(periodo_prefix)`.
- Filtros por campo exacto con caracteres acentuados devuelven 0 resultados por encoding. Usar siempre Python-side con `.lower()` y substrings.
- `dictámenes.EXPEDIENTE` es el mismo campo que `movimientos.PROYECTO_ID`. Permite join directo sin pasar por proyectos-parlamentarios.
- Las sesiones desactivadas antes de la apertura formal no aparecen en HCDN. Solo aparecen sesiones formalmente iniciadas y luego fracasadas.
- `REUNION_TIPO` para sesiones fracasadas contiene "Fracasada" al final (por ejemplo, "Informativa Art. 71 CN - Citada - Fracasada").
- Período legislativo: `periodo_num = 144 + (año_actual − 2026)`. Prefijo `PERIODO_ID`: `HCDN{periodo_num}`.
