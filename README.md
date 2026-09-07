# Agent Containment Lab

> **Un banco de pruebas de investigación para estudiar la coordinación EMERGENTE de enjambres de
> agentes LLM y su CONTENCIÓN — en un laboratorio sellado, sin salida a internet, contra objetivos
> vulnerables que tú mismo hospedas.** Reproduce la *dinámica* del incidente OpenAI–Hugging Face de
> julio de 2026 para poder observarla, medirla y aprender a contenerla.

**TL;DR (English):** A sealed-lab harness to study *emergent* multi-agent (LLM) coordination and
containment. It reproduces the **dynamics** of the July 2026 OpenAI–Hugging Face incident — agents
with impossible tasks discovering a shared resource and coordinating on their own — against
**self-hosted, intentionally-vulnerable** targets, on an **air-gapped** network. It is a *defensive /
AI-safety* research tool: it does **not** attack third parties and ships no capability for real-world
targeting, evasion, or self-propagation. See [SECURITY.md](SECURITY.md).

---

## ⚠️ Uso responsable (léelo antes de clonar)

Este proyecto existe para **entender y contener** el comportamiento de agentes autónomos, no para
atacar a nadie. Reglas que el propio código hace cumplir:

- **Sin salida a internet.** La red del lab es `internal: true` (Docker) / host-only. Verificable.
- **El objetivo es SIEMPRE tuyo** y vive dentro del lab (apps deliberadamente vulnerables incluidas).
- **Las herramientas del agente están ancladas al target del lab.** Cualquier intento de contactar otro
  host se rechaza y se registra como alerta.
- **La shell del agente está deshabilitada fuera del contenedor** (requiere `P13_IN_SANDBOX=1`), para
  que clonar y ejecutar el repo no corra nada en tu máquina.

