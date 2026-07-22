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
    # Get Competitor Banks
    ##########################################################
    
    def get_competitor_banks(self):
    
        competitor_root = (
            f"{CUSTOMER_ROOT_FOLDER}/Competitor"
        )
    
        banks = self._list_folder(
            competitor_root
        )
    
        return [
    
            b["name"]
    
            for b in banks
    
            if "folder" in b
    
        ]

    ##########################################################
    # Load One Competitor
    ##########################################################
    
    def load_competitor(self, bank_name):
    
        competitor_root = (
            f"{CUSTOMER_ROOT_FOLDER}/Competitor/{bank_name}"
        )
    
        files = self._list_folder(
            competitor_root
        )
    
        markdown = ""
    
        for file in files:
    
            if not file["name"].lower().endswith(".md"):
                continue
    
            print(f"Loading {bank_name} : {file['name']}")
    
            response = requests.get(
                file["@microsoft.graph.downloadUrl"]
            )
    
            response.raise_for_status()
    
            markdown += "\n\n"
    
            markdown += f"# {file['name']}\n"
    
            markdown += response.text
    
        return markdown

    ##########################################################
    # Load Relevant Competitor Pages
    ##########################################################
    
    def load_competitor_filtered(
        self,
        bank_name,
        keywords=None
    ):
    
        competitor_root = (
            f"{CUSTOMER_ROOT_FOLDER}/Competitor/{bank_name}"
        )
    
        files = self._list_folder(
            competitor_root
        )
    
        markdown = ""
    
        keywords = [
    
            k.lower()
    
            for k in (keywords or [])
    
        ]
    
        for file in files:
    
            filename = file["name"].lower()
    
            if not filename.endswith(".md"):
                continue
    
            ##################################################
            # Skip unnecessary pages
            ##################################################
    
            skip = [
    
                "page=",
                "atm-location",
                "branch-location",
                "career",
                "employee",
                "network",
                "contact",
                "privacy",
                "governance"
    
            ]
    
            if any(s in filename for s in skip):
                continue
    
            ##################################################
            # Filter by keyword
            ##################################################
    
            if len(keywords) > 0:
    
                if not any(
    
                    k in filename
    
                    for k in keywords
    
                ):
    
                    continue
    
            print(f"Loading {bank_name}: {file['name']}")
    
            response = requests.get(
                file["@microsoft.graph.downloadUrl"]
            )
    
            response.raise_for_status()
    
            markdown += "\n\n"
    
            markdown += f"# {file['name']}\n"
    
            markdown += response.text
    
        return markdown
