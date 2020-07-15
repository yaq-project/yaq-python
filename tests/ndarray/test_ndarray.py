import pathlib
import subprocess
import sys
import time

import numpy as np

import yaqc
from yaqd_core import testing


pyfile = pathlib.Path(__file__).parent / "NdarrayTestDaemon.py"
config = pyfile.with_suffix(".toml")


@testing.run_daemon_from_file(pyfile, config)
def test_subtract_int():
    s = yaqc.Client(38001)
    result = s.subtract(minuend=np.arange(8), subtrahend=-1 * np.arange(8))
    np.testing.assert_equal(result, np.arange(8) * 2)


@testing.run_daemon_from_file(pyfile, config)
def test_sum_float():
    s = yaqc.Client(38001)
    result = s.sum(np.linspace(0, 10))
    np.testing.assert_equal(result, np.sum(np.linspace(0, 10)))
