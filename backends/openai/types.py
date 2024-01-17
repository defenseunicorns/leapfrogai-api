from __future__ import annotations

from dataclasses import dataclass
from typing import Annotated, Dict, Optional

from fastapi import File, Form, UploadFile
from pydantic import BaseModel


##########
# GENERIC
##########
class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int | None = None
    total_tokens: int


##########
# COMPLETION
##########
class CompletionRequest(BaseModel):
    model: str
    prompt: str | list[int]
    stream: bool | None = False
    max_tokens: int | None = 16
    temperature: float | None = 1.0


class CompletionChoice(BaseModel):
    index: int
    text: str
    logprobs: object = None
    finish_reason: str = ""


class CompletionResponse(BaseModel):
    id: str = ""
    object: str = "completion"
    created: int = 0
    model: str = ""
    choices: list[CompletionChoice]
    usage: Usage | None = None


##########
# CHAT
##########


class ChatFunction(BaseModel):
    name: str
    parameters: Dict[str, str]
    description: str


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatDelta(BaseModel):
    role: str
    content: str | None = ""


class ChatCompletionRequest(BaseModel):
    model: str
    messages: list[ChatMessage]
    functions: list[ChatFunction] | None = None
    temperature: float | None = 1.0
    stream: bool | None = False
    stop: str | None = None
    max_tokens: int | None = 128


class ChatChoice(BaseModel):
    index: int
    message: ChatMessage
    finish_reason: str


class ChatStreamChoice(BaseModel):
    index: int
    delta: ChatDelta
    finish_reason: str | None = ""


# TODO @JPERRY do we want two distinct response types for stream vs not-stream or do we want the choices to be unioned?
class ChatCompletionResponse(BaseModel):
    """https://platform.openai.com/docs/api-reference/chat/object"""

    id: str = ""
    object: str = "chat.completion"
    created: int = 0
    model: str = ""
    choices: list[ChatChoice] | list[
        ChatStreamChoice
    ]  # TODO: @JPERRY look into this more, difference between streaming and not streaming
    usage: Usage | None = None


class CreateEmbeddingRequest(BaseModel):
    model: str
    input: str | list[str]
    user: str | None = None


class EmbeddingResponseData(BaseModel):
    embedding: list[float]
    index: int
    object: str = "embedding"


class CreateEmbeddingResponse(BaseModel):
    data: list[EmbeddingResponseData]
    model: str
    object: str = "list"
    usage: Usage


# yes I know, this is a pure API response class for matching OpenAI
class ModelResponseModel(BaseModel):
    id: str
    object: str = "model"
    created: int = 0
    owned_by: str = "leapfrogai"


class ModelResponse(BaseModel):
    object: str = "list"
    data: list[ModelResponseModel] = []


##########
# AUDIO
##########


class CreateTranscriptionRequest(BaseModel):
    file: UploadFile
    model: str
    language: str
    prompt: str
    response_format: str
    temperature: float

    @classmethod
    def as_form(
        cls,
        file: UploadFile = File(...),
        model: str = Form(...),
        language: Optional[str] = Form(""),
        prompt: Optional[str] = Form(""),
        response_format: Optional[str] = Form(""),
        temperature: Optional[float] = Form(1),
    ) -> CreateTranscriptionRequest:
        return cls(
            file=file,
            model=model,
            language=language,
            prompt=prompt,
            response_format=response_format,
            temperature=temperature,
        )


class CreateTranscriptionResponse(BaseModel):
    text: str

##########
# RAG/VECTORDB
##########

class FilesByURLRequest(BaseModel):
    urls: list
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "urls": [
                        "https://adlnet.gov/assets/uploads/webinars/DevSecOps%20and%20LTW%20Webinar%20Slides_Weiss-Smith-Udell.pdf",
                        "https://dodcio.defense.gov/Portals/0/Documents/DoD%20Enterprise%20DevSecOps%20Reference%20Design%20v1.0_Public%20Release.pdf",
                        "https://dodcio.defense.gov/Portals/0/Documents/Library/DoDEnterpriseDevSecOpsFundamentals.pdf",
                    ]
                }
            ]
        }
    }


class Query(BaseModel):
    query: str
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "query": "how can one mitigate and reduce risk?",
                },                
            ]
        }
    }


class URLRequest(BaseModel):
    # urls = ConfigDict(strict=False)
    urls: list
    extensions: list
    url_base: str
    limit: int
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "urls": ['https://read.84000.co/section/all-translated.html'],
                    "extensions": ['pdf'],
                    "url_base": "https://read.84000.co",
                    "limit": 3,
                },
            ]
        }
    }
