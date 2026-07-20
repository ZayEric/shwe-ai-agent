import json
import requests
import pandas as pd

from io import BytesIO
from fnmatch import fnmatch

from services.auth_service import get_graph_token
from config import (
    DRIVE_ID,
    CUSTOMER_SHAREPOINT_FOLDER
)


class CustomerSharePointService:

    def __init__(self):

        self.token = get_graph_token()

        self.headers = {
            "Authorization": f"Bearer {self.token}"
        }

    def _download_latest_file(self, file_pattern):

        list_url = (
            f"https://graph.microsoft.com/v1.0/drives/"
            f"{DRIVE_ID}/root:/{CUSTOMER_SHAREPOINT_FOLDER}:/children"
        )

        response = requests.get(
            list_url,
            headers=self.headers
        )

        response.raise_for_status()

        files = response.json()["value"]

        matched = []

        for f in files:

            if fnmatch(f["name"], file_pattern):

                matched.append(f)

        if not matched:

            raise Exception(f"No file found : {file_pattern}")

        latest = sorted(
            matched,
            key=lambda x: x["lastModifiedDateTime"],
            reverse=True
        )[0]

        print(f"Downloading {latest['name']}")

        download_url = latest["@microsoft.graph.downloadUrl"]

        response = requests.get(download_url)

        response.raise_for_status()

        return latest["name"], response.content

    #######################################################
    # Excel
    #######################################################

    def load_excel(self, pattern):

        filename, content = self._download_latest_file(pattern)

        return pd.read_excel(BytesIO(content))

    #######################################################
    # JSON
    #######################################################

    def load_json(self, pattern):

        filename, content = self._download_latest_file(pattern)

        return json.loads(content.decode("utf-8"))

    #######################################################
    # Markdown
    #######################################################

    def load_markdown(self, pattern):

        filename, content = self._download_latest_file(pattern)

        return content.decode("utf-8")
