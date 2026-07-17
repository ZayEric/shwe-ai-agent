import numpy as np

from services.sharepoint_service import load_ibmb


def get_ibmb():

    df = load_ibmb()

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
