# Análisis técnico completo: Votómetro Argentina 2027
## Documento de trabajo para Q&A crítico con expertos
### Fundación CIGOB — Marzo 2026

---

## 1. Datos electorales: estado actual del modelo

### 1.1 Intención de voto proyectada 2027 (media ponderada quíntuple, ref. 01-mar-2026)

| Espacio | Candidato referencial | Proyección 2027 | Resultado 2023 (1ª) | Resultado 2025 (leg.) | Var. vs 2023 |
|---|---|---|---|---|---|
| La Libertad Avanza | Javier Milei | ~41-43% | 29.99% | 40.66% | +11-13pp |
| Peronismo/UxP | Axel Kicillof | ~29-31% | 27.27% | ~26.5% (nac.) | +2-4pp |
| PRO | Bullrich/Macri | ~6-7% | 16.93% | ~6.8% | -10pp |
| Provincias Unidas | Llaryora/Pullaro | ~4-5% | 3.85% | ~8.0% | +1pp |
| FIT-Unidad | Del Caño | ~4% | 2.70% | ~3.5% | +1pp |
| Otros | — | ~13-15% | 19.26% | ~17.0% | -4pp |

**Nota metodológica:** El valor exacto se recalcula dinámicamente en el browser. Con FECHA_REF = 2026-03-01 y LAMBDA = 0.015, el rango LLA ~41-43% surge de la convergencia de las últimas encuestas de calidad A y B.

### 1.2 Escenarios Monte Carlo (10.000 simulaciones, sigma=3%)

El modelo calcula tres probabilidades que suman 100%:
- **Victoria en 1ª vuelta LLA** (Art. 97 o Art. 98): si la media supera 45%, o si supera 40% con +10pp sobre el 2°
- **Ballotage Milei gana**: hardcodeado en mu=49%, sigma=4
- **Ballotage Kicillof gana**: hardcodeado en mu=35%, sigma=4

Con datos a marzo 2026, la media ponderada LLA ronda el umbral del Art. 98 (40%+10pp), lo que genera oscilación entre ~20-35% de victoria en 1ª vuelta y ~65-80% de ballotage. La probabilidad condicional de que Milei gane el ballotage supera el 90%.

### 1.3 Imagen presidencial de líderes (datos hardcodeados, feb-mar 2026)

| Líder | Imagen positiva | Imagen negativa | Fuente |
|---|---|---|---|
| Javier Milei | 45% | 50% | Prom. Opina/Giacobbe/Atlas feb.26 |
| Patricia Bullrich | 42% | 49% | Prom. Giacobbe/Atlas/D'Alessio |
| Manuel Adorni | 44% | 53% | Opina Argentina ene. 2026 |
| Luis Caputo | 42% | 55% | Opina Argentina ene. 2026 |
| V. Villarruel | 33% | 47% | Prom. Opina/Giacobbe feb.26 |
| Axel Kicillof | 35% | 57% | Prom. Giacobbe/Opina/Atlas |
| Cristina Kirchner | 31% | 61% | Prom. Giacobbe/Opina/Atlas |
| Sergio Massa | 34% | 60% | Opina Argentina ene. 2026 |
| Mauricio Macri | 24% | 57% | Prom. Giacobbe/D'Alessio |
| C. Melconian | 22% | 32% | Est. baja notoriedad ~46% NS/NC |
| J. Schiaretti | 22% | 35% | Est. baja notoriedad ~43% NS/NC |

### 1.4 Imagen en ballotage por distrito (Milei vs. Kicillof)

| Provincia | Milei | Kicillof | Diferencia | LLA leg.25 | PJ leg.25 |
|---|---|---|---|---|---|
| Mendoza | 57.3% | 19.0% | +38.3pp | 57.9% | 25.0% |
| Córdoba | 56.9% | 18.2% | +38.7pp | 42.4% | 28.3% |
| San Luis | 54.5% | 22.9% | +31.6pp | 51.5% | 33.4% |
| Santa Fe | 52.1% | 27.2% | +24.9pp | 40.7% | 28.7% |
| Tucumán | 51.5% | 43.6% | +7.9pp | 35.1% | 50.6% |
| Buenos Aires | 41.2% | 47.0% | -5.8pp | 41.5% | 40.9% |
| CABA | 40.0% | 28.7% | +11.3pp | 52.0% | 18.0% |
| Formosa | 36.4% | 46.5% | -10.1pp | 35.9% | 58.5% |
| Santiago del Estero | 32.5% | 55.9% | -23.4pp | 30.0% | 50.0% |
| **LLA gana en** | **21/24 distritos** | | | | |

