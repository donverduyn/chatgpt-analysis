# Makefile

install:
	./scripts/setup-env.sh

dev:
	./scripts/start-jupyter.sh

lint:
	flake8 notebooks/ scripts/

format:
	black notebooks/ scripts/

gpu-info:
	./scripts/gpu-info.sh