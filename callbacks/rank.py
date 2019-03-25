"""
Callback functions to be passed to the models callables. (Refactor into decorator pattern.)
"""


def get_rank_realm_points(response: dict) -> dict:
    """Get realm points for a particular guild or character."""
    resp = {}

    for key, value in response.items():

        if key in ("Last Updated", "Description", "URL"):
            resp.update({key: value})
            continue

        realm_points = value.get("Realm Points")
        resp.update({key: int(realm_points)})

    resp.update({"Embed Description": "Realm Points"})

    return resp


def get_rank_deaths(response: dict) -> dict:
    """Get deaths for a particular guild or character."""
    resp = {}

    for key, value in response.items():

        if key in ("Last Updated", "Description", "URL"):
            resp.update({key: value})
            continue

        deaths = value.get("Deaths")
        resp.update({key: int(deaths)})

    resp.update({"Embed Description": "Death"})

    return resp


def get_rank_deathblows(response: dict) -> dict:
    """Get deathblows for a particular guild or character."""
    resp = {}

    for key, value in response.items():

        if key in ("Last Updated", "Description", "URL"):
            resp.update({key: value})
            continue

        deathblows = value.get("Deathblows")
        resp.update({key: int(deathblows)})

    resp.update({"Embed Description": "Deathblows"})

    return resp


def get_rank_kills(response: dict) -> dict:
    """Get kills for a particular guild or character."""
    resp = {}

    for key, value in response.items():

        if key in ("Last Updated", "Description", "URL"):
            resp.update({key: value})
            continue

        kills = value.get("Kills")
        resp.update({key: int(kills)})

    resp.update({"Embed Description": "Kills"})

    return resp


def get_rank_solo_kills(response: dict) -> dict:
    """Calculate solo kills for a particular guild or character."""
    resp = {}

    for key, value in response.items():

        if key in ("Last Updated", "Description", "URL"):
            resp.update({key: value})
            continue

        solo_kills = value.get("Solo Kills")
        resp.update({key: int(solo_kills)})

    resp.update({"Embed Description": "Solo Kills"})

    return resp


CALLBACK_MAP = {
    "rps": get_realm_points,
    "deathblows": get_deathblows,
    "deaths": get_deaths,
    "kills": get_kills,
    "solos": get_solo_kills,
    "irs": get_realm_points_per_death,
}
