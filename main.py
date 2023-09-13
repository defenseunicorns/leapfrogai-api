from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from utils import helper
import time

# We need to import all the functions in these files so the router decorator gets processed
from backends.openai import router as openai_router
from backends.openai.routes import *

app = FastAPI()
app.include_router(openai_router)
# print(openai_router.routes)

models = helper.load_configs().models

@app.get("/")
async def root():
    return models
    # return helper.helperFunction()

async def random_streamer():
    for i in range(100):
        yield f"data: {i}\n\n"
        time.sleep(0.5)

@app.get("/streamer")
async def test_streamer():
    return StreamingResponse(random_streamer())