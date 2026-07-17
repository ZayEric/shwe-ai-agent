import requests
import pandas as pd
from io import BytesIO
from fnmatch import fnmatch

from services.auth_service import get_graph_token
from config import *


def load_excel(file_pattern):

    token = get_graph_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    list_url = (
        f"https://graph.microsoft.com/v1.0/drives/"
        f"{DRIVE_ID}/root:/{SHAREPOINT_FOLDER}:/children"
    )

    response = requests.get(list_url, headers=headers)

    response.raise_for_status()

    files = response.json()["value"]

    excel_files = []

    for f in files:

        if fnmatch(f["name"], file_pattern):

            excel_files.append(f)

    if len(excel_files) == 0:

        raise Exception(f"No file found : {file_pattern}")

    latest = sorted(

        excel_files,

        key=lambda x: x["lastModifiedDateTime"],

        reverse=True

    )[0]

    print("Downloading :", latest["name"])

    download_url = latest["@microsoft.graph.downloadUrl"]

    excel_response = requests.get(download_url)

    excel_response.raise_for_status()

    excel = BytesIO(excel_response.content)

    return pd.read_excel(excel)


def load_blacklist():

    return load_excel(BLACKLIST_PATTERN)


def load_wallet():

    return load_excel(WALLET_PATTERN)


def load_ibmb():

    return load_excel(IBMB_PATTERN)
