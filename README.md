# LeapfrogAI Python API

## Description

A Python API that exposes LLM backends, via FastAPI and gRPC, in the OpenAI API specification.

## Usage

See [instructions](#instructions) to get the API up and running. Then, go to http://localhost:8080/docs for the Swagger documentation on API usage.

## Instructions

Choose a LeapfrogAI model backend and get that running separately. Some examples of existing backends:

- https://github.com/defenseunicorns/leapfrogai-backend-ctransformers
- https://github.com/defenseunicorns/leapfrogai-backend-whisper

#### Run Locally

1. Create `config.yaml`, see `config-example.yaml` for common examples.

2. Setup and run the API:

```bash
# Setup Python Virtual Environment
python -m venv .venv
source .venv/bin/activate
make requirements-dev

# Start Model Backend
make dev
```

### Docker Run

1. Create `config.yaml`, see `config-example.yaml` for common examples.

2. Copy `config.yaml` into the container during the run command as a volume:

```bash
# Build the docker image
docker build -t ghcr.io/defenseunicorns/leapfrogai/leapfrogai-api:latest .

# Run the docker container
docker run -p 8080:8080 -v ./config.yaml:/leapfrogai/config.yaml ghcr.io/defenseunicorns/leapfrogai/leapfrogai-api:latest
```
