__all__ = ["HasMeasureTrigger"]


import asyncio
import pathlib
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod

from yaqd_core import IsSensor, IsDaemon
from ._is_sensor import MeasureType


class HasMeasureTrigger(IsSensor, IsDaemon, ABC):
    def __init__(self, name: str, config: Dict[str, Any], config_filepath: pathlib.Path):
        super().__init__(name, config, config_filepath)
        self._looping = False
        if self._config["loop_at_startup"]:
            self.measure(loop=True)

    def get_measured(self) -> MeasureType:
        return super().get_measured()

    @abstractmethod
    async def _measure(self) -> MeasureType:
        """Do measurement, filling _measured dictionary.

        Returns dictionary with keys channel names, values numbers or arrays.
        """
        raise NotImplementedError

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
            self._tasks.append(self._loop.create_task(self._runner()))
        return self._measurement_id

    async def _runner(self) -> None:
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
        current_task = asyncio.current_task()
        if current_task:
            self._tasks.remove(current_task)

    def stop_looping(self) -> None:
        """Stop looping."""
        self._looping = False
