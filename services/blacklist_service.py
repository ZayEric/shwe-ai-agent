from services.sharepoint_service import load_blacklist

def search_blacklist(name=None,nrc=None):

    df = load_blacklist()

    if name:

        result=df[df["Name"].str.contains(name,case=False,na=False)]

    elif nrc:

        result=df[df["NRC"]==nrc]

    else:

        return None

    return result.to_dict("records")
