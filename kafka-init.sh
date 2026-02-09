docker exec -it kafka kafka-topics \
  --bootstrap-server localhost:9092 \
  --create \
  --topic event_processor.events.saved.v1 \
  --partitions 1 \
  --replication-factor 1