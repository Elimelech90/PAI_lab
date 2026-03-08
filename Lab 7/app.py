from flask import Flask, jsonify
import requests

app = Flask(__name__)

JOKE_API_BASE = "https://v2.jokeapi.dev/joke"

CATEGORIES = ["Any", "Programming", "Misc", "Dark", "Pun", "Spooky", "Christmas"]

def fetch_joke(category="Any", joke_type=None):
    """Fetch a joke from JokeAPI."""
    url = f"{JOKE_API_BASE}/{category}"
    params = {
        "safe-mode": True,
        "lang": "en"
    }
    if joke_type in ("single", "twopart"):
        params["type"] = joke_type

    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        if data.get("error"):
            return {"error": data.get("message", "No joke found for this category.")}

        result = {
            "category": data.get("category", category),
            "type": data.get("type"),
            "id": data.get("id"),
            "flags": data.get("flags", {}),
        }

        if data["type"] == "single":
            result["joke"] = data["joke"]
        else:
            result["setup"] = data["setup"]
            result["delivery"] = data["delivery"]

        return result

    except requests.exceptions.ConnectionError:
        return {"error": "Could not connect to JokeAPI. Check your internet connection."}
    except requests.exceptions.Timeout:
        return {"error": "Request timed out. Try again."}
    except Exception as e:
        return {"error": str(e)}


@app.route("/api/joke")
def get_joke():
    return jsonify(fetch_joke())


@app.route("/api/joke/<category>")
def get_joke_by_category(category):
    if category not in CATEGORIES:
        return jsonify({"error": f"Unknown category: {category}"}), 400
    return jsonify(fetch_joke(category=category))


@app.route("/api/joke/<category>/<joke_type>")
def get_joke_typed(category, joke_type):
    if category not in CATEGORIES:
        return jsonify({"error": f"Unknown category: {category}"}), 400
    if joke_type not in ("single", "twopart"):
        return jsonify({"error": "Type must be 'single' or 'twopart'"}), 400
    return jsonify(fetch_joke(category=category, joke_type=joke_type))


if __name__ == "__main__":
    app.run(debug=True, port=5000)