import os

TEMP_DIR ="./temp_docs"
DB_DIR = "./chroma_db"

MODEL_LLM = "llama3.2:1b"
MODEL_EMBEDDING = "nomic-embed-text"
LLM_TEMPERATURE = 0.1

CHUNK_SIZE = 10000
CHUNK_OVERLAP = 200
RETRIEVER_K = 4

os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(DB_DIR, exist_ok=True)
