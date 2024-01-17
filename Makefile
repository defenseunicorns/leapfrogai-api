VERSION ?= $(shell git describe --abbrev=0 --tags)

create-venv:
	python -m venv .venv

activate-venv:
	source .venv/bin/activate

requirements-dev:
	python -m pip install -r requirements-dev.txt

requirements:
	pip-sync requirements.txt requirements-dev.txt

build-requirements:
	pip-compile -o requirements.txt pyproject.toml --allow-unsafe

build-requirements-dev:
	pip-compile --extra dev -o requirements-dev.txt pyproject.toml --allow-unsafe

test:
	pytest **/*.py

dev:
	uvicorn main:app --port 3000 --reload

docker-build:
	docker build -t ghcr.io/defenseunicorns/leapfrogai/leapfrogai-api:${VERSION} .

docker-push:
	docker push ghcr.io/defenseunicorns/leapfrogai/leapfrogai-api:${VERSION}

uvicorn_local:
	python -m uvicorn main:app --host 0.0.0.0 --port 8080 --reload