import json

from services.document_loader import DocumentLoader


class RetrievalService:

    def __init__(self):
        self.loader = DocumentLoader()

    def retrieve(self, question):

        question = question.lower()

        docs = self.loader.load_all()

        context = {}

        ####################################################
        # Always include Executive Summary
        ####################################################

        try:

            with open(
                "output/insight.json",
                "r",
                encoding="utf-8"
            ) as f:

                insight = json.load(f)

                context["executive_summary"] = insight.get(
                    "executive_summary",
                    {}
                )

        except Exception:

            context["executive_summary"] = {}

        ####################################################
        # Competitor
        ####################################################

        competitor_keywords = [

            "competitor",
            "compare",
            "benchmark",
            "aya",
            "abank",
            "cb",
            "kbz",
            "uab",
            "yoma",
            "wallet"
        ]

        if any(k in question for k in competitor_keywords):

            context["competitor"] = docs.get(
                "competitor",
                {}
            )

        ####################################################
        # Wallet
        ####################################################

        if "wallet" in question:

            wallet = docs.get("wallet")

            if wallet is not None:

                context["wallet"] = {

                    "columns": list(wallet.columns),

                    "sample": wallet.head(50).to_dict(
                        orient="records"
                    )

                }

        ####################################################
        # IBMB
        ####################################################

        if "ibmb" in question:

            ibmb = docs.get("ibmb")

            if ibmb is not None:

                context["ibmb"] = {

                    "columns": list(ibmb.columns),

                    "sample": ibmb.head(50).to_dict(
                        orient="records"
                    )

                }

        ####################################################
        # CBS / Customer
        ####################################################

        customer_keywords = [

            "customer",
            "segment",
            "saving",
            "loan",
            "deposit",
            "cbs"
        ]

        if any(k in question for k in customer_keywords):

            customer = docs.get("customer")

            if customer is not None:

                context["customer"] = {

                    "columns": list(customer.columns),

                    "sample": customer.head(50).to_dict(
                        orient="records"
                    )

                }

        ####################################################
        # Campaign
        ####################################################

        if "campaign" in question:

            campaign = docs.get("campaign")

            if campaign is not None:

                context["campaign"] = {

                    "columns": list(campaign.columns),

                    "sample": campaign.head(50).to_dict(
                        orient="records"
                    )

                }

        ####################################################
        # Facebook
        ####################################################

        if "facebook" in question:

            context["facebook"] = docs.get(
                "facebook",
                []
            )

        ####################################################
        # Play Store
        ####################################################

        if "review" in question or "play" in question:

            context["playstore"] = docs.get(
                "playstore",
                []
            )

        return context
