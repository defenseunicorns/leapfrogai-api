from typing import Annotated, Iterator, BinaryIO
from itertools import chain
import leapfrogai
from fastapi import Depends, File, UploadFile, Form

from utils import get_model_config
from utils.config import Config
from . import router
from .grpc_client import (
    chat_completion,
    completion,
    create_embeddings,
    stream_chat_completion,
    stream_completion,
    create_transcription,
)
from .helpers import grpc_chat_role
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


# read_chunks is a helper method that chunks the bytes of a file (audio file) into a iterator of AudioRequests
def read_chunks(file: BinaryIO, chunk_size: int) -> Iterator[leapfrogai.AudioRequest]:
    while True:
        chunk = file.read(chunk_size)
        if not chunk:
            break
        yield leapfrogai.AudioRequest(chunk_data=chunk)


@router.post("/audio/transcriptions")
async def transcribe(
    model_config: Annotated[Config, Depends(get_model_config)],
    req: CreateTranscriptionRequest = Depends()
) -> CreateTranscriptionResponse:
    model = model_config.models[req.model]

    # Create a request that contains the metadata for the AudioRequest
    audio_metadata = leapfrogai.AudioMetadata(prompt=req.prompt,
                                              temperature=req.temperature,
                                              inputlanguage=req.language)
    audio_metadata_request = leapfrogai.AudioRequest(metadata=audio_metadata)

    # Read the file and get an iterator of all the data chunks
    chunk_iterator = read_chunks(req.file.file, 1024)

    # combine our metadata and chunk_data iterators
    request_iterator = chain((audio_metadata_request,), chunk_iterator)

    return await create_transcription(model, request_iterator)