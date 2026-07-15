from openai import OpenAI

from config import *

client = OpenAI(
    api_key=AZURE_OPENAI_KEY,
    base_url=os.getenv("AZURE_OPENAI_ENDPOINT")
)


def explain_result(search_result):
    print("========== Azure Config ==========")
    print("Endpoint:", repr(AZURE_OPENAI_ENDPOINT))
    print("Deployment:", repr(AZURE_OPENAI_DEPLOYMENT))
    print("API Version:", repr(AZURE_OPENAI_API_VERSION))
    print("Key exists:", AZURE_OPENAI_KEY is not None)
    print("==================================")
    prompt = f"""
    You are an AML Compliance Officer.
    
    Explain this blacklist screening result.
    
    {search_result}
    
    Provide:
    1. Match summary
    2. Risk level
    3. Recommendation
    """
    print(AZURE_OPENAI_ENDPOINT)
    print(AZURE_OPENAI_DEPLOYMENT)
    print(client.base_url)
    print("Calling Azure OpenAI...")
    response = client.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content
