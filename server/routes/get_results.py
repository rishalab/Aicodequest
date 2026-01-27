from flask import Blueprint, jsonify
from db.mongo import sessions

bp = Blueprint("get_result", __name__)

@bp.route("/api/get-results", methods=["GET"])
def get_result():
    try:
        all_sessions = list(sessions.find({}))

        total_sessions = len(all_sessions)
        total_no_of_participants = total_sessions
        total_bugs_solved = 0

        total_human_score = 0
        total_ai_score = 0

        human_time_sum = 0
        human_time_count = 0
        ai_time_sum = 0
        ai_time_count = 0

        total_turns = 0
        human_wins = 0
        ai_wins = 0

        leaderboard = []

        for session in all_sessions:
            per_session_human_wins = 0
            per_session_ai_wins = 0
            per_session_total_turns = 0

            username = session.get("username", "unknown")
            human_score = session.get("human_score", 0)
            ai_score = session.get("ai_score", 0)
            turns = session.get("turns", [])

            total_human_score += human_score
            total_ai_score += ai_score
            total_bugs_solved += len(turns)

            user_human_time = 0
            user_human_count = 0

            for turn in turns:
                duration = turn.get("duration_ms", 0)
                winner = turn.get("winner")
                turn_type = turn.get("turn")  # 0 = human, 1 = ai

                total_turns += 1
                per_session_total_turns += 1

                if turn_type == 0:
                    human_time_sum += duration
                    human_time_count += 1
                    user_human_time += duration
                    user_human_count += 1

                else:
                    ai_time_sum += duration
                    ai_time_count += 1

                if winner == "human":
                    human_wins += 1
                    per_session_human_wins += 1
                elif winner == "ai":
                    ai_wins += 1
                    per_session_ai_wins += 1

            avg_user_human_time = (
                user_human_time / user_human_count
                if user_human_count > 0 else 0
            )

            leaderboard.append({
                "username": username,
                "human_score": human_score,
                "ai_score": ai_score,
                "avg_human_time_ms": round(avg_user_human_time, 2),
                "bug_detection_accuracy": {
                    "human": round(per_session_human_wins / per_session_total_turns, 3)
                    if per_session_total_turns > 0 else 0,
                    "ai": round(per_session_ai_wins / per_session_total_turns, 3)
                    if per_session_total_turns > 0 else 0
                }
            })

        leaderboard.sort(
            key=lambda x: (-x["human_score"], x["avg_human_time_ms"])
        )

        total_avg_time_by_human = (
            human_time_sum / human_time_count
            if human_time_count > 0 else 0
        )

        total_avg_time_by_ai = (
            ai_time_sum / ai_time_count
            if ai_time_count > 0 else 0
        )

        return jsonify({
            "success": True,
            "summary": {
                "total_sessions": total_sessions,
                "total_participants": total_no_of_participants,
                "total_bugs_solved": total_bugs_solved,
                "total_human_score": total_human_score,
                "total_ai_score": total_ai_score,
                "avg_human_time_ms": round(total_avg_time_by_human, 2),
                "avg_ai_time_ms": round(total_avg_time_by_ai, 2),
                "bug_detection_accuracy": {
                    "human": round(human_wins / total_turns, 3) if total_turns > 0 else 0,
                    "ai": round(ai_wins / total_turns, 3) if total_turns > 0 else 0
                }
            },
            "leaderboard": leaderboard
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
