__all__ = ["HasPosition"]


import pathlib
from abc import abstractmethod
from typing import Any, Dict, Optional

import yaqd_core


class HasPosition(yaqd_core.IsDaemon):
    def __init__(
        self, name: str, config: Dict[str, Any], config_filepath: pathlib.Path
    ):
        self._units = self._config["units"]
        super().__init__(name, config, config_filepath)

    def get_position(self) -> float:
        return self._state["position"]

    def get_units(self) -> Optional[str]:
        return self._units

    def get_destination(self) -> float:
        return self._state["destination"]

    def set_position(self, position: float) -> None:
        self._busy = True
        self._state["destination"] = position
        self._set_position(position)

    @abstractmethod
    def _set_position(self, position: float) -> None:
        raise NotImplementedError

    def set_relative(self, distance: float) -> float:
        new = self._state["destination"] + distance
        self.set_position(new)
        return new
