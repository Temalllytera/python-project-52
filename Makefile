install:
	uv sync

tailwind:
	uv run python manage.py tailwind build

collectstatic:
	uv run python manage.py collectstatic --no-input --ignore source.css

migrate:
	uv run python manage.py migrate

build:
	./build.sh

render-start:
	uv run gunicorn task_manager.wsgi

start:
	uv run python manage.py tailwind runserver

test:
	uv run python manage.py test

test-coverage:
	uv run coverage run manage.py test
	uv run coverage report
	uv run coverage xml

lint:
	uv run ruff check .

lint-fix:
	uv run ruff check --fix .

check: lint test-coverage

.PHONY: install tailwind collectstatic migrate build render-start start test test-coverage lint lint-fix check