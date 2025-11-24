from yaqd_core import IsDaemon


class ConnectionTest(IsDaemon):
    _kind = "connection-test"

    def echo(self, s: str):
        return s


if __name__ == "__main__":
    ConnectionTest.main()
