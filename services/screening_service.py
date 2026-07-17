from datetime import datetime
import time

from repositories.blacklist_repository import get_blacklist
from repositories.wallet_repository import get_wallet
from repositories.ibmb_repository import get_ibmb

from services.matching_service import match_customer
from services.openai_service import explain_result


def run_screening():

    start = time.time()

    blacklist = get_blacklist()
    wallet = get_wallet()
    ibmb = get_ibmb()

    results = []

    wallet_matches = 0
    ibmb_matches = 0

    for _, customer in blacklist.iterrows():

        result = match_customer(customer, wallet, ibmb)

        if result["wallet"]:
            wallet_matches += 1

        if result["ibmb"]:
            ibmb_matches += 1

        if result["wallet"] or result["ibmb"]:
            results.append(result)

    execution_time = round(time.time() - start, 2)

    response = {

        "screening_date": datetime.utcnow().isoformat(),

        "total_blacklist": len(blacklist),

        "wallet_matches": wallet_matches,

        "ibmb_matches": ibmb_matches,

        "total_matches": len(results),

        "execution_time_seconds": execution_time,

        "records": results

    }

    response["ai_summary"] = explain_result(response)

    return response
