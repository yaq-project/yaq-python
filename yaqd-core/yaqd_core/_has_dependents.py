__all__ = ["HasDependents"]


from abc import abstractmethod
from typing import Dict

import yaqd_core


class HasDependents(yaqd_core.IsDaemon):
    @abstractmethod
    def get_dependent_hardware(self) -> Dict[str, str]:
        raise NotImplementedError
