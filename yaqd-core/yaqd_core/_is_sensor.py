__all__ = ["IsSensor"]


import asyncio
import pathlib
from typing import Dict, Any, Union, Tuple, List

import yaqd_core

MeasureType = Dict[str, Union[float]]


class IsSensor(yaqd_core.IsDaemon):
    def __init__(
        self, name: str, config: Dict[str, Any], config_filepath: pathlib.Path
    ):
        super().__init__(name, config, config_filepath)
        self._measured: MeasureType = dict()  # values must be numbers or arrays
        self._channel_names: List[str] = []
        self._channel_units: Dict[str, str] = dict()
        self._channel_shapes: Dict[str, Tuple[int]] = dict()
        self._measurement_id = 0
        self._measured["measurement_id"] = self._measurement_id

    def get_channel_names(self):
        """Get current channel names."""
        return self._channel_names

    def get_channel_shapes(self):
        """Get channel shapes."""
        # as default behavior, assume all channels are scalars
        if self._channel_shapes:
            return self._channel_shapes
        return {k: () for k in self._channel_names}

    def get_channel_units(self):
        """Get channel units."""
        return self._channel_units

    def get_measured(self) -> MeasureType:
        assert "measurement_id" in self._measured
        return self._measured

    def get_measurement_id(self) -> int:
        return int(self._measured["measurement_id"])

    def get_channel_signs(self) -> Dict[str, bool]:
        return getattr(self, "_channel_signs", {n: False for n in self._channel_names})
