import pathlib
import subprocess
import sys
import time
import math

import pytest

import yaqc
import yaqd_core
from yaqd_core import testing


config = pathlib.Path(__file__).parent / "config.toml"


@testing.run_daemon_entry_point("fake-continuous-hardware", config=config)
def test_set_position():
    c = yaqc.Client(39424)
    c.set_position(0)
    time.sleep(2)
    assert math.isclose(c.get_position(), 0)
    c.set_position(1)
    time.sleep(2)
    assert math.isclose(c.get_position(), 1)
