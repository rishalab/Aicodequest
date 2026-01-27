from flask import Blueprint, request, jsonify
from models.session import create_session
from db.mongo import sessions

bp = Blueprint("start_game", __name__)

@bp.route("/api/start-game", methods=["GET","POST"])
def start_game():
    if request.method == "GET":
        username = request.args.get("username")
    else:
        data = request.get_json(silent=True)
        username = data.get("username") if data else None

    if not username:
        return jsonify({"error": "username required"}), 400
        
    session = create_session(username)
    result = sessions.insert_one(session)
    session["_id"] = str(result.inserted_id)
    return jsonify(session)
