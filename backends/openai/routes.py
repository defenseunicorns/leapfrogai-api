from typing import Annotated

import leapfrogai
from fastapi import Depends

from utils import get_model_config
from utils.config import Config

from . import router
from .grpc_client import (
    chat_completion,
    completion,
    create_embeddings,
    stream_chat_completion,
    stream_completion,
)
from .helpers import grpc_chat_role
from .types import (
    ChatCompletionRequest,
    CompletionRequest,
    CreateEmbeddingRequest,
    CreateEmbeddingResponse,
    ModelResponse,
    ModelResponseModel,
)


@router.post("/completions")
async def complete(
    req: CompletionRequest, model_config: Annotated[Config, Depends(get_model_config)]
):
    model = model_config.models[req.model]
    request = leapfrogai.CompletionRequest(
        prompt=req.prompt,
        max_new_tokens=req.max_new_tokens,
        temperature=req.temperature,
    )

    if req.stream:
        return await stream_completion(model, request)
    else:
        return await completion(model, request)


@router.post("/chat/completions")
async def complete(
    req: ChatCompletionRequest,
    model_config: Annotated[Config, Depends(get_model_config)],
):
    model = model_config.models[req.model]
    chat_items: list[leapfrogai.ChatItem] = []
    for m in req.messages:
        chat_items.append(
            leapfrogai.ChatItem(role=grpc_chat_role(m.role), content=m.content)
        )
    request = leapfrogai.ChatCompletionRequest(
        chat_items=chat_items,
        max_new_tokens=req.max_tokens,
        temperature=req.temperature,
    )

    if req.stream:
        return await stream_chat_completion(model, request)
    else:
        return await chat_completion(model, request)


@router.get("/models")
async def models(
    model_config: Annotated[Config, Depends(get_model_config)]
) -> ModelResponse:
    res = ModelResponse()
    for model in model_config.models:
        m = ModelResponseModel(id=model)
        res.data.append(m)
    return res


@router.post("/embeddings")
async def embeddings(
    req: CreateEmbeddingRequest,
    model_config: Annotated[Config, Depends(get_model_config)],
) -> CreateEmbeddingResponse:
    request = leapfrogai.EmbeddingRequest(inputs=[req.input])
    model = model_config.models[req.model]
    return await create_embeddings(model, request)
