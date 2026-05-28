from fastapi import FastAPI
from pydantic import BaseModel

from src.graph.education_graph import app

api = FastAPI()

class ChatRequest(BaseModel):
    message: str

@api.post("/chat")
def chat(req: ChatRequest):

    result = app.invoke({
        "user_input": req.message
    })

    print(result)

    return result