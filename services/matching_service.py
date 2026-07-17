def match_customer(

    blacklist_customer,

    wallet_df,

    ibmb_df

):

    name = blacklist_customer["Name"]

    nrc = blacklist_customer["NRC/Company Registration No"]

    wallet_match = wallet_df[

        (wallet_df["Name"] == name)

        |

        (

            wallet_df["NRC/Company Registration No"]

            == nrc

        )

    ]

    ibmb_match = ibmb_df[

        (ibmb_df["Name"] == name)

        |

        (

            ibmb_df["NRC/Company Registration No"]

            == nrc

        )

    ]

    return {

        "blacklist": blacklist_customer,

        "wallet": wallet_match.to_dict("records"),

        "ibmb": ibmb_match.to_dict("records")

    }
