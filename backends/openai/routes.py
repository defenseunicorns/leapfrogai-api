from .types import CompletionRequest, CompletionResponse, ChatCompletionRequest
from .grpc_client import (
    stream_completion,
    completion,
    stream_chat_completion,
    chat_completion,
)
import leapfrogai
from . import router


@router.post("/completions")
async def complete(
    req: CompletionRequest,
):
    request = leapfrogai.CompletionRequest(
        prompt=req.prompt,
        max_new_tokens=req.max_new_tokens,
        temperature=req.temperature,
    )

    if req.stream:
        return stream_completion(request)
    else:
        return completion(request)


@router.post("/chat/completions")
async def complete(
    req: ChatCompletionRequest,
):
    request = leapfrogai.ChatCompletionRequest(
        prompt=req.prompt,
        max_new_tokens=req.max_new_tokens,
        temperature=req.temperature,
    )

    if req.stream:
        return stream_chat_completion(request)
    else:
        return chat_completion(request)
