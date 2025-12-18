import json
from models.explanation_levels import AUDIENCE_LEVELS

def build_prompt(decision_context, audience_level, user_question=None):
    style = AUDIENCE_LEVELS[audience_level]

    prompt = f"""
You are a Soil & Water Conservation expert.

Explain the decision in a {style} manner.

Decision Context (DO NOT CHANGE):
{decision_context}

Rules:
- Do NOT suggest new measures
- Do NOT change risks
- Do NOT make predictions
"""

    if user_question:
        prompt += f"\nUser Question:\n{user_question}"

    return prompt