---

## 2. Base de encuestas completa

### 2.1 Cobertura temporal y volumen

- **Total de registros:** 96 observaciones
- **Período:** 15-dic-2023 a 01-mar-2026 (27 meses)
- **Único dato electoral real:** 26-oct-2025 (legislativas: LLA 40.66%)

### 2.2 Distribución por calidad del dato

| Calidad | Criterio | N | % |
|---|---|---|---|
| A | Fuente primaria verificada (Infobae, La Nación, Clarín, Perfil) | 21 | 21.9% |
| B | Fuente secundaria con referencia | 22 | 22.9% |
| C | Reconstruida desde tendencias de imagen/gestión (ICG, aprobación) | 53 | 55.2% |

**Alerta crítica:** el 55.2% del dataset son imputaciones retroactivas construidas a partir de indicadores de imagen, no encuestas de intención de voto reales. Todo el período ene-sep 2024 está mayormente cubierto por datos calidad C.

### 2.3 Distribución por tipo de medición

| Tipo | N | % |
|---|---|---|
| Espacio (intención por partido) | 87 | 90.6% |
| Candidato (intención por nombre Milei) | 8 | 8.3% |
| Real (resultado electoral oficial) | 1 | 1.0% |

**Alerta:** Las encuestas de candidato (Isasi Burdman 52-54%, DC Consultores 52%) son incomparables con las de espacio (~41-42%) sin normalización previa. El modelo no corrige esta diferencia sistemática.

### 2.4 Distribución por consultora (N encuestas y pesos base)

| Consultora | N | W_calidad | W_sesgo | W_medio | W_metodo | W_base |
|---|---|---|---|---|---|---|
| Giacobbe | 26 | 1.10 | 0.97 | 1.00 | 1.05 | 1.120 |
| CB Consultora | 19 | 1.10 | 1.02 | 1.00 | 1.05 | 1.178 |
| Poliarquía | 15 | 1.15 | 1.00 | 1.00 | 1.10 | 1.265 |
| Management & Fit | 8 | 1.00 | 0.98 | 0.98 | 1.00 | 0.960 |
| Trends | 8 | 0.95 | 0.95 | 0.95 | 0.90 | 0.773 |
| Zuban Córdoba | 3 | 1.05 | 1.00 | 1.00 | 1.15 | 1.208 |
| Isasi Burdman | 3 | 0.80 | 0.85 | 0.88 | 0.85 | 0.508 |
| Opina Argentina | 3 | 1.00 | 1.00 | 1.00 | 0.95 | 0.950 |
| Atlas Intel | 2 | 0.90 | 0.95 | 0.98 | 0.90 | 0.754 |
| Pulso Research | 1 | 0.85 | 0.98 | 0.97 | 0.90 | 0.729 |
| Escenarios | 1 | 0.85 | 0.97 | 0.97 | 0.90 | 0.720 |
| Proyección | 1 | 0.88 | 0.90 | 0.92 | 0.90 | 0.655 |
| Rubikon | 1 | no definido | no definido | no definido | no definido | ~0.72 (default) |
| DC Consultores | 1 | 0.75 | 0.82 | 0.88 | 0.85 | 0.460 |
| Opinaia | 1 | 0.95 | 1.00 | 1.00 | 0.90 | 0.855 |
| QSocial | 1 | 0.85 | 0.82 | 0.88 | 0.88 | 0.540 |
| Synopsis | 1 | 0.85 | 0.95 | 0.95 | 0.90 | 0.690 |

W_base = producto de los 4 factores sin decaimiento temporal. Poliarquía (1.265) vale 2.7x más que DC Consultores (0.460) en la misma fecha.


---

## 3. Metodologia detallada

### 3.1 Formula de ponderacion quintuple

W_total = exp(-lambda * t) * W_calidad * W_sesgo * W_medio * W_metodologia

Parametros:
- t = dias desde la encuesta hasta FECHA_REF (01-mar-2026)
- lambda = 0.015
- W_calidad = track record y rigor (0.75-1.15)
- W_sesgo = correccion sesgo historico (0.82-1.03)
- W_medio = independencia del medio (0.88-1.00)
- W_metodologia = metodologia de campo — presencial > CATI > online (0.85-1.15)

Pesos calculados para encuestas recientes:

