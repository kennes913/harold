"""
Useful filtering/parsing decorators to modify dictionary responses
in callback functions.
"""


def comparison(comp):
    def decorator(func):
        def wrapped(resp):
            initial_resp = func(resp)
            resp = {}
            for key, value in initial_resp.items():
                if key in (
                    "Last Updated",
                    "Description",
                    "URL",
                    "Embed Description",
                ):
                    resp.update({key: value})
                    continue
                rank_value = value.get(f"# {comp.title()}")
                resp.update({key: int(rank_value)})
            return resp

        return wrapped

    return decorator
