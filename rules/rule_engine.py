import json


def load_rules():
    with open("rules/conservation_rules.json", "r") as f:
        return json.load(f)


def match_condition(value, condition):
    """
    value: actual input value (number or string)
    condition: rule condition (e.g. '>15', '8-15', 'Sandy', 'High')
    """
    # Numeric conditions
    if isinstance(value, (int, float)):
        if condition.startswith(">"):
            return value > float(condition[1:])
        if condition.startswith("<"):
            return value < float(condition[1:])
        if "-" in condition:
            low, high = condition.split("-")
            return float(low) <= value <= float(high)

    # Categorical match
    return str(value).lower() == str(condition).lower()


def rule_matches(rule_conditions, input_data):
    """
    Check if all conditions of a rule match input data
    """
    for key, condition in rule_conditions.items():
        if key not in input_data:
            return False
        if not match_condition(input_data[key], condition):
            return False
    return True


def get_measures(input_data):
    rules = load_rules()
    matched = []

    for rule in rules:
        if rule_matches(rule["condition"], input_data):
            matched.append({
                "measure": rule["measure"],
                "priority": rule["priority"],
                "explanation": rule.get("explanation", "")
            })

    return matched

