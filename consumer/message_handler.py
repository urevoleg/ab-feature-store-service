from decoder.binary_decoder import decode_binary_data
from decoder.event_extractor import extract_events
from triggers.engine import TriggerEngine


def handle_message(msg: dict, engine: TriggerEngine):
    payload = decode_binary_data(msg["binaryData"])
    events = extract_events(payload)

    for event in events:
        engine.process(event)
