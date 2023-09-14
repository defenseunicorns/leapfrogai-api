from .types import (
    CompletionRequest,
    ChatCompletionRequest,
    ModelResponse,
    ModelResponseModel,
)
from .grpc_client import (
    stream_completion,
    completion,
    stream_chat_completion,
    chat_completion,
)
import leapfrogai
from utils import get_model_config
from utils.config import Config
from fastapi import Depends
from typing import Annotated
from . import router


@router.post("/completions")
async def complete(
    req: CompletionRequest, model_config: Annotated[Config, Depends(get_model_config)]
):
    request = leapfrogai.CompletionRequest(
        prompt=req.prompt,
        max_new_tokens=req.max_new_tokens,
        temperature=req.temperature,
    )

    if req.stream:
        return await stream_completion(request)
    else:
        return await completion(request)


@router.post("/chat/completions")
async def complete(
    req: ChatCompletionRequest,
    model_config: Annotated[Config, Depends(get_model_config)],
):
    chat_items: list[leapfrogai.ChatItem] = []
    for m in req.messages:
        chat_items.append(
            leapfrogai.ChatItem(role=leapfrogai.ChatRole.USER, content=m.content)
        )
    request = leapfrogai.ChatCompletionRequest(
        chat_items=chat_items,
        max_new_tokens=req.max_tokens,
        temperature=req.temperature,
    )

    if req.stream:
        return await stream_chat_completion(request)
    else:
        return await chat_completion(request)


@router.get("/models")
async def models(
    model_config: Annotated[Config, Depends(get_model_config)]
) -> ModelResponse:
    res = ModelResponse()
    for model in model_config.models:
        m = ModelResponseModel(id=model)
        res.data.append(m)
    return res


# @router.post("/embeddings")
# async def create_embeddings(req: CreateEmbeddingRequest):
#    request = leapfrogai.EmbeddingRequest(
