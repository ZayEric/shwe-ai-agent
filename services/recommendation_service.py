def get_recommendation(risk):

    mapping = {

        "Critical": [
            "Block transaction",
            "Escalate to AML",
            "Freeze account"
        ],

        "High": [
            "Manual review",
            "Request supporting documents"
        ],

        "Medium": [
            "Enhanced Due Diligence"
        ],

        "Low": [
            "Proceed"
        ]
    }

    return mapping[risk]
