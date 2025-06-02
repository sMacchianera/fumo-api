from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

def get_deaths_since_jan1(yearly_total):
    now = datetime.now()
    start_of_year = datetime(now.year, 1, 1)
    seconds_passed = (now - start_of_year).total_seconds()
    seconds_in_year = 365.25 * 24 * 60 * 60
    return int((seconds_passed / seconds_in_year) * yearly_total)

@app.route("/api/fumo")
def deaths_data():
    world_total = 8000000
    italy_total = 93000
    return jsonify({
        "world_deaths": get_deaths_since_jan1(world_total),
        "italy_deaths": get_deaths_since_jan1(italy_total),
        "source": "Simulazione basata su dati OMS e ISS",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == "__main__":
    app.run(debug=True)