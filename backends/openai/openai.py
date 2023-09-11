from fastapi import APIRouter

router = APIRouter()
stop_token  = "<|im_end|>"

# class OpenAI_Handler:
#     stoptoken: str # TODO: This should be moved to the .toml files for each model

#     def __init__(self):
#         self.stoptoken = "<|im_end|>"


@router.get("/openai")
async def openai_route():
    return {"Hello": "World"}