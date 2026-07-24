import json
import requests
import pandas as pd
import time
import logging

from io import BytesIO
from fnmatch import fnmatch

from services.auth_service import get_graph_token
from config import *

logger = logging.getLogger(__name__)

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
            headers=self.headers,
            timeout=60
        )

        response.raise_for_status()

        return response.json()["value"]

    ##########################################################
    # Download Latest File
    ##########################################################

    def _download_latest_file(self, folder, pattern):
    
        start = time.time()
    
        full_path = f"{CUSTOMER_ROOT_FOLDER}/{folder}"
    
        print(f"Listing folder: {full_path}")
    
        files = self._list_folder(full_path)
    
        print(
            f"List completed in {time.time()-start:.2f}s"
        )
    
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
    
        print(
            f"Downloading {latest['name']}"
        )
    
        start = time.time()
    
        response = requests.get(
            latest["@microsoft.graph.downloadUrl"],
            timeout=60
        )
    
        response.raise_for_status()
    
        print(
            f"Download completed in {time.time()-start:.2f}s"
        )
    
        return latest["name"], response.content

    ##########################################################
    # Excel
    ##########################################################

    def load_excel(self, folder, pattern):
    
        # Measure download time
        start_download = time.time()
    
        filename, content = self._download_latest_file(
            folder,
            pattern
        )
    
        download_time = time.time() - start_download
    
        logger.info(
            "%s downloaded in %.2f sec (%.2f MB)",
            filename,
            download_time,
            len(content) / 1024 / 1024
        )
    
        # Measure Excel parsing time
        start_parse = time.time()
    
        df = pd.read_excel(
            BytesIO(content)
        )
    
        parse_time = time.time() - start_parse
    
        logger.info(
            "%s parsed in %.2f sec",
            filename,
            parse_time
        )
    
        logger.info(
            "%s rows=%d cols=%d",
            filename,
            len(df),
            len(df.columns)
        )
    
        return df

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
                file["@microsoft.graph.downloadUrl"],
                timeout=60
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
                file["@microsoft.graph.downloadUrl"],
                timeout=60
            )
    
            response.raise_for_status()
    
            markdown += "\n\n"
    
            markdown += f"# {file['name']}\n"
    
            markdown += response.text
    
        return markdown
