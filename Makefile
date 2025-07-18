VENV = ".venv"
BIN = $(VENV)/bin
LOCK = "uv.lock"
LINT_TARGETS := src
FORMAT_TARGETS := src
PORT = 8000

.PHONY: install nuke clean lint format docker docker-down 

install:
	@uv lock;
	@uv sync;

nuke: docker-down nuke

clean:
	@rm -rf $(VENV) $(LOCK);

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