# Use a imagem oficial do Python
FROM python:3.11-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia os requisitos e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .

# Define a variável de ambiente para o Flask
ENV FLASK_APP=app.py

# Expõe a porta padrão do Flask
EXPOSE 5000

# Comando para rodar o app Flask
CMD ["flask", "run", "--host=0.0.0.0"]