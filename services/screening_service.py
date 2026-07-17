def screen_customer(data):

    blacklist = blacklist_repository.load()

    wallet = wallet_repository.load()

    ibmb = ibmb_repository.load()

    result = matching_service.compare(
        blacklist,
        wallet,
        ibmb,
        data
    )

    summary = openai_service.explain_result(result)

    return {
        "matched": True,
        "summary": summary,
        "records": result
    }
