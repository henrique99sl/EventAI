import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///local.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "troque_essa_chave")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "troque_essa_tambem")
    # Adicione outros configs conforme necessário, ex:
    # CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
