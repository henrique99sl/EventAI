from flask import Blueprint, request, jsonify
from .chroma_service import query_chroma

assistant_bp = Blueprint("assistant", __name__)


@assistant_bp.route("/assistant", methods=["POST"])
def assistant():
    question = request.json.get("question")
    # Chama o serviço LangChain + Chroma
    answer = query_chroma(question)
    return jsonify({"answer": answer})
