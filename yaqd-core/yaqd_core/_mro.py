import yaqd_core


import copy


def assert_mro(cls, avpr):
    traits = list(copy.copy(avpr["traits"]))  # no particular order
    mro = list(cls.__mro__)
    while mro:
        cls = mro.pop(0)
        if cls == yaqd_core.HasLimits:
            assert traits.pop(traits.index("has-limits"))
            assert yaqd_core.HasPosition in mro
            assert yaqd_core.IsDaemon in mro
        elif cls == yaqd_core.HasMeasureTrigger:
            assert traits.pop(traits.index("has-measure-trigger"))
            assert yaqd_core.IsSensor in mro
            assert yaqd_core.IsDaemon in mro
        elif cls == yaqd_core.HasPosition:
            assert traits.pop(traits.index("has-position"))
            assert yaqd_core.IsDaemon in mro
        elif cls == yaqd_core.HasTurret:
            assert traits.pop(traits.index("has-turret"))
            assert yaqd_core.IsDaemon in mro
        elif cls == yaqd_core.IsDaemon:
            assert traits.pop(traits.index("is-daemon"))
        elif cls == yaqd_core.IsDiscrete:
            assert traits.pop(traits.index("is-discrete"))
            assert yaqd_core.HasPosition in mro
            assert yaqd_core.IsDaemon in mro
        elif cls == yaqd_core.IsHomeable:
            assert traits.pop(traits.index("is-homeable"))
            assert yaqd_core.HasPosition in mro
            assert yaqd_core.IsDaemon in mro
        elif cls == yaqd_core.IsSensor:
            assert traits.pop(traits.index("is-sensor"))
            assert yaqd_core.IsDaemon in mro
        elif cls == yaqd_core.UsesSerial:
            assert traits.pop(traits.index("uses-serial"))
            assert yaqd_core.IsDaemon in mro
        elif cls == yaqd_core.UsesI2C:
            assert traits.pop(traits.index("uses-i2c"))
            assert yaqd_core.UsesSerial in mro
            assert yaqd_core.IsDaemon in mro
        elif cls == yaqd_core.UsesUart:
            assert traits.pop(traits.index("uses-uart"))
            assert yaqd_core.UsesSerial in mro
            assert yaqd_core.IsDaemon in mro
        else:
            pass
    if traits:  # should be empty, will enter this case if not
        raise Exception(f"I didn't find a class matching trait(s): {traits}")
