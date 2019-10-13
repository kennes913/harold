"""

"""
from functools import wraps


def ranking(grouping: str = "realm") -> None:
    """
    This decorator wraps callbacks that return parsed statistics, 
    modifies the results to find rankings for a statistic for the 
    "realm" or "server".

    Argument:
        grouping :: str 
    """

    def decorator(stats_function):
        @wraps
        def wrapper(response: dict) -> dict:
            """
            """

            stats_response = stats_function(response)
            modified_response = {}

            for key, value in stats_response.items():

                if key in ("Last Updated", "Description", "URL"):
                    modified_response.update({key: value})
                    continue

                rank_value = value.get(f"# {grouping.title()}")
                modified_response.update({key: int(rank_value)})

            return resp

        return wrapper

    return decorator
