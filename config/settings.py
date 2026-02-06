import os



class Settings:
    # App
    APP_NAME = "trigger-engine"
    ENV = os.getenv("ENV", "local")

    # Kafka
    KAFKA_BOOTSTRAP_SERVERS = os.getenv(
        "KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"
    )
    KAFKA_TOPIC = os.getenv(
        "KAFKA_TOPIC", "event_processor.events.saved.v1"
    )
    KAFKA_GROUP_ID = os.getenv(
        "KAFKA_GROUP_ID", "ab-trigger-engine-v1"
    )
    KAFKA_AUTO_OFFSET_RESET = "earliest"

    # Redis
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB = int(os.getenv("REDIS_DB", "0"))
    REDIS_TTL_SECONDS = int(
        os.getenv("REDIS_TTL_SECONDS", "172800")  # 2 дня
    )

    # Triggers
    TRIGGERS_PATH = os.getenv(
        "TRIGGERS_PATH", "triggers/triggers.yaml"
    )


settings = Settings()
