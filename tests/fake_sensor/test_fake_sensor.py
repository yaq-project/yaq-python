import pathlib
import subprocess
import sys
import time
import math
import numpy as np

import pytest

import yaqc
import yaqd_core
from yaqd_core import testing


config = pathlib.Path(__file__).parent / "config.toml"


@testing.run_daemon_entry_point("fake-sensor", config=config)
def test_keys():
    c = yaqc.Client(39426)
    assert "random_walk" in c.get_measured()
    assert "measurement_id" in c.get_measured()


@testing.run_daemon_entry_point("fake-sensor", config=config)
def test_measurement_id():
    c = yaqc.Client(39426)
    time.sleep(0.2)
    first = c.get_measurement_id()
    time.sleep(0.2)
    second = c.get_measurement_id()
    assert isinstance(first, int)
    assert isinstance(second, int)
    assert second > first


if __name__ == "__main__":
    test_keys()
    test_measurement_id()
