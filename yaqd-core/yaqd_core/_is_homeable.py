__all__ = ["IsHomeable"]


from abc import abstractmethod

import yaqd_core


class IsHomeable(yaqd_core.HasPosition, yaqd_core.IsDaemon):
    @abstractmethod
    def home(self):
        raise NotImplementedError
