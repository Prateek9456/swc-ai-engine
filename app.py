from flask import Flask, request, jsonify

import pickle

# Import internal modules
from models.runoff_logic import predict_runoff
from rules.rule_engine import get_measures
from models.explanation import generate_explanation
from models.context_builder import build_decision_context
from llm.explainer_agent import build_prompt
from models.audience_validator import validate_audience_level



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

    # Build decision context for LLM
    decision_context = build_decision_context(
    slope=data["slope"],
    rainfall=data["rainfall"],
    soil_type=data["soil_type"],
    infiltration=data["infiltration"],
    erosion_risk=erosion_risk,
    runoff_risk=runoff_risk,
    selected_measures=selected_measures,
    rejected_measures=["Only vegetative barriers"]
)

    # ======================
    # Explanation Agent
    # ======================
    explanation_data = {
        "slope": data["slope"],
        "rainfall": data["rainfall"],
        "infiltration": data["infiltration"],
        "erosion_risk": erosion_risk,
        "runoff_risk": runoff_risk
    }

    explanation = generate_explanation(explanation_data, measures)

    # ======================
    # Response
    # ======================
    return jsonify({
        "erosionRisk": erosion_risk,
        "runoffRisk": runoff_risk,
        "measures": measures_data,
        "explanation": explanation
    })

@app.route("/llm-explain", methods=["POST"])
def llm_explain():
    data = request.json

    decision_context = data["decision_context"]
    question = data.get("question")

    # 👇 ADD THESE TWO LINES HERE
    audience_level = data.get("audience_level", "farmer")
    validate_audience_level(audience_level)

    # 👇 build prompt AFTER validation
    prompt = build_prompt(
        decision_context=decision_context,
        audience_level=audience_level,
        user_question=question
    )

    return jsonify({
        "llm_prompt": prompt
    })


if __name__ == "__main__":
 app.run(debug=True, port=5000)

