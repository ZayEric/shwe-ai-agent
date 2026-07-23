import json
import logging
from pathlib import Path

from services.openai_service import generate_customer_insight

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent

PROMPT_FILE = (
    BASE_DIR.parent
    / "prompts"
    / "dashboard_prompt.txt"
)


class DashboardService:

    def generate_dashboard(
        self,
        facebook_summary,
        wallet_summary,
        ibmb_summary,
        customer_summary,
        campaign_summary,
        competitor_summary,
        playstore_summary
    ):

        logger.info("=" * 80)
        logger.info("DashboardService started")

        with open(
            PROMPT_FILE,
            "r",
            encoding="utf-8"
        ) as f:
            system_prompt = f.read()

        logger.info("Dashboard prompt loaded")

        user_prompt = f"""
Facebook Summary
{json.dumps(facebook_summary, indent=2, ensure_ascii=False)}

--------------------------------------------------------

Play Store Summary
{json.dumps(playstore_summary, indent=2, ensure_ascii=False)}

--------------------------------------------------------

Wallet Summary
{json.dumps(wallet_summary, indent=2, ensure_ascii=False)}

--------------------------------------------------------

IBMB Summary
{json.dumps(ibmb_summary, indent=2, ensure_ascii=False)}

--------------------------------------------------------

Customer Summary
{json.dumps(customer_summary, indent=2, ensure_ascii=False)}

--------------------------------------------------------

Campaign Summary
{json.dumps(campaign_summary, indent=2, ensure_ascii=False)}

--------------------------------------------------------

Competitor Summary
{json.dumps(competitor_summary, indent=2, ensure_ascii=False)}
"""

        logger.info(
            "Dashboard Prompt Size = %s characters",
            len(user_prompt)
        )

        dashboard = generate_customer_insight(
            system_prompt=system_prompt,
            user_prompt=user_prompt
        )

        if isinstance(dashboard, str):
            try:
                dashboard = json.loads(dashboard)
            except Exception:
                logger.exception("Dashboard JSON Parse Error")
                dashboard = {}

        logger.info("Dashboard generated successfully")

        return dashboard
