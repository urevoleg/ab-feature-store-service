import logging
import logging.config

import pathlib
from pprint import pprint

from config.settings import settings
from consumer.kafka_consumer import create_consumer
from consumer.message_handler import handle_message
from triggers.loader import load_triggers
from triggers.engine import TriggerEngine
from state.inmemory_store import InMemoryStateStore


def setup_logging():
    import yaml

    with pathlib.Path("config/logging.yaml").open() as f:
        logging.config.dictConfig(yaml.safe_load(f))


def main():
    setup_logging()
    logger = logging.getLogger(settings.APP_NAME)

    logger.info("Starting trigger engine (InMemory mode)")

    triggers = load_triggers(settings.TRIGGERS_PATH)
    store = InMemoryStateStore()
    engine = TriggerEngine(triggers, store)

    consumer = create_consumer()

    for msg in consumer:
        try:
            handle_message(msg.value, engine)
            consumer.commit()
        except Exception as e:
            logger.exception("Failed to process message")

        # временно — для наглядности
        logger.info("Current state:")
        for trigger_state in store.dump():
            pprint(trigger_state)


if __name__ == "__main__":
    main()
