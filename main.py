from fastapi import FastAPI

# We need to import all the functions in these files so the router decorator gets processed
from backends.openai import router as openai_router
from backends.openai.routes import *
from utils import get_model_config

app = FastAPI()
app.include_router(openai_router)
get_model_config().load()
