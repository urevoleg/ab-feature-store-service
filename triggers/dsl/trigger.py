

def match_trigger(where: dict, event_attrs: dict) -> bool:
    if not where:
        return True

    if "eq" in where:
        for key, value in where["eq"].items():
            if event_attrs.get(key) != value:
                return False
        return True

    if "in" in where:
        for key, values in where["in"].items():
            if event_attrs.get(key) not in values:
                return False
        return True

    if "and" in where:
        return all(match_trigger(cond, event_attrs) for cond in where["and"])

    if "or" in where:
        return any(match_trigger(cond, event_attrs) for cond in where["or"])

    raise ValueError(f"Unknown DSL operator: {where}")