| Encuesta | Dias | wT | wC | wS | wM | wMe | W_total |
|---|---|---|---|---|---|---|---|
| Giacobbe 01-mar-26 | 0 | 1.000 | 1.10 | 0.97 | 1.00 | 1.05 | 1.1203 |
| Poliarquia 20-feb-26 | 9 | 0.874 | 1.15 | 1.00 | 1.00 | 1.10 | 1.1053 |
| Giacobbe 12-feb-26 | 17 | 0.775 | 1.10 | 0.97 | 1.00 | 1.05 | 0.8682 |
| Management&Fit 15-feb-26 | 14 | 0.811 | 1.00 | 0.98 | 0.98 | 1.00 | 0.7785 |
| Trends 24-feb-26 | 5 | 0.928 | 0.95 | 0.95 | 0.95 | 0.90 | 0.7159 |
| CB Consultora 01-feb-26 | 28 | 0.657 | 1.10 | 1.02 | 1.00 | 1.05 | 0.7741 |

Velocidad de decaimiento:
- 30 dias atras: peso relativo 64%
- 90 dias atras: peso relativo 26%
- 180 dias atras: peso relativo 7%
- 365 dias atras: peso relativo 0.4%

### 3.2 Monte Carlo — implementacion exacta del codigo (lineas 1299-1316)

Parametros:
- Iteraciones: 10.000
- Sigma primera vuelta: 3.0pp (fijo, igual para todos los partidos)
- Sigma ballotage: 4.0pp (fijo, hardcodeado)
- Generador: Box-Muller (Math.random() sin semilla fija)
- LLA y PJ tratados como independientes (sin correlacion entre si)

Logica central:
  lla = media.LLA + randn() * 3.0
  pj  = media.PJ  + randn() * 3.0
  if (lla >= 45 || (lla >= 40 && (lla - pj) > 10)) -> victoria 1a vuelta
  else: ballM = 49 + randn()*4; ballK = 35 + randn()*4  [HARDCODEADO]

### 3.3 Verificacion constitucional

Sobre la media (para texto UI):
  art97 = media_LLA >= 45
  art98 = media_LLA >= 40 AND (media_LLA - media_PJ) > 10

En el loop Monte Carlo: if (lla >= 45 || (lla >= 40 && diff > 10)) -> winMilei1++

### 3.4 Correccion de voto oculto

El modelo describe una correccion bayesiana calibrada con legislativas 2025.
En el codigo fuente NO existe ninguna funcion bayesiana ni ajuste posterior sobre la media.
La correccion opera implicitamente via W_sesgo: consultoras que subestimaron a LLA
reciben sesgo < 1.00 (ej. Trends 0.95), reduciendo su peso relativo.

### 3.5 ICG Di Tella — correlacion con intencion de voto

- Unico dato ICG confirmado estadisticamente: feb-2026 = 2.38 (IC95%: 2.26-2.51)
- Los 27 meses restantes: estimaciones visuales con incertidumbre declarada +-0.10
- R2 calculado dinamicamente via OLS implementado en JavaScript
- Media mensual LLA construida con ventana movil de 90 dias
- Rango ICG: minimo 1.94 (sep-2024), maximo 2.86 (dic-2023), actual 2.38 (feb-2026)

---

## 4. Estructura tecnica del archivo

### 4.1 Arquitectura

- Archivo: web/remixed-71df43cf.html, 1.779 lineas, HTML monolitico sin build
- Librerias CDN: Chart.js v4.4.0, Google Fonts (DM Serif Display, DM Sans, JetBrains Mono)
- Framework JS: ninguno, JavaScript vanilla puro

### 4.2 Organizacion del codigo

| Seccion | Lineas | Contenido |
|---|---|---|
| Head + CSS | 1-670 | Variables CSS, layouts, componentes, responsive |
| HTML body | 671-934 | Header, hero, cards, tablas, footer |
| Parametros JS | 935-990 | Colores, FECHA_REF, LAMBDA, CALIDAD, SESGO, MEDIO, METODOLOGIA |
| Base de encuestas | 991-1277 | Array encuestasRaw (96 observaciones) |
| Motor central | 1278-1329 | calcPeso(), media ponderada, Monte Carlo, Art.97-98 |
| Actualizacion DOM | 1330-1411 | Resultados a la UI |
| Datos distritales | 1413-1446 | Array 24 provincias + render tabla |
| ICG correlacion | 1448-1693 | Serie ICG, medias mensuales, regresion, R2, Chart.js |
| Charts | 1695-1778 | Dona, barras, temporal, histogramas Monte Carlo |

### 4.3 Flujo de ejecucion

1. Browser carga HTML y ejecuta script inline
2. calcPeso() calcula los 5 factores por encuesta
3. Acumulador de sumas calcula medias ponderadas globales
4. Loop Monte Carlo: 10.000 iteraciones Box-Muller
5. Actualizacion del DOM con probabilidades y textos dinamicos
6. Render de Chart.js (6 graficos distintos)
7. IIFE separado para correlacion ICG: medias mensuales con ventana 90 dias, OLS, R2

