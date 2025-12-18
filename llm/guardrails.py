def validate_llm_output(text):
    forbidden_phrases = [
        "I recommend a new measure",
        "override",
        "change erosion risk"
    ]

    for phrase in forbidden_phrases:
        if phrase.lower() in text.lower():
            raise ValueError("LLM violated guardrails")

    return text
