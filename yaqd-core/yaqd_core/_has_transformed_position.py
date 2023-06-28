__all__ = ["HasTransformedPosition"]


import pathlib
from typing import Dict, Any, Optional, List
from yaqd_core import HasLimits, HasPosition, IsDaemon


class HasTransformedPosition(HasLimits, HasPosition, IsDaemon):
    def __init__(
        self, name: str, config: Dict[str, Any], config_filepath: pathlib.Path
    ):
        super().__init__(name, config, config_filepath)
        self._native_units = None

    # --- conversion of coordinates ---------------------------------------------------------------

    def to_native(self, transformed_position):
        relative = self._transformed_to_relative(transformed_position)
        return relative + self._state["native_reference_position"]

    def to_transformed(self, native_position):
        relative = native_position - self._state["native_reference_position"]
        return self._relative_to_transformed(relative)

    def _relative_to_transformed(self, relative_position):
        """convert a relative coordinate to a transformed coordinate.
        Relative coordinates differ from natural coordinates in that the null position has been subtracted.
        (i.e. in relative coordinates reference position is zero).

        This placeholder function has trivial behavior, f(x) = x.
        Daemons that need more than a reference_position should override this method.
        Note that override should still obey inversion:
        ```
        _relative_to_transformed(_transformed_to_relative(x)) == x
        ```.
        """
        return relative_position

    def _transformed_to_relative(self, transformed_position):
        """convert a transformed coordinate to a relative coordinate
        Relative coordinates differ from natural coordinates in that the null position has been subtracted.
        (i.e. in relative coordinates reference position is zero).

        This placeholder function has trivial behavior, f(x) = x.
        Daemons that need more than a reference_position should override this method.
        Note that override should still obey inversion:
        ```
        _relative_to_transformed(_transformed_to_relative(x)) == x
        ```.
        """
        return transformed_position

    # --- wrap parent messages that deal with position --------------------------------------------
    # --- clients use transformed position, but parent messages except/return native position.

    def set_position(self, position: float) -> None:
        super().set_position(self.to_native(position))

    def set_relative(self, distance: float) -> float:
        new = self.to_transformed(self._state["destination"]) + distance
        self.set_position(new)
        return new

    def get_position(self) -> float:
        position = super().get_position()
        return self.to_transformed(position)

    def get_destination(self) -> float:
        return self.to_transformed(super().get_destination())

    def in_limits(self, position: float) -> bool:
        return super().in_limits(self.to_native(position))

    def get_limits(self) -> List[float]:
        return sorted(map(self.to_transformed, self.limits))

    # --- setting or returning native coordinates -------------------------------------------------
    # --- new messages introduce by this trait

    @property
    def limits(self) -> List[float]:
        return self._joint_limit(
            self._state["hw_limits"],
            sorted(map(self.to_native, self._config["limits"])),
            self._config["native_limits"],
        )

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
        return self.limits

    def get_native_units(self) -> Optional[str]:
        return self._native_units
