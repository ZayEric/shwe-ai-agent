import pandas as pd

from config import *

from services.customer_sharepoint_service import CustomerSharePointService


class DocumentLoader:

    def __init__(self):

        self.sp = CustomerSharePointService()

    ##########################################################
    # Safe Loader
    ##########################################################

    def _safe_load(self, loader, default):

        try:
            return loader()

        except Exception as e:

            print(f"Warning: {e}")

            return default

    ##########################################################
    # Load All Documents
    ##########################################################

    def load_all(self):

        return {

            ##################################################
            # Facebook
            ##################################################

            "facebook": self._safe_load(

                lambda: self.sp.load_json(

                    FACEBOOK_FOLDER,

                    FACEBOOK_PATTERN

                ),

                []

            ),

            ##################################################
            # Play Store
            ##################################################

            "playstore": self._safe_load(

                lambda: self.sp.load_json(

                    PLAYSTORE_FOLDER,

                    PLAYSTORE_PATTERN

                ),

                []

            ),

            ##################################################
            # Competitors
            ##################################################

            "competitor": self._safe_load(

                lambda: self.sp.load_competitors(),

                {}

            ),

            ##################################################
            # Wallet
            ##################################################

            "wallet": self._safe_load(

                lambda: self.sp.load_excel(

                    WALLET_FOLDER,

                    WALLET_PATTERN

                ),

                pd.DataFrame()

            ),

            ##################################################
            # IBMB
            ##################################################

            "ibmb": self._safe_load(

                lambda: self.sp.load_excel(

                    IBMB_FOLDER,

                    IBMB_PATTERN

                ),

                pd.DataFrame()

            ),

            ##################################################
            # Campaign
            ##################################################

            "campaign": self._safe_load(

                lambda: self.sp.load_excel(

                    CAMPAIGN_FOLDER,

                    CAMPAIGN_PATTERN

                ),

                pd.DataFrame()

            ),

            ##################################################
            # Customer
            ##################################################

            "customer": self._safe_load(

                lambda: self.sp.load_excel(

                    CUSTOMER_FOLDER,

                    CUSTOMER_PATTERN

                ),

                pd.DataFrame()

            )

        }
