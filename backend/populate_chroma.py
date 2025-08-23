import chromadb
from chromadb.config import Settings
import os
# Use o mesmo diretório de persistência do seu backend (veja CHROMA_PERSIST_DIR)


CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "chroma_db")

client = chromadb.Client(Settings(persist_directory=CHROMA_PERSIST_DIR))

# Cria a coleção se não existir
collection_name = "eventai_docs"
try:
    collection = client.get_collection(collection_name)
except Exception:
    collection = client.create_collection(collection_name)

# Adiciona documentos
documents = [
    "O próximo evento será no dia 30 de agosto de 2025, no Centro de Convenções.",
    "Para participar dos eventos, acesse a área de inscrições no site.",
    "Os eventos são gratuitos para membros cadastrados."
]
metadatas = [
    {"origem": "agenda"},
    {"origem": "inscricao"},
    {"origem": "faq"}
]
ids = ["doc1", "doc2", "doc3"]

collection.add(documents=documents, metadatas=metadatas, ids=ids)

print("Coleção populada com sucesso!")
