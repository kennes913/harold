"""
"""
import bs4
import discord

import config

def generate_amount_message(url, title, footer, description, values):

    embed=discord.Embed(title=title, url=url, description=description)
    embed.set_thumbnail(url="https://playphoenix.online/assets/images/phoenix-logo.png")
    
    for name, value in values:
        embed.add_field(name=name, value=value, inline=True)
    
    embed.set_footer(text=footer)

    return embed 

def parse_amount_table(resp, name, table):

    embed_message_dict = {'url':'', 'title':'', 'values':'', 'footer':'' }

    soup = bs4.BeautifulSoup(resp.text)

    # This is bad and could break easily.
    last_update = str(soup.findAll("aside")[0].contents[44]) \
        + str(soup.findAll("aside")[0].contents[46])
    
    tables = dict(zip(config.TABLES, soup.findAll("table")))

    stats = tables.get(table)
    if stats:
        rows = stats.findAll("tr")
        table_values = []

        for idx, row in enumerate(rows):
            if idx == 0:
                continue
            else:
                modified = row.getText().split('\n')[1:-1]
                table_values.append(
                    tuple(modified[:2])
                )
    else:
        return False

    title = "Stats - {name} - {stat}".format(
        name=name,
        stat=config.TABLE_NAME_MAP.get(table)
    )
    
    embed_message_dict.update(
        {
            'url':resp.url,
            'description':config.TABLE_NAME_MAP.get(table),
            "title":title,
            "values":table_values,
            "footer":last_update.replace('\n', '').strip() + " (UTC)"
        }
    )
    return embed_message_dict
