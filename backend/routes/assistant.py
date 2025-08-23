from flask import Blueprint, request, jsonify, g
from models import db
from models.chat_log import ChatLog
from assistant.chroma_service import query_chroma

assistant_bp = Blueprint("assistant", __name__)


def jwt_required_custom(f):
    # Usa o decorador customizado do app principal
    from app import jwt_required
    return jwt_required(f)


@assistant_bp.route("/assistant", methods=["POST"])
@jwt_required_custom
def assistant():
    user_id = getattr(g.current_user, "id", None)
    data = request.get_json()
    question = data.get("question")
    answer = query_chroma(question)

    # Logging das conversas
    log = ChatLog(user_id=user_id, question=question, answer=answer)
    db.session.add(log)
    db.session.commit()

    return jsonify({"answer": answer})
