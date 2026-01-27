from datetime import datetime
from config.constants import LEVELS

def create_session(username):
    return {
        "username": username,
        "current_level": "A1",
        "current_question": 0,
        "current_turn": 0,  # 0 = AI attack, 1 = Human attack
        "human_score": 0,
        "ai_score": 0,
        "turns": [],
        "first_turn":True,
        "status": "active",
        "active_code":"",
        "code_history":[],
        "created_at": datetime.utcnow()
    }
