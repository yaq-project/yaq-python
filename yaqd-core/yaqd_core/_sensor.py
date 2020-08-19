__all__ = ["Sensor"]


import asyncio
import pathlib
from typing import Dict, Any, Union, Tuple, List
from ._daemon import Base

MeasureType = Dict[str, Union[float]]


class Sensor(Base):
    _kind = "base-sensor"

    def __init__(self, name: str, config: Dict[str, Any], config_filepath: pathlib.Path):
        super().__init__(name, config, config_filepath)
        self._measured: MeasureType = dict()  # values must be numbers or arrays
        self._channel_names: List[str] = []
        self._channel_units: Dict[str, str] = dict()
        self._channel_shapes: Dict[str, Tuple[int]] = dict()
        self._measurement_id = 0
        self._looping = False

    def measure(self, loop: bool = False) -> int:
        """Start a measurement, optionally looping.

        Sensor will remain busy until measurement completes.

        Parameters
        ----------
        loop: bool, optional
            Toggle looping behavior. Default False.

        See Also
        --------
        stop_looping
        """
        self._looping = loop
        if not self._busy:
            self._busy = True
            self._loop.create_task(self._runner(loop=loop))
        return self._measurement_id

    def get_channel_names(self):
        """Get current channel names."""
        return self._channel_names

    def get_channel_shapes(self):
        """Get channel shapes."""
        # as default behavior, assume all channels are scalars
        if self._channel_shapes:
            return self._channel_shapes
        return {k: () for k in self._channel_names}

    def get_channel_units(self):
        """Get channel units."""
        return self._channel_units

    def get_measured(self) -> MeasureType:
        """Get most recently measured values."""
        return self._measured

    async def _measure(self) -> MeasureType:
        """Do measurement, filling _measured dictionary.

        Returns dictionary with keys channel names, values numbers or arrays.
        """
        raise NotImplementedError

    async def _runner(self, loop: bool) -> None:
        """Handle execution of _measure, including looping and setting of _measurement_id."""
        while True:
            self._measured = await self._measure()
            assert set(self._measured.keys()) == set(self._channel_names)
            self._measured["measurement_id"] = self._measurement_id
            if not self._looping:
                self._busy = False
                self._measurement_id += 1
                break
            await asyncio.sleep(0)

    def stop_looping(self) -> None:
        """Stop looping."""
        self._looping = False
