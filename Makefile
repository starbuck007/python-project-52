install:
	uv sync

collectstatic:
	python manage.py collectstatic --noinput

migrate:
	python manage.py migrate

build:
	./build.sh

run:
	python manage.py runserver

render-start:
	gunicorn task_manager.wsgi:application --bind 0.0.0.0:$(PORT)

test:
	python manage.py test task_manager.tests

check:
	python -m flake8

test-coverage:
	coverage run --source=task_manager manage.py test
	coverage xml

cov:
	uv run coverage xml

lint:
	uv run ruff check task_manager/

fix:
	uv run ruff check --fix task_manager/
