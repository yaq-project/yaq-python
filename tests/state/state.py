from yaqd_core import Base


class StateTest(Base):
    _kind = "state-test"

    def increment_test(self):
        self._state["test"] += 1


if __name__ == "__main__":
    StateTest.main()
