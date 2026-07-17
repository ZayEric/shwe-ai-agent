import numpy as np

from services.sharepoint_service import load_blacklist


def get_blacklist():

    df = load_blacklist()

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
