from yaqd_core import IsDaemon, HasPosition


class Test(IsDaemon):
    _kind = "mro"


if __name__ == "__main__":
    Test.main()
