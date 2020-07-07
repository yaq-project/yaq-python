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
    with subprocess.Popen(["yaqd-fake-discrete-hardware", "--config", config]) as proc:
        while True:
            try:
                clients = yaqc.Client(39425)
            except ConnectionRefusedError:
                time.sleep(0.01)
            else:
                break
        yield clients
        proc.terminate()


def test_set_identifier(run_daemon):
    c = run_daemon
    for k, v in c.get_position_identifiers().items():
        c.set_identifier(k)
        time.sleep(0.1)
        assert c.get_identifier() == k
