from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Base URL of the API
API_BASE_URL = "https://my-json-server.typicode.com/VincentPeters/videogame-api"


@app.route("/")
def home():
    url = f"{API_BASE_URL}/platform"
    print(url)
    # Fetch all platforms
    response = requests.get(url)
    if response.status_code == 200:
        platforms = response.json()
    else:
        platforms = []
    return render_template("home.html", platforms=platforms)


@app.route("/platforms/<int:platform_id>")
def platform(platform_id):
    # Fetch the selected platform
    platform_response = requests.get(f"{API_BASE_URL}/platform/{platform_id}")
    if platform_response.status_code == 200:
        platform = platform_response.json()
    else:
        platform = None

    # Fetch games for the selected platform
    games_response = requests.get(f"{API_BASE_URL}/games?platform={platform_id}")
    if games_response.status_code == 200:
        games = games_response.json()
    else:
        games = []

    return render_template("platform.html", platform=platform, games=games)


@app.route("/games/<int:game_id>")
def game(game_id):
    # Fetch the selected game
    response = requests.get(f"{API_BASE_URL}/games/{game_id}")
    if response.status_code == 200:
        game = response.json()
    else:
        game = None
    return render_template("game.html", game=game)


app.run(host="0.0.0.0", port=5000)
