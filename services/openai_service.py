from openai import AzureOpenAI
from config import *

raise Exception(
    f"""
Endpoint={repr(AZURE_OPENAI_ENDPOINT)}
Deployment={repr(AZURE_OPENAI_DEPLOYMENT)}
Version={repr(AZURE_OPENAI_API_VERSION)}
Key={AZURE_OPENAI_KEY is not None}
"""
)
