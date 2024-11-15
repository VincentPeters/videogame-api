from flask import Flask, request, url_for
import requests

app = Flask(__name__)

API_BASE_URL = "https://my-json-server.typicode.com/VincentPeters/videogame-api"


@app.route("/")
def home():
    url = f"{API_BASE_URL}/platform"
    # Fetch all platforms
    response = requests.get(url)
    if response.status_code == 200:
        platforms = response.json()
    else:
        platforms = []

    # Build HTML response with links
    response_text = "<h1>Platforms</h1><ul>"
    for platform in platforms:
        platform_url = url_for("platform", platform_id=platform["id"])
        response_text += f'<li><a href="{platform_url}">{platform["name"]}</a></li>'
    response_text += "</ul>"

    return response_text


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

    if platform:
        response_text = f"<h1>Platform: {platform['name']}</h1>"
        response_text += f"<p>Description: {platform['description']}</p>"
        response_text += f"<p>Manufacturer: {platform['manufacturer']}</p>"
        response_text += f"<p>Year: {platform['year']}</p>"
        response_text += "<h2>Games Available:</h2><ul>"
        for game in games:
            game_url = url_for("game", game_id=game["id"])
            response_text += f'<li><a href="{game_url}">{game["name"]}</a></li>'
        response_text += "</ul>"
    else:
        response_text = "Platform not found."

    return response_text


@app.route("/games/<int:game_id>")
def game(game_id):
    # Fetch the selected game
    response = requests.get(f"{API_BASE_URL}/games/{game_id}")
    if response.status_code == 200:
        game = response.json()
    else:
        game = None

    if game:
        response_text = f"<h1>Game: {game['name']}</h1>"
        response_text += f"<p>Genre: {game['genre']}</p>"
        response_text += f"<p>Release Date: {game['release_date']}</p>"
        response_text += f"<p>Developer: {game['developer']}</p>"
        response_text += f"<p>Publisher: {game['publisher']}</p>"
        platform_url = url_for("platform", platform_id=game["platform"])
        response_text += (
            f'<p>Platform: <a href="{platform_url}">Platform {game["platform"]}</a></p>'
        )
    else:
        response_text = "Game not found."

    return response_text


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
