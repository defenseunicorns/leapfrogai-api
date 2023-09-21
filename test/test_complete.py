import time

import httpx

url = "http://127.0.0.1:8000/complete"

with httpx.post(url) as r:
    print("processing the completion: ", r)

    for chunk in r.iter_lines():  # or, for line in r.iter_lines():
        print("HELLO WORLD")
        print(chunk, flush=True)
2
