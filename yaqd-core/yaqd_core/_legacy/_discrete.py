__all__ = ["DiscreteHardware"]


from yaqd_core import IsDiscrete, HasPosition, IsDaemon


class DiscreteHardware(IsDiscrete, HasPosition, IsDaemon):
    pass
