from fastapi import FastAPI

# from backends.leapfrogai import router as leapfrogai_router
# from backends.leapfrogai.routes import *

# We need to import all the functions in these files so the router decorator gets processed
from backends.openai import router as openai_router
from backends.openai.routes import *
from utils import get_model_config

app = FastAPI()
app.include_router(openai_router)
# app.include_router(leapfrogai_router)
get_model_config().load()
