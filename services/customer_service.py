import pandas as pd


class CustomerService:

    def __init__(self, customer_df: pd.DataFrame):

        if customer_df is None:
            customer_df = pd.DataFrame()

        self.df = customer_df

    ##########################################################
    # Public
    ##########################################################

    def summarize(self):

        if self.df.empty:
            return {
                "message": "No customer data found."
            }

        return {

            "total_customers": len(self.df),

            "active_customers": self.active_customers(),

            "customer_levels": self.customer_levels(),

            "customer_types": self.customer_types(),

            "customer_roles": self.customer_roles(),

            "kyc_status": self.kyc_status(),

            "gender_distribution": self.gender_distribution(),

            "onboarding_trend": self.onboarding_trend()

        }

    ##########################################################
    # Active
    ##########################################################

    def active_customers(self):

        if "Status" not in self.df.columns:
            return 0

        return int(
            self.df[
                self.df["Status"].str.upper() == "ACTIVE"
            ].shape[0]
        )

    ##########################################################
    # Customer Level
    ##########################################################

    def customer_levels(self):

        if "customer_level" not in self.df.columns:
            return {}

        return (
            self.df["customer_level"]
            .fillna("Unknown")
            .value_counts()
            .to_dict()
        )

    ##########################################################
    # Customer Type
    ##########################################################

    def customer_types(self):

        if "customer_type" not in self.df.columns:
            return {}

        return (
            self.df["customer_type"]
            .fillna("Unknown")
            .value_counts()
            .to_dict()
        )

    ##########################################################
    # Customer Role
    ##########################################################

    def customer_roles(self):

        if "customer_role" not in self.df.columns:
            return {}

        return (
            self.df["customer_role"]
            .fillna("Unknown")
            .value_counts()
            .to_dict()
        )

    ##########################################################
    # KYC
    ##########################################################

    def kyc_status(self):

        if "kyc_status" not in self.df.columns:
            return {}

        return (
            self.df["kyc_status"]
            .fillna("Unknown")
            .value_counts()
            .to_dict()
        )

    ##########################################################
    # Gender
    ##########################################################

    def gender_distribution(self):

        if "gender" not in self.df.columns:
            return {}

        return (
            self.df["gender"]
            .fillna("Unknown")
            .value_counts()
            .to_dict()
        )

    ##########################################################
    # Onboarding Trend
    ##########################################################

    def onboarding_trend(self):
    
        if "onboarded_date" not in self.df.columns:
            return {}
    
        df = self.df.copy()
    
        df["onboarded_date"] = pd.to_datetime(
            df["onboarded_date"],
            errors="coerce"
        )
    
        result = (
            df.groupby(
                df["onboarded_date"].dt.to_period("M")
            )
            .size()
        )
    
        return {
    
            str(period): int(count)
    
            for period, count in result.items()
    
        }
