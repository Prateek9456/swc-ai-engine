from flask import Flask, request, jsonify
from geo.factor_builder import build_factors
from engine.rule_engine import evaluate_rules

RULE_FILE = "rules/icar_table_4_1_mechanical_measures.json"

app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json(force=True)

    lat = data.get("lat")
    lon = data.get("lon")
    land_use = data.get("land_use")
    overrides = data.get("overrides")

    if lat is None or lon is None or land_use is None:
        return jsonify({"error": "lat, lon, land_use are required"}), 400

    factors = build_factors(lat, lon, land_use, overrides)

    result = evaluate_rules(factors, RULE_FILE)

    return jsonify({
        "location": {
            "latitude": lat,
            "longitude": lon
        },
        "factors": {
            "rainfall_mm": factors.rainfall_mm,
            "slope_percent": factors.slope_percent,
            "soil_depth": factors.soil_depth,
            "drainage": factors.drainage,
            "land_use": land_use
        },
        "mechanical_measures": {
            "mode": result["mode"],
            "measures": result["measures"],
            "land_use_considered": result["mode"] == "STRICT"
        }
    })

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
