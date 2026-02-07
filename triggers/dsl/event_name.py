import re
from functools import lru_cache


@lru_cache(maxsize=512)
def _compile(pattern: str):
    return re.compile(pattern)


def match_event_name(rule: dict, value: str) -> bool:
    if "or" in rule:
        return any(
            match_event_name(sub, value)
            for sub in rule["or"]
        )

    if "and" in rule:
        return all(
            match_event_name(sub, value)
            for sub in rule["and"]
        )

    if "eq" in rule:
        return value == rule["eq"]

    if "in" in rule:
        if not isinstance(rule["in"], set):
            rule["in"] = set(rule["in"])
        return value in rule["in"]

    if "regex" in rule:
        return bool(_compile(rule["regex"]).match(value))

    if "ends_with" in rule:
        return value.endswith(rule["ends_with"])

    if "starts_with" in rule:
        return value.startswith(rule["starts_with"])

    raise ValueError(f"Unsupported event_name rule: {rule}")
