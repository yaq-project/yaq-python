__all__ = ["Base"]


import yaqd_core


class Base(yaqd_core.IsDaemon):
    """Legacy class left for downstream packages that expect it. Do not use in new designs."""

    pass
