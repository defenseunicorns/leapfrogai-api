VERSION ?= $(shell git describe --abbrev=0 --tags)

create-venv:
	python -m venv .venv

activate-venv:
	source .venv/bin/activate

requirements-dev:
	python -m pip install -r requirements-dev.txt

requirements:
	pip-sync requirements.txt

build-requirements:
	python -m piptools compile -o requirements.txt pyproject.toml

build-requirements-dev:
	python -m piptools compile --extra dev -o requirements-dev.txt pyproject.toml --allow-unsafe

.PHONY: test
test:
	python -m pytest . -v

dev:
	if ! [ -f config.yaml ]; then cp config-example.yaml config.yaml; fi
	uvicorn leapfrogai_api.main:app --port 3000 --reload

docker-build:
	docker build -t ghcr.io/defenseunicorns/leapfrogai/leapfrogai-api:${VERSION} .

docker-run:
	docker run -p 8080:8080 -v ./config.yaml:/leapfrogai/config.yaml ghcr.io/defenseunicorns/leapfrogai/leapfrogai-api:${VERSION}

docker-push:
	docker push ghcr.io/defenseunicorns/leapfrogai/leapfrogai-api:${VERSION}

zarf-build:
	zarf package create . --confirm --set LFAI_API_VERSION=${VERSION}

lint:
	ruff check .
	ruff format .
