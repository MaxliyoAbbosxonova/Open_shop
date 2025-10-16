mig:
	python manage.py makemigrations
	python manage.py migrate
sup:
	python manage.py createsuperuser
run:
	python manage.py runserver
msg:
	python manage.py makemessages -l uz -l en

compile_msg:
	python manage.py compilemessages -i .venv

mig2:
	docker compose exec backend_service python manage.py makemigrations
	docker compose exec backend_service python manage.py migrate
