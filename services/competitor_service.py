import re
from collections import Counter


class CompetitorService:

    def __init__(self, markdown_text: str):

        self.markdown = markdown_text or ""

    ############################################################
    # Public
    ############################################################

    def summarize(self):

        return {

            "products": self.extract_products(),

            "campaigns": self.extract_campaigns(),

            "headings": self.extract_headings(),

            "top_keywords": self.top_keywords(),

            "word_count": self.word_count()

        }

    ############################################################
    # Products
    ############################################################

    def extract_products(self):

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

        text = self.markdown.lower()

        for keyword in keywords:

            if keyword.lower() in text:

                found.append(keyword)

        return sorted(list(set(found)))

    ############################################################
    # Campaigns
    ############################################################

    def extract_campaigns(self):

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

        lines = self.markdown.splitlines()

        for line in lines:

            lower = line.lower()

            for word in campaign_words:

                if word in lower:

                    result.append(line.strip())

                    break

        return result[:20]

    ############################################################
    # Markdown Headings
    ############################################################

    def extract_headings(self):

        headings = []

        for line in self.markdown.splitlines():

            if line.startswith("#"):

                headings.append(line.replace("#", "").strip())

        return headings

    ############################################################
    # Keyword Frequency
    ############################################################

    def top_keywords(self, top_n=20):

        stop_words = {

            "the", "and", "for", "with", "your",

            "from", "this", "that", "have",

            "will", "our", "you", "are",

            "bank", "banking"

        }

        text = re.sub(r'[^a-zA-Z ]', ' ', self.markdown)

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

    def word_count(self):

        return len(self.markdown.split())
