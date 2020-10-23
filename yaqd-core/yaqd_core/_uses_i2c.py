__all__ = ["UsesI2C"]


import yaqd_core


class UsesI2C(yaqd_core.UsesSerial, yaqd_core.IsDaemon):
    pass
