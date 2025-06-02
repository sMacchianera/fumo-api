from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)

def get_world_deaths():
    try:
        url = "https://www.worldometers.info/smoking/"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        counter = soup.find("span", {"rel": "current_population"})
        number = int(counter.text.replace(",", ""))
        return number
    except Exception as e:
        return None

def estimate_italy_deaths():
    # Stima su base annua (fonte ISS): 93.000 morti
    deaths_per_year = 93000
    now = datetime.now()
    start_of_year = datetime(now.year, 1, 1)
    seconds_passed = (now - start_of_year).total_seconds()
    seconds_per_year = 365.25 * 24 * 3600
    estimated = int((seconds_passed / seconds_per_year) * deaths_per_year)
    return estimated

@app.route("/api/fumo")
def fumo_data():
    world = get_world_deaths()
    italy = estimate_italy_deaths()
    if world is None:
        return jsonify({"error": "World data unavailable"}), 503
    return jsonify({
        "world_deaths": world,
        "italy_estimate": italy
    })

if __name__ == "__main__":
    app.run(debug=True)
