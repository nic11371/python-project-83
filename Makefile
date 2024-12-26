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

poetry-install:
	poetry init

PORT ?= 8000
poetry-start:
	uvicorn page_analyzer:app --host 0.0.0.0 --port $PORT
