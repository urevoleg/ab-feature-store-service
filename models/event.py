from dataclasses import dataclass
from datetime import datetime
from typing import Dict


@dataclass
class NormalizedEvent:
    event_name: str
    user_id: str
    ts: datetime
    props: Dict
