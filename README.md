# LeapfrogAI Python API

## Description

API to expose LLM backends via FastAPI and gRPC.

## Instructions

Choose a LeapfrogAI model backend and get that running separately. Conisder:
    * https://github.com/defenseunicorns/leapfrogai-backend-ctransformers
    * https://github.com/defenseunicorns/leapfrogai-backend-whisper

#### Run Locally

1. Setup `config.yaml`, see `config-example.yaml` for common examples.

2. Setup and run the API

```bash
# Setup Python Virtual Environment
python -m venv .venv
source .venv/bin/activate
make requirements-dev

# Start Model Backend
make dev
```

### Docker Run

```bash
# Build the docker image
docker build -t ghcr.io/defenseunicorns/leapfrogai/leapfrogai-api:latest .

# Run the docker container
docker run -p 8080:8080 ghcr.io/defenseunicorns/leapfrogai/leapfrogai-api:latest
```

1. Create `config.yaml`, see `config-example.yaml` for common examples.
2. Copy `config.yaml` into the work directory of the container while it is running.
