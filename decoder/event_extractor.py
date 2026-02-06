from datetime import datetime
from typing import List

import pendulum

from models.event import NormalizedEvent


def extract_events(payload: dict) -> List[NormalizedEvent]:
    events = []

    # достаем magnit_id
    user_ids = payload["user_prop"]["ids"]
    magnit_id = next(
        x["value"] for x in user_ids if x["key"] == "magnit_id"
    )

    for e in payload["event_prop"]:
        events.append(
            NormalizedEvent(
                event_name=e["event_name"],
                user_id=magnit_id,
                ts=pendulum.parse(e["timestamp_with_offset"]),
                props=e["event_attrs"],
            )
        )

    return events
