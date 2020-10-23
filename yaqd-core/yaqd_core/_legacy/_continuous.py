__all__ = ["ContinuousHardware"]


from yaqd_core import HasLimits, HasPosition, IsDaemon


class ContinuousHardware(HasLimits, HasPosition, IsDaemon):
    """Legacy class left for downstream packages that expect it. Do not use in new designs."""

    pass
