build:
	make build-docker
	make migrate-python
	make test-python
	make manage-createsuperuser
	make manage-loaddata
	make manage-collectstatic

build-docker:
	docker-compose build
	docker-compose up --no-start postgres
	docker-compose start postgres
	sleep 5

run:
	docker-compose up

manage-python:
	docker-compose run --rm maemp python manage.py $(command)

makemigrations-python: command=makemigrations
makemigrations-python: manage-python
mm: makemigrations-python

migrate-python: command=migrate
migrate-python: manage-python

test-python:
	docker-compose run --rm maemp coverage run -m pytest -v --create-db $(path)
	docker-compose run --rm maemp coverage report

py-shell: command=shell
py-shell: manage-python


manage-createsuperuser: command=shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('testsu@xample.com', 'testsu@xample.com', 'adminpass') if User.objects.filter(email='testsu@xample.com').count() == 0 else None"
manage-createsuperuser: manage-python

manage-collectstatic: command=collectstatic --noinput
manage-collectstatic: manage-python

manage-loaddata: command=loaddata products
manage-loaddata: manage-python