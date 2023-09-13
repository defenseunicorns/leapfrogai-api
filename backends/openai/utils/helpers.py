import grpc
import leapfrogai
from backends.openai.models import CompletionResponse, ChatCompletionResponse

async def recv_completion(
    stream: grpc.aio.UnaryStreamCall[
        leapfrogai.CompletionRequest, leapfrogai.CompletionResponse
    ]
):
    async for c in stream:
        yield CompletionResponse(
            choices=[
                CompletionChoice(
                    index=0,
                    text = c.choices[0].text,
                    logprobs=None,
                    finish_reason=c.choices[0].finish_reason
                )
            ]
        )
        
    # do we need to yield "[DONE]"?

async def recv_chat(
    stream: grpc.aio.UnaryStreamCall[
        leapfrogai.ChatCompletionRequest, leapfrogai.ChatCompletionResponse
    ]
):
    async for c in stream:
        yield ChatCompletionResponse()
