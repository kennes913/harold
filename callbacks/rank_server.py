"""
"""
from callbacks.decorators import comparison


@comparison("server")
def get_realm_points(response: dict) -> dict:
    """Get realm points for a particular guild or character."""
    resp = {}

    for key, value in response.items():

        if key in ("Last Updated", "Description", "URL"):
            resp.update({key: value})
            continue
        realm_points = value.get("Realm Points")

        resp.update({key: realm_points})

    resp.update({"Embed Description": "Realm Points Rank (All Server)"})

    return resp


@comparison("server")
def get_deaths(response: dict) -> dict:
    """Get deaths for a particular guild or character."""
    resp = {}

    for key, value in response.items():

        if key in ("Last Updated", "Description", "URL"):
            resp.update({key: value})
            continue

        deaths = value.get("Deaths")
        resp.update({key: deaths})

    resp.update({"Embed Description": "Death Rank (All Server)"})

    return resp


@comparison("server")
def get_deathblows(response: dict) -> dict:
    """Get deathblows for a particular guild or character."""
    resp = {}

    for key, value in response.items():

        if key in ("Last Updated", "Description", "URL"):
            resp.update({key: value})
            continue

        deathblows = value.get("Deathblows")
        resp.update({key: deathblows})

    resp.update({"Embed Description": "Deathblows Rank (All Server)"})

    return resp


@comparison("server")
def get_kills(response: dict) -> dict:
    """Get kills for a particular guild or character."""
    resp = {}

    for key, value in response.items():

        if key in ("Last Updated", "Description", "URL"):
            resp.update({key: value})
            continue

        kills = value.get("Kills")
        resp.update({key: kills})

    resp.update({"Embed Description": "Kills Rank (All Server)"})

    return resp


@comparison("server")
def get_solo_kills(response: dict) -> dict:
    """Calculate solo kills for a particular guild or character."""
    resp = {}

    for key, value in response.items():

        if key in ("Last Updated", "Description", "URL"):
            resp.update({key: value})
            continue

        solo_kills = value.get("Solo Kills")
        resp.update({key: solo_kills})

    resp.update({"Embed Description": "Solo Kills Rank (All Server)"})

    return resp


CALLBACK_MAP = {
    "rps": get_realm_points,
    "deathblows": get_deathblows,
    "deaths": get_deaths,
    "kills": get_kills,
    "solos": get_solo_kills,
}
