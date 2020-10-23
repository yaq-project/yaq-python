__all__ = ["UsesUart"]


import yaqd_core


class UsesUart(yaqd_core.UsesSerial, yaqd_core.IsDaemon):
    pass
