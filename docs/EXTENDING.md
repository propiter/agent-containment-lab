# Extender el lab

## Añadir un target vulnerable (self-hosted)

1. Crea `target/mi-objetivo/` con tu app + `Dockerfile`. Coloca una `flag` alcanzable solo explotando
   el fallo.
2. Añádela al `docker-compose.yml` en la **misma red interna** (`labnet`, `internal: true`).
3. Apunta el harness: `--target http://mi-objetivo:PUERTO`.

Buenas ideas: una sola vuln clara (SQLi, subida de archivo, SSTI) para calibrar; o **dos fallos
encadenados** (como `target/ejemplo-chain`: file-read → SSTI) para medir *vulnerability chaining*.

## Añadir una detección de contención

En `harness/observer.py`, método `_inspect`: añade un patrón y una entrada en `ALERTAS`. Ejemplos de
comportamientos que querrías detectar: exfiltración por DNS, intentos de persistencia, uso de
credenciales robadas, o un agente escribiendo en el board una asignación a otros (coordinación).

## Añadir un motor

En `harness/adapters.py`, crea una clase con atributo `name` y método `step(history) -> str` que
devuelva texto con `PENSAMIENTO:` y `ACCION:`. Regístrala en `ENGINES`. Ejemplos: otro runtime local
(llama.cpp, vLLM), o un proveedor OpenAI-compatible (ya cubierto por `ApiEngine` vía `ACL_API_BASE`).

## Añadir una métrica

En `harness/analyze.py`, función `analyze`: calcula tu métrica desde los `*.jsonl` y el `board`, y
muéstrala en `to_markdown`. Ideas: curva de crecimiento del board en el tiempo, profundidad del árbol
de coordinación, latencia entre "descubrí el board" y "publiqué".

## Escalar

`--swarm` acepta cientos de agentes; `--max-parallel` limita la concurrencia. Para estudiar "hasta
dónde crece", barre `--swarm` y `--impossible-ratio` y grafica participación vs. escala. **Todo dentro
del lab sellado** — la escala se estudia en contención, no soltando agentes contra el mundo.
