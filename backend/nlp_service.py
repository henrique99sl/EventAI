from transformers import pipeline

# Carregar pipeline HuggingFace para sentimento
sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")


def analyze_feedback(text):
    result = sentiment_analyzer(text)[0]
    sentiment = result["label"]
    # Exemplo de extração de tópicos (simples split de palavras-chave)
    # Em produção, use spaCy ou huggingface zero-shot/classification
    topics = ", ".join(set([w.lower() for w in text.split() if len(w) > 4]))
    return sentiment, topics
