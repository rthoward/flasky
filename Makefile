.PHONY: test

dev:
	@FLASK_APP=main.py FLASK_ENV=development pipenv run flask run

test:
	@pipenv run pytest -s

format:
	@pipenv run black .

check:
	@pipenv run mypy main.py
