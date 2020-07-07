import json
import pathlib

__here__ = pathlib.Path(__file__).parent

with open(__here__ / "HandshakeRequest.avsc", "r") as f:
    handshake_request = json.load(f)


with open(__here__ / "HandshakeResponse.avsc", "r") as f:
    handshake_response = json.load(f)
