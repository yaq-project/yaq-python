import pathlib
import subprocess
import sys
import time

import numpy as np
import pytest

import yaqc

# msgpack = yaqc.msgpack


@pytest.fixture(scope="module")
def run_daemon():
    pyfile = pathlib.Path(__file__).parent / "NdarrayTestDaemon.py"
    config = pyfile.with_suffix(".toml")
    with subprocess.Popen([sys.executable, pyfile, "--config", config]) as proc:
        start = time.time()
        while True:
            print(time.time() - start)
            try:
                client = yaqc.Client(38001)
            except ConnectionRefusedError:
                if time.time() - start > 3:
                    yield None
                    proc.terminate()
                time.sleep(0.01)
            else:
                break
        print("Connection made")
        yield client
        proc.terminate()


@pytest.mark.skip
def test_subtract_int(run_daemon):
    s = run_daemon
    result = s.subtract(minuend=np.arange(8), subtrahend=-1 * np.arange(8))
    np.testing.assert_equal(result, np.arange(8) * 2)


@pytest.mark.skip
def test_sum_float(run_daemon):
    s = run_daemon
    result = s.sum(np.linspace(0, 10))
    np.testing.assert_equal(result, np.sum(np.linspace(0, 10)))
