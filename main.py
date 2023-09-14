from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from utils import config, get_model_config
import time

# We need to import all the functions in these files so the router decorator gets processed
from backends.openai import router as openai_router
from backends.openai.routes import *

app = FastAPI()
app.include_router(openai_router)
# print(openai_router.routes)

# models = config.load_configs().models
get_model_config().load()

# @app.get("/")
# async def root():
#     return models