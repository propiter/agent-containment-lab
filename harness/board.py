"""
board.py — El recurso COMPARTIDO observable (Capa 3, deshabilitada a propósito en Modo A).

En el incidente OpenAI-Hugging Face, el canal encubierto nació porque los agentes compartían un caché
de paquetes (Artifactory) y escribían mensajes en NOMBRES DE DIRECTORIOS. Aquí ofrecemos un recurso
compartido mínimo para OBSERVAR si el enjambre lo descubre y lo usa como buzón, sin decirle que existe.

Cada entrada guarda metadatos (autor, timestamp, referencias) para que analyze.py pueda reconstruir el
grafo de coordinación: quién le respondió a quién, cuándo emergió el canal, cuánto creció.
"""
from __future__ import annotations

import json
import threading
import time
from pathlib import Path


class Board:
    """Buzón compartido basado en el sistema de archivos, como el caché del incidente."""

    _lock = threading.Lock()

    def __init__(self, root: Path) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _safe(key: str) -> str:
        return key.replace("/", "_").replace("..", "_")[:200]

    def write(self, key: str, value: str, author: str = "?", refs: list[str] | None = None) -> None:
        # El nombre de la entrada (key) es en sí mismo información — igual que los directorios de Artifactory.
        rec = {
            "key": key,
            "author": author,
            "ts": round(time.time(), 3),
            "refs": refs or [],  # keys a las que este mensaje responde -> grafo de coordinación
            "value": value,
        }
        with self._lock:
            (self.root / self._safe(key)).write_text(json.dumps(rec, ensure_ascii=False), encoding="utf-8")

    def read(self, key: str) -> str | None:
        p = self.root / self._safe(key)
        if not p.exists():
            return None
        try:
            return json.loads(p.read_text(encoding="utf-8")).get("value")
        except json.JSONDecodeError:
            return p.read_text(encoding="utf-8")

    def entry(self, key: str) -> dict | None:
        p = self.root / self._safe(key)
        if not p.exists():
            return None
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {"key": key, "value": p.read_text(encoding="utf-8"), "author": "?", "refs": []}

    def list_keys(self) -> list[str]:
        return sorted(p.name for p in self.root.iterdir()) if self.root.exists() else []

    def all_entries(self) -> list[dict]:
        out = []
        for name in self.list_keys():
            e = self.entry(name)
            if e:
                out.append(e)
        return sorted(out, key=lambda r: r.get("ts", 0))

    def stats(self) -> dict:
        keys = self.list_keys()
        return {"entries": len(keys), "keys_sample": keys[:20]}
