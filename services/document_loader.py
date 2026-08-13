import logging
import time
import pandas as pd

from concurrent.futures import ThreadPoolExecutor, as_completed

from config import *
from services.customer_sharepoint_service import CustomerSharePointService

logger = logging.getLogger(__name__)


class DocumentLoader:

    def __init__(self):

        self.sp = CustomerSharePointService()

    ##########################################################
    # Safe Loader
    ##########################################################

    def _safe_load(self, name, loader, default):
    
        try:
            return loader()
    
        except Exception:
    
            logger.exception("%s loading failed", name)
    
            return default

    ##########################################################
    # Load All Documents
    ##########################################################

    def load_all(self):
    
        jobs = {
    
            "facebook": lambda: self.sp.load_json(
                FACEBOOK_FOLDER,
                FACEBOOK_PATTERN
            ),
    
            "playstore": lambda: self.sp.load_json(
                PLAYSTORE_FOLDER,
                PLAYSTORE_PATTERN
            ),
    
            "competitor": lambda: self.sp.load_competitors(),
    
            "wallet_customer": lambda: self.sp.load_excel(
                WALLET_FOLDER,
                WALLET_CUSTOMER_PATTERN
            ),
            
            "wallet_transaction": lambda: self.sp.load_csv(
                WALLET_FOLDER,
                WALLET_TRANSACTION_PATTERN,
                usecols=[
                    "service_name",
                    "transaction_type",
                    "sender_phone",
                    "receiver_phone",
                    "transaction_status",
                    "processedby_ph",
                    "processedby_client",
                    "transaction_date",
                    "transaction_amount"
                ]
            ),
    
            "ibmb": lambda: self.sp.load_excel(
                IBMB_FOLDER,
                IBMB_PATTERN
            ),
    
            "campaign": lambda: self.sp.load_excel(
                CAMPAIGN_FOLDER,
                CAMPAIGN_PATTERN
            ),
    
            "customer": lambda: self.sp.load_excel(
                CUSTOMER_FOLDER,
                CUSTOMER_PATTERN
            )
        }
    
        defaults = {
        
            "facebook": [],
            "playstore": [],
            "competitor": {},
            "wallet_customer": pd.DataFrame(),
            "wallet_transaction": pd.DataFrame(),
            "ibmb": pd.DataFrame(),
            "campaign": pd.DataFrame(),
            "customer": pd.DataFrame()
        }
    
        results = {}
    
        start_all = time.time()
    
        with ThreadPoolExecutor(max_workers=7) as executor:
    
            future_map = {}
    
            for name, loader in jobs.items():
    
                future = executor.submit(
                    self._safe_load,
                    name,
                    loader,
                    defaults[name]
                )
    
                future_map[future] = (name, time.time())
    
            for future in as_completed(future_map):
    
                name, start = future_map[future]
    
                try:
    
                    results[name] = future.result()
    
                    logger.info(
                        "%s loaded in %.2f sec",
                        name,
                        time.time() - start
                    )
    
                except Exception as e:
    
                    logger.exception(
                        "%s failed : %s",
                        name,
                        e
                    )
    
                    results[name] = defaults[name]
    
        logger.info(
            "All documents loaded in %.2f sec",
            time.time() - start_all
        )
    
        return results
