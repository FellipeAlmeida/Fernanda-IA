from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")

# tranforma pergunta do usuario em vetor
embeddings = OllamaEmbeddings(
    model=EMBEDDING_MODEL,
    base_url=OLLAMA_BASE_URL
)
db = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)

# calcula similaridade e retorna os 2 chunks mais próximos
retriever = db.as_retriever(
    search_kwargs={
        "k": 2
    }
)

# entrega para o especialista
def search_context(question: str):

    docs = retriever.invoke(question)

    return "\n\n".join(
        doc.page_content
        for doc in docs
    )   

