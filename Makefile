install:
	uv sync

collectstatic:
	uv run python manage.py collectstatic --no-input

migrate:
	uv run python manage.py migrate

build:
	./build.sh

render-start:
	uv run gunicorn task_manager.wsgi

start:
	uv run python manage.py runserver

test:
	uv run python manage.py test

lint:
	uv run ruff check .

lint-fix:
	uv run ruff check --fix .

.PHONY: install collectstatic migrate build render-start start test lint lint-fix