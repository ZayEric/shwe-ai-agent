import re

def normalize_text(value):

    if value is None:
        return ""

    return (
        str(value)
        .upper()
        .strip()
    )


def normalize_nrc(value):

    if value is None:
        return ""

    value = str(value).upper()

    value = value.replace(" ", "")

    value = re.sub(r'[^A-Z0-9()/]', "", value)

    return value
