__all__ = ["HasTransformedPosition"]


import pathlib
from typing import Dict, Any, Optional, List
from abc import abstractmethod

from yaqd_core import HasLimits, HasPosition, IsDaemon


class HasTransformedPosition(HasLimits, HasPosition, IsDaemon):
    def __init__(
        self, name: str, config: Dict[str, Any], config_filepath: pathlib.Path
    ):
        super().__init__(name, config, config_filepath)

    # --- conversion of coordinates ---------------------------------------------------------------

    def to_native(self, transformed_position):
        relative = self._transformed_to_relative(transformed_position)
        return relative + self._state["native_reference_position"]

    def to_transformed(self, native_position):
        relative = native_position - self._state["native_reference_position"]
        return self._relative_to_transformed(self, relative)

    @abstractmethod
    def _relative_to_transformed(self, relative_position):
        """convert a relative coordinate to a transformed coordinate.
        Relative coordinates differ from natural coordinates in that the null position has been subtracted.
        (i.e. in relative coordinates reference position is zero).
        The inverse function of `_transformed_to_relative`.

        If you needo only an offset, return relative_position
        """
        raise NotImplementedError

    @abstractmethod
    def _transformed_to_relative(self, transformed_position):
        """convert a transformed coordinate to a relative coordinate
        Relative coordinates differ from natural coordinates in that the null position has been subtracted.
        (i.e. in relative coordinates reference position is zero).
        The inverse function of `_relative_to_transformed`

        If you need only an offset, return transformed_position
        """
        raise NotImplementedError

    # --- methods for transformed positions -------------------------------------------------------

    def set_position(self, position: float) -> None:
        super().set_position(self.to_native(position))

    def get_position(self) -> float:
        return self.to_transformed(self._state["position"])

    def get_destination(self) -> float:
        return self.to_transformed(self._state["destination"])

    def in_limits(self, position: float) -> bool:
        return super().in_limits(self.to_native(position))

    def get_limits(self) -> List[float]:
        return [self.to_transformed(lim) for lim in super().get_limits()]

    # --- native properties -----------------------------------------------------------------------

    def get_native_reference(self) -> float:
        return self._state["native_reference_position"]

    def set_native_reference(self, native_position):
        self._state["native_reference_position"] = native_position

    def set_native_position(self, native_position):
        super().set_position(native_position)

    def get_native_position(self) -> float:
        return self._state["position"]

    def get_native_destination(self) -> float:
        return self._state["destination"]

    def get_native_limits(self) -> List[float]:
        return super().get_limits()

    @abstractmethod
    def get_native_units(self) -> str:
        raise NotImplementedError
