__all__ = ["HasMapping"]


import asyncio
import pathlib
from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod

from yaqd_core import IsSensor, IsDaemon


class HasMapping(IsSensor, IsDaemon, ABC):
    def __init__(
        self, name: str, config: Dict[str, Any], config_filepath: pathlib.Path
    ):
        super().__init__(name, config, config_filepath)
        self.__mappings: Dict[
            str, Any
        ] = dict()  # don't interact directly, use property
        self._mapping_id: int = 0
        self._channel_mappings: Dict[str, List[str]] = dict()
        self._mapping_units: Dict[str, str] = dict()
        self._mappings: Dict[str, object] = dict()

    @property
    def _mappings(self) -> Dict[str, Any]:
        return self.__mapped

    @_mappings.setter
    def _mappings(self, new):
        self.__mapped = new
        self._mapping_id += 1
        self.__mapped["mapping_id"] = self._mapping_id

    def get_channel_mappings(self) -> Dict[str, List[str]]:
        return self._channel_mappings

    def get_mapping_id(self) -> int:
        return self._mapping_id

    def get_mapping_units(self) -> Dict[str, str]:
        return self._mapping_units

    def get_mappings(self) -> Dict[str, object]:
        return self._mappings
