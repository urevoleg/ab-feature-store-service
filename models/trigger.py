from dataclasses import dataclass
from typing import Optional, Dict


@dataclass
class Trigger:
    name: str
    type: str
    where: Optional[Dict] = None
