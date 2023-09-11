from .openai import router
from .models import CompletionRequest, CompletionResponse
from typing import Union, Iterator
from fastapi.responses import StreamingResponse
import grpc
import leapfrogai
from fastapi import APIRouter

another_router = APIRouter()

def response_processor(response):
    for resp in response:
        yield resp


@another_router.post("/complete")
async def complete():
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = leapfrogai.CompletionStreamServiceStub(channel)
        
        request = leapfrogai.CompletionRequest(
            prompt="What is 1+1?",
            max_new_tokens=10,
            temperature=0.5
        )
        
        # if request.stream:
        response: Iterator[leapfrogai.CompletionResponse] = stub.CompleteStream(request)
        # for c in response:
        #     print(c.choices[0].text)
        
        return StreamingResponse(response, media_type="text/event-stream")    
        # for completion in response:
        #     if req.stream:
        #         # buffer
        #         return StreamingResponse(completion) 
        #     else:
        #         pass
        #         # stream
    
    pass

