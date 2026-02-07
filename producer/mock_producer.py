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
PAGES = ("mainpage", "delivery", "productScreen", "clubMain", "todayMain", "success", "magnets", "favCategory")
EVENTS = ("app_launch", "add_to_cart",
          "product_listing", "product_view",
          "mainpage_click", "auth", "reg_success",
          "today_benefitsMain_magnet_click",
          "today_benefitsMain_magnet_click",
          "today_gameWin_view",
          "profile_gameWin_view",
          "delivery_gameWin_view",
          "catalog_gameWin_view",
          "market_gameWin_view",
          "miniAppCosmetic_gameWin_view",
          "system_gameWin_view",
          )
USERS = ("6d85b107-73e0-4457-a742-eb9c52ad83a1",
         "945e60dd-0c64-419f-98a8-16654e3d4a5d",
         "014dfea7-f697-4683-be8b-346d712198a0",
         "7c0643dc-2d10-49bd-9155-02c24835a577",
         "69fc4284-81a5-4a31-9650-609f35a89eef",
         "66efe36d-f183-407a-af59-e492d1a2d351",
         "6659d065-374a-4c42-a942-31d6287bf1d7",
         "34b8d772-2ca2-4030-886c-cc825851fd97",
         "9607c6f3-beb2-4df1-abfe-c2f52c3ab133",
         "633b3711-9b17-44b2-b297-b7b88e136850")


def build_event(event_name: str, magnit_id: str, batch_size: int = 25) -> dict:
    payload = {
        "event_prop": [
            {
                "event_name": event_name,
                "timestamp_with_offset": pendulum.now("UTC").to_iso8601_string(),
                "event_attrs": {
                    "action": random.choice(ACTIONS),
                    "page": random.choice(PAGES)
                },
                "version": 0
            } for _ in range(batch_size)
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
