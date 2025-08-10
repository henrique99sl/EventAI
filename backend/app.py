from flask import Flask, jsonify, request, g
from dotenv import load_dotenv
import os
import jwt
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import re
from email_validator import validate_email, EmailNotValidError

# Carregar variáveis de ambiente do .env
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'troque_essa_chave')

# --- Swagger ---
from flasgger import Swagger
swagger = Swagger(app)

# Importe o db do models (NÃO crie um novo aqui)
from models import db
db.init_app(app)

from flask_migrate import Migrate
migrate = Migrate(app, db)

from models.user import User
from models.venue import Venue
from models.event import Event

# --- Helper: JWT required decorator ---
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

# --- Helper: Admin required decorator ---
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = g.current_user
        if user.role != "admin":
            return jsonify({"error": "Acesso restrito a administradores"}), 403
        return f(*args, **kwargs)
    return decorated

# --- Helper: Validação de senha forte ---
def is_strong_password(password):
    return (
        len(password) >= 8 and
        re.search(r"\d", password) and
        re.search(r"[A-Z]", password) and
        re.search(r"[a-z]", password)
    )

@app.route("/")
def status():
    """
    Status do serviço
    ---
    tags:
      - healthcheck
    responses:
      200:
        description: Serviço funcionando
    """
    return jsonify({"status": "ok"})

@app.route("/users", methods=["GET"])
def get_users():
    """
    Lista todos os usuários
    ---
    tags:
      - users
    responses:
      200:
        description: Lista de usuários
    """
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])

@app.route("/venues", methods=["GET"])
def get_venues():
    """
    Lista todos os locais (venues)
    ---
    tags:
      - venues
    responses:
      200:
        description: Lista de locais
    """
    venues = Venue.query.all()
    return jsonify([v.to_dict() for v in venues])

@app.route("/events", methods=["GET"])
def get_events():
    """
    Lista todos os eventos
    ---
    tags:
      - events
    responses:
      200:
        description: Lista de eventos
    """
    events = Event.query.all()
    return jsonify([e.to_dict() for e in events])

@app.route("/users", methods=["POST"])
def create_user():
    """
    Cria um novo usuário
    ---
    tags:
      - users
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
              example: "johndoe"
            email:
              type: string
              example: "johndoe@email.com"
            password:
              type: string
              example: "SenhaForte2023"
            role:
              type: string
              example: "user"
    responses:
      201:
        description: Usuário criado
      400:
        description: Erro de validação
    """
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "user")

    if not username or not email or not password:
        return jsonify({"error": "Username, email e password são obrigatórios"}), 400

    # Validação de email (formato)
    try:
        validate_email(email)
    except EmailNotValidError:
        return jsonify({"error": "E-mail inválido"}), 400

    # Validação de senha forte
    if not is_strong_password(password):
        return jsonify({"error": "Senha fraca. Use mínimo 8 caracteres, letras maiúsculas, minúsculas e número."}), 400

    # Verifica se já existe email cadastrado
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "Email já cadastrado"}), 400

    # Verifica se já existe username cadastrado
    existing_username = User.query.filter_by(username=username).first()
    if existing_username:
        return jsonify({"error": "Username já cadastrado"}), 400

    # Garante que só admin pode criar outros admins
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
    """
    Faz login de um usuário e retorna um token JWT
    ---
    tags:
      - users
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              example: "johndoe@email.com"
            password:
              type: string
              example: "SenhaForte2023"
    responses:
      200:
        description: Login com sucesso
      400:
        description: Dados inválidos
      401:
        description: Credenciais inválidas
    """
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
    """
    Retorna os dados do usuário autenticado
    ---
    tags:
      - users
    security:
      - Bearer: []
    responses:
      200:
        description: Dados do usuário autenticado
      401:
        description: Não autorizado
    """
    return jsonify(g.current_user.to_dict())

@app.route("/users/<int:user_id>", methods=["DELETE"])
@jwt_required
@admin_required
def delete_user(user_id):
    """
    Deleta um usuário (apenas admin)
    ---
    tags:
      - users
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: ID do usuário
    security:
      - Bearer: []
    responses:
      200:
        description: Usuário deletado
      401:
        description: Não autorizado
      403:
        description: Apenas admin pode deletar
      404:
        description: Usuário não encontrado
    """
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Usuário deletado"}), 200

if __name__ == "__main__":
    app.run(debug=True)