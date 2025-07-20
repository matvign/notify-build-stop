VENV = ".venv"
BIN = $(VENV)/bin
LOCK = "uv.lock"
LINT_TARGETS := src
FORMAT_TARGETS := src
PORT = 8000

.PHONY: install nuke clean main smptd lint format docker docker-down docker-nuke

install:
	@uv lock;
	@uv sync;

nuke: docker-nuke clean

clean:
	@rm -rf $(VENV) $(LOCK);

main:
	@dotenvx run uv run main.py

smtpd:
	@dotenvx run uv run mail_server.py

lint:
	@echo "Linting..."
	@uvx ruff check $(LINT_TARGETS)

format:
	@echo "Formatting..."
	@uvx ruff format $(FORMAT_TARGETS)

docker:
	@echo "Starting mssql docker container..."
	@docker compose up -d

docker-down:
	@echo "Shutting down docker container..."
	@docker compose down

docker-nuke:
	@echo "Nuking docker containers and volumes..."
	@docker compose down --volumes --remove-orphans
