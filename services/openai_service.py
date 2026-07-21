import json
from openai import OpenAI
from config import *

print("===== Foundry Configuration =====")
print("Endpoint:", AZURE_OPENAI_ENDPOINT)
print("Deployment:", AZURE_OPENAI_DEPLOYMENT)

if AZURE_OPENAI_KEY:
    print("Key Length:", len(AZURE_OPENAI_KEY))
else:
    print("No key!")

print("================================")

client = OpenAI(
    base_url=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_KEY,
)


###############################################################
# Generic Azure OpenAI Call
###############################################################

def ask_openai(system_prompt: str, user_prompt: str):

    response = client.responses.create(

        model=AZURE_OPENAI_DEPLOYMENT,

        input=[

            {
                "role": "system",
                "content": system_prompt
            },

            {
                "role": "user",
                "content": user_prompt
            }

        ]

    )

    return response.output_text
    
    try:
        return json.loads(content)

    except Exception:

        return {

            "raw_response": content

        }

###############################################################
# AML
###############################################################

def explain_result(search_result):

    system_prompt = """
You are an AML Compliance Officer.

The screening engine has already completed deterministic matching.

Generate

1. Executive Summary
2. Risk Interpretation
3. Compliance Recommendation
4. Next Actions
"""

    user_prompt = f"""

Summary

Total Blacklist Records : {search_result["total_blacklist"]}

Wallet Matches : {search_result["wallet_matches"]}

IBMB Matches : {search_result["ibmb_matches"]}

Total Matches : {search_result["total_matches"]}

Matched Records

{search_result["records"]}

"""

    return ask_openai(

        system_prompt,

        user_prompt

    )


###############################################################
# Customer Intelligence
###############################################################

def generate_customer_insight(

    system_prompt,

    user_prompt

):

    return ask_openai(

        system_prompt,

        user_prompt

    )
