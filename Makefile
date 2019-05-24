.PHONY: test

dev:
	@FLASK_APP=main.py FLASK_ENV=development pipenv run flask run

test:
	@pipenv run pytest -s

format:
	@pipenv run black .

check:
	@pipenv run mypy main.py

pg:
	$(eval DOCKER_IP := $(shell docker network inspect bridge | grep Gateway | awk '{ gsub(/"/, "", $$2); print $$2; }'))
	@psql postgresql://postgres:postgres@$(DOCKER_IP):5432/postgres
