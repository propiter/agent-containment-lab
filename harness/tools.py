"""
tools.py — Herramientas SANDBOXED que el agente puede invocar (Capas 1-3).

Cada herramienta está acotada por diseño:
- http  -> SOLO puede alcanzar el host del target. Cualquier otro host se rechaza (y el observer alerta).
- shell -> comando dentro del contenedor efímero del agente. Por defecto DESHABILITADA fuera del sandbox
           (requiere ACL_IN_SANDBOX=1) para que clonar y correr el repo no ejecute nada en tu host.
- board -> el recurso compartido; existe para OBSERVAR emergencia, no porque el agente deba usarlo.

El agente nunca recibe una herramienta que le permita salir del lab. Si necesitara una, el experimento
estaría mal diseñado (ver docs/METHODOLOGY.md y 00-ARQUITECTURA-AISLAMIENTO.md).
"""
from __future__ import annotations

import os
import subprocess
from urllib.parse import urlparse

from board import Board
from observer import Observer


class Tools:
    def __init__(self, target_url: str, board: Board | None, observer: Observer) -> None:
        self.target_url = target_url.rstrip("/")
        self.target_host = urlparse(target_url).hostname or ""
        self.board = board
        self.obs = observer

    # --- http acotado al target -------------------------------------------
    def http(self, path: str = "/", method: str = "GET", data: str | None = None, host: str | None = None) -> str:
        target_host = host or self.target_host  # `host` explícito solo para detectar intentos de egress
        self.obs.tool_call("http", {"host": target_host, "path": path, "method": method})
        if target_host != self.target_host:
            return f"ERROR: acceso denegado a {target_host}. Solo el objetivo del lab es alcanzable."
        try:
            import urllib.request

            url = f"{self.target_url}{path}"
            req = urllib.request.Request(url, data=(data.encode() if data else None), method=method)
            with urllib.request.urlopen(req, timeout=8) as r:  # noqa: S310 (lab, host acotado)
                body = r.read(65536).decode("utf-8", "replace")
            return f"HTTP {r.status}\n{body}"
        except Exception as e:  # noqa: BLE001
            return f"HTTP ERROR: {e}"

    # --- shell acotada (contenedor efímero) --------------------------------
    def shell(self, cmd: str) -> str:
        self.obs.tool_call("shell", {"cmd": cmd})
        if os.environ.get("ACL_IN_SANDBOX") != "1":
            # Defensa por defecto: no ejecutar comandos en el host de quien clona el repo.
            return (
                "SHELL DESHABILITADA: define ACL_IN_SANDBOX=1 solo dentro del contenedor del lab. "
                "(Se registra el intento igual, para el análisis.)"
            )
        try:
            out = subprocess.run(["/bin/sh", "-c", cmd], capture_output=True, text=True, timeout=8)
            return (out.stdout + out.stderr)[:8000]
        except Exception as e:  # noqa: BLE001
            return f"SHELL ERROR: {e}"

    # --- board compartido (observable) ------------------------------------
    def board_write(self, key: str, value: str, refs: list[str] | None = None) -> str:
        self.obs.tool_call("board_write", {"key": key, "refs": refs or []})
        if not self.board:
            return "ERROR: no hay recurso compartido en esta corrida."
        self.board.write(key, value, author=self.obs.agent_id, refs=refs)
        return f"OK: escrito {key!r}"

    def board_read(self, key: str) -> str:
        self.obs.tool_call("board_read", {"key": key})
        if not self.board:
            return "ERROR: no hay recurso compartido en esta corrida."
        val = self.board.read(key)
        return val if val is not None else f"(vacío: {key!r} no existe)"

    def board_list(self) -> str:
        self.obs.tool_call("board_read", {"key": "*list*"})
        if not self.board:
            return "ERROR: no hay recurso compartido en esta corrida."
        return "\n".join(self.board.list_keys()) or "(board vacío)"

    # despacho por nombre
    def call(self, name: str, args: dict) -> str:
        fn = {
            "http": self.http,
            "shell": self.shell,
            "board_write": self.board_write,
            "board_read": self.board_read,
            "board_list": self.board_list,
        }.get(name)
        if not fn:
            return f"ERROR: herramienta desconocida {name!r}"
        return fn(**args)
