from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/api/fumo")
def fumo_data():
    try:
        url = "https://www.worldometers.info/smoking/"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)

        soup = BeautifulSoup(response.text, 'html.parser')

        # Cerca tutti i contatori (divs con classe "number")
        numbers = soup.select("div.maincounter-number")
        if not numbers:
            raise Exception("Contatore non trovato")

        # Prende il primo contatore (Deaths caused by smoking this year)
        raw_text = numbers[0].text.strip().replace(",", "")
        deaths = int(raw_text)

        return jsonify({"world_deaths": deaths})

    except Exception as e:
        return jsonify({"error": "Scraping failed", "details": str(e)}), 500
