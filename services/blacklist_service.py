from services.sharepoint_service import load_blacklist
import numpy as np

def search_blacklist(name=None, nrc=None):

    df = load_blacklist()

    # Replace NaN/Infinity with None
    df = df.replace([np.nan, np.inf, -np.inf], None)

    print(df.columns.tolist())
    print(df.head(10))
    print(df["Name"].tolist()[:10])
    print(df["Name"].dtype)

    df["Name"] = (
        df["Name"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.upper()
    )

    name = name.strip().upper()

    if name:
        result = df[df["Name"].astype(str).str.contains(name, case=False, na=False)]

    elif nrc:
        result = df[df["NRC/Company Registration No"].astype(str) == str(nrc)]

    else:
        return []

    print("Matched rows:")
    print(result)

    print("As dict:")
    print(result.to_dict("records"))

    return result.to_dict("records")
