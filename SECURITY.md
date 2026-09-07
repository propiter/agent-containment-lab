# Política de seguridad y uso responsable

Este proyecto es una herramienta de **investigación defensiva / AI-safety**. Su objetivo es estudiar y
**contener** el comportamiento emergente de agentes autónomos, no facilitar ataques.

## Lo que este proyecto ES

- Un laboratorio **sellado** (sin ruta a internet) para observar coordinación emergente de enjambres de
  agentes LLM contra objetivos **vulnerables que el propio investigador hospeda**.
- Un marco de **contención** (5 capas) con instrumentación para detectar pérdida de aislamiento.

## Lo que este proyecto NO es y NO tendrá

- ❌ No contiene exploits armados contra software de terceros.
- ❌ No incluye capacidad de targeting de sistemas ajenos, escaneo de internet ni C2 hacia infra real.
- ❌ No incluye técnicas de evasión de detección para uso malicioso.
- ❌ No incluye mecanismos de auto-propagación fuera del lab.

Los "targets" incluidos son aplicaciones **deliberadamente vulnerables** pensadas para correr en la red
aislada del lab. Los exploits que un agente pueda descubrir aplican a esos objetivos de juguete.

## Garantías técnicas de contención (las hace cumplir el código)

1. **Red sin internet** — `docker-compose.yml` usa `internal: true`. Verifícalo con
   `scripts/verify-isolation.sh`.
2. **HTTP anclado al target** — `harness/tools.py` rechaza cualquier host que no sea el objetivo del lab
   y lo registra como alerta `egress_fuera_de_target`.
3. **Shell gated** — la herramienta shell del agente está deshabilitada salvo `P13_IN_SANDBOX=1`
   (definido solo dentro del contenedor), para que clonar/ejecutar no toque tu host.
4. **Monitoreo siempre activo** — `harness/observer.py` registra y alerta sobre egress, escalada,
   acceso a metadata de nube y manipulación de logs.

## Uso legal

Apuntar cualquier parte de este software a sistemas que no te pertenecen o para los que no tienes
autorización escrita es contrario a su propósito y muy probablemente **ilegal** (p.ej., en Colombia,
Ley 1273 de 2009; leyes equivalentes en otras jurisdicciones). La responsabilidad es de quien lo usa.

## Reportar un problema

Si encuentras una forma en que este proyecto podría facilitar un mal uso (p.ej. una herramienta que se
salga del sellado), abre un *issue* describiendo el problema de contención — sin publicar un exploit
funcional contra terceros. Los PRs que refuercen la contención son especialmente bienvenidos.
