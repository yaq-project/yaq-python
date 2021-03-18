__all__ = ["HasTurret"]


from abc import abstractmethod

import yaqd_core


class HasTurret(yaqd_core.IsDaemon):
    @abstractmethod
    def set_turret(self, identifier: str):
        self._busy = True

    @abstractmethod
    def get_turret_options(self):
        ...

    def get_turret(self):
        return self._state["turret"]
