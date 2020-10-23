__all__ = ["FakeHasTurret"]


import asyncio
import math

from yaqd_core import HasTurret, HasLimits, HasPosition, IsDaemon


class FakeHasTurret(HasTurret, HasLimits, HasPosition, IsDaemon):
    _kind = "fake-has-turret"

    def __init__(self, name, config, config_filepath):
        super().__init__(name, config, config_filepath)
        self._velocity = config["velocity"]
        self._units = config["units"]

    def _set_position(self, position: float) -> None:
        pass

    def set_turret(self, index):
        self._busy = True
        self.logger.debug(self._state["turret"], index)
        if index != self._state["turret"]:
            self._state["turret"] = index

    def get_turret(self):
        return self._state["turret"]

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
