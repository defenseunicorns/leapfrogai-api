import grpc
import leapfrogai
from .types import (
    CompletionResponse,
    ChatCompletionResponse,
    CompletionChoice,
    Usage,
    ChatStreamChoice,
    ChatDelta,
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

    yield "event: data\n\ndata: [DONE]"


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
                )
            ],
            usage=Usage(prompt_tokens=0, completion_tokens=0, total_tokens=0),
        ).model_dump_json()
        yield "\n\n"

    yield "event: data\n\ndata: [DONE]"
