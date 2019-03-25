"""
"""

import discord


def build_stats_embed(response: dict):
    """
    """
    embed = discord.Embed(
        title=response.get("Description"),
        url=response.get("URL"),
        description=response.get("Embed Description"),
    )
    embed.set_thumbnail(
        url="https://playphoenix.online/assets/images/phoenix-logo.png"
    )
    for name, value in response.items():
        if name in ("Last Updated", "Description", "URL", "Embed Description"):
            continue
        embed.add_field(name=name, value=value, inline=True)

    embed.set_footer(text=response.get("Last Updated"))

    return embed


def build_realm_kills_embed(response: dict):
    """
    """
    embed = discord.Embed(
        title=response.get("Description"),
        url=response.get("URL"),
        description=response.get("Embed Description"),
    )
    embed.set_thumbnail(
        url="https://playphoenix.online/assets/images/phoenix-logo.png"
    )

    for name, value in response.items():
        if name in ("Last Updated", "Description", "URL", "Embed Description"):
            continue
        value = " ".join(
            [
                f"{realm.replace('Kills', '').strip()}:{kills}"
                for realm, kills in value.items()
            ]
        )
        embed.add_field(name=name, value=value, inline=True)

    embed.set_footer(text=response.get("Last Updated"))

    return embed


def build_rank_embed(response: dict):
    """
    """
    embed = discord.Embed(
        title=response.get("Description"),
        url=response.get("URL"),
        description=response.get("Embed Description"),
    )
    embed.set_thumbnail(
        url="https://playphoenix.online/assets/images/phoenix-logo.png"
    )

    for name, value in response.items():
        if name in ("Last Updated", "Description", "URL", "Embed Description"):
            continue
        value = " ".join(
            [
                f"{realm.replace('Kills', '').strip()}:{kills}"
                for realm, kills in value.items()
            ]
        )
        embed.add_field(name=name, value=value, inline=True)

    embed.set_footer(text=response.get("Last Updated"))

    return embed


EMBED_MESSAGE_MAP = {
    "rps": build_stats_embed,
    "deathblows": build_stats_embed,
    "deaths": build_stats_embed,
    "kills": build_stats_embed,
    "solos": build_stats_embed,
    "realm kills": build_realm_kills_embed,
    "irs": build_stats_embed,
    "rank": build_rank_embed,
}
