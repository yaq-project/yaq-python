__all__ = ["FakeHasTransformedPosition"]

import asyncio
import math
import pathlib
from typing import Dict, Any, Optional, List

from yaqd_core import HasTransformedPosition


class FakeHasTransformedPosition(HasTransformedPosition):
    _kind = "fake-has-transformed-position"

    def __init__(
        self, name: str, config: Dict[str, Any], config_filepath: pathlib.Path
    ):
        super().__init__(name, config, config_filepath)
        # current parameters for a fake daemon with has transformed position
        # limits should be specified in the config for the fake
        self._velocity = config["velocity"]
        self.set_native_reference(1.0)
        self.factor = config["factor"]

    def _set_position(self, position: float) -> None:
        pass

    def _relative_to_transformed(self, relative_position):
        """convert a relative coordinate to a transformed coordinate.
        Relative coordinates differ from natural coordinates in that the null position has been subtracted.
        (i.e. in relative coordinates reference position is zero).
        """
        transformed_position = 2.0 * relative_position
        return transformed_position

    def _transformed_to_relative(self, transformed_position):
        """convert a transformed coordinate to a relative coordinate
        Relative coordinates differ from natural coordinates in that the null position has been subtracted.
        (i.e. in relative coordinates reference position is zero).
        """
        relative_position = 0.5 * transformed_position
        return relative_position

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
