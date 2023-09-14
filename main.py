from fastapi import FastAPI
from utils import get_model_config

# We need to import all the functions in these files so the router decorator gets processed
from backends.openai import router as openai_router
from backends.openai.routes import *

app = FastAPI()
app.include_router(openai_router)
get_model_config().load()
