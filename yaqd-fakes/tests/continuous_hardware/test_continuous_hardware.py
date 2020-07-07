import pathlib
import subprocess
import sys
import time
import math

import pytest

import yaqc
import yaqd_core


@pytest.fixture(scope="module")
def run_daemon():
    config = pathlib.Path(__file__).parent / "config.toml"
    with subprocess.Popen(["yaqd-fake-continuous-hardware", "--config", config]) as proc:
        while True:
            try:
                clients = yaqc.Client(39424)
            except ConnectionRefusedError:
                time.sleep(0.01)
            else:
                break
        yield clients
        proc.terminate()


def test_set_position(run_daemon):
    c = run_daemon
    c.set_position(0)
    time.sleep(2)
    assert math.isclose(c.get_position(), 0)
    c.set_position(1)
    time.sleep(2)
    assert math.isclose(c.get_position(), 1)
