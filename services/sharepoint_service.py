import requests
import pandas as pd
from io import BytesIO

from services.auth_service import get_graph_token
from config import *

def load_blacklist():

    token = get_graph_token()

    url = f"https://graph.microsoft.com/v1.0/sites/{SITE_ID}/drives/{DRIVE_ID}/root:/{FILE_PATH}:/content"

    headers = {

        "Authorization":f"Bearer {token}"

    }

    response = requests.get(url,headers=headers)

    excel = BytesIO(response.content)

    df = pd.read_excel(excel)

    return df
