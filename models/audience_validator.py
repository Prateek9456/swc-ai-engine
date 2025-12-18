from models.explanation_levels import AUDIENCE_LEVELS

def validate_audience_level(level):
    if level not in AUDIENCE_LEVELS:
        raise ValueError(
            f"Invalid audience_level. Allowed values: {list(AUDIENCE_LEVELS.keys())}"
        )

