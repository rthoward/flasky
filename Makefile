.PHONY: test

dev:
	FLASK_APP=main.py FLASK_ENV=development pipenv run flask run

test:
	pipenv run pytest -s
