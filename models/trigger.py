from dataclasses import dataclass
from typing import Optional, Dict


@dataclass
class Trigger:
    name: str
    description: str
    type: str
    event_name: str
    where: Optional[Dict] = None
