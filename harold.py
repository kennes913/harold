"""
Harold -- An asynchronous Discord bot that parses HTML from https://herald.playphoenix.online/.
"""
import logging
import sys
import urllib

import bs4
import discord
import requests

import config
import messages
import models

from callbacks import stats, rank_server, rank_realm, realm_kills

from discord.ext import commands

logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler(
    filename="log/discord.log", encoding="utf-8", mode="w"
)
stream_handler.setFormatter(
    logging.Formatter("harold:%(asctime)s:%(name)s: %(message)s")
)
file_handler.setFormatter(
    logging.Formatter("harold:%(asctime)s:%(name)s: %(message)s")
)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)


description = """

        __  __                 __    __
       / / / /___ __________  / /___/ /
      / /_/ / __ `/ ___/ __ \/ / __  / 
     / __  / /_/ / /  / /_/ / / /_/ /  
    /_/ /_/\__,_/_/   \____/_/\__,_/   
    

Get player and guild statistics, ranks and realm kills from https://herald.playphoenix.online/.

"""
HAROLD = commands.Bot(command_prefix="?", description=description)


@HAROLD.command(escription="Get statistics about characters.")
async def character(ctx, name, table):
    """Get character statistics.

    Arguments:

        name :: The name of the character
        table :: The name of the metric you want to query. 

    Examples:
        
        ?character Debug rps
        ?character Debug kills
        ?character Debug deathblows
        ?character Debug solos
        ?character Debug deaths
        ?character Debug irs

    """
    if table not in config.SUPPORTED_TABLE_COMMANDS:
        await ctx.send(f"⚠️ I can't find data for table: {table}.")

    quoted = (
        f"http://{urllib.parse.quote(f'herald.playphoenix.online/c/{name}/')}"
    )
    model = models.MODEL_MAP.get(table)
    embed_message_model = messages.EMBED_MESSAGE_MAP.get(table)

    callback = None
    if table not in ("realm kills", "rank"):
        callback = stats.CALLBACK_MAP.get(table)

    response = model(callback)(quoted) if callback else model(None)(quoted)
    if not response:
        await ctx.send(
            f"⚠️ Redirected to {config.FAILED_RESPONSE_REDIRECT}. Check your character query. Is '{name}' a character name?"
        )
    else:
        embed = embed_message_model(response)
        await ctx.send(embed=embed)


@HAROLD.command(description="Get statistics about guilds.")
async def guild(ctx, guild, table):
    """Get guild statisitics.

    Arguments:

        guild :: The name of the character
        table :: The name of the metric you want to query. 

    Examples:

            ?guild 'Swipe Right' rps
            ?guild 'Swipe Right' kills
            ?guild 'Swipe Right' deathblows
            ?guild 'Swipe Right' solos
            ?guild 'Swipe Right' deaths
            ?guild 'Swipe Right' irs
    """
    if table not in config.SUPPORTED_TABLE_COMMANDS:
        await ctx.send(f"⚠️ I can't find data for table: {table}.")

    quoted = (
        f"http://{urllib.parse.quote(f'herald.playphoenix.online/g/{guild}/')}"
    )
    model = models.MODEL_MAP.get(table)
    embed_message_model = messages.EMBED_MESSAGE_MAP.get(table)

    callback = None
    if table not in ("realm kills", "rank"):
        callback = stats.CALLBACK_MAP.get(table)

    response = model(callback)(quoted) if callback else model(None)(quoted)
    if not response:
        await ctx.send(
            f"⚠️ Redirected to {config.FAILED_RESPONSE_REDIRECT}. Check your guild query. Is '{guild}' a guild name?"
        )
    embed = embed_message_model(response)
    await ctx.send(embed=embed)


@HAROLD.command(description="Get ranks for character or guilds.")
async def rank(ctx, entity, name, table, comparison):
    """Get ranks for specific stats relative to the server or the realm.

    Arguments:

        entity :: The name of the character or guild.
        name :: The name of the metric you want to query. 
        table :: The name of the metric you want to query. 
        comparison :: The set of things you're ranking.


    Examples:

        ?rank guild|character `character`|`guild` rps server|realm
        ?rank guild|character `character`|`guild` kills server|realm
        ?rank guild|character `character`|`guild` deathblows server|realm
        ?rank guild|character `character`|`guild` solos server|realm
        ?rank guild|character `character`|`guild` deaths server|realm

    """
    if entity not in ("character", "guild"):
        await ctx.send(f"⚠️ You can only get ranks for characters or guilds.")

    if comparison not in ("server", "realm"):
        await ctx.send(
            f"⚠️ You can only get ranks relative to realm or server."
        )
    if table not in config.SUPPORTED_TABLE_COMMANDS:
        await ctx.send(f"⚠️ I can't find data for table: {table}.")

    entity = "c" if entity == "character" else "g"
    quoted = f"http://{urllib.parse.quote(f'herald.playphoenix.online/{entity}/{name}/')}"
    model = models.MODEL_MAP.get("rank")
    embed_message_model = messages.EMBED_MESSAGE_MAP.get(table)

    callback = rank_realm.CALLBACK_MAP.get(table)
    response = model(callback)(quoted)
    if not response:
        await ctx.send(
            f"⚠️ Redirected to {config.FAILED_RESPONSE_REDIRECT}. Check your query."
        )
    embed = embed_message_model(response)
    await ctx.send(embed=embed)


@HAROLD.command(description="Get kills for each realm.")
async def realm(ctx, entity, name, realm):
    """Get the realm breakdown of havoc and death that has been wrought.

    Arguments:

        entity :: Character or guild.
        name :: The name of the character or guild.
        realm :: Albion, Midgard or Hibernia

    Sample Commands:

        ?realm character Debug albion
        ?realm guild 'Swipe Right' midgard    
    """
    if entity not in ("character", "guild"):
        await ctx.send(f"⚠️ You can only get ranks for characters or guilds.")

    if realm.lower() not in ("albion", "midgard", "hibernia"):
        await ctx.send(
            f"⚠️ There are only 3 realms: Hibernia, Midgard, Albion."
        )
    entity = "c" if entity == "character" else "g"
    quoted = f"http://{urllib.parse.quote(f'herald.playphoenix.online/{entity}/{name}/')}"
    model = models.MODEL_MAP.get("realm kills")
    embed_message_model = messages.EMBED_MESSAGE_MAP.get("realm kills")

    callback = realm_kills.CALLBACK_MAP.get(realm)
    response = model(callback)(quoted) if callback else model(None)(quoted)

    if not response:
        await ctx.send(
            f"⚠️ Redirected to {config.FAILED_RESPONSE_REDIRECT}. Check your query."
        )
    embed = embed_message_model(response)
    await ctx.send(embed=embed)


if __name__ == "__main__":
    HAROLD.run(config.TOKEN)
