from itertools import chain
from typing import Annotated

import leapfrogai
from fastapi import Depends, HTTPException

from utils import get_model_config
from utils.config import Config

from . import router
from .grpc_client import (
    chat_completion,
    completion,
    create_embeddings,
    create_transcription,
    stream_chat_completion,
    stream_completion,
)
from .helpers import grpc_chat_role, read_chunks
from .types import (
    ChatCompletionRequest,
    CompletionRequest,
    CreateEmbeddingRequest,
    CreateEmbeddingResponse,
    CreateTranscriptionRequest,
    CreateTranscriptionResponse,
    ModelResponse,
    ModelResponseModel,
)


@router.post("/completions")
async def complete(
    req: CompletionRequest, model_config: Annotated[Config, Depends(get_model_config)]
):
    # Get the model backend configuration
    model = model_config.get_model_backend(req.model)
    if model == None:
        raise HTTPException(
            status_code=405,
            detail=f"Model {req.model} not found. Currently supported models are {list(model_config.models.keys())}",
        )

    request = leapfrogai.CompletionRequest(
        prompt=req.prompt,  # type: ignore
        max_new_tokens=req.max_tokens,
        temperature=req.temperature,
    )

    if req.stream:
        return await stream_completion(model, request)
    else:
        return await completion(model, request)


@router.post("/chat/completions")
async def chat_complete(
    req: ChatCompletionRequest,
    model_config: Annotated[Config, Depends(get_model_config)],
):
    # Get the model backend configuration
    model = model_config.get_model_backend(req.model)
    if model == None:
        raise HTTPException(
            status_code=405,
            detail=f"Model {req.model} not found. Currently supported models are {list(model_config.models.keys())}",
        )

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
    # Get the model backend configuration
    model = model_config.get_model_backend(req.model)
    if model == None:
        raise HTTPException(
            status_code=405,
            detail=f"Model {req.model} not found. Currently supported models are {list(model_config.models.keys())}",
        )

    request = leapfrogai.EmbeddingRequest(inputs=[req.input])  # type: ignore
    return await create_embeddings(model, request)


@router.post("/audio/transcriptions")
async def transcribe(
    model_config: Annotated[Config, Depends(get_model_config)],
    req: CreateTranscriptionRequest = Depends(CreateTranscriptionRequest.as_form),
) -> CreateTranscriptionResponse:
    # Get the model backend configuration
    model = model_config.get_model_backend(req.model)
    if model == None:
        raise HTTPException(
            status_code=405,
            detail=f"Model {req.model} not found. Currently supported models are {list(model_config.models.keys())}",
        )

    # Create a request that contains the metadata for the AudioRequest
    audio_metadata = leapfrogai.AudioMetadata(
        prompt=req.prompt, temperature=req.temperature, inputlanguage=req.language
    )
    audio_metadata_request = leapfrogai.AudioRequest(metadata=audio_metadata)

    # Read the file and get an iterator of all the data chunks
    chunk_iterator = read_chunks(req.file.file, 1024)

    # combine our metadata and chunk_data iterators
    request_iterator = chain((audio_metadata_request,), chunk_iterator)

    return await create_transcription(model, request_iterator)