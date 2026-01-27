from flask import Blueprint, request, jsonify
from bson import ObjectId
from datetime import datetime

from db.mongo import sessions
from game.validator import run_tests
from game.scorer import apply_score
from ai.AiModule import AiModule
from config.constants import QUESTIONS_PER_LEVEL, LEVELS
from scale.groqQueue import GroqQueue

bp = Blueprint("submit_turn", __name__)
groq_queue = GroqQueue(AiModule())

@bp.route("/api/submit-code", methods=["POST"])
def submit_code():
    data = request.json

    session = sessions.find_one({"_id": ObjectId(data["session_id"])})

    start = session["turn_start_time"]

    winner = None
    ai_corrected_code=""

    msg=""

    if session["current_turn"] == 0:
        # Human Defense -> human code check
        results = run_tests(
            session["current_level"],
            session["current_question"],
            data["code"],
            data["language"]
        )
        winner = "human" if results["overall_pass"] else "ai"

        if winner == "human":
            msg = "You got all the test cases right"
        else:
            msg = "You loose some test cases failed"

        apply_score(session, winner)

        session["turns"].append({
            "level": session["current_level"],
            "question": session["current_question"],
            "turn": session["current_turn"],
            "winner": winner,
            "duration_ms": (datetime.utcnow() - start).total_seconds() * 1000
        })
        session["code_history"].append({
            "question": session["current_question"],
            "turn": 0,
            "actor": "human",
            "code": data["code"],
            "timestamp": datetime.utcnow()
        })

        session["active_code"] = data["code"]

    else:
        # Human attack -> ai code check
        print("data code ; ", data["code"])
        corrected_ai_code = groq_queue.submit(
                            groq_queue.ai.detect_bug_by_ai,
                            data["code"]
                        )
        print("corrected CODE \n\n", corrected_ai_code)
        ai_corrected_code=corrected_ai_code
        results = run_tests(
            session["current_level"],
            session["current_question"],
            corrected_ai_code,
            data["language"]
        )
        winner = "ai" if results["overall_pass"] else "human"

        if winner == "ai":
            msg = "Ai got all the test cases right"
        else:
            msg="You won, AI was enable to find the pertubation"

        apply_score(session, winner)

        session["turns"].append({
            "level": session["current_level"],
            "question": session["current_question"],
            "turn": session["current_turn"],
            "winner": winner,
            "duration_ms": (datetime.utcnow() - start).total_seconds() * 1000
        })

        session["code_history"].append({
            "question": session["current_question"],
            "turn": 1,
            "actor": "human",
            "code": data["code"],
            "timestamp": datetime.utcnow()
        })

        session["active_code"] = data["code"]

    sessions.update_one({"_id": session["_id"]}, {"$set": session})

    return jsonify({
        "winner": winner,
        "human_score": session["human_score"],
        "ai_score": session["ai_score"],
        "status": session["status"],
        "results_info": results,
        "msg":msg,
        "ai_corrected_code":ai_corrected_code,
    })

@bp.route("/api/submit-action", methods=["POST"])
def submit_action():
    data = request.json
    session = sessions.find_one({"_id": ObjectId(data["session_id"])})
    action = data["action"]
    print("Action \n\n",action)
    if action in ["INJECT"]:
        # Move to human attack phase, same question
        session["current_turn"] = 1

    elif action in ["DETECT","SKIP"]:
        # Move to next question, reset to defense
        session["current_turn"] = 0
        session["current_question"] += 1
        session["first_turn"] = True
        session["active_code"] = None

        # level progression
        if session["current_question"] >= QUESTIONS_PER_LEVEL[session["current_level"]]:
            next_level_index = LEVELS.index(session["current_level"]) + 1
            if next_level_index >= len(LEVELS):
                session["status"] = "completed"
            else:
                session["current_level"] = LEVELS[next_level_index]
                session["current_question"] = 0

    sessions.update_one({"_id": session["_id"]}, {"$set": session})
    return jsonify({"msg": "ok"})



    