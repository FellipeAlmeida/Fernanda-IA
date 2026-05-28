from langchain_ollama import ChatOllama
from dotenv import load_dotenv
import os

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME")

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")

llm = ChatOllama(
    model=MODEL_NAME,
    base_url=OLLAMA_BASE_URL,
    temperature=0.1,
    num_predict=120
)

def invoke_llm(prompt: str):

    response = llm.invoke(prompt)

    return response.content