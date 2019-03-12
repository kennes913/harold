"""
harold --  An asynchronous Discord bot that queries https://herald.playphoenix.online/.
"""
import logging
import sys
import urllib

import bs4
import discord
import pandas
import requests

import config

from discord.ext import commands

from utils import parse_amount_table, generate_amount_message

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
async def character(name, table):
    """Get character statistics 

    Sample commands:

            ?character `character` rps
            ?character `character` kills
            ?character `character` deathblows
            ?character `character` solos
            ?character `character` deaths
            ?character `character` irs
    """
    if table not in ("rps", "deathblows", "deaths", "kills", "solos", "irs"):
        await HAROLD.say("This table is not supported yet.")
    else:
        uri = urllib.parse.quote(
            'herald.playphoenix.online/c/{name}/'.format(name=name)
        )
        resp = requests.get("https://{uri}".format(uri=uri))
        if resp.status_code == 502:
            await HAROLD.say("The Herald is temporarily down. (502: Bad Gateway Error)")
        else:
            if table != "irs":
                message_metadata = parse_amount_table(resp, name, table)
                if isinstance(message_metadata, dict):
                    embedded_message = generate_amount_message(
                        **message_metadata)
                    await HAROLD.say(embed=embedded_message)
                elif not message_metadata:
                    await HAROLD.say("That table doesn't exist.")
            else:
                rps = parse_amount_table(resp, guild, "rps")
                deaths = parse_amount_table(resp, guild, "deaths")
                if isinstance(rps, dict) and isinstance(deaths, dict):
                    calculated_irs = []
                    rvals = rps.get("values")
                    dvals = deaths.get("values")
                    for index in range(4):
                        time_period = rvals[index][0]
                        rpsf = float(rvals[index][1].replace(',', ''))
                        deathsf = float(dvals[index][1].replace(',', ''))
                        calculated_irs.append(
                            tuple([
                                time_period,
                                rpsf if deathsf == 0 else "{0:.2f}".format(
                                    rpsf / deathsf)
                            ]
                            )
                        )
                    embed = generate_amount_message(
                        "https://www.youtube.com/watch?v=mG_k83Yiy1A",
                        "Stats - {name} - I.R.S.".format(name=name),
                        rps.get("footer"),
                        "I Remain Standing",
                        calculated_irs)
                    await HAROLD.say(embed=embed)
                else:
                    await HAROLD.say("I.R.S. calculation not possible right now.")


@HAROLD.command(description="Get statistics about guilds.")
async def guild(guild, table):
    """Get guild statisitics.

        Sample Commands:

            ?guild `guild` rps
            ?guild `guild` kills
            ?guild `guild` deathblows
            ?guild `guild` solos
            ?guild `guild` deaths
            ?guild `guild` irs
    """
    if table not in ("rps", "deathblows", "deaths", "kills", "solos", "irs"):
        await HAROLD.say("This table is not supported yet.")
    else:
        uri = urllib.parse.quote(
            'herald.playphoenix.online/g/{guild}/'.format(guild=guild)
        )
        resp = requests.get("https://{uri}".format(uri=uri))
        if resp.status_code == 502:
            await HAROLD.say("The Herald is temporarily down.")
        else:
            if table != "irs":
                message_metadata = parse_amount_table(resp, guild, table)
                if isinstance(message_metadata, dict):
                    embedded_message = generate_amount_message(
                        **message_metadata)
                    await HAROLD.say(embed=embedded_message)
                elif not message_metadata:
                    await HAROLD.say("That table doesn't exist.")
            else:
                rps = parse_amount_table(resp, guild, "rps")
                deaths = parse_amount_table(resp, guild, "deaths")
                if isinstance(rps, dict) and isinstance(deaths, dict):
                    calculated_irs = []
                    rvals = rps.get("values")
                    dvals = deaths.get("values")
                    for index in range(4):
                        time_period = rvals[index][0]
                        rpsf = float(rvals[index][1].replace(',', ''))
                        deathsf = float(dvals[index][1].replace(',', ''))
                        calculated_irs.append(
                            tuple([
                                time_period,
                                rpsf if deathsf == 0 else "{0:.2f}".format(
                                    rpsf / deathsf)
                            ]
                            )
                        )
                    embed = generate_amount_message(
                        "https://www.youtube.com/watch?v=mG_k83Yiy1A",
                        "Stats - {guild} - I.R.S.".format(guild=guild),
                        rps.get("footer"),
                        "I Remain Standing",
                        calculated_irs)
                    await HAROLD.say(embed=embed)
                else:
                    await HAROLD.say("I.R.S. calculation not possible right now.")


if __name__ == "__main__":
    HAROLD.run(config.TOKEN)
