def build_decision_context(
    slope,
    rainfall,
    soil_type,
    infiltration,
    erosion_risk,
    runoff_risk,
    selected_measures,
    rejected_measures=None
):
    """
    This function creates a SAFE, CONTROLLED context object
    that will be passed to the LLM for explanation ONLY.
    """

    context = {
        "erosion_risk": erosion_risk,
        "runoff_risk": runoff_risk,

        # Convert raw numbers into qualitative bands
        "slope": ">15%" if slope > 15 else "≤15%",
        "rainfall": ">1500 mm" if rainfall > 1500 else "≤1500 mm",

        "soil": soil_type,
        "infiltration": infiltration,

        # Measures already selected by rule engine
        "selected_measures": selected_measures,

        # Optional: measures NOT selected
        "rejected_measures": rejected_measures or []
    }

    return context
