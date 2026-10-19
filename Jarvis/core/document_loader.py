import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from config.config import TEMP_DIR, DB_DIR, CHUNK_SIZE, MODEL_EMBEDDING, CHUNK_SIZE, CHUNK_OVERLAP
import logging



def get_embeddings():
    """Inicialización del modelo de embeddings"""
    return OllamaEmbeddings(
        model=MODEL_EMBEDDING,  
        base_url="localhost:11434"
    )

def process_and_index_files(uploaded_files) -> Chroma:
    documents = []
    
    print("\n--- [LOG] INICIANDO PROCESAMIENTO DE ARCHIVOS ---")
    for file in uploaded_files:
        print(f"--> [LOG] Leyendo archivo: {file.name}")
        file_path = os.path.join(TEMP_DIR, file.name)
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())
        
        if file.name.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        elif file.name.endswith(".txt"):
            loader = TextLoader(file_path, encoding="utf-8")
        else:
            print(f"--> [LOG] Formato no soportado: {file.name}")
            continue
        
        loaded_doc = loader.load()
        print(f"--> [LOG] Páginas/documentos cargados de {file.name}: {len(loaded_doc)}")
        documents.extend(loaded_doc)
        
    print(f"--> [LOG] Dividiendo {len(documents)} páginas en fragmentos (chunks)...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, 
        chunk_overlap=CHUNK_OVERLAP
    )
    splits = text_splitter.split_documents(documents)
    print(f"--> [LOG] Total de fragmentos creados: {len(splits)}")
    
    print("--> [LOG] Generando embeddings con Ollama y guardando en ChromaDB...")
    vectorstore = Chroma.from_documents(
        documents=splits, 
        embedding=get_embeddings(), 
        persist_directory=DB_DIR
    )
    print("--- [LOG] INDEXACIÓN COMPLETADA CON ÉXITO ---\n")
    return vectorstore


def load_existing_vectorstore() -> Chroma:
    """Carga el vectorstore existente desde el directorio de la base de datos"""
    if os.path.exists(DB_DIR) and os.listdir(DB_DIR):
        return Chroma(persist_directory=DB_DIR, embedding_function=get_embeddings())
    return None
