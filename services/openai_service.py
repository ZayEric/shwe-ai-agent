from openai import OpenAI
from config import *

client=OpenAI(api_key=OPENAI_API_KEY)

def explain_result(search_result):

    prompt=f"""

You are an AML Officer.

Explain this blacklist result.

{search_result}

"""

    response=client.responses.create(

        model="gpt-5.5",

        input=prompt

    )

    return response.output_text
