__all__ = ["UsesSerial"]


from abc import abstractmethod

import yaqd_core


class UsesSerial(yaqd_core.IsDaemon):
    @abstractmethod
    def direct_serial_write(self, message: bytes):
        raise NotImplementedError
