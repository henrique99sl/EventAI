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
from flask_cors import CORS
import logging

from models import db
from models.user import User
from models.venue import Venue
from models.event import Event

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from pythonjsonlogger import jsonlogger

try:
    from prometheus_flask_exporter import PrometheusMetrics

    PROMETHEUS_AVAILABLE = True
except ImportError:
    PROMETHEUS_AVAILABLE = False

try:
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address

    RATE_LIMITER_AVAILABLE = True
except ImportError:
    RATE_LIMITER_AVAILABLE = False


def create_app(test_config=None):
    load_dotenv()
    app = Flask(__name__)

    # Configuração básica
    if test_config:
        app.config.update(test_config)
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "troque_essa_chave")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "troque_essa_tambem")
    app.config["TESTING"] = test_config.get("TESTING") if test_config else False
    CORS(app, origins=os.getenv("CORS_ORIGINS", "*").split(","))

    Swagger(app)
    db.init_app(app)

    from flask_migrate import Migrate

    Migrate(app, db)

    # --- Sentry ---
    SENTRY_DSN = os.getenv("SENTRY_DSN")
    ENVIRONMENT = os.getenv("FLASK_ENV", "development")
    if SENTRY_DSN and ENVIRONMENT == "production":
        sentry_sdk.init(
            dsn=SENTRY_DSN,
            integrations=[FlaskIntegration()],
            traces_sample_rate=1.0,
            environment=ENVIRONMENT,
        )

    # --- Logging estruturado (JSON logger) ---
    logger = logging.getLogger()
    log_handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter()
    log_handler.setFormatter(formatter)
    logger.handlers = [log_handler]
    logger.setLevel(logging.INFO)
    app.logger = logger

    # --- Prometheus métricas (somente fora de teste) ---
    if PROMETHEUS_AVAILABLE and not app.config.get("TESTING", False):
        PrometheusMetrics(app)

    # --- Flask-Limiter para rate limiting (com Redis para multi-pod) ---
    limiter = None
    if RATE_LIMITER_AVAILABLE and not app.config.get("TESTING"):
        limiter_storage_uri = os.getenv("REDIS_URL", "memory://")
        limiter_default = ["200 per day", "50 per hour"]
        limiter = Limiter(
            get_remote_address,
            app=app,
            storage_uri=limiter_storage_uri,
            default_limits=limiter_default,
        )

    # --- Handlers globais de erro ---
    @app.errorhandler(404)
    def not_found_error(error):
        app.logger.warning(f"404: {error}")
        return jsonify({"error": "Recurso não encontrado"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f"500: {error}")
        return jsonify({"error": "Erro interno do servidor"}), 500

    # --- Endpoint /health ---
    @app.route("/health")
    def health():
        return jsonify({"status": "ok"}), 200

    # --- Helpers internos ---
    def jwt_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            auth_header = request.headers.get("Authorization", None)
            if not auth_header or not auth_header.startswith("Bearer "):
                return (
                    jsonify({"error": "Missing or invalid Authorization header"}),
                    401,
                )
            token = auth_header.split(" ")[1]
            try:
                payload = jwt.decode(
                    token, app.config["JWT_SECRET_KEY"], algorithms=["HS256"]
                )
            except jwt.ExpiredSignatureError:
                return jsonify({"error": "Token expired"}), 401
            except jwt.InvalidTokenError:
                return jsonify({"error": "Invalid token"}), 401
            user = User.query.get(payload["user_id"])
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
            len(password) >= 8
            and re.search(r"\d", password)
            and re.search(r"[A-Z]", password)
            and re.search(r"[a-z]", password)
        )

    # --- Rotas ---
    @app.route("/")
    def status():
        return jsonify({"status": "ok"})

    # USERS
    @app.route("/users", methods=["GET"])
    def get_users():
        users = User.query.all()
        return jsonify([u.to_dict() for u in users])

    @app.route("/users/<int:user_id>", methods=["GET"])
    @jwt_required
    def get_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404
        return jsonify(user.to_dict())

    @app.route("/users", methods=["POST"])
    def create_user():
        data = request.json
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        role = data.get("role", "user")

        if not username or not email or not password:
            return (
                jsonify({"error": "Username, email e password são obrigatórios"}),
                400,
            )

        try:
            validate_email(email)
        except EmailNotValidError:
            return jsonify({"error": "E-mail inválido"}), 400

        if not is_strong_password(password):
            return (
                jsonify(
                    {
                        "error": (
                            "Senha fraca. Use mínimo 8 caracteres, letras "
                            "maiúsculas, minúsculas e número."
                        )
                    }
                ),
                400,
            )

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({"error": "Email já cadastrado"}), 400

        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            return jsonify({"error": "Username já cadastrado"}), 400

        if role == "admin":
            admin_header = request.headers.get("Authorization", None)
            if not admin_header or not admin_header.startswith("Bearer "):
                return (
                    jsonify(
                        {
                            "error": (
                                "Apenas administradores podem criar outros "
                                "administradores"
                            )
                        }
                    ),
                    403,
                )
            token = admin_header.split(" ")[1]
            try:
                payload = jwt.decode(
                    token, app.config["JWT_SECRET_KEY"], algorithms=["HS256"]
                )
                admin_user = User.query.get(payload["user_id"])
                if not admin_user or admin_user.role != "admin":
                    return (
                        jsonify(
                            {
                                "error": (
                                    "Apenas administradores podem criar outros "
                                    "administradores"
                                )
                            }
                        ),
                        403,
                    )
            except Exception:
                return (
                    jsonify(
                        {
                            "error": (
                                "Apenas administradores podem criar outros "
                                "administradores"
                            )
                        }
                    ),
                    403,
                )

        password_hash = generate_password_hash(password)
        user = User(
            username=username, email=email, password_hash=password_hash, role=role
        )
        db.session.add(user)
        db.session.commit()
        app.logger.info(
            "Novo usuário criado", extra={"user_id": user.id, "role": user.role}
        )
        return jsonify(user.to_dict()), 201

    @app.route("/users/<int:user_id>", methods=["PUT", "PATCH"])
    @jwt_required
    def update_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404
        data = request.json
        if "username" in data:
            existing_username = User.query.filter_by(username=data["username"]).first()
            if existing_username and existing_username.id != user.id:
                return jsonify({"error": "Username já cadastrado"}), 400
            user.username = data["username"]
        if "email" in data:
            try:
                validate_email(data["email"])
            except EmailNotValidError:
                return jsonify({"error": "E-mail inválido"}), 400
            existing_email = User.query.filter_by(email=data["email"]).first()
            if existing_email and existing_email.id != user.id:
                return jsonify({"error": "Email já cadastrado"}), 400
            user.email = data["email"]
        if "role" in data and g.current_user.role == "admin":
            user.role = data["role"]
        db.session.commit()
        app.logger.info("Usuário atualizado", extra={"user_id": user.id})
        return jsonify(user.to_dict())

    @app.route("/users/<int:user_id>", methods=["DELETE"])
    @jwt_required
    @admin_required
    def delete_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404
        db.session.delete(user)
        db.session.commit()
        app.logger.info("Usuário deletado", extra={"user_id": user_id})
        return jsonify({"message": "Usuário deletado"}), 200

    # LOGIN & AUTH
    @app.route("/login", methods=["POST"])
    def login():
        # Só aplica rate-limit se não estiver em modo de teste
        if limiter:
            limit_decorator = limiter.shared_limit("5 per minute", scope="login")
            return limit_decorator(_login)()
        return _login()

    def _login():
        data = request.json
        email = data.get("email")
        password = data.get("password")
        if not email or not password:
            return jsonify({"error": "Email and password required"}), 400

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password_hash, password):
            return jsonify({"error": "Invalid credentials"}), 401

        payload = {"user_id": user.id, "exp": datetime.utcnow() + timedelta(hours=2)}
        token = jwt.encode(payload, app.config["JWT_SECRET_KEY"], algorithm="HS256")
        if isinstance(token, bytes):
            token = token.decode("utf-8")
        app.logger.info("Login realizado", extra={"user_id": user.id})
        return jsonify({"token": token, "user": user.to_dict()})

    @app.route("/me", methods=["GET"])
    @jwt_required
    def get_me():
        return jsonify(g.current_user.to_dict())

    # VENUES
    @app.route("/venues", methods=["GET"])
    def get_venues():
        venues = Venue.query.all()
        return jsonify([v.to_dict() for v in venues])

    @app.route("/venues/<int:venue_id>", methods=["GET"])
    def get_venue(venue_id):
        venue = Venue.query.get(venue_id)
        if not venue:
            return jsonify({"error": "Venue não encontrado"}), 404
        return jsonify(venue.to_dict())

    @app.route("/venues", methods=["POST"])
    @jwt_required
    def create_venue():
        data = request.json
        name = data.get("name")
        address = data.get("address")
        if not name or not address:
            return jsonify({"error": "Nome e endereço são obrigatórios"}), 400
        venue = Venue(name=name, address=address)
        db.session.add(venue)
        db.session.commit()
        app.logger.info("Venue criado", extra={"venue_id": venue.id})
        return jsonify(venue.to_dict()), 201

    @app.route("/venues/<int:venue_id>", methods=["PUT", "PATCH"])
    @jwt_required
    def update_venue(venue_id):
        venue = Venue.query.get(venue_id)
        if not venue:
            return jsonify({"error": "Venue não encontrado"}), 404
        data = request.json or {}
        if "name" not in data or "address" not in data:
            return jsonify({"error": "Campos obrigatórios não fornecidos"}), 400
        venue.name = data["name"]
        venue.address = data["address"]
        db.session.commit()
        app.logger.info("Venue atualizado", extra={"venue_id": venue.id})
        return jsonify(venue.to_dict())

    @app.route("/venues/<int:venue_id>", methods=["DELETE"])
    @jwt_required
    def delete_venue(venue_id):
        venue = Venue.query.get(venue_id)
        if not venue:
            return jsonify({"error": "Venue não encontrado"}), 404
        db.session.delete(venue)
        db.session.commit()
        app.logger.info("Venue deletado", extra={"venue_id": venue_id})
        return jsonify({"message": "Venue deletado"}), 200

    # EVENTS
    @app.route("/events", methods=["GET"])
    def get_events():
        query = Event.query
        name = request.args.get("name")
        date = request.args.get("date")
        venue_id = request.args.get("venue_id")
        if name:
            query = query.filter(Event.name.ilike(f"%{name}%"))
        if date:
            try:
                datetime.strptime(date, "%Y-%m-%d")
                query = query.filter(Event.date == date)
            except ValueError:
                return (
                    jsonify({"error": "Formato de data inválido. Use YYYY-MM-DD."}),
                    400,
                )
        if venue_id:
            query = query.filter(Event.venue_id == venue_id)
        events = query.all()
        return jsonify([e.to_dict() for e in events])

    @app.route("/events/<int:event_id>", methods=["GET"])
    def get_event(event_id):
        event = Event.query.get(event_id)
        if not event:
            return jsonify({"error": "Evento não encontrado"}), 404
        return jsonify(event.to_dict())

    @app.route("/events", methods=["POST"])
    @jwt_required
    def create_event():
        data = request.json
        name = data.get("name")
        date_str = data.get("date")
        venue_id = data.get("venue_id")
        if not name or not date_str or not venue_id:
            return jsonify({"error": "Nome, data e venue_id são obrigatórios"}), 400
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Formato de data inválido. Use YYYY-MM-DD."}), 400
        if not Venue.query.get(venue_id):
            return jsonify({"error": "Venue inexistente"}), 400
        event = Event(
            name=name, date=date_obj, venue_id=venue_id, owner_id=g.current_user.id
        )
        db.session.add(event)
        db.session.commit()
        app.logger.info(
            "Evento criado", extra={"event_id": event.id, "user_id": g.current_user.id}
        )
        return jsonify(event.to_dict()), 201

    @app.route("/events/<int:event_id>", methods=["PUT", "PATCH"])
    @jwt_required
    def update_event(event_id):
        event = Event.query.get(event_id)
        if not event:
            return jsonify({"error": "Evento não encontrado"}), 404
        if (
            hasattr(event, "owner_id")
            and event.owner_id != g.current_user.id
            and g.current_user.role != "admin"
        ):
            return jsonify({"error": "Sem permissão"}), 403
        data = request.json or {}
        if "name" in data:
            event.name = data["name"]
        if "date" in data:
            try:
                date_obj = datetime.strptime(data["date"], "%Y-%m-%d").date()
                event.date = date_obj
            except ValueError:
                return (
                    jsonify({"error": "Formato de data inválido. Use YYYY-MM-DD."}),
                    400,
                )
        if "venue_id" in data:
            if not Venue.query.get(data["venue_id"]):
                return jsonify({"error": "Venue inexistente"}), 400
            event.venue_id = data["venue_id"]
        db.session.commit()
        app.logger.info(
            "Evento atualizado",
            extra={"event_id": event.id, "user_id": g.current_user.id},
        )
        return jsonify(event.to_dict())

    @app.route("/events/<int:event_id>", methods=["DELETE"])
    @jwt_required
    def delete_event(event_id):
        event = Event.query.get(event_id)
        if not event:
            return jsonify({"error": "Evento não encontrado"}), 404
        if (
            hasattr(event, "owner_id")
            and event.owner_id != g.current_user.id
            and g.current_user.role != "admin"
        ):
            return jsonify({"error": "Sem permissão"}), 403
        db.session.delete(event)
        db.session.commit()
        app.logger.info(
            "Evento deletado",
            extra={"event_id": event_id, "user_id": g.current_user.id},
        )
        return jsonify({"message": "Evento deletado"}), 200

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(
        debug=(os.getenv("FLASK_ENV", "development") != "production"),
        host="0.0.0.0",
        port=5001,
    )
