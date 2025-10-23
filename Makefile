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

loaddata:
	python3 manage.py loaddata categories users

mig2:
	docker compose exec -it backend_service sh -c 'uv run python3 manage.py makemigrations'
	docker compose exec -it backend_service sh -c 'uv run python3 manage.py migrate'
