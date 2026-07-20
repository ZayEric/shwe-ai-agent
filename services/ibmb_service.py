import pandas as pd


class IBMBService:

    def __init__(self, ibmb_df: pd.DataFrame):

        if ibmb_df is None:
            ibmb_df = pd.DataFrame()

        self.df = ibmb_df

    ############################################################
    # Public
    ############################################################

    def summarize(self):

        if self.df.empty:
            return {
                "message": "No IBMB data found."
            }

        return {

            "total_records": len(self.df),

            "total_customers": self.total_customers(),

            "active_customers": self.active_customers(),

            "transaction_summary": self.transaction_summary(),

            "service_summary": self.service_summary(),

            "device_summary": self.device_summary(),

            "top_regions": self.top_regions()

        }

    ############################################################
    # Customer Summary
    ############################################################

    def total_customers(self):

        if "CustomerID" not in self.df.columns:
            return None

        return int(
            self.df["CustomerID"].nunique()
        )

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

            result["maximum_amount"] = float(
                self.df["TransactionAmount"].max()
            )

        if "TransactionType" in self.df.columns:

            result["transaction_types"] = (
                self.df["TransactionType"]
                .value_counts()
                .to_dict()
            )

        return result

    ############################################################
    # Digital Services
    ############################################################

    def service_summary(self):

        if "Service" not in self.df.columns:
            return {}

        return (
            self.df["Service"]
            .value_counts()
            .to_dict()
        )

    ############################################################
    # Device Summary
    ############################################################

    def device_summary(self):

        if "Device" not in self.df.columns:
            return {}

        return (
            self.df["Device"]
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