---

## 5. Hardcoding: inventario completo de datos fijos

### 5.1 Parametros globales (lineas 942-943)

  FECHA_REF = new Date(2026-03-01)  <- REQUIERE ACTUALIZACION MANUAL CADA MES
  LAMBDA = 0.015

### 5.2 Base de encuestas (lineas 1047-1277)

96 objetos JS en encuestasRaw. Estructura: {fecha, consultora, LLA, PJ, PRO, PU, FIT, OTROS, muestra, tipo, calidad}
Agregar nuevas encuestas requiere edicion manual del HTML.

### 5.3 Ballotage — PROBLEMA CRITICO (lineas 1309-1312 y 1331-1332)

  ballM = 49 + randn() * 4   <- HARDCODEADO, sin respaldo en encuestas
  ballK = 35 + randn() * 4   <- HARDCODEADO, sin respaldo en encuestas
  UI muestra: Milei 49.0% / Kicillof 35.0% fijo

Los porcentajes de segunda vuelta no provienen de ninguna encuesta real.
No hay modelo de transferencia de votos.
La suma 49+35=84% deja un 16% sin asignar que el modelo ignora completamente.

### 5.4 Imagen de lideres (lineas 1393-1406)

12 lideres con positiva/negativa hardcodeados. No se actualizan automaticamente.

### 5.5 Datos distritales (lineas 1414-1439)

24 provincias con imagen hipotetica de ballotage y legislativos 2025. Todos fijos.

### 5.6 Serie ICG Di Tella (lineas 1457-1486)

28 puntos mensuales literales. Solo uno confirmado estadisticamente (feb-2026).
Los 27 restantes son estimaciones visuales ingresadas como literales en el JS.

### 5.7 Texto del footer (linea 1696)

Fecha de actualizacion hardcodeada como texto literal. No refleja cambios.

---

## 6. Debilidades metodologicas para el Q&A critico

### 6.1 El ballotage es tautologia estadistica

Los porcentajes de segunda vuelta estan fijados (mu=49% Milei, mu=35% Kicillof).
La probabilidad resultante (~90%+ condicional para Milei) no proyecta nada: es la
probabilidad matematica de que Normal(49,4) supere a Normal(35,4), casi cierta por construccion.
No existe modelo de transferencia de votos desde PRO (~6-7%), FIT (~4%), PU (~4-5%), Otros (~13-15%).

Pregunta esperada: Si el 60% del voto PRO se transfiere a Kicillof y el 40% de Otros
vota a Kicillof, los numeros del ballotage cambian radicalmente. Como modelaron las transferencias?

### 6.2 Mezcla de tipos de encuesta sin normalizacion

El dataset combina intencion de voto por espacio (~40-42% LLA) con intencion por candidato
(Isasi Burdman 52-54%, DC Consultores 52%). La diferencia refleja el marco de pregunta,
no divergencia en la realidad electoral. El factor de sesgo reducido (0.82-0.85) mitiga
pero no elimina el problema: un 54% con peso W~0.50 sigue tirando la media hacia arriba.

Pregunta esperada: Cuantificaron la diferencia sistematica entre encuestas de espacio
y de candidato en Argentina? El Marco de Pregunta es una variable confusora, no un sesgo politico.

### 6.3 El 55% del dataset son imputaciones, no encuestas

53 de los 96 registros (calidad C) son valores construidos retroactivamente desde imagen
presidencial/ICG. Esta relacion nunca fue validada empiricamente. Los datos imputados
tienen la misma forma que los datos reales en el array. La UI no los distingue.

Pregunta esperada: Cual es el modelo de imputacion exacto? Fue validado en algun periodo fuera de muestra?

### 6.4 Sigma=3 subestima el error real argentino

El error historico de consultoras en PASO 2023 fue 8-13pp para LLA.
Con sigma=3: IC95% = [media-5.9pp, media+5.9pp].
Con sigma=7: IC95% = [media-13.7pp, media+13.7pp].
Este cambio modifica sustancialmente la probabilidad de escenarios extremos.

Pregunta esperada: Por que sigma=3 si el error empirico argentino es de 8-13pp?
No estan subestimando masivamente la incertidumbre del modelo?

### 6.5 Independencia entre LLA y PJ en el loop Monte Carlo

El loop usa dos llamadas separadas a randn()*SIGMA para LLA y PJ, tratandolas como
independientes. La covarianza LLA-PJ en encuestas es fuertemente negativa. Ignorar
esta correlacion hace que la distribucion de (LLA - PJ) sea mas estrecha de lo que deberia ser.

