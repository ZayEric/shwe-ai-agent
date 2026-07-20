import json
import requests
import pandas as pd

from io import BytesIO
from fnmatch import fnmatch

from services.auth_service import get_graph_token
from config import DRIVE_ID, CUSTOMER_ROOT_FOLDER


class CustomerSharePointService:

    def __init__(self):

        self.token = get_graph_token()

        self.headers = {
            "Authorization": f"Bearer {self.token}"
        }

    ##########################################################
    # Generic Downloader
    ##########################################################

    def _download_latest_file(self, folder, file_pattern):

        full_path = f"{CUSTOMER_ROOT_FOLDER}/{folder}"

        list_url = (
            f"https://graph.microsoft.com/v1.0/drives/"
            f"{DRIVE_ID}/root:/{full_path}:/children"
        )

        response = requests.get(
            list_url,
            headers=self.headers
        )

        response.raise_for_status()

        files = response.json()["value"]

        matched = [

            f for f in files

            if fnmatch(f["name"], file_pattern)

        ]

        if not matched:

            raise Exception(

                f"No file matching '{file_pattern}' found in '{folder}'."

            )

        latest = max(

            matched,

            key=lambda x: x["lastModifiedDateTime"]

        )

        print(f"Downloading {folder}/{latest['name']}")

        download_url = latest["@microsoft.graph.downloadUrl"]

        response = requests.get(download_url)

        response.raise_for_status()

        return latest["name"], response.content

    ##########################################################
    # Excel
    ##########################################################

    def load_excel(self, folder, pattern):

        _, content = self._download_latest_file(folder, pattern)

        return pd.read_excel(BytesIO(content))

    ##########################################################
    # JSON
    ##########################################################

    def load_json(self, folder, pattern):

        _, content = self._download_latest_file(folder, pattern)

        return json.loads(content.decode("utf-8"))

    ##########################################################
    # Markdown
    ##########################################################

    def load_markdown(self, folder, pattern):

        _, content = self._download_latest_file(folder, pattern)

        return content.decode("utf-8")
