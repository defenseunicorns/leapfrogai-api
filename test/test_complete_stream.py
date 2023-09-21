import time

import httpx
from pydantic import BaseModel

url = "http://127.0.0.1:8000/complete"


class CompletionRequest(BaseModel):
    model: str
    prompt: str | list[int]
    stream: bool | None = False
    max_new_tokens: int | None = 16
    temperature: float | None = 1.0


thedata = CompletionRequest(
    model="somethign",
    prompt="What is your favorite name?",
    max_new_tokens=512,
    temperature=0.7,
)


thedata = {
    "prompt": "What is your favorite name?",
    "max_new_tokens": "512",
    "temperature": "0.7",
}

with httpx.stream("POST", url, data=thedata) as r:
    print("processing the stream: ", r.is_stream_consumed)
    print(r.is_closed)
    # print(r.iter_bytes)

    for chunk in r.iter_lines():  # or, for line in r.iter_lines():
        print("HELLO WORLD")
        print(chunk, flush=True)
2