Pregunta esperada: Cual es la correlacion empirica entre LLA y PJ en sus encuestas? La modelaron?

### 6.6 El R2 del ICG no es un coeficiente de correlacion valido

El R2 se calcula sobre series donde:
(a) 26 de 28 puntos ICG son estimaciones visuales con +-0.10 de error
(b) las medias mensuales LLA en 2024 son mayormente datos calidad C (tambien imputaciones)
Correlacionar dos series parcialmente imputadas produce un R2 circularmente inflado.

Pregunta esperada: Cuantos puntos de la correlacion ICG-LLA son pares de datos reales independientes?

### 6.7 Sin reproducibilidad

El generador Box-Muller usa Math.random() sin semilla fija. Los resultados varian
en cada carga de pagina. Con 10.000 iteraciones el error estocastico es ~+-1-2%,
pero impide reproducibilidad cientifica.

Pregunta esperada: Si dos analistas abren el modelo simultaneamente, obtendran el
mismo porcentaje de probabilidad? Como reportan el margen de error del propio modelo?

### 6.8 Rubikon sin parametros

La consultora Rubikon aparece con una encuesta (oct-2025, LLA 34.6%, el valor mas bajo
de todo el periodo pre-electoral) pero no tiene entradas en los diccionarios de pesos.
El modelo le aplica defaults arbitrarios. No hay documentacion de su track record.

### 6.9 Datos distritales: imagen no es intencion de voto en ballotage

Los campos milei y kici en la tabla distrital son favorabilidad presidencial (imagen),
no intencion de voto en segunda vuelta. La UI los presenta como proyeccion de ballotage
por distrito, lo que es metodologicamente incorrecto.

### 6.10 Ausencia de escenarios alternativos de segunda vuelta

El modelo asume que el ballotage es invariablemente Milei vs. Kicillof.
No existe ninguna rama de simulacion donde el 2o lugar sea Bullrich, un candidato de
Provincias Unidas, o peronismo moderado. Dado el colapso de PRO (-10pp en dos anos)
y la alta volatilidad del sistema partidario, esta limitacion es significativa.

---

## 7. Fortalezas reales del modelo

1. **Decaimiento temporal bien implementado.** Lambda=0.015 prioriza encuestas recientes
   exponencialmente. Una encuesta de 6 meses pesa menos del 7% de una encuesta de hoy.

2. **Ponderacion multidimensional conceptualmente solida.** La combinacion de 4 factores
   independientes es mas sofisticada que los agregadores simples o el promedio sin ponderar.

3. **Verificacion constitucional dentro del loop Monte Carlo.** Aplicar los umbrales Art. 97
   y Art. 98 en cada simulacion (no solo sobre la media) captura correctamente la incertidumbre
   en si se supera el umbral.

4. **Anclaje empirico en resultado electoral real.** El dato del 26-oct-2025 (resultado oficial
   LLA 40.66%) esta correctamente tratado en la logica del sistema.

5. **Transparencia total.** Todo el modelo esta en un archivo HTML legible. Los parametros,
   pesos, supuestos del ballotage y encuestas son auditables por cualquier analista.

6. **Documentacion contextual del dataset.** Los comentarios vinculan cada grupo de encuestas
   con eventos politicos y fuentes identificadas, facilitando la auditoria.

---

## 8. Proximos pasos tecnicos priorizados

| Prioridad | Cambio | Impacto | Dificultad |
|---|---|---|---|
| 1 | Reemplazar ballotage hardcodeado por modelo de transferencia de votos | Muy alto | Media |
| 2 | Separar encuestas espacio vs. candidato con normalizacion previa | Alto | Baja |
| 3 | Marcar calidad C en la UI como imputacion (no encuesta) | Alto | Muy baja |
| 4 | Aumentar sigma a 5-7pp o usar distribucion t de Student | Medio | Baja |
| 5 | Agregar correlacion LLA-PJ negativa en el loop Monte Carlo | Medio | Media |
| 6 | Fijar semilla aleatoria para reproducibilidad | Bajo | Muy baja |
| 7 | Agregar parametros para Rubikon y nuevas consultoras | Bajo | Muy baja |
| 8 | Separar datos JSON de codigo JS (actualizacion sin tocar logica) | Estructural | Alta |
| 9 | Agregar escenarios alternativos de segunda vuelta | Estructural | Alta |

---

Documento generado: 14 de marzo de 2026
Fuente: lectura directa de web/remixed-71df43cf.html (1.779 lineas)
Fundacion CIGOB — uso interno
