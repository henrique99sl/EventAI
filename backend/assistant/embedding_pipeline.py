"""
Pipeline para extrair dados do banco, gerar embeddings e indexar no ChromaDB.
Dependências:
    pip install langchain chromadb sentence-transformers
"""

import os
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

# Configurações
CHROMA_COLLECTION = "eventai_docs"
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")


def get_event_documents():
    """
    Troque por uma função que extrai do seu banco real!
    Exemplo de retorno: lista de dicionários com id, título e texto.
    """
    return [
        {"id": "faq-1", "title": "Horário do evento", "text": "O evento começa às 9h e termina às 18h."},
        {"id": "faq-2", "title": "Localização", "text": "O evento será na Avenida Central, nº 100."},
        # Adicione mais documentos do banco!
    ]


def index_documents_in_chroma():
    # Inicializa o cliente ChromaDB
    client = chromadb.Client(Settings(
        persist_directory=CHROMA_PERSIST_DIR
    ))
    try:
        collection = client.get_collection(CHROMA_COLLECTION)
    except Exception:
        collection = client.create_collection(CHROMA_COLLECTION)

    # Carrega modelo de embeddings
    embedder = SentenceTransformer(EMBEDDING_MODEL)
    docs = get_event_documents()
    texts = [doc["text"] for doc in docs]
    ids = [doc["id"] for doc in docs]
    metadatas = [{"title": doc["title"]} for doc in docs]

    embeddings = embedder.encode(texts)

    # Indexa documentos no Chroma
    collection.add(
        embeddings=embeddings.tolist(),
        documents=texts,
        metadatas=metadatas,
        ids=ids,
    )
    # Persiste no disco
    client.persist()
    print(f"Indexados {len(docs)} documentos em ChromaDB.")


if __name__ == "__main__":
    index_documents_in_chroma()
