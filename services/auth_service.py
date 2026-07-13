import requests
from config import *

def get_graph_token():

    url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"

    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": "https://graph.microsoft.com/.default",
        "grant_type": "client_credentials"
    }

    response = requests.post(url, data=data)

    print(response.status_code)
    print(response.text)

    response.raise_for_status()

    return response.json()["access_token"]
