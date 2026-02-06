import yaml
from models.trigger import Trigger


def load_triggers(path: str) -> list[Trigger]:
    with open(path) as f:
        raw = yaml.safe_load(f)

    return [Trigger(**t) for t in raw["triggers"]]
