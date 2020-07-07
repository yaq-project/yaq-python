import json
import hashlib


def hash_protocol(protocol):
    return hashlib.md5(json.dumps(protocol).encode()).digest()
