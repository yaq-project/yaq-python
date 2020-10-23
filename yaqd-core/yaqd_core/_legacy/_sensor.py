__all__ = ["Sensor"]


from yaqd_core import HasMeasureTrigger, IsSensor, IsDaemon


class Sensor(HasMeasureTrigger, IsSensor, IsDaemon):
    """Legacy class left for downstream packages that expect it. Do not use in new designs."""

    pass
