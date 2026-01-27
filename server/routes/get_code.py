from flask import Blueprint, request, jsonify
from bson import ObjectId
from db.mongo import sessions
from game.state import allowed_actions
from datetime import datetime

from ai.AiModule import AiModule
from scale.groqQueue import GroqQueue

bp = Blueprint("get_code", __name__)

groq_queue = GroqQueue(AiModule())

@bp.route("/api/get-code", methods=["GET", "POST"])
def get_code():
    if request.method == "GET":
        session = sessions.find_one({"_id": ObjectId(request.args.get("session_id"))})
    else:
        data = request.get_json(silent=True)
        session = sessions.find_one({"_id": ObjectId(data.get("session_id"))}) if data else None

    if not session:
        return jsonify({"error": "Session id is required"}), 400

    if session["status"] == "completed":
        return jsonify({
            "status": "completed",
            "human_score": session["human_score"],
            "ai_score": session["ai_score"]
        }), 200

    level = session["current_level"]
    q = session["current_question"]
    turn = session["current_turn"]

    with open(
        f"./questions/{level}/{q+1}.txt"
    ) as f:
        code = f.read()

    if session["first_turn"]:
        buggy_code = code
        session["active_code"]=buggy_code
        session["code_history"].append({
            "question": q,
            "turn": 0,
            "actor": "ai",
            "code": buggy_code,
            "timestamp": datetime.utcnow()
        })
        session["first_turn"] = False

    code_to_send=session.get("active_code",code)

    session["turn_start_time"] = datetime.utcnow()

    sessions.update_one({"_id": ObjectId(request.args.get("session_id"))},{"$set":session})

    return jsonify({
        "code": code_to_send,
        "language":"c",
        "turn": turn,
        "level": level,
        "allowed_actions": allowed_actions(turn),
    })
