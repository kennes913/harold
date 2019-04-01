"""
Configuration related variables and objects.
"""
TABLES = (
    "rps",
    "deathblows",
    "deaths",
    "kills",
    "solos",
    "realm",
    "characters",
)
TABLE_NAME_MAP = {
    "rps": "Realm Points",
    "deathblows": "Death Blows",
    "deaths": "Deaths",
    "kills": "Kills",
    "solos": "Solo Kills",
    "realm": "Realm",
}

SUPPORTED_TABLE_COMMANDS = (
    "rps",
    "deathblows",
    "deaths",
    "kills",
    "solos",
    "irs",
)

FAILED_RESPONSE_REDIRECT = "https://herald.playphoenix.online/"
TOKEN = ""
