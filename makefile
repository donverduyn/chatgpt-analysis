# Makefile

install:
	./.devcontainer/setup-env.sh

dev:
	./.devcontainer/start-jupyter.sh

lint:
	flake8 notebooks/ scripts/

format:
	black notebooks/ scripts/