from yaqd_core import Base


class ShutdownTest(Base):
    _kind = "shutdown-test"


if __name__ == "__main__":
    ShutdownTest.main()
