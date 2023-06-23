__all__ = ["FakeContinuousHardware"]


import pathlib
import asyncio
import math
from typing import List

from yaqd_core import HasLimits, HasPosition, IsDaemon


class FakeFurnace(HasLimits, HasPosition, IsDaemon):
    _kind = "fake-furnace"

    def __init__(self, name, config, config_filepath):
        super().__init__(name, config, config_filepath)
        self._step = 0.0

    def get_ramp_time(self) -> float:
        return self._state["ramp_time"]

    def get_ramp_time_limits(self) -> List[float]:
        return [0, 100]

    def get_ramp_time_units(self) -> str:
        return "min"

    def _set_position(self, position: float) -> None:
        diff = self._state["position"] - self._state["destination"]
        if self._state["ramp_time"]:
            self._step = diff / (self._state["ramp_time"] * 60)
        else:
            self._step = diff

    def set_ramp_time(self, ramp_time: float) -> None:
        self._state["ramp_time"] = ramp_time

    async def update_state(self):
        while True:
            if math.isnan(self._state["position"]):
                if math.isnan(self._state["destination"]):
                    self._state["position"] = self.get_limits()[0]
                    self._state["destination"] = self.get_limits()[0]
                else:
                    self._state["position"] = self._state["destination"]
            diff = self._state["position"] - self._state["destination"]
            if abs(diff) <= abs(self._step):  # within one step
                self._state["position"] = self._state["destination"]
                self._busy = False
                await self._busy_sig.wait()
            else:
                self._state["position"] -= self._step
                await asyncio.sleep(1)
            self.logger.debug(f"position: {self._state['position']}")
