def calculate_risk(match_type):

    if match_type == "NRC_EXACT":
        return "Critical"

    elif match_type == "NAME_EXACT":
        return "High"

    elif match_type == "FUZZY_NAME":
        return "Medium"

    else:
        return "Low"
