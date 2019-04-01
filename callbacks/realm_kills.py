"""
"""


def get_albion_kills(response: dict) -> dict:
    """Calculate Albion kills for a particular guild or character."""
    resp = {}

    for key, value in response.items():

        if key in ("Last Updated", "Description", "URL"):
            resp.update({key: value})
            continue

        solo_kills = value.get("Alb Kills")
        resp.update({key: int(solo_kills)})

    resp.update({"Embed Description": "Albion Kills"})

    return resp


def get_midgard_kills(response: dict) -> dict:
    """Calculate midgard kills for a particular guild or character."""
    resp = {}

    for key, value in response.items():

        if key in ("Last Updated", "Description", "URL"):
            resp.update({key: value})
            continue

        solo_kills = value.get("Alb Kills")
        resp.update({key: int(solo_kills)})

    resp.update({"Embed Description": "Midgard Kills"})

    return resp


def get_hibernia_kills(response: dict) -> dict:
    """Calculate Hibernia kills for a particular guild or character."""
    resp = {}

    for key, value in response.items():

        if key in ("Last Updated", "Description", "URL"):
            resp.update({key: value})
            continue

        solo_kills = value.get("Hib Kills")
        resp.update({key: int(solo_kills)})

    resp.update({"Embed Description": "Hibernia Kills"})

    return resp


CALLBACK_MAP = {
    "albion": get_albion_kills,
    "hibernia": get_hibernia_kills,
    "midgard": get_midgard_kills,
}

