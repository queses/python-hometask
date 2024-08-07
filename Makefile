install:
	poetry install

dev:
	poetry run flask --app ./hometask/app run

migrations-run:
	poetry run alembic upgrade head

migrations-sync: # example: make migration-sync MSG="add user table"
	poetry run alembic revision --autogenerate -m $(MSG)

migration-create:
	poetry run alembic revision -m $(MSG)

format:
	poetry run ruff format

lint:
	poetry run ruff check

lint-fix:
	poetry run ruff check --fix

