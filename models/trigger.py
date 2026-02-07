from dataclasses import dataclass
from typing import Optional, Dict


@dataclass
class Trigger:
    name: str
    description: str
    type: str                  # flag | metric
    event_name: Dict           # eq | in | regex
    where: Optional[Dict] = None
