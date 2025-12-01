from yaqd_core import Base


class ConnectionTest(Base):
    _kind = "connection-test"

    def echo(self, s: str):
        return s


if __name__ == "__main__":
    ConnectionTest.main()
