from repositories.blacklist_repository import get_blacklist
from repositories.wallet_repository import get_wallet
from repositories.ibmb_repository import get_ibmb

from services.matching_service import match_customer

from services.openai_service import explain_result


def run_screening():

    blacklist = get_blacklist()

    wallet = get_wallet()

    ibmb = get_ibmb()

    results = []

    for _, customer in blacklist.iterrows():

        result = match_customer(

            customer,

            wallet,

            ibmb

        )

        if result["wallet"] or result["ibmb"]:

            results.append(result)

    ai_summary = explain_result(results)

    return {

        "total_blacklist": len(blacklist),

        "matched": len(results),

        "records": results,

        "ai_summary": ai_summary

    }
