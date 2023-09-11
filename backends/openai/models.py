from pydantic import BaseModel
from typing import Optional

class CompletionRequest(BaseModel):
    prompt: Optional[str] = "What is your name?"
    stream: Optional[bool] = True
    max_new_tokens: Optional[int] = 32
    temperature: Optional[float] = 0.5

class CompletionResponse(BaseModel):
    pass