import grpc
import leapfrogai

from typing import Iterator, BinaryIO
from .types import (
    ChatCompletionResponse,
    ChatDelta,
    ChatStreamChoice,
    CompletionChoice,
    CompletionResponse,
    Usage,
)


async def recv_completion(
    stream: grpc.aio.UnaryStreamCall[
        leapfrogai.CompletionRequest, leapfrogai.CompletionResponse
    ]
):
    async for c in stream:
        yield "event: data\n"
        yield "data: " + CompletionResponse(
            id="foo",
            object="bar",
            created=55,
            model="mpt-7b-8k-chat",
            choices=[
                CompletionChoice(
                    index=0, text=c.choices[0].text, logprobs=None, finish_reason="stop"
                )
            ],
            usage=Usage(prompt_tokens=0, completion_tokens=0, total_tokens=0),
        ).model_dump_json()
        yield "\n\n"

    yield "event: data\ndata: [DONE]"


async def recv_chat(
    stream: grpc.aio.UnaryStreamCall[
        leapfrogai.ChatCompletionRequest, leapfrogai.ChatCompletionResponse
    ]
):
    async for c in stream:
        yield "event: data\n"
        yield "data: " + ChatCompletionResponse(
            id="foo",
            object="foo",
            created=55,
            model="mpt-7b-8k-chat",
            choices=[
                ChatStreamChoice(
                    index=0,
                    delta=ChatDelta(
                        role="assistant", content=c.choices[0].chat_item.content
                    ),
                    finish_reason=c.choices[0].finish_reason,
                )
            ],
            usage=Usage(prompt_tokens=0, completion_tokens=0, total_tokens=0),
        ).model_dump_json()
        yield "\n\n"

    yield "event: data\ndata: [DONE]\n\n"


def grpc_chat_role(role: str) -> leapfrogai.ChatRole:
    match role:
        case "user":
            return leapfrogai.ChatRole.USER
        case "system":
            return leapfrogai.ChatRole.SYSTEM
        case "function":
            return leapfrogai.ChatRole.FUNCTION
        case "assistant":
            return leapfrogai.ChatRole.ASSISTANT

# read_chunks is a helper method that chunks the bytes of a file (audio file) into a iterator of AudioRequests
def read_chunks(file: BinaryIO, chunk_size: int) -> Iterator[leapfrogai.AudioRequest]:
    while True:
        chunk = file.read(chunk_size)
        if not chunk:
            break
        yield leapfrogai.AudioRequest(chunk_data=chunk)