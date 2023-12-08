# LeapfrogAI Python API

## Description

A Python API that exposes LLM backends, via FastAPI and gRPC, in the OpenAI API specification.

## Usage

See [instructions](#instructions) to get the API up and running. Then, go to http://localhost:8080/docs for the Swagger documentation on API usage.

## Instructions

The instructions in this section assume the following:

1. You have properly installed and configured Python 3.11.x, to include its development tools
2. You have chosen a LeapfrogAI model backend and have that running. Some examples of existing backends:

- https://github.com/defenseunicorns/leapfrogai-backend-ctransformers
- https://github.com/defenseunicorns/leapfrogai-backend-whisper

### Local Development

For cloning a model locally and running the development backend.

1. Create `config.yaml`, see `config-example.yaml` for common examples.

2. Setup and run the API:

```bash
# Setup Python Virtual Environment
make create-venv
make activate-venv
make requirements-dev

# Start Model Backend
make dev
```

### Docker Container

#### Image Build and Run

For local image building and running.

1. Create `config.yaml`, see `config-example.yaml` for common examples.

2. Copy `config.yaml` into the container during the run command as a volume:

```bash
# Build the docker image
docker build -t ghcr.io/defenseunicorns/leapfrogai/leapfrogai-api:latest .

# Run the docker container
docker run -p 8080:8080 -v ./config.yaml:/leapfrogai/config.yaml ghcr.io/defenseunicorns/leapfrogai/leapfrogai-api:latest
```