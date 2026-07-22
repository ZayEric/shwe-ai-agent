import json

from services.customer_sharepoint_service import CustomerSharePointService


class RetrievalService:

    def __init__(self):
        self.sp = CustomerSharePointService()

    def retrieve(self, question):

        question = question.lower()

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
            "yomabank": "YOMABank"
        
        }
        
        selected_bank = None
        
        for keyword, bank in bank_mapping.items():
        
            if keyword in question:
        
                selected_bank = bank
                break
        
        
        ####################################################
        # Load ONE competitor
        ####################################################
        
        if selected_bank:
        
            context["competitor"] = {
        
                selected_bank:
        
                self.sp.load_competitor_filtered(
        
                    selected_bank,
        
                    keywords=[
        
                        "wallet",
                        "loan",
                        "deposit",
                        "mobile",
                        "digital",
                        "payment"
        
                    ]
        
                )
        
            }
        
        ####################################################
        # Generic competitor question
        ####################################################
        
        elif any(
        
            k in question
        
            for k in [
        
                "competitor",
        
                "compare",
        
                "comparison",
        
                "market"
        
            ]
        
        ):
        
            context["competitors"] = self.sp.get_competitor_banks()

        ####################################################
        # Wallet
        ####################################################

        if "wallet" in question:
        
            try:
        
                wallet = self.sp.load_excel(
                    "Wallet",
                    "Wallet*.xlsx"
                )
        
                context["wallet"] = {
                    "columns": list(wallet.columns),
                    "sample": wallet.head(30).to_dict(
                        orient="records"
                    )
                }
        
            except Exception as ex:
        
                print(f"Wallet Error: {ex}")

        ####################################################
        # IBMB
        ####################################################

        if "ibmb" in question:

            try:
            
                ibmb = self.sp.load_excel(
            
                    "IBMB",
            
                    "IBMB*.xlsx"
            
                )
            
                context["ibmb"] = {
            
                    "columns": list(ibmb.columns),
            
                    "sample": ibmb.head(30).to_dict(
                        orient="records"
                    )
            
                }
            
            except Exception as ex:
            
                print(ex)

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

            try:
            
                customer = self.sp.load_excel(
            
                    "CBS",
            
                    "Customer*.xlsx"
            
                )
            
                context["customer"] = {
            
                    "columns": list(customer.columns),
            
                    "sample": customer.head(30).to_dict(
                        orient="records"
                    )
            
                }
            
            except Exception as ex:
            
                print(ex)

        ####################################################
        # Campaign
        ####################################################

        if "campaign" in question:

            try:
            
                campaign = self.sp.load_excel(
            
                    "Campaign",
            
                    "Campaign*.xlsx"
            
                )
            
                context["campaign"] = {
            
                    "columns": list(campaign.columns),
            
                    "sample": campaign.head(30).to_dict(
                        orient="records"
                    )
            
                }
            
            except Exception as ex:
            
                print(ex)

        ####################################################
        # Facebook
        ####################################################

        if "facebook" in question:

            try:
            
                context["facebook"] = self.sp.load_json(
            
                    "Facebook",
            
                    "Facebook*.json"
            
                )
            
            except Exception:
            
                pass

        ####################################################
        # Play Store
        ####################################################

        if "review" in question or "play" in question:

            try:
            
                context["playstore"] = self.sp.load_json(
            
                    "PlayStore",
            
                    "PlayStore*.json"
            
                )
            
            except Exception:
            
                pass

        return context
