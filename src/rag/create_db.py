from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # vai para a pasta src

knowledge_dir = BASE_DIR / "knowledge"

docs = []

for arquivo in knowledge_dir.glob("*.pdf"):
    loader = PyPDFLoader(str(arquivo))
    docs.extend(loader.load())

# separa em chunks (linhas)
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = splitter.split_documents(docs)

# "traduz" valor semântico em vetor
embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

# cria base vetorial
db = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

print("Base criada")