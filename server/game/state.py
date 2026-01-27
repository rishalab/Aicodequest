def allowed_actions(turn_index):
    if turn_index == 0:
        return ["INJECT", "SKIP"]           # AI injected, human detects
    return ["DETECT"]       # Human attack turn
