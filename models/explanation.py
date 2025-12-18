def generate_explanation(data, measures):
    """
    Generate a human-readable explanation for conservation recommendations.

    Parameters:
    data (dict): User input + model outputs
    measures (list): List of recommended conservation measures

    Returns:
    str: Explanation text
    """

    slope = data.get("slope")
    rainfall = data.get("rainfall")
    infiltration = data.get("infiltration")
    erosion_risk = data.get("erosion_risk")
    runoff_risk = data.get("runoff_risk")

    measures_text = ", ".join(measures) if measures else "appropriate conservation practices"

    explanation = f"""
Based on the site conditions, the land has a slope of {slope}%, 
annual rainfall of {rainfall} mm, and soil infiltration capacity classified as {infiltration}.

The predicted erosion risk is {erosion_risk}, while the runoff risk is {runoff_risk}.

Considering these factors, the system recommends the following conservation measures:
{measures_text}.

These measures are selected to minimize soil loss, control surface runoff, 
and improve long-term soil and water sustainability for the given land conditions.
"""

    return explanation.strip()

