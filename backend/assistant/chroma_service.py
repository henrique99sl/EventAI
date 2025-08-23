"""
Serviço para consultar ChromaDB com busca semântica.
Dependências:
    pip install langchain chromadb sentence-transformers python-dotenv
"""

import os
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv

# Carrega variáveis do .env automaticamente
load_dotenv()

CHROMA_COLLECTION = os.getenv("CHROMA_COLLECTION", "eventai_docs")
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "chroma_db")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

# Inicializa modelos e client uma vez só (boa prática para performance)
_embedder = SentenceTransformer(EMBEDDING_MODEL)
_client = chromadb.Client(Settings(persist_directory=CHROMA_PERSIST_DIR))


def get_collection():
    """Retorna a coleção, criando se não existir."""
    try:
        return _client.get_collection(CHROMA_COLLECTION)
    except Exception:
        return _client.create_collection(CHROMA_COLLECTION)


def query_chroma(question, n_results=3):
    """Consulta a coleção ChromaDB usando busca semântica."""
    collection = get_collection()
    query_embedding = _embedder.encode([question])[0].tolist()

    # Corrigido: "ids" não é permitido em include!
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["documents", "metadatas"]  # Removido "ids"
    )

    docs = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    ids = results.get("ids", [[]])[0]

    resposta = "Resultados relevantes:\n"
    for i, doc in enumerate(docs):
        titulo = metadatas[i].get('title') or metadatas[i].get('origem') or ids[i]
        resposta += f"\nTítulo: {titulo}\nTrecho: {doc}\n"
    return resposta if docs else "Nenhum resultado relevante encontrado."


if __name__ == "__main__":
    pergunta = input("Digite sua pergunta: ")
    print(query_chroma(pergunta))
