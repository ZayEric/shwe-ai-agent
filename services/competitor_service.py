import re
from collections import Counter


class CompetitorService:

    def __init__(self, competitors: dict):

        """
        competitors =

        {
            "KBZBank": "...markdown...",
            "AYABank": "...markdown...",
            ...
        }
        """

        self.competitors = competitors or {}

    ############################################################
    # Public
    ############################################################

    def summarize(self):

        summary = {}

        for bank, markdown in self.competitors.items():

            summary[bank] = {

                "products": self.extract_products(markdown),

                "campaigns": self.extract_campaigns(markdown),

                "headings": self.extract_headings(markdown),

                "top_keywords": self.top_keywords(markdown),

                "word_count": self.word_count(markdown)

            }

        return summary

    ############################################################
    # Products
    ############################################################

    def extract_products(self, markdown):

        keywords = [

            "Saving",
            "Deposit",
            "Loan",
            "Credit Card",
            "Debit Card",
            "Wallet",
            "Mobile Banking",
            "QR",
            "Insurance",
            "Investment",
            "Remittance"

        ]

        found = []

        text = markdown.lower()

        for keyword in keywords:

            if keyword.lower() in text:

                found.append(keyword)

        return sorted(list(set(found)))

    ############################################################
    # Campaigns
    ############################################################

    def extract_campaigns(self, markdown):

        campaign_words = [

            "promotion",
            "discount",
            "cashback",
            "reward",
            "bonus",
            "campaign",
            "special offer"

        ]

        result = []

        for line in markdown.splitlines():

            lower = line.lower()

            for word in campaign_words:

                if word in lower:

                    result.append(line.strip())

                    break

        return result[:20]

    ############################################################
    # Markdown Headings
    ############################################################

    def extract_headings(self, markdown):

        headings = []

        for line in markdown.splitlines():

            if line.startswith("#"):

                headings.append(

                    line.replace("#", "").strip()

                )

        return headings

    ############################################################
    # Keyword Frequency
    ############################################################

    def top_keywords(self, markdown, top_n=20):

        stop_words = {

            "the", "and", "for", "with", "your",
            "from", "this", "that", "have",
            "will", "our", "you", "are",
            "bank", "banking"

        }

        text = re.sub(

            r"[^a-zA-Z ]",

            " ",

            markdown

        )

        words = []

        for word in text.lower().split():

            if len(word) < 3:

                continue

            if word in stop_words:

                continue

            words.append(word)

        counter = Counter(words)

        return counter.most_common(top_n)

    ############################################################
    # Word Count
    ############################################################

    def word_count(self, markdown):

        return len(markdown.split())

    ############################################################
    # Compare Competitors (Optional)
    ############################################################

    def compare_products(self):

        comparison = {}

        for bank, markdown in self.competitors.items():

            comparison[bank] = self.extract_products(markdown)

        return comparison

    ############################################################
    # Compare Campaigns (Optional)
    ############################################################

    def compare_campaigns(self):

        comparison = {}

        for bank, markdown in self.competitors.items():

            comparison[bank] = self.extract_campaigns(markdown)

        return comparison
