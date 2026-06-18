from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

loader = TextLoader("./src/knowledge/impostos.txt")

docs = loader.load()

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