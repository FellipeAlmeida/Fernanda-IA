import traceback

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.graph.education_graph import app as graph_app

api = FastAPI()


class ChatRequest(BaseModel):
    conversation_id: int
    message: str


@api.post("/chat")
def chat(req: ChatRequest):
    config = {"configurable": {"thread_id": f"conversa-{req.conversation_id}"}}

    try:
        result = graph_app.invoke({"user_input": req.message}, config=config)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {e}")

    final_response = result.get("final_response")

    if not final_response:
        raise HTTPException(
            status_code=500,
            detail=f"O grafo terminou sem final_response. Intenção: {result.get('intent')}",
        )

    return {"final_response": final_response}