from fastapi.responses import StreamingResponse
import leapfrogai
import grpc
from backends.openai.helpers import recv_chat, recv_completion
from backends.openai.types import (
    CompletionResponse,
    CompletionChoice,
    ChatCompletionResponse,
    ChatChoice,
    ChatMessage,
    CreateEmbeddingResponse,
    EmbeddingResponseData,
    Usage,
)


async def stream_completion(backend: str, request: leapfrogai.CompletionRequest):
    async with grpc.aio.insecure_channel(backend) as channel:
        stub = leapfrogai.CompletionStreamServiceStub(channel)
        stream = stub.CompleteStream(request)

        await stream.wait_for_connection()
        return StreamingResponse(
            recv_completion(stream), media_type="text/event-stream"
        )


# TODO: CLean up completion() and stream_completion() to reduce code duplication
async def completion(backend: str, request: leapfrogai.CompletionRequest):
    async with grpc.aio.insecure_channel(backend) as channel:
        stub = leapfrogai.CompletionServiceStub(channel)
        response: leapfrogai.CompletionResponse = stub.Complete(request)

        return CompletionResponse(
            choices=[
                CompletionChoice(
                    index=0,
                    text=response.choices[0].text,
                    finish_reason=response.choices[0].finish_reason,
                )
            ]
        )


async def stream_chat_completion(
    backend: str, request: leapfrogai.ChatCompletionRequest
):
    async with grpc.aio.insecure_channel(backend) as channel:
        stub = leapfrogai.ChatCompletionStreamServiceStub(channel)
        stream = stub.ChatCompleteStream(request)

        await stream.wait_for_connection()
        return StreamingResponse(recv_chat(stream), media_type="text/event-stream")


# TODO: CLean up completion() and stream_completion() to reduce code duplication
async def chat_completion(backend: str, request: leapfrogai.ChatCompletionRequest):
    async with grpc.aio.insecure_channel(backend) as channel:
        stub = leapfrogai.CompletionServiceStub(channel)
        response: leapfrogai.ChatCompletionResponse = stub.Complete(request)

        return ChatCompletionResponse(
            choices=[
                ChatChoice(
                    index=0,
                    message=ChatMessage(
                        role=response.choices[0].chat_item.role,
                        content=response.choices[0].chat_item.content,
                    ),
                )
            ]
        )


async def create_embeddings(backend: str, request: leapfrogai.EmbeddingRequest):
    async with grpc.aio.insecure_channel(backend) as channel:
        stub = leapfrogai.EmbeddingsServiceStub(channel)
        e: leapfrogai.EmbeddingResponse = await stub.CreateEmbedding(request)
        return CreateEmbeddingResponse(
            data=[
                EmbeddingResponseData(
                    embedding=e.embeddings[0].embedding,
                    index=0,
                )
            ],
            model="",
            usage=Usage(prompt_tokens=0, total_tokens=0),
        )
