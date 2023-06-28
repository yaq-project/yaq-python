__all__ = ["HasLimits"]


import pathlib
from typing import Dict, Any, Optional, List

from yaqd_core import HasPosition, IsDaemon


class HasLimits(HasPosition, IsDaemon):
    def __init__(
        self, name: str, config: Dict[str, Any], config_filepath: pathlib.Path
    ):
        super().__init__(name, config, config_filepath)
        self._out_of_limits = config["out_of_limits"]

    def get_limits(self) -> List[float]:
        # wrapper for client
        return self.limits

    @property
    def limits(self) -> List[float]:
        # for internal use
        return self._joint_limit(self._state["hw_limits"], self._config["limits"])

    @classmethod
    def _joint_limit(cls, *limits: List[float]):
        mins, maxes = [*zip(*limits)]
        assert all([mini < maxi for mini, maxi in zip(mins, maxes)])
        out = [max(*mins), min(*maxes)]
        assert out[0] < out[1]
        return out

    def in_limits(self, position: float) -> bool:
        return self._in_limits(position)

    def _in_limits(self, position):
        # for internal use
        low, upp = self.limits
        return low <= position <= upp

    def set_position(self, position: float) -> None:
        if not self._in_limits(position):
            if self._out_of_limits == "closest":
                low, upp = self.limits
                if position > upp:
                    position = upp
                elif position < low:
                    position = low
            elif self._out_of_limits == "ignore":
                return
            else:
                raise ValueError(f"{position} not in ranges {self.limits}")
        super().set_position(position)
