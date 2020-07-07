#! /usr/bin/env python3
import pathlib
from typing import Dict, Any, Sequence, Tuple, Union, Optional

from ._base import Hardware

__all__ = ["DiscreteHardware"]


class DiscreteHardware(Hardware):
    _kind: str = "discrete-hardware"

    def __init__(
        self, name: str, config: Dict[str, Any], config_filepath: pathlib.Path
    ):
        self._position_identifiers: Dict[str, Any] = config.get("identifiers", {})
        super().__init__(name, config, config_filepath)

    def get_position_identifiers(self):
        return self._position_identifiers

    def set_identifier(self, identifier):
        p = self._position_identifiers[identifier]
        self.set_position(p)
        return p

    def get_identifier(self):
        return self._state["position_identifier"]
