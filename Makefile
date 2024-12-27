install:
	pip install uv
    uv pip install -r requirements.txt

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

sync:
	uv sync
