from openai import OpenAI
from config import *

print("===== Foundry Configuration =====")
print("Endpoint:", AZURE_OPENAI_ENDPOINT)
print("Deployment:", AZURE_OPENAI_DEPLOYMENT)
print("API Key Exists:", AZURE_OPENAI_KEY is not None)
print("================================")

client = OpenAI(
    base_url=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_KEY,
)


def explain_result(search_result):

    prompt = f"""
You are an AML Compliance Officer.

Explain this blacklist screening result.

{search_result}

Provide:
1. Match summary
2. Risk level
3. Recommendation
"""

    response = client.responses.create(
        model=AZURE_OPENAI_DEPLOYMENT,
        input=prompt,
    )

    return response.output_text