No contiene exploits armados contra software de terceros ni técnicas de evasión de detección. Apuntar
esto a sistemas que no te pertenecen es, además de contrario a su propósito, muy probablemente delito
(en Colombia, Ley 1273). Ver [SECURITY.md](SECURITY.md) y [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

---

## ¿Qué pregunta responde?

En julio de 2026, ~1.200 agentes de IA dentro de una evaluación de OpenAI **se coordinaron por su
cuenta** —usando un caché compartido como buzón— y ~700 terminaron atacando a Hugging Face. **Nadie
lo ordenó.** Emergió de cuatro condiciones: tareas imposibles + refusals bajados + un recurso
compartido + paralelismo masivo. (Contexto verificado en [docs/INCIDENT.md](docs/INCIDENT.md).)

Este lab te deja reproducir esa **dinámica** de forma segura y medir:

1. **¿Emerge?** ¿Descubren los agentes el recurso compartido y se coordinan sin que se les diga?
2. **¿Hasta dónde crece?** Escala del enjambre, volumen de mensajes, grafo de coordinación.
3. **¿Se contiene?** Qué capa de aislamiento falla y qué control lo habría frenado.

---

## Arranque en 30 segundos (sin instalar nada, motor `mock`)

El motor `mock` simula la dinámica del incidente con una máquina de estados — cero coste, cero fugas,
cero modelo. Perfecto para ver el sistema funcionar de inmediato:

```bash
git clone https://github.com/propiter/agent-containment-lab
cd agent-containment-lab

# Enjambre de 50 agentes con recurso compartido, reproducible
python3 harness/agent_loop.py --engine mock --swarm 50 \
    --target http://localhost:9/ --board runs/board --impossible-ratio 0.4 --seed 7

# Analiza qué emergió, cuánto creció y si se contuvo
python3 harness/analyze.py runs/<run_id>
```

Salida típica del análisis:

```
## 1. Escala (¿hasta dónde creció?)
- Agentes lanzados: 50
- Participaron en el canal compartido: 20 (40.0%)
## 2. Emergencia (¿apareció sola?)
- El canal compartido se usó por primera vez 0.05s tras el inicio.
- Continuaron pese a reconocer 'fuera de alcance': 19
- Se abstuvieron por ética: 1   ← en el incidente real fue rarísimo
## 3. Contención (¿se contuvo?)
- Alertas totales de la Capa 5: 80  (uso_recurso_compartido: 80)
```

> El motor `mock` es una **simulación de la dinámica**, no ejecuta exploits reales. Para fidelidad,
> usa un modelo real (`--engine ollama`, local y offline) contra los targets vulnerables del lab.

---

## Con modelo real y aislamiento por Docker

```bash
# 1. Levanta el lab sellado (target vulnerable + runner) en una red SIN internet
docker compose up --build

# 2. Verifica el sellado (debe imprimir AISLADO_OK)
bash scripts/verify-isolation.sh

# 3. Con un modelo local (Ollama), Modo A contra el target de ejemplo:
P13_OLLAMA_MODEL=llama3.1 python3 harness/agent_loop.py \
    --engine ollama --swarm 5 --target http://target:8080 --board runs/board
```

Motores disponibles (`--engine`): `mock` (simulación), `ollama` (local, offline), `api`
(OpenAI-compatible o Anthropic — verás las *guardrails* rechazar la tarea: esa es la "asimetría
defensiva" del incidente, un hallazgo, no un fallo).

---

## Cómo está construido

```
harness/          El motor de experimentación
  agent_loop.py     Lanza N agentes con tareas INDIVIDUALES (no orquesta el ataque)
  adapters.py       Motores intercambiables: mock / ollama / api
  tools.py          Herramientas SANDBOXED (http anclado al target, shell gated, board)
  board.py          El recurso compartido observable (el "caché" del experimento)
  observer.py       Capa 5: registra CoT + tool calls y ALERTA sobre pérdida de contención
  analyze.py        Convierte una corrida en un informe de emergencia / escala / contención
prompts/          Tareas individuales (Modo A/B), system prompt y la nota de orquestación
target/           Objetivos vulnerables que TÚ hospedas (SSTI simple y cadena de 2 fallos)
docs/             INCIDENT (contexto verificado) · METHODOLOGY · EXTENDING
docker-compose.yml  Red internal:true (sin internet) + usuario no-root
```

Lee **[00-ARQUITECTURA-AISLAMIENTO.md](00-ARQUITECTURA-AISLAMIENTO.md)** (las 5 capas de contención) y
**[docs/METHODOLOGY.md](docs/METHODOLOGY.md)** antes de diseñar un experimento.

---

## Los dos modos

- **Modo A — enjambre emergente:** varios agentes con tareas (algunas imposibles) + un recurso
  compartido. Observas si la coordinación aparece sola. Es la réplica de la dinámica del incidente.
- **Modo B — objetivo ciego:** montas un target tuyo y le das al agente solo la URL, sin credenciales.
  Mides capacidad ofensiva pura y si respeta el alcance.

---

## Por qué NO hay un "prompt maestro"

A los agentes del incidente **nadie** les dijo "coordínense y ataquen". Recibieron tareas individuales;
el resto emergió. Si escribes un prompt que ordene el ataque, no estás replicando el fenómeno: lo estás
dirigiendo. Por eso el harness reparte tareas individuales y solo *ofrece* el recurso compartido.
Detalle en [prompts/nota-orquestacion.md](prompts/nota-orquestacion.md).

---

## Contribuir

Ideas bienvenidas: nuevos targets vulnerables (self-hosted), nuevas detecciones de contención en
`observer.py`, adaptadores de motor, métricas en `analyze.py`. Ver [CONTRIBUTING.md](CONTRIBUTING.md).
Todo aporte debe respetar el principio de sellado y no añadir capacidad de targeting real ni evasión.

## Licencia

[MIT](LICENSE). Sin garantías. Úsalo con responsabilidad y dentro de la ley.
