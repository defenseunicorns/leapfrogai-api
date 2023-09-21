FROM cgr.dev/chainguard/python:latest-dev as builder

WORKDIR /leapfrogai

COPY requirements.txt .

RUN pip install -r requirements.txt --user

FROM cgr.dev/chainguard/python:latest

WORKDIR /leapfrogai

COPY --from=builder /home/nonroot/.local/lib/python3.11/site-packages /home/nonroot/.local/lib/python3.11/site-packages
COPY --from=builder /home/nonroot/.local/bin/uvicorn /home/nonroot/.local/bin/uvicorn

COPY main.py .
COPY utils/ utils/
COPY backends/ backends/

EXPOSE 8080

ENTRYPOINT ["/home/nonroot/.local/bin/uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8080"]