install:
	uv sync

dev:
	uv run flask --app page_analyzer:app run

check:
	uv run ruff check .

check-fix:
	uv run ruff check --fix .

PORT ?= 8000
start:
	uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

build:
	./build.sh

uv-install:
	curl -LsSf https://astral.sh/uv/install.sh | sh
	source $HOME/.local/bin/env (sh, bash, zsh)
    source $HOME/.local/bin/env.fish (fish)
