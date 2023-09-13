import httpx

url = 'http://127.0.0.1:8000/streamer'

with httpx.stream('GET', url) as r:
    print("processing the stream: ")
    for chunk in r.iter_lines():  
        print(chunk, flush=True)