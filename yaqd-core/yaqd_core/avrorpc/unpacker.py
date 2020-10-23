__all__ = ["Unpacker"]

import asyncio
import io
import struct

import fastavro  # type: ignore

from .handshake import handle_handshake, handshake_request_schema


class Unpacker:
    def __init__(self, protocol, file_like=None):
        self.protocol = protocol
        if file_like is None:
            self._file = io.BytesIO()
        else:
            self._file = file_like
        self.buf = io.BytesIO()
        self.handshake_complete = False
        self.handshake_response = None
        self.meta = None
        self.message_name = None
        self.parameters = None
        self.remaining = 0
        self.named_types = {t["name"]: t for t in self.protocol.get("types", [])}

    def __iter__(self):
        return self

    def __next__(self):
        try:
            if not self.handshake_complete and self.handshake_response is None:
                handshake_request = self._read_object(handshake_request_schema)
                self.handshake_response = handle_handshake(
                    handshake_request, self.protocol
                )
                if self.handshake_response.match == "BOTH":
                    self.handshake_complete = True
            if self.meta is None:
                self.meta = self._read_object({"type": "map", "values": "bytes"})
            if self.message_name is None:
                self.message_name = self._read_object("string")
            if self.message_name != "" and self.protocol["messages"][
                self.message_name
            ].get("request", []):
                self._read_parameters(self.message_name)

            ret = (
                self.handshake_response,
                self.meta,
                self.message_name,
                self.parameters,
            )
            self.handshake_response = None
            self.meta = None
            self.message_name = None
            self.parameters = None
            return ret

        except (ValueError, struct.error):
            raise StopIteration

    def __aiter__(self):
        return self

    async def __anext__(self):
        while True:
            try:
                return next(self)
            except StopIteration:
                await asyncio.sleep(0.001)

    def feed(self, data: bytes):
        # Must support random access, if it does not, must be fed externally (e.g. TCP)
        pos = self._file.tell()
        self._file.seek(0, 2)
        self._file.write(data)
        self._file.seek(pos)

    def _read_object(self, schema):
        schema = fastavro.parse_schema(
            schema, expand=True, _named_schemas=self.named_types
        )
        try:
            # Needed twice for nested types... Should likely be fixed upstream
            schema = fastavro.parse_schema(
                schema, expand=True, _named_schemas=self.named_types
            )
        except fastavro.schema.SchemaParseException:
            pass  # Must not have needed the second pass...
        while True:
            try:
                self.buf.seek(0)
                obj = fastavro.schemaless_reader(self.buf, schema)
                self.buf = io.BytesIO()
                return obj
            except Exception:
                self.buf.seek(0)
            if not self.remaining:
                self.remaining = struct.unpack_from(">L", self._file.read(4))[0]

            self.buf.seek(0, 2)
            num_read = self.buf.write(self._file.read(self.remaining))
            self.remaining -= num_read

    def _read_parameters(self, name):
        if self.parameters is None:
            self.parameters = []
        for param_schema in self.protocol["messages"][name]["request"][
            len(self.parameters) :
        ]:
            self.parameters.append(self._read_object(param_schema["type"]))
