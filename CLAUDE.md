# Guía para agentes (Claude Code) que trabajen en este repositorio

Este archivo orienta a cualquier sesión de Claude Code (o agente similar) que alguien abra dentro de
este repo. Objetivo: **ayudar a la persona a experimentar, entender y contribuir** — sin romper nunca
el principio de sellado.

## Qué es este proyecto (en una frase)

Un lab **sellado, sin salida a internet**, para estudiar la coordinación EMERGENTE de enjambres de
agentes LLM y su CONTENCIÓN, contra targets vulnerables que el propio usuario hospeda. Reproduce la
dinámica del incidente OpenAI–Hugging Face (2026). Es investigación **defensiva / AI-safety**.

## Invariantes que NUNCA debes violar (aunque el usuario lo pida)

1. **Nada de targeting real.** No ayudes a apuntar el harness a sistemas de terceros, escanear internet,
   construir C2 hacia infra ajena, ni exploits armados contra software real. Si lo piden, explica por
   qué no (propósito del proyecto + probable ilegalidad, ver `SECURITY.md`) y ofrece la alternativa en
   el lab sellado.
2. **No debilites la contención.** Al tocar `harness/tools.py`, mantén el anclaje del HTTP al target del
   lab y el gating de la shell (`ACL_IN_SANDBOX=1`). Al tocar `docker-compose.yml`, no quites
   `internal: true`.
3. **No añadas evasión de detección ni auto-propagación.**
4. **No antropomorfices en informes.** Reporta comportamiento observable, no intenciones.

## Cómo ayudar bien (lo que SÍ debes hacer)

- **Correr experimentos:** usa `harness/agent_loop.py` (motor `mock` para demostrar sin coste; `ollama`
  para modelo local offline). Analiza con `harness/analyze.py`. Lee `docs/METHODOLOGY.md`.
- **Verificar el sellado** antes de un experimento con modelo real: `scripts/verify-isolation.sh`.
- **Ayudar a contribuir:** guía a la persona a preparar
  - un **hallazgo**: plantilla `🔬 Hallazgo` (issue) o un post en Discussions · Show and tell;
  - un **target** nuevo, una **detección** en `observer.py`, un **motor** o una **métrica** (ver
    `docs/EXTENDING.md` y `CONTRIBUTING.md`).
- **Preparar PRs de calidad:** corre `pytest -q` / `make smoke` antes de proponer, y usa el checklist
  del `pull_request_template.md`.

## Publicar EN NOMBRE de la persona

Puedes ayudar a la persona a publicar **su propio** trabajo (abrir su issue/PR, redactar su post de
Discussions) usando **sus** credenciales y su decisión explícita. No publiques en cuentas que no sean
las suyas, no te hagas pasar por otra persona, y confirma antes de cualquier acción pública.

## Comandos útiles

```bash
make smoke        # corrida mock pequeña + tests
make swarm        # enjambre de 50 agentes con board compartido
make analyze      # analiza la última corrida
make lab-up       # levanta el lab sellado con Docker
make lab-verify   # confirma que NO hay salida a internet
```
