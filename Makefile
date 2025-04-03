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
