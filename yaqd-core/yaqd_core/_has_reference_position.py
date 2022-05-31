__all__ = ["HasReferencePosition"]


import pathlib
from typing import Dict, Any, Optional, List

from yaqd_core import HasLimits, HasPosition, IsDaemon


class HasReferencePosition(HasLimits, HasPosition, IsDaemon):
    def __init__(
        self, name: str, config: Dict[str, Any], config_filepath: pathlib.Path
    ):
        super().__init__(name, config, config_filepath)

    def set_position(self, position: float) -> None:
        super().set_position(self, self._to_absolute(position))

    def get_position(self) -> float:
        return self._to_reference(self._state["position"])

    def get_destination(self) -> float:
        return self._to_reference(self._state["destination"])

    def get_reference_position(self) -> float:
        return self._state["reference_position"]

    def set_reference_position(self, reference):
        old_reference = self._state["reference_position"]
        reference_change = reference - old_reference
        self._state["reference_position"] = reference

    def in_limits(self, position: float) -> bool:
        return super().in_limits(self._to_absolute(position))

    def get_limits(self) -> List[float]:
        return [lim - self._state["reference_position"] for lim in super().get_limits()]
