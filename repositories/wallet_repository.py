import numpy as np

from services.sharepoint_service import load_wallet


def get_wallet():

    df = load_wallet()

    df = df.replace([np.nan, np.inf, -np.inf], None)

    df.columns = df.columns.str.strip()

    df["Name"] = (

        df["Name"]

        .fillna("")

        .astype(str)

        .str.strip()

        .str.upper()

    )

    return df
