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
    restart = yaqc.Client(39098)
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
    time.sleep(0.1)
    start = time.time()
    while time.time() - start < 3:
        try:
            restart = yaqc.Client(39098)
            assert restart.id()["name"] == "restart"
        except (ConnectionError):
            time.sleep(0.1)
        else:
            break
    else:
        raise TimeoutError


if __name__ == "__main__":
    test_shutdown()
    test_restart()
