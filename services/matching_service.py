from services.risk_service import calculate_risk


def match_customer(blacklist_customer, wallet_df, ibmb_df):

    name = str(blacklist_customer["Name"]).strip().upper()

    nrc = str(
        blacklist_customer["NRC/Company Registration No"]
    ).strip().upper()

    result = {
        "blacklist": blacklist_customer.to_dict(),
        "wallet": [],
        "ibmb": [],
        "match_summary": []
    }

    # ------------------------
    # Wallet Matching
    # ------------------------

    for _, wallet in wallet_df.iterrows():

        wallet_name = str(wallet["Name"]).strip().upper()

        wallet_nrc = str(
            wallet["NRC/Company Registration No"]
        ).strip().upper()

        if wallet_name == name and wallet_nrc == nrc:

            match_type = "NRC_AND_NAME_EXACT"

        elif wallet_nrc == nrc:

            match_type = "NRC_EXACT"

        elif wallet_name == name:

            match_type = "NAME_EXACT"

        else:

            continue

        result["wallet"].append(wallet.to_dict())

        result["match_summary"].append({

            "system": "Wallet",

            "match_type": match_type,

            "risk": calculate_risk(match_type),

            "confidence": 100

        })

    # ------------------------
    # IBMB Matching
    # ------------------------

    for _, ibmb in ibmb_df.iterrows():

        ibmb_name = str(ibmb["Name"]).strip().upper()

        ibmb_nrc = str(
            ibmb["NRC/Company Registration No"]
        ).strip().upper()

        if ibmb_name == name and ibmb_nrc == nrc:

            match_type = "NRC_AND_NAME_EXACT"

        elif ibmb_nrc == nrc:

            match_type = "NRC_EXACT"

        elif ibmb_name == name:

            match_type = "NAME_EXACT"

        else:

            continue

        result["ibmb"].append(ibmb.to_dict())

        result["match_summary"].append({

            "system": "IBMB",

            "match_type": match_type,

            "risk": calculate_risk(match_type),

            "confidence": 100

        })

    return result
