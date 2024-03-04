VERSION ?= $(shell git describe --abbrev=0 --tags)

create-venv:
	python -m venv .venv

activate-venv:
	source .venv/bin/activate

requirements-dev:
	python -m pip install .[dev]

requirements:
	python -m pip install .

.PHONY: test
test:
	python -m pytest . -v

dev:
	uvicorn src.main:app --port 3000 --reload

docker-build:
	docker build -t ghcr.io/defenseunicorns/leapfrogai/leapfrogai-api:${VERSION} .

docker-push:
	docker push ghcr.io/defenseunicorns/leapfrogai/leapfrogai-api:${VERSION}

zarf-build:
	zarf package create . --confirm --set LFAI_API_VERSION=${VERSION}

lint:
	ruff check .
	ruff format .
