from flask import Flask, render_template, jsonify
import requests
import json

app = Flask(__name__)

# Load anime list from JSON file
def load_anime_list(filename):
    with open(filename, 'r') as file:
        return json.load(file)

anime_list = load_anime_list("anime_list.json")

# Fetch anime info from API
def get_anime_info(title):
    response = requests.get(f"https://api.jikan.moe/v4/anime", params={"q": title, "limit": 1})
    if response.status_code == 200:
        data = response.json()
        if data["data"]:
            anime = data["data"][0]
            return {
                "title": anime["title"],
                "score": anime.get("score", "N/A"),
                "synopsis": anime.get("synopsis", "No synopsis available."),
                "image_url": anime["images"]["jpg"]["image_url"]
            }
    return None

@app.route('/')
def index():
    # Get the first anime as a default
    anime_data = get_anime_info(anime_list[0])
    return render_template("index.html", anime=anime_data, index=0, max_index=len(anime_list)-1)

@app.route('/anime/<int:index>')
def anime(index):
    anime_data = get_anime_info(anime_list[index]) if 0 <= index < len(anime_list) else None
    return jsonify(anime_data)

if __name__ == '__main__':
    app.run(debug=True)
