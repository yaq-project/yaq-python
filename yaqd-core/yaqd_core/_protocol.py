import asyncio
import io
import struct

import fastavro  # type: ignore
from . import avrorpc


class Protocol(asyncio.Protocol):
    def __init__(self, daemon, *args, **kwargs):
        self._daemon = daemon
        self.logger = daemon.logger
        self._avro_protocol = daemon._avro_protocol
        self._named_types = {t["name"]: t for t in self._avro_protocol.get("types", [])}
        asyncio.Protocol.__init__(self, *args, **kwargs)

    def connection_lost(self, exc):
        peername = self.transport.get_extra_info("peername")
        self.logger.info(f"Connection lost from {peername} to {self._daemon.name}")
        self._daemon._connection_lost(peername)

    def connection_made(self, transport):
        """Process an incomming connection."""
        peername = transport.get_extra_info("peername")
        self.logger.info(f"Connection made from {peername} to {self._daemon.name}")
        self.transport = transport
        self.unpacker = avrorpc.Unpacker(self._avro_protocol)
        self._daemon._connection_made(peername)

    def data_received(self, data):
        """Process an incomming request."""
        self.logger.debug(f"Data received: {repr(data)}")
        if not self._daemon._server.is_serving():
            self.transport.close()
        self.unpacker.feed(data)
        try:
            for hs, meta, name, params in self.unpacker:
                if hs is not None:
                    out = bytes(hs)
                    out = struct.pack(">L", len(out)) + out
                    self.transport.write(out)
                    if hs.match == "NONE":
                        name = ""

                out_meta = io.BytesIO()
                fastavro.schemaless_writer(out_meta, {"type": "map", "values": "bytes"}, meta)
                length = out_meta.tell()
                self.transport.write(struct.pack(">L", length) + out_meta.getvalue())
                self.logger.debug(f"Wrote meta, {meta}, {out_meta.getvalue()}")
                try:
                    response_out = io.BytesIO()
                    response = None
                    response_schema = "null"
                    if name:
                        fun = getattr(self._daemon, name)
                        if params is None:
                            params = []
                        response = fun(*params)
                        response_schema = fastavro.parse_schema(
                            self._avro_protocol["messages"][name].get("response", "null"),
                            expand=True,
                            _named_schemas=self._named_types,
                        )
                        # Needed twice for nested types... Probably can be fixed upstream
                        response_schema = fastavro.parse_schema(
                            response_schema, expand=True, _named_schemas=self._named_types,
                        )
                    fastavro.schemaless_writer(response_out, response_schema, response)
                except Exception as e:
                    self.logger.error(f"Caught exception: {type(e)} in message {name}")
                    self.transport.write(struct.pack(">L", 1) + b"\1")
                    error_out = io.BytesIO()
                    fastavro.schemaless_writer(error_out, ["string"], repr(e))
                    length = error_out.tell()
                    self.transport.write(struct.pack(">L", length) + error_out.getvalue())
                else:
                    self.transport.write(struct.pack(">L", 1) + b"\0")
                    self.logger.debug(f"Wrote non-error flag")
                    length = response_out.tell()
                    self.transport.write(struct.pack(">L", length) + response_out.getvalue())
                    self.logger.debug(f"Wrote response {response}, {response_out.getvalue()}")
                self.transport.write(struct.pack(">L", 0))
                if name == "shutdown":
                    self.logger.debug("Closing transport")
                    self.transport.close()

        except (ValueError):
            pass
