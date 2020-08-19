#! /usr/bin/env python3
import pathlib
from typing import Dict, Any

from ._base import Hardware

__all__ = ["DiscreteHardware"]


class DiscreteHardware(Hardware):
    _kind: str = "discrete-hardware"

    def __init__(self, name: str, config: Dict[str, Any], config_filepath: pathlib.Path):
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
