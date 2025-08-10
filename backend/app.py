from flask import Flask, jsonify, request, g
from dotenv import load_dotenv
import os
import jwt
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import re
from email_validator import validate_email, EmailNotValidError
from flasgger import Swagger
from models import db
from models.user import User
from models.venue import Venue
from models.event import Event

def create_app(test_config=None):
    load_dotenv()
    app = Flask(__name__)
    if test_config:
        app.config.update(test_config)
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'troque_essa_chave')
    Swagger(app)
    db.init_app(app)
    from flask_migrate import Migrate
    Migrate(app, db)

    # (insere aqui todas as tuas routes e helpers, tal como já tens — igual ao exemplo anterior)

    # --- Helper: JWT required decorator ---
    # ... (o resto do código das rotas, helpers, etc. igual como já tens)

    # Exemplo do healthcheck:
    @app.route("/")
    def status():
        return jsonify({"status": "ok"})

    # Copia todas as tuas rotas para dentro desta função!

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)