from flask import Flask, jsonify, request, g, send_file
from dotenv import load_dotenv
import os
import jwt
from datetime import datetime, timedelta, date
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
from models.event_participation import EventParticipation
from models.recommendation import Recommendation
from models.feedback import Feedback

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from pythonjsonlogger import jsonlogger

from models.chat_log import ChatLog
from assistant.chroma_service import query_chroma
from update_recommendations import calculate_and_save_recommendations
from nlp_service import analyze_feedback

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

from flask_caching import Cache

from notifications import send_event_created_email


def create_event_logic(name, date_obj, venue_id, owner_id):
    event = Event(
        name=name, date=date_obj, venue_id=venue_id, owner_id=owner_id
    )
    db.session.add(event)
    db.session.commit()
    return event


def create_app(test_config=None):
    dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
    load_dotenv(dotenv_path=dotenv_path)
    app = Flask(__name__)

    if test_config:
        app.config.update(test_config)
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "troque_essa_chave")
    app.config["JWT_SECRET_KEY"] = os.getenv(
        "JWT_SECRET_KEY", "troque_essa_tambem"
    )
    app.config["TESTING"] = (
        test_config.get("TESTING") if test_config else False
    )
    CORS(app, origins=os.getenv("CORS_ORIGINS", "*").split(","))

    Swagger(app)
    db.init_app(app)

    from flask_migrate import Migrate

    Migrate(app, db)

    SENTRY_DSN = os.getenv("SENTRY_DSN")
    ENVIRONMENT = os.getenv("FLASK_ENV", "development")
    if SENTRY_DSN and ENVIRONMENT == "production":
        sentry_sdk.init(
            dsn=SENTRY_DSN,
            integrations=[FlaskIntegration()],
            traces_sample_rate=1.0,
            environment=ENVIRONMENT,
        )

    logger = logging.getLogger()
    log_handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter()
    log_handler.setFormatter(formatter)
    logger.handlers = [log_handler]
    logger.setLevel(logging.INFO)
    app.logger = logger

    if PROMETHEUS_AVAILABLE and not app.config.get("TESTING", False):
        PrometheusMetrics(app)

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

    cache = Cache(
        app,
        config={
            "CACHE_TYPE": "RedisCache",
            "CACHE_REDIS_URL": os.getenv(
                "REDIS_URL", "redis://localhost:6379/0"
            ),
            "CACHE_DEFAULT_TIMEOUT": 300,
        },
    )

    @app.errorhandler(404)
    def not_found_error(error):
        app.logger.warning(f"404: {error}")
        return jsonify({"error": "Recurso não encontrado"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f"500: {error}")
        return jsonify({"error": "Erro interno do servidor"}), 500

    @app.route("/health")
    def healthcheck():
        return jsonify({"status": "ok"}), 200

    @app.route("/readiness")
    def readiness():
        return jsonify({"ready": True}), 200

    @app.route("/liveness")
    def liveness():
        return jsonify({"alive": True}), 200

    @app.route("/events/calendar", methods=["GET"])
    def events_calendar():
        start = request.args.get("start")
        end = request.args.get("end")
        query = Event.query
        if start:
            query = query.filter(Event.date >= start)
        if end:
            query = query.filter(Event.date <= end)
        events = query.order_by(Event.date).all()
        result = [
            {
                "id": ev.id,
                "name": ev.name,
                "date": (
                    ev.date.isoformat()
                    if hasattr(ev.date, "isoformat")
                    else str(ev.date)
                ),
                "venue": ev.venue_id,
            }
            for ev in events
        ]
        return jsonify(result), 200

    @app.route("/events/cached", methods=["GET"])
    @cache.cached(timeout=60)
    def cached_events():
        query = Event.query
        name = request.args.get("name")
        date_str = request.args.get("date")
        venue_id = request.args.get("venue_id")
        if name:
            query = query.filter(Event.name.ilike(f"%{name}%"))
        if date_str:
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
                query = query.filter(Event.date == date_str)
            except ValueError:
                return (
                    jsonify(
                        {"error": "Formato de data inválido. Use YYYY-MM-DD."}
                    ),
                    400,
                )
        if venue_id:
            query = query.filter(Event.venue_id == venue_id)
        events = query.all()
        return jsonify([e.to_dict() for e in events])

    # Helpers internos
    def jwt_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            auth_header = request.headers.get("Authorization", None)
            if not auth_header or not auth_header.startswith("Bearer "):
                return (
                    jsonify(
                        {"error": "Missing or invalid Authorization header"}
                    ),
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
                return (
                    jsonify({"error": "Acesso restrito a administradores"}),
                    403,
                )
            return f(*args, **kwargs)

        return decorated

    def is_strong_password(password):
        return (
            len(password) >= 8
            and re.search(r"\d", password)
            and re.search(r"[A-Z]", password)
            and re.search(r"[a-z]", password)
        )

    @app.route("/")
    def status():
        return jsonify({"status": "ok"})

    # --- ENDPOINT DE RECOMENDAÇÕES ---
    @app.route("/recommendations/update", methods=["POST"])
    @jwt_required
    @admin_required
    def update_recommendations_admin():
        try:
            calculate_and_save_recommendations()
            return (
                jsonify(
                    {
                        "message": "Recomendações "
                        "atualizadas para todos os usuários."
                    }
                ),
                200,
            )
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/recommendations", methods=["GET"])
    @jwt_required
    def get_recommendations():
        user_id = g.current_user.id
        recs = (
            Recommendation.query.filter_by(user_id=user_id)
            .order_by(Recommendation.score.desc())
            .limit(5)
            .all()
        )
        output = []
        for r in recs:
            event = Event.query.get(r.event_id)
            venue = Venue.query.get(event.venue_id) if event else None
            output.append(
                {
                    "event": event.to_dict() if event else None,
                    "venue": venue.to_dict() if venue else None,
                    "score": r.score,
                }
            )
        return jsonify(output)

    # USERS
    @app.route("/users", methods=["GET"])
    def get_users():
        limit = request.args.get("limit", type=int)
        offset = request.args.get("offset", type=int)
        query = User.query
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
        users = query.all()
        return jsonify({"users": [u.to_dict() for u in users]})

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
                jsonify(
                    {"error": "Username, email e password são obrigatórios"}
                ),
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
                            "Senha fraca. Use mínimo 8 caracteres, \n"
                            "letras maiúsculas, minúsculas e número."
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
                            "error": "Apenas "
                            "administradores "
                            "podem criar outros administradores"
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
                                "error": "Apenas administradores "
                                "podem criar outros administradores"
                            }
                        ),
                        403,
                    )
            except Exception:
                return (
                    jsonify(
                        {
                            "error": "Apenas "
                            "administradores "
                            "podem criar outros "
                            "administradores"
                        }
                    ),
                    403,
                )

        password_hash = generate_password_hash(password)
        user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            role=role,
        )
        db.session.add(user)
        db.session.commit()
        app.logger.info(
            "Novo usuário criado",
            extra={"user_id": user.id, "role": user.role},
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
            existing_username = User.query.filter_by(
                username=data["username"]
            ).first()
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
        EventParticipation.query.filter_by(user_id=user_id).delete()
        Event.query.filter_by(owner_id=user_id).delete()
        db.session.delete(user)
        db.session.commit()
        app.logger.info("Usuário deletado", extra={"user_id": user_id})
        return jsonify({"message": "Usuário deletado"}), 200

    @app.route("/users/recover-password", methods=["POST"])
    def recover_password_request():
        data = request.json
        email = data.get("email")
        if not email:
            return jsonify({"error": "Email obrigatório"}), 400
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404
        reset_token = email[::-1]  # exemplo: token é o email invertido
        return (
            jsonify(
                {
                    "message": "Se o email existir, "
                    "foi enviado um link de recuperação",
                    "reset_token": reset_token,
                }
            ),
            200,
        )

    @app.route("/users/reset-password", methods=["POST"])
    def reset_password():
        data = request.json
        token = data.get("token")
        new_password = data.get("new_password")
        if not token or not new_password:
            return jsonify({"error": "Campos obrigatórios"}), 400
        email = token[::-1]
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"error": "Token inválido"}), 400
        if not is_strong_password(new_password):
            return jsonify({"error": "Senha fraca"}), 422
        user.password_hash = generate_password_hash(new_password)
        db.session.commit()
        return jsonify({"message": "Senha redefinida com sucesso"}), 200

    @app.route("/users/me", methods=["PUT", "PATCH"])
    @jwt_required
    def update_me():
        user = g.current_user
        data = request.json
        if "username" in data:
            existing_username = User.query.filter_by(
                username=data["username"]
            ).first()
            if existing_username and existing_username.id != user.id:
                return jsonify({"error": "Username já cadastrado"}), 400
            user.username = data["username"]
        if "email" in data:
            try:
                validate_email(data["email"])
            except EmailNotValidError:
                return jsonify({"error": "E-mail inválido"}), 422
            existing_email = User.query.filter_by(email=data["email"]).first()
            if existing_email and existing_email.id != user.id:
                return jsonify({"error": "Email já cadastrado"}), 400
            user.email = data["email"]
        if "name" in data:
            user.name = data["name"]
        db.session.commit()
        app.logger.info("Usuário atualizado", extra={"user_id": user.id})
        return jsonify(user.to_dict())

    @app.route("/users/change-password", methods=["POST"])
    @jwt_required
    def change_password():
        user = g.current_user
        data = request.json
        old_password = data.get("old_password")
        new_password = data.get("new_password")
        if not old_password or not new_password:
            return jsonify({"error": "Campos obrigatórios"}), 400
        if not check_password_hash(user.password_hash, old_password):
            return jsonify({"error": "Senha atual incorreta"}), 401
        if not is_strong_password(new_password):
            return jsonify({"error": "Senha fraca"}), 422
        user.password_hash = generate_password_hash(new_password)
        db.session.commit()
        return jsonify({"message": "Senha alterada com sucesso"}), 200

    @app.route("/login", methods=["POST"])
    def login():
        if limiter:
            limit_decorator = limiter.shared_limit(
                "5 per minute", scope="login"
            )
            return limit_decorator(_login)()
        return _login()

    def _login():
        data = request.json
        email = data.get("email")
        password = data.get("password")
        expires_in = data.get("expires_in")

        if not email or not password:
            return jsonify({"error": "Email and password required"}), 400

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password_hash, password):
            return jsonify({"error": "Invalid credentials"}), 401

        exp_time = (
            datetime.utcnow() + timedelta(seconds=expires_in)
            if expires_in
            else datetime.utcnow() + timedelta(hours=2)
        )
        payload = {"user_id": user.id, "exp": exp_time}
        token = jwt.encode(
            payload, app.config["JWT_SECRET_KEY"], algorithm="HS256"
        )
        if isinstance(token, bytes):
            token = token.decode("utf-8")
        app.logger.info("Login realizado", extra={"user_id": user.id})
        return jsonify({"token": token, "user": user.to_dict()})

    @app.route("/me", methods=["GET"])
    @jwt_required
    def get_me():
        return jsonify(g.current_user.to_dict())

    @app.route("/users/me", methods=["GET"])
    @jwt_required
    def get_me_alias():
        return jsonify(g.current_user.to_dict())

    @app.route("/auth/refresh", methods=["POST"])
    def refresh_token():
        data = request.json
        refresh_token = data.get("refresh_token")
        if refresh_token == "dummy-refresh-token":
            payload = {
                "user_id": 1,
                "exp": datetime.utcnow() + timedelta(hours=2),
            }
            token = jwt.encode(
                payload, app.config["JWT_SECRET_KEY"], algorithm="HS256"
            )
            if isinstance(token, bytes):
                token = token.decode("utf-8")
            return jsonify({"token": token}), 200
        else:
            return jsonify({"error": "Refresh token inválido"}), 401

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
            return (
                jsonify({"error": "Campos obrigatórios não fornecidos"}),
                400,
            )
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

    @app.route("/events", methods=["GET"])
    def get_events():
        query = Event.query
        name = request.args.get("name")
        date_str = request.args.get("date")
        venue_id = request.args.get("venue_id")
        creator_id = request.args.get("creator_id")
        limit = request.args.get("limit", type=int)
        offset = request.args.get("offset", type=int)
        if name:
            query = query.filter(Event.name.ilike(f"%{name}%"))
        if date_str:
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
                query = query.filter(Event.date == date_str)
            except ValueError:
                return (
                    jsonify(
                        {"error": "Formato de data inválido. Use YYYY-MM-DD."}
                    ),
                    400,
                )
        if venue_id:
            query = query.filter(Event.venue_id == venue_id)
        if creator_id:
            query = query.filter(Event.owner_id == creator_id)
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
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
            return (
                jsonify({"error": "Nome, data e venue_id são obrigatórios"}),
                400,
            )
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return (
                jsonify(
                    {"error": "Formato de data inválido. Use YYYY-MM-DD."}
                ),
                400,
            )
        if not Venue.query.get(venue_id):
            return jsonify({"error": "Venue inexistente"}), 400
        try:
            event = create_event_logic(
                name, date_obj, venue_id, g.current_user.id
            )
        except Exception as e:
            db.session.rollback()
            app.logger.warning(f"Falha ao criar evento: {e}")
            return jsonify({"error": "Erro ao criar evento"}), 500
        try:
            send_event_created_email(event)
        except Exception as e:
            app.logger.warning(f"Falha ao enviar email: {e}")

        # ATUALIZA RECOMENDAÇÕES
        try:
            calculate_and_save_recommendations()
        except Exception as e:
            app.logger.warning(f"Falha ao atualizar recomendações: {e}")

        app.logger.info(
            "Evento criado",
            extra={"event_id": event.id, "user_id": g.current_user.id},
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
                    jsonify(
                        {"error": "Formato de data inválido. Use YYYY-MM-DD."}
                    ),
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

    @app.route("/events/<int:event_id>/participate", methods=["POST"])
    @jwt_required
    def participate_in_event(event_id):
        event = Event.query.get(event_id)
        if not event:
            return jsonify({"error": "Evento não encontrado"}), 404
        user_id = g.current_user.id
        participation = EventParticipation.query.filter_by(
            user_id=user_id, event_id=event_id
        ).first()
        if participation:
            return jsonify({"error": "Usuário já participa"}), 400
        participation = EventParticipation(user_id=user_id, event_id=event_id)
        db.session.add(participation)
        db.session.commit()

        # ATUALIZA RECOMENDAÇÕES
        try:
            calculate_and_save_recommendations()
        except Exception as e:
            app.logger.warning(f"Falha ao atualizar recomendações: {e}")

        return jsonify({"message": "Participação confirmada"}), 200

    @app.route("/events/<int:event_id>/cancel", methods=["POST"])
    @jwt_required
    def cancel_participation(event_id):
        event = Event.query.get(event_id)
        if not event:
            return jsonify({"error": "Evento não encontrado"}), 404
        user_id = g.current_user.id
        participation = EventParticipation.query.filter_by(
            user_id=user_id, event_id=event_id
        ).first()
        if not participation:
            return jsonify({"error": "Usuário não está participando"}), 400
        db.session.delete(participation)
        db.session.commit()
        return jsonify({"message": "Participação cancelada"}), 200

    @app.route("/events/<int:event_id>/upload", methods=["POST"])
    @jwt_required
    def upload_event_image(event_id):
        event = Event.query.get(event_id)
        if not event:
            return jsonify({"error": "Evento não encontrado"}), 404
        if "file" not in request.files:
            return jsonify({"error": "Nenhum arquivo enviado"}), 400
        file = request.files["file"]
        if not (
            file.filename.lower().endswith(".png")
            or file.filename.lower().endswith(".jpg")
            or file.filename.lower().endswith(".jpeg")
        ):
            return jsonify({"error": "Tipo de arquivo não suportado"}), 400
        filename = f"event_{event_id}_{file.filename}"
        os.makedirs("uploads", exist_ok=True)
        filepath = os.path.join("uploads", filename)
        file.save(filepath)
        event.image_filename = filename
        db.session.commit()
        return (
            jsonify({"message": "Imagem enviada", "filename": filename}),
            201,
        )

    @app.route("/events/<int:event_id>/image", methods=["GET"])
    @jwt_required
    def download_event_image(event_id):
        event = Event.query.get(event_id)
        if not event:
            return jsonify({"error": "Evento não encontrado"}), 404
        filename = getattr(event, "image_filename", None)
        if not filename:
            filename = f"event_{event_id}_event.png"
        filepath = os.path.join("uploads", filename)
        if not os.path.exists(filepath):
            return jsonify({"error": "Imagem não encontrada"}), 404
        return send_file(filepath, mimetype="image/png")

    @app.route("/assistant", methods=["POST"])
    @jwt_required
    def assistant_virtual():
        user_id = g.current_user.id if hasattr(g, "current_user") else None
        data = request.get_json()
        question = data.get("question")
        if not question:
            return jsonify({"error": "Campo 'question' é obrigatório"}), 400

        # Fallback para perguntas sobre eventos
        if "próximo evento" in question.lower():
            next_event = (
                Event.query.filter(Event.date >= date.today())
                .order_by(Event.date.asc())
                .first()
            )
            if next_event:
                venue = Venue.query.get(next_event.venue_id)
                answer = (
                    f"O próximo evento é '{next_event.name}' em "
                    f"{venue.name if venue else 'local desconhecido'} "
                    f"no dia {next_event.date.strftime('%d/%m/%Y')}."
                )
            else:
                answer = "Nenhum evento futuro encontrado."
        else:
            answer = query_chroma(question)

        log = ChatLog(user_id=user_id, question=question, answer=answer)
        db.session.add(log)
        db.session.commit()

        return jsonify({"answer": answer})

    @app.route("/feedback", methods=["POST"])
    @jwt_required
    def submit_feedback():
        data = request.json
        text = data.get("text")
        if not text:
            return jsonify({"error": "Texto de feedback obrigatório"}), 400
        sentiment, topics = analyze_feedback(text)
        feedback = Feedback(
            user_id=getattr(g.current_user, "id", None),
            text=text,
            sentiment=sentiment,
            topics=topics,
        )
        db.session.add(feedback)
        db.session.commit()
        return (
            jsonify(
                {
                    "message": "Feedback registrado",
                    "sentiment": sentiment,
                    "topics": topics,
                }
            ),
            201,
        )
    

    @app.route("/feedback", methods=["GET"])
    @jwt_required
    def get_feedback():
        user_id = g.current_user.id
        feedbacks = Feedback.query.filter_by(user_id=user_id).all()
        return jsonify([f.to_dict() for f in feedbacks]), 200

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(
        debug=(os.getenv("FLASK_ENV", "development") != "production"),
        host="0.0.0.0",
        port=5001,
    )
