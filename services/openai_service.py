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
    You are an AML Compliance Officer.
    
    The screening engine has already completed deterministic matching.
    
    Summary
    
    Total Blacklist Records : {screening_result["total_blacklist"]}
    
    Wallet Matches : {screening_result["wallet_matches"]}
    
    IBMB Matches : {screening_result["ibmb_matches"]}
    
    Total Matches : {screening_result["total_matches"]}
    
    Matched Records
    
    {screening_result["records"]}
    
    Generate:
    
    1. Executive Summary
    2. Risk Interpretation
    3. Compliance Recommendation
    4. Next Actions
    """

    response = client.responses.create(
        model=AZURE_OPENAI_DEPLOYMENT,
        input=prompt,
    )

    return response.output_text
