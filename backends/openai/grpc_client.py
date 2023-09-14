from fastapi.responses import StreamingResponse
import leapfrogai
import grpc
from backends.openai.helpers import recv_chat, recv_completion
from backends.openai.types import CompletionResponse, CreateEmbeddingResponse

async def stream_completion(request: leapfrogai.CompletionRequest):
    async with grpc.aio.insecure_channel("leapfrog-01:50051") as channel:
        stub = leapfrogai.CompletionStreamServiceStub(channel)
        stream = stub.CompleteStream(request)

        await stream.wait_for_connection()
        return StreamingResponse(recv_completion(stream), media_type="text/event-stream")

# TODO: CLean up completion() and stream_completion() to reduce code duplication
async def completion(request: leapfrogai.CompletionRequest):
   async with grpc.aio.insecure_channel("leapfrog-01:50051") as channel:
       stub = leapfrogai.CompletionServiceStub(channel)
       response = stub.Complete(request)

       return CompletionResponse(response)




async def stream_chat_completion(request: leapfrogai.ChatCompletionRequest):
    async with grpc.aio.insecure_channel("leapfrog-01:50051") as channel:
        stub = leapfrogai.ChatCompletionStreamServiceStub(channel)
        stream = stub.ChatCompleteStream(request)

        await stream.wait_for_connection()
        return StreamingResponse(recv_chat(stream), media_type="text/event-stream")

# TODO: CLean up completion() and stream_completion() to reduce code duplication
async def chat_completion(request: leapfrogai.ChatCompletionRequest):
   async with grpc.aio.insecure_channel("leapfrog-01:50051") as channel:
       stub = leapfrogai.CompletionServiceStub(channel)
       response = stub.Complete(request)

       return CompletionResponse(response)


async def create_embeddings(request: leapfrogai.EmbeddingRequest):
    async with grpc.aio.insecure_channel("leapfrog-01:50051") as channel:
        stub = leapfrogai.EmbeddingsServiceStub(channel)
        embedding = stub.CreateEmbedding(request)

        return CreateEmbeddingResponse(embedding)