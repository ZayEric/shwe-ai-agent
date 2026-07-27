import json
import os
import logging

from services.document_loader import DocumentLoader
from services.facebook_service import FacebookService
from services.competitor_service import CompetitorService
from services.wallet_service import WalletService
from services.ibmb_service import IBMBService
from services.openai_service import generate_customer_insight
from services.retrieval_service import RetrievalService
from services.dashboard_service import DashboardService

import logging

logging.basicConfig(
    filename="/home/LogFiles/customer_insight.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

OUTPUT_FILE = os.path.join(
    BASE_DIR,
    "..",
    "output",
    "insight.json"
)
OUTPUT_FILE = os.path.abspath(OUTPUT_FILE)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROMPT_FILE = os.path.abspath(
    os.path.join(
        BASE_DIR,
        "..",
        "prompts",
        "customer_prompt.txt"
    )
)

print("Prompt:", PROMPT_FILE)
print("Exists:", os.path.exists(PROMPT_FILE))

class CustomerInsightService:

    def __init__(self):
        self.loader = DocumentLoader()

    ###########################################################
    # Main Analysis
    ###########################################################

    def analyze(self):
    
        logger.info("=" * 80)
        logger.info("Loading documents...")
    
        documents = self.loader.load_all()
    
        logger.info("Documents loaded")
        logger.info("Document Keys: %s", list(documents.keys()))
    
        ##################################################
        # Facebook
        ##################################################
    
        facebook_summary = {}
        facebook = documents.get("facebook", [])
    
        if len(facebook) > 0:
            facebook_summary = FacebookService(
                facebook
            ).summarize()
    
        ##################################################
        # Competitor
        ##################################################
    
        competitor_summary = CompetitorService(
            documents.get("competitor", {})
        ).summarize()
    
        ##################################################
        # Wallet
        ##################################################
    
        wallet_summary = {}
    
        wallet_df = documents.get("wallet")
    
        if wallet_df is not None and not wallet_df.empty:
            wallet_summary = WalletService(
                wallet_df
            ).summarize()
    
        ##################################################
        # IBMB
        ##################################################
    
        ibmb_summary = {}
    
        ibmb_df = documents.get("ibmb")
    
        if ibmb_df is not None and not ibmb_df.empty:
            ibmb_summary = IBMBService(
                ibmb_df
            ).summarize()
    
        ##################################################
        # Customer
        ##################################################
    
        customer_summary = self._customer_summary(
            documents.get("customer")
        )
    
        ##################################################
        # Campaign
        ##################################################
    
        campaign_summary = self._campaign_summary(
            documents.get("campaign")
        )
    
        ##################################################
        # Play Store
        ##################################################
    
        playstore_summary = documents.get(
            "playstore",
            []
        )
    
        ##################################################
        # Executive Dashboard
        ##################################################

        logger.info("========== SUMMARY SIZES ==========")
        logger.info("facebook_summary : %s", len(json.dumps(facebook_summary)))
        logger.info("wallet_summary : %s", len(json.dumps(wallet_summary)))
        logger.info("ibmb_summary : %s", len(json.dumps(ibmb_summary)))
        logger.info("customer_summary : %s", len(json.dumps(customer_summary)))
        logger.info("campaign_summary : %s", len(json.dumps(campaign_summary)))
        logger.info("competitor_summary : %s", len(json.dumps(competitor_summary)))
        logger.info("playstore_summary : %s", len(json.dumps(playstore_summary)))
        logger.info("Generating Executive Dashboard...")
    
        dashboard = DashboardService().generate_dashboard(
            facebook_summary,
            wallet_summary,
            ibmb_summary,
            customer_summary,
            campaign_summary,
            competitor_summary,
            playstore_summary
        )
    
        logger.info("Executive Dashboard completed")
    
        ##################################################
        # Customer Insight
        ##################################################
    
        system_prompt = self._load_prompt()
    
        user_prompt = self._build_prompt(
            facebook_summary,
            playstore_summary,
            wallet_summary,
            ibmb_summary,
            customer_summary,
            campaign_summary,
            competitor_summary
        )
    
        logger.info(
            "Customer Prompt Length = %s",
            len(user_prompt)
        )
    
        response = generate_customer_insight(
            system_prompt=system_prompt,
            user_prompt=user_prompt
        )
    
        if isinstance(response, str):
            try:
                response = json.loads(response)
            except Exception:
                response = {
                    "executive_summary": response
                }
    
        ##################################################
        # Merge Dashboard
        ##################################################
    
        response["executive_dashboard"] = dashboard
    
        ##################################################
        # Save
        ##################################################
    
        self._save_output(response)
    
        logger.info("Customer Insight completed.")
    
        return response
    ###########################################################
    # Read Existing Result
    ###########################################################

    def summary(self):
        return self._load_output()

    ###########################################################
    # Executive Q&A
    ###########################################################

    def ask(self, question):
    
        retriever = RetrievalService()
    
        retrieved_documents = retriever.retrieve(question)
    
        logger.info("=" * 80)
        logger.info("QUESTION: %s", question)
        logger.info(
            "RETRIEVED KEYS: %s",
            list(retrieved_documents.keys())
        )
    
        if "competitor" in retrieved_documents:
    
            logger.info(
                "Competitor Loaded: %s",
                list(
                    retrieved_documents["competitor"].keys()
                )
            )
    
        if "competitors" in retrieved_documents:
    
            logger.info(
                "Competitor List: %s",
                retrieved_documents["competitors"]
            )
    
        system_prompt = """
    You are SHWE Bank's Digital Banking Strategy Advisor.
    
    Answer ONLY using the supplied documents.
    
    If only a competitor list is supplied,
    identify the competitors clearly.
    
    If competitor markdown is supplied,
    compare products, digital services,
    wallets, promotions and campaigns.
    
    If Wallet data is supplied,
    analyse customer behaviour.
    
    If CBS customer data is supplied,
    analyse customer segments.
    
    If information is unavailable,
    state that clearly.
    
    Never invent facts.
    """
    
        user_prompt = f"""
    Question
    
    {question}
    
    Relevant Documents
    
    {json.dumps(
        retrieved_documents,
        indent=2,
        ensure_ascii=False
    )}
    """
    
        logger.info(
            "Prompt Length : %s",
            len(user_prompt)
        )
    
        response = generate_customer_insight(
    
            system_prompt=system_prompt,
    
            user_prompt=user_prompt
    
        )
    
        return response

    ###########################################################
    # Recommendation
    ###########################################################

    def recommendations(self):
        insight = self._load_output()
        return insight.get(
            "recommended_products",
            []
        )

    ###########################################################
    # Customer Segments
    ###########################################################

    def segments(self):
        insight = self._load_output()
        return insight.get(
            "customer_segments",
            []
        )

    ###########################################################
    # Prompt Builder
    ###########################################################

    def _build_prompt(
        self,
        facebook,
        playstore,
        wallet,
        ibmb,
        customer,
        campaign,
        competitor

    ):

        return f"""
Facebook Summary

{json.dumps(facebook, indent=2, ensure_ascii=False)}

------------------------------------------------------------

Play Store Reviews

{json.dumps(playstore, indent=2, ensure_ascii=False)}

------------------------------------------------------------

Wallet Summary

{json.dumps(wallet, indent=2, ensure_ascii=False)}

------------------------------------------------------------

IBMB Summary

{json.dumps(ibmb, indent=2, ensure_ascii=False)}

------------------------------------------------------------

Customer Summary

{json.dumps(customer, indent=2, ensure_ascii=False)}

------------------------------------------------------------

Campaign Summary

{json.dumps(campaign, indent=2, ensure_ascii=False)}

------------------------------------------------------------

Competitor Summary

{json.dumps(competitor, indent=2, ensure_ascii=False)}

"""

    ###########################################################
    # Customer Summary
    ###########################################################

    def _customer_summary(self, df):
        if df is None or df.empty:
            return {}
        return {

            "total_customers": len(df),
            "columns": list(df.columns),
            "sample": df.head(20).to_dict(
                orient="records"
            )
        }

    ###########################################################
    # Campaign Summary
    ###########################################################

    def _campaign_summary(self, df):
        if df is None or df.empty:
            return {}
        return {
            "total_campaigns": len(df),
            "columns": list(df.columns),
            "sample": df.head(20).to_dict(
                orient="records"
            )
        }
    ###########################################################
    # Prompt File
    ###########################################################

    def _load_prompt(self):
        with open(
            PROMPT_FILE,
            "r",

            encoding="utf-8"

        ) as f:

            return f.read()

    ###########################################################
    # Save Output
    ###########################################################

    def _save_output(self, response):
        logger.info("Saving insight.json...")
        try:
    
            logger.info("OUTPUT_FILE = %s", OUTPUT_FILE)
    
            logger.info(
                "Directory = %s",
                os.path.dirname(OUTPUT_FILE)
            )
    
            os.makedirs(
                os.path.dirname(OUTPUT_FILE),
                exist_ok=True
            )
    
            logger.info("Directory created.")
            logger.info("Current directory: %s", os.getcwd())
            logger.info("Absolute path: %s", OUTPUT_FILE)
    
            if isinstance(response, str):
    
                try:
                    response = json.loads(response)
    
                except Exception:
    
                    response = {
                        "raw_response": response
                    }
            logger.info("Response type: %s", type(response))
    
            with open(
                OUTPUT_FILE,
                "w",
                encoding="utf-8"
            ) as f:
    
                json.dump(
                    response,
                    f,
                    indent=4,
                    ensure_ascii=False
                )
            logger.info("File written.")
    
            logger.info(
                "Exists: %s",
                os.path.exists(OUTPUT_FILE)
            )
    
            if os.path.exists(OUTPUT_FILE):
    
                logger.info(
                    "File size: %s bytes",
                    os.path.getsize(OUTPUT_FILE)
                )
    
        except Exception:
            logger.exception("SAVE ERROR")   
            raise

    ###########################################################
    # Load Output
    ###########################################################

    def _load_output(self):
        if not os.path.exists(

            OUTPUT_FILE
        ):
            return {}

        with open(
            OUTPUT_FILE,
            "r",
            encoding="utf-8"
        ) as f:
            return json.load(f)

    def comparison(self):
        return self._load_output().get(
            "competitor_comparison",
            []
        )
    
    def swot(self):
        return self._load_output().get(
            "swot_analysis",
            {}
        )
    
    def dashboard(self):
        return self._load_output().get(
            "executive_dashboard",
            {}
        )

###############################################################
# Wrapper Functions
###############################################################

_service = CustomerInsightService()


def analyze_customer_insight():
    return _service.analyze()


def get_executive_summary():
    data = _service.summary()
    return data.get(
        "executive_summary",
        {}
    )

def ask_business_question(question):
    return _service.ask(question)

def get_recommendations():
    return _service.recommendations()

def get_customer_segments():
    return _service.segments()

def get_comparison():
    return _service.comparison()

def get_swot():
    return _service.swot()

def get_dashboard():
    return _service.dashboard()
