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

    # --- Helpers internos ---
    def jwt_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            auth_header = request.headers.get('Authorization', None)
            if not auth_header or not auth_header.startswith('Bearer '):
                return jsonify({"error": "Missing or invalid Authorization header"}), 401
            token = auth_header.split(" ")[1]
            try:
                payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                return jsonify({"error": "Token expired"}), 401
            except jwt.InvalidTokenError:
                return jsonify({"error": "Invalid token"}), 401
            user = User.query.get(payload['user_id'])
            if not user:
                return jsonify({"error": "User not found"}), 401
            g.current_user = user
            return f(*args, **kwargs)
        return decorated

    def admin_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            user = g.current_user
            if user.role != "admin":
                return jsonify({"error": "Acesso restrito a administradores"}), 403
            return f(*args, **kwargs)
        return decorated

    def is_strong_password(password):
        return (
            len(password) >= 8 and
            re.search(r"\d", password) and
            re.search(r"[A-Z]", password) and
            re.search(r"[a-z]", password)
        )

    # --- Rotas ---
    @app.route("/")
    def status():
        return jsonify({"status": "ok"})

    @app.route("/users", methods=["GET"])
    def get_users():
        users = User.query.all()
        return jsonify([u.to_dict() for u in users])

    @app.route("/venues", methods=["GET"])
    def get_venues():
        venues = Venue.query.all()
        return jsonify([v.to_dict() for v in venues])

    @app.route("/events", methods=["GET"])
    def get_events():
        events = Event.query.all()
        return jsonify([e.to_dict() for e in events])

    @app.route("/users", methods=["POST"])
    def create_user():
        data = request.json
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        role = data.get("role", "user")

        if not username or not email or not password:
            return jsonify({"error": "Username, email e password são obrigatórios"}), 400

        try:
            validate_email(email)
        except EmailNotValidError:
            return jsonify({"error": "E-mail inválido"}), 400

        if not is_strong_password(password):
            return jsonify({"error": "Senha fraca. Use mínimo 8 caracteres, letras maiúsculas, minúsculas e número."}), 400

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({"error": "Email já cadastrado"}), 400

        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            return jsonify({"error": "Username já cadastrado"}), 400

        if role == "admin":
            admin_header = request.headers.get('Authorization', None)
            if not admin_header or not admin_header.startswith('Bearer '):
                return jsonify({"error": "Apenas administradores podem criar outros administradores"}), 403
            token = admin_header.split(" ")[1]
            try:
                payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
                admin_user = User.query.get(payload['user_id'])
                if not admin_user or admin_user.role != "admin":
                    return jsonify({"error": "Apenas administradores podem criar outros administradores"}), 403
            except Exception:
                return jsonify({"error": "Apenas administradores podem criar outros administradores"}), 403

        password_hash = generate_password_hash(password)
        user = User(username=username, email=email, password_hash=password_hash, role=role)
        db.session.add(user)
        db.session.commit()
        return jsonify(user.to_dict()), 201

    @app.route("/login", methods=["POST"])
    def login():
        data = request.json
        email = data.get("email")
        password = data.get("password")
        if not email or not password:
            return jsonify({"error": "Email and password required"}), 400

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password_hash, password):
            return jsonify({"error": "Invalid credentials"}), 401

        payload = {
            "user_id": user.id,
            "exp": datetime.utcnow() + timedelta(hours=2)
        }
        token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm="HS256")
        if isinstance(token, bytes):
            token = token.decode('utf-8')
        return jsonify({"token": token, "user": user.to_dict()})

    @app.route("/me", methods=["GET"])
    @jwt_required
    def get_me():
        return jsonify(g.current_user.to_dict())

    @app.route("/users/<int:user_id>", methods=["DELETE"])
    @jwt_required
    @admin_required
    def delete_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "Usuário deletado"}), 200

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)