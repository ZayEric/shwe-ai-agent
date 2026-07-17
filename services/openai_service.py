from openai import OpenAI
from config import *

print("===== Foundry Configuration =====")
print("Endpoint:", AZURE_OPENAI_ENDPOINT)
print("Deployment:", AZURE_OPENAI_DEPLOYMENT)

if AZURE_OPENAI_KEY:
    print("Key Length:", len(AZURE_OPENAI_KEY))
    print("Key Prefix:", AZURE_OPENAI_KEY[:10])
    print("Key Suffix:", AZURE_OPENAI_KEY[-10:])
else:
    print("No key!")

print("================================")

client = OpenAI(
    base_url=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_KEY,
)


def explain_result(search_result):

    prompt = f"""
    You are an Anti-Money Laundering Compliance Assistant.
    
    The screening engine has already completed deterministic matching.
    
    Do NOT determine whether a customer is matched.
    Do NOT change the risk level.
    
    Use the information below only to prepare an executive compliance summary.
    
    Return:
    
    1. Executive Summary
    
    2. Interpretation
    
    3. Business Impact
    
    4. Recommended Next Actions
    
    5. Compliance Notes
    
    Screening Result
    
    {results}
    """

    response = client.responses.create(
        model=AZURE_OPENAI_DEPLOYMENT,
        input=prompt,
    )

    return response.output_text
