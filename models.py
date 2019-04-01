"""
Callable classes that are responsible for parsing the herald. The design
was inspired by an article detailing a strict enforcement of the SRP.
"""
import config

import requests
import mypy

from lxml.html.soupparser import fromstring
from typing import Callable, Union
from urllib.parse import quote


class PageMetadata:

    xpath_table_map = {
        "Realm Points": (1, 1),
        "Deathblows": (1, 2),
        "Deaths": (1, 3),
        "Kills": (2, 1),
        "Solo Kills": (2, 2),
        "Realm Kills": (2, 3),
    }
    xpath_time_period_map = {
        1: "All Time",
        2: "This Week",
        3: "Last Week",
        4: "Last 48 Hours",
    }
    xpath_base_table = "/html/body/main/div[2]/div[{div}]/table[{table}]/"
    xpath_last_updated = "/html/body/aside/text()"
    character_description = "/html/body/main/div[1]/div"


class GetAmounts(PageMetadata):
    def __init__(
        self, callback: Union[None, Callable[[dict], dict]] = None
    ) -> None:
        self.response_structure = {
            "All Time": {},
            "This Week": {},
            "Last Week": {},
            "Last 48 Hours": {},
            "Last Updated": "",
            "Description": "",
            "URL": "",
        }
        self.callback = callback

    def __call__(self, endpoint: str) -> Union[dict, str]:
        """HTTP GET `endpoint` and extract statistics realm points,
        deaths, deathblows, kills and solo kills from table.

        Arguments:
        endpoint :: str 
            The URL
        
        Example:
        
        realm_kills = models.GetRealmKills('https://herald.playphoenix.online/c/Debug')
        """
        response = requests.get(endpoint)
        if response.url == config.FAILED_RESPONSE_REDIRECT:
            return False

        print(response.url)

        if response.ok:
            soup = fromstring(response.text)
            for metric, xpath in self.xpath_table_map.items():
                if metric == "Realm Kills":
                    continue
                div, table = xpath
                stats_column = (
                    f"{self.xpath_base_table.format(div=div, table=table)}"
                )
                for row in range(1, 5):
                    element = soup.xpath(
                        f"{stats_column}/tbody/tr[{row}]/td[2]"
                    )
                    insert = self.response_structure.get(
                        self.xpath_time_period_map.get(row)
                    )
                    insert.update(
                        {
                            metric: int(
                                element[0].text_content().replace(",", "")
                            )
                        }
                    )
            last_updated = soup.xpath(self.xpath_last_updated)

            # The character description feels too procedural. There's a better
            # way to do this with an isolated function.
            chracter_data = soup.xpath(self.character_description)
            character_description = " ".join(
                chracter_data[0].text_content().split()
            )
            character_description = character_description.replace("> ", " - ")
            character_description = character_description.replace(" <", " - ")

            self.response_structure.update(
                {
                    "Last Updated": " ".join(
                        " ".join(last_updated).replace("\n", "").split()
                    )
                    + " (UTC)",
                    "Description": character_description,
                    "URL": endpoint,
                }
            )
        else:
            return (
                f"There is an issue with the Herald ({response.status_code})."
            )
        if self.callback:
            return self.callback(self.response_structure)

        return self.response_structure


