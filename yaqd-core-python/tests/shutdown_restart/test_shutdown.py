import pathlib
import subprocess
import sys
import time

import pytest

import yaqc
import yaqd_core


@pytest.fixture(scope="module")
def run_daemon():
    config = pathlib.Path(__file__).parent / "shutdown.toml"
    pyfile = config.with_suffix(".py")
    with subprocess.Popen([sys.executable, pyfile, "--config", config]) as proc:
        while True:
            try:
                clients = yaqc.Client(39098), yaqc.Client(39099)
            except ConnectionRefusedError:
                time.sleep(0.01)
            else:
                break
        yield clients

        proc.terminate()


def test_shutdown(run_daemon):
    restart, shutdown = run_daemon
    assert shutdown.id()["name"] == "shutdown"
    assert restart.id()["name"] == "restart"

    shutdown.shutdown()
    with pytest.raises(ConnectionError):
        shutdown.id()


def test_restart(run_daemon):
    restart, shutdown = run_daemon
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
