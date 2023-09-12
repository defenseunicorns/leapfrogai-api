from .openai import router
from .models import CompletionRequest, CompletionResponse
from typing import Iterator, Union
from fastapi.responses import StreamingResponse
import grpc
import leapfrogai
from fastapi import APIRouter

another_router = APIRouter()


async def recv(
    stream: grpc.aio.UnaryStreamCall[
        leapfrogai.CompletionRequest, leapfrogai.CompletionResponse
    ]
):
    async for c in stream:
        yield c.choices[0].text


@another_router.post("/complete")
async def complete(
    req: CompletionRequest,
):
    async with grpc.aio.insecure_channel("100.113.209.116:50051") as channel:
        stub = leapfrogai.CompletionStreamServiceStub(channel)

        request = leapfrogai.CompletionRequest(
            prompt=req.prompt,
            max_new_tokens=req.max_new_tokens,
            temperature=req.temperature,
        )

        stream = stub.CompleteStream(request)

        await stream.wait_for_connection()

        return StreamingResponse(recv(stream), media_type="text/event-stream")
    pass
