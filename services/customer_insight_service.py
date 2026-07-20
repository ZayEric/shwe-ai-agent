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

        ##############################################
        # Summaries
        ##############################################

        facebook_summary = FacebookService(
            documents["facebook"]
        ).summarize()

        competitor_summary = CompetitorService(
            documents["competitor"]
        ).summarize()

        wallet_summary = WalletService(
            documents["wallet"]
        ).summarize()

        ibmb_summary = IBMBService(
            documents["ibmb"]
        ).summarize()

        customer_summary = self._customer_summary(
            documents["customer"]
        )

        campaign_summary = self._campaign_summary(
            documents["campaign"]
        )

        playstore_summary = documents["playstore"]

        ##############################################
        # Build Prompt
        ##############################################

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

        ##############################################
        # Azure OpenAI
        ##############################################

        response = generate_customer_insight(

            system_prompt=system_prompt,

            user_prompt=user_prompt

        )

        ##############################################
        # Save JSON
        ##############################################

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

{json.dumps(insight, indent=2)}

Question

{question}
"""

        return generate_customer_insight(

            system_prompt,

            user_prompt

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

{json.dumps(facebook, indent=2)}

--------------------------------

PlayStore Reviews

{json.dumps(playstore, indent=2)}

--------------------------------

Wallet Summary

{json.dumps(wallet, indent=2)}

--------------------------------

IBMB Summary

{json.dumps(ibmb, indent=2)}

--------------------------------

Customer Summary

{json.dumps(customer, indent=2)}

--------------------------------

Campaign Summary

{json.dumps(campaign, indent=2)}

--------------------------------

Competitor Summary

{json.dumps(competitor, indent=2)}

"""

    ###########################################################
    # Customer Summary
    ###########################################################

    def _customer_summary(self, df):

        if df.empty:

            return {}

        return {

            "total_customers": len(df),

            "columns": list(df.columns),

            "sample":

                df.head(20).to_dict(

                    orient="records"

                )

        }

    ###########################################################
    # Campaign Summary
    ###########################################################

    def _campaign_summary(self, df):

        if df.empty:

            return {}

        return {

            "total_campaigns": len(df),

            "columns": list(df.columns),

            "sample":

                df.head(20).to_dict(

                    orient="records"

                )

        }

    ###########################################################
    # Prompt File
    ###########################################################

    def _load_prompt(self):

        with open(

            PROMPT_FILE,

            encoding="utf-8"

        ) as f:

            return f.read()

    ###########################################################
    # Save Output
    ###########################################################

    def _save_output(self, response):

        os.makedirs("output", exist_ok=True)

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

        if not os.path.exists(OUTPUT_FILE):

            return {}

        with open(

            OUTPUT_FILE,

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
