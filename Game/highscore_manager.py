import json
from game_variables.game_variables import GameVariables

def load_scores():
    try:
        with open(GameVariables.HIGHSCORE_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_scores(scores):
    with open(GameVariables.HIGHSCORE_FILE, "w") as f:
        json.dump(scores, f)

def update_score(player_name, score, force_save=False):
    scores = load_scores()
    if isinstance(scores.get(player_name), int):
        scores[player_name] = {"score": scores[player_name], "upgrades": {}}
    elif player_name not in scores:
        scores[player_name] = {"score": 0, "upgrades": {}}

    # Wenn force_save → immer überschreiben
    if force_save or score > scores[player_name]["score"]:
        scores[player_name]["score"] = score

    scores[player_name]["upgrades"] = {
        "HAS_SHIELD": GameVariables.HAS_SHIELD,
        "HAS_SPEED": GameVariables.HAS_SPEED,
        "HAS_DOUBLEJUMP": GameVariables.HAS_DOUBLEJUMP,
        "HAS_MULTIPLIER": GameVariables.HAS_MULTIPLIER,
        "HAS_EXTRA_LIFE": GameVariables.HAS_EXTRA_LIFE,
    }
    save_scores(scores)
