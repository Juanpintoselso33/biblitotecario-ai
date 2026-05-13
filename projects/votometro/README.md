# Votómetro Argentina 2027

HTML estático puro para proyección electoral. Colaboración CIGOB + Redlines Estrategia y Comunicación.

## Archivos

| Archivo | Descripción |
|---|---|
| `web/votometro.html` | Versión activa — editar aquí |

## Cómo actualizar encuestas

Editar directamente `web/votometro.html`. Las encuestas están en el array `pollsData` al inicio del script.

> Ver `scripts/mantener-votometro` en `.claude/skills/` para el proceso completo de actualización.

## Deploy

GitHub Pages: `https://juanpintoselso33.github.io/biblitotecario-ai/`

Workflow: editar → commit → push `main` → deploy automático.

## Metodología

- Ponderación quíntuple: decaimiento temporal (λ=0.015) × calidad consultora × sesgo histórico × orientación del medio × metodología
- Monte Carlo: 10.000 simulaciones con σ=6.5 calibrado al error histórico argentino
- Corrección de voto oculto bayesiana
- Verificación Arts. 97-98 CN en cada simulación
- Prior de fundamentals con blend dinámico encuestas × prior estructural
