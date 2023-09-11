from fastapi import FastAPI, APIRouter
from fastapi.responses import StreamingResponse
from utils import helper
from backends.openai import openai 
from backends.openai.completion import another_router
import time


app = FastAPI()

app.include_router(openai.router)
app.include_router(another_router)

@app.get("/")
async def root():
    return helper.load_configs().models
    # return helper.helperFunction()


async def random_streamer():
    for i in range(100):
        yield f"data: {i}\n\n"
        time.sleep(0.5)

@app.get("/streamer")
async def test_streamer():
    return StreamingResponse(random_streamer())