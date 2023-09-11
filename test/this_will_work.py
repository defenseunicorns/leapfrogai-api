import httpx


url = 'http://127.0.0.1:8000/complete'

with httpx.stream('POST', url) as r:
    print("processing the stream: ")
    for chunk in r.iter_lines():  # or, for line in r.iter_lines():
        print(chunk, flush=True)


# url = 'http://127.0.0.1:8000/streamer'

# with httpx.stream('GET', url) as r:
#     print("processing the stream: ")
#     for chunk in r.iter_lines():  # or, for line in r.iter_lines():
#         print(chunk, flush=True)