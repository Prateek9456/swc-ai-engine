# models/explanation_levels.py

AUDIENCE_LEVELS = {
    "scientist": {
        "tone": "technical",
        "detail": "high",
        "allowed_terms": "scientific"
    },
    "extension_officer": {
        "tone": "professional",
        "detail": "medium",
        "allowed_terms": "policy_practical"
    },
    "farmer": {
        "tone": "simple",
        "detail": "low",
        "allowed_terms": "layman"
    }
}
