# type: ignore


from yaqd_core import IsDaemon, HasPosition


class Test(HasPosition, IsDaemon):
    _kind = "mro"

    def _set_position(self, position):
        super()._set_position(position)


if __name__ == "__main__":
    Test.main()
