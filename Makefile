.PHONY: help smoke swarm analyze lab-up lab-verify clean

help:
	@echo "Targets:"
	@echo "  make smoke      - corrida mock pequeña + tests (sin instalar nada)"
	@echo "  make swarm      - enjambre mock de 50 agentes con board compartido"
	@echo "  make analyze    - analiza la última corrida en runs/"
	@echo "  make lab-up     - levanta el lab sellado con Docker (target + runner)"
	@echo "  make lab-verify - verifica que el lab NO tiene salida a internet"
	@echo "  make clean      - borra runs/ (evidencia de corridas)"

smoke:
	python3 harness/agent_loop.py --engine mock --swarm 8 --target http://localhost:9/ \
		--board runs/board --impossible-ratio 0.5 --seed 1
	@echo "--- tests ---"
	pytest -q || true

swarm:
	python3 harness/agent_loop.py --engine mock --swarm 50 --target http://localhost:9/ \
		--board runs/board --impossible-ratio 0.4 --seed 7

analyze:
	@last=$$(ls -1dt runs/2* 2>/dev/null | head -1); \
	if [ -z "$$last" ]; then echo "no hay corridas en runs/"; else python3 harness/analyze.py $$last; fi

lab-up:
	docker compose up --build

lab-verify:
	bash scripts/verify-isolation.sh

clean:
	rm -rf runs/2* runs/board
	@touch runs/.gitkeep
	@echo "runs/ limpio"
