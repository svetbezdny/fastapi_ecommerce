MAKEFLAGS += -s

run:
	export PYTHONPATH=$$PWD && \
	uv run app/main.py

lint:
	uv run mypy .
	uv run ruff check
	uv run ruff format

base-up:
	docker compose -f "docker-compose.postgres.yml" up -d