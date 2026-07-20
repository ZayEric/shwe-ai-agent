from config import *

from services.customer_sharepoint_service import CustomerSharePointService


class DocumentLoader:

    def __init__(self):

        self.sp = CustomerSharePointService()

    def load_all(self):

        return {

            "facebook": self.sp.load_json(
                FACEBOOK_FOLDER,
                FACEBOOK_PATTERN
            ),

            "playstore": self.sp.load_json(
                PLAYSTORE_FOLDER,
                PLAYSTORE_PATTERN
            ),

            "competitor": self.sp.load_markdown(
                COMPETITOR_FOLDER,
                COMPETITOR_PATTERN
            ),

            "wallet": self.sp.load_excel(
                WALLET_FOLDER,
                WALLET_PATTERN
            ),

            "ibmb": self.sp.load_excel(
                IBMB_FOLDER,
                IBMB_PATTERN
            ),

            "campaign": self.sp.load_excel(
                CAMPAIGN_FOLDER,
                CAMPAIGN_PATTERN
            ),

            "customer": self.sp.load_excel(
                CUSTOMER_FOLDER,
                CUSTOMER_PATTERN
            )

        }
