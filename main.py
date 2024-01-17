from fastapi import FastAPI

# We need to import all the functions in these files so the router decorator gets processed
from backends.openai import router as openai_router
from backends.openai.routes import *
from backends.lfai import router as lfai_router
from backends.lfai.routes import *
from utils import get_model_config
import asyncio

app = FastAPI()

# super simple healthz check
@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

@app.get("/models")
async def models():
    return get_model_config()


@app.on_event('startup')
async def watch_for_configs():
    asyncio.create_task(get_model_config().watch_and_load_configs())

app.include_router(openai_router)
app.include_router(lfai_router)