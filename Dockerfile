ARG ARCH=amd64

FROM ghcr.io/defenseunicorns/leapfrogai/python:3.11-dev-${ARCH} as builder

WORKDIR /leapfrogai

COPY requirements.txt .

RUN pip install -r requirements.txt --user

FROM ghcr.io/defenseunicorns/leapfrogai/python:3.11-${ARCH}

WORKDIR /leapfrogai

COPY --from=builder /home/nonroot/.local/lib/python3.11/site-packages /home/nonroot/.local/lib/python3.11/site-packages
COPY --from=builder /home/nonroot/.local/bin/uvicorn /home/nonroot/.local/bin/uvicorn

COPY leapfrogai_api/ leapfrogai_api/

EXPOSE 8080

ENTRYPOINT ["/home/nonroot/.local/bin/uvicorn", "leapfrogai_api.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8080"]