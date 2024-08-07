dev:
	poetry run flask --app ./hometask/app run

script:
	poetry run python -m hometask.script
