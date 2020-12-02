from yaqd_core import Base


class ConfigTest(Base):
    _kind = "config-test"

    def get_test(self):
        return self._config["test"]

if __name__ == "__main__":
    ConfigTest.main()
