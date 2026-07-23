from services.openai_service import generate_customer_insight

from services.document_loader import DocumentLoader

from pathlib import Path

import json


class DashboardService:

    def __init__(self):

        self.loader = DocumentLoader()

    def generate_dashboard(self, documents):

        prompt = Path(
            "prompts/dashboard_prompt.txt"
        ).read_text(
            encoding="utf-8"
        )

        user_prompt = f"""

Documents

{documents}

"""

        dashboard = generate_customer_insight(

            system_prompt=prompt,

            user_prompt=user_prompt

        )

        return dashboard
