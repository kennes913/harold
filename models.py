"""
"""
import requests
import mypy

from lxml.html.soupparser import fromstring
from typing import Callable, Union
from urllib.parse import quote


class HeraldPageMetadata:

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


class ParseAmount(HeraldPageMetadata):
    def __init__(
        self, callback: Union[None, Callable[[dict], dict]] = None
    ) -> None:
        self.response_structure = {
            "All Time": {},
            "This Week": {},
            "Last Week": {},
            "Last 48 Hours": {},
            "Last Updated": "",
            "Character Description": "",
        }
        self.callback = callback

    def __call__(self, endpoint: str) -> Union[dict, str]:
        response = requests.get(endpoint)

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
            character_description = soup.xpath(self.character_description)
            self.response_structure.update(
                {
                    "Last Updated": " ".join(
                        " ".join(last_updated).replace("\n", "").split()
                    ),
                    "Character Description": " ".join(
                        character_description[0].text_content().split()
                    ),
                }
            )

        else:
            return (
                f"There is an issue with the Herald ({response.status_code})."
            )
        if self.callback:
            return self.callback(self.response_structure)

        return self.response_structure


class ParseRealmKills(HeraldPageMetadata):
    def __init__(self, callback: Union[None, Callable[[dict], dict]]) -> None:
        self.response_structure = {
            "All Time": {},
            "This Week": {},
            "Last Week": {},
            "Last 48 Hours": {},
            "Last Updated": "",
            "Character Description": "",
        }
        self.callback = callback

    def __call__(self, endpoint: str) -> Union[dict, str]:
        response = requests.get(endpoint)
        if response.ok:
            soup = fromstring(response.text)
            for metric, xpath in self.xpath_table_map.items():
                if metric == "Realm Kills":
                    div, table = xpath
                    stats_column = (
                        f"{self.xpath_base_table.format(div=div, table=table)}"
                    )
                    for column in range(2, 5):
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
            character_description = soup.xpath(self.character_description)
            self.response_structure.update(
                {
                    "Last Updated": " ".join(
                        " ".join(last_updated).replace("\n", "").split()
                    ),
                    "Character Description": " ".join(
                        character_description[0].text_content().split()
                    ),
                }
            )
        else:
            return (
                f"There is an issue with the Herald ({response.status_code})."
            )
        if self.callback:
            return self.callback(self.response_structure)

        return self.response_structure


class ParseRank(HeraldPageMetadata):
    def __init__(self, callback: Union[None, Callable[[dict], dict]]) -> None:
        self.response_structure = {
            "All Time": {},
            "This Week": {},
            "Last Week": {},
            "Last 48 Hours": {},
            "Last Updated": "",
            "Character Description": "",
        }
        self.callback = callback

    def __call__(self, endpoint: str) -> Union[dict, str]:
        response = requests.get(endpoint)

        if response.ok:
            soup = fromstring(response.text)
            for metric, xpath in self.xpath_table_map.items():
                if metric == "Realm Kills":
                    continue
                metric_ranking = {}
                div, table = xpath
                stats_column = (
                    f"{self.xpath_base_table.format(div=div, table=table)}"
                )
                for column in range(3, 6):
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
                        metric_ranking.update(
                            {
                                measurement: int(
                                    element[0].text_content().replace(",", "")
                                )
                            }
                        )
                        insert.update({metric: metric_ranking})
            last_updated = soup.xpath(self.xpath_last_updated)
            character_description = soup.xpath(self.character_description)
            self.response_structure.update(
                {
                    "Last Updated": " ".join(
                        " ".join(last_updated).replace("\n", "").split()
                    ),
                    "Character Description": " ".join(
                        character_description[0].text_content().split()
                    ),
                }
            )
        else:
            return (
                f"There is an issue with the Herald ({response.status_code})."
            )
        if self.callback:
            return self.callback(self.response_structure)

        return self.response_structure
