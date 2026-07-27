import pandas as pd


class WalletService:

    def __init__(self, wallet_df: pd.DataFrame):

        if wallet_df is None:
            wallet_df = pd.DataFrame()

        self.df = wallet_df

    ##########################################################
    # Public
    ##########################################################

    def summarize(self):

        if self.df.empty:
            return {
                "message": "No Wallet transaction data found."
            }

        return {

            "total_transactions": len(self.df),

            "total_amount": self.total_amount(),

            "average_amount": self.average_amount(),

            "max_amount": self.max_amount(),

            "transaction_status": self.transaction_status(),

            "transaction_types": self.transaction_types(),

            "top_services": self.top_services(),

            "sender_clients": self.sender_clients(),

            "receiver_clients": self.receiver_clients(),

            "top_senders": self.top_senders(),

            "top_receivers": self.top_receivers()

        }

    ##########################################################
    # Amount
    ##########################################################

    def total_amount(self):

        if "TransactionAmount" not in self.df.columns:
            return 0

        return float(self.df["TransactionAmount"].sum())

    def average_amount(self):

        if "TransactionAmount" not in self.df.columns:
            return 0

        return float(self.df["TransactionAmount"].mean())

    def max_amount(self):

        if "TransactionAmount" not in self.df.columns:
            return 0

        return float(self.df["TransactionAmount"].max())

    ##########################################################
    # Transaction Status
    ##########################################################

    def transaction_status(self):

        if "transaction_status" not in self.df.columns:
            return {}

        return (
            self.df["transaction_status"]
            .fillna("Unknown")
            .value_counts()
            .to_dict()
        )

    ##########################################################
    # Transaction Type
    ##########################################################

    def transaction_types(self):

        if "transaction_type" not in self.df.columns:
            return {}

        return (
            self.df["transaction_type"]
            .fillna("Unknown")
            .value_counts()
            .to_dict()
        )

    ##########################################################
    # Service
    ##########################################################

    def top_services(self):

        if "service_name" not in self.df.columns:
            return {}

        return (
            self.df["service_name"]
            .fillna("Unknown")
            .value_counts()
            .head(10)
            .to_dict()
        )

    ##########################################################
    # Sender Client
    ##########################################################

    def sender_clients(self):

        if "sender_client" not in self.df.columns:
            return {}

        return (
            self.df["sender_client"]
            .fillna("Unknown")
            .value_counts()
            .to_dict()
        )

    ##########################################################
    # Receiver Client
    ##########################################################

    def receiver_clients(self):

        if "receiver_client" not in self.df.columns:
            return {}

        return (
            self.df["receiver_client"]
            .fillna("Unknown")
            .value_counts()
            .to_dict()
        )

    ##########################################################
    # Top Senders
    ##########################################################

    def top_senders(self):

        if "sender_name" not in self.df.columns:
            return {}

        return (
            self.df["sender_name"]
            .fillna("Unknown")
            .value_counts()
            .head(10)
            .to_dict()
        )

    ##########################################################
    # Top Receivers
    ##########################################################

    def top_receivers(self):

        if "receiver_name" not in self.df.columns:
            return {}

        return (
            self.df["receiver_name"]
            .fillna("Unknown")
            .value_counts()
            .head(10)
            .to_dict()
        )
