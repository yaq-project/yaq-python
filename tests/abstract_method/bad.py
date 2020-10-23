from yaqd_core import IsDaemon, HasMeasureTrigger, IsSensor


class Test(HasMeasureTrigger, IsSensor, IsDaemon):
    _kind = "abstract"


if __name__ == "__main__":
    Test.main()
