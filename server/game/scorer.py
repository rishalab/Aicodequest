def apply_score(session, winner):
    if winner == "human":
        session["human_score"] += 1
    else:
        session["ai_score"] += 1
