from pydantic import BaseModel
from typing import Optional


class CompletionRequest(BaseModel):
    model: str
    prompt: str | list[int]
    stream: bool | None = False
    max_new_tokens: int | None = 16
    temperature: float | None = 1.0


# class CompletionChoiceMessage(BaseModel):
#     role: str
#     content: str


# class CompletionChoice(BaseModel):
#     index: int
#     message: CompletionChoiceMessage
#     finish_reason: str


# class CompletionResponse(BaseModel):
#     id: str
#     object: str
#     created: int
#     model: str
#     choices: list(CompletionChoice)
