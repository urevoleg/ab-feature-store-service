import base64
import json


def decode_binary_data(binary_data: str) -> dict:
    raw = base64.b64decode(binary_data)
    return json.loads(raw)
