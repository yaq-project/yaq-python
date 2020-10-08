import pathlib
import time
import pytest

import yaqc
import yaqd_core
from yaqd_core import testing


config = pathlib.Path(__file__).parent / "shutdown.toml"
pyfile = config.with_suffix(".py")


@testing.run_daemon_from_file(pyfile, config)
def test_shutdown():
    shutdown = yaqc.Client(39099)
    assert shutdown.id()["name"] == "shutdown"

    shutdown.shutdown()
    with pytest.raises(ConnectionError):
        shutdown.id()


@testing.run_daemon_from_file(pyfile, config)
def test_restart():
    restart = yaqc.Client(39098)
    assert restart.id()["name"] == "restart"

    restart.shutdown(restart=True)
    x = 0

    def add_one():
        nonlocal x
        x += 1

    restart.register_connection_callback(add_one)
    time.sleep(0.1)
    assert restart.id()["name"] == "restart"
    assert x == 1


if __name__ == "__main__":
    test_shutdown()
    test_restart()
