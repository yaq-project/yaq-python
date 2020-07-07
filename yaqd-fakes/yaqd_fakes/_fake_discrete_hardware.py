__all__ = ["FakeDiscreteHardware"]

import asyncio
from typing import Dict, Any, List
import math

from yaqd_core import DiscreteHardware

from .__version__ import __branch__


class FakeDiscreteHardware(DiscreteHardware):
    _kind = "fake-discrete-hardware"
    _branch = __branch__

    def __init__(self, name, config, config_filepath):
        super().__init__(name, config, config_filepath)
        self._tolerance = config["tolerance"]
        self._sleep = config["sleep"]

    def _set_position(self, position):
        pass

    async def update_state(self):
        while True:
            if not math.isclose(self._state["position"], self._state["destination"]):
                await asyncio.sleep(self._sleep)
                self._state["position"] = self._state["destination"]
            for k, v in self._position_identifiers.items():
                if abs(self._state["position"] - v) < self._tolerance:
                    self._state["position_identifier"] = k
                    break
            else:
                self._state["position_identifier"] = None
            self._busy = False
            await self._busy_sig.wait()
