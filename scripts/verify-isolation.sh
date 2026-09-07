#!/usr/bin/env bash
# Verifica que el lab NO tiene ruta a internet (Capa 1 de contención).
# Debe imprimir AISLADO_OK. Si Google responde, tu lab está mal sellado: NO continúes.
set -euo pipefail

echo "[*] Comprobando aislamiento de la red del lab..."

if command -v docker >/dev/null 2>&1 && docker compose ps >/dev/null 2>&1; then
  echo "[*] Vía Docker (red internal:true):"
  docker compose run --rm --entrypoint sh agente -c \
    "curl -sS --max-time 5 https://google.com >/dev/null 2>&1 && echo 'FUGA: hay internet' || echo 'AISLADO_OK'"
else
  echo "[!] Docker no disponible o lab no levantado."
  echo "    Si corres el harness fuera de Docker, el aislamiento depende de TU red host-only."
  echo "    Recomendado: usa 'docker compose up' para el sellado automático (internal:true)."
fi
