import json
import os

from services.document_loader import DocumentLoader
from services.facebook_service import FacebookService
from services.competitor_service import CompetitorService
from services.wallet_service import WalletService
from services.ibmb_service import IBMBService
from services.openai_service import generate_customer_insight


OUTPUT_FILE = "output/insight.json"
PROMPT_FILE = "prompts/customer_prompt.txt"


class CustomerInsightService:

    def __init__(self):

        self.loader = DocumentLoader()

    ###########################################################
    # Main Analysis
    ###########################################################

    def analyze(self):

        documents = self.loader.load_all()
        print("=" * 80)
        print("DOCUMENTS")
        print(documents.keys())
        print("=" * 80)
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

        #print("=" * 80)
        #print("COMPETITOR SUMMARY")
        #print(json.dumps(competitor_summary, indent=2, ensure_ascii=False))
        #print("=" * 80)

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
        # Build Prompt
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

        ##################################################
        # Azure OpenAI
        ##################################################

        print("=" * 80)
        print("PROMPT LENGTH")
        print(len(user_prompt))
        print("=" * 80)
        
        response = generate_customer_insight(

            system_prompt=system_prompt,

            user_prompt=user_prompt

        )

        ##################################################
        # Save Output
        ##################################################

        self._save_output(response)

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

        insight = self._load_output()

        system_prompt = (
            "You are an executive banking advisor. "
            "Answer using ONLY the supplied insight JSON."
        )

        user_prompt = f"""
Insight

{json.dumps(insight, indent=2, ensure_ascii=False)}

Question

{question}
"""

        return generate_customer_insight(

            system_prompt=system_prompt,

            user_prompt=user_prompt

        )

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

        print("Saving insight.json...")
        os.makedirs("output", exist_ok=True)
        print(os.getcwd())
        print(OUTPUT_FILE)
        
        if isinstance(response, str):

            try:

                response = json.loads(response)

            except Exception:

                response = {

                    "raw_response": response

                }

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
