__all__ = ["Unpacker"]

import asyncio
import io
import struct

import fastavro  # type: ignore

from .handshake import handle_handshake, handshake_request_schema


class Unpacker:
    def __init__(self, protocol):
        self.protocol = protocol

        self._msg_bufs = asyncio.Queue()

        self._buf = io.BytesIO()
        self._remaining = 0

        self.handshake_complete = False
        self._handshake_response = None
        self.named_types = {t["name"]: t for t in self.protocol.get("types", [])}

    def __aiter__(self):
        return self

    async def __anext__(self):
        msg = await self._msg_bufs.get()
        print("Processing a message")
        parameters = None
        meta = self._read_object(
            {"type": "map", "values": "bytes"},
            msg,
        )
        message_name = self._read_object("string", msg)
        if message_name != "" and self.protocol["messages"][
            message_name
        ].get("request", []):
            parameters = self._read_parameters(message_name, msg)

        print(f"Identifieed {message_name=} with {parameters=}")
        hs = None
        if self._handshake_response:
            hs = self._handshake_response
            self._handshake_response = None
        return (
            hs,
            meta,
            message_name,
            parameters,
        )

    def feed(self, data: bytes):
        self._buf.seek(0, 2)
        while data:
            print(data, self._remaining, len(data))
            if self._remaining:
                written = self._buf.write(data[:self._remaining])
                data = data[written:]
                self._remaining -= written
            if data:
                self._remaining = struct.unpack_from(">L", data[:4])[0]
                data = data[4:]
                if  self._remaining == 0:
                    self._buf.seek(0)
                    if not self.handshake_complete:
                        print("Doing handshake")
                        handshake_request = self._read_object(
                            handshake_request_schema,
                            self._buf,
                        )
                        print("Read handshake request", handshake_request)
                        self._handshake_response = handle_handshake(
                            handshake_request, self.protocol
                        )
                        print(self._handshake_response.match)
                        if self._handshake_response.match == "BOTH":
                            print("Handshake complete")
                            self.handshake_complete = True

                    self._msg_bufs.put_nowait(self._buf)
                    self._buf = io.BytesIO()


    def _read_object(self, schema, buf):
        schema = fastavro.parse_schema(
            schema, expand=True, named_schemas=self.named_types
        )
        try:
            # Needed twice for nested types... Should likely be fixed upstream
            schema = fastavro.parse_schema(
                schema, expand=True, named_schemas=self.named_types
            )
        except fastavro.schema.SchemaParseException:
            pass  # Must not have needed the second pass...
        obj = fastavro.schemaless_reader(buf, schema)
        return obj

    def _read_parameters(self, name, buf):
        parameters = []
        for param_schema in self.protocol["messages"][name]["request"]:
            parameters.append(self._read_object(param_schema["type"], buf))
        return parameters
