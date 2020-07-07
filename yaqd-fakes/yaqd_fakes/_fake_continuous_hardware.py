__all__ = ["FakeContinuousHardware"]

import asyncio
from typing import Dict, Any, List
import math

from yaqd_core import ContinuousHardware

from .__version__ import __branch__


class FakeContinuousHardware(ContinuousHardware):
    _kind = "fake-continuous-hardware"
    _branch = __branch__

    def __init__(self, name, config, config_filepath):
        super().__init__(name, config, config_filepath)
        self._velocity = config["velocity"]

    def _set_position(self, position: float) -> None:
        pass

    async def update_state(self):
        while True:
            if math.isnan(self._state["position"]):
                self._state["position"] = self._state["destination"]
            diff = self._state["position"] - self._state["destination"]
            step = math.copysign(self._velocity, diff) * 0.001
            if abs(diff) <= abs(step):  # within one step
                self._state["position"] = self._state["destination"]
                self._busy = False
                await self._busy_sig.wait()
            else:
                self._state["position"] -= step
                await asyncio.sleep(0.001)
            self.logger.debug(f"position: {self._state['position']}")
