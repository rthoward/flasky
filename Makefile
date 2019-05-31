.PHONY: test

dev:
	@FLASK_APP=main.py FLASK_ENV=development pipenv run flask run

dev.kill:
	pkill -f "flask run"

test:
	@pipenv run pytest -s test

format:
	@pipenv run black .

check:
	@pipenv run mypy main.py

docs.check:
	yarn --cwd docs/ lint && yarn --cwd docs/ format:check

docs.format:
	yarn --cwd docs/ format

docs.serve:
	yarn --cwd docs/ serve

pg:
	$(eval DOCKER_IP := $(shell docker network inspect bridge | grep Gateway | awk '{ gsub(/"/, "", $$2); print $$2; }'))
	@pgcli postgresql://postgres:postgres@$(DOCKER_IP):5432/postgres
