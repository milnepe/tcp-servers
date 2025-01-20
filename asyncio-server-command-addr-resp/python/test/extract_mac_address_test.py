import json

message = b'{"src_addr": "f0:24:f9:59:1f:60","data": "Hello TCP Server!","level": 1,"count": 24673}\r\n'
# message = b'{"command": "ON"}'

def extract_mac_address(message):
    try:
        message_json = json.loads(message)
        mac = message_json.get("src_addr")
        if not mac:
            return "00:00:00:00:00:00"
        return mac
    except json.JSONDecodeError:
        print(f"Failed to decode JSON message: {message}")
        return "00:00:00:00:00:00"

print(extract_mac_address(message)) # f0:24:f9:59:1f:60
