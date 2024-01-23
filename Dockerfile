ARG ARCH=amd64

FROM ghcr.io/defenseunicorns/leapfrogai/python:3.11-dev-${ARCH} as builder

WORKDIR /leapfrogai

COPY requirements.txt .

RUN pip install -r requirements.txt --user

RUN mkdir -p /home/nonroot/huggingface/hub/cache

FROM ghcr.io/defenseunicorns/leapfrogai/python:3.11-${ARCH}

WORKDIR /leapfrogai

COPY --from=builder /home/nonroot/.local/lib/python3.11/site-packages /home/nonroot/.local/lib/python3.11/site-packages
COPY --from=builder /home/nonroot/.local/bin/uvicorn /home/nonroot/.local/bin/uvicorn
COPY --from=builder /home/nonroot/huggingface/hub/cache /home/nonroot/huggingface/hub/cache

COPY main.py .
COPY utils/ utils/
COPY backends/ backends/
COPY vectordb/ vectordb/

EXPOSE 8080

ENTRYPOINT ["/home/nonroot/.local/bin/uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8080"]