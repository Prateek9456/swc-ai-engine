def predict_runoff(rainfall, infiltration):
    """
    Predict runoff risk based on rainfall and soil infiltration capacity.

    Parameters:
    rainfall (float): Annual rainfall in mm
    infiltration (str): Low / Medium / High

    Returns:
    str: Low / Medium / High runoff risk
    """

    infiltration = infiltration.capitalize()

    if rainfall > 1500 and infiltration == "Low":
        return "High"
    elif rainfall > 800:
        return "Medium"
    else:
        return "Low"

