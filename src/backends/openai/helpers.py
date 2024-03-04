from typing import BinaryIO, Iterator, Union

import grpc
import leapfrogai

from src.backends.openai.types import (
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
    ],
):
    async for c in stream:
        yield (
            "data: "
            + CompletionResponse(
                id="foo",
                object="completion.chunk",
                created=55,
                model="mpt-7b-8k-chat",
                choices=[
                    CompletionChoice(
                        index=0,
                        text=c.choices[0].text,
                        logprobs=None,
                        finish_reason="stop",
                    )
                ],
                usage=Usage(prompt_tokens=0, completion_tokens=0, total_tokens=0),
            ).model_dump_json()
        )
        yield "\n\n"

    yield "data: [DONE]"


async def recv_chat(
    stream: grpc.aio.UnaryStreamCall[
        leapfrogai.ChatCompletionRequest, leapfrogai.ChatCompletionResponse
    ],
):
    async for c in stream:
        yield (
            "data: "
            + ChatCompletionResponse(
                id="foo",
                object="chat.completion.chunk",
                created=55,
                model="mpt-7b-8k-chat",
                choices=[
                    ChatStreamChoice(
                        index=0,
                        delta=ChatDelta(
                            role="assistant", content=c.choices[0].chat_item.content
                        ),
                        finish_reason=None,
                    )
                ],
                usage=Usage(prompt_tokens=0, completion_tokens=0, total_tokens=0),
            ).model_dump_json()
        )
        yield "\n\n"

    yield "data: [DONE]\n\n"


def grpc_chat_role(role: str) -> Union[leapfrogai.ChatRole, None]:
    match role:
        case "user":
            return leapfrogai.ChatRole.USER  # type: ignore
        case "system":
            return leapfrogai.ChatRole.SYSTEM  # type: ignore
        case "function":
            return leapfrogai.ChatRole.FUNCTION  # type: ignore
        case "assistant":
            return leapfrogai.ChatRole.ASSISTANT  # type: ignore
        case _:
            return None


# read_chunks is a helper method that chunks the bytes of a file (audio file) into a iterator of AudioRequests
def read_chunks(file: BinaryIO, chunk_size: int) -> Iterator[leapfrogai.AudioRequest]:
    while True:
        chunk = file.read(chunk_size)
        if not chunk:
            break
        yield leapfrogai.AudioRequest(chunk_data=chunk)
