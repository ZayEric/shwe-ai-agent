import pandas as pd


class WalletService:

    def __init__(self, wallet_df: pd.DataFrame):

        if wallet_df is None:
            wallet_df = pd.DataFrame()

        self.df = wallet_df

    ############################################################
    # Public
    ############################################################

    def summarize(self):

        if self.df.empty:
            return {"message": "No Wallet data found."}

        return {

            "total_records": len(self.df),

            "total_customers": self.total_customers(),

            "active_customers": self.active_customers(),

            "transaction_summary": self.transaction_summary(),

            "channel_summary": self.channel_summary(),

            "top_regions": self.top_regions(),

            "top_products": self.top_products()

        }

    ############################################################
    # Customers
    ############################################################

    def total_customers(self):

        if "CustomerID" not in self.df.columns:
            return None

        return int(self.df["CustomerID"].nunique())

    def active_customers(self):

        if "Status" not in self.df.columns:
            return None

        return int(
            self.df[
                self.df["Status"].str.upper() == "ACTIVE"
            ].shape[0]
        )

    ############################################################
    # Transaction Summary
    ############################################################

    def transaction_summary(self):

        result = {}

        if "TransactionAmount" in self.df.columns:

            result["total_amount"] = float(
                self.df["TransactionAmount"].sum()
            )

            result["average_amount"] = float(
                self.df["TransactionAmount"].mean()
            )

            result["max_amount"] = float(
                self.df["TransactionAmount"].max()
            )

        return result

    ############################################################
    # Channel Summary
    ############################################################

    def channel_summary(self):

        if "Channel" not in self.df.columns:
            return {}

        return (
            self.df["Channel"]
            .value_counts()
            .to_dict()
        )

    ############################################################
    # Region Summary
    ############################################################

    def top_regions(self, top=10):

        if "Region" not in self.df.columns:
            return {}

        return (
            self.df["Region"]
            .value_counts()
            .head(top)
            .to_dict()
        )

    ############################################################
    # Product Summary
    ############################################################

    def top_products(self, top=10):

        if "Product" not in self.df.columns:
            return {}

        return (
            self.df["Product"]
            .value_counts()
            .head(top)
            .to_dict()
        )
