from services.openai_service import generate_customer_insight
from pathlib import Path

import json
import logging
logger = logging.getLogger(__name__)

class DashboardService:

    def __init__(self):

        self.loader = DocumentLoader()

    def generate_dashboard(self, documents):
        logger.info("DashboardService started")
        
        prompt = Path(
            "prompts/dashboard_prompt.txt"
        ).read_text(
            encoding="utf-8"
        )
        logger.info("Prompt loaded")

        user_prompt = f"""

        Facebook Summary
        
        {facebook_summary}
        
        Wallet Summary
        
        {wallet_summary}
        
        IBMB Summary
        
        {ibmb_summary}
        
        Campaign Summary
        
        {campaign_summary}
        
        Competitor Summary
        
        {competitor_summary}
        """
        logger.info("Prompt size = %s", len(user_prompt))
        dashboard = generate_customer_insight(

            system_prompt=prompt,

            user_prompt=user_prompt

        )
        logger.info("Dashboard generated")
        return dashboard
