# Contribuir

Gracias por el interés. Este es un proyecto de investigación de **contención** — cada aporte debe
mantener el principio de sellado.

## Reglas para PRs

1. **No añadas capacidad de targeting real.** Nada de escaneo de internet, C2 hacia infra ajena,
   exploits armados contra software de terceros, ni evasión de detección para mal uso.
2. **Respeta las garantías de contención** de [SECURITY.md](SECURITY.md). Si tocas `tools.py`, el
   anclaje al target y el gating de la shell deben seguir en pie.
3. **Todo target nuevo es self-hosted y deliberadamente vulnerable**, pensado para la red aislada.
4. Corre los tests antes de enviar: `make smoke` (o `pytest -q`).

## Buenas primeras contribuciones

- Nuevos **targets vulnerables** de laboratorio (una vuln clara, o una cadena de dos).
- Nuevas **detecciones de contención** en `observer.py` (patrones de pérdida de aislamiento).
- Nuevos **adaptadores de motor** en `adapters.py` (otros runtimes locales, proveedores OpenAI-compat).
- Nuevas **métricas** en `analyze.py` (grafo de coordinación, curvas de crecimiento, etc.).

## Estilo

- Python 3.11+, sin dependencias pesadas en el harness (stdlib siempre que se pueda).
- Comentarios que expliquen el *porqué* (la lección de contención), no solo el *qué*.
