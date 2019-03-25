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

from callbacks import stats, rank

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
    Get player and guild stats from https://herald.playphoenix.online/

    Currently supported commands:

        Character Stats:

            ?character `character` rps
            ?character `character` kills
            ?character `character` deathblows
            ?character `character` solos
            ?character `character` deaths
            ?character `character` irs
        
        Guild Stats:

            ?guild `guild` rps
            ?guild `guild` kills
            ?guild `guild` deathblows
            ?guild `guild` solos
            ?guild `guild` deaths
            ?guild `guild` irs
"""
HAROLD = commands.Bot(command_prefix="?", description=description)


@HAROLD.command(description="Get statistics about characters.")
async def character(ctx, name, table):
    """Get character statistics 

    Sample commands:

            ?character `character` rps
            ?character `character` kills
            ?character `character` deathblows
            ?character `character` solos
            ?character `character` deaths
            ?character `character` irs
            ?character `character` realm kills
            ?character `character` rank
    """
    if table not in config.SUPPORTED_TABLE_COMMANDS:
        await ctx.send(f"🤖 - I can't find data for table: {table}.")

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
            f"🤖 - Redirected to home. Check your character query: {name}."
        )
    else:
        embed = embed_message_model(response)
        await ctx.send(embed=embed)


@HAROLD.command(description="Get statistics about guilds.")
async def guild(ctx, guild, table):
    """Get guild statisitics.

        Sample Commands:

            ?guild `guild` rps
            ?guild `guild` kills
            ?guild `guild` deathblows
            ?guild `guild` solos
            ?guild `guild` deaths
            ?guild `guild` irs
            ?guild `guild` realm kills
            ?guild `guild` rank
    """
    if table not in config.SUPPORTED_TABLE_COMMANDS:
        await ctx.send(f"🤖 - I can't find data for table: {table}.")

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
            f"🤖 - Redirected to home. Check your character query: {guild}."
        )
    embed = embed_message_model(response)
    await ctx.send(embed=embed)


@HAROLD.command(
    description="Get rank of player or guild with respect to specific stats."
)
async def rank(ctx, name, table):
    """Get guild statisitics.

        Sample Commands:

            ?guild `guild` rps
            ?guild `guild` kills
            ?guild `guild` deathblows
            ?guild `guild` solos
            ?guild `guild` deaths
            ?guild `guild` irs
            ?guild `guild` realm kills
            ?guild `guild` rank
    """
    if table not in config.SUPPORTED_TABLE_COMMANDS:
        await ctx.send(f"🤖 - I can't find data for table: {table}.")

    quoted = (
        f"http://{urllib.parse.quote(f'herald.playphoenix.online/g/{guild}/')}"
    )
    model = models.MODEL_MAP.get(table)
    embed_message_model = messages.EMBED_MESSAGE_MAP.get(table)

    callback = None
    if table not in ("realm kills", "rank"):
        callback = rank.CALLBACK_MAP.get(table)

    response = model(callback)(quoted) if callback else model(None)(quoted)
    if not response:
        await ctx.send(
            f"🤖 - Redirected to home. Check your character query: {guild}."
        )
    embed = embed_message_model(response)
    await ctx.send(embed=embed)


if __name__ == "__main__":
    HAROLD.run(config.TOKEN)
