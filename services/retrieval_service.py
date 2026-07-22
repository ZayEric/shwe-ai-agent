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

        competitors = docs.get("competitor", {})
        
        # Default: no competitor selected
        selected_competitors = {}
        
        # Bank name detection
        bank_mapping = {
        
            "aya": "AYABank",
            "ayabank": "AYABank",
        
            "abank": "ABank",
        
            "cb": "CBBank",
            "cbbank": "CBBank",
        
            "kbz": "KBZBank",
            "kbzbank": "KBZBank",
        
            "uab": "UABBank",
        
            "yoma": "YOMABank",
            "yomabank": "YOMABank",
        
            "true money": "TrueMoney",
            "truemoney": "TrueMoney"
        
        }
        
        for keyword, bank in bank_mapping.items():
        
            if keyword in question.lower():
        
                if bank in competitors:
        
                    selected_competitors[bank] = competitors[bank]
        
        # If no specific bank is mentioned,
        # but user asks competitor comparison,
        # return all competitors.
        
        generic_keywords = [
        
            "competitor",
            "compare",
            "comparison",
            "benchmark",
            "market",
            "industry"
        
        ]
        
        if len(selected_competitors) == 0:
        
            if any(k in question.lower() for k in generic_keywords):
        
                selected_competitors = competitors
        
        if len(selected_competitors) > 0:
        
            context["competitor"] = selected_competitors

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
