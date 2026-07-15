@router.post("/blacklist")
def blacklist(data: dict):

    print("Incoming JSON:", data)

    name = data.get("name")
    nrc = data.get("nrc")

    print("Name:", repr(name))
    print("NRC:", repr(nrc))

    result = search_blacklist(name=name, nrc=nrc)

    print("Search Result:", result)

    if result is None:
        result = []

    explanation = (
        explain_result(result)
        if result
        else "No blacklist match found."
    )

    return {
        "matched": len(result) > 0,
        "records": result,
        "ai_summary": explanation
    }