class GetRealmKills(PageMetadata):
    def __init__(
        self, callback: Union[None, Callable[[dict], dict]] = None
    ) -> None:
        self.response_structure = {
            "All Time": {},
            "This Week": {},
            "Last Week": {},
            "Last 48 Hours": {},
            "Last Updated": "",
            "Description": "",
            "URL": "",
        }
        self.callback = callback

    def __call__(self, endpoint: str) -> Union[dict, str]:
        """HTTP GET `endpoint` and extract amount of realm 
        kills from table.

        Arguments:
        endpoint :: str 
            The URL
        
        Example:
        
        realm_kills = models.GetRealmKills('https://herald.playphoenix.online/c/Debug')
        """
        response = requests.get(endpoint)
        if response.url == config.FAILED_RESPONSE_REDIRECT:
            return False

        if response.ok:
            soup = fromstring(response.text)
            for metric, xpath in self.xpath_table_map.items():
                if metric == "Realm Kills":
                    div, table = xpath
                    stats_column = (
                        f"{self.xpath_base_table.format(div=div, table=table)}"
                    )
                    column_range = (
                        range(2, 4) if "/g/" in endpoint else range(2, 5)
                    )
                    for column in column_range:
                        dimension_elements = soup.xpath(
                            f"{stats_column}/thead/tr/th[{column}]"
                        )
                        measurement = dimension_elements[0].text_content()
                        for row in range(1, 5):
                            element = soup.xpath(
                                f"{stats_column}/tbody/tr[{row}]/td[{column}]"
                            )
                            insert = self.response_structure.get(
                                self.xpath_time_period_map.get(row)
                            )
                            insert.update(
                                {
                                    measurement: int(
                                        element[0]
                                        .text_content()
                                        .replace(",", "")
                                    )
                                }
                            )
            last_updated = soup.xpath(self.xpath_last_updated)

            # The character description feels too procedural. There's a better
            # way to do this with an isolated function.
            chracter_data = soup.xpath(self.character_description)
            character_description = " ".join(
                chracter_data[0].text_content().split()
            )
            character_description = character_description.replace("> ", " - ")
            character_description = character_description.replace(" <", " - ")

            self.response_structure.update(
                {
                    "Last Updated": " ".join(
                        " ".join(last_updated).replace("\n", "").split()
                    )
                    + " (UTC)",
                    "Description": character_description,
                    "URL": endpoint,
                }
            )
        else:
            return (
                f"There is an issue with the Herald ({response.status_code})."
            )
        if self.callback:
            return self.callback(self.response_structure)

        return self.response_structure


class GetRanks(PageMetadata):
    def __init__(
        self, callback: Union[None, Callable[[dict], dict]] = None
    ) -> None:
        self.response_structure = {
            "All Time": {},
            "This Week": {},
            "Last Week": {},
            "Last 48 Hours": {},
            "Last Updated": "",
            "Description": "",
        }
        self.callback = callback

    def __call__(self, endpoint: str) -> Union[dict, str]:
        """HTTP GET `endpoint` and extract rank statistics for realm points,
        deaths, deathblows, kills and solo kills from table.

        Arguments:
        endpoint :: str 
            The URL
        
        Example:
        
        realm_kills = models.GetRanks('https://herald.playphoenix.online/c/Debug')
        """
        response = requests.get(endpoint)
        if response.url == config.FAILED_RESPONSE_REDIRECT:
            return False

        if response.ok:
            soup = fromstring(response.text)

            for metric, xpath in self.xpath_table_map.items():

                if metric == "Realm Kills":
                    continue

                div, table = xpath
                stats_column = (
                    f"{self.xpath_base_table.format(div=div, table=table)}"
                )
                column_range = (
                    range(3, 5) if "/g/" in endpoint else range(3, 6)
                )

                for column in column_range:

                    dimension_elements = soup.xpath(
                        f"{stats_column}/thead/tr/th[{column}]"
                    )
                    measurement = dimension_elements[0].text_content()

                    for row in range(1, 5):

                        element = soup.xpath(
                            f"{stats_column}/tbody/tr[{row}]/td[{column}]"
                        )

                        insert = self.response_structure.get(
                            self.xpath_time_period_map.get(row)
                        )
                        metric_ranking = insert.setdefault(metric, {})
                        metric_ranking.update(
                            {
                                measurement: int(
                                    element[0].text_content().replace(",", "")
                                )
                            }
                        )
            last_updated = soup.xpath(self.xpath_last_updated)

            # The character description feels too procedural. There's a better
            # way to do this with an isolated function.
            chracter_data = soup.xpath(self.character_description)
            character_description = " ".join(
                chracter_data[0].text_content().split()
            )
            character_description = character_description.replace("> ", " - ")
            character_description = character_description.replace(" <", " - ")

            self.response_structure.update(
                {
                    "Last Updated": " ".join(
                        " ".join(last_updated).replace("\n", "").split()
                    )
                    + " (UTC)",
                    "Description": character_description,
                    "URL": endpoint,
                }
            )
        else:
            return (
                f"There is an issue with the Herald ({response.status_code})."
            )
        if self.callback:
            return self.callback(self.response_structure)

        return self.response_structure


MODEL_MAP = {
    "rps": GetAmounts,
    "deathblows": GetAmounts,
    "deaths": GetAmounts,
    "kills": GetAmounts,
    "solos": GetAmounts,
    "irs": GetAmounts,
    "realm kills": GetRealmKills,
    "rank": GetRanks,
}
