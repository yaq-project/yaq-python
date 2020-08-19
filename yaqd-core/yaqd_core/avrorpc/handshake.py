from dataclasses import dataclass, asdict
from enum import Enum
import json
from io import BytesIO
from typing import Dict, Optional

import fastavro  # type: ignore

from .protocol import hash_protocol

handshake_request_schema = fastavro.parse_schema(
    {
        "type": "record",
        "name": "HandshakeRequest",
        "namespace": "org.apache.avro.ipc",
        "fields": [
            {"name": "clientHash", "type": {"type": "fixed", "name": "MD5", "size": 16},},
            {"name": "clientProtocol", "type": ["null", "string"]},
            {"name": "serverHash", "type": "MD5"},
            {"name": "meta", "type": ["null", {"type": "map", "values": "bytes"}]},
        ],
    }
)


@dataclass
class HandshakeRequest:
    """avro RPC handshake request."""

    clientHash: bytes
    clientProtocol: Optional[str]
    serverHash: bytes
    meta: Optional[Dict[str, bytes]] = None

    def __bytes__(self):
        fo = BytesIO()
        fastavro.schemaless_writer(fo, handshake_request_schema, asdict(self))
        fo.seek(0)
        return fo.read()

    @classmethod
    def from_bytes(cls, data):
        fo = BytesIO()
        fo.write(data)
        fo.seek(0)
        return cls(**fastavro.schemaless_reader(fo, handshake_request_schema))


class HandshakeMatch(str, Enum):
    BOTH = "BOTH"
    CLIENT = "CLIENT"
    NONE = "NONE"


handshake_response_schema = fastavro.parse_schema(
    {
        "type": "record",
        "name": "HandshakeResponse",
        "namespace": "org.apache.avro.ipc",
        "fields": [
            {
                "name": "match",
                "type": {
                    "type": "enum",
                    "name": "HandshakeMatch",
                    "symbols": ["BOTH", "CLIENT", "NONE"],
                },
            },
            {"name": "serverProtocol", "type": ["null", "string"]},
            {
                "name": "serverHash",
                "type": ["null", {"type": "fixed", "name": "MD5", "size": 16}],
            },
            {"name": "meta", "type": ["null", {"type": "map", "values": "bytes"}]},
        ],
    }
)


@dataclass
class HandshakeResponse:
    match: HandshakeMatch
    serverProtocol: Optional[str]
    serverHash: Optional[bytes]
    meta: Optional[Dict[str, bytes]] = None

    def __dict__(self):
        asdict(self)

    def __bytes__(self):
        fo = BytesIO()
        fastavro.schemaless_writer(fo, handshake_response_schema, asdict(self))
        fo.seek(0)
        return fo.read()

    @classmethod
    def from_bytes(cls, data):
        fo = BytesIO()
        fo.write(data)
        fo.seek(0)
        return cls(**fastavro.schemaless_reader(fo, handshake_request_schema))


def handle_handshake(request, protocol):
    request = HandshakeRequest(**request)
    # TODO actual caching

    match = HandshakeMatch.NONE
    server_protocol = None
    server_hash = None

    if request.clientProtocol is None:
        match = HandshakeMatch.NONE
    elif request.serverHash == hash_protocol(protocol):
        match = HandshakeMatch.BOTH

    if match != HandshakeMatch.BOTH:
        server_protocol = json.dumps(protocol)
        server_hash = hash_protocol(protocol)
    return HandshakeResponse(match=match, serverProtocol=server_protocol, serverHash=server_hash)
