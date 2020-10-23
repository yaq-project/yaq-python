__all__ = ["HasTurret"]


from abc import abstractmethod

import yaqd_core


class HasTurret(yaqd_core.IsDaemon):
    @abstractmethod
    def set_turret(self, index):
        self._busy = True

    def get_turret(self):
        return self._state["turret"]
