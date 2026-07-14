import requests
import pandas as pd
from io import BytesIO
from fnmatch import fnmatch

from services.auth_service import get_graph_token
from config import *


def load_blacklist():

    token = get_graph_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # -------------------------------------
    # Step 1 : Get all files in Blacklist folder
    # -------------------------------------

    list_url = (
        f"https://graph.microsoft.com/v1.0/drives/"
        f"{DRIVE_ID}/root:/{SHAREPOINT_FOLDER}:/children"
    )

    response = requests.get(list_url, headers=headers)
    print("Listing SharePoint files...")
    print(response.status_code)
    print(response.text)

    response.raise_for_status()

    files = response.json()["value"]

    # -------------------------------------
    # Step 2 : Keep only Excel files
    # -------------------------------------
    print("Reading Excel...")
    excel_files = []

    for f in files:

        if fnmatch(f["name"], FILE_PATTERN):

            excel_files.append(f)

    if len(excel_files) == 0:

        raise Exception("No Excel blacklist file found.")

    # -------------------------------------
    # Step 3 : Pick latest file
    # -------------------------------------

    latest = sorted(
        excel_files,
        key=lambda x: x["lastModifiedDateTime"],
        reverse=True
    )[0]

    print("Latest blacklist:", latest["name"])

    # -------------------------------------
    # Step 4 : Download latest Excel
    # -------------------------------------

    download_url = latest["@microsoft.graph.downloadUrl"]

    excel_response = requests.get(download_url)

    excel_response.raise_for_status()

    excel = BytesIO(excel_response.content)

    # -------------------------------------
    # Step 5 : Read Excel
    # -------------------------------------

    df = pd.read_excel(excel)

    return df
