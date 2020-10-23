__all__ = ["FakeContinuousHardware"]


import pathlib
import asyncio
import math
import json

from yaqd_core import HasLimits, HasPosition, IsDaemon


class FakeContinuousHardware(HasLimits, HasPosition, IsDaemon):
    _kind = "fake-continuous-hardware"

    def __init__(self, name, config, config_filepath):
        super().__init__(name, config, config_filepath)
        self._velocity = config["velocity"]
        self._units = config["units"]

    def _set_position(self, position: float) -> None:
        pass

    async def update_state(self):
        while True:
            if math.isnan(self._state["position"]):
                if math.isnan(self._state["destination"]):
                    self._busy = False
                    await self._busy_sig.wait()
                    continue
                self._state["position"] = self._state["destination"]
            diff = self._state["position"] - self._state["destination"]
            step = math.copysign(self._velocity, diff) * 0.025
            if abs(diff) <= abs(step):  # within one step
                self._state["position"] = self._state["destination"]
                self._busy = False
                await self._busy_sig.wait()
            else:
                self._state["position"] -= step
                await asyncio.sleep(0.025)
            self.logger.debug(f"position: {self._state['position']}")
