import json
import requests
import pandas as pd

from io import BytesIO
from fnmatch import fnmatch

from services.auth_service import get_graph_token
from config import *


class CustomerSharePointService:

    def __init__(self):

        self.token = get_graph_token()

        self.headers = {
            "Authorization": f"Bearer {self.token}"
        }

    ##########################################################
    # Generic Graph API
    ##########################################################

    def _list_folder(self, folder_path):

        url = (
            f"https://graph.microsoft.com/v1.0/drives/"
            f"{DRIVE_ID}/root:/{folder_path}:/children"
        )

        response = requests.get(
            url,
            headers=self.headers
        )

        response.raise_for_status()

        return response.json()["value"]

    ##########################################################
    # Download Latest File
    ##########################################################

    def _download_latest_file(self, folder, pattern):

        full_path = f"{CUSTOMER_ROOT_FOLDER}/{folder}"

        files = self._list_folder(full_path)

        matched = [

            f for f in files

            if fnmatch(f["name"], pattern)

        ]

        if len(matched) == 0:

            raise Exception(
                f"No file found : {folder}/{pattern}"
            )

        latest = sorted(

            matched,

            key=lambda x: x["lastModifiedDateTime"],

            reverse=True

        )[0]

        print(f"Downloading {folder}/{latest['name']}")

        response = requests.get(
            latest["@microsoft.graph.downloadUrl"]
        )

        response.raise_for_status()

        return latest["name"], response.content

    ##########################################################
    # Excel
    ##########################################################

    def load_excel(self, folder, pattern):

        _, content = self._download_latest_file(
            folder,
            pattern
        )

        return pd.read_excel(
            BytesIO(content)
        )

    ##########################################################
    # JSON
    ##########################################################

    def load_json(self, folder, pattern):

        _, content = self._download_latest_file(
            folder,
            pattern
        )

        return json.loads(
            content.decode("utf-8")
        )

    ##########################################################
    # Markdown
    ##########################################################

    def load_markdown(self, folder, pattern):

        _, content = self._download_latest_file(
            folder,
            pattern
        )

        return content.decode("utf-8")

    ##########################################################
    # Load ALL Competitors
    ##########################################################

    def load_competitors(self):

        competitors = {}

        competitor_root = (
            f"{CUSTOMER_ROOT_FOLDER}/Competitor"
        )

        banks = self._list_folder(
            competitor_root
        )

        for bank in banks:

            # Skip files
            if "folder" not in bank:
                continue

            bank_name = bank["name"]

            print(f"Reading {bank_name}")

            bank_path = (
                f"{competitor_root}/{bank_name}"
            )

            files = self._list_folder(
                bank_path
            )

            markdown = ""

            for file in files:

                if not file["name"].lower().endswith(".md"):
                    continue

                print(
                    f"   -> {file['name']}"
                )

                response = requests.get(
                    file["@microsoft.graph.downloadUrl"]
                )

                response.raise_for_status()

                markdown += "\n\n"

                markdown += (
                    f"# {file['name']}\n"
                )

                markdown += response.text

            competitors[bank_name] = markdown

        return competitors
