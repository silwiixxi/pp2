import json
import os

SETTINGS_FILE = "settings.json"
LEADERBOARD_FILE = "leaderboard.json"


def load_json(file, default):
    if not os.path.exists(file):
        return default
    with open(file, "r") as f:
        return json.load(f)


def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)


def load_settings():
    return load_json(SETTINGS_FILE, {
        "sound": True,
        "car_color": "red",
        "difficulty": "normal"
    })


def save_settings(settings):
    save_json(SETTINGS_FILE, settings)


def load_leaderboard():
    return load_json(LEADERBOARD_FILE, [])


def save_leaderboard(data):
    data = sorted(data, key=lambda x: x["score"], reverse=True)[:10]
    save_json(LEADERBOARD_FILE, data)