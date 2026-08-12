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

    print("Getting Graph token...")
    print("Tenant:", TENANT_ID)
    print("Client:", CLIENT_ID)
    
    print("Token URL:", url)
    response = requests.post(url, data=data)

    print(response.text)
    print(response.status_code)

    if response.status_code != 200:
        raise Exception(response.text)

    return response.json()["access_token"]
