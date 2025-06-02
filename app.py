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

        if response.status_code != 200:
            raise Exception(f"Errore HTTP {response.status_code}")

        soup = BeautifulSoup(response.text, "html.parser")
        number_div = soup.select_one("div.maincounter-number span")

        if not number_div:
            raise Exception("Contatore non trovato nel DOM")

        return int(number_div.text.replace(",", ""))

    except Exception as e:
        print(f"Errore scraping: {e}")
        return None

def estimate_italy_deaths():
    deaths_per_year = 93000  # Stima ISS
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
    return jsonify({
        "world_deaths": world,
        "italy_estimate": italy,
        "source": "worldometers.info"
    })

if __name__ == "__main__":
    app.run(debug=True)