# Integração LangChain + Chroma no EventAI Backend

Este guia mostra como implementar um **Assistente Virtual Inteligente** no backend Flask, usando LangChain para orquestração LLM e Chroma para busca semântica.

---

## 1. Instalação dos Pacotes

Adicione ao `requirements.txt`:

```
langchain
chromadb
openai
sentence-transformers
```

Instale:

```bash
pip install langchain chromadb openai sentence-transformers
```

---

## 2. Estrutura Recomendada

Sugestão de organização (backend/):

```
backend/
  assistants/
    __init__.py
    event_assistant.py   # Lógica do assistente virtual
  ...
```

---

## 3. Setup: ChromaDB + Embeddings

Crie `assistants/event_assistant.py`:

```python name=assistants/event_assistant.py
import chromadb
from sentence_transformers import SentenceTransformer
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

# Configuração do modelo de embeddings
EMBEDDINGS_MODEL = "all-MiniLM-L6-v2"  # Rápido e bom para PT/EN
embedder = SentenceTransformer(EMBEDDINGS_MODEL)

# Inicializar ChromaDB local
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="eventai_docs")

def index_documents(docs):
    """Indexa documentos relevantes no ChromaDB"""
    texts = [doc['text'] for doc in docs]
    embeddings = embedder.encode(texts)
    for doc, emb in zip(docs, embeddings):
        collection.add(
            documents=[doc['text']],
            embeddings=[emb.tolist()],
            metadatas=[doc]
        )

def semantic_search(query, top_k=3):
    """Busca semântica nos documentos indexados"""
    emb_query = embedder.encode([query])[0]
    results = collection.query(
        query_embeddings=[emb_query.tolist()],
        n_results=top_k
    )
    return results['documents'], results['metadatas']

def answer_question(question, docs):
    """Gera resposta usando LLM contextualizado com docs"""
    # Construa prompt contextualizado
    context = "\n".join([doc['text'] for doc in docs])
    prompt = f"Baseado nas informações abaixo, responda à pergunta:\n\n{context}\n\nPergunta: {question}"
    llm = OpenAI(temperature=0.2, model="gpt-3.5-turbo")  # Ou outro LLM
    answer = llm(prompt)
    return answer

# Exemplo: indexação inicial (rodar uma vez no setup do projeto)
# docs = [
#     {"text": "A palestra de abertura será às 9h no Auditório 1", "tipo": "agenda"},
#     {"text": "O evento será no Centro de Convenções, Rua X", "tipo": "localizacao"}
# ]
# index_documents(docs)
```

---

## 4. Endpoint Flask para Perguntas

No `app.py` ou `routes/chatbot.py`:

```python name=routes/chatbot.py
from flask import Blueprint, request, jsonify
from assistants.event_assistant import semantic_search, answer_question

bp = Blueprint('chatbot', __name__)

@bp.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get('question')
    if not question:
        return jsonify({"error": "Pergunta não informada"}), 400

    # Busca semântica nos docs
    docs, metas = semantic_search(question)
    # Gera resposta LLM
    resposta = answer_question(question, metas)
    return jsonify({"resposta": resposta, "contextos": metas})
```

No `app.py`:

```python name=app.py
from routes.chatbot import bp as chatbot_bp
app.register_blueprint(chatbot_bp)
```

---

## 5. Como Popular a Base Chroma

- Extraia textos de **agenda**, **FAQ**, **regulamentos**, **palestrantes**, **feedbacks** do banco de dados (PostgreSQL).
- Use um script para transformar cada registro relevante em embedding e indexar via `index_documents`.
- Agende reindexações sempre que houver alteração significativa nesses dados.

---

## 6. Segurança e Performance

- Limite o número de buscas e tamanho dos contextos.
- Cache respostas frequentes (Redis).
- Rate limit no endpoint `/ask`.
- Proteja API do OpenAI (env/secret).

---

## 7. Teste Rápido

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Onde será a palestra de abertura?"}'
```

---

## 8. Expansão

- Adicione personalização no contexto (perfil do usuário).
- Use feedbacks para atualizar docs indexados.
- Permita uploads de novos documentos pelo admin.

---

## 9. Referências

- [LangChain Docs](https://python.langchain.com/)
- [ChromaDB Docs](https://docs.trychroma.com/)
- [Sentence Transformers](https://www.sbert.net/)
- [OpenAI GPT API](https://platform.openai.com/docs/)

---

**Dúvidas? Sugestões? Contribua!**