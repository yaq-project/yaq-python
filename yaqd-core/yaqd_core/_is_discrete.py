__all__ = ["IsDiscrete"]


import pathlib
from typing import Dict, Any, Optional


import yaqd_core


class IsDiscrete(yaqd_core.HasPosition, yaqd_core.IsDaemon):
    def __init__(
        self, name: str, config: Dict[str, Any], config_filepath: pathlib.Path
    ):
        self._position_identifiers: Dict[str, float] = config.get("identifiers", {})
        super().__init__(name, config, config_filepath)

    def get_position_identifiers(self) -> Dict[str, float]:
        return self._position_identifiers

    def set_identifier(self, identifier: str) -> float:
        p = self._position_identifiers[identifier]
        self.set_position(p)
        return p

    def get_identifier(self) -> str:
        return self._state["position_identifier"]
