# type: ignore


from yaqd_core import IsDaemon, HasMeasureTrigger, IsSensor


class Test(HasMeasureTrigger, IsSensor, IsDaemon):
    _kind = "abstract"

    def _measure(self):
        return super()


if __name__ == "__main__":
    Test.main()
