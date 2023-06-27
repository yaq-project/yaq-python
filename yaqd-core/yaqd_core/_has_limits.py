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
        return self._joint_limit(self._state["hw_limits"], self._config["limits"])

    def _joint_limit(self, *limits):
        mins = []
        maxes = []
        for limit in limits:
            assert limit[0] < limit[1]
            mins.append(limit[0])
            maxes.append(limit[1])
        out = [max(mins), min(maxes)]
        assert out[0] < out[1]
        return out

    def in_limits(self, position: float) -> bool:
        low, upp = self.get_limits()
        return low <= position <= upp

    def set_position(self, position: float) -> None:
        if not self.in_limits(position):
            if self._out_of_limits == "closest":
                low, upp = self.get_limits()
                if position > upp:
                    position = upp
                elif position < low:
                    position = low
            elif self._out_of_limits == "ignore":
                return
            else:
                raise ValueError(f"{position} not in ranges {self.get_limits()}")
        super().set_position(position)
