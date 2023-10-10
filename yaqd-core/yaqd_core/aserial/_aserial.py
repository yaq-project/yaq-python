__all__ = ["ASerial", "get_aserial"]

import asyncio
from typing import Any, Dict

import serial  # type: ignore


class ASerial(serial.Serial):
    def __init__(self, port=None, baudrate=9600, eol=b"\n", *args, **kwargs):
        super().__init__(port, baudrate, timeout=0, *args, **kwargs)
        self._readlock = asyncio.Lock()
        self.eol = eol

    async def aread(self, size=1):
        async with self._readlock:
            return await self._aread(size)

    async def _aread(self, size=1):
        buf = b""
        while len(buf) < size:
            buf += self.read(size - len(buf))
            await asyncio.sleep(0.01)
        return buf

    async def areadline(self, size=-1):
        async with self._readlock:
            return await self._areadline(size)

    async def _areadline(self, size=-1):
        buf = b""
        while not buf.endswith(self.eol) and (size < 0 or len(buf) < size):
            buf += self.readline(size - len(buf) if size >= 0 else -1)
            await asyncio.sleep(0.01)
        return buf

    async def areadlines(self, hint=-1):
        async with self._readlock:
            size = 0
            while hint < 0 or size < hint:
                s = await self._areadline()
                size += len(s)
                yield s

    async def awrite_then_read(self, data, size=1):
        async with self._readlock:
            self.write(data)
            return await self._aread(size)

    async def awrite_then_readline(self, data, size=-1):
        async with self._readlock:
            self.write(data)
            return await self._areadline(size)


_serial_objects: Dict[str, ASerial] = {}


def get_aserial(
    port: str,
    baudrate: int = 9600,
    eol: bytes = b"\n",
    **kwargs: Any,
) -> ASerial:
    """Create a new ASerial object or return already existed one.

    Parameters
    ----------
    port: str
        Serial port identificator, e.g. 'COM0' or '/dev/ttyUSB0'
        If an matching open port exists, all other arguments are ignored.
    baudrate: int, optional
        Baud rate of the port. Defaults to 9600.
    eol: bytes, optional
        End of line terminator. Defaults to new-line.

    Other Parameters
    ----------------
    **kwargs: `serial.Serial` arguments, optional


    Returns
    -------
    ASerial
        Corresponding ASerial object
    """
    if port not in _serial_objects:
        _serial_objects[port] = ASerial(port=port, baudrate=baudrate, eol=eol, **kwargs)
    return _serial_objects[port]
