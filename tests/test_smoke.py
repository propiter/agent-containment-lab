"""
Test de humo: corre un enjambre mock pequeño y verifica que
  1) el harness produce evidencia,
  2) el recurso compartido EMERGE (agentes imposibles lo usan sin que se les diga),
  3) el observer ALERTA sobre ello,
  4) el analizador produce un informe coherente.

No requiere modelo, red ni Docker.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _run(*args: str) -> str:
    out = subprocess.run(
        [sys.executable, *args], cwd=ROOT, capture_output=True, text=True, timeout=120
    )
    assert out.returncode == 0, f"fallo: {out.stderr}\n{out.stdout}"
    return out.stdout


def test_swarm_emergence_and_containment(tmp_path):
    board = f"runs/board_test"
    stdout = _run(
        "harness/agent_loop.py",
        "--engine", "mock",
        "--swarm", "10",
        "--target", "http://localhost:9/",
        "--board", board,
        "--impossible-ratio", "0.5",
        "--seed", "1",
    )
    assert "Corrida" in stdout
    assert "EMERGIÓ un canal" in stdout, "el recurso compartido debería emerger con tareas imposibles"

    # localizar el run_dir más reciente
    runs = sorted((ROOT / "runs").glob("2*"), key=lambda p: p.stat().st_mtime)
    assert runs, "no se generó ninguna corrida"
    run_dir = runs[-1]

    # hay evidencia por agente y alertas de contención
    agent_logs = [p for p in run_dir.glob("*.jsonl") if p.stem != "alerts"]
    assert len(agent_logs) == 10
    assert (run_dir / "alerts.jsonl").exists(), "el observer debería haber alertado"

    # el analizador corre y reporta emergencia
    report = _run("harness/analyze.py", str(run_dir))
    assert "Emergencia" in report
    assert "Contención" in report
