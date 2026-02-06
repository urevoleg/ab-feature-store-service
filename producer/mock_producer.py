import os
import json
import base64
import random
import time
import uuid
from datetime import datetime, timezone
import pendulum
from kafka import KafkaProducer

from config.settings import settings

from dotenv import load_dotenv
load_dotenv()

ACTIONS = ("click", "view", "scroll", "add_to_cart")
EVENTS = ("app_launch", "add_to_cart",
          "product_listing", "product_view",
          "mainpage_click", "auth", "reg_success")
USERS = ("6d85b107-73e0-4457-a742-eb9c52ad83a1",
         "945e60dd-0c64-419f-98a8-16654e3d4a5d",
         "014dfea7-f697-4683-be8b-346d712198a0",
         "7c0643dc-2d10-49bd-9155-02c24835a577",
         "69fc4284-81a5-4a31-9650-609f35a89eef")


def build_event(event_name: str, magnit_id: str) -> dict:
    payload = {
        "event_prop": [
            {
                "event_name": event_name,
                "timestamp_with_offset": pendulum.now("UTC").to_iso8601_string(),
                "event_attrs": {
                    "action": random.choice(ACTIONS)
                },
                "version": 0
            }
        ],
        "user_prop": {
            "ids": [
                {"key": "magnit_id", "value": magnit_id}
            ]
        }
    }

    binary_data = str(base64.b64encode(
        json.dumps(payload).encode()
    ).decode())

    return {
        "id": str(uuid.uuid4()),
        "specVersion": "1.0",
        "type": f"{event_name}@v1",
        "binaryData": binary_data,
        "time": pendulum.now("UTC").to_iso8601_string()
    }


def main(dry_run: bool = True):
    producer = KafkaProducer(
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode("utf-8"),
    )

    while True:
        event = build_event(
            event_name=random.choice(EVENTS),
            magnit_id=random.choice(USERS)
        )

        print(event)
        if not dry_run:
            producer.send(settings.KAFKA_TOPIC, event)
            producer.flush()
        time.sleep(1)


if __name__ == "__main__":
    main(dry_run=False)
