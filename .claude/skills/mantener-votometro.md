# Skill: mantener-votometro

Proceso para actualizar, mantener y mejorar el Votómetro Argentina 2027.
Invocar cuando se pida agregar encuestas, actualizar datos o modificar el modelo.

---

## Estado actual del archivo

**Archivo:** `web/remixed-71df43cf.html` (~1779 líneas)
**Problema central:** datos, lógica y presentación están mezclados en un solo HTML.

---

## Dónde está cada cosa en el archivo

| Contenido | Líneas aprox. |
|---|---|
| CSS / estilos | 1–400 |
| HTML estructura | 400–900 |
| Metodología visible (cards) | 895–910 |
| Base de encuestas (JS array) | 1080–1350 |
| Lógica de ponderación / Monte Carlo | 1350–1600 |
| Gráficos Chart.js | 1600–1779 |

Para leer la base de encuestas:
```python
import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\Users\trico\OneDrive\UBA\Analisis CIGOB\web\remixed-71df43cf.html', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines[1079:1350], start=1080):
    if 'fecha' in line or 'consultora' in line or 'LLA' in line:
        print(f'{i}: {line}', end='')
```

---

## Proceso para agregar una encuesta nueva

### Paso 1: Identificar el bloque temporal correcto
Las encuestas están organizadas por mes con comentarios:
```javascript
// ── MAR 2026 ─────────────────────────────────────────────────────────
// [contexto político del período]
```

### Paso 2: Formato de entrada de datos
```javascript
{ fecha:'YYYY-MM-DD', consultora:'Nombre', LLA:XX.X, PJ:XX.X, PRO:X.X, PU:X.X, FIT:X.X, OTROS:XX.X, muestra:NNNN, tipo:'espacio', calidad:'A|B|C' },
```

**Campos:**
- `fecha`: ISO 8601
- `LLA`: La Libertad Avanza (Milei)
- `PJ`: Peronismo / kirchnerismo
- `PRO`: PRO / Macri
- `PU`: Provincias Unidas (Schiaretti)
- `FIT`: Frente de Izquierda
- `OTROS`: resto
- `muestra`: tamaño muestral
- `tipo`: `'espacio'` (por espacio político) o `'candidato'` (por candidato)
- `calidad`: track record de la consultora (`A`=alta, `B`=media, `C`=baja)

### Paso 3: Calidad de consultoras (referencia)
| Calidad | Consultoras |
|---|---|
| A | Proyección (Torcuato Di Tella), AtlasIntel, Opina Argentina |
| B | Management & Fit, D'Alessio IROL, Trends |
| C | Giacobbe, Poliarquía, CB Consultora, QSocial |

**Nota:** QSocial tiene sesgo pro-gobierno de ~5pp — el modelo lo corrige automáticamente.

### Paso 4: Agregar contexto político al comentario del período
Si hay un evento relevante en el período, agregarlo en el comentario del bloque mensual. Ayuda a la narrativa y al análisis posterior.

---

## Proceso para actualizar la proyección final

La proyección visible (primera vuelta, ballotage, Monte Carlo) se calcula en el JS a partir del array de encuestas. Si los datos están bien cargados, el modelo recalcula solo.

Para verificar que actualizó correctamente:
1. Abrir el HTML en un navegador
2. Revisar que la fecha "Proyección actualizada" en el hero refleja el período más reciente
3. Verificar que los números de primera vuelta son coherentes con las últimas encuestas

---

## Problemas conocidos y cómo manejarlos

| Problema | Workaround actual |
|---|---|
| Datos hardcodeados | Editar el array JS directamente — tedioso pero funciona |
| Sin fecha de última actualización automática | Actualizar manualmente la línea del hero que dice "Proyección actualizada · [mes año]" |
| Un solo escenario de ballotage | El modelo usa Trends ene-2026; actualizar si hay encuesta de 2ª vuelta más reciente |
| Nombres de encuestadoras inconsistentes | Mantener consistencia con el nombre exacto ya usado en el array |

---

## Roadmap técnico (pendiente)

**Corto plazo (antes de escalar):**
1. Separar la base de encuestas a un archivo `data/encuestas.json`
2. Cargar el JSON con `fetch()` en el HTML
3. Agregar línea visible "Última actualización: [fecha]" calculada desde los datos

**Mediano plazo:**
4. Script Python para validar encuestas nuevas antes de agregarlas
5. Múltiples escenarios de transferencia de voto en ballotage
6. Proyección distrital por provincia

**Largo plazo:**
7. Panel de administración simple para cargar encuestas sin editar código
8. API pública de los datos agregados
