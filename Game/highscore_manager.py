import json
from game_variables.game_variables import GameVariables

def load_scores():
    try:
        with open(GameVariables.HIGHSCORE_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_scores(scores):
    with open(GameVariables.HIGHSCORE_FILE, "w") as f:
        json.dump(scores, f, indent=4)

def update_score(name, score):
    scores = load_scores()

    if name not in scores or score > scores[name]:
        scores[name] = score

    save_scores(scores)
