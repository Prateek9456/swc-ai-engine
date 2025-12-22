from flask import Flask, request, jsonify

import pickle

# Import internal modules
from models.runoff_logic import predict_runoff
from rules.rule_engine import get_measures



app = Flask(__name__)
@app.route("/", methods=["GET"])
def home():
    return "Flask is running"


# Load ML model
with open("models/erosion_model.pkl", "rb") as f:
    model = pickle.load(f)


@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    # ======================
    # Validate input
    # ======================
    required_fields = ["slope", "rainfall", "soil_type", "infiltration"]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    # ======================
    # ML Prediction
    # ======================
    erosion_risk = model.predict([[
        data["slope"],
        data["rainfall"],
        data.get("soil_type_encoded", 1)  # fallback if not provided
    ]])[0]

    # ======================
    # Runoff Logic (NO ML)
    # ======================
    runoff_risk = predict_runoff(
        rainfall=data["rainfall"],
        infiltration=data["infiltration"]
    )

    # ======================
    # Rule Engine
    # ======================
    rule_input = {
        "slope": data["slope"],
        "rainfall": data["rainfall"],
        "soil_type": data["soil_type"],
        "erosion_risk": erosion_risk
    }

    measures_data = get_measures(rule_input)
    measures = [m["measure"] for m in measures_data]

    
    # Extract selected measure names
    selected_measures = [m["measure"] for m in measures_data]

    # ======================
    # Response
    # ======================
    return jsonify({
        "erosionRisk": erosion_risk,
        "runoffRisk": runoff_risk,
        "measures": measures_data,
    })

if __name__ == "__main__":
 app.run(debug=True, port=5000)

